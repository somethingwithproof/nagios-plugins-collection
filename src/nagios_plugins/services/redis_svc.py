"""Read Redis memory and cache statistics."""

from __future__ import annotations


def get_stats(url: str, timeout: int = 5) -> dict[str, float | int]:
    """Read Redis statistics with the configured connection timeout."""
    try:
        import redis  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("redis extra not installed") from e

    r = redis.from_url(url, socket_timeout=timeout)
    info = r.info()  # type: ignore
    hits = float(info.get("keyspace_hits", 0))
    misses = float(info.get("keyspace_misses", 0))
    total = hits + misses
    hitratio = (hits / total) if total > 0 else 1.0
    return {
        "used_memory": int(info.get("used_memory", 0)),
        "evicted_keys": int(info.get("evicted_keys", 0)),
        "blocked_clients": int(info.get("blocked_clients", 0)),
        "hitratio": hitratio,
    }
