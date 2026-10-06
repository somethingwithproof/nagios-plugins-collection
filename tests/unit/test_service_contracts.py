# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Exercise vendor response parsing without live accounts or credentials."""

import datetime as dt
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from nagios_plugins.services.aws_cloudwatch import get_metric_statistics
from nagios_plugins.services.aws_s3 import latest_object_age_seconds
from nagios_plugins.services.aws_sqs import queue_depth
from nagios_plugins.services.k8s import summarize_nodes
from nagios_plugins.services.pg import replication_lag_seconds
from nagios_plugins.services.redis_svc import get_stats


def test_backup_freshness_chooses_latest_across_pages() -> None:
    now = dt.datetime.now(dt.UTC)
    s3 = MagicMock()
    s3.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"LastModified": now - dt.timedelta(hours=2)}]},
        {},
        {"Contents": [{"LastModified": now - dt.timedelta(minutes=5)}]},
    ]
    with patch("boto3.client", return_value=s3):
        age = latest_object_age_seconds("backups", "daily/", timeout=7)
    assert 300 <= age <= 301
    s3.get_paginator.return_value.paginate.assert_called_once_with(
        Bucket="backups", Prefix="daily/", PaginationConfig={"PageSize": 1000}
    )


def test_empty_backup_prefix_is_not_reported_healthy() -> None:
    s3 = MagicMock()
    s3.get_paginator.return_value.paginate.return_value = [{}]
    with patch("boto3.client", return_value=s3), pytest.raises(RuntimeError, match="No objects"):
        latest_object_age_seconds("backups")


def test_queue_depth_parses_integer_attributes() -> None:
    sqs = MagicMock()
    sqs.get_queue_attributes.return_value = {
        "Attributes": {
            "ApproximateNumberOfMessages": "15",
            "ApproximateNumberOfMessagesNotVisible": "4",
        }
    }
    with patch("boto3.client", return_value=sqs):
        counts = queue_depth("https://sqs.example/queue")
    assert counts == {"depth": 15, "inflight": 4, "delayed": 0}


def test_cloudwatch_chooses_latest_datapoint() -> None:
    client = MagicMock()
    now = dt.datetime.now(dt.UTC)
    client.get_metric_statistics.return_value = {
        "Datapoints": [
            {"Timestamp": now, "Average": 7, "Unit": "Count"},
            {"Timestamp": now - dt.timedelta(minutes=5), "Average": 1},
        ]
    }
    with patch("boto3.client", return_value=client):
        result = get_metric_statistics("AWS/Test", "Requests", [])
    assert result["value"] == 7.0
    assert result["unit"] == "Count"
    assert result["timestamp"] == now.isoformat()


def test_cloudwatch_missing_data_is_unknown() -> None:
    client = MagicMock()
    client.get_metric_statistics.return_value = {"Datapoints": []}
    with patch("boto3.client", return_value=client), pytest.raises(RuntimeError, match="No data"):
        get_metric_statistics("AWS/Test", "Requests", [])


@pytest.mark.parametrize("row,expected", [(None, 0.0), ((None,), 0.0), ((12.5,), 12.5)])
def test_postgres_lag_rows(row: tuple[float | None] | None, expected: float) -> None:
    connection = MagicMock()
    connection.__enter__.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value = row
    with patch("psycopg.connect", return_value=connection):
        result = replication_lag_seconds("postgresql://monitor@db.example/monitor", timeout=7)
    assert result == expected


@pytest.mark.parametrize(
    "info,expected_ratio", [({}, 1.0), ({"keyspace_hits": 3, "keyspace_misses": 1}, 0.75)]
)
def test_redis_hit_ratio(info: dict, expected_ratio: float) -> None:
    client = MagicMock()
    client.info.return_value = info
    with patch("redis.from_url", return_value=client):
        result = get_stats("redis://cache.example", timeout=7)
    assert result["hitratio"] == expected_ratio
    assert result["used_memory"] == 0


def test_kubernetes_pressure_and_kubeconfig_fallback() -> None:
    conditions = [
        SimpleNamespace(type="Ready", status="True"),
        SimpleNamespace(type="DiskPressure", status="True"),
        SimpleNamespace(type="MemoryPressure", status="True"),
        SimpleNamespace(type="PIDPressure", status="True"),
    ]
    api = MagicMock()
    api.list_node.return_value.items = [
        SimpleNamespace(status=SimpleNamespace(conditions=conditions)),
        SimpleNamespace(status=SimpleNamespace(conditions=None)),
    ]
    with (
        patch(
            "kubernetes.config.load_incluster_config", side_effect=RuntimeError("outside cluster")
        ),
        patch("kubernetes.config.load_kube_config") as load_config,
        patch("kubernetes.client.CoreV1Api", return_value=api),
    ):
        result = summarize_nodes("role=worker", timeout=7)
    load_config.assert_called_once()
    api.list_node.assert_called_once_with(label_selector="role=worker", _request_timeout=7)
    assert result.ready == 1
    assert result.not_ready == 1
    assert result.disk_pressure == 1
    assert result.memory_pressure == 1
    assert result.pid_pressure == 1
