"""AWS CloudWatch metrics service module."""

from __future__ import annotations

import datetime as dt


def get_metric_statistics(
    namespace: str,
    metric_name: str,
    dimensions: list[dict[str, str]],
    statistic: str = "Average",
    period: int = 300,
    minutes_back: int = 5,
    region: str | None = None,
    timeout: int = 10,
) -> dict[str, float | str]:
    """Get CloudWatch metric statistics.

    Args:
        namespace: AWS service namespace (e.g., AWS/EC2, AWS/RDS, AWS/Lambda)
        metric_name: Name of the metric to retrieve
        dimensions: List of dimension dicts with Name and Value keys
        statistic: Statistic type (Average, Sum, Maximum, Minimum, SampleCount)
        period: Period in seconds for the metric (default 300 = 5 minutes)
        minutes_back: How many minutes back to query (default 5)
        region: AWS region name
        timeout: Request timeout in seconds

    Returns:
        Dictionary with metric value and timestamp

    Raises:
        RuntimeError: If boto3 is not installed or no data is available
    """
    try:
        import boto3  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("boto3 extra not installed") from e

    cloudwatch = boto3.client(
        "cloudwatch",
        region_name=region,
        config=boto3.session.Config(connect_timeout=timeout, read_timeout=timeout),
    )  # type: ignore

    end_time = dt.datetime.now(dt.timezone.utc)
    start_time = end_time - dt.timedelta(minutes=minutes_back)

    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic],
    )

    datapoints = response.get("Datapoints", [])
    if not datapoints:
        raise RuntimeError(f"No data available for {namespace}/{metric_name}")

    # Get the most recent datapoint
    latest = max(datapoints, key=lambda x: x["Timestamp"])
    value = latest.get(statistic, 0.0)

    return {
        "value": float(value),
        "timestamp": latest["Timestamp"].isoformat(),
        "unit": latest.get("Unit", "None"),
    }
