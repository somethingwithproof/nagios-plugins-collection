#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""
Job Status Check Plugin for Nagios.

This plugin checks the status of jobs by querying a JSON API endpoint.
It validates root status and component statuses to determine overall health.

Usage:
    check_jobs.py --url URL [--timeout SECONDS] [--json] [--verbose]

Returns:
    0 (OK): All jobs and components are healthy
    1 (WARNING): Some jobs or components have warnings
    2 (CRITICAL): Critical issues with jobs or components
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import json
import logging

import httpx

from nagios_plugins.base import AsyncNagiosPlugin, CheckResult, Status

logger = logging.getLogger("check_jobs")


class JobStatusChecker:
    """Job status checker."""

    def __init__(
        self,
        url: str,
        timeout: int = 30,
    ):
        """Initialize the job status checker.

        Args:
            url: URL to the jobs status API
            timeout: HTTP request timeout in seconds
        """
        self.url = url
        self.timeout = timeout

    async def check_jobs(self) -> CheckResult:
        """Check the job statuses.

        Returns:
            CheckResult with the check result
        """
        try:
            # Make request to the jobs API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.url)
                response.raise_for_status()

                # Parse the JSON response
                data = response.json()

            # Check the overall status
            root_status = data.get("status", "unknown").lower()
            root_title = data.get("title", "Jobs")
            root_message = data.get("message", "").replace("\n", "; ")

            # Create metrics
            metrics = {"root_status": 1 if root_status == "ok" else 0}
            failed_components: list[str] = []

            # Check if overall status is OK
            if root_status != "ok":
                return CheckResult(
                    Status.WARNING,
                    f"Root status {root_title} is {root_status.upper()}.Message: {root_message}",
                    metrics=metrics,
                    details=json.dumps(data, indent=2),
                )

            # Check each component
            for component in data.get("components", []):
                component_name = component.get("name", "unknown")
                component_status = component.get("status", "unknown").lower()
                component_message = (
                    component.get("message", "").replace("\n", "; ")
                    if component.get("message")
                    else ""
                )

                metrics[f"component_{component_name}_status"] = 1 if component_status == "ok" else 0

                if component_status != "ok":
                    failed_components.append(
                        f"Component {component_name} status {component_status.upper()}:"
                        f" {component_message}"
                    )

            # If any components failed, return a warning
            if failed_components:
                return CheckResult(
                    Status.WARNING,
                    failed_components[0],
                    metrics=metrics,
                    details="\n".join(failed_components),
                )

            # All checks passed
            return CheckResult(
                Status.OK,
                "All jobs and components are healthy",
                metrics=metrics,
            )

        except httpx.HTTPError as e:
            logger.exception("HTTP request failed")
            return CheckResult(
                Status.UNKNOWN,
                f"Failed to connect to jobs API: {str(e)}",
                metrics={"root_status": 0},
            )
        except json.JSONDecodeError as e:
            logger.exception("JSON response decoding failed")
            return CheckResult(
                Status.UNKNOWN,
                f"Invalid JSON response from jobs API: {str(e)}",
                metrics={"root_status": 0},
            )
        except Exception as e:
            logger.exception("Unexpected monitoring failure")
            return CheckResult(
                Status.UNKNOWN,
                f"Unexpected error: {str(e)}",
                metrics={"root_status": 0},
            )


class CheckJobs(AsyncNagiosPlugin):
    """Check job statuses."""

    has_thresholds = False

    def __init__(self) -> None:
        """Register the jobs status API argument."""
        super().__init__()
        self.parser.add_argument("--url", required=True, help="URL to the jobs status API")

    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Check the configured jobs endpoint."""
        return await JobStatusChecker(url=args.url, timeout=args.timeout).check_jobs()


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckJobs().run()


if __name__ == "__main__":
    raise SystemExit(main())
