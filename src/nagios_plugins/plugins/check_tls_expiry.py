#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""TLS expiry checker."""

from __future__ import annotations

import argparse
import ssl

from nagios_plugins.base import (
    CheckResult,
    NagiosArgumentParser,
    NagiosPlugin,
    PerfData,
    Status,
    ThresholdRange,
    threshold_check,
)
from nagios_plugins.services.http import add_tls_arguments
from nagios_plugins.services.tls import days_remaining, fetch_server_cert


def days(text: str) -> int:
    """Parse a whole number of days for ``-w``/``-c``; Nagios ranges are not accepted."""
    try:
        return int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"expected a whole number of days, not a range: {text!r}"
        ) from None


def at_or_below(limit: int | None) -> str | None:
    """Return the Nagios range that alerts when a value is ``limit`` or less."""
    return None if limit is None else str(ThresholdRange(None, limit, inclusive=True))


class CheckTlsExpiry(NagiosPlugin):
    """Check TLS certificate expiry and basic chain details.

    -w/-c are whole days, not Nagios ranges: the check alerts when the days
    remaining are at or below them, as check_http -C does. Perfdata carries
    them as the equivalent range (for example @~:30).
    """

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--host", required=True, help="Hostname to check")
        self.parser.add_argument("--port", type=int, default=443, help="Port to connect to")
        # Verification is what this check measures, so it cannot be turned off.
        add_tls_arguments(self.parser, insecure=False, client_cert=False)

    def add_threshold_arguments(self, parser: NagiosArgumentParser) -> None:
        """Take thresholds as whole days remaining, as the command always has."""
        parser.add_argument(
            "-w",
            "--warning",
            type=days,
            metavar="DAYS",
            help="WARNING when the certificate expires in DAYS days or fewer (not a range)",
        )
        parser.add_argument(
            "-c",
            "--critical",
            type=days,
            metavar="DAYS",
            help="CRITICAL when the certificate expires in DAYS days or fewer (not a range)",
        )

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            info = fetch_server_cert(
                args.host, args.port, timeout=args.timeout, ca_file=args.ca_file
            )
        except ssl.SSLCertVerificationError as e:
            # An expired, untrusted or mismatched certificate is the failure this check
            # exists to catch, so it is CRITICAL rather than an UNKNOWN handshake error.
            return CheckResult(
                Status.CRITICAL,
                f"TLS certificate for {args.host}:{args.port} failed verification: "
                f"{e.verify_message or e.reason}",
            )
        remaining = days_remaining(info)
        warning, critical = at_or_below(args.warning), at_or_below(args.critical)
        status = threshold_check(remaining, warning, critical)
        msg = (
            f"TLS cert for {args.host}:{args.port} expires in {remaining}d (SANs={info.san_count})"
        )
        metrics = {
            "days_remaining": PerfData(remaining, warning=warning, critical=critical),
            "san_count": info.san_count,
        }
        return CheckResult(status, msg, metrics=metrics)


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckTlsExpiry().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
