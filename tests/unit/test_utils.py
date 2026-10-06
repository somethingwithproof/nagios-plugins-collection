# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for the utils module."""

import os
import socket
import subprocess
import time
from unittest.mock import MagicMock, patch

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.utils import (
    check_http_endpoint,
    check_tcp_port,
    execute_command,
    format_bytes,
    get_file_age_seconds,
    is_process_running,
    parse_size_string,
)


class TestExecuteCommand:
    """Tests for the execute_command function."""

    def test_successful_command(self) -> None:
        """Test a successful command execution."""
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.communicate.return_value = ("stdout output", "stderr output")
            mock_process.returncode = 0
            mock_popen.return_value = mock_process

            exit_code, stdout, stderr = execute_command(["echo", "hello"])

            assert exit_code == 0
            assert stdout == "stdout output"
            assert stderr == "stderr output"
            mock_popen.assert_called_once_with(
                ["echo", "hello"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                universal_newlines=True,
            )

    def test_command_timeout(self) -> None:
        """Test a command that times out."""
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.communicate.side_effect = [
                subprocess.TimeoutExpired("cmd", 30),
                ("stdout after timeout", "stderr after timeout"),
            ]
            mock_process.returncode = 1
            mock_popen.return_value = mock_process

            exit_code, stdout, stderr = execute_command(["sleep", "60"], timeout=30)

            assert exit_code == 1
            assert stdout == "stdout after timeout"
            assert "Command timed out after 30 seconds" in stderr

    def test_command_error(self) -> None:
        """Test a command that raises a SubprocessError."""
        with patch("subprocess.Popen") as mock_popen:
            mock_popen.side_effect = subprocess.SubprocessError("Command failed")

            exit_code, stdout, stderr = execute_command(["invalid_command"])

            assert exit_code == 1
            assert stdout == ""
            assert "Error executing command: Command failed" in stderr


class TestCheckTcpPort:
    """Tests for the check_tcp_port function."""

    def test_port_open(self) -> None:
        """Test checking a port that is open."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_sock.connect_ex.return_value = 0
            mock_socket.return_value = mock_sock

            success, error = check_tcp_port("localhost", 80)

            assert success is True
            assert error is None
            mock_sock.connect_ex.assert_called_once_with(("localhost", 80))

    def test_port_closed(self) -> None:
        """Test checking a port that is closed."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_sock.connect_ex.return_value = 1
            mock_socket.return_value = mock_sock

            success, error = check_tcp_port("localhost", 80)

            assert success is False
            assert error is not None
            assert "Port 80 is closed on localhost" in error

    def test_hostname_resolution_error(self) -> None:
        """Test checking a port with a hostname that cannot be resolved."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_sock.connect_ex.side_effect = socket.gaierror("Name resolution error")
            mock_socket.return_value = mock_sock

            success, error = check_tcp_port("invalid_hostname", 80)

            assert success is False
            assert error is not None
            assert "Could not resolve hostname: invalid_hostname" in error

    def test_connection_timeout(self) -> None:
        """Test checking a port that times out."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_sock.connect_ex.side_effect = TimeoutError("Connection timed out")
            mock_socket.return_value = mock_sock

            success, error = check_tcp_port("slow_host", 80)

            assert success is False
            assert error is not None
            assert "Connection to slow_host:80 timed out" in error


class TestCheckHttpEndpoint:
    """Tests for the check_http_endpoint function."""

    def test_successful_request(self) -> None:
        """Test a successful HTTP request."""
        with patch("httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "OK"
            mock_response.json.return_value = {"status": "ok"}
            mock_client.return_value.__enter__.return_value.request.return_value = mock_response

            status, message, data = check_http_endpoint("http://example.com")

            assert status == Status.OK
            assert "HTTP 200" in message
            assert "http://example.com" in message
            assert data == {"status": "ok"}

    def test_unexpected_status_code(self) -> None:
        """Test an HTTP request with an unexpected status code."""
        with patch("httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_client.return_value.__enter__.return_value.request.return_value = mock_response

            status, message, data = check_http_endpoint("http://example.com")

            assert status == Status.CRITICAL
            assert "HTTP 404 - Expected 200" in message
            assert data is None

    def test_content_check_failure(self) -> None:
        """Test an HTTP request with content that doesn't match the expected pattern."""
        with patch("httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "Not what we expected"
            mock_client.return_value.__enter__.return_value.request.return_value = mock_response

            status, message, data = check_http_endpoint(
                "http://example.com", expected_content="Expected pattern"
            )

            assert status == Status.CRITICAL
            assert "Content check failed" in message
            assert data is None

    def test_timeout(self) -> None:
        """Test an HTTP request that times out."""
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.request.side_effect = (
                httpx.TimeoutException("Request timed out")
            )

            status, message, data = check_http_endpoint("http://example.com")

            assert status == Status.CRITICAL
            assert "Connection timed out" in message
            assert data is None

    def test_request_error(self) -> None:
        """Test an HTTP request that raises a RequestError."""
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.request.side_effect = (
                httpx.RequestError("Request failed")
            )

            status, message, data = check_http_endpoint("http://example.com")

            assert status == Status.CRITICAL
            assert "Request error: Request failed" in message
            assert data is None


class TestParseSizeString:
    """Tests for the parse_size_string function."""

    def test_parse_bytes(self) -> None:
        """Test parsing a size string in bytes."""
        assert parse_size_string("1024") == 1024
        assert parse_size_string("1024B") == 1024

    def test_parse_kilobytes(self) -> None:
        """Test parsing a size string in kilobytes."""
        assert parse_size_string("1K") == 1024
        assert parse_size_string("1KB") == 1024
        assert parse_size_string("1.5K") == 1536

    def test_parse_megabytes(self) -> None:
        """Test parsing a size string in megabytes."""
        assert parse_size_string("1M") == 1024**2
        assert parse_size_string("1MB") == 1024**2
        assert parse_size_string("1.5M") == int(1.5 * 1024**2)

    def test_parse_gigabytes(self) -> None:
        """Test parsing a size string in gigabytes."""
        assert parse_size_string("1G") == 1024**3
        assert parse_size_string("1GB") == 1024**3
        assert parse_size_string("1.5G") == int(1.5 * 1024**3)

    def test_parse_terabytes(self) -> None:
        """Test parsing a size string in terabytes."""
        assert parse_size_string("1T") == 1024**4
        assert parse_size_string("1TB") == 1024**4
        assert parse_size_string("1.5T") == int(1.5 * 1024**4)

    def test_parse_petabytes(self) -> None:
        """Test parsing a size string in petabytes."""
        assert parse_size_string("1P") == 1024**5
        assert parse_size_string("1PB") == 1024**5
        assert parse_size_string("1.5P") == int(1.5 * 1024**5)

    def test_invalid_size_string(self) -> None:
        """Test parsing an invalid size string."""
        with pytest.raises(ValueError):
            parse_size_string("")
        with pytest.raises(ValueError):
            parse_size_string("invalid")
        with pytest.raises(ValueError):
            parse_size_string("1X")


class TestFormatBytes:
    """Tests for the format_bytes function."""

    def test_format_bytes(self) -> None:
        """Test formatting bytes."""
        assert format_bytes(0) == "0B"
        assert format_bytes(1023) == "1023.00B"

    def test_format_kilobytes(self) -> None:
        """Test formatting kilobytes."""
        assert format_bytes(1024) == "1.00KB"
        assert format_bytes(1536) == "1.50KB"

    def test_format_megabytes(self) -> None:
        """Test formatting megabytes."""
        assert format_bytes(1024**2) == "1.00MB"
        assert format_bytes(int(1.5 * 1024**2)) == "1.50MB"

    def test_format_gigabytes(self) -> None:
        """Test formatting gigabytes."""
        assert format_bytes(1024**3) == "1.00GB"
        assert format_bytes(int(1.5 * 1024**3)) == "1.50GB"

    def test_format_terabytes(self) -> None:
        """Test formatting terabytes."""
        assert format_bytes(1024**4) == "1.00TB"
        assert format_bytes(int(1.5 * 1024**4)) == "1.50TB"

    def test_format_petabytes(self) -> None:
        """Test formatting petabytes."""
        assert format_bytes(1024**5) == "1.00PB"
        assert format_bytes(int(1.5 * 1024**5)) == "1.50PB"

    def test_format_with_custom_precision(self) -> None:
        """Test formatting with a custom precision."""
        assert format_bytes(1536, precision=0) == "2KB"
        assert format_bytes(1536, precision=1) == "1.5KB"
        assert format_bytes(1536, precision=3) == "1.500KB"

    def test_negative_bytes(self) -> None:
        """Test formatting negative bytes."""
        with pytest.raises(ValueError):
            format_bytes(-1)


class TestIsProcessRunning:
    """Tests for the is_process_running function."""

    @patch("sys.platform", "linux")
    def test_process_running_linux(self) -> None:
        """Test checking if a process is running on Linux."""
        with patch("subprocess.check_output") as mock_check_output:
            mock_check_output.return_value = "12345"
            assert is_process_running("test_process") is True

            mock_check_output.side_effect = subprocess.SubprocessError()
            assert is_process_running("test_process") is False

    @patch("sys.platform", "win32")
    def test_process_running_windows(self) -> None:
        """Test checking if a process is running on Windows."""
        with patch("subprocess.check_output") as mock_check_output:
            mock_check_output.return_value = "test_process.exe"
            assert is_process_running("test_process") is True

            mock_check_output.side_effect = subprocess.SubprocessError()
            assert is_process_running("test_process") is False


class TestGetFileAgeSeconds:
    """Tests for the get_file_age_seconds function."""

    def test_file_age(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        """Test getting the age of a file."""
        # Create a temporary file
        file_path = tmp_path / "test_file.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("test")

        # Set the file's modification time to 1 hour ago
        mtime = time.time() - 3600
        os.utime(file_path, (mtime, mtime))

        # Check the file age
        age = get_file_age_seconds(file_path)
        assert 3590 <= age <= 3610  # Allow for small timing differences

    def test_file_not_found(self) -> None:
        """Test getting the age of a file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            get_file_age_seconds("/path/to/nonexistent/file")
