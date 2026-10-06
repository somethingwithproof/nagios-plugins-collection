"""Validate health schemas, freshness thresholds and monitoring failures."""

import datetime as dt
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_component_status import ComponentStatusChecker
from nagios_plugins.plugins.check_jobs import JobStatusChecker
from nagios_plugins.plugins.check_monghealth import MongoHealthChecker as LegacyMongoHealthChecker
from nagios_plugins.plugins.check_mongodb_health import MongoHealthChecker


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
    client_type = httpx.AsyncClient
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200, json={"status": state, "updated": updated.isoformat(), "response_time": 3}
        )
    )
    with patch(
        "httpx.AsyncClient", side_effect=lambda **kwargs: client_type(transport=transport, **kwargs)
    ):
        result = await ComponentStatusChecker("https://monitor.example", ["database"]).check()
    assert result.status == expected
    assert result.metrics["total_components"] == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("response_status", [500, 404])
async def test_component_api_failure(response_status: int) -> None:
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(response_status))
    )
    with patch("httpx.AsyncClient", return_value=client):
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
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    )
    with patch("httpx.AsyncClient", return_value=client):
        result = await JobStatusChecker("https://monitor.example/jobs").check_jobs()
    assert result.status == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("status,body", [(503, "offline"), (200, "invalid json")])
async def test_job_health_api_failure(status: int, body: str) -> None:
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(status, text=body))
    )
    with patch("httpx.AsyncClient", return_value=client):
        result = await JobStatusChecker("https://monitor.example/jobs").check_jobs()
    assert result.status == Status.UNKNOWN


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "alive,search,expected",
    [(False, True, Status.CRITICAL), (True, False, Status.CRITICAL), (True, True, Status.OK)],
)
async def test_mongodb_health_api(alive: bool, search: bool, expected: Status) -> None:
    payload = {"alive": alive, "search_reachable": search, "site_api_reachable": True}
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    )
    with patch("httpx.AsyncClient", return_value=client):
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
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    )
    with patch("httpx.AsyncClient", return_value=client):
        result = await LegacyMongoHealthChecker("monitor.example", ssl=True).check_components(
            [("search", True)]
        )
    assert result.status.value == expected.value
