"""Require named LGPL exceptions and reject unknown licenses in mixed expressions."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("license_policy", ROOT / "scripts/check_licenses.py")
assert spec is not None
assert spec.loader is not None
licenses = importlib.util.module_from_spec(spec)
spec.loader.exec_module(licenses)
policy = json.loads((ROOT / "packaging/license-policy.json").read_text())


def test_client_exception_is_scoped_to_its_distribution() -> None:
    assert licenses.approved_license("psycopg", "LGPL-3.0-only", policy)
    assert not licenses.approved_license("unreviewed-client", "LGPL-3.0-only", policy)


def test_mixed_license_requires_every_component_to_be_reviewed() -> None:
    assert licenses.approved_license("client", "Apache-2.0 OR BSD-3-Clause", policy)
    assert not licenses.approved_license("client", "MIT AND GPL-3.0-only", policy)


def test_missing_license_is_rejected() -> None:
    assert not licenses.approved_license("client", "", policy)
