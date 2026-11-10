#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor the age of the latest backup object in S3."""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status, threshold_check
from nagios_plugins.services.aws_s3 import latest_object_age_seconds


class CheckBackupFreshness(NagiosPlugin):
    """Monitor the age of the latest backup object in S3."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--bucket", required=True)
        self.parser.add_argument(
            "--prefix",
            default="",
            help="Key prefix of the backups; every object under it is listed, so keep it narrow",
        )
        self.parser.add_argument("--region")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            age = latest_object_age_seconds(
                args.bucket, prefix=args.prefix, region=args.region, timeout=args.timeout
            )
        except RuntimeError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        # Nagios ranges: a plain N alerts above N (outside 0..N).
        status = threshold_check(age, args.warning, args.critical)
        return CheckResult(status, f"backup_age={age}s", metrics={"age_seconds": age})


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckBackupFreshness().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
