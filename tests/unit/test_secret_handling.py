# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Credentials never reach plugin output and can be supplied outside argv."""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs

import httpx
import pytest

from nagios_plugins.base import (
    MAX_SECRET_BYTES,
    CheckResult,
    NagiosPlugin,
    Status,
    configure_logging,
)
from nagios_plugins.plugins import check_jobs, check_monghealth
from nagios_plugins.plugins.check_oauth2_token import CheckOAuth2Token
from nagios_plugins.plugins.check_postgres_replication_lag import CheckPostgresReplicationLag
from nagios_plugins.plugins.check_prometheus_query import CheckPrometheusQuery
from nagios_plugins.redaction import redact
from tests.fakes import FakeHttpBackend, serve_http

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
    with serve_http(lambda request: httpx.Response(401)):
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
    backend = FakeHttpBackend()
    backend.reply(httpx.Response(200, json={"access_token": "t", "expires_in": 60}))
    with serve_http(backend):
        assert CheckOAuth2Token().run(list(args)) == Status.OK.value
    (secret,) = parse_qs(backend.requests[0].content.decode())["client_secret"]
    return secret


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
    monkeypatch.delenv("CHECK_OAUTH2_CLIENT_SECRET_FILE", raising=False)
    plugin, args = CheckOAuth2Token(), _token_args()
    with pytest.raises(SystemExit) as exited:
        plugin.run(args)
    assert exited.value.code == 3
    assert (
        "$CHECK_OAUTH2_CLIENT_SECRET or $CHECK_OAUTH2_CLIENT_SECRET_FILE is required"
        in capsys.readouterr().out
    )


def test_client_secret_from_file_named_in_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The ``*_FILE`` convention used for mounted container secrets."""
    secret_file = tmp_path / "secret"
    secret_file.write_text(SECRET + "\n", encoding="utf-8")
    monkeypatch.delenv("CHECK_OAUTH2_CLIENT_SECRET", raising=False)
    monkeypatch.setenv("CHECK_OAUTH2_CLIENT_SECRET_FILE", str(secret_file))
    assert _posted_secret(*_token_args()) == SECRET


def test_environment_value_takes_precedence_over_environment_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    secret_file = tmp_path / "secret"
    secret_file.write_text("from-file", encoding="utf-8")
    monkeypatch.setenv("CHECK_OAUTH2_CLIENT_SECRET", "from-env")
    monkeypatch.setenv("CHECK_OAUTH2_CLIENT_SECRET_FILE", str(secret_file))
    assert _posted_secret(*_token_args()) == "from-env"


def test_unreadable_environment_secret_file_is_a_usage_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("CHECK_OAUTH2_CLIENT_SECRET", raising=False)
    monkeypatch.setenv("CHECK_OAUTH2_CLIENT_SECRET_FILE", str(tmp_path / "missing"))
    plugin, args = CheckOAuth2Token(), _token_args()
    with pytest.raises(SystemExit) as exited:
        plugin.parse_args(args)
    assert exited.value.code == 3
    assert "cannot read the --client-secret file" in capsys.readouterr().out


@pytest.mark.parametrize(
    "flag,env,header,expected",
    [
        ("--bearer-token", "CHECK_JOBS_BEARER_TOKEN", "Authorization", f"Bearer {SECRET}"),
        ("--api-key", "CHECK_JOBS_API_KEY", "X-API-Key", SECRET),
    ],
)
def test_every_credential_flag_reads_secret_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    flag: str,
    env: str,
    header: str,
    expected: str,
) -> None:
    """Each shared credential flag accepts its -file option and ``*_FILE`` variable."""
    secret_file = tmp_path / "secret"
    secret_file.write_text(SECRET, encoding="utf-8")
    base = ["--url", "https://jobs.example/api"]
    for args, environ in (
        ([f"{flag}-file", str(secret_file)], {}),
        ([], {env: SECRET}),
        ([], {f"{env}_FILE": str(secret_file)}),
    ):
        backend = FakeHttpBackend()
        backend.reply(httpx.Response(200, json={"jobs": []}))
        with monkeypatch.context() as scoped, serve_http(backend):
            for name, value in environ.items():
                scoped.setenv(name, value)
            check_jobs.CheckJobs().run([*base, *args])
        assert backend.requests[0].headers[header] == expected


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
        ["--host", "db", "--username", "monitor", "--password-file", str(secret_file)]
    )
    assert args.password == SECRET


def _usage_error(args: list[str], capsys: pytest.CaptureFixture[str]) -> str:
    with pytest.raises(SystemExit) as exited:
        CheckOAuth2Token().run(args)
    assert exited.value.code == 3
    captured = capsys.readouterr()
    assert captured.out.startswith("UNKNOWN - check_oauth2_token: cannot read the --client-secret")
    assert len(captured.out.splitlines()) == 1
    assert "Traceback" not in captured.err
    return captured.out


@pytest.mark.parametrize(
    "content,problem",
    [
        (b"\xff\xfesecret", "not UTF-8 text"),
        (b"a" * (MAX_SECRET_BYTES + 1), "larger than 64 KiB"),
    ],
)
def test_malformed_secret_file_is_a_usage_error(
    content: bytes, problem: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    secret_file = tmp_path / "secret"
    secret_file.write_bytes(content)
    out = _usage_error(_token_args("--client-secret-file", str(secret_file)), capsys)
    assert f"{secret_file}: {problem}" in out


def test_secret_file_at_the_size_limit_is_read(tmp_path: Path) -> None:
    secret_file = tmp_path / "secret"
    secret_file.write_bytes(b"a" * MAX_SECRET_BYTES)
    secret = _posted_secret(*_token_args("--client-secret-file", str(secret_file)))
    assert secret == "a" * MAX_SECRET_BYTES


def test_directory_as_secret_file_is_a_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out = _usage_error(_token_args("--client-secret-file", str(tmp_path)), capsys)
    assert "not a regular file" in out


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="POSIX FIFOs")
def test_fifo_secret_file_is_refused_without_waiting_for_a_writer(tmp_path: Path) -> None:
    """Opening a FIFO for reading blocks until a writer appears; it must be refused."""
    fifo = tmp_path / "secret"
    os.mkfifo(fifo)
    started = time.monotonic()
    completed = subprocess.run(
        [sys.executable, "-m", "nagios_plugins.plugins.check_oauth2_token"]
        + _token_args("--client-secret-file", str(fifo), "-t", "1"),
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert completed.returncode == 3
    assert completed.stdout.startswith("UNKNOWN - ")
    assert f"{fifo}: not a regular file" in completed.stdout
    assert time.monotonic() - started < 15


def test_stuck_secret_file_read_is_bounded_by_the_timeout(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A read that never returns (a hung network mount) ends at --timeout."""

    def stuck(path: str) -> str:
        time.sleep(30)
        return "never"

    started = time.monotonic()
    with patch("nagios_plugins.base._read_secret", side_effect=stuck):
        code = CheckOAuth2Token().run(_token_args("--client-secret-file", "/mnt/s", "-t", "1"))
    assert code == 3
    assert capsys.readouterr().out == "UNKNOWN - Plugin timed out after 1 seconds\n"
    assert time.monotonic() - started < 10
