# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for OAuth2 token checker."""

from urllib.parse import parse_qs

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_oauth2_token import CheckOAuth2Token
from tests.fakes import FakeHttpBackend

ARGS = ["--token-url", "https://issuer/token", "--client-id", "id", "--client-secret", "s"]


def _run_with_body(backend: FakeHttpBackend, body: object, *extra: str) -> int:
    backend.reply(httpx.Response(200, json=body))
    return CheckOAuth2Token().run([*ARGS, *extra])


def test_token_ok_and_scopes(http_backend: FakeHttpBackend) -> None:
    body = {"access_token": "t", "expires_in": 3600, "scope": "openid profile"}
    code = _run_with_body(http_backend, body, "--scope", "openid", "--scope", "profile")
    assert code == Status.OK.value
    form = parse_qs(http_backend.requests[0].content.decode())
    assert form["grant_type"] == ["client_credentials"]
    assert form["scope"] == ["openid profile"]


@pytest.mark.parametrize("body", [{}, {"expires_in": 3600}, {"access_token": ""}, []])
def test_success_without_access_token_is_critical(
    http_backend: FakeHttpBackend, body: object
) -> None:
    """A 200 response that issues no token is the failure being monitored."""
    assert _run_with_body(http_backend, body) == Status.CRITICAL.value


def test_missing_expires_in_is_not_reported_as_zero(
    http_backend: FakeHttpBackend, capsys: pytest.CaptureFixture[str]
) -> None:
    """expires_in is optional, so it is omitted rather than published as 0."""
    assert _run_with_body(http_backend, {"access_token": "t"}) == Status.OK.value
    out = capsys.readouterr().out
    assert "expires_in=unknown" in out
    assert "expires_in=0" not in out


def test_rejected_client_is_critical_without_the_secret(
    http_backend: FakeHttpBackend, capsys: pytest.CaptureFixture[str]
) -> None:
    http_backend.reply(httpx.Response(401, json={"error": "invalid_client"}))
    assert CheckOAuth2Token().run(ARGS) == Status.CRITICAL.value
    out = capsys.readouterr().out
    assert out.startswith("CRITICAL - HTTP error: HTTP 401 Unauthorized from https://issuer/token")
