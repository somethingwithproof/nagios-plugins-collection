#!/usr/bin/env python3
"""
Hadoop Health Check Plugin for Nagios.

This plugin checks the health of a Hadoop cluster by querying its status API
or using command-line tools. It supports checking various components of the
Hadoop ecosystem and returns appropriate Nagios status codes.

Author: Thomas Vincent
Copyright: © 2025 Thomas Vincent
License: MIT License
"""

import argparse
import asyncio
import json
import logging
import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

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
logger = logging.getLogger("hadoop_health_checker")
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
        }
        if self.details:
            result_dict["details"] = self.details
        return json.dumps(result_dict, indent=2)


class HealthCheck(ABC):
    """Abstract base class for all health checks."""
    
    @abstractmethod
    async def check(self) -> CheckResult:
        """Perform the health check and return the result.
        
        Returns:
            CheckResult: The result of the health check.
        """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check.
        """


class CommandHealthCheck(HealthCheck):
    """Base class for checks that use command-line tools."""
    
    async def execute_command(self, command: List[str]) -> str:
        """Execute a command asynchronously and return its output.
        
        Args:
            command: The command to execute as a list of strings.
            
        Returns:
            str: The command output.
            
        Raises:
            subprocess.CalledProcessError: If the command execution fails.
        """
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=True
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(
                    "Command %s failed with return code %s",
                    ' '.join(command),
                    process.returncode
                )
                logger.error("stderr: %s", stderr)
                raise subprocess.CalledProcessError(
                    process.returncode, command, stdout, stderr
                )
                
            return stdout
        except (subprocess.SubprocessError, OSError, asyncio.TimeoutError) as e:
            logger.error("Error executing command %s: %s", ' '.join(command), str(e))
            raise


class HadoopVersionCheck(CommandHealthCheck):
    """Check Hadoop version."""
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check.
        """
        return "hadoop_version"
    
    async def check(self) -> CheckResult:
        """Check the Hadoop version.
        
        Returns:
            CheckResult: The result of the health check.
        """
        try:
            output = await self.execute_command(['hadoop', 'version'])
            version = output.splitlines()[0].split(' ')[1]
            return CheckResult(
                Status.OK, 
                f"Hadoop version: {version}",
                metrics={"version": version}
            )
        except (subprocess.SubprocessError, OSError) as e:
            logger.exception("Error fetching Hadoop version: %s", str(e))
            return CheckResult(
                Status.UNKNOWN, 
                f"Error fetching Hadoop version: {str(e)}"
            )


class HadoopHealthCommandCheck(CommandHealthCheck):
    """Check Hadoop health using the 'hadoop health' command."""
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check.
        """
        return "hadoop_health"
    
    async def check(self) -> CheckResult:
        """Check the Hadoop health.
        
        Returns:
            CheckResult: The result of the health check.
        """
        try:
            output = await self.execute_command(['hadoop', 'health', '-json'])
            health_data = json.loads(output)
            status = health_data.get('status', 'UNKNOWN')
            message = health_data.get('message', 'No message returned')
            
            # Create metrics from health data
            metrics = {}
            for key, value in health_data.items():
                if isinstance(value, (int, float, bool)) and key != 'status':
                    metrics[key] = value
            
            # Determine Nagios status based on Hadoop status
            if status.upper() == 'GOOD':
                nagios_status = Status.OK
            elif status.upper() == 'CONCERNING':
                nagios_status = Status.WARNING
            elif status.upper() == 'BAD':
                nagios_status = Status.CRITICAL
            else:
                nagios_status = Status.UNKNOWN
                
            return CheckResult(
                nagios_status, 
                message,
                metrics=metrics,
                details=json.dumps(health_data, indent=2)
            )
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON from hadoop health command: %s", str(e))
            return CheckResult(
                Status.UNKNOWN, 
                f"Error decoding JSON from hadoop health command: {str(e)}"
            )
        except (subprocess.SubprocessError, OSError) as e:
            logger.exception("Error checking Hadoop health: %s", str(e))
            return CheckResult(
                Status.UNKNOWN, 
                f"Error checking Hadoop health: {str(e)}"
            )


class HDFSCapacityCheck(CommandHealthCheck):
    """Check HDFS capacity."""
    
    def __init__(self, warning_threshold: int = 90, critical_threshold: int = 95):
        """Initialize the HDFS capacity check.
        
        Args:
            warning_threshold: The warning threshold percentage.
            critical_threshold: The critical threshold percentage.
        """
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check.
        """
        return "hdfs_capacity"
    
    async def check(self) -> CheckResult:
        """Check the HDFS capacity.
        
        Returns:
            CheckResult: The result of the health check.
        """
        try:
            output = await self.execute_command(['hdfs', 'dfsadmin', '-report'])
            
            # Parse the output to find the capacity used percentage
            capacity_used = None
            for line in output.splitlines():
                if "DFS Used%" in line:
                    capacity_used = float(line.split()[-2].strip('%'))
                    break
            
            if capacity_used is None:
                return CheckResult(
                    Status.UNKNOWN, 
                    "Could not determine HDFS capacity"
                )
            
            # Create metrics
            metrics = {"capacity_used_percent": capacity_used}
            
            # Determine status based on thresholds
            if capacity_used > self.critical_threshold:
                return CheckResult(
                    Status.CRITICAL, 
                    f"HDFS capacity is critical: {capacity_used}% used",
                    metrics=metrics
                )
            elif capacity_used > self.warning_threshold:
                return CheckResult(
                    Status.WARNING, 
                    f"HDFS capacity is warning: {capacity_used}% used",
                    metrics=metrics
                )
            
            return CheckResult(
                Status.OK, 
                f"HDFS capacity: {capacity_used}% used",
                metrics=metrics
            )
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            logger.exception("Error checking HDFS capacity: %s", str(e))
            return CheckResult(
                Status.UNKNOWN, 
                f"Error checking HDFS capacity: {str(e)}"
            )


class DataNodeStatusCheck(CommandHealthCheck):
    """Check DataNode status."""
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check.
        """
        return "datanode_status"
    
    async def check(self) -> CheckResult:
        """Check the DataNode status.
        
        Returns:
            CheckResult: The result of the health check.
        """
        try:
            output = await self.execute_command(['hdfs', 'dfsadmin', '-report'])
            
            # Parse the output to find the number of live datanodes
            live_datanodes = None
            for line in output.splitlines():
                if "Live datanodes" in line:
                    live_datanodes = int(line.split(':')[1].strip())
                    break
            
            if live_datanodes is None:
                return CheckResult(
                    Status.UNKNOWN, 
                    "Could not determine DataNode status"
                )
            
            # Create metrics
            metrics = {"live_datanodes": live_datanodes}
            
            # Determine status based on the number of live datanodes
            if live_datanodes == 0:
                return CheckResult(
                    Status.CRITICAL, 
                    "No live DataNodes found",
                    metrics=metrics
                )
            
            return CheckResult(
                Status.OK, 
                f"{live_datanodes} live DataNodes found",
                metrics=metrics
            )
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            logger.exception("Error checking DataNode status: %s", str(e))
            return CheckResult(
                Status.UNKNOWN, 
                f"Error checking DataNode status: {str(e)}"
            )


class APIHealthCheck(HealthCheck):
    """Check Hadoop health using a JSON API."""
    
    def __init__(self, url: str, max_update_minutes: Optional[int] = None):
        """Initialize the API health check.
        
        Args:
            url: The URL of the JSON API.
            max_update_minutes: The maximum allowed time since the last update in minutes.
        """
        self.url = self._normalize_url(url)
        self.max_update_minutes = max_update_minutes
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check.
        """
        return "api_health"
    
    def _normalize_url(self, url: str) -> str:
        """Ensure URL starts with http:// or https://.
        
        Args:
            url: The URL to normalize.
            
        Returns:
            str: The normalized URL.
        """
        if not url.startswith(("http://", "https://")):
            return "http://" + url
        return url
    
    def _check_update_time(self, component: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if component has been updated within the specified time.
        
        Args:
            component: The component to check.
            
        Returns:
            Tuple[bool, str]: A tuple of (is_recent, message).
        """
        if self.max_update_minutes is None:
            return True, ""
            
        try:
            time_from_json = datetime.strptime(component["updated"], "%Y-%m-%d %H:%M:%S")
            time_now = datetime.now()
            time_delta = time_now - time_from_json
            
            minutes_since_update = time_delta.days * 24 * 60 + time_delta.seconds // 60
            
            if minutes_since_update > self.max_update_minutes:
                return False, f'Component "{component["name"]}" has not been updated in {time_delta}'
            return True, ""
        except (KeyError, ValueError) as e:
            return False, f'Error parsing update time for component "{component.get("name", "unknown")}": {str(e)}'
    
    async def check(self) -> CheckResult:
        """Check the Hadoop health using the JSON API.
        
        Returns:
            CheckResult: The result of the health check.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.url, timeout=30.0)
                response.raise_for_status()
                jsondict = response.json()
            
            # Check main status
            if jsondict.get("status", "").lower() != "ok":
                return CheckResult(
                    Status.WARNING, 
                    f'Hadoop: {jsondict.get("status", "unknown")}'
                )
            
            # Check subcomponents
            subcomponents = jsondict.get("subcomponents", [])
            issues = []
            
            # Create metrics
            metrics = {
                "components_total": len(subcomponents),
                "components_ok": 0
            }
            
            for component in subcomponents:
                # Check component status
                if component.get("status", "").lower() != "ok":
                    issues.append(
                        f'Component "{component.get("name", "unknown")}" has status '
                        f'"{component.get("status", "unknown")}" and message: '
                        f'{component.get("message", "No message")}'
                    )
                    continue
                
                # Check update time if required
                is_recent, message = self._check_update_time(component)
                if not is_recent:
                    issues.append(message)
                    continue
                
                # If we get here, the component is OK
                metrics["components_ok"] += 1
            
            if issues:
                return CheckResult(
                    Status.WARNING, 
                    "; ".join(issues),
                    metrics=metrics
                )
            
            update_msg = f'within {self.max_update_minutes} minutes' if self.max_update_minutes else ''
            return CheckResult(
                Status.OK, 
                f'All components have status "ok" and have been updated {update_msg}',
                metrics=metrics
            )
            
        except (httpx.HTTPError, ValueError, KeyError) as e:
            logger.exception("Error checking API health: %s", str(e))
            return CheckResult(
                Status.CRITICAL, 
                f"Could not retrieve or parse JSON data from {self.url}: {str(e)}"
            )


class HealthCheckRunner:
    """Run multiple health checks and aggregate results."""
    
    def __init__(self, checks: List[HealthCheck]):
        """Initialize the health check runner.
        
        Args:
            checks: The list of health checks to run.
        """
        self.checks = checks
    
    async def run_checks(self) -> List[Tuple[str, CheckResult]]:
        """Run all health checks.
        
        Returns:
            List[Tuple[str, CheckResult]]: A list of (check_name, check_result) tuples.
        """
        results = []
        
        # Run checks concurrently
        tasks = [check.check() for check in self.checks]
        check_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for check, result in zip(self.checks, check_results):
            if isinstance(result, Exception):
                logger.error("Error running check %s: %s", check.name, str(result))
                results.append((
                    check.name, 
                    CheckResult(Status.UNKNOWN, f"Check failed: {str(result)}")
                ))
            else:
                results.append((check.name, result))
        
        return results
    
    def get_most_severe_status(self, results: List[Tuple[str, CheckResult]]) -> Status:
        """Get the most severe status from all check results.
        
        Args:
            results: The list of check results.
            
        Returns:
            Status: The most severe status.
        """
        # Find the most severe status
        most_severe = Status.OK
        for _, result in results:
            if result.status.value > most_severe.value:
                most_severe = result.status
        
        return most_severe


class OutputFormatter:
    """Format check results in different formats."""
    
    @staticmethod
    def format_results(results: List[Tuple[str, CheckResult]], output_format: str) -> str:
        """Format results according to the specified output format.
        
        Args:
            results: The list of check results.
            output_format: The output format ('json' or 'text').
            
        Returns:
            str: The formatted results.
        """
        if output_format == 'json':
            result_dict = {
                name: {
                    "status": result.status.name, 
                    "message": result.message,
                    "metrics": result.metrics
                } 
                for name, result in results
            }
            return json.dumps(result_dict, indent=2)
        
        # Default to text format
        return "\n".join([f"[{name}] {result}" for name, result in results])


def create_cli_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser.
    
    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(
        description='Hadoop Health Checker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Add subparsers for different check types
    subparsers = parser.add_subparsers(
        dest='check_type', 
        help='Type of health check to perform'
    )
    
    # Parser for command-line checks
    cmd_parser = subparsers.add_parser(
        'command', 
        help='Check Hadoop health using command-line tools'
    )
    cmd_parser.add_argument(
        '--hdfs-warning', 
        type=int, 
        default=90, 
        help='HDFS warning threshold (default: 90%%)'
    )
    cmd_parser.add_argument(
        '--hdfs-critical', 
        type=int, 
        default=95, 
        help='HDFS critical threshold (default: 95%%)'
    )
    cmd_parser.add_argument(
        '--check', 
        choices=['hadoop', 'hdfs', 'datanode', 'version', 'all'], 
        default='all', 
        help='Select specific checks (default: all)'
    )
    
    # Parser for API checks
    api_parser = subparsers.add_parser(
        'api', 
        help='Check Hadoop health using a JSON API'
    )
    api_parser.add_argument(
        '--url', 
        required=True, 
        help='URL of the JSON API'
    )
    api_parser.add_argument(
        '--update-minutes', 
        type=int, 
        help='Maximum time since last update in minutes'
    )
    
    # Common options
    parser.add_argument(
        '--output', 
        choices=['text', 'json'], 
        default='text', 
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Enable verbose output'
    )
    
    return parser


def setup_command_checks(args: argparse.Namespace) -> List[HealthCheck]:
    """Set up command-line health checks based on command-line arguments.
    
    Args:
        args: The command-line arguments.
        
    Returns:
        List[HealthCheck]: The list of health checks.
    """
    checks = {
        'hadoop': HadoopHealthCommandCheck(),
        'hdfs': HDFSCapacityCheck(
            warning_threshold=args.hdfs_warning, 
            critical_threshold=args.hdfs_critical
        ),
        'datanode': DataNodeStatusCheck(),
        'version': HadoopVersionCheck()
    }
    
    if args.check == 'all':
        return list(checks.values())
    
    return [checks[args.check]]


async def main_async() -> int:
    """Main async function.
    
    Returns:
        int: The exit code.
    """
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Set up health checks
    checks = []
    
    if args.check_type == 'command':
        checks = setup_command_checks(args)
    elif args.check_type == 'api':
        checks = [APIHealthCheck(args.url, args.update_minutes)]
    else:
        parser.print_help()
        return Status.UNKNOWN.value
    
    # Run health checks
    runner = HealthCheckRunner(checks)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Running Hadoop health checks..."),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("check", total=None)
        results = await runner.run_checks()
    
    # Print formatted results
    print(OutputFormatter.format_results(results, args.output))
    
    # Determine exit code based on the most severe status
    most_severe_status = runner.get_most_severe_status(results)
    return most_severe_status.value


def main() -> int:
    """Main function.
    
    Returns:
        int: The exit code.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(main_async())


if __name__ == '__main__':
    sys.exit(main())
