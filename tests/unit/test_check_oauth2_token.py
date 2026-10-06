# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for OAuth2 token checker."""

from unittest.mock import MagicMock, patch

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
