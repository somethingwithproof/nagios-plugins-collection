#!/usr/bin/env python3
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
import json
import logging
import sys
from typing import Dict, List, Optional, Tuple, Any

import httpx
from rich.console import Console
from rich.logging import RichHandler

from nagios_plugins.base import Status, CheckResult
from nagios_plugins.utils import check_http_endpoint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("check_mongodb_health")


class MongoHealthChecker:
    """MongoDB health checker."""

    MODE_CHECKS = {
        1: [("mongrations_current", "Current migrations"), ("search_reachable", "Search service")],
        2: [("search_reachable", "Search service"), ("site_api_reachable", "Site API")],
        3: [("mongrations_current", "Current migrations"), ("search_reachable", "Search service")],
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
        self.console = Console()
        
        # Validate mode
        if mode not in self.MODE_CHECKS:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {list(self.MODE_CHECKS.keys())}")

    async def check(self) -> CheckResult:
        """Perform the MongoDB health check.

        Returns:
            CheckResult with the check result
        """
        try:
            # Normalize URL format
            if not self.url.startswith(("http://", "https://")):
                normalized_url = f"http://{self.url}"
            else:
                normalized_url = self.url
            
            # Get health status using HTTP endpoint check utility
            status, message, response_data = await check_http_endpoint(
                url=normalized_url,
                timeout=self.timeout,
            )
            
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
                    "CRITICAL - MongoDB engine is not alive!",
                    metrics=metrics,
                )
            
            # Verify required checks based on mode
            required_checks = self.MODE_CHECKS[self.mode]
            metrics["check_count"] = len(required_checks)
            
            failing_checks = []
            for check_key, check_name in required_checks:
                metrics[f"check_{check_key}"] = 1 if check_key in response_data and response_data.get(check_key) else 0
                
                if check_key not in response_data or not response_data.get(check_key):
                    failing_checks.append(check_name)
                else:
                    metrics["passing_checks"] += 1
            
            if failing_checks:
                failing_list = ", ".join(failing_checks)
                return CheckResult(
                    Status.CRITICAL,
                    f"CRITICAL - MongoDB checks failing: {failing_list}",
                    metrics=metrics,
                    details=json.dumps(response_data, indent=2),
                )
            
            # All checks passed
            return CheckResult(
                Status.OK,
                f"OK - MongoDB engine alive and all {len(required_checks)} checks passing",
                metrics=metrics,
                details=json.dumps(response_data, indent=2),
            )
                
        except Exception as e:
            logger.exception("Error checking MongoDB health")
            return CheckResult(
                Status.UNKNOWN,
                f"Error checking MongoDB health: {str(e)}",
                metrics={"error": 1},
                details=str(e),
            )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Check MongoDB health status",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    # Required arguments
    parser.add_argument(
        "--url",
        required=True,
        help="URL of the MongoDB health endpoint",
    )
    
    # Optional arguments
    parser.add_argument(
        "--mode",
        type=int,
        default=1,
        choices=[1, 2, 3],
        help="Check mode: 1=Migrations+Search, 2=Search+API, 3=Migrations+Search",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds",
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


def main() -> int:
    """Main function.

    Returns:
        Exit code
    """
    args = parse_args()

    # Set logging level based on verbosity
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)

    # Create checker instance
    checker = MongoHealthChecker(
        url=args.url,
        mode=args.mode,
        timeout=args.timeout,
    )

    # Run the check with asyncio
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    result = loop.run_until_complete(checker.check())

    # Output the result
    if args.json:
        print(result.to_json())
    else:
        print(result)

    return result.status.value


if __name__ == "__main__":
    sys.exit(main())