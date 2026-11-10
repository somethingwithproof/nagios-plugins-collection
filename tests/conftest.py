# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Pytest configuration for nagios-plugins-collection tests."""

from collections.abc import Iterator

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest

from tests.fakes import FakeHttpBackend, offline_http, serve_http


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


@pytest.fixture(autouse=True)
def _no_remote_http() -> Iterator[None]:
    """Fail any HTTP request to a non-loopback host that a test did not fake."""
    with offline_http():
        yield


@pytest.fixture
def http_backend() -> Iterator[FakeHttpBackend]:
    """Route all httpx traffic, sync and async, to a :class:`FakeHttpBackend`."""
    backend = FakeHttpBackend()
    with serve_http(backend):
        yield backend
