#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""
MongoDB Health Check Plugin for Nagios.

This plugin checks the health of a MongoDB instance by querying its status API.
It supports checking various components of the MongoDB engine and returns
appropriate Nagios status codes.

Usage:
    check_monghealth.py --host HOSTNAME [--port PORT] [--timeout SECONDS]
                       [--username USERNAME] [--password PASSWORD] [--ssl]
                       [--mode {1,2,3}] [--json] [--verbose]

Returns:
    0 (OK): All monitored MongoDB components are healthy
    1 (WARNING): Some MongoDB components have minor issues
    2 (CRITICAL): MongoDB is not accessible or has critical issues
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import json
import logging
from typing import Any

import httpx

from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, Status

logger = logging.getLogger("check_monghealth")


class MongoHealthChecker:
    """MongoDB health checker."""

    def __init__(
        self,
        host: str,
        port: int = 27017,
        timeout: int = 5,
        username: str | None = None,
        password: str | None = None,
        ssl: bool = False,
    ):
        """Initialize the MongoDB health checker.

        Args:
            host: MongoDB host
            port: MongoDB port
            timeout: Connection timeout in seconds
            username: MongoDB username
            password: MongoDB password
            ssl: Whether to use SSL
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.username = username
        self.password = password
        self.ssl = ssl

        # Construct the base URL
        protocol = "https" if ssl else "http"
        self.base_url = f"{protocol}://{host}:{port}"

        # Set up authentication
        self.auth = None
        if username and password:
            self.auth = (username, password)

    async def check_engine_status(self) -> tuple[bool, dict[str, Any]]:
        """Check the MongoDB engine status.

        Returns:
            A tuple of (is_alive, status_data)
        """
        url = f"{self.base_url}/api/status"
        try:
            async with httpx.AsyncClient(timeout=self.timeout, auth=self.auth) as client:
                response = await client.get(url)
                response.raise_for_status()

                # Parse the JSON response
                data = response.json()
                is_alive = data.get("alive", False)
                return is_alive, data
        except httpx.HTTPError:
            logger.exception("HTTP request failed")
            return False, {}
        except Exception:
            logger.exception("Engine status check failed")
            return False, {}

    async def check_components(self, required_components: list[tuple[str, bool]]) -> CheckResult:
        """Check the status of MongoDB components.

        Args:
            required_components: List of (component_name, expected_value) tuples

        Returns:
            CheckResult with the check result
        """
        is_alive, data = await self.check_engine_status()

        if not is_alive:
            return CheckResult(
                Status.CRITICAL,
                "MongoDB engine is not alive!",
                metrics={"alive": 0},
            )

        # Check required components
        failed_components = []
        for component, expected_value in required_components:
            if component not in data:
                failed_components.append(f"{component} (missing)")
            elif data[component] != expected_value:
                failed_components.append(
                    f"{component} (expected: {expected_value}, got: {data[component]})"
                )

        # Create metrics
        metrics = {"alive": 1}
        for key, value in data.items():
            if isinstance(value, (int, float, bool)):
                metrics[key] = 1 if value else 0

        if failed_components:
            return CheckResult(
                Status.CRITICAL,
                f"Failed components: {', '.join(failed_components)}",
                metrics=metrics,
                details=json.dumps(data, indent=2),
            )

        return CheckResult(
            Status.OK,
            "All MongoDB components are healthy",
            metrics=metrics,
            details=json.dumps(data, indent=2),
        )


# Components that must report true for each --mode.
CHECK_MODES = {
    1: [("mongrations_current", True), ("search_reachable", True)],
    2: [("search_reachable", True), ("site_api_reachable", True)],
    3: [
        ("mongrations_current", True),
        ("search_reachable", True),
        ("site_api_reachable", True),
    ],
}


class CheckMonghealth(AsyncNagiosPlugin):
    """Check MongoDB health."""

    default_timeout = 5
    has_thresholds = False

    def __init__(self) -> None:
        """Register the status API connection and mode arguments."""
        super().__init__()
        self.parser.add_argument("--host", required=True, help="MongoDB host")
        self.parser.add_argument(
            "--port", type=int, default=27017, help="MongoDB port (default: 27017)"
        )
        self.parser.add_argument("--username", help="MongoDB username")
        self.parser.add_secret_argument(
            "--password", env="CHECK_MONGHEALTH_PASSWORD", help="MongoDB password"
        )
        self.parser.add_argument("--ssl", action="store_true", help="Use SSL")
        self.parser.add_argument(
            "--mode",
            type=int,
            choices=[1, 2, 3],
            default=1,
            help="Check mode (1: basic, 2: extended, 3: full; default: 1)",
        )

    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Check the MongoDB status API for the components of the selected mode."""
        checker = MongoHealthChecker(
            host=args.host,
            port=args.port,
            timeout=args.timeout,
            username=args.username,
            password=args.password,
            ssl=args.ssl,
        )
        return await checker.check_components(CHECK_MODES[args.mode])


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckMonghealth().run()


if __name__ == "__main__":
    raise SystemExit(main())
