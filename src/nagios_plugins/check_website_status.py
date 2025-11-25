"""
check_website_status - Website Availability Monitoring Plugin for Nagios

This plugin checks the availability and response of a website.
"""

import argparse
import re
import time
from typing import Optional

from .base import CheckResult, NagiosPlugin, Status, ThresholdRange

try:
    import httpx

    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class CheckWebsiteStatus(NagiosPlugin):
    """Check website availability and response."""

    name = "check_website_status"
    version = "2.0.0"
    description = "Check website availability and response content"

    def _add_arguments(self) -> None:
        self.parser.add_argument(
            "-U",
            "--url",
            required=True,
            help="URL to check",
        )
        self.parser.add_argument(
            "-s",
            "--string",
            help="String to search for in response body",
        )
        self.parser.add_argument(
            "-r",
            "--regex",
            help="Regular expression to search for in response body",
        )
        self.parser.add_argument(
            "-e",
            "--expect",
            default="200",
            help="Expected HTTP status code(s), comma-separated (default: 200)",
        )
        self.parser.add_argument(
            "-k",
            "--insecure",
            action="store_true",
            help="Disable SSL certificate verification",
        )
        self.parser.add_argument(
            "-f",
            "--follow-redirects",
            action="store_true",
            help="Follow HTTP redirects",
        )
        self.parser.add_argument(
            "-m",
            "--method",
            default="GET",
            choices=["GET", "HEAD", "POST"],
            help="HTTP method (default: GET)",
        )
        self.parser.add_argument(
            "-d",
            "--data",
            help="POST data (for POST method)",
        )
        self.parser.add_argument(
            "-H",
            "--header",
            action="append",
            help="Add HTTP header (format: 'Name: Value')",
        )
        self.parser.add_argument(
            "-a",
            "--auth",
            help="HTTP Basic auth (format: user:password)",
        )
        self.parser.add_argument(
            "-w",
            "--warning",
            help="Warning threshold for response time (seconds)",
        )
        self.parser.add_argument(
            "-c",
            "--critical",
            help="Critical threshold for response time (seconds)",
        )
        self.parser.add_argument(
            "--content-type",
            help="Expected Content-Type header",
        )
        self.parser.add_argument(
            "--min-size",
            type=int,
            help="Minimum response size in bytes",
        )
        self.parser.add_argument(
            "--max-size",
            type=int,
            help="Maximum response size in bytes",
        )

        self.parser.epilog = """
Examples:
  %(prog)s -U https://example.com
  %(prog)s -U https://example.com -s "Welcome"
  %(prog)s -U https://example.com -r "version.*[0-9]+"
  %(prog)s -U https://api.example.com -e 200,201 -w 2 -c 5
  %(prog)s -U https://example.com -H "Authorization: Bearer token"
        """

    def _make_request(
        self,
        url: str,
        method: str,
        headers: dict,
        auth: Optional[tuple],
        data: Optional[str],
        verify_ssl: bool,
        follow_redirects: bool,
        timeout: int,
    ) -> tuple:
        """Make HTTP request and return response with timing."""
        if not HAS_HTTPX:
            raise ImportError("httpx library required. Install with: pip install httpx")

        with httpx.Client(
            timeout=timeout,
            verify=verify_ssl,
            follow_redirects=follow_redirects,
        ) as client:
            start = time.time()

            if method == "GET":
                response = client.get(url, headers=headers, auth=auth)
            elif method == "HEAD":
                response = client.head(url, headers=headers, auth=auth)
            elif method == "POST":
                response = client.post(url, headers=headers, auth=auth, content=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            elapsed = time.time() - start

            return response, elapsed

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the website status check."""
        # Normalize URL
        url = args.url
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        # Build headers
        headers = {"User-Agent": "check_website_status/2.0.0 (Nagios Plugin)"}
        if args.header:
            for h in args.header:
                if ":" in h:
                    key, value = h.split(":", 1)
                    headers[key.strip()] = value.strip()

        # Parse auth
        auth = None
        if args.auth:
            parts = args.auth.split(":", 1)
            if len(parts) == 2:
                auth = (parts[0], parts[1])

        try:
            response, elapsed = self._make_request(
                url,
                args.method,
                headers,
                auth,
                args.data,
                not args.insecure,
                args.follow_redirects,
                args.timeout,
            )
        except ImportError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        except httpx.TimeoutException:
            return CheckResult(Status.CRITICAL, f"Request to {url} timed out")
        except httpx.ConnectError as e:
            return CheckResult(Status.CRITICAL, f"Connection failed: {e}")
        except Exception as e:
            return CheckResult(Status.CRITICAL, f"Request failed: {e}")

        # Check status code
        expected_codes = [int(c.strip()) for c in args.expect.split(",")]
        if response.status_code not in expected_codes:
            return CheckResult(
                Status.CRITICAL,
                f"HTTP {response.status_code} (expected {args.expect})",
            )

        body = response.text
        body_size = len(response.content)

        perfdata = {
            "time": {
                "value": round(elapsed, 3),
                "unit": "s",
                "warn": args.warning or "",
                "crit": args.critical or "",
            },
            "size": {"value": body_size, "unit": "B"},
        }

        # Check string presence
        if args.string:
            if args.string not in body:
                return CheckResult(
                    Status.CRITICAL,
                    f"String '{args.string}' not found in response",
                    perfdata,
                )

        # Check regex match
        if args.regex:
            if not re.search(args.regex, body):
                return CheckResult(
                    Status.CRITICAL,
                    f"Pattern '{args.regex}' not found in response",
                    perfdata,
                )

        # Check content type
        if args.content_type:
            actual_ct = response.headers.get("content-type", "")
            if args.content_type.lower() not in actual_ct.lower():
                return CheckResult(
                    Status.WARNING,
                    f"Content-Type mismatch: expected '{args.content_type}', got '{actual_ct}'",
                    perfdata,
                )

        # Check size constraints
        if args.min_size and body_size < args.min_size:
            return CheckResult(
                Status.WARNING,
                f"Response too small: {body_size}B < {args.min_size}B",
                perfdata,
            )

        if args.max_size and body_size > args.max_size:
            return CheckResult(
                Status.WARNING,
                f"Response too large: {body_size}B > {args.max_size}B",
                perfdata,
            )

        # Check timing thresholds
        warn_range = ThresholdRange.parse(args.warning)
        crit_range = ThresholdRange.parse(args.critical)

        if crit_range and crit_range.check(elapsed):
            return CheckResult(
                Status.CRITICAL,
                f"Response time {elapsed:.3f}s exceeds threshold",
                perfdata,
            )

        if warn_range and warn_range.check(elapsed):
            return CheckResult(
                Status.WARNING,
                f"Response time {elapsed:.3f}s exceeds threshold",
                perfdata,
            )

        return CheckResult(
            Status.OK,
            f"HTTP {response.status_code} - {elapsed:.3f}s, {body_size}B",
            perfdata,
        )


def main() -> None:
    """Entry point for the check_website_status plugin."""
    plugin = CheckWebsiteStatus()
    plugin.run()


if __name__ == "__main__":
    main()
