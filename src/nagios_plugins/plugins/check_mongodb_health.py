#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""
MongoDB Health Check Plugin for Nagios.

This plugin checks the health of a MongoDB instance by querying its health API
and verifying that required health checks are passing.

Usage:
    check_mongodb_health.py --url URL [--mode MODE] [--timeout SECONDS]
                          [--json] [--verbose]

Returns:
    0 (OK): MongoDB engine is alive and all required checks are passing
    2 (CRITICAL): MongoDB engine is not alive or required checks are failing
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import asyncio
import json
import logging

from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, Status
from nagios_plugins.utils import check_http_endpoint_async

logger = logging.getLogger("check_mongodb_health")


class MongoHealthChecker:
    """MongoDB health checker."""

    SEARCH_SERVICE = "Search service"
    MODE_CHECKS = {
        1: [("mongrations_current", "Current migrations"), ("search_reachable", SEARCH_SERVICE)],
        2: [("search_reachable", SEARCH_SERVICE), ("site_api_reachable", "Site API")],
        3: [("mongrations_current", "Current migrations"), ("search_reachable", SEARCH_SERVICE)],
    }

    def __init__(
        self,
        url: str,
        mode: int = 1,
        timeout: int = 10,
    ):
        """Initialize the MongoDB health checker.

        Args:
            url: URL of the MongoDB health endpoint
            mode: Check mode (1, 2, or 3) determining which checks to verify
            timeout: Request timeout in seconds
        """
        self.url = url
        self.mode = mode
        self.timeout = timeout

        # Validate mode
        if mode not in self.MODE_CHECKS:
            raise ValueError(
                f"Invalid mode: {mode}. Must be one of {list(self.MODE_CHECKS.keys())}"
            )

    async def check(self) -> CheckResult:
        """Perform the MongoDB health check.

        Returns:
            CheckResult with the check result
        """
        try:
            # Normalize URL format
            if not self.url.startswith(("http://", "https://")):
                normalized_url = f"https://{self.url}"
            else:
                normalized_url = self.url

            # Get health status using HTTP endpoint check utility
            async with asyncio.timeout(self.timeout):
                status, message, response_data = await check_http_endpoint_async(url=normalized_url)

            # Create metrics dictionary
            metrics = {
                "engine_alive": 0,
                "check_count": 0,
                "passing_checks": 0,
            }

            # Handle connection failures
            if status != Status.OK or not response_data:
                return CheckResult(
                    Status.CRITICAL,
                    f"Error connecting to MongoDB health endpoint: {message}",
                    metrics=metrics,
                )

            # Check if engine is alive
            engine_alive = response_data.get("alive", False)
            metrics["engine_alive"] = 1 if engine_alive else 0

            if not engine_alive:
                return CheckResult(
                    Status.CRITICAL,
                    "MongoDB engine is not alive!",
                    metrics=metrics,
                )

            # Verify required checks based on mode
            required_checks = self.MODE_CHECKS[self.mode]
            metrics["check_count"] = len(required_checks)

            failing_checks = []
            for check_key, check_name in required_checks:
                metrics[f"check_{check_key}"] = int(bool(response_data.get(check_key)))
                if not response_data.get(check_key):
                    failing_checks.append(check_name)
                else:
                    metrics["passing_checks"] += 1

            if failing_checks:
                failing_list = ", ".join(failing_checks)
                return CheckResult(
                    Status.CRITICAL,
                    f"MongoDB checks failing: {failing_list}",
                    metrics=metrics,
                    details=json.dumps(response_data, indent=2),
                )

            # All checks passed
            return CheckResult(
                Status.OK,
                f"MongoDB engine alive and all {len(required_checks)} checks passing",
                metrics=metrics,
                details=json.dumps(response_data, indent=2),
            )

        except TimeoutError:
            return CheckResult(
                Status.CRITICAL, "MongoDB health request timed out", metrics={"error": 1}
            )
        except Exception as e:
            logger.exception("Error checking MongoDB health")
            return CheckResult(
                Status.UNKNOWN,
                f"Error checking MongoDB health: {str(e)}",
                metrics={"error": 1},
                details=str(e),
            )


class CheckMongodbHealth(AsyncNagiosPlugin):
    """Check MongoDB health status."""

    default_timeout = 10
    has_thresholds = False

    def __init__(self) -> None:
        """Register the health endpoint and mode arguments."""
        super().__init__()
        self.parser.add_argument("--url", required=True, help="URL of the MongoDB health endpoint")
        self.parser.add_argument(
            "--mode",
            type=int,
            default=1,
            choices=[1, 2, 3],
            help="Check mode: 1=Migrations+Search, 2=Search+API, 3=Migrations+Search (default: 1)",
        )

    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Check the configured MongoDB health endpoint."""
        return await MongoHealthChecker(url=args.url, mode=args.mode, timeout=args.timeout).check()


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckMongodbHealth().run()


if __name__ == "__main__":
    raise SystemExit(main())
