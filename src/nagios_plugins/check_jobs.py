"""
check_jobs - Job Status Monitoring Plugin for Nagios

This plugin checks the status of jobs via a JSON API endpoint.
"""

import argparse
import json
from typing import Any, Dict, List

from .base import CheckResult, NagiosPlugin, Status

try:
    import httpx

    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class CheckJobs(NagiosPlugin):
    """Check job status via JSON API."""

    name = "check_jobs"
    version = "2.0.0"
    description = "Check job execution status via JSON API"

    def _add_arguments(self) -> None:
        self.parser.add_argument(
            "-U",
            "--url",
            required=True,
            help="URL of the job status JSON endpoint",
        )
        self.parser.add_argument(
            "-k",
            "--insecure",
            action="store_true",
            help="Disable SSL certificate verification",
        )
        self.parser.add_argument(
            "-s",
            "--status-field",
            default="status",
            help="JSON field name for overall status (default: status)",
        )
        self.parser.add_argument(
            "-c",
            "--components-field",
            default="components",
            help="JSON field name for components array (default: components)",
        )
        self.parser.add_argument(
            "--ok-value",
            default="ok",
            help="Value indicating OK status (default: ok)",
        )
        self.parser.add_argument(
            "-H",
            "--header",
            action="append",
            help="Add HTTP header (format: 'Name: Value')",
        )
        self.parser.add_argument(
            "--auth-user",
            help="HTTP Basic auth username",
        )
        self.parser.add_argument(
            "--auth-pass",
            help="HTTP Basic auth password",
        )

        self.parser.epilog = """
Examples:
  %(prog)s -U https://api.example.com/status
  %(prog)s -U https://api.example.com/health -k
  %(prog)s -U https://api.example.com/status -s state --ok-value healthy

Expected JSON format:
  {
    "status": "ok",
    "components": [
      {"name": "database", "status": "ok"},
      {"name": "cache", "status": "ok"}
    ]
  }
        """

    def _fetch_status(
        self,
        url: str,
        headers: Dict[str, str],
        auth: tuple,
        verify_ssl: bool,
        timeout: int,
    ) -> Dict[str, Any]:
        """Fetch and parse the job status JSON."""
        if not HAS_HTTPX:
            raise ImportError("httpx library required. Install with: pip install httpx")

        with httpx.Client(timeout=timeout, verify=verify_ssl) as client:
            response = client.get(url, headers=headers, auth=auth if auth[0] else None)
            response.raise_for_status()
            return response.json()

    def _check_components(
        self,
        components: List[Dict[str, Any]],
        ok_value: str,
    ) -> List[Dict[str, Any]]:
        """Check each component and return failed ones."""
        failed = []
        for comp in components:
            name = comp.get("name", "unknown")
            status = str(comp.get("status", "unknown")).lower()
            message = comp.get("message", "")

            if status != ok_value.lower():
                failed.append({
                    "name": name,
                    "status": status,
                    "message": message,
                })

        return failed

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the job status check."""
        # Normalize URL
        url = args.url
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        # Build headers
        headers = {}
        if args.header:
            for h in args.header:
                if ":" in h:
                    key, value = h.split(":", 1)
                    headers[key.strip()] = value.strip()

        auth = (args.auth_user, args.auth_pass)

        try:
            data = self._fetch_status(
                url,
                headers,
                auth,
                not args.insecure,
                args.timeout,
            )
        except ImportError as e:
            return CheckResult(Status.UNKNOWN, str(e))
        except httpx.HTTPStatusError as e:
            return CheckResult(
                Status.CRITICAL,
                f"HTTP {e.response.status_code}: {e.response.reason_phrase}",
            )
        except httpx.TimeoutException:
            return CheckResult(Status.CRITICAL, f"Request to {url} timed out")
        except json.JSONDecodeError:
            return CheckResult(Status.UNKNOWN, "Invalid JSON response")
        except Exception as e:
            return CheckResult(Status.UNKNOWN, f"Request failed: {e}")

        # Check overall status
        overall_status = str(data.get(args.status_field, "unknown")).lower()
        components = data.get(args.components_field, [])

        perfdata = {
            "total_components": {"value": len(components)},
        }

        # If overall status is not OK
        if overall_status != args.ok_value.lower():
            title = data.get("title", "Jobs")
            message = data.get("message", "").replace("\n", "; ")
            return CheckResult(
                Status.WARNING,
                f"{title} status is {overall_status.upper()}: {message}",
                perfdata,
            )

        # Check individual components
        if components:
            failed = self._check_components(components, args.ok_value)

            perfdata["failed_components"] = {"value": len(failed)}

            if failed:
                # Report first failed component
                first = failed[0]
                msg = first.get("message", "no details")
                return CheckResult(
                    Status.WARNING,
                    f"Component {first['name']} has status {first['status'].upper()}: {msg}",
                    perfdata,
                )

        return CheckResult(
            Status.OK,
            f"All {len(components)} component(s) OK" if components else "Status OK",
            perfdata,
        )


def main() -> None:
    """Entry point for the check_jobs plugin."""
    plugin = CheckJobs()
    plugin.run()


if __name__ == "__main__":
    main()
