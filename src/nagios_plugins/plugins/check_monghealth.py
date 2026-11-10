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
import sys
from typing import Any

import httpx

from nagios_plugins.base import CheckResult, NagiosArgumentParser, Status, run_async_check

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


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = NagiosArgumentParser(
        description="Check MongoDB health",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host",
        required=True,
        help="MongoDB host",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=27017,
        help="MongoDB port",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Connection timeout in seconds",
    )
    parser.add_argument(
        "--username",
        help="MongoDB username",
    )
    parser.add_secret_argument(
        "--password", env="CHECK_MONGHEALTH_PASSWORD", help="MongoDB password"
    )
    parser.add_argument(
        "--ssl",
        action="store_true",
        help="Use SSL",
    )
    parser.add_argument(
        "--mode",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Check mode (1: basic, 2: extended, 3: full)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )

    return parser.parse_args()


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


async def _check(args: argparse.Namespace) -> CheckResult:
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
    return run_async_check(parse_args(), _check)


if __name__ == "__main__":
    sys.exit(main())
