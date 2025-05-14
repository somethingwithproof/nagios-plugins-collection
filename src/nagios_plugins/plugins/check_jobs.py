#!/usr/bin/env python3
"""
Job Status Check Plugin for Nagios.

This plugin checks the status of jobs by querying a JSON API endpoint.
It validates root status and component statuses to determine overall health.

Usage:
    check_jobs.py --url URL [--timeout SECONDS] [--json] [--verbose]

Returns:
    0 (OK): All jobs and components are healthy
    1 (WARNING): Some jobs or components have warnings
    2 (CRITICAL): Critical issues with jobs or components
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import json
import logging
import sys

import httpx
from rich.console import Console
from rich.logging import RichHandler

from nagios_plugins.base import Status, CheckResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("check_jobs")


class JobStatusChecker:
    """Job status checker."""

    def __init__(
        self,
        url: str,
        timeout: int = 30,
    ):
        """Initialize the job status checker.

        Args:
            url: URL to the jobs status API
            timeout: HTTP request timeout in seconds
        """
        self.url = url
        self.timeout = timeout
        self.console = Console()

    async def check_jobs(self) -> CheckResult:
        """Check the job statuses.

        Returns:
            CheckResult with the check result
        """
        try:
            # Make request to the jobs API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.url)
                response.raise_for_status()

                # Parse the JSON response
                data = response.json()

            # Check the overall status
            root_status = data.get("status", "unknown").lower()
            root_title = data.get("title", "Jobs")
            root_message = data.get("message", "").replace("\n", "; ")

            # Create metrics
            metrics = {"root_status": 1 if root_status == "ok" else 0}
            failed_components = []

            # Check if overall status is OK
            if root_status != "ok":
                return CheckResult(
                    Status.WARNING,
                    f"Root status {root_title} is {root_status.upper()}."
                    f"Message: {root_message}",
                    metrics=metrics,
                    details=json.dumps(data, indent=2),
                )

            # Check each component
            for component in data.get("components", []):
                component_name = component.get("name", "unknown")
                component_status = component.get("status", "unknown").lower()
                component_message = (
                    component.get("message", "").replace("\n", "; ")
                    if component.get("message")
                    else ""
                )

                metrics[f"component_{component_name}_status"] = 1 if component_status == "ok" else 0

                if component_status != "ok":
                    failed_components.append(
                        f"Component {component_name} status {component_status.upper()}:"
                        f" {component_message}"
                    )

            # If any components failed, return a warning
            if failed_components:
                return CheckResult(
                    Status.WARNING,
                    failed_components[0],
                    metrics=metrics,
                    details="\n".join(failed_components),
                )

            # All checks passed
            return CheckResult(
                Status.OK,
                "All jobs and components are healthy",
                metrics=metrics,
            )

        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return CheckResult(
                Status.UNKNOWN,
                f"Failed to connect to jobs API: {str(e)}",
                metrics={"root_status": 0},
            )
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return CheckResult(
                Status.UNKNOWN,
                f"Invalid JSON response from jobs API: {str(e)}",
                metrics={"root_status": 0},
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return CheckResult(
                Status.UNKNOWN,
                f"Unexpected error: {str(e)}",
                metrics={"root_status": 0},
            )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Check job statuses",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL to the jobs status API",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP request timeout in seconds",
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

    # Create checker and run check
    checker = JobStatusChecker(
        url=args.url,
        timeout=args.timeout,
    )

    result = await checker.check_jobs()

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
