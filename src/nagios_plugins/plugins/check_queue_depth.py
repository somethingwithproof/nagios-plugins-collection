#!/usr/bin/env python3
from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services.aws_sqs import queue_depth


class CheckQueueDepth(NagiosPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.parser.add_argument("--queue-url", required=True)
        self.parser.add_argument("--region")

    def check(self, args: argparse.Namespace) -> CheckResult:
        try:
            m = queue_depth(args.queue_url, region=args.region, timeout=args.timeout)
        except RuntimeError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        status = Status.OK
        depth = m["depth"]
        if args.critical and depth >= int(args.critical):
            status = Status.CRITICAL
        elif args.warning and depth >= int(args.warning):
            status = Status.WARNING
        msg = f"depth={depth} inflight={m['inflight']} delayed={m['delayed']}"
        return CheckResult(status, msg, metrics=m)


def main() -> int:
    return CheckQueueDepth().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
