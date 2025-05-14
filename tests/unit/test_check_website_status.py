"""Tests for the check_website_status plugin."""

import asyncio
from unittest.mock import MagicMock, patch

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_website_status import WebsiteStatusChecker


class TestWebsiteStatusChecker:
    """Tests for the WebsiteStatusChecker class."""

    @pytest.fixture
    def checker(self):
        """Create a WebsiteStatusChecker instance."""
        return WebsiteStatusChecker(
            url="https://example.com",
            pattern="Example Domain",
            timeout=10,
            warning_threshold=1.0,
            critical_threshold=2.0,
        )

    @pytest.mark.asyncio
    async def test_check_website_success(self, checker):
        """Test a successful website check."""
        # Mock httpx.AsyncClient
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Example Domain"
        mock_response.elapsed.total_seconds.return_value = 0.5

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_website()

            # Verify result
            assert result.status == Status.OK
            assert "Website OK" in result.message
            assert "0.5s" in result.message
            assert result.metrics["status_code"] == 200
            assert result.metrics["duration"] == 0.5
            assert result.metrics["pattern_found"] == 1

    @pytest.mark.asyncio
    async def test_check_website_warning(self, checker):
        """Test a website check with warning response time."""
        # Mock httpx.AsyncClient
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Example Domain"
        mock_response.elapsed.total_seconds.return_value = 1.5  # Between warning and critical

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_website()

            # Verify result
            assert result.status == Status.WARNING
            assert "exceeds warning threshold" in result.message
            assert result.metrics["status_code"] == 200
            assert result.metrics["duration"] == 1.5

    @pytest.mark.asyncio
    async def test_check_website_critical_response_time(self, checker):
        """Test a website check with critical response time."""
        # Mock httpx.AsyncClient
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Example Domain"
        mock_response.elapsed.total_seconds.return_value = 2.5  # Above critical

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_website()

            # Verify result
            assert result.status == Status.CRITICAL
            assert "exceeds critical threshold" in result.message
            assert result.metrics["status_code"] == 200
            assert result.metrics["duration"] == 2.5

    @pytest.mark.asyncio
    async def test_check_website_error_status_code(self, checker):
        """Test a website check with an error status code."""
        # Mock httpx.AsyncClient
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.elapsed.total_seconds.return_value = 0.5

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_website()

            # Verify result
            assert result.status == Status.CRITICAL
            assert "HTTP 404 error" in result.message
            assert result.metrics["status_code"] == 404
            assert result.metrics["duration"] == 0.5

    @pytest.mark.asyncio
    async def test_check_website_pattern_not_found(self, checker):
        """Test a website check with the pattern not found in the response."""
        # Mock httpx.AsyncClient
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Not what we're looking for"
        mock_response.elapsed.total_seconds.return_value = 0.5

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_website()

            # Verify result
            assert result.status == Status.CRITICAL
            assert "Pattern not found" in result.message
            assert result.metrics["status_code"] == 200
            assert result.metrics["duration"] == 0.5
            assert result.metrics["pattern_found"] == 0

    @pytest.mark.asyncio
    async def test_check_website_timeout(self, checker):
        """Test a website check that times out."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.side_effect = httpx.TimeoutException("Timeout")
            mock_client.return_value = mock_instance

            result = await checker.check_website()

            # Verify result
            assert result.status == Status.CRITICAL
            assert "timed out" in result.message
            assert result.metrics["duration"] == 10  # Timeout value

    @pytest.mark.asyncio
    async def test_check_website_http_error(self, checker):
        """Test a website check with an HTTP error."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.side_effect = httpx.HTTPError("HTTP Error")
            mock_client.return_value = mock_instance

            result = await checker.check_website()

            # Verify result
            assert result.status == Status.CRITICAL
            assert "HTTP error" in result.message
            assert result.metrics["duration"] == 0

    @pytest.mark.asyncio
    async def test_check_website_unexpected_error(self, checker):
        """Test a website check with an unexpected error."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.side_effect = Exception("Unexpected error")
            mock_client.return_value = mock_instance

            # Mock logger to prevent output during tests
            with patch("nagios_plugins.plugins.check_website_status.logger"):
                result = await checker.check_website()

                # Verify result
                assert result.status == Status.UNKNOWN
                assert "Unexpected error" in result.message
                assert result.metrics["duration"] == 0