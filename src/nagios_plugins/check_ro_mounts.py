"""
check_ro_mounts - Read-Only Mount Detection Plugin for Nagios

This plugin checks mount points on a remote host for read-only mounts
which often indicate filesystem issues.
"""

import argparse
import shlex
import subprocess
from dataclasses import dataclass
from typing import List, Optional

from .base import CheckResult, NagiosPlugin, Status, get_env_or_arg


@dataclass
class Mount:
    """Represents a filesystem mount point."""

    device: str
    mountpoint: str
    fstype: str
    options: str

    @property
    def is_readonly(self) -> bool:
        """Check if the mount is read-only."""
        opts = self.options.split(",")
        return "ro" in opts


class CheckROMounts(NagiosPlugin):
    """Check for read-only mounts on a remote host."""

    name = "check_ro_mounts"
    version = "2.0.0"
    description = "Check for read-only filesystem mounts on a remote host"

    def _add_arguments(self) -> None:
        self.parser.add_argument(
            "-H",
            "--host",
            required=True,
            help="Hostname or IP address of remote host",
        )
        self.parser.add_argument(
            "-u",
            "--username",
            help="SSH username (default: nagios or NAGIOS_SSH_USER env)",
        )
        self.parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=22,
            help="SSH port (default: 22)",
        )
        self.parser.add_argument(
            "-m",
            "--mtab-path",
            default="/proc/mounts",
            help="Path to mtab/mounts file (default: /proc/mounts)",
        )
        self.parser.add_argument(
            "-i",
            "--include",
            action="append",
            help="Include only these mount points (can be specified multiple times)",
        )
        self.parser.add_argument(
            "-x",
            "--exclude",
            action="append",
            help="Exclude these mount points (can be specified multiple times)",
        )
        self.parser.add_argument(
            "-X",
            "--exclude-type",
            action="append",
            help="Exclude filesystem types (can be specified multiple times)",
        )
        self.parser.add_argument(
            "-w",
            "--warning",
            type=int,
            default=0,
            help="Warning threshold for number of RO mounts",
        )
        self.parser.add_argument(
            "-c",
            "--critical",
            type=int,
            default=1,
            help="Critical threshold for number of RO mounts (default: 1)",
        )

        self.parser.epilog = """
Examples:
  %(prog)s -H server.example.com
  %(prog)s -H server.example.com -X tmpfs -X devpts
  %(prog)s -H server.example.com -i /data -i /backup

Environment variables:
  NAGIOS_SSH_USER - Default SSH username
        """

    def _execute_ssh_command(
        self, host: str, user: str, port: int, command: str
    ) -> List[str]:
        """Execute a command via SSH and return output lines."""
        ssh_cmd = ["ssh", f"{user}@{host}", "-p", str(port), "-o", "BatchMode=yes", command]

        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise RuntimeError(f"SSH command failed: {result.stderr.strip()}")

        return result.stdout.strip().splitlines()

    def _parse_mounts(self, lines: List[str]) -> List[Mount]:
        """Parse mount output into Mount objects."""
        mounts = []
        for line in lines:
            parts = shlex.split(line)
            if len(parts) >= 4:
                mounts.append(
                    Mount(
                        device=parts[0],
                        mountpoint=parts[1],
                        fstype=parts[2],
                        options=parts[3],
                    )
                )
        return mounts

    def _filter_mounts(
        self,
        mounts: List[Mount],
        include: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
        exclude_types: Optional[List[str]] = None,
    ) -> List[Mount]:
        """Filter mounts based on criteria."""
        result = mounts

        # Filter by type first
        if exclude_types:
            result = [m for m in result if m.fstype not in exclude_types]

        # Include filter takes precedence
        if include:
            result = [m for m in result if m.mountpoint in include]
        elif exclude:
            result = [m for m in result if m.mountpoint not in exclude]

        return result

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the read-only mount check."""
        username = get_env_or_arg("NAGIOS_SSH_USER", args.username, "nagios")

        try:
            # Get mount information
            lines = self._execute_ssh_command(
                args.host, username, args.port, f"cat {args.mtab_path}"
            )
        except subprocess.TimeoutExpired:
            return CheckResult(Status.UNKNOWN, "SSH command timed out")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Failed to get mount info: {e}")

        mounts = self._parse_mounts(lines)
        filtered = self._filter_mounts(
            mounts,
            include=args.include,
            exclude=args.exclude,
            exclude_types=args.exclude_type,
        )

        ro_mounts = [m for m in filtered if m.is_readonly]
        rw_mounts = [m for m in filtered if not m.is_readonly]

        ro_count = len(ro_mounts)
        total_count = len(filtered)

        perfdata = {
            "ro_mounts": {"value": ro_count, "warn": args.warning, "crit": args.critical, "min": 0},
            "total_mounts": {"value": total_count, "min": 0},
        }

        if ro_count >= args.critical:
            ro_list = ", ".join(m.mountpoint for m in ro_mounts[:5])
            extra = f" (and {ro_count - 5} more)" if ro_count > 5 else ""
            return CheckResult(
                Status.CRITICAL,
                f"{ro_count} read-only mount(s): {ro_list}{extra}",
                perfdata,
            )

        if args.warning > 0 and ro_count >= args.warning:
            ro_list = ", ".join(m.mountpoint for m in ro_mounts)
            return CheckResult(
                Status.WARNING,
                f"{ro_count} read-only mount(s): {ro_list}",
                perfdata,
            )

        return CheckResult(
            Status.OK,
            f"All {len(rw_mounts)} mount(s) are read-write",
            perfdata,
        )


def main() -> None:
    """Entry point for the check_ro_mounts plugin."""
    plugin = CheckROMounts()
    plugin.run()


if __name__ == "__main__":
    main()
