#!/bin/bash

# Script to automate conventional commits for the Hadoop Health Monitor project
# Usage: ./commit-changes.sh [--no-push]

set -e

# Check if user wants to skip pushing
PUSH=true
if [[ "$1" == "--no-push" ]]; then
  PUSH=false
fi

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Base directory - this should be the root of the repository
# Change this to match your repository structure
REPO_DIR="nagios-plugins-collection"
CHECK_HADOOP_DIR="${REPO_DIR}/check_hadoop"
MODULE_NAME="hadoop_health_monitor"
FULL_MODULE_PATH="${CHECK_HADOOP_DIR}/${MODULE_NAME}"

# Create required directories if they don't exist
echo -e "${BLUE}Creating directory structure...${NC}"
mkdir -p "${FULL_MODULE_PATH}/"{domain/{entities,services,value_objects},application,infrastructure/{command,api,output},adapters/{hadoop,nags},checks,constants}
mkdir -p "${CHECK_HADOOP_DIR}/tests/"{unit/{domain,application,infrastructure,adapters,checks},integration/{hadoop,nags,kubernetes},corner_cases}
mkdir -p "${CHECK_HADOOP_DIR}/docs/source/"{api,examples}
mkdir -p "${REPO_DIR}/.github/workflows"

# Function to make a commit with conventional format
make_commit() {
  local type=$1
  local scope=$2
  local message=$3
  local files=("${@:4}")
  
  # Add specified files
  git add "${files[@]}"
  
  # Format commit message according to conventional commits
  local commit_msg="${type}(${scope}): ${message}"
  
  echo -e "${GREEN}Committing: ${commit_msg}${NC}"
  git commit -m "${commit_msg}"
  
  # Push if requested
  if $PUSH; then
    echo -e "${BLUE}Pushing changes...${NC}"
    git push
  fi
}

# Step 1: Initial project structure
echo -e "${YELLOW}Step 1: Setting up initial project structure${NC}"
touch "${FULL_MODULE_PATH}/__init__.py"
touch "${FULL_MODULE_PATH}/version.py"
echo "__version__ = '0.1.0'" > "${FULL_MODULE_PATH}/version.py"
touch "${FULL_MODULE_PATH}/constants/__init__.py"
touch "${FULL_MODULE_PATH}/domain/__init__.py"
touch "${FULL_MODULE_PATH}/domain/entities/__init__.py"
touch "${FULL_MODULE_PATH}/domain/services/__init__.py"
touch "${FULL_MODULE_PATH}/domain/value_objects/__init__.py"
touch "${FULL_MODULE_PATH}/application/__init__.py"
touch "${FULL_MODULE_PATH}/infrastructure/__init__.py"
touch "${FULL_MODULE_PATH}/infrastructure/command/__init__.py"
touch "${FULL_MODULE_PATH}/infrastructure/api/__init__.py"
touch "${FULL_MODULE_PATH}/infrastructure/output/__init__.py"
touch "${FULL_MODULE_PATH}/adapters/__init__.py"
touch "${FULL_MODULE_PATH}/adapters/hadoop/__init__.py"
touch "${FULL_MODULE_PATH}/adapters/nags/__init__.py"
touch "${FULL_MODULE_PATH}/checks/__init__.py"

make_commit "feat" "structure" "Initialize project structure" \
  "${FULL_MODULE_PATH}/__init__.py" \
  "${FULL_MODULE_PATH}/version.py" \
  "${FULL_MODULE_PATH}/constants/__init__.py" \
  "${FULL_MODULE_PATH}/domain/__init__.py" \
  "${FULL_MODULE_PATH}/domain/entities/__init__.py" \
  "${FULL_MODULE_PATH}/domain/services/__init__.py" \
  "${FULL_MODULE_PATH}/domain/value_objects/__init__.py" \
  "${FULL_MODULE_PATH}/application/__init__.py" \
  "${FULL_MODULE_PATH}/infrastructure/__init__.py" \
  "${FULL_MODULE_PATH}/infrastructure/command/__init__.py" \
  "${FULL_MODULE_PATH}/infrastructure/api/__init__.py" \
  "${FULL_MODULE_PATH}/infrastructure/output/__init__.py" \
  "${FULL_MODULE_PATH}/adapters/__init__.py" \
  "${FULL_MODULE_PATH}/adapters/hadoop/__init__.py" \
  "${FULL_MODULE_PATH}/adapters/nags/__init__.py" \
  "${FULL_MODULE_PATH}/checks/__init__.py"

# Step 2: Create configuration files
echo -e "${YELLOW}Step 2: Creating configuration files${NC}"
cp pyproject.toml "${CHECK_HADOOP_DIR}/pyproject.toml"
cp tox.ini "${CHECK_HADOOP_DIR}/tox.ini"
cp requirements.txt "${CHECK_HADOOP_DIR}/requirements.txt"
cp requirements-dev.txt "${CHECK_HADOOP_DIR}/requirements-dev.txt"

cat > "${CHECK_HADOOP_DIR}/setup.py" << 'EOF'
#!/usr/bin/env python3
from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        packages=find_packages(include=["hadoop_health_monitor", "hadoop_health_monitor.*"]),
        entry_points={
            "console_scripts": [
                "hadoop-health-monitor=hadoop_health_monitor.cli:main",
            ],
        },
    )
EOF

cat > "${CHECK_HADOOP_DIR}/MANIFEST.in" << 'EOF'
include LICENSE
include README.md
include CHANGELOG.md
include requirements.txt
include requirements-dev.txt
recursive-include docs/source *
recursive-exclude docs/build *
recursive-include tests *
EOF

cat > "${CHECK_HADOOP_DIR}/README.md" << 'EOF'
# Hadoop Health Monitor

A comprehensive health monitoring tool for Hadoop clusters, designed for integration with Nagios/NRPE monitoring systems.

## Features

- Command-line health checks using Hadoop tools
- API-based health checks for Hadoop REST APIs
- Customizable thresholds for warnings and alerts
- Multiple output formats (text, JSON)
- Parallel execution of health checks
- Integration with Nagios monitoring system

## Installation

```bash
pip install hadoop-health-monitor
```

## Usage

### Command-line Checks

```bash
hadoop-health-monitor command --check all
```

### API Checks

```bash
hadoop-health-monitor api --url http://hadoop-cluster:8088/ws/v1/cluster/info
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with tox
tox
```

## License

Apache License 2.0
EOF

cat > "${CHECK_HADOOP_DIR}/CHANGELOG.md" << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-03-30

### Added
- Initial release
- Command-line health checks
- API-based health checks
- Integration with Nagios/NRPE
EOF

make_commit "build" "config" "Add project configuration files" \
  "${CHECK_HADOOP_DIR}/pyproject.toml" \
  "${CHECK_HADOOP_DIR}/tox.ini" \
  "${CHECK_HADOOP_DIR}/requirements.txt" \
  "${CHECK_HADOOP_DIR}/requirements-dev.txt" \
  "${CHECK_HADOOP_DIR}/setup.py" \
  "${CHECK_HADOOP_DIR}/MANIFEST.in" \
  "${CHECK_HADOOP_DIR}/README.md" \
  "${CHECK_HADOOP_DIR}/CHANGELOG.md"

# Step 3: Create domain model
echo -e "${YELLOW}Step 3: Creating domain model${NC}"
cat > "${FULL_MODULE_PATH}/constants/status.py" << 'EOF'
"""Status code constants for health checks."""
from enum import Enum, auto


class Status(str, Enum):
    """Status codes for health checks."""
    
    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"
    
    @staticmethod
    def to_exit_code(status: str) -> int:
        """Convert status string to exit code.
        
        Args:
            status: The status string
            
        Returns:
            int: The corresponding exit code
        """
        status_map = {
            Status.OK: 0,
            Status.WARNING: 1,
            Status.CRITICAL: 2,
            Status.UNKNOWN: 3
        }
        return status_map.get(status, 3)  # Default to UNKNOWN exit code
EOF

cat > "${FULL_MODULE_PATH}/domain/entities/check_result.py" << 'EOF'
"""Check result entity."""
from dataclasses import dataclass
from typing import Dict, Any, Optional

from hadoop_health_monitor.constants.status import Status


@dataclass
class CheckResult:
    """Data class to store health check results.
    
    Attributes:
        status: The status of the check (OK, WARNING, CRITICAL, UNKNOWN)
        message: A descriptive message for the check result
        data: Additional data associated with the check result
    """
    
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
    
    def __str__(self) -> str:
        """String representation of the check result.
        
        Returns:
            str: A formatted string representation
        """
        return f"{self.status} - {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert check result to dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the check result
        """
        result = {
            "status": self.status,
            "message": self.message
        }
        
        if self.data:
            result["data"] = self.data
            
        return result
    
    @property
    def exit_code(self) -> int:
        """Get the exit code for this check result.
        
        Returns:
            int: The exit code corresponding to the status
        """
        return Status.to_exit_code(self.status)
EOF

# Add __init__.py files to make proper Python modules
touch "${FULL_MODULE_PATH}/constants/__init__.py"
cat > "${FULL_MODULE_PATH}/constants/__init__.py" << 'EOF'
"""Constants package for Hadoop Health Monitor."""
from hadoop_health_monitor.constants.status import Status

__all__ = ["Status"]
EOF

make_commit "feat" "domain" "Add domain model for check results" \
  "${FULL_MODULE_PATH}/constants/status.py" \
  "${FULL_MODULE_PATH}/constants/__init__.py" \
  "${FULL_MODULE_PATH}/domain/entities/check_result.py"

# Step 4: Create base health check
echo -e "${YELLOW}Step 4: Creating base health check${NC}"
cat > "${FULL_MODULE_PATH}/checks/base.py" << 'EOF'
"""Base class for health checks."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from hadoop_health_monitor.domain.entities.check_result import CheckResult
from hadoop_health_monitor.constants.status import Status


class HealthCheck(ABC):
    """Abstract base class for all health checks.
    
    This class defines the interface that all health checks must implement.
    """
    
    @abstractmethod
    def check(self) -> CheckResult:
        """Perform the health check and return the result.
        
        Returns:
            CheckResult: The result of the health check
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check
        """
        pass
    
    @property
    def description(self) -> str:
        """Return a description of the health check.
        
        Returns:
            str: A description of what this health check evaluates
        """
        return f"Health check for {self.name}"
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about this health check.
        
        Returns:
            Dict[str, Any]: A dictionary containing metadata
        """
        return {
            "name": self.name,
            "description": self.description,
        }


class CommandHealthCheck(HealthCheck):
    """Base class for checks that use command-line tools."""
    
    def __init__(self):
        """Initialize the command health check."""
        self._command_executor = None  # Will be injected
    
    @property
    def command_executor(self):
        """Get the command executor.
        
        Returns:
            CommandExecutor: The command executor
        """
        if self._command_executor is None:
            from hadoop_health_monitor.infrastructure.command.executor import CommandExecutor
            self._command_executor = CommandExecutor()
        return self._command_executor
    
    def execute_command(self, command: List[str], timeout: Optional[int] = 60) -> str:
        """Execute a command and return its output.
        
        Args:
            command: The command to execute as a list of strings
            timeout: The timeout in seconds
            
        Returns:
            str: The command output
            
        Raises:
            RuntimeError: If the command fails to execute
        """
        return self.command_executor.execute(command, timeout=timeout)
EOF

cat > "${FULL_MODULE_PATH}/infrastructure/command/executor.py" << 'EOF'
"""Command execution infrastructure."""
import logging
import subprocess
from typing import List, Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)


class CommandExecutor:
    """Execute shell commands and capture their output."""
    
    def execute(self, command: List[str], timeout: Optional[int] = 60) -> str:
        """Execute a command and return its output.
        
        Args:
            command: The command to execute as a list of strings
            timeout: The timeout in seconds
            
        Returns:
            str: The command output
            
        Raises:
            RuntimeError: If the command fails to execute
        """
        try:
            logger.debug("Executing command: %s", " ".join(command))
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=timeout
            )
            
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            logger.error(
                "Command failed with exit code %d: %s\nStdout: %s\nStderr: %s",
                e.returncode, " ".join(command), e.stdout, e.stderr
            )
            raise RuntimeError(f"Command failed: {e.stderr}")
            
        except subprocess.TimeoutExpired as e:
            logger.error(
                "Command timed out after %d seconds: %s", 
                timeout, " ".join(command)
            )
            raise RuntimeError(f"Command timed out after {timeout} seconds")
            
        except Exception as e:
            logger.error(
                "Error executing command %s: %s", 
                " ".join(command), str(e)
            )
            raise RuntimeError(f"Error executing command: {str(e)}")
EOF

# Add __init__.py to make proper Python modules
cat > "${FULL_MODULE_PATH}/checks/__init__.py" << 'EOF'
"""Health check package for Hadoop Health Monitor."""
from hadoop_health_monitor.checks.base import HealthCheck, CommandHealthCheck

__all__ = ["HealthCheck", "CommandHealthCheck"]
EOF

cat > "${FULL_MODULE_PATH}/infrastructure/command/__init__.py" << 'EOF'
"""Command execution infrastructure package."""
from hadoop_health_monitor.infrastructure.command.executor import CommandExecutor

__all__ = ["CommandExecutor"]
EOF

make_commit "feat" "checks" "Add base health check classes" \
  "${FULL_MODULE_PATH}/checks/base.py" \
  "${FULL_MODULE_PATH}/checks/__init__.py" \
  "${FULL_MODULE_PATH}/infrastructure/command/executor.py" \
  "${FULL_MODULE_PATH}/infrastructure/command/__init__.py"

# Step 5: Create Hadoop-specific checks
echo -e "${YELLOW}Step 5: Creating Hadoop-specific checks${NC}"
cat > "${FULL_MODULE_PATH}/checks/hadoop_version.py" << 'EOF'
"""Hadoop version health check."""
import re
from typing import Optional

from hadoop_health_monitor.checks.base import CommandHealthCheck
from hadoop_health_monitor.domain.entities.check_result import CheckResult
from hadoop_health_monitor.constants.status import Status


class HadoopVersionCheck(CommandHealthCheck):
    """Check Hadoop version."""
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check
        """
        return "hadoop_version"
    
    @property
    def description(self) -> str:
        """Return a description of the health check.
        
        Returns:
            str: A description of what this health check evaluates
        """
        return "Checks the installed Hadoop version"
    
    def check(self) -> CheckResult:
        """Perform the health check and return the result.
        
        Returns:
            CheckResult: The result of the health check
        """
        try:
            output = self.execute_command(['hadoop', 'version'])
            version = self._parse_version(output)
            
            if version:
                return CheckResult(
                    status=Status.OK,
                    message=f"Hadoop version: {version}",
                    data={"version": version}
                )
            else:
                return CheckResult(
                    status=Status.UNKNOWN,
                    message="Unable to parse Hadoop version",
                    data={"raw_output": output}
                )
                
        except Exception as e:
            return CheckResult(
                status=Status.UNKNOWN,
                message=f"Error checking Hadoop version: {str(e)}"
            )
    
    def _parse_version(self, output: str) -> Optional[str]:
        """Parse Hadoop version from command output.
        
        Args:
            output: The output from the hadoop version command
            
        Returns:
            Optional[str]: The parsed version or None if not found
        """
        if not output:
            return None
            
        # Try to match "Hadoop X.Y.Z" pattern
        match = re.search(r'Hadoop\s+(\d+\.\d+\.\d+)', output)
        if match:
            return match.group(1)
            
        # Try to match the first line with version-like content
        lines = output.splitlines()
        if lines:
            parts = lines[0].split()
            for part in parts:
                if re.match(r'\d+\.\d+\.\d+', part):
                    return part
                    
        return None
EOF

cat > "${FULL_MODULE_PATH}/checks/hdfs_capacity.py" << 'EOF'
"""HDFS capacity health check."""
import re
from typing import Optional, Dict, Any, Tuple

from hadoop_health_monitor.checks.base import CommandHealthCheck
from hadoop_health_monitor.domain.entities.check_result import CheckResult
from hadoop_health_monitor.constants.status import Status


class HDFSCapacityCheck(CommandHealthCheck):
    """Check HDFS capacity."""
    
    def __init__(self, warning_threshold: int = 90, critical_threshold: int = 95):
        """Initialize the HDFS capacity check.
        
        Args:
            warning_threshold: The threshold percentage for warning status
            critical_threshold: The threshold percentage for critical status
        """
        super().__init__()
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check
        """
        return "hdfs_capacity"
    
    @property
    def description(self) -> str:
        """Return a description of the health check.
        
        Returns:
            str: A description of what this health check evaluates
        """
        return (f"Checks HDFS capacity usage (warning at {self.warning_threshold}%, "
                f"critical at {self.critical_threshold}%)")
    
    def check(self) -> CheckResult:
        """Perform the health check and return the result.
        
        Returns:
            CheckResult: The result of the health check
        """
        try:
            output = self.execute_command(['hdfs', 'dfsadmin', '-report'])
            capacity_used, details = self._parse_capacity(output)
            
            if capacity_used is None:
                return CheckResult(
                    status=Status.UNKNOWN,
                    message="Could not determine HDFS capacity",
                    data={"raw_output": output}
                )
                
            status = Status.OK
            message = f"HDFS capacity: {capacity_used:.2f}% used"
            
            if capacity_used > self.critical_threshold:
                status = Status.CRITICAL
                message = f"HDFS capacity is critical: {capacity_used:.2f}% used"
            elif capacity_used > self.warning_threshold:
                status = Status.WARNING
                message = f"HDFS capacity is warning: {capacity_used:.2f}% used"
                
            return CheckResult(
                status=status,
                message=message,
                data=details
            )
                
        except Exception as e:
            return CheckResult(
                status=Status.UNKNOWN,
                message=f"Error checking HDFS capacity: {str(e)}"
            )
    
    def _parse_capacity(self, output: str) -> Tuple[Optional[float], Dict[str, Any]]:
        """Parse HDFS capacity from command output.
        
        Args:
            output: The output from the hdfs dfsadmin -report command
            
        Returns:
            Tuple[Optional[float], Dict[str, Any]]: The percentage used and details
        """
        details = {}
        capacity_used = None
        
        if not output:
            return None, details
            
        # Extract capacity information
        for line in output.splitlines():
            # Look for DFS Used%
            if "DFS Used%" in line:
                try:
                    capacity_used = float(line.split()[-2].strip('%'))
                    details["capacity_used_percent"] = capacity_used
                except (ValueError, IndexError):
                    pass
                    
            # Look for total capacity
            elif "Present Capacity" in line or "Configured Capacity" in line:
                try:
                    parts = line.split()
                    if len(parts) >= 3:
                        capacity = parts[-2]
                        unit = parts[-1]
                        details["total_capacity"] = f"{capacity} {unit}"
                except (ValueError, IndexError):
                    pass
                    
            # Look for used capacity
            elif "DFS Used" in line and "DFS Used%" not in line:
                try:
                    parts = line.split()
                    if len(parts) >= 3:
                        used = parts[-2]
                        unit = parts[-1]
                        details["used_capacity"] = f"{used} {unit}"
                except (ValueError, IndexError):
                    pass
                    
        return capacity_used, details
EOF

make_commit "feat" "hadoop" "Add Hadoop-specific health checks" \
  "${FULL_MODULE_PATH}/checks/hadoop_version.py" \
  "${FULL_MODULE_PATH}/checks/hdfs_capacity.py"

# Step 6: Add missing check for DataNode status
echo -e "${YELLOW}Step 6: Adding DataNode status check${NC}"
cat > "${FULL_MODULE_PATH}/checks/datanode_status.py" << 'EOF'
"""DataNode status health check."""
import re
from typing import Optional, Dict, Any, List, Tuple

from hadoop_health_monitor.checks.base import CommandHealthCheck
from hadoop_health_monitor.domain.entities.check_result import CheckResult
from hadoop_health_monitor.constants.status import Status


class DataNodeStatusCheck(CommandHealthCheck):
    """Check DataNode status."""
    
    def __init__(self, min_datanodes: int = 1):
        """Initialize the DataNode status check.
        
        Args:
            min_datanodes: Minimum number of live DataNodes required
        """
        super().__init__()
        self.min_datanodes = min_datanodes
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check
        """
        return "datanode_status"
    
    @property
    def description(self) -> str:
        """Return a description of the health check.
        
        Returns:
            str: A description of what this health check evaluates
        """
        return f"Checks DataNode status (minimum {self.min_datanodes} required)"
    
    def check(self) -> CheckResult:
        """Perform the health check and return the result.
        
        Returns:
            CheckResult: The result of the health check
        """
        try:
            output = self.execute_command(['hdfs', 'dfsadmin', '-report'])
            live_datanodes, details = self._parse_datanodes(output)
            
            if live_datanodes is None:
                return CheckResult(
                    status=Status.UNKNOWN,
                    message="Could not determine DataNode status",
                    data={"raw_output": output}
                )
                
            if live_datanodes == 0:
                return CheckResult(
                    status=Status.CRITICAL,
                    message="No live DataNodes found",
                    data=details
                )
                
            if live_datanodes < self.min_datanodes:
                return CheckResult(
                    status=Status.WARNING,
                    message=f"Only {live_datanodes} live DataNodes found ({self.min_datanodes} required)",
                    data=details
                )
                
            return CheckResult(
                status=Status.OK,
                message=f"{live_datanodes} live DataNodes found",
                data=details
            )
                
        except Exception as e:
            return CheckResult(
                status=Status.UNKNOWN,
                message=f"Error checking DataNode status: {str(e)}"
            )
    
    def _parse_datanodes(self, output: str) -> Tuple[Optional[int], Dict[str, Any]]:
        """Parse DataNode information from command output.
        
        Args:
            output: The output from the hdfs dfsadmin -report command
            
        Returns:
            Tuple[Optional[int], Dict[str, Any]]: Count of live DataNodes and details
        """
        details = {
            "live_datanodes": 0,
            "dead_datanodes": 0,
            "decommissioned_datanodes": 0
        }
        
        if not output:
            return None, details
            
        # Extract DataNode information
        for line in output.splitlines():
            # Look for live DataNodes
            if "Live datanodes" in line or "Live DataNodes" in line:
                try:
                    live_datanodes = int(line.split(':')[1].strip())
                    details["live_datanodes"] = live_datanodes
                except (ValueError, IndexError):
                    pass
                    
            # Look for dead DataNodes
            elif "Dead datanodes" in line or "Dead DataNodes" in line:
                try:
                    dead_datanodes = int(line.split(':')[1].strip())
                    details["dead_datanodes"] = dead_datanodes
                except (ValueError, IndexError):
                    pass
                    
            # Look for decommissioned DataNodes
            elif "Decommissioned datanodes" in line or "Decommissioned DataNodes" in line:
                try:
                    decommissioned_datanodes = int(line.split(':')[1].strip())
                    details["decommissioned_datanodes"] = decommissioned_datanodes
                except (ValueError, IndexError):
                    pass
                    
        return details["live_datanodes"], details
EOF

make_commit "feat" "hadoop" "Add DataNode status check" \
  "${FULL_MODULE_PATH}/checks/datanode_status.py"

# Step 6: Create application services
echo -e "${YELLOW}Step 6: Creating application services${NC}"
cat > "${FULL_MODULE_PATH}/application/check_runner.py" << 'EOF'
"""Health check runner."""
import logging
from typing import List, Tuple, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from hadoop_health_monitor.checks.base import HealthCheck
from hadoop_health_monitor.domain.entities.check_result import CheckResult
from hadoop_health_monitor.constants.status import Status

logger = logging.getLogger(__name__)


class HealthCheckRunner:
    """Run multiple health checks and aggregate results."""
    
    def __init__(self, checks: List[HealthCheck], max_workers: int = 5):
        """Initialize the health check runner.
        
        Args:
            checks: The list of health checks to run
            max_workers: The maximum number of concurrent workers
        """
        self.checks = checks
        self.max_workers = max_workers
    
    def run_checks(self) -> List[Tuple[str, CheckResult]]:
        """Run all health checks in parallel.
        
        Returns:
            List[Tuple[str, CheckResult]]: List of (check name, result) tuples
        """
        results = []
        
        # Run checks in parallel with a thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all checks to the executor
            future_to_check = {
                executor.submit(self._run_check, check): check 
                for check in self.checks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_check):
                check = future_to_check[future]
                try:
                    name, result = future.result()
                    results.append((name, result))
                except Exception as e:
                    logger.error(f"Error running check {check.name}: {str(e)}")
                    results.append((
                        check.name, 
                        CheckResult(
                            Status.UNKNOWN, 
                            f"Check failed: {str(e)}"
                        )
                    ))
        
        return results
    
    def _run_check(self, check: HealthCheck) -> Tuple[str, CheckResult]:
        """Run a single health check.
        
        Args:
            check: The health check to run
            
        Returns:
            Tuple[str, CheckResult]: The check name and result
            
        Raises:
            Exception: If the check fails
        """
        logger.debug(f"Running health check: {check.name}")
        try:
            result = check.check()
            return check.name, result
        except Exception as e:
            logger.error(f"Error in health check {check.name}: {str(e)}")
            raise
    
    def get_most_severe_status(self, results: List[Tuple[str, CheckResult]]) -> str:
        """Get the most severe status from all check results.
        
        Args:
            results: The list of check results
            
        Returns:
            str: The most severe status
        """
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
            current = result.status
            if severity.get(current, 0) > severity.get(most_severe, 0):
                most_severe = current
        
        return most_severe
    
    def summarize_results(self, results: List[Tuple[str, CheckResult]]) -> Dict[str, Any]:
        """Summarize the results of all health checks.
        
        Args:
            results: The list of check results
            
        Returns:
            Dict[str, Any]: A summary of the results
        """
        most_severe = self.get_most_severe_status(results)
        
        # Count results by status
        status_counts = {
            Status.OK: 0,
            Status.WARNING: 0,
            Status.CRITICAL: 0,
            Status.UNKNOWN: 0
        }
        
        for _, result in results:
            status = result.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Create a summary message
        status_messages = []
        for status, count in status_counts.items():
            if count > 0:
                status_messages.append(f"{count} {status}")
                
        summary_message = ", ".join(status_messages)
        
        return {
            "overall_status": most_severe,
            "summary": summary_message,
            "exit_code": Status.to_exit_code(most_severe),
            "checks_by_status": status_counts,
            "total_checks": len(results)
        }
EOF

cat > "${FULL_MODULE_PATH}/infrastructure/output/formatters.py" << 'EOF'
"""Output formatters."""
import json
from typing import List, Tuple, Dict, Any

from hadoop_health_monitor.domain.entities.check_result import CheckResult


class OutputFormatter:
    """Format check results in different formats."""
    
    @staticmethod
    def format_results(
        results: List[Tuple[str, CheckResult]], 
        output_format: str,
        include_summary: bool = True
    ) -> str:
        """Format results according to the specified output format.
        
        Args:
            results: The list of (check name, result) tuples
            output_format: The output format (json, text)
            include_summary: Whether to include a summary
            
        Returns:
            str: The formatted results
        """
        if output_format.lower() == 'json':
            return OutputFormatter.format_json(results, include_summary)
        
        # Default to text format
        return OutputFormatter.format_text(results, include_summary)
    
    @staticmethod
    def format_json(
        results: List[Tuple[str, CheckResult]], 
        include_summary: bool = True
    ) -> str:
        """Format results as JSON.
        
        Args:
            results: The list of (check name, result) tuples
            include_summary: Whether to include a summary
            
        Returns:
            str: The JSON-formatted results
        """
        # Convert results to a dictionary
        result_dict = {
            name: result.to_dict() 
            for name, result in results
        }
        
        # Add summary if requested
        if include_summary and results:
            from hadoop_health_monitor.application.check_runner import HealthCheckRunner
            runner = HealthCheckRunner([])  # Empty runner just for summary
            summary = runner.summarize_results(results)
            result_dict["_summary"] = summary
        
        return json.dumps(result_dict, indent=2)
    
    @staticmethod
    def format_text(
        results: List[Tuple[str, CheckResult]], 
        include_summary: bool = True
    ) -> str:
        """Format results as text.
        
        Args:
            results: The list of (check name, result) tuples
            include_summary: Whether to include a summary
            
        Returns:
            str: The text-formatted results
        """
        lines = []
        
        # Add summary if requested
        if include_summary and results:
            from hadoop_health_monitor.application.check_runner import HealthCheckRunner
            runner = HealthCheckRunner([])  # Empty runner just for summary
            summary = runner.summarize_results(results)
            
            lines.append(f"OVERALL STATUS: {summary['overall_status']}")
            lines.append(f"SUMMARY: {summary['summary']}")
            lines.append("")
        
        # Add individual check results
        for name, result in results:
            lines.append(f"[{name}] {result}")
        
        return "\n".join(lines)
EOF

# Add __init__.py to make proper Python modules
touch "${FULL_MODULE_PATH}/application/__init__.py"
touch "${FULL_MODULE_PATH}/infrastructure/output/__init__.py"

cat > "${FULL_MODULE_PATH}/application/__init__.py" << 'EOF'
"""Application services package."""
EOF

cat > "${FULL_MODULE_PATH}/infrastructure/output/__init__.py" << 'EOF'
"""Output formatting infrastructure package."""
from hadoop_health_monitor.infrastructure.output.formatters import OutputFormatter

__all__ = ["OutputFormatter"]
EOF

make_commit "feat" "application" "Add application services for running checks" \
  "${FULL_MODULE_PATH}/application/check_runner.py" \
  "${FULL_MODULE_PATH}/application/__init__.py" \
  "${FULL_MODULE_PATH}/infrastructure/output/formatters.py" \
  "${FULL_MODULE_PATH}/infrastructure/output/__init__.py"

# Add adapter files
echo -e "${YELLOW}Step 7: Creating API adapters${NC}"
mkdir -p "${FULL_MODULE_PATH}/adapters/hadoop"

cat > "${FULL_MODULE_PATH}/adapters/hadoop/__init__.py" << 'EOF'
"""Hadoop adapter package."""
EOF

cat > "${FULL_MODULE_PATH}/adapters/hadoop/api_adapter.py" << 'EOF'
"""Hadoop API health check adapter."""
import datetime
import logging
from typing import Dict, Tuple, List, Any, Optional

import httpx

from hadoop_health_monitor.checks.base import HealthCheck
from hadoop_health_monitor.domain.entities.check_result import CheckResult
from hadoop_health_monitor.constants.status import Status

logger = logging.getLogger(__name__)


class APIHealthCheck(HealthCheck):
    """Check Hadoop health using a JSON API."""
    
    def __init__(self, url: str, max_update_minutes: Optional[int] = None, timeout: int = 30):
        """Initialize the API health check.
        
        Args:
            url: The URL of the JSON API
            max_update_minutes: Maximum time since last update in minutes
            timeout: HTTP request timeout in seconds
        """
        self.url = self._normalize_url(url)
        self.max_update_minutes = max_update_minutes
        self.timeout = timeout
    
    @property
    def name(self) -> str:
        """Return the name of the health check.
        
        Returns:
            str: The name of the health check
        """
        return "api_health"
    
    @property
    def description(self) -> str:
        """Return a description of the health check.
        
        Returns:
            str: A description of what this health check evaluates
        """
        time_msg = f" with {self.max_update_minutes}m freshness" if self.max_update_minutes else ""
        return f"Checks Hadoop health via API ({self.url}){time_msg}"
    
    def _normalize_url(self, url: str) -> str:
        """Ensure URL starts with http:// or https://.
        
        Args:
            url: The URL to normalize
            
        Returns:
            str: The normalized URL
        """
        if not url.startswith(("http://", "https://")):
            return "http://" + url
        return url
    
    def _check_update_time(self, component: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if component has been updated within the specified time.
        
        Args:
            component: The component data
            
        Returns:
            Tuple[bool, str]: (is_recent, message)
        """
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
        """Perform the health check and return the result.
        
        Returns:
            CheckResult: The result of the health check
        """
        try:
            response = httpx.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            jsondict = response.json()
            
            # Check main status
            if jsondict.get("status", "").lower() != "ok":
                return CheckResult(
                    status=Status.WARNING,
                    message=f'Hadoop: {jsondict.get("status", "unknown")}',
                    data=jsondict
                )
            
            # Check subcomponents
            subcomponents = jsondict.get("subcomponents", [])
            issues = []
            
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
            
            if issues:
                return CheckResult(
                    status=Status.WARNING,
                    message="; ".join(issues),
                    data={"components_with_issues": len(issues), "total_components": len(subcomponents)}
                )
            
            update_msg = f'within {self.max_update_minutes} minutes' if self.max_update_minutes else ''
            return CheckResult(
                status=Status.OK, 
                message=f'All components have status "ok" and have been updated {update_msg}',
                data={"total_components": len(subcomponents)}
            )
            
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return CheckResult(
                status=Status.CRITICAL,
                message=f"Could not retrieve or parse JSON data from {self.url}: {str(e)}"
            )
EOF

# Step 8: Create CLI interface
echo -e "${YELLOW}Step 8: Creating CLI interface${NC}"
cat > "${FULL_MODULE_PATH}/cli.py" << 'EOF'
"""Command-line interface for the Hadoop health monitor."""
import sys
import logging
import argparse
from typing import List, Dict, Any

from hadoop_health_monitor.version import __version__
from hadoop_health_monitor.constants.status import Status
from hadoop_health_monitor.checks.base import HealthCheck
from hadoop_health_monitor.application.check_runner import HealthCheckRunner
from hadoop_health_monitor.infrastructure.output.formatters import OutputFormatter

# Import health checks
from hadoop_health_monitor.checks.hadoop_version import HadoopVersionCheck
from hadoop_health_monitor.checks.hdfs_capacity import HDFSCapacityCheck
from hadoop_health_monitor.adapters.hadoop.api_adapter import APIHealthCheck

logger = logging.getLogger(__name__)


def create_cli_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser.
    
    Returns:
        argparse.ArgumentParser: The argument parser
    """
    parser = argparse.ArgumentParser(
        description='Hadoop Health Monitor',
        epilog='For more information, visit: '
               'https://github.com/thomasvincent/nagios-plugins-collection/tree/master/check_hadoop'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'%(prog)s {__version__}'
    )
    
    # Add subparsers for different check types
    subparsers = parser.add_subparsers(
        dest='check_type', 
        help='Type of health check to perform',
        required=True
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
        help='Maximum time since last update in