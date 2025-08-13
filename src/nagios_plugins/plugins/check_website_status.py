#!/usr/bin/env python3
"""Simple website status checker used in unit tests.

The original project contains a much more feature rich implementation that is
integrated with a plugin framework.  For the purposes of the kata we only need a
light‑weight class that can be instantiated directly and whose behaviour is easy
to mock in tests.
"""

from __future__ import annotations

import logging
import re
import time
from typing import Optional

import httpx

from nagios_plugins.base import CheckResult, Status

# Module level logger so tests can patch it
logger = logging.getLogger(__name__)


class WebsiteStatusChecker:
    """Perform a simple HTTP check on a web site."""

    def __init__(
        self,
        url: str,
        pattern: Optional[str] = None,
        timeout: int = 10,
        warning_threshold: float = 1.0,
        critical_threshold: float = 2.0,
    ) -> None:
        self.url = url
        self.pattern = pattern
        self.timeout = timeout
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    async def check_website(self) -> CheckResult:
        """Check the configured website and return a :class:`CheckResult`."""
        start_time = time.time()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.url)

            duration = response.elapsed.total_seconds()
            metrics = {"status_code": response.status_code, "duration": duration}

            if response.status_code != 200:
                if self.pattern is not None:
                    metrics["pattern_found"] = (
                        1 if re.search(self.pattern, response.text) else 0
                    )
                return CheckResult(
                    Status.CRITICAL,
                    f"HTTP {response.status_code} error",
                    metrics,
                )

            if self.pattern is not None:
                found = 1 if re.search(self.pattern, response.text) else 0
                metrics["pattern_found"] = found
                if found == 0:
                    return CheckResult(Status.CRITICAL, "Pattern not found", metrics)

            if duration > self.critical_threshold:
                return CheckResult(
                    Status.CRITICAL,
                    f"Response time {duration:.1f}s exceeds critical threshold",
                    metrics,
                )
            if duration > self.warning_threshold:
                return CheckResult(
                    Status.WARNING,
                    f"Response time {duration:.1f}s exceeds warning threshold",
                    metrics,
                )

            return CheckResult(
                Status.OK,
                f"Website OK - {duration:.1f}s",
                metrics,
            )
        except httpx.TimeoutException:
            metrics = {"duration": self.timeout}
            return CheckResult(
                Status.CRITICAL,
                "Website check timed out",
                metrics,
            )
        except httpx.HTTPError as exc:
            metrics = {"duration": 0}
            return CheckResult(Status.CRITICAL, f"HTTP error: {exc}", metrics)
        except Exception as exc:  # pragma: no cover - defensive
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                raise
            metrics = {"duration": 0}
            logger.exception("Unexpected error")
            return CheckResult(Status.UNKNOWN, f"Unexpected error: {exc}", metrics)
