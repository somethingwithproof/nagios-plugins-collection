#!/usr/bin/env python3
"""Audit the actual locked runtime distributions against a reviewed license policy."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[1]


def normalize_name(name: str) -> str:
    """Compare distribution names using the standard PyPI normalization."""
    return re.sub(r"[-_.]+", "-", name).lower()


def runtime_distributions() -> list[str]:
    """Select requirements whose markers apply to the current audit environment."""
    names = []
    for line in (ROOT / "packaging/container-requirements.txt").read_text().splitlines():
        if not re.match(r"[A-Za-z\d_.-]+==", line):
            continue
        requirement = Requirement(line.rstrip("\\ "))
        if requirement.marker is None or requirement.marker.evaluate():
            names.append(normalize_name(requirement.name))
    return sorted(set(names))


def approved_license(name: str, label: str, policy: dict[str, Any]) -> bool:
    """Require every license component to be approved, with named client exceptions."""
    approved = set(policy["allowed"])
    approved.update(policy["exceptions"].get(normalize_name(name), {}).get("licenses", []))
    labels = set()
    for expression in label.split(";"):
        component: list[str] = []
        for word in expression.split():
            if word in {"OR", "AND"}:
                labels.add(" ".join(component))
                component = []
            else:
                component.append(word)
        labels.add(" ".join(component))
    return bool(label.strip()) and labels <= approved


def main() -> None:
    """Generate license evidence for shipping clients and fail on unknown licenses."""
    names = runtime_distributions()
    result = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "piplicenses",
            "--format=json",
            "--with-urls",
            "--with-license-file",
            "--packages",
            *names,
        ],
        text=True,
    )
    report = ROOT / "dist/licenses.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(result)
    records = json.loads(result)
    found = {normalize_name(record["Name"]) for record in records}
    if missing := set(names) - found:
        raise ValueError(f"Missing runtime license metadata: {sorted(missing)}")
    policy = json.loads((ROOT / "packaging/license-policy.json").read_text())
    rejected = [
        (record["Name"], record["License"])
        for record in records
        if not approved_license(record["Name"], record["License"], policy)
    ]
    if rejected:
        raise ValueError(f"Unreviewed runtime licenses: {rejected}")
    print(f"Reviewed licenses for all {len(records)} locked runtime distributions")


if __name__ == "__main__":
    main()
