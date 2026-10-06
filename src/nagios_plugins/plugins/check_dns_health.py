#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Monitor DNS answers and resolution latency."""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status

try:
    import dns.resolver  # type: ignore

    _DNS_OK = True
except Exception:  # pragma: no cover - optional
    _DNS_OK = False


class CheckDnsHealth(NagiosPlugin):
    """Check DNS recursion/authoritative responsiveness and TCP fallback (optional dnspython)."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--name", required=True, help="Name to resolve")
        self.parser.add_argument("--type", default="A", help="Record type")
        self.parser.add_argument("--server", help="DNS server to query")
        self.parser.add_argument("--tcp", action="store_true", help="Force TCP")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        if not _DNS_OK:
            return CheckResult(Status.UNKNOWN, "dnspython not installed; install [dns] extra")
        try:
            r = dns.resolver.Resolver()
            if args.server:
                r.nameservers = [args.server]
            r.use_edns(0, 0, 1232)
            r.lifetime = args.timeout
            r.timeout = args.timeout
            answer = r.resolve(args.name, args.type, tcp=args.tcp)
            rtt_ms = (
                getattr(answer.response, "time", 0) * 1000
                if getattr(answer, "response", None)
                else 0
            )
            count = len(answer)
            return CheckResult(
                Status.OK,
                f"DNS {args.name} {args.type} answers={count}",
                metrics={"answers": count, "rtt_ms": int(rtt_ms)},
            )
        except dns.resolver.NXDOMAIN:
            return CheckResult(Status.CRITICAL, "NXDOMAIN")
        except dns.exception.Timeout:
            return CheckResult(Status.CRITICAL, "DNS timeout")
        except Exception as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"Error: {e}")


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckDnsHealth().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
