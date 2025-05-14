#!/usr/bin/env python3
"""
Hadoop Cluster Health Check Plugin for Nagios.

This plugin checks the health of a Hadoop cluster by querying its JSON status API.
It validates component statuses and can check the freshness of component updates.

Usage:
    check_hadoop.py --url URL [--max-update-minutes MINUTES] [--json] [--verbose]

Returns:
    0 (OK): All Hadoop components are healthy and within time thresholds
    1 (WARNING): Some components have minor issues or have not been updated recently
    2 (CRITICAL): Critical issues with Hadoop components or API
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from typing import Optional

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
logger = logging.getLogger("check_hadoop")


class HadoopClusterChecker:
    """Hadoop cluster health checker."""

    def __init__(
        self,
        url: str,
        max_update_minutes: Optional[int] = None,
        timeout: int = 30,
    ):
        """Initialize the Hadoop cluster health checker.

        Args:
            url: URL to the Hadoop cluster status API
            max_update_minutes: Maximum allowed minutes since last component update
            timeout: HTTP request timeout in seconds
        """
        self.url = url
        self.max_update_minutes = max_update_minutes
        self.timeout = timeout
        self.console = Console()

    async def check_cluster(self) -> CheckResult:
        """Check the Hadoop cluster status.

        Returns:
            CheckResult with the check result
        """
        try:
            # Make request to the Hadoop API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.url)
                response.raise_for_status()

                # Parse the JSON response
                data = response.json()

            # Check the overall status
            if data.get("status", "").lower() != "ok":
                return CheckResult(
                    Status.WARNING,
                    f"Hadoop: {data.get('message', 'Status not OK')}",
                    metrics={"status": 0},
                    details=json.dumps(data, indent=2),
                )

            # Create basic metrics
            metrics = {"status": 1}
            components_status = []
            stale_components = []

            # Check each subcomponent
            now = datetime.now()
            for component in data.get("subcomponents", []):
                component_name = component.get("name", "unknown")
                component_status = component.get("status", "unknown").lower()
                metrics[f"component_{component_name}_status"] = 1 if component_status == "ok" else 0

                # Check component status
                if component_status != "ok":
                    components_status.append(
                        f"Component '{component_name}' has status '{component_status}': "
                        f"{component.get('message', 'No message')}"
                    )

                # Check component update time if specified
                if self.max_update_minutes and "updated" in component:
                    time_from_json = datetime.strptime(component["updated"], "%Y-%m-%d %H:%M:%S")
                    time_delta = now - time_from_json
                    time_delta_minutes = time_delta.days * 24 * 60 + time_delta.seconds // 60
                    metrics[f"component_{component_name}_minutes_since_update"] = time_delta_minutes

                    if time_delta_minutes > self.max_update_minutes:
                        stale_components.append(
                            f"Component '{component_name}' updated {time_delta_minutes}m ago "
                            f"(max:{self.max_update_minutes}m)"
                        )

            # Get memory information if available
            mem_component = next(
                (c for c in data.get("subcomponents", []) if c.get("name", "").lower() == "mem"),
                None,
            )
            if mem_component:
                mem_message = mem_component.get("message", "").replace("k", "")
                metrics["mem"] = mem_message

            # Evaluate results
            if components_status:
                return CheckResult(
                    Status.WARNING,
                    components_status[0],
                    metrics=metrics,
                    details="\n".join(components_status),
                )

            if stale_components:
                return CheckResult(
                    Status.WARNING,
                    stale_components[0],
                    metrics=metrics,
                    details="\n".join(stale_components),
                )

            # All checks passed
            return CheckResult(
                Status.OK,
                "Hadoop cluster is healthy" 
                + (f", memory: {mem_message}" if "mem_message" in locals() else ""),
                metrics=metrics,
            )

        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return CheckResult(
                Status.CRITICAL,
                f"Failed to connect to Hadoop API: {str(e)}",
                metrics={"status": 0},
            )
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return CheckResult(
                Status.CRITICAL,
                f"Invalid JSON response from Hadoop API: {str(e)}",
                metrics={"status": 0},
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return CheckResult(
                Status.UNKNOWN,
                f"Unexpected error: {str(e)}",
                metrics={"status": 0},
            )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Check Hadoop cluster health",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL to the Hadoop cluster status API",
    )
    parser.add_argument(
        "--max-update-minutes",
        type=int,
        help="Maximum allowed minutes since last component update",
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
    checker = HadoopClusterChecker(
        url=args.url,
        max_update_minutes=args.max_update_minutes,
        timeout=args.timeout,
    )

    result = await checker.check_cluster()

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
