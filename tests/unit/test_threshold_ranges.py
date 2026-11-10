# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Checks that used ``value >= N`` follow the Nagios range guidelines."""

from __future__ import annotations

import argparse
import re
from collections.abc import Callable, Iterator
from contextlib import AbstractContextManager, contextmanager
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins.base import (
    NagiosPlugin,
    PerfData,
    Status,
    ThresholdRange,
    format_perfdata,
    nagios_range,
)
from nagios_plugins.plugins.check_backup_freshness import CheckBackupFreshness
from nagios_plugins.plugins.check_cloud_budget import CheckCloudBudget
from nagios_plugins.plugins.check_http_sli import CheckHttpSli
from nagios_plugins.plugins.check_postgres_replication_lag import CheckPostgresReplicationLag
from nagios_plugins.plugins.check_queue_depth import CheckQueueDepth
from tests.fakes import serve_http


@contextmanager
def _budget(value: float) -> Iterator[None]:
    """Cost Explorer reports ``value`` dollars; with a $100 budget that is the percentage."""
    with patch("boto3.client") as client:
        client.return_value.get_cost_and_usage.return_value = {
            "ResultsByTime": [{"Total": {"UnblendedCost": {"Amount": str(value)}}}]
        }
        yield


Backend = Callable[[float], AbstractContextManager[object]]
CHECKS: dict[str, tuple[type[NagiosPlugin], list[str], Backend]] = {
    "queue_depth": (
        CheckQueueDepth,
        ["--queue-url", "https://sqs.example/q"],
        lambda value: patch(
            "nagios_plugins.plugins.check_queue_depth.queue_depth",
            return_value={"depth": int(value), "inflight": 0, "delayed": 0},
        ),
    ),
    "backup_freshness": (
        CheckBackupFreshness,
        ["--bucket", "backups"],
        lambda value: patch(
            "nagios_plugins.plugins.check_backup_freshness.latest_object_age_seconds",
            return_value=int(value),
        ),
    ),
    "postgres_lag": (
        CheckPostgresReplicationLag,
        [],
        lambda value: patch(
            "nagios_plugins.plugins.check_postgres_replication_lag.replication_lag_seconds",
            return_value=float(value),
        ),
    ),
    "cloud_budget": (CheckCloudBudget, ["--budget", "100"], _budget),
}


@pytest.mark.parametrize(
    "value,thresholds,expected",
    [
        # A plain N is the range 0:N: equal to N is inside it, so not an alert.
        (10, ["-w", "10", "-c", "20"], Status.OK),
        (11, ["-w", "10", "-c", "20"], Status.WARNING),
        (20, ["-w", "10", "-c", "20"], Status.WARNING),
        (21, ["-w", "10", "-c", "20"], Status.CRITICAL),
        # Full range syntax now works: alert inside 5..15 with @.
        (8, ["-c", "@5:15"], Status.CRITICAL),
        (16, ["-c", "@5:15"], Status.OK),
        # N: alerts below N.
        (3, ["-w", "5:"], Status.WARNING),
        (0, [], Status.OK),
    ],
)
@pytest.mark.parametrize("name", sorted(CHECKS))
def test_thresholds_are_nagios_ranges(
    name: str,
    value: float,
    thresholds: list[str],
    expected: Status,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plugin, args, backend = CHECKS[name]
    monkeypatch.setenv("CHECK_POSTGRES_DSN", "postgresql://monitor@db/postgres")
    with backend(value):
        code = plugin().run([*args, *thresholds])
    assert code == expected.value


@pytest.mark.parametrize("text", ["@", "@ ", " @"])
def test_a_bare_at_sign_is_not_a_range(text: str) -> None:
    with pytest.raises(ValueError, match="'@' needs a range"):
        ThresholdRange.from_string(text)
    with pytest.raises(argparse.ArgumentTypeError):
        nagios_range(text)


@pytest.mark.parametrize(
    "text,canonical",
    [
        ("10", "10"),
        (":10", "~:10"),
        ("1e1", "10"),
        ("1_000:", "1000:"),
        (" 5:7 ", "5:7"),
        ("@0:2.50", "@2.5"),
        ("@:", "@~:"),
        ("~:", ""),
    ],
)
def test_ranges_are_normalized_for_options_and_perfdata(text: str, canonical: str) -> None:
    assert nagios_range(text) == canonical
    assert format_perfdata({"m": PerfData(1, warning=text, critical=text)}) == (
        f"m=1;{canonical};{canonical}".rstrip(";")
    )


def test_perfdata_rejects_a_malformed_threshold() -> None:
    with pytest.raises(ValueError):
        PerfData(1, warning="@")


def test_sli_rejects_a_malformed_range_while_parsing() -> None:
    with pytest.raises(SystemExit) as exited:
        CheckHttpSli().parse_args(["--url", "https://a.example/", "--error-rate-critical", "@"])
    assert exited.value.code == 3


def test_canonical_threshold_reaches_perfdata(capsys: pytest.CaptureFixture[str]) -> None:
    with serve_http(lambda request: httpx.Response(200)):
        CheckHttpSli().run(["--url", "https://a.example/", "--samples", "1", "-w", ":1e4"])
    assert re.search(r" p95_ms=[\d.]+;~:10000 ", capsys.readouterr().out)
