# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""The shared HTTP client: credentials, redirects, retries, proxies and options."""

import base64
import logging
import time
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins import __version__
from nagios_plugins.base import NagiosArgumentParser
from nagios_plugins.deadline import Deadline
from nagios_plugins.services import http
from tests.fakes import FakeHttpBackend

API_KEY = "k3y-value"
TOKEN = "t0ken-value"
BASIC = "Basic " + base64.b64encode(b"monitor:pa55").decode()
CREDENTIALS = {
    "api-key": (http.HttpSettings(api_key=API_KEY), "X-API-Key", API_KEY),
    "bearer": (http.HttpSettings(bearer_token=TOKEN), "Authorization", f"Bearer {TOKEN}"),
    "basic": (http.HttpSettings(username="monitor", password="pa55"), "Authorization", BASIC),
}


def _redirect(location: str) -> httpx.Response:
    return httpx.Response(302, headers={"Location": location})


async def _get(settings: http.HttpSettings, url: str, *, use_async: bool) -> httpx.Response:
    if use_async:
        async with http.async_client(settings, follow_redirects=True) as client:
            return await client.get(url)
    with http.client(settings, follow_redirects=True) as client:
        return client.get(url)


@pytest.mark.asyncio
@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("kind", CREDENTIALS)
@pytest.mark.parametrize(
    "location",
    ["https://elsewhere.example/landing", "https://api.example:8443/landing"],
    ids=["other-host", "other-port"],
)
async def test_credentials_are_dropped_on_cross_origin_redirects(
    http_backend: FakeHttpBackend, kind: str, location: str, use_async: bool
) -> None:
    settings, header, value = CREDENTIALS[kind]
    http_backend.reply(_redirect(location), httpx.Response(200))
    response = await _get(settings, "https://api.example/start", use_async=use_async)
    first, second = http_backend.requests
    assert first.headers[header] == value
    assert str(second.url) == location
    assert header not in second.headers
    assert response.status_code == 200
    assert len(response.history) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("kind", CREDENTIALS)
async def test_credentials_follow_same_origin_redirects(
    http_backend: FakeHttpBackend, kind: str, use_async: bool
) -> None:
    settings, header, value = CREDENTIALS[kind]
    http_backend.reply(
        _redirect("/v2/start"), _redirect("https://api.example:443/v3"), httpx.Response(200)
    )
    await _get(settings, "https://api.example/start", use_async=use_async)
    assert [r.headers.get(header) for r in http_backend.requests] == [value] * 3


@pytest.mark.asyncio
@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("kind", CREDENTIALS)
async def test_https_to_http_redirect_is_refused_with_credentials(
    http_backend: FakeHttpBackend, kind: str, use_async: bool
) -> None:
    settings, _, _ = CREDENTIALS[kind]
    http_backend.reply(_redirect("http://api.example/start"), httpx.Response(200))
    with pytest.raises(http.InsecureRedirect, match="HTTPS to http://api.example/start"):
        await _get(settings, "https://api.example/start", use_async=use_async)
    assert len(http_backend.requests) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
async def test_downgrade_redirect_without_credentials_is_followed(
    http_backend: FakeHttpBackend, use_async: bool
) -> None:
    http_backend.reply(_redirect("http://www.example/"), httpx.Response(200))
    response = await _get(http.HttpSettings(), "https://www.example/", use_async=use_async)
    assert response.status_code == 200
    assert len(http_backend.requests) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
async def test_url_userinfo_is_basic_auth_bound_to_its_origin(
    http_backend: FakeHttpBackend, use_async: bool
) -> None:
    http_backend.reply(_redirect("https://elsewhere.example/"), httpx.Response(200))
    await _get(http.HttpSettings(), "https://monitor:pa55@api.example/", use_async=use_async)
    first, second = http_backend.requests
    assert first.headers["Authorization"] == BASIC
    assert "Authorization" not in second.headers
    http_backend.requests.clear()
    http_backend.reply(_redirect("http://api.example/"))
    with pytest.raises(http.InsecureRedirect):
        await _get(http.HttpSettings(), "https://monitor:pa55@api.example/", use_async=use_async)


def test_redirect_limit_is_enforced(http_backend: FakeHttpBackend) -> None:
    http_backend.reply(_redirect("/again"))
    with (
        http.client(http.HttpSettings(), follow_redirects=True, max_redirects=3) as client,
        pytest.raises(httpx.TooManyRedirects),
    ):
        client.get("https://loop.example/")
    assert len(http_backend.requests) == 4


def test_redirects_are_not_followed_unless_asked(http_backend: FakeHttpBackend) -> None:
    http_backend.reply(_redirect("/elsewhere"))
    with http.client(http.HttpSettings()) as client:
        response = client.get("https://site.example/")
    assert response.status_code == 302
    assert response.next_request is not None
    assert len(http_backend.requests) == 1


def _settings(retries: int) -> http.HttpSettings:
    return http.HttpSettings(retry=http.RetryPolicy(retries=retries, delay=0.01))


@pytest.mark.parametrize(
    "method,answers,expected_requests,expected_status",
    [
        ("GET", [503, 200], 2, 200),
        ("GET", [502, 504, 503], 3, 503),
        ("GET", [500, 200], 1, 500),
        ("POST", [503, 200], 1, 503),
        ("PUT", [503, 200], 2, 200),
    ],
)
def test_gateway_errors_are_retried_only_for_idempotent_methods(
    http_backend: FakeHttpBackend,
    method: str,
    answers: list[int],
    expected_requests: int,
    expected_status: int,
) -> None:
    http_backend.reply(*(httpx.Response(status) for status in answers))
    with http.client(_settings(2)) as client:
        response = client.request(method, "https://api.example/")
    assert response.status_code == expected_status
    assert len(http_backend.requests) == expected_requests


@pytest.mark.parametrize(
    "method,error,expected_requests",
    [
        ("POST", httpx.ConnectError("refused"), 2),
        ("POST", httpx.ReadTimeout("slow"), 1),
        ("GET", httpx.ReadTimeout("slow"), 2),
        ("GET", httpx.RemoteProtocolError("reset"), 2),
    ],
)
def test_transport_errors_retry_when_safe(
    http_backend: FakeHttpBackend, method: str, error: Exception, expected_requests: int
) -> None:
    """A request that never connected is safe to repeat; one that was sent is not, for POST."""
    http_backend.reply(error, httpx.Response(200))
    with http.client(_settings(1)) as client:
        if expected_requests == 1:
            with pytest.raises(type(error)):
                client.request(method, "https://api.example/")
        else:
            assert client.request(method, "https://api.example/").status_code == 200
    assert len(http_backend.requests) == expected_requests


@pytest.mark.asyncio
async def test_async_client_retries(http_backend: FakeHttpBackend) -> None:
    http_backend.reply(httpx.ConnectError("refused"), httpx.Response(503), httpx.Response(200))
    async with http.async_client(_settings(2)) as client:
        assert (await client.get("https://api.example/")).status_code == 200
    assert len(http_backend.requests) == 3


def test_backoff_doubles_and_is_capped() -> None:
    policy = http.RetryPolicy(retries=10, delay=0.5)
    assert [policy.backoff(n) for n in range(6)] == [0.5, 1.0, 2.0, 4.0, 5.0, 5.0]


def test_retries_stop_when_the_run_budget_is_spent(http_backend: FakeHttpBackend) -> None:
    """A pause that would not leave time for another attempt is not taken."""
    http_backend.reply(httpx.Response(503))
    settings = http.HttpSettings(retry=http.RetryPolicy(retries=5, delay=0.6))
    started = time.monotonic()
    with Deadline(1, "UNKNOWN - x"), http.client(settings) as client:
        assert client.get("https://api.example/").status_code == 503
    # A 0.6s pause plus the 0.5s minimum attempt does not fit the 1s budget.
    assert len(http_backend.requests) == 1
    assert time.monotonic() - started < 1


def test_attempt_timeouts_shrink_to_the_run_budget(http_backend: FakeHttpBackend) -> None:
    with Deadline(2, "UNKNOWN - x"), http.client(http.HttpSettings(timeout=30)) as client:
        client.get("https://api.example/")
    timeouts = http_backend.requests[0].extensions["timeout"]
    assert set(timeouts) == {"connect", "read", "write", "pool"}
    assert all(0 < value <= 2 for value in timeouts.values())


def test_user_agent_names_the_version_and_command(http_backend: FakeHttpBackend) -> None:
    parser = NagiosArgumentParser(prog="check_example")
    parser.add_argument("-t", "--timeout", type=int, default=10)
    http.add_http_arguments(parser, env_prefix="CHECK_EXAMPLE")
    with http.client(parser.parse_args([])) as client:
        client.get("https://api.example/")
    agent = http_backend.requests[0].headers["User-Agent"]
    assert agent == f"nagios-plugins-collection/{__version__} (check_example)"


def test_proxies_come_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.internal:3128")
    monkeypatch.setenv("NO_PROXY", "direct.example")
    with http.client(http.HttpSettings()) as client:
        proxied = client._transport_for_url(httpx.URL("https://api.example/"))
        direct = client._transport_for_url(httpx.URL("https://direct.example/"))
    assert proxied is not client._transport
    assert direct is client._transport


def test_insecure_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        http.HttpSettings(insecure=True).ssl_context()
    assert "not verified" in caplog.text


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://user:pw@api.example:8443/v1/q?token=abc#x", "https://***@api.example:8443/v1/q"),
        ("http://[::1]:9090/metrics?x=1", "http://[::1]:9090/metrics"),
        ("https://api.example", "https://api.example"),
    ],
)
def test_safe_url_drops_credentials_and_query(url: str, expected: str) -> None:
    assert http.safe_url(url) == expected


def test_describe_error_never_shows_the_query_string() -> None:
    request = httpx.Request("GET", "https://u:pw@api.example/q?api_key=abc")
    status = httpx.HTTPStatusError(
        "boom", request=request, response=httpx.Response(401, request=request)
    )
    assert http.describe_error(status) == "HTTP 401 Unauthorized from https://***@api.example/q"
    timeout = httpx.ReadTimeout("read timed out", request=request)
    assert "api_key" not in http.describe_error(timeout)
    assert "timed out" in http.describe_error(timeout)


def _parser() -> NagiosArgumentParser:
    parser = NagiosArgumentParser(prog="check_example")
    parser.add_argument("-t", "--timeout", type=int, default=10)
    http.add_http_arguments(parser, env_prefix="CHECK_EXAMPLE")
    return parser


@pytest.mark.parametrize(
    "args",
    [
        ["--insecure", "--ca-file", "ca.pem"],
        ["--client-key", "key.pem"],
        ["--bearer-token", "t", "--username", "u"],
        ["--password", "p"],
        ["--retries", "-1"],
        ["--api-key", "k", "--api-key-header", "Authorization", "--bearer-token", "t"],
    ],
)
def test_contradictory_options_are_usage_errors(
    args: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exited:
        _parser().parse_args(args)
    assert exited.value.code == 3
    assert capsys.readouterr().out.startswith("UNKNOWN - check_example: ")


def test_settings_read_every_shared_option() -> None:
    args = _parser().parse_args(
        ["--username", "u", "--password", "p", "--retries", "4", "--retry-delay", "2"]
    )
    settings = http.HttpSettings.from_args(args)
    assert (settings.username, settings.password) == ("u", "p")
    assert settings.retry == http.RetryPolicy(4, 2.0)
    assert settings.timeout == 10


def test_no_retry_options_for_measuring_checks() -> None:
    parser = NagiosArgumentParser(prog="check_example")
    parser.add_argument("-t", "--timeout", type=int, default=10)
    http.add_http_arguments(parser, env_prefix="CHECK_EXAMPLE", retries=None)
    with patch("sys.stdout.write"), pytest.raises(SystemExit):
        parser.parse_args(["--retries", "1"])
    assert http.HttpSettings.from_args(parser.parse_args([])).retry.retries == 0
