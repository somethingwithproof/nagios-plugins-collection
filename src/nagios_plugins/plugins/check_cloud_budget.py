#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor month-to-date AWS spend against alert thresholds."""

from __future__ import annotations

import argparse
import datetime as dt

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services import aws


def _month_range_utc(now: dt.datetime | None = None) -> tuple[str, str]:
    """Return the Cost Explorer period for month-to-date spend, including today.

    Cost Explorer treats End as exclusive and rejects End == Start, so End is
    tomorrow; on the first of the month the period is that single day.
    """
    today = (now or dt.datetime.now(dt.UTC)).date()
    return today.replace(day=1).isoformat(), (today + dt.timedelta(days=1)).isoformat()


class CheckCloudBudget(NagiosPlugin):
    """Monitor month-to-date AWS spend against alert thresholds."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--region", default="us-east-1")
        self.parser.add_argument(
            "--budget", type=float, required=True, help="Monthly budget amount in USD"
        )

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            ce = aws.client("ce", region=args.region, timeout=args.timeout)
        except RuntimeError as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"{e}; install [aws]")
        start, end = _month_range_utc()
        resp = ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
        )
        results = resp.get("ResultsByTime", [])
        if not results:
            return CheckResult(
                Status.UNKNOWN, f"Cost Explorer returned no costs for {start}..{end}"
            )
        amount = float(results[0]["Total"]["UnblendedCost"]["Amount"])
        percent = (amount / args.budget * 100) if args.budget > 0 else 0.0
        status = Status.OK
        if args.critical and percent >= float(args.critical):
            status = Status.CRITICAL
        elif args.warning and percent >= float(args.warning):
            status = Status.WARNING
        msg = f"mtd_usd={amount:.2f} {percent:.1f}% of budget {args.budget:.2f}"
        metrics = {"mtd_usd": round(amount, 2), "percent_of_budget": round(percent, 1)}
        return CheckResult(status, msg, metrics=metrics)


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckCloudBudget().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
