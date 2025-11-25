"""
check_monghealth - MongoDB Health Monitoring Plugin for Nagios

This plugin checks MongoDB server health via the HTTP API or direct connection.
"""

import argparse
import json
import os
from typing import Any, Dict, Optional

from .base import CheckResult, NagiosPlugin, Status, get_env_or_arg

try:
    import httpx

    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure

    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False


class CheckMongHealth(NagiosPlugin):
    """Check MongoDB health status."""

    name = "check_monghealth"
    version = "2.0.0"
    description = "Check MongoDB server health"

    def _add_arguments(self) -> None:
        self.parser.add_argument(
            "-H",
            "--host",
            default="localhost",
            help="MongoDB host (default: localhost)",
        )
        self.parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=27017,
            help="MongoDB port (default: 27017)",
        )
        self.parser.add_argument(
            "-u",
            "--username",
            help="MongoDB username",
        )
        self.parser.add_argument(
            "-P",
            "--password",
            help="MongoDB password (prefer MONGO_PASSWORD env variable)",
        )
        self.parser.add_argument(
            "-d",
            "--database",
            default="admin",
            help="Authentication database (default: admin)",
        )
        self.parser.add_argument(
            "-m",
            "--mode",
            choices=["status", "replication", "connections", "memory"],
            default="status",
            help="Check mode (default: status)",
        )
        self.parser.add_argument(
            "-w",
            "--warning",
            type=float,
            help="Warning threshold (depends on mode)",
        )
        self.parser.add_argument(
            "-c",
            "--critical",
            type=float,
            help="Critical threshold (depends on mode)",
        )
        self.parser.add_argument(
            "--replica-set",
            help="Expected replica set name",
        )

        self.parser.epilog = """
Examples:
  %(prog)s -H mongo.example.com
  %(prog)s -H mongo.example.com -m connections -w 80 -c 90
  %(prog)s -H mongo.example.com -m replication --replica-set rs0

Modes:
  status      - Basic server status (is it running?)
  replication - Check replica set health and lag
  connections - Check current vs available connections
  memory      - Check memory usage

Environment variables:
  MONGO_PASSWORD - MongoDB password
        """

    def _get_client(
        self,
        host: str,
        port: int,
        username: Optional[str],
        password: Optional[str],
        auth_db: str,
        timeout: int,
    ) -> "MongoClient":
        """Create a MongoDB client connection."""
        if not HAS_PYMONGO:
            raise ImportError("pymongo library required. Install with: pip install pymongo")

        connect_kwargs: Dict[str, Any] = {
            "host": host,
            "port": port,
            "serverSelectionTimeoutMS": timeout * 1000,
            "connectTimeoutMS": timeout * 1000,
        }

        if username and password:
            connect_kwargs["username"] = username
            connect_kwargs["password"] = password
            connect_kwargs["authSource"] = auth_db

        return MongoClient(**connect_kwargs)

    def _check_status(self, client: "MongoClient") -> CheckResult:
        """Check basic MongoDB server status."""
        try:
            # Simple ping
            client.admin.command("ping")

            # Get server status
            status = client.admin.command("serverStatus")
            version = status.get("version", "unknown")
            uptime = status.get("uptime", 0)

            # Format uptime
            days = uptime // 86400
            hours = (uptime % 86400) // 3600

            perfdata = {
                "uptime": {"value": uptime, "unit": "s"},
            }

            return CheckResult(
                Status.OK,
                f"MongoDB {version} running, up {days}d {hours}h",
                perfdata,
            )

        except ConnectionFailure as e:
            return CheckResult(Status.CRITICAL, f"Connection failed: {e}")
        except OperationFailure as e:
            return CheckResult(Status.CRITICAL, f"Operation failed: {e}")

    def _check_connections(
        self,
        client: "MongoClient",
        warning: Optional[float],
        critical: Optional[float],
    ) -> CheckResult:
        """Check MongoDB connection usage."""
        try:
            status = client.admin.command("serverStatus")
            connections = status.get("connections", {})

            current = connections.get("current", 0)
            available = connections.get("available", 1)
            total_created = connections.get("totalCreated", 0)

            max_conns = current + available
            used_pct = (current / max_conns * 100) if max_conns > 0 else 0

            perfdata = {
                "connections": {
                    "value": current,
                    "warn": int(max_conns * (warning / 100)) if warning else "",
                    "crit": int(max_conns * (critical / 100)) if critical else "",
                    "min": 0,
                    "max": max_conns,
                },
                "connections_pct": {
                    "value": round(used_pct, 2),
                    "unit": "%",
                    "warn": warning or "",
                    "crit": critical or "",
                },
                "total_created": {"value": total_created},
            }

            if critical and used_pct >= critical:
                return CheckResult(
                    Status.CRITICAL,
                    f"Connections {used_pct:.1f}% ({current}/{max_conns})",
                    perfdata,
                )

            if warning and used_pct >= warning:
                return CheckResult(
                    Status.WARNING,
                    f"Connections {used_pct:.1f}% ({current}/{max_conns})",
                    perfdata,
                )

            return CheckResult(
                Status.OK,
                f"Connections OK: {current}/{max_conns} ({used_pct:.1f}%)",
                perfdata,
            )

        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Failed to check connections: {e}")

    def _check_replication(
        self,
        client: "MongoClient",
        expected_rs: Optional[str],
        warning: Optional[float],
        critical: Optional[float],
    ) -> CheckResult:
        """Check MongoDB replica set health."""
        try:
            rs_status = client.admin.command("replSetGetStatus")

            rs_name = rs_status.get("set", "unknown")
            members = rs_status.get("members", [])

            # Check replica set name if specified
            if expected_rs and rs_name != expected_rs:
                return CheckResult(
                    Status.CRITICAL,
                    f"Replica set mismatch: expected {expected_rs}, got {rs_name}",
                )

            primary = None
            secondaries = []
            unhealthy = []

            for member in members:
                state = member.get("stateStr", "UNKNOWN")
                name = member.get("name", "unknown")

                if state == "PRIMARY":
                    primary = member
                elif state == "SECONDARY":
                    secondaries.append(member)
                elif state not in ["ARBITER"]:
                    unhealthy.append(f"{name}:{state}")

            if not primary:
                return CheckResult(
                    Status.CRITICAL,
                    f"No PRIMARY in replica set {rs_name}",
                )

            if unhealthy:
                return CheckResult(
                    Status.WARNING,
                    f"Unhealthy members: {', '.join(unhealthy)}",
                )

            # Check replication lag
            max_lag = 0
            primary_optime = primary.get("optimeDate")

            if primary_optime:
                for sec in secondaries:
                    sec_optime = sec.get("optimeDate")
                    if sec_optime:
                        lag = (primary_optime - sec_optime).total_seconds()
                        max_lag = max(max_lag, lag)

            perfdata = {
                "members": {"value": len(members)},
                "secondaries": {"value": len(secondaries)},
                "replication_lag": {
                    "value": round(max_lag, 2),
                    "unit": "s",
                    "warn": warning or "",
                    "crit": critical or "",
                },
            }

            if critical and max_lag >= critical:
                return CheckResult(
                    Status.CRITICAL,
                    f"Replication lag {max_lag:.1f}s (>={critical}s)",
                    perfdata,
                )

            if warning and max_lag >= warning:
                return CheckResult(
                    Status.WARNING,
                    f"Replication lag {max_lag:.1f}s (>={warning}s)",
                    perfdata,
                )

            return CheckResult(
                Status.OK,
                f"Replica set {rs_name} healthy, {len(secondaries)} secondaries, lag {max_lag:.1f}s",
                perfdata,
            )

        except OperationFailure as e:
            if "not running with --replSet" in str(e):
                return CheckResult(Status.WARNING, "Not a replica set member")
            return CheckResult(Status.UNKNOWN, f"Replication check failed: {e}")

    def _check_memory(
        self,
        client: "MongoClient",
        warning: Optional[float],
        critical: Optional[float],
    ) -> CheckResult:
        """Check MongoDB memory usage."""
        try:
            status = client.admin.command("serverStatus")
            mem = status.get("mem", {})

            resident = mem.get("resident", 0)  # MB
            virtual = mem.get("virtual", 0)  # MB

            perfdata = {
                "resident_mb": {"value": resident, "unit": "MB"},
                "virtual_mb": {"value": virtual, "unit": "MB"},
            }

            # Check against thresholds (MB)
            if critical and resident >= critical:
                return CheckResult(
                    Status.CRITICAL,
                    f"Memory usage {resident}MB (>={critical}MB)",
                    perfdata,
                )

            if warning and resident >= warning:
                return CheckResult(
                    Status.WARNING,
                    f"Memory usage {resident}MB (>={warning}MB)",
                    perfdata,
                )

            return CheckResult(
                Status.OK,
                f"Memory OK: {resident}MB resident, {virtual}MB virtual",
                perfdata,
            )

        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Memory check failed: {e}")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the MongoDB health check."""
        password = get_env_or_arg("MONGO_PASSWORD", args.password)

        try:
            client = self._get_client(
                args.host,
                args.port,
                args.username,
                password,
                args.database,
                args.timeout,
            )
        except ImportError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        except Exception as e:
            return CheckResult(Status.CRITICAL, f"Connection failed: {e}")

        try:
            if args.mode == "status":
                return self._check_status(client)
            elif args.mode == "connections":
                return self._check_connections(client, args.warning, args.critical)
            elif args.mode == "replication":
                return self._check_replication(
                    client, args.replica_set, args.warning, args.critical
                )
            elif args.mode == "memory":
                return self._check_memory(client, args.warning, args.critical)
            else:
                return CheckResult(Status.UNKNOWN, f"Unknown mode: {args.mode}")
        finally:
            client.close()


def main() -> None:
    """Entry point for the check_monghealth plugin."""
    plugin = CheckMongHealth()
    plugin.run()


if __name__ == "__main__":
    main()
