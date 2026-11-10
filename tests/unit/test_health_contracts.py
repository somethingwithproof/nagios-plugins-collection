# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Validate health schemas, freshness thresholds and monitoring failures."""

import datetime as dt

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_component_status import ComponentStatusChecker
from nagios_plugins.plugins.check_jobs import JobStatusChecker
from nagios_plugins.plugins.check_monghealth import MongoHealthChecker as LegacyMongoHealthChecker
from nagios_plugins.plugins.check_mongodb_health import MongoHealthChecker
from tests.fakes import serve_http


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("state", "age", "expected"),
    [
        ("ok", 0, Status.OK),
        ("ok", 15, Status.WARNING),
        ("ok", 30, Status.CRITICAL),
        ("error", 0, Status.CRITICAL),
    ],
)
async def test_component_freshness(state: str, age: int, expected: Status) -> None:
    updated = dt.datetime.now(dt.UTC) - dt.timedelta(minutes=age)
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200, json={"status": state, "updated": updated.isoformat(), "response_time": 3}
        )
    )
    with serve_http(transport.handle_request):
        result = await ComponentStatusChecker("https://monitor.example", ["database"]).check()
    assert result.status == expected
    assert result.metrics["total_components"] == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("response_status", [500, 404])
async def test_component_api_failure(response_status: int) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(response_status))
    with serve_http(transport.handle_request):
        result = await ComponentStatusChecker("monitor.example", ["database"]).check()
    assert result.status == Status.CRITICAL


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"status": "ok"}, Status.OK),
        ({"status": "down", "message": "maintenance\nretry"}, Status.WARNING),
        (
            {
                "status": "ok",
                "components": [{"name": "worker", "status": "error", "message": "offline"}],
            },
            Status.WARNING,
        ),
        ({"status": "ok", "components": [{"name": "worker", "status": "ok"}]}, Status.OK),
    ],
)
async def test_job_health(payload: dict, expected: Status) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    with serve_http(transport.handle_request):
        result = await JobStatusChecker("https://monitor.example/jobs").check_jobs()
    assert result.status == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("status,body", [(503, "offline"), (200, "invalid json")])
async def test_job_health_api_failure(status: int, body: str) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(status, text=body))
    with serve_http(transport.handle_request):
        result = await JobStatusChecker("https://monitor.example/jobs").check_jobs()
    assert result.status == Status.UNKNOWN


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "alive,search,expected",
    [(False, True, Status.CRITICAL), (True, False, Status.CRITICAL), (True, True, Status.OK)],
)
async def test_mongodb_health_api(alive: bool, search: bool, expected: Status) -> None:
    payload = {"alive": alive, "search_reachable": search, "site_api_reachable": True}
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    with serve_http(transport.handle_request):
        result = await MongoHealthChecker("https://monitor.example/health", mode=2).check()
    assert result.status == expected
    assert result.metrics["engine_alive"] == int(alive)


def test_invalid_mongodb_mode() -> None:
    with pytest.raises(ValueError, match="Invalid mode"):
        MongoHealthChecker("monitor.example", mode=99)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"alive": False}, Status.CRITICAL),
        ({"alive": True}, Status.CRITICAL),
        ({"alive": True, "search": False}, Status.CRITICAL),
        ({"alive": True, "search": True}, Status.OK),
    ],
)
async def test_legacy_mongodb_components(payload: dict, expected: Status) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    with serve_http(transport.handle_request):
        result = await LegacyMongoHealthChecker("monitor.example", ssl=True).check_components(
            [("search", True)]
        )
    assert result.status.value == expected.value


@pytest.mark.asyncio
@pytest.mark.parametrize(("state", "age"), [("error", 0), ("ok", 15), ("ok", 0)])
async def test_component_status_line_has_one_status_prefix(state: str, age: int) -> None:
    updated = dt.datetime.now(dt.UTC) - dt.timedelta(minutes=age)
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"status": state, "updated": updated.isoformat()})
    )
    with serve_http(transport.handle_request):
        result = await ComponentStatusChecker("https://monitor.example", ["database"]).check()
    line = str(result).splitlines()[0]
    assert line.startswith(f"{result.status} - ")
    assert not line.startswith(f"{result.status} - {result.status}")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"alive": False},
        {"alive": True, "search_reachable": False},
        {"alive": True, "search_reachable": True, "site_api_reachable": True},
    ],
)
async def test_mongodb_status_line_has_one_status_prefix(payload: dict) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    with serve_http(transport.handle_request):
        result = await MongoHealthChecker("https://monitor.example/health", mode=2).check()
    line = str(result).splitlines()[0]
    assert not line.startswith(f"{result.status} - {result.status}")
    assert line.count(" - ") == 1


MALFORMED = [
    httpx.Response(200, text="<html>maintenance</html>"),
    httpx.Response(200, json=[]),
    httpx.Response(200, json={}),
    httpx.Response(500, text="boom"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("answer", MALFORMED, ids=["html", "list", "empty", "http-500"])
async def test_malformed_component_answers_are_critical(answer: httpx.Response) -> None:
    with serve_http(lambda request: answer):
        result = await ComponentStatusChecker("https://monitor.example", ["database"]).check()
    assert result.status == Status.CRITICAL


@pytest.mark.asyncio
@pytest.mark.parametrize("answer", MALFORMED, ids=["html", "list", "empty", "http-500"])
async def test_malformed_mongodb_health_answers_are_critical(answer: httpx.Response) -> None:
    with serve_http(lambda request: answer):
        result = await MongoHealthChecker("https://monitor.example/health", mode=2).check()
    assert result.status == Status.CRITICAL
    assert result.message.startswith("Error connecting to MongoDB health endpoint: ")
