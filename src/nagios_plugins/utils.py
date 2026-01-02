#!/usr/bin/env python3
"""Utility functions for Nagios plugins.

This module provides utility functions that are used by multiple Nagios plugins.
"""

from __future__ import annotations

import json
import platform
import re
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from nagios_plugins.base import Status


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


def execute_command(
    command: list[str], timeout: int = 30, shell: bool = False
) -> tuple[int, str, str]:
    """Execute a command and return ``(exit_code, stdout, stderr)``.

    Security: ``shell=True`` is disallowed per project standards and will raise
    ``ValueError``. Callers must pass the command as a list of tokens.

    Args:
        command: The command to execute as a list of strings.
        timeout: The timeout in seconds.
        shell: Present for backward compatibility; must be False.

    Returns:
        Tuple containing the exit code, standard output and standard error.
    """
    if shell:
        raise ValueError("shell=True is disallowed by project security standards")

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return process.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            return (
                1,
                stdout,
                f"Command timed out after {timeout} seconds: {command}",
            )
    except subprocess.SubprocessError as exc:
        return 1, "", f"Error executing command: {exc}"


def check_tcp_port(host: str, port: int, timeout: int = 5) -> tuple[bool, str | None]:
    """Check if a TCP port is open.

    A straightforward implementation that relies on ``socket.socket`` so the
    behaviour can be easily mocked in the unit tests.  It returns ``(True,
    None)`` when the port is open and ``(False, message)`` otherwise.

    Args:
        host: The host to check.
        port: The port to check.
        timeout: Timeout for the connection attempt in seconds.

    Returns:
        Tuple containing a success flag and an optional error message.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        if result == 0:
            return True, None
        return False, f"Port {port} is closed on {host}"
    except socket.gaierror:
        return False, f"Could not resolve hostname: {host}"
    except TimeoutError:
        return False, f"Connection to {host}:{port} timed out"
    except Exception as exc:  # pragma: no cover - defensive
        return False, f"Error checking port {port} on {host}: {exc}"
    finally:
        from contextlib import suppress

        with suppress(Exception):
            sock.close()


async def check_http_endpoint_async(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    data: dict[str, Any] | None = None,
    timeout: int = 30,
    expected_status: int | None = 200,
    expected_content: str | None = None,
    verify_ssl: bool = True,
) -> tuple[Status, str, dict[str, Any] | None]:
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
        async with httpx.AsyncClient(timeout=timeout, verify=verify_ssl) as client:
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
                (
                    "HTTP "
                    f"{response.status_code} - Expected {expected_status} - {url} - "
                    f"{response_time:.2f}ms"
                ),
                None,
            )

        # Check content
        if expected_content and not re.search(expected_content, response.text):
            return (
                Status.CRITICAL,
                f"Content check failed - Pattern not found - {url} - {response_time:.2f}ms",
                None,
            )

        # Try to parse JSON response
        response_data = None
        from contextlib import suppress

        with suppress(json.JSONDecodeError, ValueError):
            response_data = response.json()

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
            f"Request error: {e!s} - {url} - {response_time:.2f}ms",
            None,
        )
    except (OSError, httpx.HTTPError, ValueError, KeyError) as e:
        elapsed_time = time.time() - start_time
        response_time = elapsed_time * 1000  # Convert to milliseconds
        return (
            Status.UNKNOWN,
            f"Error: {e!s} - {url} - {response_time:.2f}ms",
            None,
        )


def check_http_endpoint(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    data: dict[str, Any] | None = None,
    timeout: int = 30,
    expected_status: int | None = 200,
    expected_content: str | None = None,
    verify_ssl: bool = True,
) -> tuple[Status, str, dict[str, Any] | None]:
    """Check an HTTP endpoint synchronously.

    This helper performs an HTTP request using :class:`httpx.Client` and
    returns a tuple of ``(Status, message, response_data)`` to keep the API
    compatible with the unit tests.

    Returns:
        Tuple containing the resulting status, human readable message and
        optional JSON data.
    """
    start_time = time.time()
    try:
        with httpx.Client(timeout=timeout, verify=verify_ssl) as client:
            response = client.request(
                method,
                url,
                headers=headers,
                json=data,
                follow_redirects=True,
            )

        elapsed = time.time() - start_time
        response_time = elapsed * 1000

        if expected_status and response.status_code != expected_status:
            return (
                Status.CRITICAL,
                f"HTTP {response.status_code} - Expected {expected_status} - {url} - {response_time:.2f}ms",
                None,
            )

        if expected_content and not re.search(expected_content, response.text):
            return (
                Status.CRITICAL,
                f"Content check failed - Pattern not found - {url} - {response_time:.2f}ms",
                None,
            )

        from contextlib import suppress

        with suppress(json.JSONDecodeError, ValueError):
            response_data = response.json()

        return (
            Status.OK,
            f"HTTP {response.status_code} - {url} - {response_time:.2f}ms",
            response_data,
        )
    except httpx.TimeoutException:
        elapsed = time.time() - start_time
        response_time = elapsed * 1000
        return (
            Status.CRITICAL,
            f"Connection timed out - {url} - {response_time:.2f}ms",
            None,
        )
    except httpx.RequestError as exc:
        elapsed = time.time() - start_time
        response_time = elapsed * 1000
        return (
            Status.CRITICAL,
            f"Request error: {exc} - {url} - {response_time:.2f}ms",
            None,
        )
    except OSError as exc:  # pragma: no cover - defensive
        elapsed = time.time() - start_time
        response_time = elapsed * 1000
        return (
            Status.UNKNOWN,
            f"OS error: {exc} - {url} - {response_time:.2f}ms",
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
    try:
        value = float(value)
    except ValueError as exc:
        raise ValueError(f"Invalid numeric value in size string: {value}") from exc

    # Convert to bytes based on the unit
    unit_multipliers = {
        "": 1,
        "K": 1024,
        "M": 1024**2,
        "G": 1024**3,
        "T": 1024**4,
        "P": 1024**5,
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
    """Check if a process is currently running.

    The implementation uses :func:`subprocess.check_output` so it can be
    easily mocked in the tests.  On Windows it searches the task list, while on
    other platforms it relies on ``pgrep``.
    """

    try:
        if sys.platform.startswith("win"):
            output = subprocess.check_output(
                ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
                universal_newlines=True,
            )
            return process_name.lower() in output.lower()
        else:
            subprocess.check_output(
                ["pgrep", "-f", process_name],
                universal_newlines=True,
            )
            return True
    except subprocess.SubprocessError:
        return False


def get_file_age_seconds(file_path: str | Path) -> int:
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


def get_directory_size(directory: str | Path) -> int:
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


def get_system_info() -> dict[str, Any]:
    """Get system information.

    Returns:
        A dictionary containing system information.
    """
    info: dict[str, Any] = {
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
            with open("/proc/meminfo", encoding="utf-8") as f:
                meminfo = f.read()

            # Extract total memory
            match = re.search(r"MemTotal:\s+(\d+)", meminfo)
            if match:
                info["total_memory_kb"] = int(match.group(1))

            # Extract free memory
            match = re.search(r"MemFree:\s+(\d+)", meminfo)
            if match:
                info["free_memory_kb"] = int(match.group(1))
        except (OSError, FileNotFoundError):
            # Warning: Could not read system memory info
            pass

    return info
