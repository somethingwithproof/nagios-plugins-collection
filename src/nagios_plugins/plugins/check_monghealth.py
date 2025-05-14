#!/usr/bin/env python3
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
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any

import httpx
from rich.console import Console
from rich.logging import RichHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("check_monghealth")


# Define constants for status codes
class Status(Enum):
    """Nagios status codes."""

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __str__(self) -> str:
        """Return the string representation of the status."""
        return self.name


@dataclass
class CheckResult:
    """Data class to store check results."""

    status: Status
    message: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    details: Optional[str] = None

    def __str__(self) -> str:
        """Return the string representation of the check result."""
        output = f"{self.status} - {self.message}"
        if self.metrics:
            metrics_str = " ".join(f"{key}={value}" for key, value in self.metrics.items())
            output += f" | {metrics_str}"
        if self.details:
            output += f"\n{self.details}"
        return output

    def to_json(self) -> str:
        """Convert the check result to a JSON string."""
        result_dict = {
            "status": self.status.name,
            "message": self.message,
            "metrics": self.metrics,
        }
        if self.details:
            result_dict["details"] = self.details
        return json.dumps(result_dict, indent=2)


class MongoHealthChecker:
    """MongoDB health checker."""

    def __init__(
        self,
        host: str,
        port: int = 27017,
        timeout: int = 5,
        username: Optional[str] = None,
        password: Optional[str] = None,
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
        self.console = Console()

        # Construct the base URL
        protocol = "https" if ssl else "http"
        self.base_url = f"{protocol}://{host}:{port}"

        # Set up authentication
        self.auth = None
        if username and password:
            self.auth = (username, password)

    async def check_engine_status(self) -> Tuple[bool, Dict[str, Any]]:
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
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return False, {}
        except Exception as e:
            logger.error(f"Error checking engine status: {e}")
            return False, {}

    async def check_components(self, required_components: List[Tuple[str, bool]]) -> CheckResult:
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
    parser = argparse.ArgumentParser(
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
    parser.add_argument(
        "--password",
        help="MongoDB password",
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


async def main_async() -> int:
    """Main async function.

    Returns:
        Exit code
    """
    args = parse_args()

    # Set logging level based on verbosity
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)

    # Define check modes
    check_modes = {
        1: [("mongrations_current", True), ("search_reachable", True)],
        2: [("search_reachable", True), ("site_api_reachable", True)],
        3: [
            ("mongrations_current", True),
            ("search_reachable", True),
            ("site_api_reachable", True),
        ],
    }

    # Create the MongoDB health checker
    checker = MongoHealthChecker(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        username=args.username,
        password=args.password,
        ssl=args.ssl,
    )

    # Check MongoDB health
    result = await checker.check_components(check_modes[args.mode])

    # Output the result
    if args.json:
        print(result.to_json())
    else:
        print(result)

    return result.status.value


def main() -> int:
    """Main function.

    Returns:
        Exit code
    """
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(main_async())


if __name__ == "__main__":
    sys.exit(main())
