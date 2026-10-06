# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for Prometheus query plugin."""

from unittest.mock import MagicMock, patch

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_prometheus_query import CheckPrometheusQuery


def test_prom_ok_scalar() -> None:
    plugin = CheckPrometheusQuery()
    ok_json = {"status": "success", "data": {"result": [{"value": [0, "0.42"]}]}}
    with patch("httpx.Client") as mock_client:
        mock = MagicMock()
        mock.__enter__.return_value.get.return_value.json.return_value = ok_json
        mock.__enter__.return_value.get.return_value.raise_for_status.return_value = None
        mock_client.return_value = mock
        code = plugin.run(
            ["--server", "http://prom:9090", "--query", "up", "--warning", "1", "--critical", "2"]
        )
        assert code == Status.OK.value


def test_prom_critical_when_threshold_exceeded() -> None:
    plugin = CheckPrometheusQuery()
    crit_json = {"status": "success", "data": {"result": [{"value": [0, "5"]}]}}
    with patch("httpx.Client") as mock_client:
        mock = MagicMock()
        mock.__enter__.return_value.get.return_value.json.return_value = crit_json
        mock.__enter__.return_value.get.return_value.raise_for_status.return_value = None
        mock_client.return_value = mock
        code = plugin.run(
            [
                "--server",
                "http://prom:9090",
                "--query",
                "errors",
                "--warning",
                "1",
                "--critical",
                "2",
            ]
        )
        assert code == Status.CRITICAL.value
