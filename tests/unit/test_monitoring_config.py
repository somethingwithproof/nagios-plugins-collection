# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""The generated Icinga 2, Nagios and man page definitions match the plugin parsers."""

from __future__ import annotations

import argparse
import importlib.util
import re
import shlex
import sys
from pathlib import Path
from types import ModuleType

import pytest

from nagios_plugins.base import NagiosArgumentParser

ROOT = Path(__file__).resolve().parents[2]


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "generate_monitoring_config", ROOT / "scripts/generate_monitoring_config.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve their module while executing
    spec.loader.exec_module(module)
    return module


generator = _load()
COMMANDS = {command.name: command for command in generator.load_commands()}


def _icinga_blocks() -> dict[str, str]:
    text = generator.ICINGA.read_text()
    return dict(re.findall(r'object CheckCommand "(\w+)" \{\n(.*?)\n\}\n', text, re.S))


def _nagios_lines() -> dict[str, str]:
    text = generator.NAGIOS.read_text()
    return dict(re.findall(r"command_name\s+(\S+)\n\s+command_line\s+(.+)", text))


def _parser(name: str) -> NagiosArgumentParser:
    parser: NagiosArgumentParser = generator._plugin(f"nagios_plugins.plugins.{name}")().parser
    return parser


def _action(parser: argparse.ArgumentParser, flag: str) -> argparse.Action:
    return next(action for action in parser._actions if flag in action.option_strings)


def test_committed_files_are_up_to_date() -> None:
    """CI fails when a parser changes without regenerating contrib/."""
    assert generator.main(["--check"]) == 0


def test_every_installed_command_is_generated() -> None:
    assert set(_icinga_blocks()) == set(COMMANDS)
    assert set(_nagios_lines()) == set(COMMANDS)
    assert {page.stem for page in generator.MAN.glob("*.1")} == set(COMMANDS)


@pytest.mark.parametrize("name", sorted(COMMANDS))
def test_nagios_command_line_parses(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """Filling the $ARGn$ macros, with secrets in the environment, satisfies the parser."""
    parser = _parser(name)
    for secret in parser.secret_options:
        if secret.required:
            monkeypatch.setenv(secret.env, "from-environment")
    line = _nagios_lines()[name]
    args = shlex.split(line)[1:]
    assert args[-1].startswith("$ARG") and args[-1].endswith("$")
    args = args[:-1]  # the free-form trailing $ARGn$ may be empty
    filled, mapped = [], set()
    for flag, macro in zip(args[::2], args[1::2], strict=True):
        assert re.fullmatch(r"'?\$ARG\d+\$'?", macro), line
        action = _action(parser, flag)
        mapped.add(action.dest)
        filled += [flag, str(next(iter(action.choices))) if action.choices else "1"]
    required = {action.dest for action in parser._actions if action.required}
    assert mapped == required
    namespace, _ = parser.parse_known_args(filled)
    assert all(getattr(namespace, dest) is not None for dest in required)


@pytest.mark.parametrize("name", sorted(COMMANDS))
def test_icinga_arguments_are_real_options(name: str) -> None:
    parser = _parser(name)
    block = _icinga_blocks()[name]
    flags = {flag for action in parser._actions for flag in action.option_strings}
    declared = re.findall(r'^    "(--?[\w-]+)" = \{', block, re.M)
    assert declared and set(declared) <= flags
    required = {
        max(action.option_strings, key=len)
        for action in parser._actions
        if action.required and action.option_strings
    }
    marked = set(
        re.findall(r'^    "(--?[\w-]+)" = \{\n(?:      .*\n)*?      required = true', block, re.M)
    )
    assert marked == required


@pytest.mark.parametrize("name", sorted(COMMANDS))
def test_secrets_stay_off_the_command_line(name: str) -> None:
    """Secret values go through the environment; only their -file options are arguments."""
    parser = _parser(name)
    block = _icinga_blocks()[name]
    line = _nagios_lines()[name]
    for secret in parser.secret_options:
        assert f'"{secret.flag}" =' not in block
        assert f'{secret.env} = "${name}_{secret.dest}$"' in block
        assert f'"{secret.file_flag}" =' in block
        assert f"{secret.flag} " not in line


def test_man_page_documents_options_environment_and_exit_codes() -> None:
    page = (generator.MAN / "check_oauth2_token.1").read_text()
    assert page.startswith('.\\" SPDX-FileCopyrightText:')
    assert ".TH CHECK\\_OAUTH2\\_TOKEN 1" in page
    assert "\\fB\\-\\-token\\-url\\fR \\fITOKEN_URL\\fR" in page
    assert "\\fBCHECK_OAUTH2_CLIENT_SECRET_FILE\\fR" in page
    assert ".SH EXIT STATUS" in page
    assert "\\fB\\-\\-client\\-secret\\fR \\fI" not in page


def test_roff_escaping() -> None:
    assert generator._roff(".starts with a dot") == "\\&.starts with a dot"
    assert generator._roff("a-b\\c") == "a\\-b\\ec"


def test_icinga_strings_escape_quotes_and_macros() -> None:
    assert generator._icinga_string('say "$5" \\') == '"say \\"$$5\\" \\\\"'


def test_check_reports_stale_and_leftover_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(generator, "ROOT", tmp_path)
    monkeypatch.setattr(generator, "ICINGA", tmp_path / "contrib/icinga2/x.conf")
    monkeypatch.setattr(generator, "NAGIOS", tmp_path / "contrib/nagios/x.cfg")
    monkeypatch.setattr(generator, "MAN", tmp_path / "contrib/man/man1")
    monkeypatch.setattr(generator, "load_commands", lambda: [COMMANDS["check_dig"]])
    assert generator.main(["--check"]) == 1
    assert "out of date: contrib/icinga2/x.conf" in capsys.readouterr().err

    assert generator.main([]) == 0
    assert generator.main(["--check"]) == 0
    leftover = tmp_path / "contrib/man/man1/check_removed.1"
    leftover.write_text("old")
    assert generator.main(["--check"]) == 1
    assert generator.main([]) == 0
    assert not leftover.exists()
