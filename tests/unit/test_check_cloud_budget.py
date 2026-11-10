# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for the AWS month-to-date budget check."""

import datetime as dt
from collections.abc import Mapping, Sequence
from unittest.mock import patch

import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_cloud_budget import CheckCloudBudget, _month_range_utc


@pytest.mark.parametrize(
    "now,expected",
    [
        (dt.datetime(2026, 11, 1, 0, 5, tzinfo=dt.UTC), ("2026-11-01", "2026-11-02")),
        (dt.datetime(2026, 11, 9, 12, tzinfo=dt.UTC), ("2026-11-01", "2026-11-10")),
        (dt.datetime(2026, 12, 31, 23, tzinfo=dt.UTC), ("2026-12-01", "2027-01-01")),
    ],
)
def test_period_end_is_exclusive_and_after_start(
    now: dt.datetime, expected: tuple[str, str]
) -> None:
    """Cost Explorer rejects End == Start, which the first of the month used to send."""
    assert _month_range_utc(now) == expected


def _run(results: Sequence[Mapping[str, object]], *args: str) -> tuple[int, object]:
    with patch("boto3.client") as client:
        client.return_value.get_cost_and_usage.return_value = {"ResultsByTime": results}
        code = CheckCloudBudget().run(["--budget", "100", "--timeout", "7", *args])
    return code, client


def test_budget_thresholds_and_client_config() -> None:
    results = [{"Total": {"UnblendedCost": {"Amount": "85.5"}}}]
    code, client = _run(results, "-w", "80", "-c", "90")
    assert code == Status.WARNING.value
    config = client.call_args.kwargs["config"]  # type: ignore[attr-defined]
    assert (config.connect_timeout, config.read_timeout) == (7, 7)
    assert config.retries == {"max_attempts": 3, "mode": "standard"}


def test_missing_cost_results_are_unknown() -> None:
    assert _run([], "-w", "80")[0] == Status.UNKNOWN.value
