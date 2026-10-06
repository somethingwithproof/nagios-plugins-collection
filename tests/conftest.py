# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Pytest configuration for nagios-plugins-collection tests."""

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest


def pytest_addoption(parser: Parser) -> None:
    """Add command-line options to pytest."""
    parser.addoption(
        "--nagios-version",
        action="store",
        default="4.4.10",
        help="Nagios version to test against",
    )


@pytest.fixture
def nagios_version(request: FixtureRequest) -> str:
    """Return the Nagios version to test against."""
    cfg: Config = request.config
    return str(cfg.getoption("--nagios-version"))
