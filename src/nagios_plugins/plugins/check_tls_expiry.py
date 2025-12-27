#!/usr/bin/env python3
"""TLS expiry checker."""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services.tls import days_remaining, fetch_server_cert


class CheckTlsExpiry(NagiosPlugin):
    """Check TLS certificate expiry and basic chain details."""

    def __init__(self) -> None:
        super().__init__()
        self.parser.add_argument("--host", required=True, help="Hostname to check")
        self.parser.add_argument("--port", type=int, default=443, help="Port to connect to")

    def check(self, args: argparse.Namespace) -> CheckResult:
        info = fetch_server_cert(args.host, args.port, timeout=args.timeout)
        remaining = days_remaining(info)
        status = Status.OK
        if args.critical and remaining <= int(args.critical):
            status = Status.CRITICAL
        elif args.warning and remaining <= int(args.warning):
            status = Status.WARNING
        msg = (
            f"TLS cert for {args.host}:{args.port} expires in {remaining}d (SANs={info.san_count})"
        )
        metrics = {"days_remaining": remaining, "san_count": info.san_count}
        return CheckResult(status, msg, metrics=metrics)


def main() -> int:
    return CheckTlsExpiry().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
