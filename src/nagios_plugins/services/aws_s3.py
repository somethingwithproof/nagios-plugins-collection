from __future__ import annotations

import datetime as dt


def latest_object_age_seconds(
    bucket: str, prefix: str = "", region: str | None = None, timeout: int = 10
) -> int:
    try:
        import boto3  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("boto3 extra not installed") from e

    s3 = boto3.client(
        "s3",
        region_name=region,
        config=boto3.session.Config(connect_timeout=timeout, read_timeout=timeout),
    )  # type: ignore
    paginator = s3.get_paginator("list_objects_v2")
    latest: dt.datetime | None = None
    for page in paginator.paginate(
        Bucket=bucket, Prefix=prefix, PaginationConfig={"PageSize": 1000}
    ):
        for obj in page.get("Contents", []) or []:
            lm = obj["LastModified"]
            if latest is None or lm > latest:
                latest = lm
    if latest is None:
        raise RuntimeError("No objects found")
    now = dt.datetime.now(dt.UTC)
    return int((now - latest).total_seconds())
