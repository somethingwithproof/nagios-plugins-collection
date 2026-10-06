#!/usr/bin/env python3
"""Monitor Kubernetes node readiness."""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services.k8s import summarize_nodes


class CheckK8sNodeStatus(NagiosPlugin):
    """Monitor Kubernetes node readiness."""

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
        msg = f"ready={s.ready} not_ready={s.not_ready} disk={s.disk_pressure} mem={s.memory_pressure} pid={s.pid_pressure}"
        status = Status.OK
        if s.not_ready > 0 or s.disk_pressure or s.memory_pressure or s.pid_pressure:
            status = Status.CRITICAL
        metrics = {
            "ready": s.ready,
            "not_ready": s.not_ready,
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
