#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor recent Elasticsearch or OpenSearch error counts."""

from __future__ import annotations

import argparse
import time
from typing import Any

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services import http


class CheckLogErrors(NagiosPlugin):
    """Search ES/OS for error logs in the last N minutes and threshold count/rate."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--endpoint", required=True, help="ES/OpenSearch endpoint")
        self.parser.add_argument("--index", required=True, help="Index or alias")
        self.parser.add_argument("--minutes", type=int, default=5)
        self.parser.add_argument("--query", default="level:ERROR OR status:[500 TO 599]")
        http.add_http_arguments(self.parser, env_prefix="CHECK_LOG_ERRORS")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
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
            with http.client(args) as client:
                r = client.post(url, json=body)
            r.raise_for_status()
            hits = _total_hits(r.json())
            if hits is None:
                return CheckResult(Status.UNKNOWN, "Search response has no hits.total count")
            status = Status.OK
            if args.critical and hits >= int(args.critical):
                status = Status.CRITICAL
            elif args.warning and hits >= int(args.warning):
                status = Status.WARNING
            return CheckResult(
                status, f"errors={hits} in {args.minutes}m", metrics={"errors": hits}
            )
        except httpx.HTTPError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {http.describe_error(e)}")
        except Exception as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"Error: {e}")


def _total_hits(body: Any) -> int | None:
    """Read ``hits.total`` from an ES 7+/OpenSearch object or an ES 6 integer."""
    total = body.get("hits", {}).get("total") if isinstance(body, dict) else None
    if isinstance(total, dict):
        total = total.get("value")
    if isinstance(total, bool) or not isinstance(total, int):
        return None
    return total


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckLogErrors().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
