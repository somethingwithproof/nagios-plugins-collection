# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for AWS-related plugins using service function mocks."""

from unittest.mock import patch

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_backup_freshness import CheckBackupFreshness
from nagios_plugins.plugins.check_queue_depth import CheckQueueDepth


def test_queue_depth_thresholds() -> None:
    plugin = CheckQueueDepth()
    with patch(
        "nagios_plugins.plugins.check_queue_depth.queue_depth",
        return_value={"depth": 10, "inflight": 2, "delayed": 0},
    ):
        code = plugin.run(["--queue-url", "url", "--warning", "5", "--critical", "20"])
        assert code == Status.WARNING.value  # 10 >= 5 and < 20 -> WARNING
    with patch(
        "nagios_plugins.plugins.check_queue_depth.queue_depth",
        return_value={"depth": 3, "inflight": 0, "delayed": 0},
    ):
        code = plugin.run(["--queue-url", "url", "--warning", "5", "--critical", "20"])
        assert code == Status.OK.value


def test_backup_freshness_thresholds() -> None:
    plugin = CheckBackupFreshness()
    with patch(
        "nagios_plugins.plugins.check_backup_freshness.latest_object_age_seconds", return_value=1800
    ):
        code = plugin.run(
            ["--bucket", "b", "--prefix", "p/", "--warning", "3600", "--critical", "7200"]
        )
        assert code == Status.OK.value
    with patch(
        "nagios_plugins.plugins.check_backup_freshness.latest_object_age_seconds", return_value=8000
    ):
        code = plugin.run(
            ["--bucket", "b", "--prefix", "p/", "--warning", "3600", "--critical", "7200"]
        )
        assert code == Status.CRITICAL.value
