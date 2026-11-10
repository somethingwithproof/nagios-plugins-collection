# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Read PostgreSQL replication lag using a database connection."""

from __future__ import annotations

from nagios_plugins.redaction import register_secret


def replication_lag_seconds(dsn: str, timeout: int = 10) -> float | None:
    """Return the largest standby lag in seconds, or None when no standby is connected.

    A connected standby with NULL lag columns is caught up and idle, so it reports 0.
    """
    register_secret(dsn)
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
            if not row:
                return None
            return 0.0 if row[0] is None else float(row[0])
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"postgres error: {e}") from e
