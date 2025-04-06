#!/usr/bin/env python3
"""Utility functions for Nagios plugins.

This module provides utility functions that are used by multiple Nagios plugins.
"""

import json
import os
import re
import socket
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import httpx

from nagios_plugins.base import Status


def execute_command(
    command: List[str], timeout: int = 30, shell: bool = False
) -> Tuple[int, str, str]:
    """Execute a command and return the exit code, stdout, and stderr.

    Args:
        command: The command to execute as a list of strings.
        timeout: The timeout in seconds.
        shell: Whether to execute the command in a shell.

    Returns:
        A tuple of (exit_code, stdout, stderr).

    Raises:
        subprocess.TimeoutExpired: If the command times out.
        subprocess.SubprocessError: If there is an error executing the command.
    """
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate(timeout=timeout)
        return process.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        return 1, stdout, f"Command timed out after {timeout} seconds: {' '.join(command)}"
    except subprocess.SubprocessError as e:
        return 1, "", f"Error executing command: {str(e)}"


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
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return True, None
        return False, f"Port {port} is closed on {host}"
    except socket.gaierror:
        return False, f"Could not resolve hostname: {host}"
    except socket.timeout:
        return False, f"Connection to {host}:{port} timed out"
    except Exception as e:  # pylint: disable=broad-except
        return False, f"Error checking port {port} on {host}: {str(e)}"


def check_http_endpoint(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    expected_status: Optional[int] = 200,
    expected_content: Optional[str] = None,
) -> Tuple[Status, str, Optional[Dict[str, Any]]]:
    """Check an HTTP endpoint.

    Args:
        url: The URL to check.
        method: The HTTP method to use.
        headers: The HTTP headers to send.
        data: The data to send in the request body.
        timeout: The timeout in seconds.
        expected_status: The expected HTTP status code.
        expected_content: A regex pattern to match in the response content.

    Returns:
        A tuple of (status, message, response_data).
    """
    start_time = time.time()
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.request(
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
    value = float(value)
    
    # Convert to bytes based on the unit
    unit_multipliers = {
        "": 1,
        "K": 1024,
        "M": 1024 ** 2,
        "G": 1024 ** 3,
        "T": 1024 ** 4,
        "P": 1024 ** 5,
    }
    
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
    
    format_str = f"{{:.{precision}f}}{{}}".format(value, units[unit_index])
    return format_str


def is_process_running(process_name: str) -> bool:
    """Check if a process is running.

    Args:
        process_name: The name of the process to check.

    Returns:
        True if the process is running, False otherwise.
    """
    if sys.platform == "win32":
        # Windows
        try:
            output = subprocess.check_output(
                ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
                universal_newlines=True,
            )
            return process_name.lower() in output.lower()
        except subprocess.SubprocessError:
            return False
    else:
        # Unix-like
        try:
            subprocess.check_output(["pgrep", "-f", process_name], universal_newlines=True)
            return True
        except subprocess.SubprocessError:
            return False


def get_file_age_seconds(file_path: str) -> int:
    """Get the age of a file in seconds.

    Args:
        file_path: The path to the file.

    Returns:
        The age of the file in seconds.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_mtime = os.path.getmtime(file_path)
    current_time = time.time()
    return int(current_time - file_mtime)
