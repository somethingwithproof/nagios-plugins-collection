#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
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
import tempfile

from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, Status
from nagios_plugins.utils import execute_command

logger = logging.getLogger("check_ro_mounts")


def is_within(path: str, root: str) -> bool:
    """Return whether ``path`` is ``root`` or below it, by whole path components.

    ``/run`` covers ``/run/user`` but not ``/runner``.
    """
    root = root.rstrip("/") or "/"
    return root == "/" or path == root or path.startswith(root + "/")


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
        # Empty entries (for example from a trailing comma) would exclude everything.
        self.exclude_mounts = {m for m in (exclude_mounts or []) if m}
        self.timeout = timeout

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
                if any(is_within(mount_point, excl) for excl in self.exclude_mounts):
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
                if mount["mount_point"] == "/" or is_within(mount["mount_point"], "/var"):
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


class CheckRoMounts(AsyncNagiosPlugin):
    """Check for read-only mounts."""

    has_thresholds = False

    def __init__(self) -> None:
        """Register the local or SSH target and exclude arguments."""
        super().__init__()
        self.parser.add_argument("--host", help="Remote host to check over SSH (default: local)")
        self.parser.add_argument("--ssh-user", help="SSH username")
        self.parser.add_argument("--ssh-port", type=int, default=22, help="SSH port (default: 22)")
        self.parser.add_argument(
            "--exclude", help="Comma-separated list of mount points to exclude"
        )

    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Check mounts on the local or configured remote host."""
        exclude_mounts = [x.strip() for x in args.exclude.split(",")] if args.exclude else []
        return await MountStatusChecker(
            host=args.host,
            ssh_user=args.ssh_user,
            ssh_port=args.ssh_port,
            exclude_mounts=exclude_mounts,
            timeout=args.timeout,
        ).check_mounts()


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckRoMounts().run()


if __name__ == "__main__":
    raise SystemExit(main())
