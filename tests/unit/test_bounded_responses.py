# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Response bodies and plugin output are bounded."""

import gzip
from datetime import timedelta

import httpx
import pytest

from nagios_plugins.base import (
    MAX_DETAILS_CHARS,
    MAX_MESSAGE_CHARS,
    CheckResult,
    Status,
)
from nagios_plugins.plugins.check_prometheus_query import CheckPrometheusQuery
from nagios_plugins.plugins.check_website_status import CheckWebsiteStatus
from nagios_plugins.services import http
from tests.fakes import serve_http

LIMIT = 1000
SETTINGS = http.HttpSettings(max_response_bytes=LIMIT)


def _body(size: int, **headers: str) -> httpx.Response:
    return httpx.Response(200, content=b"x" * size, headers=headers)


def _gzipped(compressed: bytes) -> httpx.Response:
    """An unread gzip response, as the wire delivers it (passed through by the fake)."""
    response = httpx.Response(
        200, stream=httpx.ByteStream(compressed), headers={"Content-Encoding": "gzip"}
    )
    response.elapsed = timedelta(milliseconds=1)
    return response


@pytest.mark.parametrize("size", [0, LIMIT])
def test_body_up_to_the_limit_is_read(size: int) -> None:
    with serve_http(lambda request: _body(size)), http.client(SETTINGS) as client:
        response = client.get("https://api.example/")
    assert response.content == b"x" * size
    assert response.elapsed >= timedelta(0)


def test_larger_body_is_refused() -> None:
    with (
        serve_http(lambda request: _body(LIMIT + 1)),
        http.client(SETTINGS) as client,
        pytest.raises(http.ResponseTooLarge, match="larger than 1000 bytes"),
    ):
        client.get("https://u:p@api.example/data?token=t")


@pytest.mark.asyncio
async def test_async_larger_body_is_refused() -> None:
    with serve_http(lambda request: _body(LIMIT + 1)):
        async with http.async_client(SETTINGS) as client:
            with pytest.raises(http.ResponseTooLarge):
                await client.get("https://api.example/")


@pytest.mark.asyncio
async def test_async_body_keeps_json_and_status() -> None:
    with serve_http(lambda request: httpx.Response(201, json={"ok": True})):
        async with http.async_client(SETTINGS) as client:
            response = await client.get("https://api.example/")
    assert response.status_code == 201
    assert response.json() == {"ok": True}


def test_limit_applies_after_decompression() -> None:
    """A small gzip body that inflates past the limit is refused, not held in memory."""
    bomb = gzip.compress(b"0" * (LIMIT * 50))
    assert len(bomb) < LIMIT

    with (
        serve_http(lambda request: _gzipped(bomb)),
        http.client(SETTINGS) as client,
        pytest.raises(http.ResponseTooLarge),
    ):
        client.get("https://api.example/")


def test_compressed_body_within_the_limit_is_decoded() -> None:
    payload = b'{"value": 1}'

    with (
        serve_http(lambda request: _gzipped(gzip.compress(payload))),
        http.client(SETTINGS) as client,
    ):
        response = client.get("https://api.example/")
    assert response.json() == {"value": 1}
    assert "content-encoding" not in response.headers


def test_redirect_history_survives_the_bounded_read() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/old":
            return httpx.Response(302, headers={"Location": "https://api.example/new"})
        return httpx.Response(200, text="here")

    with serve_http(respond), http.client(SETTINGS, follow_redirects=True) as client:
        response = client.get("https://api.example/old")
    assert response.text == "here"
    assert [r.status_code for r in response.history] == [302]


def test_streaming_callers_read_for_themselves() -> None:
    with (
        serve_http(lambda request: _body(LIMIT * 3)),
        http.client(SETTINGS) as client,
        client.stream("GET", "https://api.example/") as response,
    ):
        assert len(response.read()) == LIMIT * 3


def test_oversized_answer_is_unknown(capsys: pytest.CaptureFixture[str]) -> None:
    with serve_http(lambda request: _body(5000)):
        code = CheckPrometheusQuery().run(
            ["--server", "https://prom.example", "--query", "up", "--max-response-bytes", "100"]
        )
    out = capsys.readouterr().out
    assert code == Status.UNKNOWN.value
    assert "larger than 100 bytes" in out


def test_oversized_answer_is_unknown_for_async_checks(capsys: pytest.CaptureFixture[str]) -> None:
    with serve_http(lambda request: _body(5000)):
        code = CheckWebsiteStatus().run(
            ["--url", "https://www.example/", "--max-response-bytes", "100"]
        )
    out, err = capsys.readouterr()
    assert code == Status.UNKNOWN.value
    assert out.startswith("UNKNOWN - Response from https://www.example/ is larger than 100 bytes")
    assert "Traceback" not in err


@pytest.mark.parametrize("value", ["0", "-1", "ten"])
def test_max_response_bytes_must_be_positive(value: str) -> None:
    with pytest.raises(SystemExit) as exited:
        CheckPrometheusQuery().parse_args(
            ["--server", "https://p", "--query", "up", f"--max-response-bytes={value}"]
        )
    assert exited.value.code == 3


def test_long_output_is_truncated() -> None:
    result = CheckResult(Status.OK, "m" * (MAX_MESSAGE_CHARS + 10), details="d" * 100_000)
    status_line, details = str(result).split("\n", 1)
    assert status_line.endswith(" [truncated 10 characters]")
    assert len(details) < MAX_DETAILS_CHARS + 64
    assert details.endswith(f"[truncated {100_000 - MAX_DETAILS_CHARS} characters]")
    assert "[truncated" in result.to_json()


def test_oversized_sli_probe_counts_as_failed(capsys: pytest.CaptureFixture[str]) -> None:
    from nagios_plugins.plugins.check_http_sli import CheckHttpSli

    with serve_http(lambda request: _body(5000)):
        code = CheckHttpSli().run(
            ["--url", "https://www.example/", "--samples", "2", "--max-response-bytes", "100"]
        )
    assert code == Status.CRITICAL.value
    assert "error_rate=100.00%" in capsys.readouterr().out
