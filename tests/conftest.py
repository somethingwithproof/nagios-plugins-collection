"""Pytest configuration for nagios-plugins-collection tests."""

import pytest


def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--nagios-version",
        action="store",
        default="4.4.10",
        help="Nagios version to test against",
    )


@pytest.fixture
def nagios_version(request):
    """Return the Nagios version to test against."""
    return request.config.getoption("--nagios-version")
