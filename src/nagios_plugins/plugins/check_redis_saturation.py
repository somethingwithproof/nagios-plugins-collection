#!/usr/bin/env python3
"""Monitor Redis memory use, evictions and cache hits."""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services.redis_svc import get_stats


class CheckRedisSaturation(NagiosPlugin):
    """Monitor Redis memory use, evictions and cache hits."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--url", required=True, help="Redis URL e.g. redis://host:6379/0")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            stats = get_stats(args.url)
        except RuntimeError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        status = Status.OK
        if args.critical and (
            stats["blocked_clients"] > int(args.critical) or stats["hitratio"] < 0.5
        ):
            status = Status.CRITICAL
        elif args.warning and (
            stats["evicted_keys"] > int(args.warning) or stats["hitratio"] < 0.8
        ):
            status = Status.WARNING
        msg = f"used={stats['used_memory']} evicted={stats['evicted_keys']} blocked={stats['blocked_clients']} hitratio={stats['hitratio']:.2f}"
        return CheckResult(
            status,
            msg,
            metrics={
                k: (int(v) if isinstance(v, float) and v.is_integer() else v)
                for k, v in stats.items()
            },
        )


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckRedisSaturation().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
