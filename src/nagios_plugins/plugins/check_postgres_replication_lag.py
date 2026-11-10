#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor PostgreSQL replication lag in seconds."""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status, threshold_check
from nagios_plugins.services.pg import replication_lag_seconds


class CheckPostgresReplicationLag(NagiosPlugin):
    """Monitor PostgreSQL replication lag in seconds."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_secret_argument(
            "--dsn", env="CHECK_POSTGRES_DSN", help="PostgreSQL DSN for primary", required=True
        )

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            lag = replication_lag_seconds(args.dsn, timeout=args.timeout)
        except RuntimeError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        if lag is None:
            return CheckResult(
                Status.CRITICAL, "No standby connected (pg_stat_replication is empty)"
            )
        # Nagios ranges: a plain N alerts above N (outside 0..N).
        status = threshold_check(lag, args.warning, args.critical)
        return CheckResult(
            status, f"replication_lag={lag:.1f}s", metrics={"lag_seconds": round(lag, 1)}
        )


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckPostgresReplicationLag().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
