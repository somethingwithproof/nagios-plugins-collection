"""Tests for the check_hadoop plugin."""

import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_hadoop import HadoopClusterChecker


class TestHadoopClusterChecker:
    """Tests for the HadoopClusterChecker class."""

    @pytest.fixture
    def checker(self):
        """Create a HadoopClusterChecker instance."""
        return HadoopClusterChecker(
            url="http://example.com/hadoop/status",
            max_update_minutes=60,
            timeout=30,
        )

    def create_mock_response(self, status="ok", components=None, mem_component=None):
        """Create a mock response with the given status and components."""
        now = datetime.now()
        one_hour_ago = (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        two_hours_ago = (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

        if components is None:
            components = [
                {
                    "name": "component1",
                    "status": "ok",
                    "message": "Component 1 is healthy",
                    "updated": one_hour_ago,
                },
                {
                    "name": "component2",
                    "status": "ok",
                    "message": "Component 2 is healthy",
                    "updated": one_hour_ago,
                },
            ]

        if mem_component:
            components.append(
                {
                    "name": "mem",
                    "status": "ok",
                    "message": mem_component,
                    "updated": one_hour_ago,
                }
            )

        return {
            "status": status,
            "message": f"Hadoop cluster status is {status}",
            "subcomponents": components,
        }

    @pytest.mark.asyncio
    async def test_check_cluster_success(self, checker):
        """Test a successful cluster check."""
        mock_data = self.create_mock_response(
            status="ok", mem_component="1024k"
        )

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = mock_data
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_cluster()

            # Verify result
            assert result.status == Status.OK
            assert "Hadoop cluster is healthy" in result.message
            assert "memory: 1024" in result.message
            assert result.metrics["status"] == 1
            assert result.metrics["component_component1_status"] == 1
            assert result.metrics["component_component2_status"] == 1
            assert result.metrics["mem"] == "1024"

    @pytest.mark.asyncio
    async def test_check_cluster_overall_status_warning(self, checker):
        """Test a cluster check with warning overall status."""
        mock_data = self.create_mock_response(status="warning")

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = mock_data
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_cluster()

            # Verify result
            assert result.status == Status.WARNING
            assert "Hadoop: Hadoop cluster status is warning" in result.message
            assert result.metrics["status"] == 0

    @pytest.mark.asyncio
    async def test_check_cluster_component_status_warning(self, checker):
        """Test a cluster check with a component in warning status."""
        now = datetime.now()
        one_hour_ago = (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        
        mock_data = self.create_mock_response(
            status="ok",
            components=[
                {
                    "name": "component1",
                    "status": "ok",
                    "message": "Component 1 is healthy",
                    "updated": one_hour_ago,
                },
                {
                    "name": "component2",
                    "status": "warning",
                    "message": "Component 2 has issues",
                    "updated": one_hour_ago,
                },
            ],
        )

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = mock_data
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_cluster()

            # Verify result
            assert result.status == Status.WARNING
            assert "Component 'component2' has status 'warning'" in result.message
            assert result.metrics["status"] == 1
            assert result.metrics["component_component1_status"] == 1
            assert result.metrics["component_component2_status"] == 0

    @pytest.mark.asyncio
    async def test_check_cluster_stale_component(self, checker):
        """Test a cluster check with a stale component."""
        now = datetime.now()
        one_hour_ago = (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        three_hours_ago = (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
        
        mock_data = self.create_mock_response(
            status="ok",
            components=[
                {
                    "name": "component1",
                    "status": "ok",
                    "message": "Component 1 is healthy",
                    "updated": one_hour_ago,
                },
                {
                    "name": "component2",
                    "status": "ok",
                    "message": "Component 2 is healthy",
                    "updated": three_hours_ago,  # Stale component
                },
            ],
        )

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = mock_data
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await checker.check_cluster()

            # Verify result
            assert result.status == Status.WARNING
            assert "Component 'component2'" in result.message
            assert "updated" in result.message
            assert result.metrics["status"] == 1
            assert result.metrics["component_component1_status"] == 1
            assert result.metrics["component_component2_status"] == 1
            assert "component_component2_minutes_since_update" in result.metrics

    @pytest.mark.asyncio
    async def test_check_cluster_http_error(self, checker):
        """Test a cluster check with an HTTP error."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.side_effect = httpx.HTTPError("HTTP Error")
            mock_client.return_value = mock_instance

            # Mock logger to prevent output during tests
            with patch("nagios_plugins.plugins.check_hadoop.logger"):
                result = await checker.check_cluster()

                # Verify result
                assert result.status == Status.CRITICAL
                assert "Failed to connect to Hadoop API" in result.message
                assert result.metrics["status"] == 0

    @pytest.mark.asyncio
    async def test_check_cluster_json_decode_error(self, checker):
        """Test a cluster check with a JSON decode error."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "{", 0)
            mock_instance.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_instance

            # Mock logger to prevent output during tests
            with patch("nagios_plugins.plugins.check_hadoop.logger"):
                result = await checker.check_cluster()

                # Verify result
                assert result.status == Status.CRITICAL
                assert "Invalid JSON response" in result.message
                assert result.metrics["status"] == 0

    @pytest.mark.asyncio
    async def test_check_cluster_unexpected_error(self, checker):
        """Test a cluster check with an unexpected error."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.__aenter__.return_value.get.side_effect = Exception("Unexpected error")
            mock_client.return_value = mock_instance

            # Mock logger to prevent output during tests
            with patch("nagios_plugins.plugins.check_hadoop.logger"):
                result = await checker.check_cluster()

                # Verify result
                assert result.status == Status.UNKNOWN
                assert "Unexpected error" in result.message
                assert result.metrics["status"] == 0