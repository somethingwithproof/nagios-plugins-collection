#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor HTTP latency percentiles and request failures."""

from __future__ import annotations

import argparse
import asyncio
import statistics

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services.http_tls import add_tls_arguments, tls_verification


class CheckHttpSli(NagiosPlugin):
    """Probe one or more URLs concurrently and report p50/p95/p99 and error-rate."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument(
            "--url", action="append", required=True, help="URL to probe (repeatable)"
        )
        self.parser.add_argument("--samples", type=int, default=3, help="Samples per URL")
        add_tls_arguments(self.parser)

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        return asyncio.run(self._async_check(args))

    async def _async_check(self, args: argparse.Namespace) -> CheckResult:
        """Collect HTTP samples and summarize latency and failures."""
        latencies: list[float] = []
        errors = 0
        total = 0
        async with httpx.AsyncClient(
            verify=tls_verification(args.ca_file), timeout=args.timeout
        ) as client:
            tasks = [self._probe(client, url) for url in args.url for _ in range(args.samples)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            total += 1
            if not isinstance(r, (int, float)):
                errors += 1
            else:
                latencies.append(float(r))
        if not total:
            return CheckResult(Status.UNKNOWN, "No probes executed")
        error_rate = errors / total
        p50, p95, p99 = self._percentiles(latencies)
        status = Status.CRITICAL if errors == total else Status.OK
        if (
            errors == total
            or args.critical
            and (error_rate >= float(args.critical) or p95 >= float(args.critical))
        ):
            status = Status.CRITICAL
        elif args.warning and (error_rate >= float(args.warning) or p95 >= float(args.warning)):
            status = Status.WARNING
        msg = f"SLI p95={p95:.1f}ms error_rate={error_rate:.2%}"
        metrics = {
            "p50_ms": round(p50, 1),
            "p95_ms": round(p95, 1),
            "p99_ms": round(p99, 1),
            "error_rate": round(error_rate, 4),
        }
        return CheckResult(status, msg, metrics=metrics)

    @staticmethod
    def _percentiles(latencies: list[float]) -> tuple[float, float, float]:
        """Handle empty and singleton samples before computing percentiles."""
        if not latencies:
            return (float("inf"),) * 3
        if len(latencies) == 1:
            return (latencies[0],) * 3
        percentiles = statistics.quantiles(latencies, n=100)
        return percentiles[49], percentiles[94], percentiles[98]

    async def _probe(self, client: httpx.AsyncClient, url: str) -> float | None:
        """Return elapsed milliseconds for one successful HTTP request."""
        try:
            r = await client.get(url, follow_redirects=True)
            r.raise_for_status()
            return float(r.elapsed.total_seconds() * 1000)
        except Exception:
            return None


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckHttpSli().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
