# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Every advertised console command must follow the Nagios CLI contract."""

import argparse
import importlib
import logging
from importlib.metadata import EntryPoint, distribution
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins.base import CheckResult, run_async_check

ENTRY_POINTS = list(distribution("nagios-plugins-collection").entry_points)


@pytest.mark.parametrize("entry_point", ENTRY_POINTS, ids=lambda entry: entry.name)
def test_installed_command_help(entry_point: EntryPoint) -> None:
    command = entry_point.load()
    assert callable(command)
    with patch("sys.argv", [entry_point.name, "--help"]), pytest.raises(SystemExit) as exited:
        command()
    assert exited.value.code == 0


@pytest.mark.parametrize("entry_point", ENTRY_POINTS, ids=lambda entry: entry.name)
def test_usage_error_exits_unknown(
    entry_point: EntryPoint, capsys: pytest.CaptureFixture[str]
) -> None:
    """argparse exits 2, which Nagios reads as CRITICAL; usage errors must be UNKNOWN."""
    command = entry_point.load()
    with (
        patch("sys.argv", [entry_point.name, "--no-such-option"]),
        pytest.raises(SystemExit) as exited,
    ):
        command()
    assert exited.value.code == 3
    captured = capsys.readouterr()
    assert captured.out.startswith(f"UNKNOWN - {entry_point.name}: ")
    assert len(captured.out.splitlines()) == 1
    assert captured.err.startswith("usage: ")


@pytest.mark.parametrize("entry_point", ENTRY_POINTS, ids=lambda entry: entry.name)
def test_import_does_not_configure_logging(entry_point: EntryPoint) -> None:
    """Configuring logging at import would print records before the status line."""
    root = logging.getLogger()
    before = list(root.handlers)
    importlib.reload(importlib.import_module(entry_point.module))
    assert root.handlers == before


def test_logs_go_to_stderr_and_status_line_is_first_on_stdout(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A failing legacy check logs its exception without touching stdout."""
    from nagios_plugins.plugins import check_jobs

    with (
        patch("sys.argv", ["check_jobs", "--url", "http://jobs.invalid/status"]),
        patch("httpx.AsyncClient.get", side_effect=httpx.ConnectError("refused")),
    ):
        code = check_jobs.main()
    captured = capsys.readouterr()
    assert code == 3
    assert captured.out.splitlines()[0].startswith("UNKNOWN - Failed to connect to jobs API")
    assert len(captured.out.splitlines()) == 1
    assert "HTTP request failed" in captured.err


def test_unhandled_exception_in_standalone_check_is_unknown(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Exceptions escaping a legacy check report UNKNOWN instead of a traceback exit 1."""

    async def broken(_: argparse.Namespace) -> CheckResult:
        raise RuntimeError("boom")

    code = run_async_check(argparse.Namespace(verbose=0, json=False), broken)
    captured = capsys.readouterr()
    assert code == 3
    assert captured.out == "UNKNOWN - Unhandled exception: boom\n"
    assert "Traceback" in captured.err
