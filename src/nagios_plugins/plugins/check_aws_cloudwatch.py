#!/usr/bin/env python3
"""Check AWS CloudWatch metrics.

This plugin monitors AWS CloudWatch metrics for various AWS services including
EC2, RDS, Lambda, and ELB. It supports IAM role and access key authentication,
configurable time ranges, and threshold-based alerting.

Example:
    check_aws_cloudwatch \\
        --namespace AWS/EC2 \\
        --metric CPUUtilization \\
        --instance-id i-1234567890abcdef0 \\
        --warning 70 \\
        --critical 90
"""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status, threshold_check
from nagios_plugins.services.aws_cloudwatch import get_metric_statistics


class CheckAwsCloudwatch(NagiosPlugin):
    """Check AWS CloudWatch metrics plugin."""

    def __init__(self) -> None:
        """Initialize the plugin."""
        super().__init__()
        self.parser.add_argument(
            "--namespace",
            required=True,
            help="AWS namespace (e.g., AWS/EC2, AWS/RDS, AWS/Lambda, AWS/ELB)",
        )
        self.parser.add_argument(
            "--metric",
            required=True,
            help="Metric name (e.g., CPUUtilization, DatabaseConnections)",
        )
        self.parser.add_argument(
            "--region",
            help="AWS region (uses default credentials region if not specified)",
        )
        self.parser.add_argument(
            "--statistic",
            default="Average",
            choices=["Average", "Sum", "Maximum", "Minimum", "SampleCount"],
            help="Statistic type (default: Average)",
        )
        self.parser.add_argument(
            "--period",
            type=int,
            default=300,
            help="Period in seconds for the metric (default: 300)",
        )
        self.parser.add_argument(
            "--minutes-back",
            type=int,
            default=5,
            help="How many minutes back to query (default: 5)",
        )

        # Dimension arguments for different AWS services
        self.parser.add_argument(
            "--instance-id",
            help="EC2 instance ID (for AWS/EC2 namespace)",
        )
        self.parser.add_argument(
            "--db-instance-id",
            help="RDS database instance ID (for AWS/RDS namespace)",
        )
        self.parser.add_argument(
            "--function-name",
            help="Lambda function name (for AWS/Lambda namespace)",
        )
        self.parser.add_argument(
            "--load-balancer-name",
            help="ELB load balancer name (for AWS/ELB namespace)",
        )
        self.parser.add_argument(
            "--dimensions",
            help="Custom dimensions in format 'Name=Value,Name=Value'",
        )

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the CloudWatch metric check.

        Args:
            args: Parsed command-line arguments

        Returns:
            CheckResult with status and metric data
        """
        try:
            # Build dimensions based on namespace and provided arguments
            dimensions = self._build_dimensions(args)

            # Get metric statistics from CloudWatch
            result = get_metric_statistics(
                namespace=args.namespace,
                metric_name=args.metric,
                dimensions=dimensions,
                statistic=args.statistic,
                period=args.period,
                minutes_back=args.minutes_back,
                region=args.region,
                timeout=args.timeout,
            )

            value = float(result["value"])
            unit = result["unit"]

            # Check against thresholds
            status = threshold_check(
                value=value,
                warning=args.warning,
                critical=args.critical,
            )

            # Format message
            dimension_str = ", ".join(f"{d['Name']}={d['Value']}" for d in dimensions)
            message = (
                f"{args.namespace}/{args.metric}={value:.2f}{unit} "
                f"({dimension_str}, {args.statistic}, {args.period}s)"
            )

            # Build performance data
            metrics = {
                "value": round(value, 2),
                "unit": unit,
            }

            return CheckResult(
                status=status,
                message=message,
                metrics=metrics,
            )

        except RuntimeError as exc:
            return CheckResult(Status.UNKNOWN, str(exc))
        except Exception as exc:  # pylint: disable=broad-except
            return CheckResult(Status.UNKNOWN, f"Unexpected error: {str(exc)}")

    def _build_dimensions(self, args: argparse.Namespace) -> list[dict[str, str]]:
        """Build CloudWatch dimensions from arguments.

        Args:
            args: Parsed command-line arguments

        Returns:
            List of dimension dictionaries

        Raises:
            ValueError: If required dimensions are missing for the namespace
        """
        dimensions = []

        # Parse custom dimensions if provided
        if args.dimensions:
            for dim in args.dimensions.split(","):
                if "=" not in dim:
                    raise ValueError(f"Invalid dimension format: {dim}")
                name, value = dim.split("=", 1)
                dimensions.append({"Name": name.strip(), "Value": value.strip()})
            return dimensions

        # Build dimensions based on namespace
        namespace = args.namespace.upper()

        if "EC2" in namespace:
            if not args.instance_id:
                raise ValueError("--instance-id required for AWS/EC2 namespace")
            dimensions.append({"Name": "InstanceId", "Value": args.instance_id})

        elif "RDS" in namespace:
            if not args.db_instance_id:
                raise ValueError("--db-instance-id required for AWS/RDS namespace")
            dimensions.append({"Name": "DBInstanceIdentifier", "Value": args.db_instance_id})

        elif "LAMBDA" in namespace:
            if not args.function_name:
                raise ValueError("--function-name required for AWS/Lambda namespace")
            dimensions.append({"Name": "FunctionName", "Value": args.function_name})

        elif "ELB" in namespace:
            if not args.load_balancer_name:
                raise ValueError("--load-balancer-name required for AWS/ELB namespace")
            dimensions.append({"Name": "LoadBalancerName", "Value": args.load_balancer_name})

        else:
            raise ValueError(
                f"Unsupported namespace: {args.namespace}. "
                "Use --dimensions to specify custom dimensions."
            )

        return dimensions


def main() -> int:
    """Entry point for the plugin."""
    return CheckAwsCloudwatch().run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
