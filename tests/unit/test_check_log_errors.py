# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for the Elasticsearch/OpenSearch error-count plugin."""

import json

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_log_errors import CheckLogErrors
from tests.fakes import FakeHttpBackend


def _run_with_body(backend: FakeHttpBackend, body: object) -> int:
    backend.reply(httpx.Response(200, json=body))
    return CheckLogErrors().run(
        ["--endpoint", "http://es:9200", "--index", "logs", "-w", "1", "-c", "10"]
    )


@pytest.mark.parametrize(
    "body", [{}, {"hits": {}}, {"hits": {"total": {}}}, {"hits": {"total": "5"}}, []]
)
def test_missing_hit_count_is_unknown(http_backend: FakeHttpBackend, body: object) -> None:
    """A response without a hit count is missing data, not zero errors."""
    assert _run_with_body(http_backend, body) == Status.UNKNOWN.value


@pytest.mark.parametrize(
    "body,expected",
    [
        ({"hits": {"total": {"value": 0, "relation": "eq"}}}, Status.OK),
        ({"hits": {"total": {"value": 5, "relation": "eq"}}}, Status.WARNING),
        ({"hits": {"total": 25}}, Status.CRITICAL),
    ],
)
def test_hit_counts_from_es7_objects_and_es6_integers(
    http_backend: FakeHttpBackend, body: object, expected: Status
) -> None:
    """Both total formats are thresholded."""
    assert _run_with_body(http_backend, body) == expected.value
    (request,) = http_backend.requests
    assert request.method == "POST"
    assert request.url.path == "/logs/_search"
    assert "query" in json.loads(request.content)


def test_search_post_is_not_retried(http_backend: FakeHttpBackend) -> None:
    """A gateway error on POST is reported, not repeated: POST is not idempotent."""
    http_backend.reply(httpx.Response(503))
    code = CheckLogErrors().run(["--endpoint", "http://es:9200", "--index", "logs"])
    assert code == Status.CRITICAL.value
    assert len(http_backend.requests) == 1
