# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Credentials never reach plugin output, whether recognized by pattern or registered."""

import logging

import httpx
import pytest

from nagios_plugins.base import CheckResult, Status, configure_logging
from nagios_plugins.plugins import check_jobs
from nagios_plugins.plugins.check_postgres_replication_lag import CheckPostgresReplicationLag
from nagios_plugins.plugins.check_prometheus_query import CheckPrometheusQuery
from nagios_plugins.redaction import (
    MASK,
    clear_secrets,
    redact,
    register_embedded_secrets,
    register_secret,
)
from nagios_plugins.services import http
from tests.fakes import FakeHttpBackend, serve_http

SECRET = "s3cr3t-value"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


@pytest.mark.parametrize(
    "text",
    [
        f'{{"password": "{SECRET}", "user": "monitor"}}',
        f"{{'password': '{SECRET}'}}",
        f"password: {SECRET}",
        f'"clientSecret":"{SECRET}"',
        f"X-API-Key: {SECRET}",
        f"x-auth-token: {SECRET}",
        f"Authorization: Token {SECRET}",
        f"Proxy-Authorization: Digest username=u, response={SECRET}",
        f"Set-Cookie: session={SECRET}; Path=/",
        f"private_key={SECRET}",
        f"aws_secret_access_key = {AWS_SECRET}",
        f'"SecretAccessKey": "{AWS_SECRET}", "SessionToken": "{SECRET}"',
        f"https://monitor:p@ss{SECRET}@db.example/app",
        f"redis://:{SECRET}@@cache.example:6379",
    ],
)
def test_patterns_mask_credential_forms(text: str) -> None:
    masked = redact(text)
    assert SECRET not in masked
    assert AWS_SECRET not in masked
    assert MASK in masked


def test_userinfo_is_masked_up_to_the_last_at_sign() -> None:
    assert redact("https://u:p@ss@db.example/x?q=a@b") == "https://***@db.example/x?q=a@b"


def test_aws_access_key_ids_are_masked() -> None:
    assert redact("AccessKeyId AKIAIOSFODNN7EXAMPLE and ASIAIOSFODNN7EXAMPLE") == (
        f"AccessKeyId {MASK} and {MASK}"
    )


def test_json_masking_keeps_the_quotes() -> None:
    assert redact(f'{{"token": "{SECRET}", "n": 1}}') == '{"token": "***", "n": 1}'


@pytest.mark.parametrize(
    "text",
    [
        "HTTP 503 for url 'https://prom.example/api/v1/query?query=up' expires_in=3600 key_count=2",
        "monkey=banana author: x primary_key_count=3 password_hint=none",
        "https://example.com/path?q=user@example.com",
    ],
)
def test_ordinary_text_is_unchanged(text: str) -> None:
    assert redact(text) == text


def test_registered_secret_is_masked_in_plain_and_encoded_forms() -> None:
    register_secret("p@ss word/1")
    text = "echo p@ss word/1, p%40ss%20word%2F1 and p%40ss+word%2F1"
    assert redact(text) == f"echo {MASK}, {MASK} and {MASK}"


def test_short_values_are_not_registered() -> None:
    register_secret("ab")
    assert redact("tab ab") == "tab ab"


def test_quoted_fragment_of_a_registered_secret_is_masked() -> None:
    register_secret("host=db password=my secret dbname=app")
    message = 'missing "=" after "secret" in connection info string'
    assert redact(message) == 'missing "=" after "***" in connection info string'


def test_embedded_url_password_is_registered_without_the_url() -> None:
    register_embedded_secrets(f"https://monitor:{SECRET}@jobs.example/api")
    assert redact(f"server said {SECRET}") == f"server said {MASK}"
    assert redact("jobs.example") == "jobs.example"


def test_clear_secrets_forgets_registrations() -> None:
    register_secret(SECRET)
    clear_secrets()
    assert redact(SECRET) == SECRET


@pytest.mark.parametrize(
    "dsn",
    [
        "host=db.example password=my secret dbname=app",
        "postgresql://monitor:pa ss@w0rd@db.example/app",
        "postgresql://monitor:pa%zzss@db.example/app",
    ],
)
def test_libpq_errors_never_echo_the_dsn(dsn: str, capsys: pytest.CaptureFixture[str]) -> None:
    """libpq quotes the token it rejected, which can be part of the password."""
    pytest.importorskip("psycopg")
    assert CheckPostgresReplicationLag().run(["--dsn", dsn, "-t", "2"]) == Status.UNKNOWN.value
    out = capsys.readouterr().out
    for fragment in ("secret", "pa ss", "w0rd", "pa%zzss"):
        if fragment in dsn:
            assert fragment not in out, out


def test_registered_secrets_are_masked_everywhere(capsys: pytest.CaptureFixture[str]) -> None:
    """Status line, long output, JSON and log records all mask a registered value."""
    register_secret(SECRET)
    configure_logging(0)
    logging.getLogger("test").warning("value %s", SECRET)
    result = CheckResult(Status.CRITICAL, f"got {SECRET}", details=f"body {SECRET}")
    assert SECRET not in str(result)
    assert SECRET not in result.to_json()
    assert SECRET not in capsys.readouterr().err


def test_api_key_echoed_by_a_server_is_masked(capsys: pytest.CaptureFixture[str]) -> None:
    """A credential in a custom header has no recognizable name; registration masks it."""
    backend = FakeHttpBackend()
    backend.reply(httpx.Response(200, json={"jobs": [{"name": f"echo {SECRET}", "status": "x"}]}))
    with serve_http(backend):
        check_jobs.CheckJobs().run(
            ["--url", "https://jobs.example/api", "--api-key", SECRET, "--api-key-header", "X-K"]
        )
    assert backend.requests[0].headers["X-K"] == SECRET
    assert SECRET not in capsys.readouterr().out


def test_http_settings_register_their_credentials() -> None:
    http.HttpSettings(bearer_token=SECRET)
    assert redact(f"token was {SECRET}") == f"token was {MASK}"


def test_url_option_password_is_masked_when_echoed(capsys: pytest.CaptureFixture[str]) -> None:
    body = {"status": "error", "errorType": "bad_data", "error": f"auth {SECRET} rejected"}
    with serve_http(lambda request: httpx.Response(200, json=body)):
        code = CheckPrometheusQuery().run(
            ["--server", f"https://monitor:{SECRET}@prom.example", "--query", "up"]
        )
    out = capsys.readouterr().out
    assert code == Status.UNKNOWN.value
    assert out.startswith("UNKNOWN - Prometheus error: bad_data: auth *** rejected")


def test_prometheus_error_does_not_dump_the_body(capsys: pytest.CaptureFixture[str]) -> None:
    body = {"status": "error", "errorType": "timeout", "error": "query timed out", "data": "x" * 50}
    with serve_http(lambda request: httpx.Response(200, json=body)):
        CheckPrometheusQuery().run(["--server", "https://prom.example", "--query", "up"])
    assert capsys.readouterr().out == "UNKNOWN - Prometheus error: timeout: query timed out\n"
