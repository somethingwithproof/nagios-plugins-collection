#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor recent Elasticsearch or OpenSearch error counts."""

from __future__ import annotations

import argparse
import time
from typing import Any

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, Status, threshold_check
from nagios_plugins.services.http_tls import add_tls_arguments, tls_verification


class CheckLogErrors(NagiosPlugin):
    """Search ES/OS for error logs in the last N minutes and threshold count/rate."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--endpoint", required=True, help="ES/OpenSearch endpoint")
        self.parser.add_argument("--index", required=True, help="Index or alias")
        self.parser.add_argument("--minutes", type=int, default=5)
        self.parser.add_argument("--query", default="level:ERROR OR status:[500 TO 599]")
        add_tls_arguments(self.parser)

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
            with httpx.Client(
                timeout=args.timeout, verify=tls_verification(args.ca_file)
            ) as client:
                r = client.post(url, json=body)
            r.raise_for_status()
            hits = _total_hits(r.json())
            if hits is None:
                return CheckResult(Status.UNKNOWN, "Search response has no hits.total count")
            # Nagios ranges: a plain N alerts above N (outside 0..N).
            status = threshold_check(hits, args.warning, args.critical)
            return CheckResult(
                status, f"errors={hits} in {args.minutes}m", metrics={"errors": hits}
            )
        except httpx.HTTPError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {e}")
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
