# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for the Elasticsearch/OpenSearch error-count plugin."""

from unittest.mock import patch

import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_log_errors import CheckLogErrors


def _run_with_body(body: object) -> int:
    with patch("httpx.Client") as mock_client:
        response = mock_client.return_value.__enter__.return_value.post.return_value
        response.json.return_value = body
        response.raise_for_status.return_value = None
        return CheckLogErrors().run(
            ["--endpoint", "http://es:9200", "--index", "logs", "-w", "1", "-c", "10"]
        )


@pytest.mark.parametrize(
    "body", [{}, {"hits": {}}, {"hits": {"total": {}}}, {"hits": {"total": "5"}}, []]
)
def test_missing_hit_count_is_unknown(body: object) -> None:
    """A response without a hit count is missing data, not zero errors."""
    assert _run_with_body(body) == Status.UNKNOWN.value


@pytest.mark.parametrize(
    "body,expected",
    [
        ({"hits": {"total": {"value": 0, "relation": "eq"}}}, Status.OK),
        ({"hits": {"total": {"value": 5, "relation": "eq"}}}, Status.WARNING),
        ({"hits": {"total": 25}}, Status.CRITICAL),
    ],
)
def test_hit_counts_from_es7_objects_and_es6_integers(body: object, expected: Status) -> None:
    """Both total formats are thresholded."""
    assert _run_with_body(body) == expected.value
