# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""The run deadline always ends a plugin with one UNKNOWN line and exit 3."""

import argparse
import asyncio
import json
import os
import signal
import socket
import subprocess
import sys
import textwrap
import threading
import time
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from nagios_plugins import deadline
from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, NagiosPlugin, Status
from nagios_plugins.deadline import Deadline, remaining_time
from nagios_plugins.plugins.check_dig import CheckDig, execute_command_async
from nagios_plugins.plugins.check_tls_expiry import CheckTlsExpiry
from nagios_plugins.utils import CommandResult, execute_command

TIMED_OUT = "UNKNOWN - Plugin timed out after 1 seconds\n"
posix_only = pytest.mark.skipif(not hasattr(signal, "setitimer"), reason="needs SIGALRM")


@pytest.fixture(autouse=True)
def short_margin(monkeypatch: pytest.MonkeyPatch) -> None:
    """End runs 0.2s after --timeout; keep the in-process watchdog out of the way."""
    monkeypatch.setattr(deadline, "DEADLINE_MARGIN", 0.2)
    monkeypatch.setattr(deadline, "WATCHDOG_GRACE", 30.0)


class Sleeper(NagiosPlugin):
    """Block the main thread in a sleep."""

    def check(self, args: argparse.Namespace) -> CheckResult:
        time.sleep(30)
        return CheckResult(Status.OK, "not reached")


def _child_pid_file(tmp_path: Path) -> tuple[list[str], Path]:
    pid_file = tmp_path / "child.pid"
    code = f"import os, time; open({str(pid_file)!r}, 'w').write(str(os.getpid())); time.sleep(30)"
    return [sys.executable, "-c", code], pid_file


def _assert_killed(pid_file: Path) -> None:
    pid = int(pid_file.read_text())
    try:
        reaped, status = os.waitpid(pid, 0)
    except ChildProcessError:  # already reaped by subprocess's own cleanup
        return
    assert reaped == pid
    assert os.WIFSIGNALED(status)


@posix_only
def test_sync_check_is_interrupted(capsys: pytest.CaptureFixture[str]) -> None:
    started = time.monotonic()
    assert Sleeper().run(["--timeout", "1"]) == 3
    assert time.monotonic() - started < 2
    assert capsys.readouterr().out == TIMED_OUT


@posix_only
def test_json_timeout_result(capsys: pytest.CaptureFixture[str]) -> None:
    assert Sleeper().run(["--timeout", "1", "--json"]) == 3
    assert json.loads(capsys.readouterr().out)["status"] == "UNKNOWN"


@posix_only
def test_dns_resolution_is_bounded(capsys: pytest.CaptureFixture[str]) -> None:
    """getaddrinfo ignores socket timeouts; only the run deadline bounds it."""
    with patch("socket.getaddrinfo", side_effect=lambda *a, **k: time.sleep(30)):
        code = CheckTlsExpiry().run(["--host", "slow-dns.example", "--timeout", "1"])
    assert code == 3
    assert capsys.readouterr().out == TIMED_OUT


@posix_only
def test_tcp_connect_is_bounded(capsys: pytest.CaptureFixture[str]) -> None:
    resolved = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.1", 443))]
    with (
        patch("socket.getaddrinfo", return_value=resolved),
        patch.object(socket.socket, "connect", side_effect=lambda *a: time.sleep(30)),
    ):
        code = CheckTlsExpiry().run(["--host", "blackhole.example", "--timeout", "1"])
    assert code == 3
    assert capsys.readouterr().out == TIMED_OUT


@posix_only
def test_subprocess_wait_is_bounded_and_child_killed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    command, pid_file = _child_pid_file(tmp_path)

    class Waits(NagiosPlugin):
        def check(self, args: argparse.Namespace) -> CheckResult:
            execute_command(command, timeout=60)
            return CheckResult(Status.OK, "not reached")

    assert Waits().run(["--timeout", "1"]) == 3
    assert capsys.readouterr().out == TIMED_OUT
    _assert_killed(pid_file)


def test_async_subprocess_is_cancelled_and_child_killed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    command, pid_file = _child_pid_file(tmp_path)

    class AwaitsChild(AsyncNagiosPlugin):
        async def check_async(self, args: argparse.Namespace) -> CheckResult:
            await execute_command_async(command)
            return CheckResult(Status.OK, "not reached")

    assert AwaitsChild().run(["--timeout", "1"]) == 3
    assert capsys.readouterr().out == TIMED_OUT
    _assert_killed(pid_file)


def test_gather_with_return_exceptions_cannot_swallow_the_deadline(
    capsys: pytest.CaptureFixture[str],
) -> None:
    class Gathers(AsyncNagiosPlugin):
        async def check_async(self, args: argparse.Namespace) -> CheckResult:
            await asyncio.gather(asyncio.sleep(30), asyncio.sleep(30), return_exceptions=True)
            return CheckResult(Status.OK, "not reached")

    assert Gathers().run(["--timeout", "1"]) == 3
    assert capsys.readouterr().out == TIMED_OUT


def test_plugin_timeouts_report_before_the_deadline(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """check_dig's own per-attempt timeout fits inside --timeout and stays CRITICAL."""
    command, pid_file = _child_pid_file(tmp_path)
    # By name: test_cli_contract reloads plugin modules, replacing their classes.
    with patch(
        "nagios_plugins.plugins.check_dig.SSHDNSChecker._build_ssh_command",
        return_value=command,
    ):
        code = CheckDig().run(["--host", "h", "--query", "q", "--timeout", "1", "--retries", "3"])
    assert code == 2
    assert capsys.readouterr().out.startswith("CRITICAL - DNS query failed after 1 attempts")
    _assert_killed(pid_file)


def test_retries_stop_when_the_timeout_is_spent(capsys: pytest.CaptureFixture[str]) -> None:
    failed = CommandResult(exit_code=255, stdout="", stderr="refused", execution_time=0.0)
    started = time.monotonic()
    with patch(
        "nagios_plugins.plugins.check_dig.execute_command_async",
        new=AsyncMock(return_value=failed),
    ) as run:
        code = CheckDig().run(["--host", "h", "--query", "q", "--timeout", "2", "--retries", "9"])
    assert code == 2
    # Attempts at 0s and 1s; the second 1s pause spends the budget.
    assert run.call_count == 2
    assert time.monotonic() - started < 2.5
    assert capsys.readouterr().out.startswith("CRITICAL - DNS query failed after 2 attempts")


def test_deadline_is_disarmed_after_a_run(capsys: pytest.CaptureFixture[str]) -> None:
    class Fine(NagiosPlugin):
        def check(self, args: argparse.Namespace) -> CheckResult:
            assert remaining_time() is not None
            return CheckResult(Status.OK, "fine")

    before = signal.getsignal(signal.SIGALRM) if hasattr(signal, "SIGALRM") else None
    assert Fine().run([]) == 0
    assert remaining_time() is None
    if hasattr(signal, "setitimer"):
        assert signal.getitimer(signal.ITIMER_REAL) == (0.0, 0.0)
        assert signal.getsignal(signal.SIGALRM) == before
    assert not [t for t in threading.enumerate() if isinstance(t, threading.Timer)]
    assert capsys.readouterr().out == "OK - fine\n"


def test_remaining_time_tracks_the_timeout() -> None:
    assert remaining_time() is None
    with Deadline(5, "UNKNOWN - x"):
        left = remaining_time()
        assert left is not None and 4 < left <= 5
    assert remaining_time() is None


@pytest.mark.parametrize("value", ["0", "-5", "soon"])
def test_timeout_must_be_a_positive_whole_number(
    value: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exited:
        Sleeper().parse_args(["--timeout", value])
    assert exited.value.code == 3
    assert capsys.readouterr().out.startswith("UNKNOWN - ")


def _run_script(body: str, *args: str) -> tuple[subprocess.CompletedProcess[str], float]:
    """Run plugin code in a child interpreter, where the watchdog may exit the process."""
    script = textwrap.dedent(
        """
        import argparse, asyncio, signal, sys, time
        from nagios_plugins import deadline
        from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, NagiosPlugin, Status
        deadline.DEADLINE_MARGIN = 0.2
        deadline.WATCHDOG_GRACE = 0.5
        """
    ) + textwrap.dedent(body)
    started = time.monotonic()
    completed = subprocess.run(
        [sys.executable, "-c", script, *args],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    return completed, time.monotonic() - started


@posix_only
def test_watchdog_exits_when_the_main_thread_cannot_be_interrupted() -> None:
    """SIGALRM blocked in the main thread stands in for a blocking C call."""
    completed, elapsed = _run_script(
        """
        class Stuck(NagiosPlugin):
            def check(self, args):
                signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGALRM})
                time.sleep(30)
                return CheckResult(Status.OK, "not reached")
        sys.exit(Stuck().run(sys.argv[1:]))
        """,
        "--timeout",
        "1",
    )
    assert completed.returncode == 3
    assert completed.stdout == TIMED_OUT
    assert elapsed < 5


def test_watchdog_is_the_fallback_without_sigalrm() -> None:
    """Without an alarm (Windows, non-main thread) the watchdog ends a blocked event loop."""
    completed, elapsed = _run_script(
        """
        deadline.Deadline._alarm_available = staticmethod(lambda: False)
        class BlocksLoop(AsyncNagiosPlugin):
            async def check_async(self, args):
                time.sleep(30)
                return CheckResult(Status.OK, "not reached")
        sys.exit(BlocksLoop().run(sys.argv[1:]))
        """,
        "--timeout",
        "1",
        "--json",
    )
    assert completed.returncode == 3
    assert json.loads(completed.stdout)["message"] == "Plugin timed out after 1 seconds"
    assert elapsed < 5
