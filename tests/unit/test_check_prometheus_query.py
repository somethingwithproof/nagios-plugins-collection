# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for Prometheus query plugin."""

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_prometheus_query import CheckPrometheusQuery
from tests.fakes import FakeHttpBackend

THRESHOLDS = ["-w", "1", "-c", "2"]


def _run(backend: FakeHttpBackend, data: object, *args: str) -> int:
    backend.reply(httpx.Response(200, json={"status": "success", "data": data}))
    return CheckPrometheusQuery().run(
        ["--server", "http://prom:9090", "--query", "up", *THRESHOLDS, *args]
    )


@pytest.mark.parametrize("sample,expected", [("0.42", Status.OK), ("5", Status.CRITICAL)])
def test_vector_sample_is_thresholded(
    http_backend: FakeHttpBackend, sample: str, expected: Status
) -> None:
    data = {"resultType": "vector", "result": [{"value": [0, sample]}]}
    assert _run(http_backend, data) == expected.value
    (request,) = http_backend.requests
    assert request.url.path == "/api/v1/query"
    assert request.url.params["query"] == "up"


@pytest.mark.parametrize(
    "data",
    [{"resultType": "vector", "result": []}, {}, {"resultType": "vector", "result": [{}]}],
)
def test_prom_empty_result_is_unknown(http_backend: FakeHttpBackend, data: object) -> None:
    """An absent series is missing data, not a sample of 0."""
    assert _run(http_backend, data) == Status.UNKNOWN.value


def test_prom_scalar_result(http_backend: FakeHttpBackend) -> None:
    """Scalar results carry the sample directly in ``result``."""
    assert _run(http_backend, {"resultType": "scalar", "result": [0, "1.5"]}) == 1


def test_bearer_token_from_environment(
    http_backend: FakeHttpBackend, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CHECK_PROMETHEUS_QUERY_BEARER_TOKEN", "s3cret")
    _run(http_backend, {"resultType": "scalar", "result": [0, "0"]})
    assert http_backend.requests[0].headers["Authorization"] == "Bearer s3cret"
