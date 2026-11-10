# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Every advertised console command must follow the Nagios CLI contract."""

import argparse
import importlib
import inspect
import logging
from importlib.metadata import EntryPoint, distribution
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, NagiosPlugin, nagios_range

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


def test_unhandled_exception_in_async_check_is_unknown(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Exceptions escaping an async check report UNKNOWN instead of a traceback exit 1."""

    class Broken(AsyncNagiosPlugin):
        async def check_async(self, args: argparse.Namespace) -> CheckResult:
            raise RuntimeError("boom")

    code = Broken().run([])
    captured = capsys.readouterr()
    assert code == 3
    assert captured.out == "UNKNOWN - Unhandled exception: boom\n"
    assert "Traceback" in captured.err


@pytest.mark.parametrize("entry_point", ENTRY_POINTS, ids=lambda entry: entry.name)
def test_every_command_runs_on_the_plugin_base(entry_point: EntryPoint) -> None:
    """One framework: each command is a NagiosPlugin whose parser is named after it."""
    module = importlib.import_module(entry_point.module)
    plugins = [
        value
        for value in vars(module).values()
        if inspect.isclass(value)
        and issubclass(value, NagiosPlugin)
        and value.__module__ == module.__name__
    ]
    assert len(plugins) == 1, plugins
    assert plugins[0].command_name() == entry_point.name
    assert plugins[0]().parser.prog == entry_point.name
    assert not hasattr(module, "parse_args")


@pytest.mark.parametrize(
    "command,timeout",
    [
        ("check_component_status", 10),
        ("check_mongodb_health", 10),
        ("check_monghealth", 5),
        ("check_hadoop", 30),
        ("check_jobs", 30),
        ("check_dig", 30),
        ("check_ro_mounts", 30),
    ],
)
def test_migrated_commands_keep_their_timeout_defaults(command: str, timeout: int) -> None:
    module = importlib.import_module(f"nagios_plugins.plugins.{command}")
    (plugin,) = (
        value
        for value in vars(module).values()
        if inspect.isclass(value)
        and issubclass(value, NagiosPlugin)
        and value.__module__ == module.__name__
    )
    assert plugin().parser.get_default("timeout") == timeout


@pytest.mark.parametrize(
    "verbosity,level",
    [(0, logging.WARNING), (1, logging.INFO), (2, logging.DEBUG), (5, logging.DEBUG)],
)
def test_verbosity_selects_log_level(verbosity: int, level: int) -> None:
    from nagios_plugins.base import configure_logging

    configure_logging(verbosity)
    assert logging.getLogger().level == level


def _plugin_class(entry_point: EntryPoint) -> type[NagiosPlugin]:
    module = importlib.import_module(entry_point.module)
    (plugin,) = (
        value
        for value in vars(module).values()
        if inspect.isclass(value)
        and issubclass(value, NagiosPlugin)
        and value.__module__ == module.__name__
    )
    return plugin


@pytest.mark.parametrize("value", ["5:1", "abc", "1..5"])
@pytest.mark.parametrize("entry_point", ENTRY_POINTS, ids=lambda entry: entry.name)
def test_malformed_ranges_are_usage_errors(
    entry_point: EntryPoint, value: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """A typo in -w must exit UNKNOWN before the check contacts anything."""
    plugin = _plugin_class(entry_point)()
    warning = [a for a in plugin.parser._actions if "--warning" in a.option_strings]
    if not warning or warning[0].type is not nagios_range:
        pytest.skip("-w is not a Nagios range for this command")
    with pytest.raises(SystemExit) as exited:
        plugin.parse_args(["-w", value])
    assert exited.value.code == 3
    assert "invalid Nagios range" in capsys.readouterr().out
