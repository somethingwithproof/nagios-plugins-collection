# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Read SQS queue backlog and in-flight counts."""

from __future__ import annotations

from nagios_plugins.services import aws


def queue_depth(queue_url: str, region: str | None = None, timeout: int = 10) -> dict[str, int]:
    """Return visible and in-flight message counts for an SQS queue."""
    sqs = aws.client("sqs", region=region, timeout=timeout)
    attrs = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=[
            "ApproximateNumberOfMessages",
            "ApproximateNumberOfMessagesNotVisible",
            "ApproximateNumberOfMessagesDelayed",
        ],
    )["Attributes"]
    if "ApproximateNumberOfMessages" not in attrs:
        raise RuntimeError("SQS returned no ApproximateNumberOfMessages for the queue")
    try:
        return _depths(attrs)
    except ValueError as error:
        raise RuntimeError(f"SQS returned a non-numeric queue attribute: {error}") from None


def _depths(attrs: dict[str, str]) -> dict[str, int]:
    """Convert the SQS attribute strings; a missing secondary count is zero."""
    return {
        "depth": int(attrs["ApproximateNumberOfMessages"]),
        "inflight": int(attrs.get("ApproximateNumberOfMessagesNotVisible", 0)),
        "delayed": int(attrs.get("ApproximateNumberOfMessagesDelayed", 0)),
    }
