#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Evaluate a Prometheus query against alert thresholds."""

from __future__ import annotations

import argparse

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, PerfData, Status, threshold_check
from nagios_plugins.services.http_tls import add_tls_arguments, tls_verification


class CheckPrometheusQuery(NagiosPlugin):
    """Run a PromQL query and threshold the scalar value."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--server", required=True, help="Prometheus base URL")
        self.parser.add_argument("--query", required=True, help="PromQL query returning a scalar")
        add_tls_arguments(self.parser)

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        url = f"{args.server.rstrip('/')}/api/v1/query"
        try:
            with httpx.Client(
                timeout=args.timeout, verify=tls_verification(args.ca_file)
            ) as client:
                r = client.get(url, params={"query": args.query})
            r.raise_for_status()
            data = r.json()
            if data.get("status") != "success":
                return CheckResult(Status.UNKNOWN, f"Prometheus error: {data}")
            result = data.get("data", {}).get("result", [])
            if not result:
                value = 0.0
            else:
                # Expecting scalar or vector with one sample
                val = result[0].get("value") or result[0].get("scalar") or [None, "0"]
                value = float(val[1])
            status = threshold_check(value, args.warning, args.critical)
            perf = PerfData(value, warning=args.warning, critical=args.critical)
            return CheckResult(status, f"PromQL {args.query}={value}", metrics={"value": perf})
        except httpx.HTTPError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {e}")
        except Exception as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"Error: {e}")


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckPrometheusQuery().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
