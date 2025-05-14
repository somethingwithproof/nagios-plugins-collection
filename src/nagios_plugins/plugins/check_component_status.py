#!/usr/bin/env python3
"""
Component Status Checker Plugin for Nagios.

This plugin checks the status of components by querying a JSON API,
verifying both component status and update freshness.

Usage:
    check_component_status.py --url URL --components COMPONENT [COMPONENT ...]
                             [--warning MINUTES] [--critical MINUTES]
                             [--timeout SECONDS] [--json] [--verbose]

Returns:
    0 (OK): All components are OK and recently updated
    1 (WARNING): Components are OK but not updated recently
    2 (CRITICAL): One or more components are in an error state
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import datetime
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
logger = logging.getLogger("check_component_status")


class ComponentStatusChecker:
    """Component status checker for monitoring API endpoints."""

    def __init__(
        self,
        url: str,
        components: List[str],
        warning_threshold: int = 10,
        critical_threshold: Optional[int] = None,
        timeout: int = 10,
    ):
        """Initialize the component status checker.

        Args:
            url: URL of the API host (without protocol)
            components: List of component names to check
            warning_threshold: Warning threshold in minutes for stale updates
            critical_threshold: Critical threshold in minutes for stale updates
            timeout: Request timeout in seconds
        """
        self.url = url
        self.components = components
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold or warning_threshold * 2
        self.timeout = timeout
        self.console = Console()

    async def get_component_status(self, component: str) -> Tuple[str, Optional[datetime.datetime], Dict[str, Any]]:
        """Check the status of a component by querying the JSON API.

        Args:
            component: Name of the component

        Returns:
            Tuple of (status, updated_time, metrics) where:
            - status is one of ('ok', 'error')
            - updated_time is the datetime when component was last updated
            - metrics is a dictionary of component metrics
        """
        # Ensure URL has proper format
        api_url = f"http://{self.url}/api/component/{component}"
        
        # Use the utility function for HTTP checking
        status, message, response_data = await check_http_endpoint(
            url=api_url,
            timeout=self.timeout,
            expected_status=200,
        )
        
        # Process response
        if status == Status.OK and response_data:
            component_status = response_data.get("status", "").lower()
            
            # Parse updated timestamp
            updated_str = response_data.get("updated")
            updated_time = None
            if updated_str:
                try:
                    updated_time = datetime.datetime.fromisoformat(updated_str)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid timestamp format: {updated_str}")
            
            # Extract metrics
            metrics = {
                "status": component_status,
                "response_time_ms": response_data.get("response_time", 0),
            }
            
            return component_status, updated_time, metrics
        else:
            logger.error(f"Error fetching component status: {message}")
            return "error", None, {"status": "error"}

    async def check(self) -> CheckResult:
        """Perform the component status check.

        Returns:
            CheckResult with the check result
        """
        try:
            # Check all components
            component_statuses = {}
            all_metrics = {}
            critical_components = []
            warning_components = []
            
            # Get current time for freshness checks
            current_time = datetime.datetime.now()
            
            for component in self.components:
                status, updated_time, metrics = await self.get_component_status(component)
                component_statuses[component] = (status, updated_time)
                
                # Add component-specific metrics
                for metric_name, metric_value in metrics.items():
                    all_metrics[f"{component}_{metric_name}"] = metric_value
                
                # Check component status
                if status != "ok":
                    critical_components.append(component)
                    continue
                
                # Check update freshness if we have a timestamp
                if updated_time:
                    minutes_since_update = (current_time - updated_time).total_seconds() / 60
                    all_metrics[f"{component}_minutes_since_update"] = round(minutes_since_update, 2)
                    
                    if minutes_since_update > self.critical_threshold:
                        critical_components.append(component)
                    elif minutes_since_update > self.warning_threshold:
                        warning_components.append(component)
            
            # Add summary metrics
            all_metrics["total_components"] = len(self.components)
            all_metrics["critical_components"] = len(critical_components)
            all_metrics["warning_components"] = len(warning_components)
            all_metrics["ok_components"] = len(self.components) - len(critical_components) - len(warning_components)
            
            # Determine overall status and message
            if critical_components:
                component_list = ", ".join(critical_components)
                return CheckResult(
                    Status.CRITICAL,
                    f"CRITICAL - Components with issues: {component_list}",
                    metrics=all_metrics,
                    details=json.dumps(component_statuses, default=str, indent=2),
                )
            elif warning_components:
                component_list = ", ".join(warning_components)
                return CheckResult(
                    Status.WARNING,
                    f"WARNING - Components not recently updated: {component_list}",
                    metrics=all_metrics,
                    details=json.dumps(component_statuses, default=str, indent=2),
                )
            else:
                return CheckResult(
                    Status.OK,
                    f"OK - All {len(self.components)} components are healthy and recently updated",
                    metrics=all_metrics,
                    details=json.dumps(component_statuses, default=str, indent=2),
                )

        except Exception as e:
            logger.exception("Error checking components")
            return CheckResult(
                Status.UNKNOWN,
                f"Error checking components: {str(e)}",
                metrics={"error": 1},
                details=str(e),
            )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Check component status via JSON API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    # Required arguments
    parser.add_argument(
        "--url",
        required=True,
        help="URL of the API endpoint (without protocol)",
    )
    parser.add_argument(
        "--components",
        required=True,
        nargs="+",
        help="List of component names to check",
    )
    
    # Optional arguments
    parser.add_argument(
        "--warning",
        type=int,
        default=10,
        help="Warning threshold in minutes for stale updates",
    )
    parser.add_argument(
        "--critical",
        type=int,
        help="Critical threshold in minutes for stale updates (default: 2x warning)",
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
    checker = ComponentStatusChecker(
        url=args.url,
        components=args.components,
        warning_threshold=args.warning,
        critical_threshold=args.critical,
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