#!/usr/bin/env python3
"""
check_procs.py - Remote Process Monitoring Plugin for Nagios

This plugin checks the number of running processes on a remote host via SSH.
It supports filtering by process status flags, parent PID, memory usage, and CPU usage.

Author: Thomas Vincent
License: MIT License
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

try:
    from paramiko import SSHClient, AutoAddPolicy
    from paramiko.ssh_exception import AuthenticationException, SSHException
except ImportError:
    print("UNKNOWN - paramiko library is required. Install with: pip install paramiko")
    sys.exit(3)

# Plugin return codes (Nagios standard)
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


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


def parse_range(range_str: Optional[str]) -> Optional[Tuple[Optional[int], Optional[int], bool]]:
    """
    Parse a Nagios-style range string.

    Format: [@]start:end
    - @ means alert if inside range (default is alert if outside)
    - start: can be ~ for negative infinity
    - end: can be omitted for positive infinity

    Returns: (start, end, inside) or None if no range specified
    """
    if not range_str:
        return None

    inside = False
    if range_str.startswith('@'):
        inside = True
        range_str = range_str[1:]

    if ':' in range_str:
        parts = range_str.split(':', 1)
        start = None if parts[0] == '~' else int(parts[0]) if parts[0] else 0
        end = None if not parts[1] else int(parts[1])
    else:
        start = 0
        end = int(range_str)

    return (start, end, inside)


def is_outside_range(value: int, range_tuple: Optional[Tuple[Optional[int], Optional[int], bool]]) -> bool:
    """Check if a value is outside the specified range (triggers alert)."""
    if range_tuple is None:
        return False

    start, end, inside = range_tuple

    # Check if value is inside the range
    in_range = True
    if start is not None and value < start:
        in_range = False
    if end is not None and value > end:
        in_range = False

    # If @ prefix, alert when inside; otherwise alert when outside
    return in_range if inside else not in_range


def transform_lines_into_processes(lines: List[str]) -> List[Process]:
    """Parse ps output lines into Process objects."""
    result = []
    # Skip header lines
    for line in lines[1:]:
        parts = re.split(r'\s+', line.strip(), maxsplit=8)
        if len(parts) >= 8:
            result.append(Process(
                uid=parts[0],
                pid=parts[1],
                parent_pid=parts[2],
                vsz=parts[3],
                rss=parts[4],
                status=parts[5],
                time=parts[6],
                pcpu=parts[7],
                command=parts[8] if len(parts) > 8 else ""
            ))
    return result


def test_status_flags(flags_to_check: List[str], process_status: str) -> bool:
    """Check if any of the specified flags are in the process status."""
    process_flags = list(process_status)
    return any(flag in process_flags for flag in flags_to_check)


def get_ssh_connection(host: str, port: int, username: str,
                       password: Optional[str] = None,
                       key_filename: Optional[str] = None,
                       timeout: int = 30) -> SSHClient:
    """
    Establish an SSH connection to the remote host.

    Uses paramiko for secure SSH connections. Supports both password
    and key-based authentication.
    """
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())

    try:
        connect_kwargs = {
            'hostname': host,
            'port': port,
            'username': username,
            'timeout': timeout,
        }

        if password:
            connect_kwargs['password'] = password
        if key_filename:
            connect_kwargs['key_filename'] = key_filename

        client.connect(**connect_kwargs)
        return client
    except AuthenticationException as e:
        print(f"UNKNOWN - Authentication failed: {e}")
        sys.exit(UNKNOWN)
    except SSHException as e:
        print(f"UNKNOWN - SSH error: {e}")
        sys.exit(UNKNOWN)
    except Exception as e:
        print(f"UNKNOWN - Connection error: {e}")
        sys.exit(UNKNOWN)


def get_processes(ssh_client: SSHClient, command_filter: Optional[str] = None) -> List[Process]:
    """
    Get process list from remote host via SSH.

    Uses paramiko's exec_command for secure command execution
    (no shell injection vulnerability).
    """
    # Build the ps command - use list-style arguments to avoid injection
    if command_filter:
        # Sanitize command filter to prevent injection
        safe_filter = re.sub(r'[^\w\-.]', '', command_filter)
        ps_command = f"ps -C {safe_filter} -o uid,pid,ppid,vsz,rss,stat,bsdtime,pcpu,comm"
    else:
        ps_command = "ps -eo uid,pid,ppid,vsz,rss,stat,bsdtime,pcpu,comm"

    try:
        stdin, stdout, stderr = ssh_client.exec_command(ps_command, timeout=30)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if error and not output:
            print(f"UNKNOWN - Remote command error: {error.strip()}")
            sys.exit(UNKNOWN)

        return transform_lines_into_processes(output.splitlines())
    except Exception as e:
        print(f"UNKNOWN - Failed to get processes: {e}")
        sys.exit(UNKNOWN)


def filter_processes(processes: List[Process],
                     status_flags: Optional[List[str]] = None,
                     ppid: Optional[str] = None,
                     vsz_min: Optional[int] = None,
                     rss_min: Optional[int] = None,
                     pcpu_min: Optional[float] = None) -> List[Process]:
    """Filter processes based on specified criteria."""
    result = processes

    if status_flags:
        result = [p for p in result if test_status_flags(status_flags, p.status)]
    if ppid:
        result = [p for p in result if p.parent_pid == ppid]
    if vsz_min is not None:
        result = [p for p in result if int(p.vsz) > vsz_min]
    if rss_min is not None:
        result = [p for p in result if int(p.rss) > rss_min]
    if pcpu_min is not None:
        result = [p for p in result if float(p.pcpu) > pcpu_min]

    return result


def check_thresholds(proc_count: int, warning: Optional[str],
                     critical: Optional[str]) -> Tuple[int, str]:
    """
    Check process count against thresholds.

    Returns: (exit_code, message)
    """
    warn_range = parse_range(warning)
    crit_range = parse_range(critical)

    perf_data = f" | procs={proc_count};{warning or ''};{critical or ''};0;"

    if crit_range and is_outside_range(proc_count, crit_range):
        return CRITICAL, f"PROCS CRITICAL - {proc_count} processes{perf_data}"

    if warn_range and is_outside_range(proc_count, warn_range):
        return WARNING, f"PROCS WARNING - {proc_count} processes{perf_data}"

    return OK, f"PROCS OK - {proc_count} processes{perf_data}"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Check running processes on a remote host via SSH.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -H server.example.com -C httpd -w 1:10 -c 1:20
  %(prog)s -H server.example.com -u admin -s S,Z -w 0:5 -c 0:10

Threshold format:
  10      - Alert if value is outside 0-10 range
  10:     - Alert if value is less than 10
  ~:10    - Alert if value is greater than 10
  10:20   - Alert if value is outside 10-20 range
  @10:20  - Alert if value is inside 10-20 range
        """
    )

    parser.add_argument('-H', '--host', required=True,
                        help='Hostname or IP address of remote host')
    parser.add_argument('-p', '--port', type=int, default=22,
                        help='SSH port (default: 22)')
    parser.add_argument('-u', '--username',
                        default=os.environ.get('NAGIOS_SSH_USER', 'nagios'),
                        help='SSH username (default: nagios or NAGIOS_SSH_USER env)')
    parser.add_argument('-P', '--password',
                        default=os.environ.get('NAGIOS_SSH_PASS'),
                        help='SSH password (prefer NAGIOS_SSH_PASS env variable)')
    parser.add_argument('-i', '--identity-file',
                        default=os.environ.get('NAGIOS_SSH_KEY'),
                        help='SSH private key file (prefer NAGIOS_SSH_KEY env variable)')
    parser.add_argument('-C', '--command',
                        help='Filter by command name')
    parser.add_argument('-s', '--status-flags',
                        help='Filter by process status flags (comma-separated, e.g., S,Z,R)')
    parser.add_argument('--ppid',
                        help='Filter by parent process ID')
    parser.add_argument('--vsz', type=int,
                        help='Filter processes with VSZ greater than this value (KB)')
    parser.add_argument('--rss', type=int,
                        help='Filter processes with RSS greater than this value (KB)')
    parser.add_argument('--pcpu', type=float,
                        help='Filter processes with CPU usage greater than this value (%%)')
    parser.add_argument('-w', '--warning',
                        help='Warning threshold for process count')
    parser.add_argument('-c', '--critical',
                        help='Critical threshold for process count')
    parser.add_argument('-t', '--timeout', type=int, default=30,
                        help='Connection timeout in seconds (default: 30)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Establish SSH connection
    ssh_client = get_ssh_connection(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        key_filename=args.identity_file,
        timeout=args.timeout
    )

    try:
        # Get and filter processes
        processes = get_processes(ssh_client, args.command)

        status_flags = args.status_flags.split(',') if args.status_flags else None
        filtered = filter_processes(
            processes,
            status_flags=status_flags,
            ppid=args.ppid,
            vsz_min=args.vsz,
            rss_min=args.rss,
            pcpu_min=args.pcpu
        )

        # Check thresholds and report
        exit_code, message = check_thresholds(
            len(filtered),
            args.warning,
            args.critical
        )

        if args.verbose and filtered:
            print(message)
            print("\nMatching processes:")
            for proc in filtered[:10]:  # Limit output
                print(f"  PID {proc.pid}: {proc.command} (status={proc.status})")
            if len(filtered) > 10:
                print(f"  ... and {len(filtered) - 10} more")
        else:
            print(message)

        sys.exit(exit_code)

    finally:
        ssh_client.close()


if __name__ == '__main__':
    main()
