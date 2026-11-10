# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Credentials never reach plugin output and can be supplied outside argv."""

import argparse
import json
import logging
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins.base import CheckResult, NagiosPlugin, Status, configure_logging
from nagios_plugins.plugins import check_monghealth
from nagios_plugins.plugins.check_oauth2_token import CheckOAuth2Token
from nagios_plugins.plugins.check_postgres_replication_lag import CheckPostgresReplicationLag
from nagios_plugins.plugins.check_prometheus_query import CheckPrometheusQuery
from nagios_plugins.redaction import redact

SECRET = "s3cr3t-value"


@pytest.mark.parametrize(
    "text",
    [
        f"for url 'https://monitor:{SECRET}@prom.example/api/v1/query?query=up'",
        f"redis://:{SECRET}@cache.example:6379/0",
        f"https://es.example/_search?q=1&token={SECRET}&size=0",
        f"https://api.example/?api_key={SECRET}",
        f"host=db.example user=monitor password={SECRET} dbname=app",
        f"host=db.example password='{SECRET} with space' dbname=app",
        f'client_secret="{SECRET}"',
        f"Authorization: Bearer {SECRET}",
    ],
)
def test_redact_masks_credentials(text: str) -> None:
    assert SECRET not in redact(text)
    assert "***" in redact(text)


def test_redact_keeps_ordinary_text() -> None:
    text = (
        "HTTP 503 for url 'https://prom.example/api/v1/query?query=up' expires_in=3600 key_count=2"
    )
    assert redact(text) == text


def test_check_result_output_and_json_are_redacted() -> None:
    result = CheckResult(
        Status.CRITICAL,
        f"HTTP error: https://u:{SECRET}@h.example/",
        details=f"token={SECRET}",
    )
    assert SECRET not in str(result)
    assert SECRET not in result.to_json()
    assert json.loads(result.to_json())["message"] == "HTTP error: https://***@h.example/"


def test_logged_tracebacks_are_redacted(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(0)
    try:
        raise RuntimeError(f"connect to postgresql://monitor:{SECRET}@db.example/app failed")
    except RuntimeError:
        logging.getLogger("test").exception("query failed")
    err = capsys.readouterr().err
    assert "Traceback" in err
    assert SECRET not in err


def test_http_error_with_userinfo_url_is_redacted(capsys: pytest.CaptureFixture[str]) -> None:
    """httpx puts the full request URL, including userinfo, in exception text."""
    url = f"https://monitor:{SECRET}@prom.example"
    request = httpx.Request("GET", f"{url}/api/v1/query")
    error = httpx.HTTPStatusError(
        f"Client error '401 Unauthorized' for url '{request.url}'",
        request=request,
        response=httpx.Response(401, request=request),
    )
    with patch("httpx.Client") as client:
        client.return_value.__enter__.return_value.get.side_effect = error
        code = CheckPrometheusQuery().run(["--server", url, "--query", "up"])
    out = capsys.readouterr().out
    assert code == Status.CRITICAL.value
    assert SECRET not in out
    assert "https://***@prom.example" in out


def test_unhandled_exception_message_is_redacted(capsys: pytest.CaptureFixture[str]) -> None:
    class Failing(NagiosPlugin):
        def check(self, args: argparse.Namespace) -> CheckResult:
            raise ValueError(f"bad response from https://u:{SECRET}@h.example/")

    assert Failing().run([]) == Status.UNKNOWN.value
    captured = capsys.readouterr()
    assert SECRET not in captured.out
    assert SECRET not in captured.err


def _token_args(*extra: str) -> list[str]:
    return ["--token-url", "https://issuer.example/token", "--client-id", "id", *extra]


def _posted_secret(*args: str) -> str:
    with patch("httpx.Client") as client:
        response = client.return_value.__enter__.return_value.post.return_value
        response.json.return_value = {"access_token": "t", "expires_in": 60}
        assert CheckOAuth2Token().run(list(args)) == Status.OK.value
        return str(
            client.return_value.__enter__.return_value.post.call_args.kwargs["data"][
                "client_secret"
            ]
        )


def test_client_secret_from_argv_still_works() -> None:
    assert _posted_secret(*_token_args("--client-secret", SECRET)) == SECRET


def test_client_secret_from_file(tmp_path: Path) -> None:
    secret_file = tmp_path / "secret"
    secret_file.write_text(f"{SECRET}\n", encoding="utf-8")
    assert _posted_secret(*_token_args("--client-secret-file", str(secret_file))) == SECRET


def test_client_secret_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHECK_OAUTH2_CLIENT_SECRET", SECRET)
    assert _posted_secret(*_token_args()) == SECRET


def test_argv_takes_precedence_over_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHECK_OAUTH2_CLIENT_SECRET", "from-env")
    assert _posted_secret(*_token_args("--client-secret", SECRET)) == SECRET


def test_missing_required_secret_is_a_usage_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("CHECK_OAUTH2_CLIENT_SECRET", raising=False)
    plugin, args = CheckOAuth2Token(), _token_args()
    with pytest.raises(SystemExit) as exited:
        plugin.run(args)
    assert exited.value.code == 3
    assert "$CHECK_OAUTH2_CLIENT_SECRET is required" in capsys.readouterr().out


def test_unreadable_secret_file_is_a_usage_error(tmp_path: Path) -> None:
    plugin = CheckOAuth2Token()
    args = _token_args("--client-secret-file", str(tmp_path / "missing"))
    with pytest.raises(SystemExit) as exited:
        plugin.run(args)
    assert exited.value.code == 3


def test_secret_flag_and_file_are_mutually_exclusive(tmp_path: Path) -> None:
    plugin = CheckOAuth2Token()
    args = _token_args("--client-secret", "a", "--client-secret-file", str(tmp_path))
    with pytest.raises(SystemExit) as exited:
        plugin.run(args)
    assert exited.value.code == 3


def test_postgres_dsn_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    dsn = f"postgresql://monitor:{SECRET}@db.example/app"
    monkeypatch.setenv("CHECK_POSTGRES_DSN", dsn)
    with patch(
        "nagios_plugins.plugins.check_postgres_replication_lag.replication_lag_seconds",
        return_value=1.0,
    ) as lag:
        assert CheckPostgresReplicationLag().run([]) == Status.OK.value
    assert lag.call_args.args[0] == dsn


def test_monghealth_password_from_file(tmp_path: Path) -> None:
    secret_file = tmp_path / "password"
    secret_file.write_text(SECRET, encoding="utf-8")
    args = check_monghealth.CheckMonghealth().parse_args(
        ["--host", "db", "--password-file", str(secret_file)]
    )
    assert args.password == SECRET
