# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""check_dns_health, check_k8s_node_status and check_oauth2_token apply -w/-c."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_dns_health import CheckDnsHealth
from nagios_plugins.plugins.check_k8s_node_status import CheckK8sNodeStatus
from nagios_plugins.plugins.check_oauth2_token import CheckOAuth2Token
from nagios_plugins.services.k8s import NodeSummary
from tests.fakes import serve_http


@pytest.mark.parametrize(
    "rtt,args,expected",
    [
        (0.5, [], Status.OK),
        (0.03, ["-w", "20"], Status.WARNING),
        (0.05, ["-w", "20", "-c", "40"], Status.CRITICAL),
    ],
)
def test_dns_rtt_thresholds(
    rtt: float, args: list[str], expected: Status, capsys: pytest.CaptureFixture[str]
) -> None:
    pytest.importorskip("dns.resolver")
    answer = MagicMock()
    answer.__len__.return_value = 1
    answer.response.time = rtt
    resolver = MagicMock()
    resolver.resolve.return_value = answer
    with patch("dns.resolver.Resolver", return_value=resolver):
        assert CheckDnsHealth().run(["--name", "www.example", *args]) == expected.value
    assert f"rtt_ms={int(rtt * 1000)}" in capsys.readouterr().out


def _nodes(not_ready: int, *args: str, pressure: int = 0) -> int:
    summary = NodeSummary(5, not_ready, pressure, 0, 0)
    with patch(
        "nagios_plugins.plugins.check_k8s_node_status.summarize_nodes", return_value=summary
    ):
        return CheckK8sNodeStatus().run(list(args))


@pytest.mark.parametrize(
    "not_ready,args,expected",
    [
        (1, [], Status.CRITICAL),
        (0, [], Status.OK),
        (1, ["-w", "0", "-c", "2"], Status.WARNING),
        (2, ["-w", "0", "-c", "2"], Status.WARNING),
        (3, ["-w", "0", "-c", "2"], Status.CRITICAL),
        (0, ["-w", "0", "-c", "2"], Status.OK),
    ],
)
def test_unready_node_count_thresholds(
    not_ready: int, args: list[str], expected: Status, capsys: pytest.CaptureFixture[str]
) -> None:
    assert _nodes(not_ready, *args) == expected.value
    if args:
        assert f"not_ready={not_ready};0;2" in capsys.readouterr().out


def test_node_pressure_stays_critical_with_thresholds() -> None:
    assert _nodes(0, "-c", "5", pressure=1) == Status.CRITICAL.value


def _token(body: dict[str, object], *args: str) -> int:
    base = ["--token-url", "https://idp.example/token", "--client-id", "id"]
    with serve_http(lambda request: httpx.Response(200, json=body)):
        return CheckOAuth2Token().run([*base, "--client-secret", "x-secret", *args])


@pytest.mark.parametrize(
    "expires_in,expected",
    [(3600, Status.OK), (299, Status.WARNING), (59, Status.CRITICAL)],
)
def test_token_lifetime_lower_bounds(
    expires_in: int, expected: Status, capsys: pytest.CaptureFixture[str]
) -> None:
    body = {"access_token": "issued-token", "expires_in": expires_in}
    assert _token(body, "-w", "300:", "-c", "60:") == expected.value
    assert f"expires_in={expires_in};300:;60:" in capsys.readouterr().out


def test_missing_lifetime_with_thresholds_is_unknown() -> None:
    assert _token({"access_token": "issued-token"}, "-w", "300:") == Status.UNKNOWN.value
    assert _token({"access_token": "issued-token"}) == Status.OK.value


def test_missing_scope_and_short_lifetime_reports_the_worse() -> None:
    body = {"access_token": "issued-token", "expires_in": 10, "scope": ""}
    assert _token(body, "--scope", "read", "-c", "60:") == Status.CRITICAL.value
