#!/usr/bin/env python3
from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services.pg import replication_lag_seconds


class CheckPostgresReplicationLag(NagiosPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.parser.add_argument("--dsn", required=True, help="PostgreSQL DSN for primary")

    def check(self, args: argparse.Namespace) -> CheckResult:
        try:
            lag = replication_lag_seconds(args.dsn, timeout=args.timeout)
        except RuntimeError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        status = Status.OK
        if args.critical and lag >= float(args.critical):
            status = Status.CRITICAL
        elif args.warning and lag >= float(args.warning):
            status = Status.WARNING
        return CheckResult(
            status, f"replication_lag={lag:.1f}s", metrics={"lag_seconds": round(lag, 1)}
        )


def main() -> int:
    return CheckPostgresReplicationLag().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
