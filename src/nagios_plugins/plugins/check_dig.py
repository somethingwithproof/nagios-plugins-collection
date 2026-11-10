#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""
DNS Query Check Plugin for Nagios.

This plugin performs DNS queries via SSH by connecting to a remote host and
executing the 'dig' command. It supports various DNS record types and
can validate responses against expected values.

Usage:
    check_dig.py --host SSH_HOST --query DOMAIN [--ssh-user USERNAME]
                [--ssh-port PORT] [--dns-port PORT] [--record-type TYPE]
                [--expected EXPECTED] [--warning SECONDS] [--critical SECONDS]
                [--timeout SECONDS] [--retries COUNT] [--json] [--verbose]

Returns:
    0 (OK): DNS query successful within time thresholds
    1 (WARNING): DNS query successful but took longer than warning threshold
    2 (CRITICAL): DNS query failed or took longer than critical threshold
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import asyncio
import logging
import shlex
import time

from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, Status, threshold_check
from nagios_plugins.deadline import remaining_time, track_child
from nagios_plugins.utils import CommandResult

logger = logging.getLogger("check_dig")

#: Seconds between attempts; bounded by what is left of --timeout.
RETRY_DELAY = 1.0


class SSHDNSChecker:
    """SSH DNS Checker using dig."""

    def __init__(
        self,
        ssh_host: str,
        query_address: str,
        ssh_user: str | None = None,
        ssh_port: int = 22,
        dns_port: int = 53,
        record_type: str = "A",
        dig_arguments: str | None = None,
        expected_address: str | None = None,
        timeout: int = 30,
        retries: int = 1,
        warning_threshold: str | float | None = None,
        critical_threshold: str | float | None = None,
    ):
        """Initialize the SSH DNS checker.

        Args:
            ssh_host: SSH host to connect to
            query_address: DNS name to query
            ssh_user: SSH username
            ssh_port: SSH port
            dns_port: DNS port
            record_type: DNS record type (A, AAAA, MX, etc.)
            dig_arguments: Additional dig command arguments
            expected_address: Expected result from the DNS query
            timeout: Command timeout in seconds
            retries: Number of attempts, bounded by the run's --timeout
            warning_threshold: Warning range for the query time in seconds
            critical_threshold: Critical range for the query time in seconds
        """
        self.ssh_host = ssh_host
        self.query_address = query_address
        self.ssh_user = ssh_user
        self.ssh_port = ssh_port
        self.dns_port = dns_port
        self.record_type = record_type
        self.dig_arguments = dig_arguments
        self.expected_address = expected_address
        self.timeout = timeout
        self.retries = retries
        self.warning_threshold = None if warning_threshold is None else str(warning_threshold)
        self.critical_threshold = None if critical_threshold is None else str(critical_threshold)

    def _build_ssh_command(self, dig_command: str) -> list[str]:
        """Build the SSH command to execute.

        Args:
            dig_command: The dig command to execute via SSH

        Returns:
            List of command arguments for SSH
        """
        if self.ssh_host.startswith("-"):
            raise ValueError("SSH host must not begin with an option prefix")
        cmd = ["ssh", "-p", str(self.ssh_port)]

        # Add SSH user if specified
        if self.ssh_user:
            cmd.extend(["-l", self.ssh_user])

        # Add host and dig command
        cmd.append(self.ssh_host)
        cmd.append(dig_command)

        return cmd

    def _build_dig_command(self) -> str:
        """Build the dig command string.

        Returns:
            Dig command string
        """
        arguments = [
            "dig",
            "-p",
            str(self.dns_port),
            "-t",
            self.record_type,
            "+short",
            self.query_address,
        ]
        if self.dig_arguments:
            arguments.extend(shlex.split(self.dig_arguments))
        return shlex.join(arguments)

    def _response_result(self, response: str, duration: float) -> CheckResult:
        """Classify DNS output and latency after a successful SSH command."""
        # dig +short exits 0 with no output for NXDOMAIN, SERVFAIL and NODATA.
        if not response:
            return CheckResult(
                Status.CRITICAL,
                f"No {self.record_type} answer for {self.query_address}",
                metrics={"duration": duration, "response_matches": 0},
            )
        # Check expected address
        if self.expected_address and self.expected_address not in response:
            return CheckResult(
                Status.CRITICAL,
                f"Expected address '{self.expected_address}' not found",
                metrics={"duration": duration, "response_matches": 0},
                details=f"Response: {response}",
            )

        # A plain number N is the range 0:N, so it alerts when the query takes longer than N.
        status = threshold_check(duration, self.warning_threshold, self.critical_threshold)
        message = f"DNS response received in {duration:.2f}s"
        if status == Status.CRITICAL:
            message = f"Query took {duration:.2f}s (critical: {self.critical_threshold}s)"
        elif status == Status.WARNING:
            message = f"Query took {duration:.2f}s (warning threshold: {self.warning_threshold}s)"

        # Create metrics
        metrics = {
            "duration": duration,
            "response_matches": (
                1 if not self.expected_address or self.expected_address in response else 0
            ),
        }

        return CheckResult(
            status,
            message,
            metrics=metrics,
            details=f"Response: {response}",
        )

    async def _query(self) -> CheckResult:
        """Run dig over SSH once and classify its answer and latency."""
        ssh_cmd = self._build_ssh_command(self._build_dig_command())
        start_time = time.time()
        result = await execute_command_async(ssh_cmd)
        duration = time.time() - start_time
        if result.exit_code != 0:
            raise RuntimeError(f"SSH command failed: {result.stderr}")
        return self._response_result(result.stdout.strip(), duration)

    async def check_dns(self) -> CheckResult:
        """Check DNS via SSH, retrying failed attempts within the run's timeout.

        Returns:
            CheckResult with the check result
        """
        attempt = 0
        last_error = None
        while attempt < self.retries:
            if attempt:
                await asyncio.sleep(_within_budget(RETRY_DELAY))
            timeout = _within_budget(self.timeout)
            if timeout <= 0:
                break
            try:
                async with asyncio.timeout(timeout):
                    return await self._query()
            except Exception as e:
                logger.exception("DNS attempt %s failed", attempt + 1)
                last_error = str(e) or type(e).__name__
            attempt += 1

        # All attempts failed or the run's timeout was spent
        return CheckResult(
            Status.CRITICAL,
            f"DNS query failed after {attempt} attempts",
            metrics={"duration": 0, "response_matches": 0},
            details=f"Last error: {last_error}",
        )


def _within_budget(seconds: float) -> float:
    """Clamp ``seconds`` to what is left of the run's --timeout (0 when spent)."""
    budget = remaining_time()
    return seconds if budget is None else min(seconds, budget)


async def execute_command_async(command: list[str], shell: bool = False) -> CommandResult:
    """Execute a command asynchronously and return the result.

    Args:
        command: The command to execute as a list of strings.
        shell: Whether to execute the command in a shell.

    Returns:
        A CommandResult object containing the exit code, stdout, stderr, and execution time.
    """
    start_time = time.time()

    if shell:
        raise ValueError("shell=True is disallowed by project security standards")
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        with track_child(process):
            stdout, stderr = await process.communicate()
        execution_time = time.time() - start_time
        return CommandResult(
            exit_code=process.returncode or 0,
            stdout=stdout.decode("utf-8", errors="replace"),
            stderr=stderr.decode("utf-8", errors="replace"),
            execution_time=execution_time,
        )
    except Exception as exc:
        execution_time = time.time() - start_time
        return CommandResult(
            exit_code=1,
            stdout="",
            stderr=f"Error executing command: {str(exc)}",
            execution_time=execution_time,
        )
    finally:
        if process.returncode is None:
            process.kill()
            await process.wait()


class CheckDig(AsyncNagiosPlugin):
    """Check DNS via SSH using dig.

    -w/-c are Nagios ranges for the query time in seconds.
    """

    def __init__(self) -> None:
        """Register the SSH target, query and retry arguments."""
        super().__init__()
        self.parser.add_argument("--host", required=True, help="SSH host to connect to")
        self.parser.add_argument("--query", required=True, help="DNS name to query")
        self.parser.add_argument("--ssh-user", help="SSH username")
        self.parser.add_argument("--ssh-port", type=int, default=22, help="SSH port (default: 22)")
        self.parser.add_argument("--dns-port", type=int, default=53, help="DNS port (default: 53)")
        self.parser.add_argument(
            "--record-type", default="A", help="DNS record type (A, AAAA, MX, etc.; default: A)"
        )
        self.parser.add_argument("--dig-arguments", help="Additional dig command arguments")
        self.parser.add_argument("--expected", help="Expected result from the DNS query")
        self.parser.add_argument(
            "--retries", type=int, default=1, help="Number of attempts (default: 1)"
        )

    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Query DNS over SSH with the configured options."""
        return await SSHDNSChecker(
            ssh_host=args.host,
            query_address=args.query,
            ssh_user=args.ssh_user,
            ssh_port=args.ssh_port,
            dns_port=args.dns_port,
            record_type=args.record_type,
            dig_arguments=args.dig_arguments,
            expected_address=args.expected,
            timeout=args.timeout,
            retries=args.retries,
            warning_threshold=args.warning,
            critical_threshold=args.critical,
        ).check_dns()


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckDig().run()


if __name__ == "__main__":
    raise SystemExit(main())
