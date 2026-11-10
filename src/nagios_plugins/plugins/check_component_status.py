#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""
Component Status Checker Plugin for Nagios.

This plugin checks the status of components by querying a JSON API,
verifying both component status and update freshness.

Usage:
    check_component_status.py --url URL --components COMPONENT [COMPONENT ...]
                             [--warning MINUTES] [--critical MINUTES]
                             [--timeout SECONDS] [--json] [--verbose]

Returns:
    0 (OK): All components are OK and recently updated
    1 (WARNING): Components are OK but not updated recently
    2 (CRITICAL): One or more components are in an error state
    3 (UNKNOWN): A component has no valid ``updated`` timestamp, or the check failed
"""

import argparse
import datetime
import json
import logging
from typing import Any

import httpx

from nagios_plugins.base import (
    AsyncNagiosPlugin,
    CheckResult,
    NagiosArgumentParser,
    Status,
    most_severe,
)
from nagios_plugins.services import http

logger = logging.getLogger("check_component_status")


class ComponentStatusChecker:
    """Component status checker for monitoring API endpoints."""

    def __init__(
        self,
        url: str,
        components: list[str],
        warning_threshold: int = 10,
        critical_threshold: int | None = None,
        timeout: int = 10,
        settings: http.HttpSettings | None = None,
    ):
        """Initialize the component status checker.

        Args:
            url: URL of the API host (without protocol)
            components: List of component names to check
            warning_threshold: Warning threshold in minutes for stale updates
            critical_threshold: Critical threshold in minutes for stale updates
            timeout: Request timeout in seconds
            settings: Shared HTTP options (TLS, authentication, retries)
        """
        self.url = url
        self.components = components
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold or warning_threshold * 2
        self.timeout = timeout
        self.settings = settings or http.HttpSettings(timeout=timeout)

    async def get_component_status(
        self, component: str, client: httpx.AsyncClient
    ) -> tuple[str, datetime.datetime | None, dict[str, Any]]:
        """Check the status of a component by querying the JSON API.

        Args:
            component: Name of the component
            client: The HTTP client shared by every component request

        Returns:
            Tuple of (status, updated_time, metrics) where:
            - status is one of ('ok', 'error')
            - updated_time is the datetime when component was last updated
            - metrics is a dictionary of component metrics
        """
        # Ensure URL has proper format
        base_url = (
            self.url if self.url.startswith(("http://", "https://")) else f"https://{self.url}"
        )
        api_url = f"{base_url.rstrip('/')}/api/component/{component}"

        problem = ""
        try:
            response = await client.get(api_url)
            response.raise_for_status()
            response_data = response.json()
        except httpx.HTTPError as error:
            problem = http.describe_error(error)
        except ValueError:
            problem = "the body is not JSON"
        if problem:
            # An expected failure of the endpoint, reported without a traceback.
            logger.error("Error fetching component %s status: %s", component, problem)
            return "error", None, {"status": "error"}

        if isinstance(response_data, dict) and response_data:
            component_status = response_data.get("status", "").lower()

            # Parse updated timestamp
            updated_str = response_data.get("updated")
            updated_time = None
            if updated_str:
                try:
                    updated_time = datetime.datetime.fromisoformat(updated_str)
                    if updated_time.tzinfo is None:
                        updated_time = updated_time.replace(tzinfo=datetime.UTC)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid timestamp format: {updated_str}")

            # Extract metrics
            metrics = {
                "status": component_status,
                "response_time_ms": response_data.get("response_time", 0),
            }

            return component_status, updated_time, metrics
        logger.error("Component %s returned no status object", component)
        return "error", None, {"status": "error"}

    async def check(self) -> CheckResult:
        """Perform the component status check.

        Returns:
            CheckResult with the check result
        """
        try:
            # Check all components
            component_statuses = {}
            all_metrics = {}
            critical_components = []
            warning_components = []
            # Freshness is part of the contract: no timestamp is missing data, not OK.
            undated_components = []

            # Get current time for freshness checks
            current_time = datetime.datetime.now(datetime.UTC)

            async with http.async_client(self.settings, follow_redirects=True) as client:
                results = [
                    await self.get_component_status(component, client)
                    for component in self.components
                ]
            for component, (status, updated_time, metrics) in zip(
                self.components, results, strict=True
            ):
                component_statuses[component] = (status, updated_time)

                # Add component-specific metrics
                for metric_name, metric_value in metrics.items():
                    all_metrics[f"{component}_{metric_name}"] = metric_value

                # Check component status
                if status != "ok":
                    critical_components.append(component)
                    continue

                if updated_time is None:
                    undated_components.append(component)
                    continue
                minutes_since_update = (current_time - updated_time).total_seconds() / 60
                all_metrics[f"{component}_minutes_since_update"] = round(minutes_since_update, 2)
                if minutes_since_update > self.critical_threshold:
                    critical_components.append(component)
                elif minutes_since_update > self.warning_threshold:
                    warning_components.append(component)

            # Add summary metrics
            all_metrics["total_components"] = len(self.components)
            all_metrics["critical_components"] = len(critical_components)
            all_metrics["warning_components"] = len(warning_components)
            all_metrics["unknown_components"] = len(undated_components)
            all_metrics["ok_components"] = (
                len(self.components)
                - len(critical_components)
                - len(warning_components)
                - len(undated_components)
            )

            findings = [
                (Status.CRITICAL, "Components with issues", critical_components),
                (Status.WARNING, "Components not recently updated", warning_components),
                (Status.UNKNOWN, "Components without a valid update time", undated_components),
            ]
            parts = [f"{label}: {', '.join(names)}" for _, label, names in findings if names]
            overall = most_severe(*(level for level, _, names in findings if names))
            return CheckResult(
                overall,
                "; ".join(parts)
                or f"All {len(self.components)} components are healthy and recently updated",
                metrics=all_metrics,
                details=json.dumps(component_statuses, default=str, indent=2),
            )

        except Exception as e:
            logger.exception("Error checking components")
            return CheckResult(
                Status.UNKNOWN,
                f"Error checking components: {str(e)}",
                metrics={"error": 1},
                details=str(e),
            )


class CheckComponentStatus(AsyncNagiosPlugin):
    """Check component status and update freshness via a JSON API."""

    default_timeout = 10

    def __init__(self) -> None:
        """Register the API endpoint and component arguments."""
        super().__init__()
        self.parser.add_argument(
            "--url", required=True, help="URL of the API endpoint (without protocol)"
        )
        self.parser.add_argument(
            "--components", required=True, nargs="+", help="List of component names to check"
        )
        http.add_http_arguments(self.parser, env_prefix="CHECK_COMPONENT_STATUS")

    def add_threshold_arguments(self, parser: NagiosArgumentParser) -> None:
        """Take staleness thresholds as whole minutes, as the command always has."""
        parser.add_argument(
            "-w",
            "--warning",
            type=int,
            default=10,
            help="Warning threshold in minutes for stale updates (default: 10)",
        )
        parser.add_argument(
            "-c",
            "--critical",
            type=int,
            help="Critical threshold in minutes for stale updates (default: 2x warning)",
        )

    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Check the configured components."""
        return await ComponentStatusChecker(
            url=args.url,
            components=args.components,
            warning_threshold=args.warning,
            critical_threshold=args.critical,
            timeout=args.timeout,
            settings=http.HttpSettings.from_args(args),
        ).check()


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckComponentStatus().run()


if __name__ == "__main__":
    raise SystemExit(main())
