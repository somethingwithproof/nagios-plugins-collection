# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Keep release matrices and retirement gates consistent with maintained platforms."""

import importlib.util
import json
import tomllib
from datetime import date
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "platform_support", ROOT / "scripts/check_platform_support.py"
)
assert spec is not None
assert spec.loader is not None
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)


def test_release_platforms_are_currently_maintained() -> None:
    support.validate_policy(date.today())


def test_expired_platform_prevents_release() -> None:
    expired_date = date(2031, 1, 1)
    with pytest.raises(ValueError, match="Retire"):
        support.validate_policy(expired_date)


def test_python_ci_and_package_metadata_match_support_policy() -> None:
    policy = json.loads((ROOT / "packaging/platform-support.json").read_text())
    workflow = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text())
    matrix = workflow["jobs"]["test"]["strategy"]["matrix"]["python-version"]
    assert set(map(str, matrix)) == set(policy["python"])
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert project["requires-python"] == ">=3.11,<3.15"
