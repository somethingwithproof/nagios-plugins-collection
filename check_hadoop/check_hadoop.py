#!/usr/bin/env python3

import sys
import json
import logging
import argparse
import subprocess
import datetime
from typing import Dict, Tuple, List, Callable, Optional, Any
from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod
import httpx
from dataclasses import dataclass

# Configure logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger("hadoop_health_checker")

# Define constants for status codes
class Status:
    OK = 'OK'
    WARNING = 'WARNING'
    CRITICAL = 'CRITICAL'
    UNKNOWN = 'UNKNOWN'
    
    @staticmethod
    def to_exit_code(status: str) -> int:
        """Convert status string to exit code"""
        status_map = {
            Status.OK: 0,
            Status.WARNING: 1,
            Status.CRITICAL: 2,
            Status.UNKNOWN: 3
        }
        return status_map.get(status, 3)  # Default to UNKNOWN exit code

@dataclass
class CheckResult:
    """Data class to store check results"""
    status: str
    message: str
    
    def __str__(self) -> str:
        return f"{self.status} - {self.message}"

class HealthCheck(ABC):
    """Abstract base class for all health checks"""
    
    @abstractmethod
    def check(self) -> CheckResult:
        """Perform the health check and return the result"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the health check"""
        pass

class CommandHealthCheck(HealthCheck):
    """Base class for checks that use command-line tools"""
    
    def execute_command(self, command: List[str]) -> str:
        """Execute a command and return its output"""
        try:
            return subprocess.check_output(command, stderr=subprocess.PIPE, encoding='utf-8')
        except Exception as e:
            logger.error(f"Error executing command {' '.join(command)}: {str(e)}")
            raise

class HadoopVersionCheck(CommandHealthCheck):
    """Check Hadoop version"""
    
    @property
    def name(self) -> str:
        return "hadoop_version"
    
    def check(self) -> CheckResult:
        try:
            output = self.execute_command(['hadoop', 'version'])
            version = output.splitlines()[0].split(' ')[1]
            return CheckResult(Status.OK, f"Hadoop version: {version}")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Error fetching Hadoop version: {str(e)}")

class HadoopHealthCommandCheck(CommandHealthCheck):
    """Check Hadoop health using the 'hadoop health' command"""
    
    @property
    def name(self) -> str:
        return "hadoop_health"
    
    def check(self) -> CheckResult:
        try:
            output = self.execute_command(['hadoop', 'health', '-json'])
            health_data = json.loads(output)
            status = health_data.get('status', Status.UNKNOWN)
            message = health_data.get('message', 'No message returned')
            return CheckResult(
                Status.OK if status.upper() == 'GOOD' else Status.CRITICAL, 
                message
            )
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Error checking Hadoop health: {str(e)}")

class HDFSCapacityCheck(CommandHealthCheck):
    """Check HDFS capacity"""
    
    def __init__(self, warning_threshold: int = 90, critical_threshold: int = 95):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
    
    @property
    def name(self) -> str:
        return "hdfs_capacity"
    
    def check(self) -> CheckResult:
        try:
            output = self.execute_command(['hdfs', 'dfsadmin', '-report'])
            for line in output.splitlines():
                if "DFS Used%" in line:
                    capacity_used = float(line.split()[-2].strip('%'))
                    if capacity_used > self.critical_threshold:
                        return CheckResult(Status.CRITICAL, f"HDFS capacity is critical: {capacity_used}% used")
                    elif capacity_used > self.warning_threshold:
                        return CheckResult(Status.WARNING, f"HDFS capacity is warning: {capacity_used}% used")
                    return CheckResult(Status.OK, f"HDFS capacity: {capacity_used}% used")
            return CheckResult(Status.UNKNOWN, "Could not determine HDFS capacity")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Error checking HDFS capacity: {str(e)}")

class DataNodeStatusCheck(CommandHealthCheck):
    """Check DataNode status"""
    
    @property
    def name(self) -> str:
        return "datanode_status"
    
    def check(self) -> CheckResult:
        try:
            output = self.execute_command(['hdfs', 'dfsadmin', '-report'])
            for line in output.splitlines():
                if "Live datanodes" in line:
                    live_datanodes = int(line.split(':')[1].strip())
                    if live_datanodes == 0:
                        return CheckResult(Status.CRITICAL, "No live DataNodes found")
                    return CheckResult(Status.OK, f"{live_datanodes} live DataNodes found")
            return CheckResult(Status.UNKNOWN, "Could not determine DataNode status")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Error checking DataNode status: {str(e)}")

class APIHealthCheck(HealthCheck):
    """Check Hadoop health using a JSON API"""
    
    def __init__(self, url: str, max_update_minutes: Optional[int] = None):
        self.url = self._normalize_url(url)
        self.max_update_minutes = max_update_minutes
    
    @property
    def name(self) -> str:
        return "api_health"
    
    def _normalize_url(self, url: str) -> str:
        """Ensure URL starts with http:// or https://"""
        if not url.startswith(("http://", "https://")):
            return "http://" + url
        return url
    
    def _check_update_time(self, component: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if component has been updated within the specified time"""
        if self.max_update_minutes is None:
            return True, ""
            
        try:
            time_from_json = datetime.datetime.strptime(component["updated"], "%Y-%m-%d %H:%M:%S")
            time_now = datetime.datetime.now()
            time_delta = time_now - time_from_json
            
            minutes_since_update = time_delta.days * 24 * 60 + time_delta.seconds // 60
            
            if minutes_since_update > self.max_update_minutes:
                return False, f'Component "{component["name"]}" has not been updated in {time_delta}'
            return True, ""
        except (KeyError, ValueError) as e:
            return False, f'Error parsing update time for component "{component.get("name", "unknown")}": {str(e)}'
    
    def check(self) -> CheckResult:
        try:
            response = httpx.get(self.url, timeout=30.0)
            response.raise_for_status()
            jsondict = response.json()
            
            # Check main status
            if jsondict.get("status", "").lower() != "ok":
                return CheckResult(Status.WARNING, f'Hadoop: {jsondict.get("status", "unknown")}')
            
            # Check subcomponents
            subcomponents = jsondict.get("subcomponents", [])
            issues = []
            
            for component in subcomponents:
                # Check component status
                if component.get("status", "").lower() != "ok":
                    issues.append(
                        f'Component "{component.get("name", "unknown")}" has status "{component.get("status", "unknown")}" '
                        f'and message: {component.get("message", "No message")}'
                    )
                    continue
                
                # Check update time if required
                is_recent, message = self._check_update_time(component)
                if not is_recent:
                    issues.append(message)
            
            if issues:
                return CheckResult(Status.WARNING, "; ".join(issues))
            
            update_msg = f'within {self.max_update_minutes} minutes' if self.max_update_minutes else ''
            return CheckResult(
                Status.OK, 
                f'All components have status "ok" and have been updated {update_msg}'
            )
            
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return CheckResult(Status.CRITICAL, f"Could not retrieve or parse JSON data from {self.url}: {str(e)}")

class HealthCheckRunner:
    """Run multiple health checks and aggregate results"""
    
    def __init__(self, checks: List[HealthCheck]):
        self.checks = checks
    
    def run_checks(self) -> List[Tuple[str, CheckResult]]:
        """Run all health checks in parallel"""
        results = []
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(check.check): check.name for check in self.checks}
            for future in futures:
                try:
                    result = future.result()
                    results.append((futures[future], result))
                except Exception as e:
                    logger.error(f"Error running check {futures[future]}: {str(e)}")
                    results.append((
                        futures[future], 
                        CheckResult(Status.UNKNOWN, f"Check failed: {str(e)}")
                    ))
        
        return results
    
    def get_most_severe_status(self, results: List[Tuple[str, CheckResult]]) -> str:
        """Get the most severe status from all check results"""
        # Define status severity (higher is more severe)
        severity = {
            Status.OK: 0,
            Status.WARNING: 1,
            Status.CRITICAL: 2,
            Status.UNKNOWN: 3
        }
        
        # Find the most severe status
        most_severe = Status.OK
        for _, result in results:
            if severity.get(result.status, 0) > severity.get(most_severe, 0):
                most_severe = result.status
        
        return most_severe

class OutputFormatter:
    """Format check results in different formats"""
    
    @staticmethod
    def format_results(results: List[Tuple[str, CheckResult]], output_format: str) -> str:
        """Format results according to the specified output format"""
        if output_format == 'json':
            result_dict = {
                name: {"status": result.status, "message": result.message} 
                for name, result in results
            }
            return json.dumps(result_dict, indent=2)
        
        # Default to text format
        return "\n".join([f"[{name}] {result}" for name, result in results])

def create_cli_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(description='Hadoop Health Checker')
    
    # Add subparsers for different check types
    subparsers = parser.add_subparsers(dest='check_type', help='Type of health check to perform')
    
    # Parser for command-line checks
    cmd_parser = subparsers.add_parser('command', help='Check Hadoop health using command-line tools')
    cmd_parser.add_argument('--hdfs-warning', type=int, default=90, help='HDFS warning threshold (default: 90%)')
    cmd_parser.add_argument('--hdfs-critical', type=int, default=95, help='HDFS critical threshold (default: 95%)')
    cmd_parser.add_argument('--check', choices=['hadoop', 'hdfs', 'datanode', 'version', 'all'], default='all', 
                          help='Select specific checks (default: all)')
    
    # Parser for API checks
    api_parser = subparsers.add_parser('api', help='Check Hadoop health using a JSON API')
    api_parser.add_argument('--url', required=True, help='URL of the JSON API')
    api_parser.add_argument('--update-minutes', type=int, help='Maximum time since last update in minutes')
    
    # Common options
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format (default: text)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    return parser

def setup_command_checks(args: argparse.Namespace) -> List[HealthCheck]:
    """Set up command-line health checks based on command-line arguments"""
    checks = {
        'hadoop': HadoopHealthCommandCheck(),
        'hdfs': HDFSCapacityCheck(warning_threshold=args.hdfs_warning, critical_threshold=args.hdfs_critical),
        'datanode': DataNodeStatusCheck(),
        'version': HadoopVersionCheck()
    }
    
    if args.check == 'all':
        return list(checks.values())
    
    return [checks[args.check]]

def main() -> None:
    """Main function"""
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
        sys.exit(Status.to_exit_code(Status.UNKNOWN))
    
    # Run health checks
    runner = HealthCheckRunner(checks)
    results = runner.run_checks()
    
    # Print formatted results
    print(OutputFormatter.format_results(results, args.output))
    
    # Determine exit code based on the most severe status
    most_severe_status = runner.get_most_severe_status(results)
    sys.exit(Status.to_exit_code(most_severe_status))

if __name__ == '__main__':
    main()