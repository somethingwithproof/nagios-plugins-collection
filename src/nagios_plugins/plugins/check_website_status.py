#!/usr/bin/env python3
"""Simple website status checker used in unit tests.

The original project contains a much more feature rich implementation that is
integrated with a plugin framework.  For the purposes of the kata we only need a
light‑weight class that can be instantiated directly and whose behaviour is easy
to mock in tests.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import re
from pathlib import Path
from typing import Any

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, Status

# Module level logger so tests can patch it
logger = logging.getLogger(__name__)


class WebsiteStatusChecker:
    """Perform a simple HTTP check on a web site."""

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
        auth: tuple[str, str] | None = None,
        retries: int = 0,
        retry_delay: float = 1.0,
        verbose: bool = False,
        log_file: str | Path | None = None,
    ) -> None:
        """Configure HTTP request, retry and latency settings."""
        self.url = url
        self.pattern = pattern
        self.timeout = timeout
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.method = method.upper()
        self.headers = headers or {}
        self.body = body
        self.auth = auth
        self.retries = retries
        self.retry_delay = retry_delay
        self.verbose = verbose

        # Setup file logging if requested
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            logger.addHandler(file_handler)
            if verbose:
                logger.setLevel(logging.DEBUG)

    async def _request(self) -> httpx.Response:
        """Send one request with the configured body and verified TLS defaults."""
        kwargs: dict[str, Any] = {"headers": self.headers}
        if self.body is not None:
            kwargs["json" if isinstance(self.body, dict) else "content"] = self.body
        async with httpx.AsyncClient(
            timeout=self.timeout, follow_redirects=True, auth=self.auth
        ) as client:
            return await client.request(self.method, self.url, **kwargs)

    def _response_result(self, response: httpx.Response) -> CheckResult:
        """Classify HTTP status, optional content and latency independently."""
        duration = response.elapsed.total_seconds()
        metrics = {"status_code": response.status_code, "duration": duration}
        if self.verbose:
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

    def _error_result(self, error: Exception) -> CheckResult:
        """Translate a terminal request failure into a Nagios result."""
        if isinstance(error, httpx.TimeoutException):
            return CheckResult(
                Status.CRITICAL, "Website check timed out", {"duration": self.timeout}
            )
        if isinstance(error, httpx.HTTPError):
            return CheckResult(Status.CRITICAL, f"HTTP error: {error}", {"duration": 0})
        return CheckResult(Status.UNKNOWN, f"Unexpected error: {error}", {"duration": 0})

    async def check_website(self) -> CheckResult:
        """Retry transport errors, preserving response status and latency semantics."""
        if self.retries < 0:
            return CheckResult(Status.UNKNOWN, "Retries must not be negative", {"duration": 0})
        for attempt in range(self.retries + 1):
            try:
                if self.verbose:
                    logger.debug(
                        "Attempt %s/%s: %s %s", attempt + 1, self.retries + 1, self.method, self.url
                    )
                return self._response_result(await self._request())
            except re.error as error:
                return self._error_result(error)
            except Exception as error:
                if self.verbose:
                    logger.exception("Website attempt %s failed", attempt + 1)
                if attempt == self.retries:
                    return self._error_result(error)
                await asyncio.sleep(self.retry_delay)
        raise RuntimeError("Website retry loop terminated unexpectedly")


class CheckWebsiteStatus(NagiosPlugin):
    """Check website content, status and response time in seconds."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--url", required=True)
        self.parser.add_argument("--pattern")
        self.parser.add_argument("--method", choices=["GET", "HEAD", "POST"], default="GET")
        self.parser.add_argument("--retries", type=int, default=0)
        self.parser.add_argument("--retry-delay", type=float, default=1.0)

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        checker = WebsiteStatusChecker(
            url=args.url,
            pattern=args.pattern,
            timeout=args.timeout,
            warning_threshold=float(args.warning) if args.warning is not None else 1.0,
            critical_threshold=float(args.critical) if args.critical is not None else 2.0,
            method=args.method,
            retries=args.retries,
            retry_delay=args.retry_delay,
            verbose=bool(args.verbose),
        )
        return asyncio.run(checker.check_website())


def main() -> int:
    """Run the installed website-status command."""
    return CheckWebsiteStatus().run()


if __name__ == "__main__":
    raise SystemExit(main())
