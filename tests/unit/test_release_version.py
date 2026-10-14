# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Reject ambiguous versions before release workflows can publish packages."""

import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "release_artifacts", Path(__file__).resolve().parents[2] / "scripts/release_artifacts.py"
)
assert spec is not None
assert spec.loader is not None
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


@pytest.mark.parametrize(
    "version", ["1.2", "01.2.3", "1.2.3-01", "1.2.3-a..b", "1.2.3+..", "1.2.3\n", "v1.2.3"]
)
def test_invalid_release_versions(version: str) -> None:
    with pytest.raises(ValueError):
        release.validate_semver(version)


@pytest.mark.parametrize("version", ["0.1.0", "2.0.0", "2.0.0-rc.1", "2.0.0+build.01"])
def test_complete_semver(version: str) -> None:
    assert release.validate_semver(version) == version


def test_release_must_match_source_version() -> None:
    with pytest.raises(ValueError, match="differs from source"):
        release.resolve_version("999.0.0")


def test_rebuild_does_not_include_stale_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(release, "ROOT", tmp_path)
    output = release.prepare_output("2.0.0")
    (output / "stale.whl").write_text("old source")
    assert release.prepare_output("2.0.0") == output
    assert list(output.iterdir()) == []


def test_release_cleanup_refuses_symlinked_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(release, "ROOT", tmp_path)
    outside = tmp_path / "unrelated"
    outside.mkdir()
    protected = outside / "keep.txt"
    protected.write_text("keep")
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist/release").symlink_to(outside)
    with pytest.raises(ValueError, match="symlinks"):
        release.prepare_output("2.0.0")
    assert protected.read_text() == "keep"


def test_native_payload_preserves_required_python_extensions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(release, "ROOT", tmp_path)
    (tmp_path / "pyproject.toml").write_text(
        '[project.scripts]\ncheck_example = "nagios_plugins.plugins.example:main"\n'
    )
    for name in ("README.md", "LICENSE"):
        (tmp_path / name).write_text("package documentation\n")
    (tmp_path / "docs/source/_static").mkdir(parents=True)
    payload = tmp_path / "payload"
    extension = (
        payload
        / "usr/lib/nagios-plugins-collection/pydantic_core"
        / "_pydantic_core.cpython-312-x86_64-linux-gnu.so"
    )
    installs = []

    def install(command, **kwargs):
        installs.append(command)
        extension.parent.mkdir(parents=True, exist_ok=True)
        extension.write_bytes(b"required native extension")

    monkeypatch.setattr(release.subprocess, "run", install)
    release.python_payload(payload, tmp_path / "project.whl", "deb")

    assert extension.read_bytes() == b"required native extension"
    assert installs[0][installs[0].index("--abi") + 1] == "cp312"
    assert installs[0][installs[0].index("--python-version") + 1] == "3.12"
