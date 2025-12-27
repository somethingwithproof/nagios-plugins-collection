#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import statistics

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, Status


class CheckHttpSli(NagiosPlugin):
    """Probe one or more URLs concurrently and report p50/p95/p99 and error-rate."""

    def __init__(self) -> None:
        super().__init__()
        self.parser.add_argument(
            "--url", action="append", required=True, help="URL to probe (repeatable)"
        )
        self.parser.add_argument("--samples", type=int, default=3, help="Samples per URL")
        self.parser.add_argument("--verify-ssl", action="store_true", default=False)

    def check(self, args: argparse.Namespace) -> CheckResult:
        return asyncio.run(self._async_check(args))

    async def _async_check(self, args: argparse.Namespace) -> CheckResult:
        latencies: list[float] = []
        errors = 0
        total = 0
        async with httpx.AsyncClient(verify=args.verify_ssl, timeout=args.timeout) as client:
            tasks = []
            for url in args.url:
                for _ in range(args.samples):
                    tasks.append(self._probe(client, url))
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
        if latencies:
            p50 = statistics.quantiles(latencies, n=100)[49]
            p95 = statistics.quantiles(latencies, n=100)[94]
            p99 = statistics.quantiles(latencies, n=100)[98]
        else:
            p50 = p95 = p99 = float("inf")
        status = Status.OK
        if args.critical and (error_rate >= float(args.critical) or p95 >= float(args.critical)):
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

    async def _probe(self, client: httpx.AsyncClient, url: str) -> float | None:
        try:
            r = await client.get(url, follow_redirects=True)
            r.raise_for_status()
            return float(r.elapsed.total_seconds() * 1000)
        except Exception:
            return None


def main() -> int:
    return CheckHttpSli().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
