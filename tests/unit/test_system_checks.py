# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Verify filesystem monitoring and remote DNS status contracts."""

import asyncio
import shlex
import sys
from pathlib import Path
from unittest.mock import AsyncMock, mock_open, patch

import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_dig import SSHDNSChecker, execute_command_async
from nagios_plugins.plugins.check_ro_mounts import MountStatusChecker
from nagios_plugins.utils import CommandResult, get_directory_size, get_system_info


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "output,expected,count",
    [
        ("/dev/root on / type ext4 (rw,relatime)", Status.OK, 0),
        ("/dev/root on / type ext4 (ro,relatime)", Status.CRITICAL, 1),
        ("/dev/data on /data type ext4 (ro,relatime)", Status.WARNING, 1),
        ("proc on /proc type proc (ro,relatime)", Status.OK, 0),
        ("unrecognized output", Status.OK, 0),
    ],
)
async def test_mount_status(output: str, expected: Status, count: int) -> None:
    with patch(
        "nagios_plugins.plugins.check_ro_mounts.execute_command", return_value=(0, output, "")
    ):
        result = await MountStatusChecker().check_mounts()
    assert result.status == expected
    assert result.metrics["ro_mounts_count"] == count


@pytest.mark.asyncio
async def test_mount_command_failure_is_unknown() -> None:
    with patch(
        "nagios_plugins.plugins.check_ro_mounts.execute_command",
        return_value=(255, "", "connection failed"),
    ):
        result = await MountStatusChecker(host="monitor.example").check_mounts()
    assert result.status == Status.UNKNOWN


@pytest.mark.asyncio
async def test_mount_exception_is_unknown() -> None:
    with patch(
        "nagios_plugins.plugins.check_ro_mounts.execute_command", side_effect=OSError("unavailable")
    ):
        result = await MountStatusChecker().check_mounts()
    assert result.status == Status.UNKNOWN


def test_mount_remote_arguments() -> None:
    command = MountStatusChecker(
        host="monitor.example", ssh_user="monitor", ssh_port=2222
    )._build_command()
    assert command == ["ssh", "-p", "2222", "-l", "monitor", "monitor.example", "mount -l"]


def test_remote_dns_preserves_argument_boundaries() -> None:
    checker = SSHDNSChecker(
        "monitor.example", "example.com", dig_arguments="+time=3 +tries=1", ssh_user="monitor"
    )
    remote = checker._build_dig_command()
    assert shlex.split(remote) == [
        "dig",
        "-p",
        "53",
        "-t",
        "A",
        "+short",
        "example.com",
        "+time=3",
        "+tries=1",
    ]
    assert checker._build_ssh_command(remote)[-2:] == ["monitor.example", remote]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "duration,expected", [(0.05, Status.OK), (1.5, Status.WARNING), (3.0, Status.CRITICAL)]
)
async def test_remote_dns_latency(duration: float, expected: Status) -> None:
    result = CommandResult(execution_time=0.05, exit_code=0, stdout="192.0.2.1", stderr="")
    checker = SSHDNSChecker(
        "monitor.example",
        "example.com",
        expected_address="192.0.2.1",
        warning_threshold=1.0,
        critical_threshold=2.0,
    )
    with (
        patch(
            "nagios_plugins.plugins.check_dig.execute_command_async",
            new=AsyncMock(return_value=result),
        ),
        patch("nagios_plugins.plugins.check_dig.time") as timer,
    ):
        timer.time.side_effect = [0.0, duration]
        checked = await checker.check_dns()
    assert checked.status == expected


@pytest.mark.asyncio
async def test_remote_dns_missing_expected_answer() -> None:
    result = CommandResult(execution_time=0.05, exit_code=0, stdout="192.0.2.2", stderr="")
    with patch(
        "nagios_plugins.plugins.check_dig.execute_command_async", new=AsyncMock(return_value=result)
    ):
        checked = await SSHDNSChecker(
            "monitor.example", "example.com", expected_address="192.0.2.1"
        ).check_dns()
    assert checked.status == Status.CRITICAL


@pytest.mark.asyncio
async def test_remote_dns_retries_failed_command() -> None:
    result = CommandResult(
        execution_time=0.05, exit_code=1, stdout="", stderr="connection unavailable"
    )
    with (
        patch(
            "nagios_plugins.plugins.check_dig.execute_command_async",
            new=AsyncMock(return_value=result),
        ) as run,
        patch("nagios_plugins.plugins.check_dig.asyncio.sleep", new=AsyncMock()),
    ):
        checked = await SSHDNSChecker("monitor.example", "example.com", retries=2).check_dns()
    assert checked.status == Status.CRITICAL
    assert run.call_count == 2


@pytest.mark.asyncio
async def test_async_command_output_and_exit_status() -> None:
    result = await execute_command_async(
        [sys.executable, "-c", "print('health'); raise SystemExit(7)"]
    )
    assert result.exit_code == 7
    assert result.stdout.strip() == "health"


@pytest.mark.asyncio
async def test_async_command_timeout_reaps_child() -> None:
    context = asyncio.timeout(0.1)
    with pytest.raises(TimeoutError):
        async with context:
            await execute_command_async([sys.executable, "-c", "import time; time.sleep(2)"])


@pytest.mark.asyncio
async def test_async_shell_execution_is_disabled() -> None:
    with pytest.raises(ValueError, match="shell=True is disallowed"):
        await execute_command_async(["echo", "health"], shell=True)


def test_command_result_formats_bounded_diagnostics() -> None:
    result = CommandResult(exit_code=0, stdout="a" * 600, stderr="b" * 600, execution_time=0.05)
    output = str(result)
    assert result.success is True
    assert "a" * 500 in output
    assert "a" * 501 not in output
    assert "b" * 500 in output
    assert "b" * 501 not in output
    assert "truncated" in output


def test_directory_size_includes_nested_files(tmp_path: Path) -> None:
    (tmp_path / "root.bin").write_bytes(b"a" * 10)
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "child.bin").write_bytes(b"b" * 20)
    assert get_directory_size(tmp_path) == 30
    with pytest.raises(FileNotFoundError):
        get_directory_size(tmp_path / "missing")
    with pytest.raises(NotADirectoryError):
        get_directory_size(tmp_path / "root.bin")


def test_system_memory_information() -> None:
    with (
        patch("platform.system", return_value="Linux"),
        patch(
            "nagios_plugins.utils.open",
            mock_open(read_data="MemTotal: 1024 kB\nMemFree: 512 kB\n"),
            create=True,
        ),
    ):
        info = get_system_info()
    assert info["total_memory_kb"] == 1024
    assert info["free_memory_kb"] == 512
    assert info["python_version"]
