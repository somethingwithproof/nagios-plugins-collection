# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Exercise the synchronous CLI with actual async HTTP client behavior."""

from datetime import timedelta
from unittest.mock import patch

import httpx
import pytest
from hypothesis import given
from hypothesis import strategies as st

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_http_sli import CheckHttpSli
from tests.fakes import serve_http


@pytest.mark.parametrize("samples", [1, 2])
def test_http_sli_ok(samples: int) -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        response = httpx.Response(200, request=request)
        response.elapsed = timedelta(milliseconds=50)
        return response

    transport = httpx.MockTransport(respond)
    with serve_http(transport.handle_request):
        code = CheckHttpSli().run(["--url", "https://example.com", "--samples", str(samples)])
    assert code == Status.OK.value


@pytest.mark.parametrize("thresholds", [[], ["--warning", "200"], ["--critical", "500"]])
def test_all_failed_probes_are_critical(thresholds: list[str]) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(503))
    with serve_http(transport.handle_request):
        code = CheckHttpSli().run(["--url", "https://example.com", *thresholds])
    assert code == Status.CRITICAL.value


def _run(statuses: list[int], latency_ms: int, *args: str) -> tuple[int, str]:
    """Probe with responses cycling through ``statuses`` and return code and status line."""
    responses = iter(statuses)

    def respond(request: httpx.Request) -> httpx.Response:
        response = httpx.Response(next(responses), request=request)
        response.elapsed = timedelta(milliseconds=latency_ms)
        return response

    transport = httpx.MockTransport(respond)
    with (
        serve_http(transport.handle_request),
        patch("sys.stdout.write") as write,
    ):
        code = CheckHttpSli().run(["--url", "https://example.com", "--samples", "4", *args])
    return code, write.call_args.args[0]


def test_error_rate_threshold_ignores_latency() -> None:
    """An error-rate range is compared with the error rate, never with p95 in ms."""
    code, _ = _run([200] * 4, 800, "--error-rate-warning", "0.05")
    assert code == Status.OK.value


@pytest.mark.parametrize(
    "args,expected",
    [
        (["--error-rate-warning", "0.2", "--error-rate-critical", "0.5"], Status.WARNING),
        (["--error-rate-critical", "0.2"], Status.CRITICAL),
        (["--latency-critical", "100"], Status.OK),
    ],
)
def test_error_rate_thresholds(args: list[str], expected: Status) -> None:
    """One failure in four samples is a 25% error rate."""
    code, _ = _run([200, 200, 200, 503], 50, *args)
    assert code == expected.value


@pytest.mark.parametrize(
    "args,expected",
    [
        (["--latency-warning", "300", "--latency-critical", "1000"], Status.WARNING),
        (["-w", "300", "-c", "1000"], Status.WARNING),
        (["-c", "400"], Status.CRITICAL),
        (["--latency-warning", "600"], Status.OK),
    ],
)
def test_latency_thresholds_and_aliases(args: list[str], expected: Status) -> None:
    """-w/-c are the p95 latency range in ms, matching --latency-warning/--latency-critical."""
    code, _ = _run([200] * 4, 500, *args)
    assert code == expected.value


def test_alias_and_explicit_latency_option_conflict() -> None:
    with pytest.raises(SystemExit) as exited:
        _run([200] * 4, 50, "-w", "300", "--latency-warning", "300")
    assert exited.value.code == 3


def test_perfdata_carries_each_threshold_and_skips_inf_latency() -> None:
    code, line = _run([200] * 4, 50, "-w", "300", "--error-rate-critical", "0.5")
    assert code == Status.OK.value
    assert "p95_ms=50;300" in line
    assert "error_rate=0;;0.5;0;1" in line
    code, line = _run([503] * 4, 50)
    assert code == Status.CRITICAL.value
    assert "inf" not in line
    assert "p95=n/a" in line


@given(st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=50))
def test_percentiles_stay_within_the_observed_latencies(latencies: list[float]) -> None:
    """A percentile of measured latencies can never exceed the slowest probe."""
    p50, p95, p99 = CheckHttpSli._percentiles(latencies)
    assert min(latencies) <= p50 <= p95 <= p99 <= max(latencies)


def test_three_samples_do_not_extrapolate_beyond_the_slowest() -> None:
    """The default sample count: p95 of 100/200/300 ms is 290 ms, not 300+."""
    p50, p95, p99 = CheckHttpSli._percentiles([100.0, 200.0, 300.0])
    assert (p50, p95, p99) == pytest.approx((200.0, 290.0, 298.0))
