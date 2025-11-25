"""
check_membase - Membase/Couchbase Statistics Monitoring Plugin for Nagios

This plugin fetches and reports Membase/Couchbase cluster statistics.
"""

import argparse
import base64
import os
from typing import Any, Dict, Optional

from .base import CheckResult, NagiosPlugin, Status, get_env_or_arg

try:
    import httpx

    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class CheckMembase(NagiosPlugin):
    """Check Membase/Couchbase cluster statistics."""

    name = "check_membase"
    version = "2.0.0"
    description = "Check Membase/Couchbase cluster statistics"

    # Metric definitions for performance data
    METRICS = {
        "curr_items": {"name": "current_active_items", "type": "gauge"},
        "curr_items_tot": {"name": "current_total_items", "type": "gauge"},
        "ep_num_active_non_resident": {"name": "items_not_in_ram", "type": "gauge"},
        "get_hits": {"name": "get_hits", "type": "counter"},
        "ep_bg_fetched": {"name": "disk_fetches", "type": "counter"},
        "mem_used": {"name": "memory_used", "type": "gauge", "unit": "B"},
        "ep_total_cache_size": {"name": "cache_size", "type": "gauge", "unit": "B"},
        "ep_queue_size": {"name": "disk_write_queue", "type": "gauge"},
    }

    def _add_arguments(self) -> None:
        self.parser.add_argument(
            "-H",
            "--host",
            required=True,
            help="Membase/Couchbase host",
        )
        self.parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=8091,
            help="REST API port (default: 8091)",
        )
        self.parser.add_argument(
            "-b",
            "--bucket",
            default="default",
            help="Bucket name (default: default)",
        )
        self.parser.add_argument(
            "-u",
            "--username",
            help="Username for authentication",
        )
        self.parser.add_argument(
            "-P",
            "--password",
            help="Password for authentication (prefer MEMBASE_PASSWORD env)",
        )
        self.parser.add_argument(
            "-m",
            "--metric",
            action="append",
            help="Specific metric(s) to check (can be repeated, or 'all')",
        )
        self.parser.add_argument(
            "-w",
            "--warning",
            help="Warning threshold (for single metric mode)",
        )
        self.parser.add_argument(
            "-c",
            "--critical",
            help="Critical threshold (for single metric mode)",
        )
        self.parser.add_argument(
            "--list-metrics",
            action="store_true",
            help="List available metrics and exit",
        )
        self.parser.add_argument(
            "--ssl",
            action="store_true",
            help="Use HTTPS",
        )

        self.parser.epilog = """
Examples:
  %(prog)s -H couchbase.example.com -u admin
  %(prog)s -H couchbase.example.com -m mem_used -w 80 -c 90
  %(prog)s -H couchbase.example.com -m all
  %(prog)s --list-metrics

Environment variables:
  MEMBASE_PASSWORD - Authentication password
        """

    def _fetch_stats(
        self,
        host: str,
        port: int,
        bucket: str,
        username: str,
        password: str,
        use_ssl: bool,
        timeout: int,
    ) -> Dict[str, Any]:
        """Fetch bucket statistics from the REST API."""
        if not HAS_HTTPX:
            raise ImportError("httpx library required. Install with: pip install httpx")

        protocol = "https" if use_ssl else "http"
        url = f"{protocol}://{host}:{port}/pools/default/buckets/{bucket}/stats"

        headers = {}
        if username and password:
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            headers["Authorization"] = f"Basic {credentials}"

        with httpx.Client(timeout=timeout, verify=not use_ssl) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    def _calculate_ratios(self, stats: Dict[str, Any]) -> Dict[str, float]:
        """Calculate derived metrics like ratios."""
        ratios = {}

        # Resident ratio
        curr_items = stats.get("curr_items", 0)
        non_resident = stats.get("ep_num_active_non_resident", 0)
        if curr_items > 0:
            ratios["resident_ratio"] = 100 - (non_resident / curr_items * 100)

        # Cache miss ratio
        get_hits = stats.get("get_hits", 0)
        bg_fetched = stats.get("ep_bg_fetched", 0)
        if get_hits > 0:
            ratios["cache_miss_ratio"] = bg_fetched / get_hits * 100

        return ratios

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the Membase statistics check."""
        if args.list_metrics:
            lines = ["Available metrics:"]
            for key, meta in self.METRICS.items():
                lines.append(f"  {key}: {meta['name']} ({meta['type']})")
            print("\n".join(lines))
            return CheckResult(Status.OK, "Metrics listed")

        password = get_env_or_arg("MEMBASE_PASSWORD", args.password)

        try:
            data = self._fetch_stats(
                args.host,
                args.port,
                args.bucket,
                args.username,
                password,
                args.ssl,
                args.timeout,
            )
        except ImportError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        except httpx.HTTPStatusError as e:
            return CheckResult(
                Status.CRITICAL,
                f"HTTP {e.response.status_code}: {e.response.reason_phrase}",
            )
        except Exception as e:
            return CheckResult(Status.CRITICAL, f"Failed to fetch stats: {e}")

        # Extract samples (most recent values)
        try:
            samples = data.get("op", {}).get("samples", {})
            stats = {key: values[-1] if values else 0 for key, values in samples.items()}
        except (KeyError, IndexError) as e:
            return CheckResult(Status.UNKNOWN, f"Failed to parse stats: {e}")

        # Determine which metrics to report
        if args.metric and "all" not in args.metric:
            requested = args.metric
        else:
            requested = list(self.METRICS.keys())

        # Build perfdata
        perfdata = {}
        for metric in requested:
            if metric in stats:
                meta = self.METRICS.get(metric, {"name": metric, "type": "gauge"})
                value = stats[metric]
                perfdata[meta["name"]] = {
                    "value": value,
                    "unit": meta.get("unit", ""),
                }

        # Add calculated ratios
        ratios = self._calculate_ratios(stats)
        for name, value in ratios.items():
            perfdata[name] = {"value": round(value, 2), "unit": "%"}

        # Single metric mode with thresholds
        if args.metric and len(args.metric) == 1 and args.metric[0] != "all":
            metric = args.metric[0]
            if metric not in stats:
                return CheckResult(Status.UNKNOWN, f"Metric '{metric}' not found")

            value = stats[metric]

            if args.critical:
                try:
                    if value >= float(args.critical):
                        return CheckResult(
                            Status.CRITICAL,
                            f"{metric}={value} (>={args.critical})",
                            perfdata,
                        )
                except ValueError:
                    pass

            if args.warning:
                try:
                    if value >= float(args.warning):
                        return CheckResult(
                            Status.WARNING,
                            f"{metric}={value} (>={args.warning})",
                            perfdata,
                        )
                except ValueError:
                    pass

            return CheckResult(Status.OK, f"{metric}={value}", perfdata)

        # Multi-metric mode
        curr_items = stats.get("curr_items", 0)
        mem_used_mb = stats.get("mem_used", 0) / 1024 / 1024

        return CheckResult(
            Status.OK,
            f"Bucket {args.bucket}: {curr_items} items, {mem_used_mb:.1f}MB used",
            perfdata,
        )


def main() -> None:
    """Entry point for the check_membase plugin."""
    plugin = CheckMembase()
    plugin.run()


if __name__ == "__main__":
    main()
