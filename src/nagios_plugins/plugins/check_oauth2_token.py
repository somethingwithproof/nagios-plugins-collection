#!/usr/bin/env python3
"""Verify an OAuth token endpoint and required scopes."""

from __future__ import annotations

import argparse

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services.http_tls import add_tls_arguments, tls_verification


class CheckOAuth2Token(NagiosPlugin):
    """Obtain an OAuth2 token and report time-to-expiry; validate scopes if provided."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--token-url", required=True)
        self.parser.add_argument("--client-id", required=True)
        self.parser.add_argument("--client-secret", required=True)
        self.parser.add_argument("--scope", action="append", default=[])
        add_tls_arguments(self.parser)

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            with httpx.Client(
                timeout=args.timeout, verify=tls_verification(args.ca_file)
            ) as client:
                r = client.post(
                    args.token_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": args.client_id,
                        "client_secret": args.client_secret,
                        "scope": " ".join(args.scope) if args.scope else None,
                    },
                )
            r.raise_for_status()
            data = r.json()
            expires_in = int(data.get("expires_in", 0))
            scopes = set((data.get("scope") or "").split())
            missing = [s for s in args.scope if s not in scopes]
            status = Status.OK
            msg = f"Token ok expires_in={expires_in}s"
            if missing:
                status = Status.WARNING
                msg += f" missing_scopes={','.join(missing)}"
            return CheckResult(
                status, msg, metrics={"expires_in": expires_in, "scope_count": len(scopes)}
            )
        except httpx.HTTPError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {e}")
        except Exception as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"Error: {e}")


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckOAuth2Token().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
