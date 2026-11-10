#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Verify that release files carry build provenance from the Release workflow.

The Release workflow runs on ``refs/heads/main`` (Release Please calls it from
a push to main, and a manual run must start on main), so its attestations
record that ref and the built commit, never the tag. Each file must therefore
be attested by ``.github/workflows/release.yml`` in this repository, on a
GitHub-hosted runner, from ``--source-ref`` at exactly ``--source-commit``.
Callers bind the commit to the release by passing the commit the ``vX.Y.Z``
tag points at.

The Release workflow runs this right after attesting, before it publishes
anything, and the Python publishing workflow runs it on the downloaded
release assets, so both use the same policy. Requires ``gh`` and
``GITHUB_REPOSITORY``.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

#: The workflow that builds and attests release files.
RELEASE_WORKFLOW = ".github/workflows/release.yml"
#: The ref the Release workflow refuses to run on anything but.
RELEASE_REF = "refs/heads/main"
_COMMIT = re.compile(r"[0-9a-f]{40}")
_REPOSITORY = re.compile(r"[A-Za-z0-9-]{1,39}/[A-Za-z0-9._-]{1,100}")
_REF = re.compile(r"refs/(?:heads|tags)/[A-Za-z0-9._/-]{1,200}")


def verify_command(path: Path, repository: str, source_ref: str, commit: str) -> list[str]:
    """Return the ``gh attestation verify`` command for one release file.

    The file is an absolute path after ``--``, so gh can never read it as an option.
    """
    return [
        "gh",
        "attestation",
        "verify",
        "--repo",
        repository,
        "--signer-workflow",
        f"{repository}/{RELEASE_WORKFLOW}",
        "--source-ref",
        source_ref,
        "--source-digest",
        commit,
        "--deny-self-hosted-runners",
        "--",
        str(path.resolve()),
    ]


def main(argv: Sequence[str] | None = None) -> int:
    """Verify every file and return 0 only when all of them pass."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--source-ref",
        default=RELEASE_REF,
        help=f"Git ref the Release workflow ran on (default: {RELEASE_REF})",
    )
    parser.add_argument(
        "--source-commit", required=True, help="Full commit SHA the files were built from"
    )
    parser.add_argument("files", nargs="+", type=Path, help="Release files to verify")
    args = parser.parse_args(argv)
    if not _COMMIT.fullmatch(args.source_commit):
        parser.error(f"--source-commit must be a full 40-character SHA: {args.source_commit!r}")
    if not _REF.fullmatch(args.source_ref):
        parser.error(f"--source-ref must be a branch or tag ref: {args.source_ref!r}")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not _REPOSITORY.fullmatch(repository):
        parser.error("GITHUB_REPOSITORY must name the repository (owner/name)")
    for path in args.files:
        if not path.is_file():
            parser.error(f"not a file: {path}")
        command = verify_command(path, repository, args.source_ref, args.source_commit)
        if subprocess.run(command, check=False).returncode != 0:
            print(f"provenance verification failed: {path}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
