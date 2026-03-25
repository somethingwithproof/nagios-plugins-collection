#!/usr/bin/env python3
"""Simple website status checker used in unit tests.

The original project contains a much more feature rich implementation that is
integrated with a plugin framework.  For the purposes of the kata we only need a
light‑weight class that can be instantiated directly and whose behaviour is easy
to mock in tests.
"""

from __future__ import annotations

import asyncio
import logging
import re
from pathlib import Path
from typing import Any, Optional

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
        method: str = "GET",
        headers: Optional[dict[str, str]] = None,
        body: Optional[str | dict[str, Any]] = None,
        auth: Optional[tuple[str, str]] = None,
        retries: int = 0,
        retry_delay: float = 1.0,
        verbose: bool = False,
        log_file: Optional[str | Path] = None,
    ) -> None:
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
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            logger.addHandler(file_handler)
            if verbose:
                logger.setLevel(logging.DEBUG)

    async def check_website(self) -> CheckResult:
        """Check the configured website and return a :class:`CheckResult`."""
        attempt = 0
        last_error = None

        while attempt <= self.retries:
            try:
                if self.verbose:
                    logger.debug(
                        f"Attempt {attempt + 1}/{self.retries + 1}: {self.method} {self.url}"
                    )

                async with httpx.AsyncClient(
                    timeout=self.timeout,
                    follow_redirects=True,
                    auth=self.auth,
                ) as client:
                    request_kwargs = {"headers": self.headers}

                    if self.body is not None:
                        if isinstance(self.body, dict):
                            request_kwargs["json"] = self.body
                        else:
                            request_kwargs["content"] = self.body

                    response = await client.request(self.method, self.url, **request_kwargs)

                duration = response.elapsed.total_seconds()
                metrics = {"status_code": response.status_code, "duration": duration}

                if self.verbose:
                    logger.debug(
                        f"Response: {response.status_code} in {duration:.3f}s"
                    )

                if response.status_code != 200:
                    if self.pattern is not None:
                        metrics["pattern_found"] = 1 if re.search(self.pattern, response.text) else 0
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

            except httpx.TimeoutException as exc:
                last_error = exc
                if self.verbose:
                    logger.warning(f"Attempt {attempt + 1} timed out")
                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay)
                    attempt += 1
                    continue

                metrics = {"duration": self.timeout}
                return CheckResult(
                    Status.CRITICAL,
                    "Website check timed out",
                    metrics,
                )

            except httpx.HTTPError as exc:
                last_error = exc
                if self.verbose:
                    logger.warning(f"Attempt {attempt + 1} failed: {exc}")
                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay)
                    attempt += 1
                    continue

                metrics = {"duration": 0}
                return CheckResult(Status.CRITICAL, f"HTTP error: {exc}", metrics)

            except Exception as exc:  # pragma: no cover - defensive
                if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                    raise
                last_error = exc
                if self.verbose:
                    logger.exception(f"Attempt {attempt + 1} unexpected error")
                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay)
                    attempt += 1
                    continue

                metrics = {"duration": 0}
                logger.exception("Unexpected error")
                return CheckResult(Status.UNKNOWN, f"Unexpected error: {exc}", metrics)

        # Should not reach here, but just in case
        metrics = {"duration": 0}
        return CheckResult(
            Status.UNKNOWN,
            f"All retry attempts exhausted. Last error: {last_error}",
            metrics,
        )
