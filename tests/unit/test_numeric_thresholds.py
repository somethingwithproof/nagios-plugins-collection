# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""check_tls_expiry and check_website_status keep plain-number thresholds.

Their -w/-c are days and seconds, not Nagios ranges. A range form must be a
usage error (exit 3, one status line), never a traceback, and the thresholds
must appear in perfdata as the equivalent range.
"""

from collections.abc import Callable
from datetime import timedelta
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins.base import Status, threshold_check
from nagios_plugins.plugins.check_tls_expiry import CheckTlsExpiry, at_or_below
from nagios_plugins.plugins.check_website_status import CheckWebsiteStatus
from nagios_plugins.services.tls import TlsCertInfo
from tests.fakes import serve_http

RANGE_FORMS = ["30:", "@0:30", "~:30", "10:20", "abc"]
CERT = TlsCertInfo(not_after=None, issuer="i", subject="s", san_count=1)  # type: ignore[arg-type]


def _tls(remaining: int, *args: str) -> int:
    with (
        patch("nagios_plugins.plugins.check_tls_expiry.fetch_server_cert", return_value=CERT),
        patch("nagios_plugins.plugins.check_tls_expiry.days_remaining", return_value=remaining),
    ):
        return CheckTlsExpiry().run(["--host", "example.com", *args])


def _site(seconds: float) -> Callable[[httpx.Request], httpx.Response]:
    def respond(request: httpx.Request) -> httpx.Response:
        response = httpx.Response(200, text="ok", request=request)
        response.elapsed = timedelta(seconds=seconds)
        return response

    return respond


def _website(seconds: float, *args: str) -> int:
    with serve_http(_site(seconds)):
        return CheckWebsiteStatus().run(["--url", "https://example.com", *args])


@pytest.mark.parametrize("option", ["-w", "-c"])
@pytest.mark.parametrize("value", RANGE_FORMS)
@pytest.mark.parametrize(
    "run", [lambda *a: _tls(10, *a), lambda *a: _website(0.1, *a)], ids=["tls", "website"]
)
def test_range_forms_are_usage_errors(
    run: Callable[..., int], option: str, value: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exited:
        run(f"{option}={value}")
    assert exited.value.code == Status.UNKNOWN.value
    out = capsys.readouterr()
    assert out.out.startswith("UNKNOWN - check_")
    assert "not a range" in out.out
    assert len(out.out.splitlines()) == 1
    assert "Traceback" not in out.err


@pytest.mark.parametrize(
    "remaining,expected",
    [
        (31, Status.OK),
        (30, Status.WARNING),
        (8, Status.WARNING),
        (7, Status.CRITICAL),
        (0, Status.CRITICAL),
        (-3, Status.CRITICAL),
    ],
)
def test_tls_alerts_at_or_below_days(
    remaining: int, expected: Status, capsys: pytest.CaptureFixture[str]
) -> None:
    assert _tls(remaining, "-w", "30", "-c", "7") == expected.value
    assert f"days_remaining={remaining};@~:30;@~:7 " in capsys.readouterr().out


def test_tls_critical_zero_is_honored(capsys: pytest.CaptureFixture[str]) -> None:
    """-c 0 alerts on the expiry day; a falsy 0 must not disable it."""
    assert _tls(0, "-c", "0") == Status.CRITICAL.value
    assert _tls(1, "-c", "0") == Status.OK.value


def test_tls_without_thresholds_is_ok(capsys: pytest.CaptureFixture[str]) -> None:
    assert _tls(-1) == Status.OK.value
    assert "days_remaining=-1 " in capsys.readouterr().out


@pytest.mark.parametrize("limit", [-5, 0, 1, 30])
@pytest.mark.parametrize("remaining", range(-10, 40))
def test_tls_perfdata_range_matches_the_alert(limit: int, remaining: int) -> None:
    """The published range alerts for exactly the days the check alerts on."""
    alerts = threshold_check(remaining, critical=at_or_below(limit)) == Status.CRITICAL
    assert alerts == (remaining <= limit)


@pytest.mark.parametrize(
    "seconds,expected",
    [(0.4, Status.OK), (0.5, Status.OK), (0.6, Status.WARNING), (1.5, Status.CRITICAL)],
)
def test_website_alerts_above_seconds(
    seconds: float, expected: Status, capsys: pytest.CaptureFixture[str]
) -> None:
    assert _website(seconds, "-w", "0.5", "-c", "1") == expected.value
    assert capsys.readouterr().out.rstrip().endswith(f" duration={seconds};0.5;1")


def test_website_default_thresholds_in_perfdata(capsys: pytest.CaptureFixture[str]) -> None:
    assert _website(0.25) == Status.OK.value
    assert "duration=0.25;1;2" in capsys.readouterr().out


@pytest.mark.parametrize("value", ["-1", "nan", "inf"])
def test_website_rejects_impossible_seconds(value: str) -> None:
    with pytest.raises(SystemExit) as exited:
        _website(0.1, f"-w={value}")
    assert exited.value.code == Status.UNKNOWN.value
