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
        body: dict[str, Any] = {
            "size": 0,
            # Without it ES 7+ and OpenSearch stop counting at 10,000.
            "track_total_hits": True,
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
                if _rejects_track_total_hits(r):
                    # Elasticsearch 6 has no such option and always counts exactly.
                    del body["track_total_hits"]
                    r = client.post(url, json=body)
            r.raise_for_status()
            total = _total(r.json())
            if total is None:
                return CheckResult(Status.UNKNOWN, "Search response has no hits.total count")
            hits, relation = total
            if relation != "eq":
                return CheckResult(
                    Status.UNKNOWN,
                    f"Search counted at least {hits} errors in {args.minutes}m "
                    f"(hits.total.relation={relation}); the exact count is unavailable",
                )
            # Nagios ranges: a plain N alerts above N (outside 0..N).
            status = threshold_check(hits, args.warning, args.critical)
            return CheckResult(
                status, f"errors={hits} in {args.minutes}m", metrics={"errors": hits}
            )
        except httpx.HTTPError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {http.describe_error(e)}")
        except Exception as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"Error: {e}")


def _rejects_track_total_hits(response: httpx.Response) -> bool:
    """Return whether the server refused the request for its ``track_total_hits`` key."""
    return response.status_code == 400 and "track_total_hits" in response.text


def _total(body: Any) -> tuple[int, str] | None:
    """Read ``hits.total`` and its relation from ES 7+/OpenSearch or an ES 6 integer.

    ES 6 integers are exact (``eq``). A ``gte`` relation is a lower bound.
    """
    total = body.get("hits", {}).get("total") if isinstance(body, dict) else None
    relation = "eq"
    if isinstance(total, dict):
        relation = total.get("relation", "eq")
        total = total.get("value")
    if isinstance(total, bool) or not isinstance(total, int) or not isinstance(relation, str):
        return None
    return total, relation


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckLogErrors().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
