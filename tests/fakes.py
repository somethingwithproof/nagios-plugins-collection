# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Fake HTTP backends that keep the shared client factory in the request path.

Patching httpx's transports (rather than ``httpx.Client``) keeps redirects,
origin-bound credentials, retries and proxy mounts under test.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from unittest.mock import patch

import httpx

Handler = Callable[[httpx.Request], httpx.Response]
_LOOPBACK = {"localhost", "127.0.0.1", "::1"}
_real_sync = httpx.HTTPTransport.handle_request
_real_async = httpx.AsyncHTTPTransport.handle_async_request


class FakeHttpBackend:
    """Record requests and answer them with ``respond`` (200 with no body by default)."""

    def __init__(self, respond: Handler | None = None) -> None:
        self.requests: list[httpx.Request] = []
        self.respond: Handler = respond or (lambda request: httpx.Response(200))

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.requests.append(request)
        return self.respond(request)

    def reply(self, *answers: httpx.Response | Exception) -> None:
        """Answer requests in turn with copies of ``answers``; the last one repeats."""
        pending = list(answers)

        def respond(request: httpx.Request) -> httpx.Response:
            answer = pending.pop(0) if len(pending) > 1 else pending[0]
            if isinstance(answer, Exception):
                raise answer
            # A copy each time: a response body can be consumed only once.
            return httpx.Response(answer.status_code, headers=answer.headers, content=answer.read())

        self.respond = respond


@contextmanager
def serve_http(handler: Handler) -> Iterator[None]:
    """Answer every sync and async httpx request with ``handler``."""

    async def handle_async(_: httpx.AsyncHTTPTransport, request: httpx.Request) -> httpx.Response:
        return handler(request)

    with (
        patch.object(httpx.HTTPTransport, "handle_request", lambda _, request: handler(request)),
        patch.object(httpx.AsyncHTTPTransport, "handle_async_request", handle_async),
    ):
        yield


def _refuse(request: httpx.Request) -> None:
    if request.url.host not in _LOOPBACK:
        raise httpx.ConnectError(f"tests may not contact {request.url.host}", request=request)


@contextmanager
def offline_http() -> Iterator[None]:
    """Refuse requests to anything but loopback, where tests run their own servers."""

    def handle(transport: httpx.HTTPTransport, request: httpx.Request) -> httpx.Response:
        _refuse(request)
        return _real_sync(transport, request)

    async def handle_async(
        transport: httpx.AsyncHTTPTransport, request: httpx.Request
    ) -> httpx.Response:
        _refuse(request)
        return await _real_async(transport, request)

    with (
        patch.object(httpx.HTTPTransport, "handle_request", handle),
        patch.object(httpx.AsyncHTTPTransport, "handle_async_request", handle_async),
    ):
        yield
