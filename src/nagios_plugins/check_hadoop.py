"""
check_hadoop - Hadoop Cluster Health Monitoring Plugin for Nagios

This plugin checks the health status of a Hadoop cluster.
"""

import argparse
import json
import subprocess
from typing import Any, Dict, Optional

from .base import CheckResult, NagiosPlugin, Status

try:
    import httpx

    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class CheckHadoop(NagiosPlugin):
    """Check Hadoop cluster health status."""

    name = "check_hadoop"
    version = "2.0.0"
    description = "Check Hadoop cluster health status"

    def _add_arguments(self) -> None:
        self.parser.add_argument(
            "-H",
            "--host",
            help="Hadoop NameNode host (for HTTP API checks)",
        )
        self.parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=50070,
            help="Hadoop NameNode HTTP port (default: 50070)",
        )
        self.parser.add_argument(
            "-m",
            "--mode",
            choices=["cli", "api"],
            default="cli",
            help="Check mode: cli (hadoop command) or api (HTTP API)",
        )
        self.parser.add_argument(
            "--ssl",
            action="store_true",
            help="Use HTTPS for API mode",
        )
        self.parser.add_argument(
            "-w",
            "--warning",
            type=float,
            help="Warning threshold for HDFS usage percentage",
        )
        self.parser.add_argument(
            "-c",
            "--critical",
            type=float,
            help="Critical threshold for HDFS usage percentage",
        )

        self.parser.epilog = """
Examples:
  %(prog)s
  %(prog)s -m api -H namenode.example.com
  %(prog)s -m api -H namenode.example.com -w 80 -c 90

Modes:
  cli - Uses the 'hadoop' command locally (requires hadoop client)
  api - Queries the NameNode HTTP API (requires network access)
        """

    def _check_cli(self) -> CheckResult:
        """Check Hadoop health using the hadoop CLI."""
        try:
            # Get version
            version_output = subprocess.run(
                ["hadoop", "version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            version = "unknown"
            if version_output.returncode == 0:
                lines = version_output.stdout.strip().splitlines()
                if lines:
                    version = lines[0].split()[-1] if lines[0] else "unknown"

            # Check HDFS health
            health_output = subprocess.run(
                ["hdfs", "dfsadmin", "-report"],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if health_output.returncode != 0:
                return CheckResult(
                    Status.CRITICAL,
                    f"HDFS report failed: {health_output.stderr.strip()}",
                )

            # Parse the report for key metrics
            report = health_output.stdout
            metrics = self._parse_dfs_report(report)

            perfdata = {
                "used_pct": {"value": metrics.get("used_percent", 0), "unit": "%"},
                "live_nodes": {"value": metrics.get("live_nodes", 0)},
                "dead_nodes": {"value": metrics.get("dead_nodes", 0)},
            }

            dead_nodes = metrics.get("dead_nodes", 0)
            if dead_nodes > 0:
                return CheckResult(
                    Status.WARNING,
                    f"Hadoop {version}: {dead_nodes} dead node(s)",
                    perfdata,
                )

            return CheckResult(
                Status.OK,
                f"Hadoop {version} healthy, {metrics.get('live_nodes', 0)} live nodes",
                perfdata,
            )

        except FileNotFoundError:
            return CheckResult(Status.UNKNOWN, "hadoop command not found in PATH")
        except subprocess.TimeoutExpired:
            return CheckResult(Status.UNKNOWN, "Hadoop command timed out")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Error checking Hadoop: {e}")

    def _parse_dfs_report(self, report: str) -> Dict[str, Any]:
        """Parse hdfs dfsadmin -report output."""
        metrics: Dict[str, Any] = {}

        for line in report.splitlines():
            line = line.strip()
            if line.startswith("DFS Used%:"):
                try:
                    metrics["used_percent"] = float(line.split(":")[1].strip().rstrip("%"))
                except (ValueError, IndexError):
                    pass
            elif line.startswith("Live datanodes"):
                try:
                    metrics["live_nodes"] = int(line.split("(")[1].split(")")[0])
                except (ValueError, IndexError):
                    pass
            elif line.startswith("Dead datanodes"):
                try:
                    metrics["dead_nodes"] = int(line.split("(")[1].split(")")[0])
                except (ValueError, IndexError):
                    pass

        return metrics

    def _check_api(
        self,
        host: str,
        port: int,
        use_ssl: bool,
        timeout: int,
        warning: Optional[float],
        critical: Optional[float],
    ) -> CheckResult:
        """Check Hadoop health using the HTTP API."""
        if not HAS_HTTPX:
            return CheckResult(
                Status.UNKNOWN,
                "httpx library required for API mode. Install with: pip install httpx",
            )

        protocol = "https" if use_ssl else "http"
        url = f"{protocol}://{host}:{port}/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState"

        try:
            with httpx.Client(timeout=timeout, verify=not use_ssl) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()

        except httpx.TimeoutException:
            return CheckResult(Status.CRITICAL, f"Connection to {host}:{port} timed out")
        except httpx.HTTPStatusError as e:
            return CheckResult(Status.CRITICAL, f"HTTP error: {e.response.status_code}")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"API request failed: {e}")

        try:
            beans = data.get("beans", [])
            if not beans:
                return CheckResult(Status.UNKNOWN, "No data in API response")

            fs_state = beans[0]
            live_nodes = fs_state.get("NumLiveDataNodes", 0)
            dead_nodes = fs_state.get("NumDeadDataNodes", 0)
            capacity = fs_state.get("CapacityTotal", 1)
            used = fs_state.get("CapacityUsed", 0)
            used_pct = (used / capacity * 100) if capacity > 0 else 0

            perfdata = {
                "used_pct": {
                    "value": round(used_pct, 2),
                    "unit": "%",
                    "warn": warning or "",
                    "crit": critical or "",
                },
                "live_nodes": {"value": live_nodes},
                "dead_nodes": {"value": dead_nodes},
                "capacity_bytes": {"value": capacity, "unit": "B"},
                "used_bytes": {"value": used, "unit": "B"},
            }

            # Check thresholds
            if critical and used_pct >= critical:
                return CheckResult(
                    Status.CRITICAL,
                    f"HDFS {used_pct:.1f}% full (>={critical}%)",
                    perfdata,
                )

            if warning and used_pct >= warning:
                return CheckResult(
                    Status.WARNING,
                    f"HDFS {used_pct:.1f}% full (>={warning}%)",
                    perfdata,
                )

            if dead_nodes > 0:
                return CheckResult(
                    Status.WARNING,
                    f"{dead_nodes} dead DataNode(s), {live_nodes} live",
                    perfdata,
                )

            return CheckResult(
                Status.OK,
                f"HDFS healthy: {live_nodes} live nodes, {used_pct:.1f}% used",
                perfdata,
            )

        except (KeyError, TypeError, json.JSONDecodeError) as e:
            return CheckResult(Status.UNKNOWN, f"Failed to parse API response: {e}")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the Hadoop health check."""
        if args.mode == "api":
            if not args.host:
                return CheckResult(Status.UNKNOWN, "Host (-H) required for API mode")
            return self._check_api(
                args.host,
                args.port,
                args.ssl,
                args.timeout,
                args.warning,
                args.critical,
            )
        else:
            return self._check_cli()


def main() -> None:
    """Entry point for the check_hadoop plugin."""
    plugin = CheckHadoop()
    plugin.run()


if __name__ == "__main__":
    main()
