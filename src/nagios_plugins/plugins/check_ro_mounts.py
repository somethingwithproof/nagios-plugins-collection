#!/usr/bin/env python3
"""
Read-Only Mount Check Plugin for Nagios.

This plugin checks if any filesystems are mounted in read-only mode.
It can exclude specific filesystems and supports remote hosts via SSH.

Usage:
    check_ro_mounts.py [--host HOST] [--ssh-user USER] [--ssh-port PORT]
                      [--exclude LIST] [--timeout SECONDS] [--json] [--verbose]

Returns:
    0 (OK): No read-only mounts found
    1 (WARNING): Non-critical filesystems are mounted read-only
    2 (CRITICAL): Critical filesystems are mounted read-only
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import asyncio
import json
import logging
import sys
import tempfile

from rich.console import Console
from rich.logging import RichHandler

from nagios_plugins.base import CheckResult, Status
from nagios_plugins.utils import execute_command

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("check_ro_mounts")


class MountStatusChecker:
    """Mount status checker."""

    def __init__(
        self,
        host: str | None = None,
        ssh_user: str | None = None,
        ssh_port: int = 22,
        exclude_mounts: list[str] | None = None,
        timeout: int = 30,
    ):
        """Initialize the mount status checker.

        Args:
            host: Remote host to check (None for local)
            ssh_user: SSH username
            ssh_port: SSH port
            exclude_mounts: List of mount points to exclude
            timeout: Command timeout in seconds
        """
        self.host = host
        self.ssh_user = ssh_user
        self.ssh_port = ssh_port
        self.exclude_mounts = set(exclude_mounts or [])
        self.timeout = timeout
        self.console = Console()

        # Add default excludes if not explicitly excluded (system and special filesystems)
        # Instead of hardcoding /tmp, use tempfile.gettempdir() to get the system temp directory
        temp_dir = tempfile.gettempdir()

        default_excludes = {"/proc", "/sys", "/dev", "/run", temp_dir, "/var/lib/docker"}
        self.exclude_mounts.update(default_excludes)

    def _build_command(self) -> list[str]:
        """Build the command to execute.

        Returns:
            Command as a list of arguments
        """
        # The core command to check mount options
        mount_cmd = "mount -l"

        if self.host:
            if self.host.startswith("-"):
                raise ValueError("SSH host must not begin with an option prefix")
            # Execute via SSH
            cmd = ["ssh"]

            # Add port if specified
            if self.ssh_port != 22:
                cmd.extend(["-p", str(self.ssh_port)])

            # Add user if specified
            if self.ssh_user:
                cmd.extend(["-l", self.ssh_user])

            # Add host and command
            cmd.append(self.host)
            cmd.append(mount_cmd)
        else:
            # Execute locally with shell
            cmd = ["mount", "-l"]

        return cmd

    def _parse_mount_output(self, output: str) -> list[dict[str, str]]:
        """Parse mount command output.

        Args:
            output: Output from mount command

        Returns:
            List of dictionaries with mount information
        """
        mounts = []

        for line in output.splitlines():
            parsed = self._parse_mount_line(line)
            if parsed:
                device, mount_point, fs_type, options = parsed
                if "ro" not in options.split(","):
                    continue

                # Skip excluded mount points
                if any(mount_point.startswith(excl) for excl in self.exclude_mounts):
                    continue

                mounts.append(
                    {
                        "device": device,
                        "mount_point": mount_point,
                        "fs_type": fs_type,
                        "options": options,
                    }
                )

        return mounts

    @staticmethod
    def _parse_mount_line(line: str) -> tuple[str, str, str, str] | None:
        """Parse Linux mount output with bounded, linear delimiter searches."""
        device, separator, remainder = line.partition(" on ")
        if not separator:
            return None
        point, separator, remainder = remainder.partition(" type ")
        if not separator:
            return None
        filesystem, separator, options = remainder.partition(" (")
        if not separator or not options.endswith(")"):
            return None
        return device, point, filesystem, options[:-1]

    async def check_mounts(self) -> CheckResult:
        """Check for read-only mounts.

        Returns:
            CheckResult with the check result
        """
        try:
            # Execute the command
            cmd = self._build_command()
            exit_code, stdout, stderr = await asyncio.to_thread(
                execute_command, cmd, timeout=self.timeout
            )
            if exit_code != 0:
                return CheckResult(Status.UNKNOWN, f"Cannot inspect mounts: {stderr}")

            # Get the mount information
            ro_mounts: list[dict[str, str]] = []

            if exit_code == 0 and stdout.strip():
                ro_mounts = self._parse_mount_output(stdout)

            # Determine severity of read-only mounts
            critical_mounts = []
            warning_mounts = []

            for mount in ro_mounts:
                # Critical if root fs or /var
                if mount["mount_point"] == "/" or mount["mount_point"].startswith("/var"):
                    critical_mounts.append(mount)
                else:
                    warning_mounts.append(mount)

            # Create metrics
            metrics = {
                "ro_mounts_count": len(ro_mounts),
                "critical_mounts_count": len(critical_mounts),
                "warning_mounts_count": len(warning_mounts),
            }

            # Create result based on findings
            if critical_mounts:
                return CheckResult(
                    Status.CRITICAL,
                    f"Critical filesystems mounted read-only:"
                    f" {', '.join(m['mount_point'] for m in critical_mounts)}",
                    metrics=metrics,
                    details=json.dumps(ro_mounts, indent=2),
                )
            elif warning_mounts:
                return CheckResult(
                    Status.WARNING,
                    f"Non-critical filesystems mounted read-only:"
                    f" {', '.join(m['mount_point'] for m in warning_mounts)}",
                    metrics=metrics,
                    details=json.dumps(ro_mounts, indent=2),
                )
            else:
                return CheckResult(
                    Status.OK,
                    "No read-only mounts found",
                    metrics=metrics,
                )

        except Exception as e:
            logger.exception("Error checking mounts")
            return CheckResult(
                Status.UNKNOWN,
                f"Error checking mounts: {str(e)}",
                metrics={"ro_mounts_count": 0},
                details=str(e),
            )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Check for read-only mounts",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host",
        help="Remote host to check (None for local)",
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
        "--exclude",
        help="Comma-separated list of mount points to exclude",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Command timeout in seconds",
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


def main() -> int:
    """Main function.

    Returns:
        Exit code
    """
    args = parse_args()

    # Set logging level based on verbosity
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)

    # Parse exclude list
    exclude_mounts = []
    if args.exclude:
        exclude_mounts = [x.strip() for x in args.exclude.split(",")]

    # Create checker and run check
    checker = MountStatusChecker(
        host=args.host,
        ssh_user=args.ssh_user,
        ssh_port=args.ssh_port,
        exclude_mounts=exclude_mounts,
        timeout=args.timeout,
    )

    # This check doesn't need to be async
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    result = loop.run_until_complete(checker.check_mounts())

    # Output the result
    if args.json:
        print(result.to_json())
    else:
        print(result)

    return result.status.value


if __name__ == "__main__":
    sys.exit(main())
