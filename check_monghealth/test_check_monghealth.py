#!/usr/bin/env python3
"""
Tests for the MongoDB Health Check Plugin.

This module contains tests for the MongoDB Health Check Plugin.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import HTTPError, Response

from check_monghealth_modernized import (
    CheckResult,
    MongoHealthChecker,
    Status,
    main,
    main_async,
    parse_args,
)


class TestStatus:
    """Tests for the Status enum."""

    def test_str(self):
        """Test the __str__ method."""
        assert str(Status.OK) == "OK"
        assert str(Status.WARNING) == "WARNING"
        assert str(Status.CRITICAL) == "CRITICAL"
        assert str(Status.UNKNOWN) == "UNKNOWN"


class TestCheckResult:
    """Tests for the CheckResult class."""

    def test_str_simple(self):
        """Test the __str__ method with a simple result."""
        result = CheckResult(Status.OK, "Everything is fine")
        assert str(result) == "OK - Everything is fine"

    def test_str_with_metrics(self):
        """Test the __str__ method with metrics."""
        result = CheckResult(
            Status.WARNING,
            "High CPU usage",
            metrics={"cpu": 85, "memory": 50},
        )
        assert str(result) == "WARNING - High CPU usage | cpu=85 memory=50"

    def test_str_with_details(self):
        """Test the __str__ method with details."""
        result = CheckResult(
            Status.CRITICAL,
            "Service is down",
            details="The service has been down for 10 minutes.",
        )
        assert (
            str(result) == "CRITICAL - Service is down\n"
            "The service has been down for 10 minutes."
        )

    def test_to_json(self):
        """Test the to_json method."""
        result = CheckResult(
            Status.OK,
            "Everything is fine",
            metrics={"cpu": 10, "memory": 20},
            details="All systems operational.",
        )
        json_str = result.to_json()
        json_data = json.loads(json_str)
        assert json_data["status"] == "OK"
        assert json_data["message"] == "Everything is fine"
        assert json_data["metrics"]["cpu"] == 10
        assert json_data["metrics"]["memory"] == 20
        assert json_data["details"] == "All systems operational."


class TestMongoHealthChecker:
    """Tests for the MongoHealthChecker class."""

    @pytest.fixture
    def checker(self):
        """Create a test checker."""
        return MongoHealthChecker(
            host="mongodb.example.com",
            port=27017,
            timeout=5,
            username="admin",
            password="secret",
            ssl=True,
        )

    def test_init(self, checker):
        """Test the __init__ method."""
        assert checker.host == "mongodb.example.com"
        assert checker.port == 27017
        assert checker.timeout == 5
        assert checker.username == "admin"
        assert checker.password == "secret"
        assert checker.ssl is True
        assert checker.base_url == "https://mongodb.example.com:27017"
        assert checker.auth == ("admin", "secret")

    @pytest.mark.asyncio
    async def test_check_engine_status_success(self, checker):
        """Test the check_engine_status method with a successful response."""
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "alive": True,
            "mongrations_current": True,
            "search_reachable": True,
        }
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("httpx.AsyncClient", return_value=mock_client):
            is_alive, data = await checker.check_engine_status()

        assert is_alive is True
        assert data["alive"] is True
        assert data["mongrations_current"] is True
        assert data["search_reachable"] is True

    @pytest.mark.asyncio
    async def test_check_engine_status_http_error(self, checker):
        """Test the check_engine_status method with an HTTP error."""
        mock_client = AsyncMock()
        mock_client.get.side_effect = HTTPError("HTTP Error")

        with patch("httpx.AsyncClient", return_value=mock_client):
            is_alive, data = await checker.check_engine_status()

        assert is_alive is False
        assert data == {}

    @pytest.mark.asyncio
    async def test_check_components_alive(self, checker):
        """Test the check_components method with a live engine."""
        with patch.object(
            checker,
            "check_engine_status",
            return_value=(True, {"alive": True, "mongrations_current": True, "search_reachable": True}),
        ):
            result = await checker.check_components([("mongrations_current", True), ("search_reachable", True)])

        assert result.status == Status.OK
        assert "All MongoDB components are healthy" in result.message
        assert result.metrics["alive"] == 1
        assert result.metrics["mongrations_current"] == 1
        assert result.metrics["search_reachable"] == 1

    @pytest.mark.asyncio
    async def test_check_components_not_alive(self, checker):
        """Test the check_components method with a dead engine."""
        with patch.object(
            checker,
            "check_engine_status",
            return_value=(False, {}),
        ):
            result = await checker.check_components([("mongrations_current", True), ("search_reachable", True)])

        assert result.status == Status.CRITICAL
        assert "MongoDB engine is not alive!" in result.message
        assert result.metrics["alive"] == 0

    @pytest.mark.asyncio
    async def test_check_components_failed(self, checker):
        """Test the check_components method with failed components."""
        with patch.object(
            checker,
            "check_engine_status",
            return_value=(True, {"alive": True, "mongrations_current": False, "search_reachable": True}),
        ):
            result = await checker.check_components([("mongrations_current", True), ("search_reachable", True)])

        assert result.status == Status.CRITICAL
        assert "Failed components" in result.message
        assert "mongrations_current" in result.message
        assert result.metrics["alive"] == 1
        assert result.metrics["mongrations_current"] == 0
        assert result.metrics["search_reachable"] == 1


def test_parse_args():
    """Test the parse_args function."""
    args = parse_args(["--host", "mongodb.example.com", "--port", "27017", "--mode", "1"])
    assert args.host == "mongodb.example.com"
    assert args.port == 27017
    assert args.mode == 1
    assert args.timeout == 5
    assert args.username is None
    assert args.password is None
    assert args.ssl is False
    assert args.json is False
    assert args.verbose == 0


@pytest.mark.asyncio
async def test_main_async():
    """Test the main_async function."""
    with patch("check_monghealth_modernized.parse_args") as mock_parse_args, \
         patch("check_monghealth_modernized.MongoHealthChecker") as mock_checker_class:
        
        # Mock the arguments
        mock_args = MagicMock()
        mock_args.host = "mongodb.example.com"
        mock_args.port = 27017
        mock_args.timeout = 5
        mock_args.username = None
        mock_args.password = None
        mock_args.ssl = False
        mock_args.mode = 1
        mock_args.json = False
        mock_args.verbose = 0
        mock_parse_args.return_value = mock_args
        
        # Mock the checker
        mock_checker = MagicMock()
        mock_checker.check_components.return_value = CheckResult(Status.OK, "All MongoDB components are healthy")
        mock_checker_class.return_value = mock_checker
        
        # Call the function
        exit_code = await main_async()
        
        # Verify the results
        assert exit_code == 0
        mock_checker_class.assert_called_once_with(
            host="mongodb.example.com",
            port=27017,
            timeout=5,
            username=None,
            password=None,
            ssl=False,
        )
        mock_checker.check_components.assert_called_once()


def test_main():
    """Test the main function."""
    with patch("asyncio.get_event_loop") as mock_get_loop, \
         patch("check_monghealth_modernized.main_async") as mock_main_async:
        
        # Mock the event loop
        mock_loop = MagicMock()
        mock_get_loop.return_value = mock_loop
        
        # Mock the main_async function
        mock_main_async.return_value = 0
        mock_loop.run_until_complete.return_value = 0
        
        # Call the function
        exit_code = main()
        
        # Verify the results
        assert exit_code == 0
        mock_get_loop.assert_called_once()
        mock_loop.run_until_complete.assert_called_once_with(mock_main_async())
