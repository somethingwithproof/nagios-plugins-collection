#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Evaluate a Prometheus query against alert thresholds."""

from __future__ import annotations

import argparse
from typing import Any

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, PerfData, Status, threshold_check
from nagios_plugins.services import http


class CheckPrometheusQuery(NagiosPlugin):
    """Run a PromQL query and threshold the scalar value."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--server", required=True, help="Prometheus base URL")
        self.parser.add_argument("--query", required=True, help="PromQL query returning a scalar")
        http.add_http_arguments(self.parser, env_prefix="CHECK_PROMETHEUS_QUERY")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        url = f"{args.server.rstrip('/')}/api/v1/query"
        try:
            with http.client(args) as client:
                r = client.get(url, params={"query": args.query})
            r.raise_for_status()
            data = r.json()
            if data.get("status") != "success":
                return CheckResult(Status.UNKNOWN, f"Prometheus error: {data}")
            value = _first_sample(data.get("data", {}))
            if value is None:
                return CheckResult(Status.UNKNOWN, f"PromQL {args.query} returned no samples")
            status = threshold_check(value, args.warning, args.critical)
            perf = PerfData(value, warning=args.warning, critical=args.critical)
            return CheckResult(status, f"PromQL {args.query}={value}", metrics={"value": perf})
        except httpx.HTTPError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {http.describe_error(e)}")
        except Exception as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"Error: {e}")


def _first_sample(data: dict[str, Any]) -> float | None:
    """Return the first sample of a scalar or instant-vector result, if any.

    An empty vector means the series is absent, which is not the same as zero.
    """
    result = data.get("result")
    if data.get("resultType") == "scalar" or (
        isinstance(result, list) and len(result) == 2 and not isinstance(result[0], dict)
    ):
        sample = result
    elif isinstance(result, list) and result and isinstance(result[0], dict):
        sample = result[0].get("value")
    else:
        return None
    if not isinstance(sample, list) or len(sample) != 2:
        return None
    return float(sample[1])


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckPrometheusQuery().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
