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


@pytest.mark.parametrize(
    "hits,expected",
    [(1, Status.OK), (2, Status.WARNING), (10, Status.WARNING), (11, Status.CRITICAL)],
)
def test_thresholds_are_nagios_ranges(
    http_backend: FakeHttpBackend, hits: int, expected: Status
) -> None:
    """-w 1 -c 10 alert above 1 and 10; a count equal to N is inside 0..N."""
    assert _run_with_body(http_backend, {"hits": {"total": hits}}) == expected.value


def test_search_counts_every_hit(http_backend: FakeHttpBackend) -> None:
    """ES 7+ caps hits.total at 10,000 unless the search asks for an exact count."""
    body = {"hits": {"total": {"value": 25000, "relation": "eq"}}}
    assert _run_with_body(http_backend, body) == Status.CRITICAL.value
    assert json.loads(http_backend.requests[0].content)["track_total_hits"] is True


def test_lower_bound_count_is_unknown(
    http_backend: FakeHttpBackend, capsys: pytest.CaptureFixture[str]
) -> None:
    body = {"hits": {"total": {"value": 10000, "relation": "gte"}}}
    assert _run_with_body(http_backend, body) == Status.UNKNOWN.value
    assert "at least 10000 errors" in capsys.readouterr().out


def test_elasticsearch_6_is_asked_again_without_track_total_hits(
    http_backend: FakeHttpBackend,
) -> None:
    rejected = httpx.Response(
        400,
        json={"error": {"type": "parsing_exception", "reason": "Unknown key [track_total_hits]"}},
    )
    http_backend.reply(rejected, httpx.Response(200, json={"hits": {"total": 25}}))
    code = CheckLogErrors().run(["--endpoint", "http://es:9200", "--index", "logs", "-c", "10"])
    assert code == Status.CRITICAL.value
    first, second = (json.loads(request.content) for request in http_backend.requests)
    assert first["track_total_hits"] is True
    assert "track_total_hits" not in second


def test_other_bad_requests_are_not_repeated(http_backend: FakeHttpBackend) -> None:
    http_backend.reply(httpx.Response(400, json={"error": "bad query"}))
    code = CheckLogErrors().run(["--endpoint", "http://es:9200", "--index", "logs"])
    assert code == Status.CRITICAL.value
    assert len(http_backend.requests) == 1
