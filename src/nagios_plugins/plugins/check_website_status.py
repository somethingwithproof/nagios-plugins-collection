#!/usr/bin/env python3
"""
Website Status Check Plugin for Nagios.

This plugin checks the status of a website by making HTTP requests
and validating response status, response time, and content.

Usage:
    check_website_status.py --url URL [--pattern PATTERN] [--timeout SECONDS]
                          [--warning SECONDS] [--critical SECONDS]
                          [--json] [--verbose]

Returns:
    0 (OK): Website is responding properly and within thresholds
    1 (WARNING): Website is responding but response time exceeds warning threshold
    2 (CRITICAL): Website is not responding or status code is invalid
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import asyncio
import logging
import re
import sys
from typing import Dict, Optional

from rich.console import Console

from nagios_plugins.base import Status, CheckResult
from nagios_plugins.plugin_framework import NagiosPluginFramework
from nagios_plugins.utils import check_http_endpoint


class WebsiteStatusChecker(NagiosPluginFramework):
    """Website status checker plugin."""
    
    def _add_plugin_arguments(self) -> None:
        """Add plugin-specific arguments."""
        self.parser.add_argument(
            "--url",
            required=True,
            help="URL of the website to check",
        )
        self.parser.add_argument(
            "--pattern",
            help="Regex pattern that should be present in the response",
        )
        self.parser.add_argument(
            "--warning",
            type=float,
            default=1.0,
            help="Warning threshold for response time in seconds",
        )
        self.parser.add_argument(
            "--critical",
            type=float,
            default=3.0,
            help="Critical threshold for response time in seconds",
        )
        self.parser.add_argument(
            "--no-verify-ssl",
            action="store_true",
            help="Disable SSL certificate verification",
        )
    
    async def check(self) -> CheckResult:
        """Perform the website status check.

        Returns:
            CheckResult with the check result
        """
        try:
            # Normalize URL
            url = self.args.url
            if not url.startswith(("http://", "https://")):
                url = f"http://{url}"
            
            self.logger.info(f"Checking website: {url}")
            
            # Perform the HTTP check
            status, message, response_data = await check_http_endpoint(
                url=url,
                timeout=self.args.timeout,
                expected_content=self.args.pattern,
                verify_ssl=not self.args.no_verify_ssl,
            )
            
            # Extract metrics
            metrics = {}
            if response_data and isinstance(response_data, dict):
                metrics.update(response_data)
            
            # Always include response time
            if "response_time" not in metrics and "response_time_ms" not in metrics:
                # Try to extract from the message
                match = re.search(r"(\d+\.\d+)ms", message)
                if match:
                    response_time_ms = float(match.group(1))
                    metrics["response_time_ms"] = response_time_ms
                    response_time_sec = response_time_ms / 1000.0
                else:
                    response_time_sec = 0
                    
            # Convert ms to seconds if needed
            if "response_time_ms" in metrics and "response_time_sec" not in metrics:
                metrics["response_time_sec"] = metrics["response_time_ms"] / 1000.0
                response_time_sec = metrics["response_time_sec"]
            
            # If there's already a status from the HTTP check, use it
            if status != Status.OK:
                return CheckResult(
                    status,
                    message,
                    metrics=metrics,
                )
            
            # Check against thresholds
            if response_time_sec > self.args.critical:
                return CheckResult(
                    Status.CRITICAL,
                    f"CRITICAL - Response time {response_time_sec:.2f}s exceeds {self.args.critical}s threshold - {url}",
                    metrics=metrics,
                )
            elif response_time_sec > self.args.warning:
                return CheckResult(
                    Status.WARNING,
                    f"WARNING - Response time {response_time_sec:.2f}s exceeds {self.args.warning}s threshold - {url}",
                    metrics=metrics,
                )
            else:
                return CheckResult(
                    Status.OK,
                    f"OK - Website responding in {response_time_sec:.2f}s - {url}",
                    metrics=metrics,
                )
                
        except Exception as e:
            self.logger.exception("Error checking website")
            return CheckResult(
                Status.UNKNOWN,
                f"UNKNOWN - Error checking website: {str(e)}",
                metrics={"error": 1},
                details=str(e),
            )


def main() -> int:
    """Main function."""
    plugin = WebsiteStatusChecker(
        name="check_website_status",
        description="Check website status and response time",
    )
    return plugin.run()


if __name__ == "__main__":
    sys.exit(main())