#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt

from nagios_plugins.base import CheckResult, NagiosPlugin, Status


def _month_range_utc() -> tuple[str, str]:
    now = dt.datetime.now(dt.timezone.utc)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return start.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")


class CheckCloudBudget(NagiosPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.parser.add_argument("--region", default="us-east-1")
        self.parser.add_argument(
            "--budget", type=float, required=True, help="Monthly budget amount in USD"
        )

    def check(self, args: argparse.Namespace) -> CheckResult:
        try:
            import boto3  # type: ignore
        except Exception:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, "boto3 not installed; install [aws]")
        start, end = _month_range_utc()
        ce = boto3.client("ce", region_name=args.region)  # type: ignore
        resp = ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
        )
        results = resp.get("ResultsByTime", [])
        amount = float(results[0]["Total"]["UnblendedCost"]["Amount"]) if results else 0.0
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
    return CheckCloudBudget().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
