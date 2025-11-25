"""
check_dig - DNS Resolution Monitoring Plugin for Nagios

This plugin checks DNS resolution using the dig command, optionally
via SSH on a remote host.
"""

import argparse
import re
import subprocess
import time
from typing import List, Optional, Tuple

from .base import CheckResult, NagiosPlugin, Status, ThresholdRange, get_env_or_arg


class CheckDig(NagiosPlugin):
    """Check DNS resolution via dig command."""

    name = "check_dig"
    version = "2.0.0"
    description = "Check DNS resolution using dig"

    def _add_arguments(self) -> None:
        self.parser.add_argument(
            "-H",
            "--host",
            help="DNS server to query (default: system resolver)",
        )
        self.parser.add_argument(
            "-l",
            "--lookup",
            required=True,
            help="Hostname to look up",
        )
        self.parser.add_argument(
            "-T",
            "--record-type",
            default="A",
            choices=["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR", "SRV"],
            help="DNS record type (default: A)",
        )
        self.parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=53,
            help="DNS server port (default: 53)",
        )
        self.parser.add_argument(
            "-a",
            "--expected-address",
            help="Expected address in response",
        )
        self.parser.add_argument(
            "-A",
            "--dig-arguments",
            help="Additional arguments to pass to dig",
        )
        self.parser.add_argument(
            "-w",
            "--warning",
            help="Warning threshold for query time (seconds)",
        )
        self.parser.add_argument(
            "-c",
            "--critical",
            help="Critical threshold for query time (seconds)",
        )
        self.parser.add_argument(
            "-R",
            "--remote-host",
            help="Execute dig on this remote host via SSH",
        )
        self.parser.add_argument(
            "-U",
            "--remote-user",
            help="SSH username for remote execution",
        )
        self.parser.add_argument(
            "-P",
            "--remote-port",
            type=int,
            default=22,
            help="SSH port for remote execution (default: 22)",
        )

        self.parser.epilog = """
Examples:
  %(prog)s -l example.com
  %(prog)s -H 8.8.8.8 -l example.com -a 93.184.216.34
  %(prog)s -l example.com -T MX -w 1 -c 2
  %(prog)s -R remote.host -l internal.domain

Environment variables:
  NAGIOS_SSH_USER - Default SSH username for remote execution
        """

    def _build_dig_command(
        self,
        lookup: str,
        record_type: str,
        server: Optional[str] = None,
        port: int = 53,
        extra_args: Optional[str] = None,
    ) -> List[str]:
        """Build the dig command with proper arguments."""
        cmd = ["dig", "+short", "+time=10", "+tries=2"]

        if server:
            cmd.append(f"@{server}")

        if port != 53:
            cmd.extend(["-p", str(port)])

        cmd.extend(["-t", record_type, lookup])

        if extra_args:
            # Sanitize extra args to prevent injection
            safe_args = re.sub(r"[;&|`$]", "", extra_args)
            cmd.extend(safe_args.split())

        return cmd

    def _execute_local(self, cmd: List[str], timeout: int) -> Tuple[str, float]:
        """Execute dig locally and return output and timing."""
        start = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start

        if result.returncode != 0:
            raise RuntimeError(f"dig failed: {result.stderr.strip()}")

        return result.stdout.strip(), elapsed

    def _execute_remote(
        self,
        cmd: List[str],
        host: str,
        user: str,
        port: int,
        timeout: int,
    ) -> Tuple[str, float]:
        """Execute dig on a remote host via SSH."""
        ssh_cmd = [
            "ssh",
            f"{user}@{host}",
            "-p",
            str(port),
            "-o",
            "BatchMode=yes",
            "-o",
            f"ConnectTimeout={timeout}",
            " ".join(cmd),
        ]

        start = time.time()
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start

        if result.returncode != 0:
            raise RuntimeError(f"Remote dig failed: {result.stderr.strip()}")

        return result.stdout.strip(), elapsed

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the DNS resolution check."""
        dig_cmd = self._build_dig_command(
            lookup=args.lookup,
            record_type=args.record_type,
            server=args.host,
            port=args.port,
            extra_args=args.dig_arguments,
        )

        try:
            if args.remote_host:
                remote_user = get_env_or_arg("NAGIOS_SSH_USER", args.remote_user, "nagios")
                output, elapsed = self._execute_remote(
                    dig_cmd,
                    args.remote_host,
                    remote_user,
                    args.remote_port,
                    args.timeout,
                )
            else:
                output, elapsed = self._execute_local(dig_cmd, args.timeout)

        except subprocess.TimeoutExpired:
            return CheckResult(Status.CRITICAL, "DNS query timed out")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"DNS query failed: {e}")

        # Check if we got any response
        if not output:
            return CheckResult(
                Status.CRITICAL,
                f"No DNS response for {args.lookup} ({args.record_type})",
            )

        # Check expected address if specified
        if args.expected_address:
            addresses = output.splitlines()
            if args.expected_address not in addresses:
                return CheckResult(
                    Status.CRITICAL,
                    f"Expected {args.expected_address} not in response: {output}",
                )

        # Check timing thresholds
        warn_range = ThresholdRange.parse(args.warning)
        crit_range = ThresholdRange.parse(args.critical)

        perfdata = {
            "time": {
                "value": round(elapsed, 3),
                "unit": "s",
                "warn": args.warning or "",
                "crit": args.critical or "",
                "min": 0,
            }
        }

        # First line of output for message
        first_result = output.splitlines()[0] if output else "no response"

        if crit_range and crit_range.check(elapsed):
            return CheckResult(
                Status.CRITICAL,
                f"DNS query took {elapsed:.3f}s - {first_result}",
                perfdata,
            )

        if warn_range and warn_range.check(elapsed):
            return CheckResult(
                Status.WARNING,
                f"DNS query took {elapsed:.3f}s - {first_result}",
                perfdata,
            )

        return CheckResult(
            Status.OK,
            f"{args.lookup} resolves to {first_result} ({elapsed:.3f}s)",
            perfdata,
        )


def main() -> None:
    """Entry point for the check_dig plugin."""
    plugin = CheckDig()
    plugin.run()


if __name__ == "__main__":
    main()
