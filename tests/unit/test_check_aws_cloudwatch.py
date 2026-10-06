# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for AWS CloudWatch plugin."""

from unittest.mock import patch

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_aws_cloudwatch import CheckAwsCloudwatch


def test_cloudwatch_ec2_cpu_ok() -> None:
    """Test EC2 CPU metric within threshold."""
    plugin = CheckAwsCloudwatch()
    with patch(
        "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
        return_value={
            "value": 45.5,
            "timestamp": "2024-01-01T12:00:00+00:00",
            "unit": "Percent",
        },
    ):
        code = plugin.run(
            [
                "--namespace",
                "AWS/EC2",
                "--metric",
                "CPUUtilization",
                "--instance-id",
                "i-1234567890abcdef0",
                "--warning",
                "70",
                "--critical",
                "90",
            ]
        )
        assert code == Status.OK.value


def test_cloudwatch_ec2_cpu_warning() -> None:
    """Test EC2 CPU metric at warning threshold."""
    plugin = CheckAwsCloudwatch()
    with patch(
        "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
        return_value={
            "value": 75.0,
            "timestamp": "2024-01-01T12:00:00+00:00",
            "unit": "Percent",
        },
    ):
        code = plugin.run(
            [
                "--namespace",
                "AWS/EC2",
                "--metric",
                "CPUUtilization",
                "--instance-id",
                "i-1234567890abcdef0",
                "--warning",
                "70",
                "--critical",
                "90",
            ]
        )
        assert code == Status.WARNING.value


def test_cloudwatch_ec2_cpu_critical() -> None:
    """Test EC2 CPU metric at critical threshold."""
    plugin = CheckAwsCloudwatch()
    with patch(
        "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
        return_value={
            "value": 95.0,
            "timestamp": "2024-01-01T12:00:00+00:00",
            "unit": "Percent",
        },
    ):
        code = plugin.run(
            [
                "--namespace",
                "AWS/EC2",
                "--metric",
                "CPUUtilization",
                "--instance-id",
                "i-1234567890abcdef0",
                "--warning",
                "70",
                "--critical",
                "90",
            ]
        )
        assert code == Status.CRITICAL.value


def test_cloudwatch_rds_connections() -> None:
    """Test RDS database connections metric."""
    plugin = CheckAwsCloudwatch()
    with patch(
        "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
        return_value={
            "value": 25.0,
            "timestamp": "2024-01-01T12:00:00+00:00",
            "unit": "Count",
        },
    ):
        code = plugin.run(
            [
                "--namespace",
                "AWS/RDS",
                "--metric",
                "DatabaseConnections",
                "--db-instance-id",
                "mydb-instance",
                "--warning",
                "50",
                "--critical",
                "100",
            ]
        )
        assert code == Status.OK.value


def test_cloudwatch_lambda_duration() -> None:
    """Test Lambda function duration metric."""
    plugin = CheckAwsCloudwatch()
    with patch(
        "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
        return_value={
            "value": 1500.0,
            "timestamp": "2024-01-01T12:00:00+00:00",
            "unit": "Milliseconds",
        },
    ):
        code = plugin.run(
            [
                "--namespace",
                "AWS/Lambda",
                "--metric",
                "Duration",
                "--function-name",
                "my-function",
                "--warning",
                "2000",
                "--critical",
                "3000",
            ]
        )
        assert code == Status.OK.value


def test_cloudwatch_elb_requests() -> None:
    """Test ELB request count metric."""
    plugin = CheckAwsCloudwatch()
    with patch(
        "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
        return_value={
            "value": 1000.0,
            "timestamp": "2024-01-01T12:00:00+00:00",
            "unit": "Count",
        },
    ):
        code = plugin.run(
            [
                "--namespace",
                "AWS/ELB",
                "--metric",
                "RequestCount",
                "--load-balancer-name",
                "my-load-balancer",
                "--statistic",
                "Sum",
            ]
        )
        assert code == Status.OK.value


def test_cloudwatch_custom_dimensions() -> None:
    """Test custom dimensions."""
    plugin = CheckAwsCloudwatch()
    with patch(
        "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
        return_value={
            "value": 50.0,
            "timestamp": "2024-01-01T12:00:00+00:00",
            "unit": "None",
        },
    ):
        code = plugin.run(
            [
                "--namespace",
                "Custom/Application",
                "--metric",
                "CustomMetric",
                "--dimensions",
                "Environment=Production,Application=WebApp",
                "--warning",
                "75",
                "--critical",
                "90",
            ]
        )
        assert code == Status.OK.value


def test_cloudwatch_missing_dimension() -> None:
    """Test error when required dimension is missing."""
    plugin = CheckAwsCloudwatch()
    code = plugin.run(
        [
            "--namespace",
            "AWS/EC2",
            "--metric",
            "CPUUtilization",
            # Missing --instance-id
        ]
    )
    assert code == Status.UNKNOWN.value


def test_cloudwatch_no_data() -> None:
    """Test handling when no data is available."""
    plugin = CheckAwsCloudwatch()
    with patch(
        "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
        side_effect=RuntimeError("No data available for AWS/EC2/CPUUtilization"),
    ):
        code = plugin.run(
            [
                "--namespace",
                "AWS/EC2",
                "--metric",
                "CPUUtilization",
                "--instance-id",
                "i-1234567890abcdef0",
            ]
        )
        assert code == Status.UNKNOWN.value


def test_cloudwatch_different_statistics() -> None:
    """Test different statistics types."""
    plugin = CheckAwsCloudwatch()
    for statistic in ["Maximum", "Minimum", "Sum", "SampleCount"]:
        with patch(
            "nagios_plugins.plugins.check_aws_cloudwatch.get_metric_statistics",
            return_value={
                "value": 100.0,
                "timestamp": "2024-01-01T12:00:00+00:00",
                "unit": "None",
            },
        ):
            code = plugin.run(
                [
                    "--namespace",
                    "AWS/EC2",
                    "--metric",
                    "NetworkIn",
                    "--instance-id",
                    "i-1234567890abcdef0",
                    "--statistic",
                    statistic,
                ]
            )
            assert code == Status.OK.value
