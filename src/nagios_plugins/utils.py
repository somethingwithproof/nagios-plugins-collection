#!/usr/bin/env python3
"""Utility functions for Nagios plugins.

This module provides utility functions that are used by multiple Nagios plugins.
"""

import asyncio
import json
import platform
import re
import socket
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from nagios_plugins.base import CheckResult, Status

# Initialize console for rich output
console = Console()


@dataclass
class CommandResult:
    """Data class to store command execution results."""

    exit_code: int
    stdout: str
    stderr: str
    execution_time: float

    @property
    def success(self) -> bool:
        """Check if the command was successful.

        Returns:
            True if the exit code is 0, False otherwise.
        """
        return self.exit_code == 0

    def __str__(self) -> str:
        """Return a string representation of the command result.

        Returns:
            A string representation of the command result.
        """
        result = f"Exit code: {self.exit_code} (Time: {self.execution_time:.2f}s)"
        if self.stdout:
            result += f"\nStdout: {self.stdout[:500]}"
            if len(self.stdout) > 500:
                result += "... (truncated)"
        if self.stderr:
            result += f"\nStderr: {self.stderr[:500]}"
            if len(self.stderr) > 500:
                result += "... (truncated)"
        return result


async def execute_command_async(
    command: List[str], timeout: int = 30, shell: bool = False
) -> CommandResult:
    """Execute a command asynchronously and return the result.

    Args:
        command: The command to execute as a list of strings.
        timeout: The timeout in seconds.
        shell: Whether to execute the command in a shell.

    Returns:
        A CommandResult object containing the exit code, stdout, stderr, and execution time.
    """
    start_time = time.time()
    
    if shell:
        # If shell is True, join the command list into a string
        cmd = " ".join(command) if isinstance(command, list) else command
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=True,
        )
    else:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=True,
        )
    
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        execution_time = time.time() - start_time
        return CommandResult(
            exit_code=process.returncode or 0,
            stdout=stdout,
            stderr=stderr,
            execution_time=execution_time,
        )
    except asyncio.TimeoutError:
        process.kill()
        stdout, stderr = await process.communicate()
        execution_time = time.time() - start_time
        return CommandResult(
            exit_code=1,
            stdout=stdout,
            stderr=f"Command timed out after {timeout} seconds: {' '.join(command)}",
            execution_time=execution_time,
        )
    except Exception as exc:  # pylint: disable=broad-except
        execution_time = time.time() - start_time
        return CommandResult(
            exit_code=1,
            stdout="",
            stderr=f"Error executing command: {str(exc)}",
            execution_time=execution_time,
        )


def execute_command(
    command: List[str], timeout: int = 30, shell: bool = False
) -> CommandResult:
    """Execute a command and return the result.

    Args:
        command: The command to execute as a list of strings.
        timeout: The timeout in seconds.
        shell: Whether to execute the command in a shell.

    Returns:
        A CommandResult object containing the exit code, stdout, stderr, and execution time.
    """
    # Use asyncio to run the async function
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no event loop is available, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Executing command..."),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("execute", total=None)
        result = loop.run_until_complete(
            execute_command_async(command, timeout, shell)
        )
    
    return result


async def check_tcp_port_async(
    host: str, port: int, timeout: int = 5
) -> Tuple[bool, Optional[str]]:
    """Check if a TCP port is open asynchronously.

    Args:
        host: The host to check.
        port: The port to check.
        timeout: The timeout in seconds.

    Returns:
        A tuple of (success, error_message).
    """
    try:
        # Create a future to connect to the host and port
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout,
        )
        writer.close()
        await writer.wait_closed()
        return True, None
    except asyncio.TimeoutError:
        return False, f"Connection to {host}:{port} timed out after {timeout} seconds"
    except socket.gaierror:
        return False, f"Could not resolve hostname: {host}"
    except ConnectionRefusedError:
        return False, f"Connection refused to {host}:{port}"
    except Exception as e:  # pylint: disable=broad-except
        return False, f"Error checking port {port} on {host}: {str(e)}"


def check_tcp_port(
    host: str, port: int, timeout: int = 5
) -> Tuple[bool, Optional[str]]:
    """Check if a TCP port is open.

    Args:
        host: The host to check.
        port: The port to check.
        timeout: The timeout in seconds.

    Returns:
        A tuple of (success, error_message).
    """
    # Use asyncio to run the async function
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no event loop is available, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(check_tcp_port_async(host, port, timeout))


async def check_http_endpoint_async(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    expected_status: Optional[int] = 200,
    expected_content: Optional[str] = None,
    verify_ssl: bool = True,
) -> Tuple[Status, str, Optional[Dict[str, Any]]]:
    """Check an HTTP endpoint asynchronously.

    Args:
        url: The URL to check.
        method: The HTTP method to use.
        headers: The HTTP headers to send.
        data: The data to send in the request body.
        timeout: The timeout in seconds.
        expected_status: The expected HTTP status code.
        expected_content: A regex pattern to match in the response content.
        verify_ssl: Whether to verify SSL certificates.

    Returns:
        A tuple of (status, message, response_data).
    """
    start_time = time.time()
    try:
        async with httpx.AsyncClient(
            timeout=timeout, verify=verify_ssl
        ) as client:
            response = await client.request(
                method,
                url,
                headers=headers,
                json=data,
                follow_redirects=True,
            )
        
        elapsed_time = time.time() - start_time
        response_time = elapsed_time * 1000  # Convert to milliseconds
        
        # Check status code
        if expected_status and response.status_code != expected_status:
            return (
                Status.CRITICAL,
                f"HTTP {response.status_code} - Expected {expected_status} - {url} - {response_time:.2f}ms",
                None,
            )
        
        # Check content
        if expected_content and not re.search(expected_content, response.text):
            return (
                Status.CRITICAL,
                f"Content check failed - Expected pattern not found - {url} - {response_time:.2f}ms",
                None,
            )
        
        # Try to parse JSON response
        response_data = None
        try:
            response_data = response.json()
        except (json.JSONDecodeError, ValueError):
            # Not JSON, that's fine
            pass
        
        return (
            Status.OK,
            f"HTTP {response.status_code} - {url} - {response_time:.2f}ms",
            response_data,
        )
    
    except httpx.TimeoutException:
        elapsed_time = time.time() - start_time
        response_time = elapsed_time * 1000  # Convert to milliseconds
        return (
            Status.CRITICAL,
            f"Connection timed out - {url} - {response_time:.2f}ms",
            None,
        )
    except httpx.RequestError as e:
        elapsed_time = time.time() - start_time
        response_time = elapsed_time * 1000  # Convert to milliseconds
        return (
            Status.CRITICAL,
            f"Request error: {str(e)} - {url} - {response_time:.2f}ms",
            None,
        )
    except Exception as e:  # pylint: disable=broad-except
        elapsed_time = time.time() - start_time
        response_time = elapsed_time * 1000  # Convert to milliseconds
        return (
            Status.UNKNOWN,
            f"Error: {str(e)} - {url} - {response_time:.2f}ms",
            None,
        )


def check_http_endpoint(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    expected_status: Optional[int] = 200,
    expected_content: Optional[str] = None,
    verify_ssl: bool = True,
) -> CheckResult:
    """Check an HTTP endpoint.

    Args:
        url: The URL to check.
        method: The HTTP method to use.
        headers: The HTTP headers to send.
        data: The data to send in the request body.
        timeout: The timeout in seconds.
        expected_status: The expected HTTP status code.
        expected_content: A regex pattern to match in the response content.
        verify_ssl: Whether to verify SSL certificates.

    Returns:
        A CheckResult object containing the status, message, and metrics.
    """
    # Use asyncio to run the async function
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no event loop is available, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    status, message, response_data = loop.run_until_complete(
        check_http_endpoint_async(
            url, method, headers, data, timeout, expected_status, expected_content, verify_ssl
        )
    )
    
    # Create metrics from response data
    metrics = {}
    if response_data and isinstance(response_data, dict):
        # Extract some common metrics if available
        if "time" in response_data:
            metrics["response_time"] = response_data["time"]
        if "status" in response_data:
            metrics["status"] = response_data["status"]
    
    # Add response time to metrics if not already present
    if "response_time" not in metrics:
        # Extract response time from message
        match = re.search(r"(\d+\.\d+)ms", message)
        if match:
            metrics["response_time"] = float(match.group(1))
    
    return CheckResult(
        status=status,
        message=message,
        metrics=metrics,
        details=json.dumps(response_data, indent=2) if response_data else None,
    )


def parse_size_string(size_str: str) -> int:
    """Parse a size string (e.g., '1.5G', '100M') into bytes.

    Args:
        size_str: The size string to parse.

    Returns:
        The size in bytes.

    Raises:
        ValueError: If the size string is invalid.
    """
    size_str = size_str.strip().upper()
    if not size_str:
        raise ValueError("Empty size string")
    
    # Extract the numeric part and the unit
    match = re.match(r"^([\d.]+)([KMGTP]?)B?$", size_str)
    if not match:
        raise ValueError(f"Invalid size string: {size_str}")
    
    value, unit = match.groups()
    try:
        value = float(value)
    except ValueError as exc:
        raise ValueError(f"Invalid numeric value in size string: {value}") from exc
    
    # Convert to bytes based on the unit
    unit_multipliers = {
        "": 1,
        "K": 1024,
        "M": 1024 ** 2,
        "G": 1024 ** 3,
        "T": 1024 ** 4,
        "P": 1024 ** 5,
    }
    
    if unit not in unit_multipliers:
        raise ValueError(f"Invalid unit in size string: {unit}")
    
    return int(value * unit_multipliers[unit])


def format_bytes(bytes_value: int, precision: int = 2) -> str:
    """Format bytes into a human-readable string.

    Args:
        bytes_value: The number of bytes.
        precision: The number of decimal places to include.

    Returns:
        A human-readable string representation of the bytes.
    """
    if bytes_value < 0:
        raise ValueError("Bytes value cannot be negative")
    
    if bytes_value == 0:
        return "0B"
    
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    unit_index = 0
    value = float(bytes_value)
    
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    
    return f"{value:.{precision}f}{units[unit_index]}"


def is_process_running(process_name: str) -> bool:
    """Check if a process is running.

    Args:
        process_name: The name of the process to check.

    Returns:
        True if the process is running, False otherwise.
    """
    system = platform.system()
    
    if system == "Windows":
        # Windows
        try:
            result = execute_command(
                ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
                shell=True,
            )
            return process_name.lower() in result.stdout.lower()
        except Exception:  # pylint: disable=broad-except
            return False
    elif system == "Darwin":  # macOS
        try:
            result = execute_command(["pgrep", "-i", process_name])
            return result.success and result.stdout.strip() != ""
        except Exception:  # pylint: disable=broad-except
            return False
    else:
        # Linux and other Unix-like
        try:
            result = execute_command(["pgrep", "-f", process_name])
            return result.success and result.stdout.strip() != ""
        except Exception:  # pylint: disable=broad-except
            return False


def get_file_age_seconds(file_path: Union[str, Path]) -> int:
    """Get the age of a file in seconds.

    Args:
        file_path: The path to the file.

    Returns:
        The age of the file in seconds.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    file_mtime = path.stat().st_mtime
    current_time = time.time()
    return int(current_time - file_mtime)


def get_directory_size(directory: Union[str, Path]) -> int:
    """Get the total size of a directory in bytes.

    Args:
        directory: The path to the directory.

    Returns:
        The total size of the directory in bytes.

    Raises:
        FileNotFoundError: If the directory does not exist.
        NotADirectoryError: If the path is not a directory.
    """
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")
    
    total_size = 0
    for item in path.glob("**/*"):
        if item.is_file():
            total_size += item.stat().st_size
    
    return total_size


def get_system_info() -> Dict[str, Any]:
    """Get system information.

    Returns:
        A dictionary containing system information.
    """
    info = {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
    
    # Add more system-specific information
    if platform.system() == "Linux":
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as f:
                meminfo = f.read()
            
            # Extract total memory
            match = re.search(r"MemTotal:\s+(\d+)", meminfo)
            if match:
                info["total_memory_kb"] = int(match.group(1))
            
            # Extract free memory
            match = re.search(r"MemFree:\s+(\d+)", meminfo)
            if match:
                info["free_memory_kb"] = int(match.group(1))
        except Exception:  # pylint: disable=broad-except
            pass
    
    return info
