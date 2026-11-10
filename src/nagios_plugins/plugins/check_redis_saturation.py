#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor Redis memory use, evictions and cache hits."""

from __future__ import annotations

import argparse

from nagios_plugins.base import (
    CheckResult,
    NagiosPlugin,
    PerfData,
    Status,
    most_severe,
    nagios_range,
    threshold_check,
)
from nagios_plugins.services.redis_svc import get_stats


class CheckRedisSaturation(NagiosPlugin):
    """Monitor Redis memory saturation, evictions and cache hits.

    -w/-c are Nagios ranges for used_memory as a percentage of maxmemory, a
    gauge that recovers when memory is freed. evicted_keys is a monotonic
    counter since restart, so it is published as perfdata (UOM c) for the
    graphing system to turn into a rate rather than compared with a threshold.
    Blocked clients and the hit ratio alert only when their own ranges are given.
    """

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_secret_argument(
            "--url",
            env="CHECK_REDIS_URL",
            help="Redis URL e.g. redis://:password@host:6379/0",
            required=True,
        )
        for name, measure in (
            ("blocked", "blocked_clients (clients waiting in BLPOP and similar)"),
            ("hitratio", "keyspace hit ratio (0-1); for example 0.8: alerts below 0.8"),
        ):
            for level in ("warning", "critical"):
                self.parser.add_argument(
                    f"--{name}-{level}",
                    type=nagios_range,
                    metavar="RANGE",
                    help=f"{level.upper()} range for {measure} (default: not checked)",
                )

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            stats = get_stats(args.url, timeout=args.timeout)
        except RuntimeError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        used, maxmemory = int(stats["used_memory"]), int(stats["maxmemory"])
        metrics: dict[str, PerfData] = {
            "used_memory": PerfData(used, "B", minimum=0, maximum=maxmemory or None),
            "evicted_keys": PerfData(stats["evicted_keys"], "c"),
            "blocked_clients": PerfData(
                stats["blocked_clients"], "", args.blocked_warning, args.blocked_critical, 0
            ),
            "hitratio": PerfData(
                round(stats["hitratio"], 4), "", args.hitratio_warning, args.hitratio_critical, 0, 1
            ),
        }
        statuses = [
            threshold_check(stats["blocked_clients"], args.blocked_warning, args.blocked_critical),
            threshold_check(stats["hitratio"], args.hitratio_warning, args.hitratio_critical),
        ]
        summary = (
            f"evicted={stats['evicted_keys']} blocked={stats['blocked_clients']} "
            f"hitratio={stats['hitratio']:.2f}"
        )
        if not maxmemory:
            if args.warning or args.critical:
                return CheckResult(
                    Status.UNKNOWN,
                    f"maxmemory is not set, so memory saturation is undefined; used={used}B "
                    f"{summary}",
                    metrics=metrics,
                )
            return CheckResult(
                most_severe(*statuses), f"used={used}B (no maxmemory) {summary}", metrics=metrics
            )
        percent = used / maxmemory * 100
        metrics["memory_used_pct"] = PerfData(
            round(percent, 2), "%", args.warning, args.critical, 0, 100
        )
        return CheckResult(
            most_severe(threshold_check(percent, args.warning, args.critical), *statuses),
            f"memory {percent:.1f}% of maxmemory ({used}/{maxmemory}B) {summary}",
            metrics=metrics,
        )


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckRedisSaturation().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
