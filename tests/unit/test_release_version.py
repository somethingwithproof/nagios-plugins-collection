# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Reject ambiguous versions before release workflows can publish packages."""

import gzip
import importlib.util
import json
import re
import subprocess
import tarfile
import tomllib
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
    _contrib(tmp_path, "check_example")
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
    export, locked_install = installs[0], installs[1]
    assert export[1:3] == ["export", "--locked"]
    assert "--no-emit-package=psycopg-binary" in export
    requirements = export[export.index("--output-file") + 1]
    assert locked_install[locked_install.index("-r") + 1] == requirements
    assert "--require-hashes" in locked_install
    assert locked_install[locked_install.index("--abi") + 1] == "cp312"
    assert locked_install[locked_install.index("--python-version") + 1] == "3.12"
    share = payload / "usr/share/nagios-plugins-collection"
    assert (share / "icinga2/nagios-plugins-collection.conf").read_text() == "icinga\n"
    assert (share / "nagios/nagios-plugins-collection.cfg").read_text() == "nagios\n"
    page = payload / "usr/share/man/man1/check_example.1.gz"
    assert gzip.decompress(page.read_bytes()) == b".TH CHECK_EXAMPLE 1\n"
    # No timestamp or name in the gzip header, so rebuilt packages are identical.
    assert page.read_bytes()[4:8] == b"\0\0\0\0"
    paths = {item["dst"] for item in release.package_contents(payload)}
    assert "/usr/share/man/man1/check_example.1.gz" in paths
    assert not {"/usr/share/man", "/usr/share/man/man1"} & paths


def _contrib(root: Path, *commands: str) -> None:
    for name, text in (("icinga2", "icinga"), ("nagios", "nagios")):
        target = root / "contrib" / name
        target.mkdir(parents=True)
        suffix = "conf" if name == "icinga2" else "cfg"
        (target / f"nagios-plugins-collection.{suffix}").write_text(f"{text}\n")
    manuals = root / "contrib/man/man1"
    manuals.mkdir(parents=True)
    for command in commands:
        (manuals / f"{command}.1").write_text(f".TH {command.upper()} 1\n")


def test_native_payload_requires_a_man_page_per_command(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(release, "ROOT", tmp_path)
    _contrib(tmp_path)
    with pytest.raises(ValueError, match="man page for check_example"):
        release.monitoring_config(tmp_path / "payload", {"check_example": "x:main"})


def test_monitoring_archive_is_reproducible(tmp_path: Path) -> None:
    _contrib(tmp_path, "check_example")
    first, second = tmp_path / "a.tar.gz", tmp_path / "b.tar.gz"
    release.stable_archive(tmp_path / "contrib", "config-1.0.0", first, 1_700_000_000)
    release.stable_archive(tmp_path / "contrib", "config-1.0.0", second, 1_700_000_000)
    assert first.read_bytes() == second.read_bytes()
    with tarfile.open(first) as archive:
        members = {member.name: member for member in archive.getmembers()}
    assert "config-1.0.0/man/man1/check_example.1" in members
    assert {(m.uid, m.uname, m.mtime) for m in members.values()} == {(0, "root", 1_700_000_000)}


ROOT = Path(__file__).resolve().parents[2]
#: Files that may name the current version as history rather than as a copy.
HISTORY = {"CHANGELOG.md", "MIGRATION.md", "docs/source/changelog.rst"}
#: Copies Release Please updates through its python strategy or the manifest.
STRATEGY_FILES = {"pyproject.toml", "uv.lock", ".release-please-manifest.json"}


def _release_please_files() -> set[str]:
    config = json.loads((ROOT / "release-please-config.json").read_text())
    entries = config["packages"]["."]["extra-files"]
    return {entry if isinstance(entry, str) else entry["path"] for entry in entries}


def _bumped_lines(text: str) -> set[int]:
    """Return the line numbers the generic updater rewrites (annotated or in a block)."""
    bumped, inside = set(), False
    for number, line in enumerate(text.splitlines(), 1):
        if "x-release-please-start-version" in line:
            inside = True
        elif "x-release-please-end" in line:
            inside = False
        elif inside or "x-release-please-version" in line:
            bumped.add(number)
    return bumped


def _tracked_files() -> list[str]:
    if not (ROOT / ".git").exists():
        pytest.skip("needs a git checkout")
    listed = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True, text=True
    )
    return [name for name in listed.stdout.split("\0") if name]


def test_release_please_updates_every_copy_of_the_version() -> None:
    """A hard-coded version Release Please does not bump would go stale at release."""
    version = release.declared_version()
    pattern = re.compile(rf"(?<![\d.]){re.escape(version)}(?![\d])")
    managed = _release_please_files()
    stale = []
    for name in _tracked_files():
        if name in HISTORY or name in STRATEGY_FILES:
            continue
        path = ROOT / name
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
            continue
        bumped = _bumped_lines(text) if name in managed else set()
        stale += [
            f"{name}:{number}"
            for number, line in enumerate(text.splitlines(), 1)
            if pattern.search(line) and number not in bumped
        ]
    assert not stale, f"version {version} is hard-coded outside Release Please: {stale}"


def test_release_please_files_and_lock_agree_with_the_source_version() -> None:
    version = release.declared_version()
    manifest = json.loads((ROOT / ".release-please-manifest.json").read_text())
    assert manifest == {".": version}
    lock = tomllib.loads((ROOT / "uv.lock").read_text())
    (project,) = [p for p in lock["package"] if p["name"] == "nagios-plugins-collection"]
    assert project["version"] == version
    for name in _release_please_files() - {"uv.lock"}:
        text = (ROOT / name).read_text(encoding="utf-8")
        lines = text.splitlines()
        versions = {
            found
            for number in _bumped_lines(text)
            for found in re.findall(r"\d+\.\d+\.\d+", lines[number - 1])
        }
        # The generic updater rewrites every x.y.z in those lines, so any other
        # version there would be overwritten too.
        assert versions == {version}, f"{name} bumps {versions}, expected {version}"


@pytest.mark.parametrize("prefix", ["../escape", "a/b", "", ".hidden", "x\\y"])
def test_archive_prefix_must_be_one_safe_component(tmp_path: Path, prefix: str) -> None:
    (tmp_path / "source").mkdir()
    with pytest.raises(ValueError, match="one safe path component"):
        release.stable_archive(tmp_path / "source", prefix, tmp_path / "out.tar.gz", 0)
