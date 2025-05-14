#!/usr/bin/env python3
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
import sys
import time
from typing import List, Optional

from rich.console import Console
from rich.logging import RichHandler

from nagios_plugins.base import Status, CheckResult
from nagios_plugins.utils import CommandResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("check_dig")


class SSHDNSChecker:
    """SSH DNS Checker using dig."""

    def __init__(
        self,
        ssh_host: str,
        query_address: str,
        ssh_user: Optional[str] = None,
        ssh_port: int = 22,
        dns_port: int = 53,
        record_type: str = "A",
        dig_arguments: Optional[str] = None,
        expected_address: Optional[str] = None,
        timeout: int = 30,
        retries: int = 1,
        warning_threshold: Optional[float] = None,
        critical_threshold: Optional[float] = None,
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
            retries: Number of retries on failure
            warning_threshold: Warning threshold in seconds
            critical_threshold: Critical threshold in seconds
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
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.console = Console()

    def _build_ssh_command(self, dig_command: str) -> List[str]:
        """Build the SSH command to execute.

        Args:
            dig_command: The dig command to execute via SSH

        Returns:
            List of command arguments for SSH
        """
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
        cmd = f"dig -p {self.dns_port} -t {self.record_type} +short {self.query_address}"

        if self.dig_arguments:
            cmd += f" {self.dig_arguments}"

        return cmd

    async def check_dns(self) -> CheckResult:
        """Check DNS via SSH.

        Returns:
            CheckResult with the check result
        """
        attempt = 0
        last_error = None

        while attempt < self.retries:
            try:
                # Build the commands
                dig_cmd = self._build_dig_command()
                ssh_cmd = self._build_ssh_command(dig_cmd)

                # Measure execution time
                start_time = time.time()
                result = await execute_command_async(ssh_cmd, timeout=self.timeout)
                duration = time.time() - start_time

                # Process result
                if result.exit_code != 0:
                    raise Exception(f"SSH command failed: {result.stderr}")

                # Response is in stdout
                response = result.stdout.strip()

                # Check expected address
                if self.expected_address and self.expected_address not in response:
                    return CheckResult(
                        Status.CRITICAL,
                        f"Expected address '{self.expected_address}' not found",
                        metrics={"duration": duration, "response_matches": 0},
                        details=f"Response: {response}",
                    )

                # Check thresholds
                status = Status.OK
                message = f"DNS response received in {duration:.2f}s"

                if self.critical_threshold and duration > self.critical_threshold:
                    status = Status.CRITICAL
                    message = f"Query took {duration:.2f}s (critical: {self.critical_threshold}s)"
                elif self.warning_threshold and duration > self.warning_threshold:
                    status = Status.WARNING
                    message = (
                        f"Query took {duration:.2f}s (warning threshold: {self.warning_threshold}s)"
                    )

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

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                last_error = str(e)
                attempt += 1

                if attempt < self.retries:
                    logger.info(f"Retrying in {self.timeout} seconds...")
                    await asyncio.sleep(self.timeout)

        # All retries failed
        return CheckResult(
            Status.CRITICAL,
            f"DNS query failed after {self.retries} attempts",
            metrics={"duration": 0, "response_matches": 0},
            details=f"Last error: {last_error}",
        )


async def execute_command_async(
    command: List[str], timeout: int = 30, shell: bool = False
) -> CommandResult:
    """Execute a command asynchronously and return the result.

    Args:
        command: The command to execute as a list of strings.
        timeout: The timeout in seconds.
        shell: Whether to execute the command in a shell.

    Returns:
        A CommandResult object containing the exit code, stdout, stderr, and execution time.
    """
    start_time = time.time()

    if shell:
        # If shell is True, join the command list into a string
        cmd = " ".join(command) if isinstance(command, list) else command
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    else:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        execution_time = time.time() - start_time
        return CommandResult(
            exit_code=process.returncode or 0,
            stdout=stdout.decode("utf-8", errors="replace"),
            stderr=stderr.decode("utf-8", errors="replace"),
            execution_time=execution_time,
        )
    except asyncio.TimeoutError:
        process.kill()
        stdout, stderr = await process.communicate()
        execution_time = time.time() - start_time
        return CommandResult(
            exit_code=1,
            stdout=stdout.decode("utf-8", errors="replace") if stdout else "",
            stderr=f"Command timed out after {timeout} seconds: {' '.join(command)}",
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


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Check DNS via SSH using dig",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host",
        required=True,
        help="SSH host to connect to",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="DNS name to query",
    )
    parser.add_argument(
        "--ssh-user",
        help="SSH username",
    )
    parser.add_argument(
        "--ssh-port",
        type=int,
        default=22,
        help="SSH port",
    )
    parser.add_argument(
        "--dns-port",
        type=int,
        default=53,
        help="DNS port",
    )
    parser.add_argument(
        "--record-type",
        default="A",
        help="DNS record type (A, AAAA, MX, etc.)",
    )
    parser.add_argument(
        "--dig-arguments",
        help="Additional dig command arguments",
    )
    parser.add_argument(
        "--expected",
        help="Expected result from the DNS query",
    )
    parser.add_argument(
        "--warning",
        type=float,
        help="Warning threshold in seconds",
    )
    parser.add_argument(
        "--critical",
        type=float,
        help="Critical threshold in seconds",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Command timeout in seconds",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=1,
        help="Number of retries on failure",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )

    return parser.parse_args()


async def main_async() -> int:
    """Main async function.

    Returns:
        Exit code
    """
    args = parse_args()

    # Set logging level based on verbosity
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)

    # Create checker and run check
    checker = SSHDNSChecker(
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
    )

    result = await checker.check_dns()

    # Output the result
    if args.json:
        print(result.to_json())
    else:
        print(result)

    return result.status.value


def main() -> int:
    """Main function.

    Returns:
        Exit code
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(main_async())


if __name__ == "__main__":
    sys.exit(main())
