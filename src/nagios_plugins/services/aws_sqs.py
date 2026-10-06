"""Read SQS queue backlog and in-flight counts."""

from __future__ import annotations


def queue_depth(queue_url: str, region: str | None = None, timeout: int = 10) -> dict[str, int]:
    """Return visible and in-flight message counts for an SQS queue."""
    try:
        import boto3  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("boto3 extra not installed") from e

    sqs = boto3.client(
        "sqs",
        region_name=region,
        config=boto3.session.Config(connect_timeout=timeout, read_timeout=timeout),
    )  # type: ignore
    attrs = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=[
            "ApproximateNumberOfMessages",
            "ApproximateNumberOfMessagesNotVisible",
            "ApproximateNumberOfMessagesDelayed",
        ],
    )["Attributes"]
    return {
        "depth": int(attrs.get("ApproximateNumberOfMessages", 0)),
        "inflight": int(attrs.get("ApproximateNumberOfMessagesNotVisible", 0)),
        "delayed": int(attrs.get("ApproximateNumberOfMessagesDelayed", 0)),
    }
