#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor HTTP latency percentiles and request failures."""

from __future__ import annotations

import argparse
import asyncio
import statistics

import httpx

from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, PerfData, Status, threshold_check
from nagios_plugins.services import http

# Most severe first when combining the latency and error-rate verdicts.
_SEVERITY = {Status.OK: 0, Status.UNKNOWN: 1, Status.WARNING: 2, Status.CRITICAL: 3}


class CheckHttpSli(AsyncNagiosPlugin):
    """Probe one or more URLs concurrently and report p50/p95/p99 and error-rate.

    Latency and error rate have separate Nagios ranges. -w/-c are aliases for
    --latency-warning/--latency-critical (p95 in milliseconds).
    """

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument(
            "--url", action="append", required=True, help="URL to probe (repeatable)"
        )
        self.parser.add_argument("--samples", type=int, default=3, help="Samples per URL")
        self.parser.add_argument(
            "--latency-warning",
            metavar="RANGE",
            help="p95 latency range in ms for WARNING (alias: -w)",
        )
        self.parser.add_argument(
            "--latency-critical",
            metavar="RANGE",
            help="p95 latency range in ms for CRITICAL (alias: -c)",
        )
        self.parser.add_argument(
            "--error-rate-warning",
            metavar="RANGE",
            help="Range for the fraction of failed requests (0-1) for WARNING",
        )
        self.parser.add_argument(
            "--error-rate-critical",
            metavar="RANGE",
            help="Range for the fraction of failed requests (0-1) for CRITICAL",
        )
        # Every sample is a measurement, so failed requests are never retried.
        http.add_http_arguments(self.parser, env_prefix="CHECK_HTTP_SLI", retries=None)

    def parse_args(self, args: list[str] | None = None) -> argparse.Namespace:
        """Resolve -w/-c into the latency thresholds they alias."""
        parsed = super().parse_args(args)
        for alias, option in (("warning", "latency_warning"), ("critical", "latency_critical")):
            if getattr(parsed, alias) is None:
                continue
            if getattr(parsed, option) is not None:
                flag = option.replace("_", "-")
                self.parser.error(f"-{alias[0]} is an alias of --{flag}; pass only one")
            setattr(parsed, option, getattr(parsed, alias))
        return parsed

    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Collect HTTP samples and summarize latency and failures."""
        latencies: list[float] = []
        errors = 0
        total = 0
        async with http.async_client(args, follow_redirects=True) as client:
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
        statuses = [threshold_check(error_rate, args.error_rate_warning, args.error_rate_critical)]
        if errors == total:
            statuses.append(Status.CRITICAL)
        else:
            statuses.append(threshold_check(p95, args.latency_warning, args.latency_critical))
        status = max(statuses, key=_SEVERITY.__getitem__)
        latency = f"{p95:.1f}ms" if latencies else "n/a"
        msg = f"SLI p95={latency} error_rate={error_rate:.2%}"
        metrics = {
            "p50_ms": round(p50, 1),
            "p95_ms": PerfData(
                round(p95, 1), warning=args.latency_warning, critical=args.latency_critical
            ),
            "p99_ms": round(p99, 1),
            "error_rate": PerfData(
                round(error_rate, 4),
                warning=args.error_rate_warning,
                critical=args.error_rate_critical,
                minimum=0,
                maximum=1,
            ),
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
            r = await client.get(url)
            r.raise_for_status()
            return float(r.elapsed.total_seconds() * 1000)
        except Exception:
            return None


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckHttpSli().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
