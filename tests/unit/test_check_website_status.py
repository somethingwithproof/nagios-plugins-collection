# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for the check_website_status plugin."""

from collections.abc import Callable
from datetime import timedelta
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_website_status import CheckWebsiteStatus, WebsiteStatusChecker
from nagios_plugins.services import http
from tests.fakes import serve_http


@pytest.mark.asyncio
async def test_invalid_pattern_does_not_retry_transport() -> None:
    """An invalid regex returns UNKNOWN after one response without retry sleeps."""
    requests = []

    def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        response = httpx.Response(200, text="healthy", request=request)
        response.elapsed = timedelta(milliseconds=5)
        return response

    transport = httpx.MockTransport(respond)
    with (
        serve_http(transport.handle_request),
        patch("asyncio.sleep", new=AsyncMock()) as sleep,
    ):
        result = await WebsiteStatusChecker(
            "https://example.com",
            pattern="[",
            settings=http.HttpSettings(retry=http.RetryPolicy(retries=3)),
        ).check_website()
    assert result.status == Status.UNKNOWN
    assert len(requests) == 1
    sleep.assert_not_called()


def _site(status: int, text: str, seconds: float) -> Callable[[httpx.Request], httpx.Response]:
    def respond(request: httpx.Request) -> httpx.Response:
        response = httpx.Response(status, text=text, request=request)
        response.elapsed = timedelta(seconds=seconds)
        return response

    return respond


def _failing(error: Exception) -> Callable[[httpx.Request], httpx.Response]:
    def respond(request: httpx.Request) -> httpx.Response:
        raise error

    return respond


class TestWebsiteStatusChecker:
    """Tests for the WebsiteStatusChecker class."""

    @pytest.fixture
    def checker(self) -> WebsiteStatusChecker:
        """Create a WebsiteStatusChecker instance."""
        return WebsiteStatusChecker(
            url="https://example.com",
            pattern="Example Domain",
            timeout=10,
            warning_threshold=1.0,
            critical_threshold=2.0,
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status,text,seconds,expected,message",
        [
            (200, "Example Domain", 0.5, Status.OK, "Website OK - 0.5s"),
            (200, "Example Domain", 1.5, Status.WARNING, "exceeds warning threshold"),
            (200, "Example Domain", 2.5, Status.CRITICAL, "exceeds critical threshold"),
            (404, "Not Found", 0.5, Status.CRITICAL, "HTTP 404 error"),
            (200, "Not what we're looking for", 0.5, Status.CRITICAL, "Pattern not found"),
        ],
    )
    async def test_response_classification(
        self,
        checker: WebsiteStatusChecker,
        status: int,
        text: str,
        seconds: float,
        expected: Status,
        message: str,
    ) -> None:
        with serve_http(_site(status, text, seconds)):
            result = await checker.check_website()
        assert result.status == expected
        assert message in result.message
        assert result.metrics["status_code"] == status
        assert result.metrics["duration"].value == seconds
        assert result.metrics["pattern_found"] == int("Example Domain" in text)

    @pytest.mark.asyncio
    async def test_check_website_timeout(self, checker: WebsiteStatusChecker) -> None:
        with serve_http(_failing(httpx.ReadTimeout("Timeout"))):
            result = await checker.check_website()
        assert result.status == Status.CRITICAL
        assert "timed out" in result.message
        assert result.metrics["duration"] == 10

    @pytest.mark.asyncio
    async def test_check_website_http_error(self, checker: WebsiteStatusChecker) -> None:
        with serve_http(_failing(httpx.ConnectError("refused"))):
            result = await checker.check_website()
        assert result.status == Status.CRITICAL
        assert result.message == "HTTP error: refused requesting https://example.com"
        assert result.metrics["duration"] == 0

    @pytest.mark.asyncio
    async def test_check_website_unexpected_error_propagates(
        self, checker: WebsiteStatusChecker
    ) -> None:
        """Unexpected failures reach the plugin wrapper, which reports UNKNOWN."""
        with serve_http(_failing(RuntimeError("Unexpected error"))), pytest.raises(RuntimeError):
            await checker.check_website()


def test_plugin_reports_unexpected_errors_as_unknown(capsys: pytest.CaptureFixture[str]) -> None:
    with serve_http(_failing(RuntimeError("Unexpected error"))):
        code = CheckWebsiteStatus().run(["--url", "https://example.com"])
    assert code == Status.UNKNOWN.value
    assert capsys.readouterr().out.startswith("UNKNOWN - Unhandled exception: Unexpected error")
