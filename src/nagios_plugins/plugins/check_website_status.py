#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Check a website's HTTP status, optional content pattern and response time."""

from __future__ import annotations

import argparse
import logging
import re
from typing import Any

import httpx

from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, Status
from nagios_plugins.services import http

# Module level logger so tests can patch it
logger = logging.getLogger(__name__)


class WebsiteStatusChecker:
    """Perform one HTTP check on a web site through the shared HTTP client."""

    def __init__(
        self,
        url: str,
        pattern: str | None = None,
        timeout: int = 10,
        warning_threshold: float = 1.0,
        critical_threshold: float = 2.0,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        body: str | dict[str, Any] | None = None,
        settings: http.HttpSettings | None = None,
    ) -> None:
        """Configure the request and latency thresholds.

        ``settings`` carries TLS, authentication and retry options; without it
        the request uses verified TLS, no authentication and no retries.
        """
        self.url = url
        self.pattern = pattern
        self.timeout = timeout
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.method = method.upper()
        self.headers = headers or {}
        self.body = body
        self.settings = settings or http.HttpSettings(timeout=timeout)

    async def _request(self) -> httpx.Response:
        """Send the request with the configured body and headers."""
        kwargs: dict[str, Any] = {"headers": self.headers}
        if self.body is not None:
            kwargs["json" if isinstance(self.body, dict) else "content"] = self.body
        async with http.async_client(self.settings, follow_redirects=True) as client:
            return await client.request(self.method, self.url, **kwargs)

    def _response_result(self, response: httpx.Response) -> CheckResult:
        """Classify HTTP status, optional content and latency independently."""
        duration = response.elapsed.total_seconds()
        metrics = {"status_code": response.status_code, "duration": duration}
        logger.debug("Response: %s in %.3fs", response.status_code, duration)
        if self.pattern is not None:
            metrics["pattern_found"] = int(bool(re.search(self.pattern, response.text)))
        if response.status_code != 200:
            return CheckResult(Status.CRITICAL, f"HTTP {response.status_code} error", metrics)
        if metrics.get("pattern_found") == 0:
            return CheckResult(Status.CRITICAL, "Pattern not found", metrics)
        if duration > self.critical_threshold:
            return CheckResult(
                Status.CRITICAL,
                f"Response time {duration:.1f}s exceeds critical threshold",
                metrics,
            )
        if duration > self.warning_threshold:
            return CheckResult(
                Status.WARNING, f"Response time {duration:.1f}s exceeds warning threshold", metrics
            )
        return CheckResult(Status.OK, f"Website OK - {duration:.1f}s", metrics)

    async def check_website(self) -> CheckResult:
        """Request the site once (the shared client retries transient failures)."""
        try:
            return self._response_result(await self._request())
        except httpx.TimeoutException:
            return CheckResult(
                Status.CRITICAL, "Website check timed out", {"duration": self.timeout}
            )
        except httpx.HTTPError as error:
            return CheckResult(
                Status.CRITICAL, f"HTTP error: {http.describe_error(error)}", {"duration": 0}
            )
        except re.error as error:
            return CheckResult(Status.UNKNOWN, f"Invalid --pattern: {error}", {"duration": 0})


class CheckWebsiteStatus(AsyncNagiosPlugin):
    """Check website content, status and response time in seconds."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--url", required=True)
        self.parser.add_argument("--pattern")
        self.parser.add_argument("--method", choices=["GET", "HEAD", "POST"], default="GET")
        http.add_http_arguments(
            self.parser, env_prefix="CHECK_WEBSITE_STATUS", retries=0, retry_delay=1.0
        )

    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        checker = WebsiteStatusChecker(
            url=args.url,
            pattern=args.pattern,
            timeout=args.timeout,
            warning_threshold=float(args.warning) if args.warning is not None else 1.0,
            critical_threshold=float(args.critical) if args.critical is not None else 2.0,
            method=args.method,
            settings=http.HttpSettings.from_args(args),
        )
        return await checker.check_website()


def main() -> int:
    """Run the installed website-status command."""
    return CheckWebsiteStatus().run()


if __name__ == "__main__":
    raise SystemExit(main())
