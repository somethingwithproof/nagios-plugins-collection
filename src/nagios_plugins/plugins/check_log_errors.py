#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, Status


class CheckLogErrors(NagiosPlugin):
    """Search ES/OS for error logs in the last N minutes and threshold count/rate."""

    def __init__(self) -> None:
        super().__init__()
        self.parser.add_argument("--endpoint", required=True, help="ES/OpenSearch endpoint")
        self.parser.add_argument("--index", required=True, help="Index or alias")
        self.parser.add_argument("--minutes", type=int, default=5)
        self.parser.add_argument("--query", default="level:ERROR OR status:[500 TO 599]")
        self.parser.add_argument("--verify-ssl", action="store_true", default=False)

    def check(self, args: argparse.Namespace) -> CheckResult:
        url = f"{args.endpoint.rstrip('/')}/{args.index}/_search"
        now = int(time.time() * 1000)
        gte = now - args.minutes * 60 * 1000
        body = {
            "size": 0,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "@timestamp": {"gte": gte, "lte": now, "format": "epoch_millis"}
                            }
                        },
                        {"query_string": {"query": args.query}},
                    ]
                }
            },
        }
        try:
            with httpx.Client(timeout=args.timeout, verify=args.verify_ssl) as client:
                r = client.post(url, json=body)
            r.raise_for_status()
            hits = r.json().get("hits", {}).get("total", {}).get("value", 0)
            status = Status.OK
            if args.critical and hits >= int(args.critical):
                status = Status.CRITICAL
            elif args.warning and hits >= int(args.warning):
                status = Status.WARNING
            return CheckResult(
                status, f"errors={hits} in {args.minutes}m", metrics={"errors": hits}
            )
        except httpx.HTTPError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {e}")
        except Exception as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"Error: {e}")


def main() -> int:
    return CheckLogErrors().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
