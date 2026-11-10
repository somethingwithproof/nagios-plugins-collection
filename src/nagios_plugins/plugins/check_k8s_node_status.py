#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor Kubernetes node readiness."""

from __future__ import annotations

import argparse

from nagios_plugins.base import (
    CheckResult,
    NagiosPlugin,
    PerfData,
    Status,
    most_severe,
    threshold_check,
)
from nagios_plugins.services.k8s import summarize_nodes


class CheckK8sNodeStatus(NagiosPlugin):
    """Monitor Kubernetes node readiness.

    -w/-c are Nagios ranges for the number of nodes that are not ready (for
    example -w 0 -c 2). Without them any unready node is CRITICAL. Disk,
    memory or PID pressure on any node is always CRITICAL.
    """

    threshold_metric = "Nagios range for the number of unready nodes"

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--label", dest="label", help="Label selector for nodes")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            s = summarize_nodes(label_selector=args.label, timeout=args.timeout)
        except RuntimeError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        if s.ready + s.not_ready == 0:
            selector = f" matching {args.label!r}" if args.label else ""
            return CheckResult(Status.UNKNOWN, f"No nodes found{selector}")
        msg = f"ready={s.ready} not_ready={s.not_ready} disk={s.disk_pressure} mem={s.memory_pressure} pid={s.pid_pressure}"
        if args.warning is None and args.critical is None:
            readiness = Status.CRITICAL if s.not_ready else Status.OK
        else:
            readiness = threshold_check(s.not_ready, args.warning, args.critical)
        pressure = s.disk_pressure or s.memory_pressure or s.pid_pressure
        status = most_severe(readiness, Status.CRITICAL if pressure else Status.OK)
        metrics = {
            "ready": s.ready,
            "not_ready": PerfData(s.not_ready, warning=args.warning, critical=args.critical),
            "disk_pressure": s.disk_pressure,
            "memory_pressure": s.memory_pressure,
            "pid_pressure": s.pid_pressure,
        }
        return CheckResult(status, msg, metrics=metrics)


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckK8sNodeStatus().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
