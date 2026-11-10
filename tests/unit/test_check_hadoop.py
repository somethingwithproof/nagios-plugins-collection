# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for the check_hadoop plugin."""

from collections.abc import Callable
from datetime import datetime, timedelta
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins.base import PerfData, Status
from nagios_plugins.plugins.check_hadoop import HadoopClusterChecker
from tests.fakes import serve_http


def _raise(error: Exception) -> Callable[[httpx.Request], httpx.Response]:
    def respond(request: httpx.Request) -> httpx.Response:
        raise error

    return respond


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
        mock_data = self.create_mock_response(status="ok", mem_component="1024k")

        with serve_http(lambda request: httpx.Response(200, json=mock_data)):
            result = await checker.check_cluster()

            # Verify result
            assert result.status == Status.OK
            assert "Hadoop cluster is healthy" in result.message
            assert "memory: 1024" in result.message
            assert result.metrics["status"] == 1
            assert result.metrics["component_component1_status"] == 1
            assert result.metrics["component_component2_status"] == 1
            assert result.metrics["mem"] == PerfData(1024.0, uom="KB")
            assert "mem=1024KB" in str(result)

    @pytest.mark.asyncio
    async def test_check_cluster_overall_status_warning(self, checker):
        """Test a cluster check with warning overall status."""
        mock_data = self.create_mock_response(status="warning")

        with serve_http(lambda request: httpx.Response(200, json=mock_data)):
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

        with serve_http(lambda request: httpx.Response(200, json=mock_data)):
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

        with serve_http(lambda request: httpx.Response(200, json=mock_data)):
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
    @pytest.mark.parametrize(
        "handler,expected,message",
        [
            (_raise(httpx.ConnectError("refused")), Status.CRITICAL, "Failed to connect"),
            (lambda request: httpx.Response(200, text="{"), Status.CRITICAL, "Invalid JSON"),
            (_raise(RuntimeError("Unexpected error")), Status.UNKNOWN, "Unexpected error"),
        ],
        ids=["transport", "json", "unexpected"],
    )
    async def test_check_cluster_failures(self, checker, handler, expected, message):
        """Transport, decoding and unexpected failures never report OK."""
        with serve_http(handler), patch("nagios_plugins.plugins.check_hadoop.logger"):
            result = await checker.check_cluster()
        assert result.status == expected
        assert message in result.message
        assert result.metrics["status"] == 0
