"""Tests for TLS expiry plugin."""

from unittest.mock import patch

import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_tls_expiry import CheckTlsExpiry
from nagios_plugins.services.tls import TlsCertInfo


@pytest.fixture
def plugin() -> CheckTlsExpiry:
    return CheckTlsExpiry()


def test_ok_when_above_thresholds(plugin: CheckTlsExpiry) -> None:
    cert = TlsCertInfo(not_after=None, issuer="i", subject="s", san_count=3)  # type: ignore[arg-type]
    with (
        patch("nagios_plugins.plugins.check_tls_expiry.fetch_server_cert", return_value=cert),
        patch("nagios_plugins.plugins.check_tls_expiry.days_remaining", return_value=30),
    ):
        exit_code = plugin.run(["--host", "example.com", "--warning", "21", "--critical", "7"])
        assert exit_code == Status.OK.value


def test_warn_when_below_warning(plugin: CheckTlsExpiry) -> None:
    cert = TlsCertInfo(not_after=None, issuer="i", subject="s", san_count=1)  # type: ignore[arg-type]
    with (
        patch("nagios_plugins.plugins.check_tls_expiry.fetch_server_cert", return_value=cert),
        patch("nagios_plugins.plugins.check_tls_expiry.days_remaining", return_value=14),
    ):
        exit_code = plugin.run(["--host", "example.com", "--warning", "21", "--critical", "7"])
        assert exit_code == Status.WARNING.value


def test_crit_when_below_critical(plugin: CheckTlsExpiry) -> None:
    cert = TlsCertInfo(not_after=None, issuer="i", subject="s", san_count=1)  # type: ignore[arg-type]
    with (
        patch("nagios_plugins.plugins.check_tls_expiry.fetch_server_cert", return_value=cert),
        patch("nagios_plugins.plugins.check_tls_expiry.days_remaining", return_value=3),
    ):
        exit_code = plugin.run(["--host", "example.com", "--warning", "21", "--critical", "7"])
        assert exit_code == Status.CRITICAL.value
