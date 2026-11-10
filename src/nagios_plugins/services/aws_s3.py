# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Read backup object timestamps through the S3 API."""

from __future__ import annotations

import datetime as dt

from nagios_plugins.deadline import remaining_time
from nagios_plugins.services import aws

#: Seconds of ``--timeout`` kept back so a long listing ends with its own error.
LISTING_RESERVE = 1.0


def latest_object_age_seconds(
    bucket: str, prefix: str = "", region: str | None = None, timeout: int = 10
) -> int:
    """Return the age in seconds of the newest object under an S3 prefix.

    S3 lists keys in name order, not by date, so every page under the prefix
    is read; keep ``prefix`` narrow (for example one backup set's folder). The
    newest timestamp is tracked page by page, and when less than
    :data:`LISTING_RESERVE` seconds of the run's ``--timeout`` remain the
    listing stops with an error instead of being cut off. An object dated in
    the future (clock skew between S3 and this host) counts as age 0.

    Raises:
        RuntimeError: No object matched, or the listing did not finish in time.
    """
    s3 = aws.client("s3", region=region, timeout=timeout)
    paginator = s3.get_paginator("list_objects_v2")
    latest: dt.datetime | None = None
    listed = 0
    for page in paginator.paginate(
        Bucket=bucket, Prefix=prefix, PaginationConfig={"PageSize": 1000}
    ):
        for obj in page.get("Contents", []) or []:
            listed += 1
            lm = obj["LastModified"]
            if latest is None or lm > latest:
                latest = lm
        budget = remaining_time()
        if budget is not None and budget < LISTING_RESERVE:
            raise RuntimeError(
                f"Listing s3://{bucket}/{prefix} did not finish within --timeout "
                f"after {listed} objects; use a narrower --prefix"
            )
    if latest is None:
        raise RuntimeError("No objects found")
    now = dt.datetime.now(dt.UTC)
    return max(0, int((now - latest).total_seconds()))
