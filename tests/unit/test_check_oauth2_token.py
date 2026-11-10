# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for OAuth2 token checker."""

from unittest.mock import MagicMock, patch

import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_oauth2_token import CheckOAuth2Token


def test_token_ok_and_scopes() -> None:
    plugin = CheckOAuth2Token()
    ok_json = {"access_token": "t", "expires_in": 3600, "scope": "openid profile"}
    with patch("httpx.Client") as mock_client:
        mock = MagicMock()
        mock.__enter__.return_value.post.return_value.json.return_value = ok_json
        mock.__enter__.return_value.post.return_value.raise_for_status.return_value = None
        mock_client.return_value = mock
        code = plugin.run(
            [
                "--token-url",
                "https://issuer/token",
                "--client-id",
                "id",
                "--client-secret",
                "sec",
                "--scope",
                "openid",
                "--scope",
                "profile",
            ]
        )
        assert code == Status.OK.value


def _run_with_body(body: object) -> int:
    with patch("httpx.Client") as mock_client:
        response = mock_client.return_value.__enter__.return_value.post.return_value
        response.json.return_value = body
        response.raise_for_status.return_value = None
        return CheckOAuth2Token().run(
            ["--token-url", "https://issuer/token", "--client-id", "id", "--client-secret", "s"]
        )


@pytest.mark.parametrize("body", [{}, {"expires_in": 3600}, {"access_token": ""}, []])
def test_success_without_access_token_is_critical(body: object) -> None:
    """A 200 response that issues no token is the failure being monitored."""
    assert _run_with_body(body) == Status.CRITICAL.value


def test_missing_expires_in_is_not_reported_as_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """expires_in is optional, so it is omitted rather than published as 0."""
    assert _run_with_body({"access_token": "t"}) == Status.OK.value
    out = capsys.readouterr().out
    assert "expires_in=unknown" in out
    assert "expires_in=0" not in out
