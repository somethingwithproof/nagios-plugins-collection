# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Read PostgreSQL replication lag using a database connection."""

from __future__ import annotations


def replication_lag_seconds(dsn: str, timeout: int = 10) -> float:
    """Return seconds since the last replayed PostgreSQL transaction."""
    try:
        import psycopg  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("psycopg extra not installed") from e

    try:
        with psycopg.connect(dsn, connect_timeout=timeout) as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT EXTRACT(EPOCH FROM COALESCE(replay_lag, flush_lag, write_lag))
                FROM pg_stat_replication
                ORDER BY COALESCE(replay_lag, flush_lag, write_lag) DESC NULLS LAST
                LIMIT 1
                """
            )
            row = cur.fetchone()
            if not row or row[0] is None:
                return 0.0
            return float(row[0])
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"postgres error: {e}") from e
