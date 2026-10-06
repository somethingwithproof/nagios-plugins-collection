# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for DNS health plugin."""

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_dns_health import CheckDnsHealth


def test_unknown_when_dns_missing() -> None:
    plugin = CheckDnsHealth()
    # Force UNKNOWN path by simulating dnspython not installed
    from nagios_plugins.plugins import check_dns_health as mod

    mod._DNS_OK = False  # type: ignore[attr-defined]
    code = plugin.run(["--name", "example.com"])  # minimal args
    assert code == Status.UNKNOWN.value
