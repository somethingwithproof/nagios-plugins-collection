"""Tests for Postgres replication and Redis saturation plugins."""

from unittest.mock import patch

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_postgres_replication_lag import CheckPostgresReplicationLag
from nagios_plugins.plugins.check_redis_saturation import CheckRedisSaturation


def test_pg_replication_thresholds() -> None:
    plugin = CheckPostgresReplicationLag()
    with patch(
        "nagios_plugins.plugins.check_postgres_replication_lag.replication_lag_seconds",
        return_value=12.3,
    ):
        code = plugin.run(["--dsn", "postgres://", "--warning", "5", "--critical", "10"])
        assert code == Status.CRITICAL.value


def test_redis_saturation_thresholds() -> None:
    plugin = CheckRedisSaturation()
    stats = {"used_memory": 1024, "evicted_keys": 1, "blocked_clients": 0, "hitratio": 0.6}
    with patch("nagios_plugins.plugins.check_redis_saturation.get_stats", return_value=stats):
        code = plugin.run(
            ["--url", "redis://localhost:6379/0", "--warning", "10", "--critical", "20"]
        )
        assert code == Status.WARNING.value
