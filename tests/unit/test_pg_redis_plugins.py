# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for Postgres replication and Redis saturation plugins."""

from unittest.mock import MagicMock, patch

import pytest

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


def _redis(
    used: int,
    maxmemory: int,
    *args: str,
    evicted: int = 0,
    blocked: int = 0,
    hitratio: float = 0.6,
) -> tuple[int, MagicMock]:
    stats = {
        "used_memory": used,
        "maxmemory": maxmemory,
        "evicted_keys": evicted,
        "blocked_clients": blocked,
        "hitratio": hitratio,
    }
    with patch(
        "nagios_plugins.plugins.check_redis_saturation.get_stats", return_value=stats
    ) as get_stats:
        code = CheckRedisSaturation().run(["--url", "redis://localhost:6379/0", *args])
    return code, get_stats


@pytest.mark.parametrize(
    "used,expected", [(500, Status.OK), (850, Status.WARNING), (950, Status.CRITICAL)]
)
def test_redis_thresholds_apply_to_memory_percent(used: int, expected: Status) -> None:
    """-w/-c are ranges for used_memory as a percentage of maxmemory."""
    code, _ = _redis(used, 1000, "--warning", "80", "--critical", "90")
    assert code == expected.value


def test_redis_eviction_counter_does_not_latch_an_alert() -> None:
    """evicted_keys only grows until restart, so it must not drive the status."""
    code, _ = _redis(100, 1000, "-w", "80", "-c", "90", evicted=10**6)
    assert code == Status.OK.value


def test_redis_without_maxmemory_cannot_evaluate_thresholds() -> None:
    assert _redis(100, 0, "-w", "80")[0] == Status.UNKNOWN.value
    assert _redis(100, 0)[0] == Status.OK.value


def test_redis_honors_timeout(capsys: pytest.CaptureFixture[str]) -> None:
    code, get_stats = _redis(100, 1000, "--timeout", "7")
    assert code == Status.OK.value
    assert get_stats.call_args.kwargs["timeout"] == 7
    assert "evicted_keys=0c" in capsys.readouterr().out


def test_pg_without_standby_is_critical(capsys: pytest.CaptureFixture[str]) -> None:
    """An empty pg_stat_replication is the failure being monitored, not zero lag."""
    with patch(
        "nagios_plugins.plugins.check_postgres_replication_lag.replication_lag_seconds",
        return_value=None,
    ):
        code = CheckPostgresReplicationLag().run(["--dsn", "postgres://", "-w", "5", "-c", "10"])
    assert code == Status.CRITICAL.value
    assert capsys.readouterr().out.startswith("CRITICAL - No standby connected")


def test_redis_blocked_clients_and_hit_ratio_are_not_checked_by_default() -> None:
    """Without their own ranges these stay perfdata only, as since 3.0."""
    assert _redis(100, 1000, "-w", "80", blocked=500, hitratio=0.01)[0] == Status.OK.value


@pytest.mark.parametrize(
    "args,blocked,hitratio,expected",
    [
        (["--blocked-warning", "5", "--blocked-critical", "20"], 5, 0.9, Status.OK),
        (["--blocked-warning", "5", "--blocked-critical", "20"], 6, 0.9, Status.WARNING),
        (["--blocked-warning", "5", "--blocked-critical", "20"], 21, 0.9, Status.CRITICAL),
        (["--hitratio-warning", "0.8:", "--hitratio-critical", "0.5:"], 0, 0.8, Status.OK),
        (["--hitratio-warning", "0.8:", "--hitratio-critical", "0.5:"], 0, 0.7, Status.WARNING),
        (["--hitratio-warning", "0.8:", "--hitratio-critical", "0.5:"], 0, 0.4, Status.CRITICAL),
        # The most severe measurement wins, memory included.
        (
            ["-w", "80", "--hitratio-warning", "0.8:", "--blocked-critical", "1"],
            2,
            0.7,
            Status.CRITICAL,
        ),
    ],
)
def test_redis_blocked_clients_and_hit_ratio_ranges(
    args: list[str], blocked: int, hitratio: float, expected: Status
) -> None:
    assert _redis(100, 1000, *args, blocked=blocked, hitratio=hitratio)[0] == expected.value


def test_redis_secondary_ranges_apply_without_maxmemory() -> None:
    assert _redis(100, 0, "--blocked-critical", "1", blocked=3)[0] == Status.CRITICAL.value


def test_redis_secondary_ranges_appear_in_perfdata(capsys: pytest.CaptureFixture[str]) -> None:
    _redis(100, 1000, "--blocked-warning", "5", "--hitratio-critical", "0.5:")
    perfdata = capsys.readouterr().out.split("|", 1)[1]
    assert "blocked_clients=0;5;;0 " in perfdata
    assert "hitratio=0.6;;0.5:;0;1" in perfdata


def test_redis_malformed_secondary_range_is_a_usage_error() -> None:
    with pytest.raises(SystemExit) as exited:
        _redis(100, 1000, "--hitratio-warning", "high")
    assert exited.value.code == Status.UNKNOWN.value
