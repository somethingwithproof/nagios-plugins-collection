#!/usr/bin/env python3
"""Monitor the age of the latest backup object in S3."""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services.aws_s3 import latest_object_age_seconds


class CheckBackupFreshness(NagiosPlugin):
    """Monitor the age of the latest backup object in S3."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--bucket", required=True)
        self.parser.add_argument("--prefix", default="")
        self.parser.add_argument("--region")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            age = latest_object_age_seconds(
                args.bucket, prefix=args.prefix, region=args.region, timeout=args.timeout
            )
        except RuntimeError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        status = Status.OK
        if args.critical and age >= int(args.critical):
            status = Status.CRITICAL
        elif args.warning and age >= int(args.warning):
            status = Status.WARNING
        return CheckResult(status, f"backup_age={age}s", metrics={"age_seconds": age})


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckBackupFreshness().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
