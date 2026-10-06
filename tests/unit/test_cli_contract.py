"""Every advertised console command must load and provide its CLI help."""

from importlib.metadata import EntryPoint, distribution
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "entry_point",
    list(distribution("nagios-plugins-collection").entry_points),
    ids=lambda entry: entry.name,
)
def test_installed_command_help(entry_point: EntryPoint) -> None:
    command = entry_point.load()
    assert callable(command)
    with patch("sys.argv", [entry_point.name, "--help"]), pytest.raises(SystemExit) as exited:
        command()
    assert exited.value.code == 0
