# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Release provenance is verified against the ref and commit the release was built from."""

import importlib.util
import re
import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
spec = importlib.util.spec_from_file_location(
    "verify_release_provenance", ROOT / "scripts/verify_release_provenance.py"
)
assert spec is not None
assert spec.loader is not None
provenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provenance)

COMMIT = "0123456789abcdef0123456789abcdef01234567"


def _steps(workflow: str, job: str) -> list[dict[str, Any]]:
    data = yaml.safe_load((WORKFLOWS / workflow).read_text(encoding="utf-8"))
    return data["jobs"][job]["steps"]


def _script(workflow: str, job: str, needle: str) -> str:
    (run,) = [step["run"] for step in _steps(workflow, job) if needle in step.get("run", "")]
    return run


def test_release_runs_only_on_the_ref_its_provenance_is_verified_against() -> None:
    """The release build's ref is what the attestations record, not the tag."""
    validate = _script("release.yml", "version", "release_artifacts.py validate")
    (required,) = re.findall(r'test "\$GITHUB_REF" = (\S+)', validate)
    assert required == provenance.RELEASE_REF == "refs/heads/main"


def test_python_publishing_verifies_main_and_the_tagged_commit() -> None:
    script = _script("publish-release.yml", "build", "verify_release_provenance.py")
    assert "refs/tags/" not in script.replace('git rev-parse "refs/tags/', "")
    assert "--source-ref" not in script, "the default must stay the release workflow's ref"
    assert 'commit="$(git rev-parse "refs/tags/v$version^{commit}")"' in script
    assert '--source-commit "$commit"' in script
    assert "gh attestation verify" not in script, "one verification policy, in the script"


def test_release_workflow_verifies_its_own_attestations_before_publishing() -> None:
    steps = _steps("release.yml", "publish")
    names = [step.get("name", step.get("uses", "")) for step in steps]
    attest = next(
        i for i, step in enumerate(steps) if "attest-build-provenance" in step.get("uses", "")
    )
    verify = next(
        i for i, step in enumerate(steps) if "verify_release_provenance" in step.get("run", "")
    )
    publish = names.index("Publish GitHub release")
    assert attest < verify < publish
    assert '--source-ref "$GITHUB_REF" --source-commit "$GITHUB_SHA"' in steps[verify]["run"]
    assert steps[publish]["if"] == "inputs.dry-run != true"


def test_dry_run_publishes_no_image_tag() -> None:
    data = yaml.safe_load((WORKFLOWS / "release.yml").read_text(encoding="utf-8"))
    version = data["jobs"]["checks"]["with"]["release-version"]
    assert version.startswith("${{ inputs.dry-run != true && ")
    assert version.endswith("|| '' }}")


def test_verify_command_binds_workflow_ref_and_commit(tmp_path: Path) -> None:
    wheel = tmp_path / "pkg.whl"
    command = provenance.verify_command(wheel, "o/r", "refs/heads/main", COMMIT)
    assert command[:3] == ["gh", "attestation", "verify"]
    assert command[-2:] == ["--", str(wheel.resolve())]
    options = dict(zip(command[3:-3:2], command[4:-3:2], strict=True))
    assert options["--signer-workflow"] == "o/r/.github/workflows/release.yml"
    assert options["--source-ref"] == "refs/heads/main"
    assert options["--source-digest"] == COMMIT
    assert command[-3] == "--deny-self-hosted-runners"


def test_main_verifies_every_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    files = [tmp_path / "a.whl", tmp_path / "b.tar.gz"]
    for path in files:
        path.write_bytes(b"x")
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    ok: subprocess.CompletedProcess[bytes] = subprocess.CompletedProcess([], 0)
    with patch.object(provenance.subprocess, "run", return_value=ok) as run:
        assert provenance.main(["--source-commit", COMMIT, *map(str, files)]) == 0
    assert [call.args[0][-1] for call in run.call_args_list] == [
        str(path.resolve()) for path in files
    ]
    assert all("refs/heads/main" in call.args[0] for call in run.call_args_list)


def test_main_fails_when_any_file_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "a.whl"
    path.write_bytes(b"x")
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    failed: subprocess.CompletedProcess[bytes] = subprocess.CompletedProcess([], 1)
    with patch.object(provenance.subprocess, "run", return_value=failed):
        assert provenance.main(["--source-commit", COMMIT, str(path)]) == 1


@pytest.mark.parametrize("commit", ["", "v1.2.3", COMMIT[:12], COMMIT.upper()])
def test_main_requires_a_full_commit(
    commit: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "a.whl"
    path.write_bytes(b"x")
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    with patch.object(provenance.subprocess, "run") as run, pytest.raises(SystemExit) as exited:
        provenance.main(["--source-commit", commit, str(path)])
    assert exited.value.code == 2
    run.assert_not_called()


def test_main_rejects_missing_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    with patch.object(provenance.subprocess, "run") as run, pytest.raises(SystemExit):
        provenance.main(["--source-commit", COMMIT, str(tmp_path / "missing.whl")])
    run.assert_not_called()


@pytest.mark.parametrize(
    "option,value",
    [("--source-ref", "--help"), ("--source-ref", "main"), ("--source-ref", "refs/heads/a b")],
)
def test_main_rejects_malformed_refs(
    option: str, value: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "a.whl"
    path.write_bytes(b"x")
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    with patch.object(provenance.subprocess, "run") as run, pytest.raises(SystemExit):
        provenance.main([f"{option}={value}", "--source-commit", COMMIT, str(path)])
    run.assert_not_called()


@pytest.mark.parametrize("repository", ["", "o", "--repo=x/y", "o/r/extra"])
def test_main_requires_a_repository(
    repository: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "a.whl"
    path.write_bytes(b"x")
    monkeypatch.setenv("GITHUB_REPOSITORY", repository)
    with patch.object(provenance.subprocess, "run") as run, pytest.raises(SystemExit):
        provenance.main(["--source-commit", COMMIT, str(path)])
    run.assert_not_called()
