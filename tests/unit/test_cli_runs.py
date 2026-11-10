# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Run installed commands end to end against fake backends."""

import datetime as dt
import runpy
import warnings
from importlib import import_module
from importlib.metadata import EntryPoint, distribution
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from nagios_plugins.utils import CommandResult
from tests.fakes import serve_http

ENTRY_POINTS = list(distribution("nagios-plugins-collection").entry_points)

#: One healthy answer for every JSON health API the HTTP commands read.
HEALTHY = {
    "status": "ok",
    "alive": True,
    "mongrations_current": True,
    "search_reachable": True,
    "site_api_reachable": True,
    "subcomponents": [],
    "components": [],
}

HTTP_COMMANDS = {
    "check_component_status": ["--url", "https://status.example", "--components", "db"],
    "check_hadoop": ["--url", "https://hadoop.example/status"],
    "check_jobs": ["--url", "https://jobs.example/api"],
    "check_monghealth": ["--host", "mongo.example", "--ssl", "--mode", "2"],
    "check_mongodb_health": ["--url", "https://mongo.example/health", "--mode", "2"],
    "check_website_status": ["--url", "https://www.example/"],
}


def _healthy(request: httpx.Request) -> httpx.Response:
    body = {**HEALTHY, "updated": dt.datetime.now(dt.UTC).isoformat()}
    return httpx.Response(200, json=body)


def _main(command: str, args: list[str]) -> int:
    main = import_module(f"nagios_plugins.plugins.{command}").main
    with patch("sys.argv", [command, *args]):
        return int(main())


@pytest.mark.parametrize("command", HTTP_COMMANDS)
def test_http_command_reports_a_healthy_backend(
    command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with serve_http(_healthy):
        assert _main(command, HTTP_COMMANDS[command]) == 0
    assert capsys.readouterr().out.startswith("OK - ")


def test_dig_reports_the_answer(capsys: pytest.CaptureFixture[str]) -> None:
    answer = CommandResult(exit_code=0, stdout="192.0.2.1\n", stderr="", execution_time=0.05)
    with patch(
        "nagios_plugins.plugins.check_dig.execute_command_async",
        new=AsyncMock(return_value=answer),
    ):
        code = _main("check_dig", ["--host", "dns.example", "--query", "www.example"])
    assert code == 0
    assert capsys.readouterr().out.startswith("OK - ")


@pytest.mark.parametrize(
    "mounts,expected",
    [("/dev/root on / type ext4 (rw,relatime)", 0), ("/dev/data on /data type ext4 (ro)", 1)],
)
def test_ro_mounts_reads_mount_output(
    mounts: str, expected: int, capsys: pytest.CaptureFixture[str]
) -> None:
    with patch(
        "nagios_plugins.plugins.check_ro_mounts.execute_command", return_value=(0, mounts, "")
    ):
        assert _main("check_ro_mounts", ["--exclude", "/boot, /tmp"]) == expected
    assert capsys.readouterr().out.startswith(("OK - ", "WARNING - ")[expected])


@pytest.mark.parametrize("entry_point", ENTRY_POINTS, ids=lambda entry: entry.name)
def test_module_runs_as_a_script(entry_point: EntryPoint) -> None:
    """``python -m nagios_plugins.plugins.NAME`` behaves like the installed command."""
    with patch("sys.argv", [entry_point.name, "--help"]), warnings.catch_warnings():
        # The module is already imported by other tests; running it again is the point.
        warnings.simplefilter("ignore", RuntimeWarning)
        with pytest.raises(SystemExit) as exited:
            runpy.run_module(entry_point.module, run_name="__main__")
    assert exited.value.code == 0
