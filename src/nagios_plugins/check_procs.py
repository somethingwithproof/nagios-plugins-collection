"""
check_procs - Remote Process Monitoring Plugin for Nagios

This plugin checks the number of running processes on a remote host via SSH.
Supports filtering by process status flags, parent PID, memory usage, and CPU usage.
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional

from .base import CheckResult, NagiosPlugin, Status, ThresholdRange, get_env_or_arg

try:
    from paramiko import SSHClient, AutoAddPolicy
    from paramiko.ssh_exception import AuthenticationException, SSHException

    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False


@dataclass
class Process:
    """Represents a process with its attributes."""

    uid: str
    pid: str
    parent_pid: str
    vsz: str
    rss: str
    status: str
    time: str
    pcpu: str
    command: str = ""


class CheckProcs(NagiosPlugin):
    """Check running processes on a remote host via SSH."""

    name = "check_procs"
    version = "2.0.0"
    description = "Check running processes on a remote host via SSH"

    def _add_arguments(self) -> None:
        self.parser.add_argument(
            "-H",
            "--host",
            required=True,
            help="Hostname or IP address of remote host",
        )
        self.parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=22,
            help="SSH port (default: 22)",
        )
        self.parser.add_argument(
            "-u",
            "--username",
            help="SSH username (default: nagios or NAGIOS_SSH_USER env)",
        )
        self.parser.add_argument(
            "-P",
            "--password",
            help="SSH password (prefer NAGIOS_SSH_PASS env variable)",
        )
        self.parser.add_argument(
            "-i",
            "--identity-file",
            help="SSH private key file (prefer NAGIOS_SSH_KEY env variable)",
        )
        self.parser.add_argument(
            "-C",
            "--command",
            help="Filter by command name",
        )
        self.parser.add_argument(
            "-s",
            "--status-flags",
            help="Filter by process status flags (comma-separated, e.g., S,Z,R)",
        )
        self.parser.add_argument(
            "--ppid",
            help="Filter by parent process ID",
        )
        self.parser.add_argument(
            "--vsz",
            type=int,
            help="Filter processes with VSZ greater than this value (KB)",
        )
        self.parser.add_argument(
            "--rss",
            type=int,
            help="Filter processes with RSS greater than this value (KB)",
        )
        self.parser.add_argument(
            "--pcpu",
            type=float,
            help="Filter processes with CPU usage greater than this value (%%)",
        )
        self.parser.add_argument(
            "-w",
            "--warning",
            help="Warning threshold for process count",
        )
        self.parser.add_argument(
            "-c",
            "--critical",
            help="Critical threshold for process count",
        )

        self.parser.epilog = """
Examples:
  %(prog)s -H server.example.com -C httpd -w 1:10 -c 1:20
  %(prog)s -H server.example.com -u admin -s S,Z -w 0:5 -c 0:10

Threshold format:
  10      - Alert if value is outside 0-10 range
  10:     - Alert if value is less than 10
  ~:10    - Alert if value is greater than 10
  10:20   - Alert if value is outside 10-20 range
  @10:20  - Alert if value is inside 10-20 range

Environment variables:
  NAGIOS_SSH_USER - Default SSH username
  NAGIOS_SSH_PASS - SSH password
  NAGIOS_SSH_KEY  - Path to SSH private key
        """

    def _get_ssh_connection(
        self,
        host: str,
        port: int,
        username: str,
        password: Optional[str] = None,
        key_filename: Optional[str] = None,
        timeout: int = 30,
    ) -> "SSHClient":
        """Establish an SSH connection to the remote host."""
        if not HAS_PARAMIKO:
            raise ImportError("paramiko library required. Install with: pip install paramiko")

        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())

        connect_kwargs = {
            "hostname": host,
            "port": port,
            "username": username,
            "timeout": timeout,
        }

        if password:
            connect_kwargs["password"] = password
        if key_filename:
            connect_kwargs["key_filename"] = key_filename

        client.connect(**connect_kwargs)
        return client

    def _get_processes(
        self, ssh_client: "SSHClient", command_filter: Optional[str] = None
    ) -> List[Process]:
        """Get process list from remote host via SSH."""
        if command_filter:
            # Sanitize command filter to prevent injection
            safe_filter = re.sub(r"[^\w\-.]", "", command_filter)
            ps_command = f"ps -C {safe_filter} -o uid,pid,ppid,vsz,rss,stat,bsdtime,pcpu,comm"
        else:
            ps_command = "ps -eo uid,pid,ppid,vsz,rss,stat,bsdtime,pcpu,comm"

        stdin, stdout, stderr = ssh_client.exec_command(ps_command, timeout=30)
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        if error and not output:
            raise RuntimeError(f"Remote command error: {error.strip()}")

        return self._parse_ps_output(output.splitlines())

    def _parse_ps_output(self, lines: List[str]) -> List[Process]:
        """Parse ps output lines into Process objects."""
        result = []
        for line in lines[1:]:  # Skip header
            parts = re.split(r"\s+", line.strip(), maxsplit=8)
            if len(parts) >= 8:
                result.append(
                    Process(
                        uid=parts[0],
                        pid=parts[1],
                        parent_pid=parts[2],
                        vsz=parts[3],
                        rss=parts[4],
                        status=parts[5],
                        time=parts[6],
                        pcpu=parts[7],
                        command=parts[8] if len(parts) > 8 else "",
                    )
                )
        return result

    def _filter_processes(
        self,
        processes: List[Process],
        status_flags: Optional[List[str]] = None,
        ppid: Optional[str] = None,
        vsz_min: Optional[int] = None,
        rss_min: Optional[int] = None,
        pcpu_min: Optional[float] = None,
    ) -> List[Process]:
        """Filter processes based on specified criteria."""
        result = processes

        if status_flags:
            result = [
                p
                for p in result
                if any(flag in list(p.status) for flag in status_flags)
            ]
        if ppid:
            result = [p for p in result if p.parent_pid == ppid]
        if vsz_min is not None:
            result = [p for p in result if int(p.vsz) > vsz_min]
        if rss_min is not None:
            result = [p for p in result if int(p.rss) > rss_min]
        if pcpu_min is not None:
            result = [p for p in result if float(p.pcpu) > pcpu_min]

        return result

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the process check."""
        # Get credentials from args or environment
        username = get_env_or_arg("NAGIOS_SSH_USER", args.username, "nagios")
        password = get_env_or_arg("NAGIOS_SSH_PASS", args.password)
        key_file = get_env_or_arg("NAGIOS_SSH_KEY", args.identity_file)

        try:
            ssh_client = self._get_ssh_connection(
                host=args.host,
                port=args.port,
                username=username,
                password=password,
                key_filename=key_file,
                timeout=args.timeout,
            )
        except AuthenticationException as e:
            return CheckResult(Status.UNKNOWN, f"Authentication failed: {e}")
        except SSHException as e:
            return CheckResult(Status.UNKNOWN, f"SSH error: {e}")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Connection error: {e}")

        try:
            processes = self._get_processes(ssh_client, args.command)

            status_flags = args.status_flags.split(",") if args.status_flags else None
            filtered = self._filter_processes(
                processes,
                status_flags=status_flags,
                ppid=args.ppid,
                vsz_min=args.vsz,
                rss_min=args.rss,
                pcpu_min=args.pcpu,
            )

            proc_count = len(filtered)
            warn_range = ThresholdRange.parse(args.warning)
            crit_range = ThresholdRange.parse(args.critical)

            perfdata = {
                "procs": {
                    "value": proc_count,
                    "warn": args.warning or "",
                    "crit": args.critical or "",
                    "min": 0,
                    "max": "",
                }
            }

            if crit_range and crit_range.check(proc_count):
                return CheckResult(Status.CRITICAL, f"{proc_count} processes", perfdata)

            if warn_range and warn_range.check(proc_count):
                return CheckResult(Status.WARNING, f"{proc_count} processes", perfdata)

            return CheckResult(Status.OK, f"{proc_count} processes", perfdata)

        finally:
            ssh_client.close()


def main() -> None:
    """Entry point for the check_procs plugin."""
    plugin = CheckProcs()
    plugin.run()


if __name__ == "__main__":
    main()
