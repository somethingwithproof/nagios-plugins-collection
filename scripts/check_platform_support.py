#!/usr/bin/env python3
"""Prevent CI and release publication after a supported platform retires."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


def validate_policy(today: date) -> None:
    """Require every declared platform to remain inside its maintenance window."""
    root = Path(__file__).resolve().parents[1]
    policy = json.loads((root / "packaging/platform-support.json").read_text())
    for category in ("python", "native_packages", "kubernetes"):
        for version, retirement in policy[category].items():
            if today >= date.fromisoformat(retirement):
                raise ValueError(f"Retire {category} {version}: support window ended {retirement}")


if __name__ == "__main__":
    validate_policy(date.today())
    print("All declared release platforms are maintained")
