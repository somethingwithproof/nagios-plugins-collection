#!/usr/bin/env python3
"""
Component Status Checker for ETL Processes.

This module provides functionality to check the status of ETL components
by querying a JSON API. It follows Google Python Style Guide and implements
modern Python features and best practices.

Author: Thomas Vincent
Copyright: © 2025 Thomas Vincent
License: MIT License
"""

import argparse
import asyncio
import json
import logging
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union, Any

import httpx
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

# Configure logging with rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("check_etl")
console = Console()


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
    timestamp: float = field(default_factory=time.time)
    
    def __str__(self) -> str:
        """Return the string representation of the check result."""
        output = f"{self.status} - {self.message}"
        if self.metrics:
            metrics_str = " ".join(
                f"{key}={value}" for key, value in self.metrics.items()
            )
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
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
        }
        if self.details:
            result_dict["details"] = self.details
        return json.dumps(result_dict, indent=2)


class ComponentStatusChecker:
    """
    A class for checking the status of ETL components by querying a JSON API.
    
    This class follows the Single Responsibility Principle and provides
    methods to check the status of ETL components.
    """

    def __init__(
        self,
        host: str,
        port: int = 80,
        timeout: int = 10,
        use_ssl: bool = False,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """
        Initialize the ComponentStatusChecker.
        
        Args:
            host: Hostname of the ETL API server
            port: Port number of the ETL API server
            timeout: Timeout in seconds for API requests
            use_ssl: Whether to use HTTPS instead of HTTP
            username: Optional username for authentication
            password: Optional password for authentication
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.use_ssl = use_ssl
        self.username = username
        self.password = password
        
        # Construct the base URL
        protocol = "https" if use_ssl else "http"
        self.base_url = f"{protocol}://{host}"
        if port != 80 and port != 443:
            self.base_url += f":{port}"
        
        # Set up authentication
        self.auth = None
        if username and password:
            self.auth = (username, password)

    async def get_component_status(
        self, component: str
    ) -> Tuple[str, Optional[datetime]]:
        """
        Check the status of a component by querying the JSON API.
        
        Args:
            component: Name of the component to check
            
        Returns:
            A tuple of (status, updated) where status is one of ('ok', 'error')
            and updated is the time the component was last updated
        """
        url = f"{self.base_url}/api/component/{component}"
        
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout, auth=self.auth
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse the JSON response
                data = response.json()
                status = data.get("status", "").lower()
                
                # Parse the updated timestamp
                updated = None
                if "updated" in data:
                    try:
                        updated = datetime.fromisoformat(data["updated"])
                    except (ValueError, TypeError):
                        logger.warning(
                            "Invalid timestamp format: %s", data["updated"]
                        )
                
                return status, updated
                
        except httpx.HTTPStatusError as e:
            logger.error("HTTP error: %s", e)
            return "error", None
        except httpx.RequestError as e:
            logger.error("Request error: %s", e)
            return "error", None
        except (json.JSONDecodeError, KeyError) as e:
            logger.error("Error parsing response: %s", e)
            return "error", None
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Unexpected error: %s", e)
            return "error", None

    async def check_components(
        self, components: List[str], threshold_minutes: int
    ) -> CheckResult:
        """
        Check the status of the given components and return a CheckResult.
        
        Args:
            components: List of component names to check
            threshold_minutes: Threshold in minutes for checking component update
            
        Returns:
            A CheckResult object with the check result
        """
        component_statuses = {}
        failed_components = []
        metrics = {}
        
        # Check each component
        for component in components:
            status, updated = await self.get_component_status(component)
            component_statuses[component] = (status, updated)
            
            # Add to metrics
            metrics[f"{component}_status"] = 1 if status == "ok" else 0
            
            # Check status
            if status != "ok":
                failed_components.append(f"{component} (status: {status})")
                continue
            
            # Check update time
            current_time = datetime.now()
            if updated is not None:
                time_diff = current_time - updated
                minutes_diff = time_diff.total_seconds() / 60
                metrics[f"{component}_age_minutes"] = minutes_diff
                
                if minutes_diff > threshold_minutes:
                    failed_components.append(
                        f"{component} (not updated in {minutes_diff:.1f} minutes)"
                    )
            else:
                failed_components.append(f"{component} (no update time)")
        
        # Create the result
        if failed_components:
            return CheckResult(
                status=Status.CRITICAL,
                message=f"Failed components: {', '.join(failed_components)}",
                metrics=metrics,
                details=json.dumps(component_statuses, default=str, indent=2),
            )
        
        return CheckResult(
            status=Status.OK,
            message=f"All {len(components)} components are healthy",
            metrics=metrics,
            details=json.dumps(component_statuses, default=str, indent=2),
        )


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args: Command-line arguments to parse. If None, sys.argv[1:] is used.
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Check ETL component status",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host",
        required=True,
        help="Hostname of the ETL API server",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=80,
        help="Port number of the ETL API server",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout in seconds for API requests",
    )
    parser.add_argument(
        "--ssl",
        action="store_true",
        help="Use HTTPS instead of HTTP",
    )
    parser.add_argument(
        "--username",
        help="Username for authentication",
    )
    parser.add_argument(
        "--password",
        help="Password for authentication",
    )
    parser.add_argument(
        "--components",
        nargs="+",
        required=True,
        help="List of component names to check",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=10,
        help="Threshold in minutes for checking component update",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )
    
    return parser.parse_args(args)


async def main_async(args: Optional[List[str]] = None) -> int:
    """
    Main async function.
    
    Args:
        args: Command-line arguments to parse. If None, sys.argv[1:] is used.
        
    Returns:
        Exit code
    """
    parsed_args = parse_args(args)
    
    # Set logging level based on verbosity
    if parsed_args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif parsed_args.verbose >= 2:
        logger.setLevel(logging.DEBUG)
    
    # Create the checker
    checker = ComponentStatusChecker(
        host=parsed_args.host,
        port=parsed_args.port,
        timeout=parsed_args.timeout,
        use_ssl=parsed_args.ssl,
        username=parsed_args.username,
        password=parsed_args.password,
    )
    
    # Check components
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Checking ETL components..."),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("check", total=None)
        result = await checker.check_components(
            parsed_args.components, parsed_args.threshold
        )
    
    # Output the result
    if parsed_args.json:
        print(result.to_json())
    else:
        print(result)
    
    return result.status.value


def main() -> int:
    """
    Main function.
    
    Returns:
        Exit code
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(main_async())


if __name__ == "__main__":
    sys.exit(main())
