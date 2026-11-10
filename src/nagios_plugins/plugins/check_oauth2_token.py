#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Verify an OAuth token endpoint and required scopes."""

from __future__ import annotations

import argparse

import httpx

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.services import http


class CheckOAuth2Token(NagiosPlugin):
    """Obtain an OAuth2 token and report time-to-expiry; validate scopes if provided."""

    def __init__(self) -> None:
        """Register the monitoring endpoint and alert arguments."""
        super().__init__()
        self.parser.add_argument("--token-url", required=True)
        self.parser.add_argument("--client-id", required=True)
        self.parser.add_secret_argument(
            "--client-secret",
            env="CHECK_OAUTH2_CLIENT_SECRET",
            help="OAuth2 client secret",
            required=True,
        )
        self.parser.add_argument("--scope", action="append", default=[])
        http.add_http_arguments(self.parser, env_prefix="CHECK_OAUTH2_TOKEN", auth=False)

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Evaluate the configured check and return status and performance data."""
        try:
            with http.client(args) as client:
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
            if not isinstance(data, dict) or not data.get("access_token"):
                return CheckResult(Status.CRITICAL, "Token endpoint returned no access_token")
            scopes = set((data.get("scope") or "").split())
            missing = [s for s in args.scope if s not in scopes]
            metrics: dict[str, int] = {"scope_count": len(scopes)}
            # expires_in is optional (RFC 6749 section 5.1); never report a missing one as 0.
            if data.get("expires_in") is None:
                msg = "Token ok expires_in=unknown"
            else:
                metrics["expires_in"] = int(data["expires_in"])
                msg = f"Token ok expires_in={metrics['expires_in']}s"
            status = Status.OK
            if missing:
                status = Status.WARNING
                msg += f" missing_scopes={','.join(missing)}"
            return CheckResult(status, msg, metrics=metrics)
        except httpx.HTTPError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {http.describe_error(e)}")
        except Exception as e:  # pragma: no cover
            return CheckResult(Status.UNKNOWN, f"Error: {e}")


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckOAuth2Token().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
