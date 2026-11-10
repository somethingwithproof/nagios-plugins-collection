# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""One HTTP client policy for every plugin.

:func:`add_http_arguments` registers the shared options and :func:`client` /
:func:`async_client` build clients from them, so TLS trust, client
certificates, authentication, timeouts, retries, proxies and the User-Agent
behave the same in every check:

* Certificates are verified against the system bundle (or ``SSL_CERT_FILE``)
  unless ``--ca-file`` names a private CA; ``--insecure`` disables
  verification and logs a warning on every run.
* ``--client-cert``/``--client-key`` present a TLS client certificate.
* ``--username``/``--password``, ``--bearer-token`` and ``--api-key`` read
  secrets from the flag, a ``-file`` option, ``$PREFIX_NAME`` or
  ``$PREFIX_NAME_FILE``.
* Proxies come from ``HTTP_PROXY``, ``HTTPS_PROXY``, ``ALL_PROXY`` and
  ``NO_PROXY``.
* Retries are bounded, back off exponentially and fit inside the run's
  ``--timeout``. A connection that was never established is retried for any
  method; a response of 502/503/504 or an error after the request was sent is
  retried only for idempotent methods.
* A response body is read up to ``--max-response-bytes`` (10 MiB by default,
  after decompression); a larger one raises :class:`ResponseTooLarge`, which
  the plugin runner reports as UNKNOWN.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import logging
import ssl
import time
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlsplit

import httpx

from nagios_plugins import __version__
from nagios_plugins.base import NagiosArgumentParser, UnknownResult
from nagios_plugins.deadline import remaining_time
from nagios_plugins.redaction import register_secret

logger = logging.getLogger(__name__)

#: Methods whose repetition has no additional effect (RFC 9110 section 9.2.2).
IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE", "TRACE"})
#: Gateway responses that usually clear on a second attempt.
RETRY_STATUSES = frozenset({502, 503, 504})
#: Failures before the request reached the server, so any method may be retried.
_NOT_SENT = (httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout)
#: Upper bound for one backoff pause in seconds.
MAX_BACKOFF = 5.0
#: An attempt with less time than this left is not started.
MIN_ATTEMPT = 0.5
#: Default ``--max-response-bytes``: far above any status document a check reads.
MAX_RESPONSE_BYTES = 10 * 1024 * 1024


class ResponseTooLarge(UnknownResult):
    """A response body exceeded the configured size; the answer cannot be judged."""

    def __init__(self, url: httpx.URL, limit: int) -> None:
        """Name the URL (without credentials or query) and the limit."""
        super().__init__(
            f"Response from {safe_url(url)} is larger than {limit} bytes "
            "(raise --max-response-bytes if this is expected)"
        )


def _decoded_copy(response: httpx.Response, body: bytes) -> httpx.Response:
    """Return an already-read copy of ``response`` holding the decoded ``body``."""
    headers = httpx.Headers(response.headers)
    headers.pop("content-encoding", None)
    headers["content-length"] = str(len(body))
    copy = httpx.Response(
        response.status_code,
        headers=headers,
        content=body,
        request=response.request,
        extensions=response.extensions,
        history=response.history,
        default_encoding=response.default_encoding,
    )
    copy.elapsed = response.elapsed
    copy.next_request = response.next_request
    return copy


def _check_size(response: httpx.Response, size: int, limit: int) -> None:
    """Raise :class:`ResponseTooLarge` once ``size`` decoded bytes exceed ``limit``."""
    if size > limit:
        raise ResponseTooLarge(response.request.url, limit)


def read_bounded(response: httpx.Response, limit: int) -> httpx.Response:
    """Read a streamed response, decoding at most ``limit`` bytes, and close it.

    Raises:
        ResponseTooLarge: The decoded body is larger than ``limit``.
    """
    chunks: list[bytes] = []
    size = 0
    try:
        for chunk in response.iter_bytes():
            size += len(chunk)
            _check_size(response, size, limit)
            chunks.append(chunk)
    finally:
        response.close()
    return _decoded_copy(response, b"".join(chunks))


async def aread_bounded(response: httpx.Response, limit: int) -> httpx.Response:
    """Asynchronous :func:`read_bounded`."""
    chunks: list[bytes] = []
    size = 0
    try:
        async for chunk in response.aiter_bytes():
            size += len(chunk)
            _check_size(response, size, limit)
            chunks.append(chunk)
    finally:
        await response.aclose()
    return _decoded_copy(response, b"".join(chunks))


@dataclass(frozen=True)
class RetryPolicy:
    """How often and how patiently to repeat a failed request.

    Args:
        retries: Additional attempts after the first.
        delay: The first pause in seconds; each further pause doubles it.
    """

    retries: int = 0
    delay: float = 0.5

    def backoff(self, attempt: int) -> float:
        """Return the pause before retry number ``attempt`` (0-based)."""
        return min(self.delay * 2.0**attempt, MAX_BACKOFF)

    def retryable(
        self,
        request: httpx.Request,
        error: Exception | None = None,
        response: httpx.Response | None = None,
    ) -> bool:
        """Return whether this outcome is transient and safe to repeat."""
        if isinstance(error, _NOT_SENT):
            return True
        idempotent = request.method in IDEMPOTENT_METHODS
        if error is not None:
            return idempotent and isinstance(error, httpx.TransportError)
        return idempotent and response is not None and response.status_code in RETRY_STATUSES

    def pause(self, attempt: int) -> float | None:
        """Return the pause before the next attempt, or None when it would not fit."""
        delay = self.backoff(attempt)
        budget = remaining_time()
        if attempt >= self.retries or (budget is not None and budget < delay + MIN_ATTEMPT):
            return None
        return delay

    def next_pause(
        self,
        request: httpx.Request,
        attempt: int,
        *,
        error: Exception | None = None,
        response: httpx.Response | None = None,
    ) -> float | None:
        """Return how long to wait before repeating ``request``, or None to stop."""
        if not self.retryable(request, error=error, response=response):
            return None
        delay = self.pause(attempt)
        if delay is not None:
            logger.info("Retrying %s %s in %.1fs", request.method, safe_url(request.url), delay)
        return delay


def _bounded_timeout(request: httpx.Request, configured: dict[str, float | None]) -> None:
    """Shrink each timeout phase of ``request`` to what is left of the run."""
    budget = remaining_time()
    if budget is None:
        return
    request.extensions["timeout"] = {
        phase: budget if value is None else min(value, budget)
        for phase, value in configured.items()
    }


Origin = tuple[str, str, int | None]
#: Request extension holding the origin credentials were configured for.
_ORIGIN = "nagios_plugins.credential_origin"


def origin(url: httpx.URL) -> Origin:
    """Return the (scheme, host, port) a credential is bound to, with default ports."""
    return url.scheme, url.host, url.port or {"http": 80, "https": 443}.get(url.scheme)


def _basic(username: str, password: str) -> str:
    """Return an HTTP basic ``Authorization`` value (RFC 7617, UTF-8)."""
    pair = f"{username}:{password}".encode()
    return f"Basic {base64.b64encode(pair).decode('ascii')}"


class InsecureRedirect(httpx.RequestError):
    """A redirect would send a credentialed request from HTTPS to plain HTTP."""


class OriginAuth(httpx.Auth):
    """Attach credentials only to requests for the origin they were configured for.

    httpx copies every header except ``Authorization`` onto a redirect, so an
    API key in a client default header would reach any host a server
    redirects to. This flow runs on every hop the shared clients send (they
    follow redirects themselves) and both adds the credentials for the
    original origin and removes them everywhere else.
    """

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        bearer_token: str | None = None,
        api_key: str | None = None,
        api_key_header: str = "X-API-Key",
    ) -> None:
        """Hold the credentials; at most one of basic or bearer sets Authorization."""
        self._headers: dict[str, str] = {}
        if username:
            self._headers["Authorization"] = _basic(username, password or "")
        if bearer_token:
            self._headers["Authorization"] = f"Bearer {bearer_token}"
        if api_key:
            self._headers[api_key_header] = api_key

    def __bool__(self) -> bool:
        """Whether any credential is configured."""
        return bool(self._headers)

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Add or strip the credential headers for this hop.

        Without configured basic or bearer credentials, user information in the
        first URL (``https://user:pass@host``) is used, as httpx itself would.
        """
        bound = request.extensions.setdefault(_ORIGIN, origin(request.url))
        same_origin = bound == origin(request.url)
        headers = dict(self._headers)
        if "Authorization" not in headers and request.url.username:
            headers["Authorization"] = _basic(request.url.username, request.url.password or "")
        for name, value in headers.items():
            if same_origin:
                request.headers[name] = value
            else:
                request.headers.pop(name, None)
        yield request


@dataclass
class _Hops:
    """Redirect bookkeeping shared by the sync and async clients."""

    follow: bool
    limit: int
    credentials: bool
    history: list[httpx.Response] = field(default_factory=list)

    def next(self, request: httpx.Request, response: httpx.Response) -> httpx.Request | None:
        """Return the next hop to send, or None when ``response`` is the answer.

        Raises:
            InsecureRedirect: A credentialed HTTPS request redirects to HTTP.
            httpx.TooManyRedirects: More hops than the client allows.
        """
        response.history = list(self.history)
        self.credentials = self.credentials or bool(request.url.userinfo)
        following = response.next_request
        if not self.follow or following is None:
            return None
        if self.credentials and request.url.scheme == "https" and following.url.scheme == "http":
            raise InsecureRedirect(
                f"refusing to follow a redirect from HTTPS to {safe_url(following.url)} "
                "with credentials configured",
                request=request,
            )
        self.history.append(response)
        if len(self.history) > self.limit:
            raise httpx.TooManyRedirects("Exceeded maximum allowed redirects.", request=request)
        return following


def _hops(client: httpx.Client | httpx.AsyncClient, kwargs: dict[str, Any]) -> _Hops:
    """Take the redirect choice from ``kwargs`` so each hop is sent on its own."""
    follow = kwargs.pop("follow_redirects", httpx.USE_CLIENT_DEFAULT)
    if follow is httpx.USE_CLIENT_DEFAULT:
        follow = client.follow_redirects
    auth = kwargs.get("auth", httpx.USE_CLIENT_DEFAULT)
    if auth is httpx.USE_CLIENT_DEFAULT:
        auth = client.auth
    return _Hops(bool(follow), client.max_redirects, bool(auth))


class RetryingClient(httpx.Client):
    """An :class:`httpx.Client` with origin-bound credentials and a :class:`RetryPolicy`.

    Redirects are followed one hop at a time so :class:`OriginAuth` sees each.
    Unless the caller streams, the body is read up to ``max_response_bytes``.
    """

    def __init__(
        self, *, retry: RetryPolicy, max_response_bytes: int = MAX_RESPONSE_BYTES, **kwargs: Any
    ) -> None:
        """Create the client; ``kwargs`` are passed to :class:`httpx.Client`."""
        super().__init__(**kwargs)
        self.retry = retry
        self.max_response_bytes = max_response_bytes

    def send(self, request: httpx.Request, **kwargs: Any) -> httpx.Response:
        """Send ``request`` and its redirects, retrying transient failures."""
        stream = kwargs.pop("stream", False)
        hops = _hops(self, kwargs)
        while True:
            response = self._attempts(request, **kwargs)
            following = hops.next(request, response)
            if following is None:
                return response if stream else read_bounded(response, self.max_response_bytes)
            response.close()
            request = following

    def _attempts(self, request: httpx.Request, **kwargs: Any) -> httpx.Response:
        """Send one hop, repeating transient failures the policy allows."""
        configured = dict(request.extensions.get("timeout") or self.timeout.as_dict())
        attempt = 0
        while True:
            _bounded_timeout(request, configured)
            try:
                response = super().send(request, follow_redirects=False, stream=True, **kwargs)
            except httpx.TransportError as error:
                if (delay := self.retry.next_pause(request, attempt, error=error)) is None:
                    raise
            else:
                if (delay := self.retry.next_pause(request, attempt, response=response)) is None:
                    return response
                response.close()
            time.sleep(delay)
            attempt += 1


class RetryingAsyncClient(httpx.AsyncClient):
    """An :class:`httpx.AsyncClient` with origin-bound credentials and a :class:`RetryPolicy`."""

    def __init__(
        self, *, retry: RetryPolicy, max_response_bytes: int = MAX_RESPONSE_BYTES, **kwargs: Any
    ) -> None:
        """Create the client; ``kwargs`` are passed to :class:`httpx.AsyncClient`."""
        super().__init__(**kwargs)
        self.retry = retry
        self.max_response_bytes = max_response_bytes

    async def send(self, request: httpx.Request, **kwargs: Any) -> httpx.Response:
        """Send ``request`` and its redirects, retrying transient failures."""
        stream = kwargs.pop("stream", False)
        hops = _hops(self, kwargs)
        while True:
            response = await self._attempts(request, **kwargs)
            following = hops.next(request, response)
            if following is None:
                if stream:
                    return response
                return await aread_bounded(response, self.max_response_bytes)
            await response.aclose()
            request = following

    async def _attempts(self, request: httpx.Request, **kwargs: Any) -> httpx.Response:
        """Send one hop, repeating transient failures the policy allows."""
        configured = dict(request.extensions.get("timeout") or self.timeout.as_dict())
        attempt = 0
        while True:
            _bounded_timeout(request, configured)
            try:
                response = await super().send(
                    request, follow_redirects=False, stream=True, **kwargs
                )
            except httpx.TransportError as error:
                if (delay := self.retry.next_pause(request, attempt, error=error)) is None:
                    raise
            else:
                if (delay := self.retry.next_pause(request, attempt, response=response)) is None:
                    return response
                await response.aclose()
            await asyncio.sleep(delay)
            attempt += 1


@dataclass(frozen=True)
class HttpSettings:
    """Everything a plugin's HTTP client needs, resolved from its options."""

    timeout: float = 10.0
    ca_file: str | None = None
    insecure: bool = False
    client_cert: str | None = None
    client_key: str | None = None
    retry: RetryPolicy = field(default_factory=RetryPolicy)
    username: str | None = None
    password: str | None = None
    bearer_token: str | None = None
    api_key: str | None = None
    api_key_header: str = "X-API-Key"
    user_agent: str = f"nagios-plugins-collection/{__version__}"
    max_response_bytes: int = MAX_RESPONSE_BYTES

    def __post_init__(self) -> None:
        """Mask the credentials in all output, however the settings were built."""
        for secret in (self.password, self.bearer_token, self.api_key):
            register_secret(secret)

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> HttpSettings:
        """Read the options registered by :func:`add_http_arguments`."""
        return cls(
            timeout=args.timeout,
            ca_file=getattr(args, "ca_file", None),
            insecure=getattr(args, "insecure", False),
            client_cert=getattr(args, "client_cert", None),
            client_key=getattr(args, "client_key", None),
            retry=RetryPolicy(getattr(args, "retries", 0), getattr(args, "retry_delay", 0.5)),
            username=getattr(args, "username", None),
            password=getattr(args, "password", None),
            bearer_token=getattr(args, "bearer_token", None),
            api_key=getattr(args, "api_key", None),
            api_key_header=getattr(args, "api_key_header", "X-API-Key"),
            user_agent=getattr(args, "http_user_agent", cls.user_agent),
            max_response_bytes=getattr(args, "max_response_bytes", MAX_RESPONSE_BYTES),
        )

    def ssl_context(self) -> ssl.SSLContext:
        """Build the TLS context for trust, verification and the client certificate."""
        if self.insecure:
            logger.warning("--insecure: TLS certificates and hostnames are not verified")
            context = httpx.create_ssl_context(verify=False)
        elif self.ca_file:
            context = ssl.create_default_context(cafile=self.ca_file)
        else:
            context = httpx.create_ssl_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        if self.client_cert:
            context.load_cert_chain(self.client_cert, self.client_key)
        return context

    def auth(self) -> OriginAuth:
        """Return the credentials, bound to the origin of each request's first hop."""
        return OriginAuth(
            username=self.username,
            password=self.password,
            bearer_token=self.bearer_token,
            api_key=self.api_key,
            api_key_header=self.api_key_header,
        )

    def client_options(self) -> dict[str, Any]:
        """Return keyword arguments shared by the sync and async clients."""
        return {
            "timeout": httpx.Timeout(self.timeout),
            "verify": self.ssl_context(),
            "headers": {"User-Agent": self.user_agent},
            "auth": self.auth(),
            "trust_env": True,
        }


def client(settings: HttpSettings | argparse.Namespace, **kwargs: Any) -> RetryingClient:
    """Return a synchronous client configured by ``settings`` or parsed options.

    ``kwargs`` (for example ``follow_redirects=True``) override the defaults.
    """
    resolved = _settings(settings)
    return RetryingClient(
        retry=resolved.retry,
        max_response_bytes=resolved.max_response_bytes,
        **{**resolved.client_options(), **kwargs},
    )


def async_client(settings: HttpSettings | argparse.Namespace, **kwargs: Any) -> RetryingAsyncClient:
    """Return an asynchronous client configured by ``settings`` or parsed options."""
    resolved = _settings(settings)
    return RetryingAsyncClient(
        retry=resolved.retry,
        max_response_bytes=resolved.max_response_bytes,
        **{**resolved.client_options(), **kwargs},
    )


def _settings(settings: HttpSettings | argparse.Namespace) -> HttpSettings:
    """Accept either resolved settings or a parsed namespace."""
    return settings if isinstance(settings, HttpSettings) else HttpSettings.from_args(settings)


def safe_url(url: httpx.URL | str) -> str:
    """Return ``url`` without credentials, query string or fragment, for messages."""
    parts = urlsplit(str(url))
    host = parts.hostname or ""
    if ":" in host:
        host = f"[{host}]"
    if parts.port:
        host += f":{parts.port}"
    userinfo = "***@" if parts.username or parts.password else ""
    return f"{parts.scheme}://{userinfo}{host}{parts.path}"


def describe_error(error: httpx.HTTPError) -> str:
    """Describe an HTTP failure without the request's credentials or query string."""
    try:
        target = safe_url(error.request.url)
    except RuntimeError:  # no request attached
        return str(error) or type(error).__name__
    if isinstance(error, httpx.HTTPStatusError):
        response = error.response
        return f"HTTP {response.status_code} {response.reason_phrase} from {target}".strip()
    if isinstance(error, httpx.TimeoutException):
        return f"timed out ({type(error).__name__}) requesting {target}"
    reason = str(error) or type(error).__name__
    return f"{reason} requesting {target}"


def add_tls_arguments(
    parser: argparse.ArgumentParser, *, insecure: bool = True, client_cert: bool = True
) -> None:
    """Register ``--ca-file`` and, unless disabled, ``--insecure`` and client certificates."""
    group = parser.add_argument_group("TLS")
    # Accepted for compatibility with 1.x command definitions; verification is always on.
    group.add_argument("--verify-ssl", action="store_true", default=True, help=argparse.SUPPRESS)
    group.add_argument(
        "--ca-file",
        metavar="PATH",
        help="PEM CA bundle (default: the bundled Mozilla CA store or $SSL_CERT_FILE)",
    )
    if insecure:
        group.add_argument(
            "--insecure",
            action="store_true",
            help="Do not verify TLS certificates or hostnames (for testing; prefer --ca-file)",
        )
    if client_cert:
        group.add_argument(
            "--client-cert", metavar="PATH", help="PEM client certificate for mutual TLS"
        )
        group.add_argument(
            "--client-key",
            metavar="PATH",
            help="PEM private key for --client-cert (when not in the same file)",
        )
    if isinstance(parser, NagiosArgumentParser):
        parser.add_validator(_check_tls)


def _check_tls(args: argparse.Namespace) -> str | None:
    """Reject TLS option combinations that cannot mean what they say."""
    if getattr(args, "insecure", False) and args.ca_file:
        return "--insecure and --ca-file are mutually exclusive"
    if getattr(args, "client_key", None) and not getattr(args, "client_cert", None):
        return "--client-key requires --client-cert"
    return None


def add_http_arguments(
    parser: NagiosArgumentParser,
    *,
    env_prefix: str,
    auth: bool = True,
    retries: int | None = 2,
    retry_delay: float = 0.5,
) -> None:
    """Register the shared HTTP options on a plugin's parser.

    Args:
        parser: The plugin's parser.
        env_prefix: Prefix of the credential environment variables, for example
            ``CHECK_PROMETHEUS_QUERY`` for ``$CHECK_PROMETHEUS_QUERY_BEARER_TOKEN``.
        auth: Whether to register the authentication options.
        retries: Default ``--retries``; None registers no retry options and
            never retries, for checks that measure every attempt.
        retry_delay: Default ``--retry-delay`` in seconds.
    """
    add_tls_arguments(parser)
    parser.set_defaults(http_user_agent=f"nagios-plugins-collection/{__version__} ({parser.prog})")
    parser.add_argument(
        "--max-response-bytes",
        type=_positive_bytes,
        default=MAX_RESPONSE_BYTES,
        metavar="BYTES",
        help="Largest response body read, after decompression; a larger one is UNKNOWN "
        f"(default: {MAX_RESPONSE_BYTES})",
    )
    if retries is not None:
        group = parser.add_argument_group("HTTP retries")
        group.add_argument(
            "--retries",
            type=int,
            default=retries,
            help=f"Retries for transient failures within --timeout (default: {retries})",
        )
        group.add_argument(
            "--retry-delay",
            type=float,
            default=retry_delay,
            metavar="SECONDS",
            help=f"First retry pause, doubled for each retry (default: {retry_delay})",
        )
        parser.add_validator(_check_retries)
    if auth:
        add_auth_arguments(parser, env_prefix)


def _positive_bytes(text: str) -> int:
    """Parse ``--max-response-bytes``: a whole number of bytes, at least 1."""
    try:
        value = int(text)
    except ValueError:
        value = 0
    if value < 1:
        raise argparse.ArgumentTypeError(f"expected a positive number of bytes: {text!r}")
    return value


def _check_retries(args: argparse.Namespace) -> str | None:
    """Retries and pauses cannot be negative."""
    if args.retries < 0 or args.retry_delay < 0:
        return "--retries and --retry-delay must not be negative"
    return None


def add_auth_arguments(parser: NagiosArgumentParser, env_prefix: str) -> None:
    """Register basic, bearer and API-key authentication with secret sources."""
    group = parser.add_argument_group("HTTP authentication")
    group.add_argument("--username", help="User name for HTTP basic authentication")
    parser.add_secret_argument(
        "--password",
        env=f"{env_prefix}_PASSWORD",
        help="password for HTTP basic authentication",
        container=group,
    )
    parser.add_secret_argument(
        "--bearer-token",
        env=f"{env_prefix}_BEARER_TOKEN",
        help="bearer token sent in the Authorization header",
        container=group,
    )
    parser.add_secret_argument(
        "--api-key",
        env=f"{env_prefix}_API_KEY",
        help="API key sent in the --api-key-header header",
        container=group,
    )
    group.add_argument(
        "--api-key-header",
        default="X-API-Key",
        metavar="NAME",
        help="Header that carries --api-key (default: X-API-Key)",
    )
    parser.add_validator(_check_auth)


def _check_auth(args: argparse.Namespace) -> str | None:
    """Basic and bearer authentication both use the Authorization header."""
    if args.bearer_token and args.username:
        return "--bearer-token and --username both set the Authorization header; pass one"
    if args.password and not args.username:
        return "--password requires --username"
    if args.api_key and args.bearer_token and args.api_key_header.lower() == "authorization":
        return "--api-key-header Authorization conflicts with --bearer-token"
    return None
