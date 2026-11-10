# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Every external base image is pinned by digest; Dependabot keeps the pins current."""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
DOCKERFILES = sorted((ROOT / "docker").rglob("Dockerfile"))
_FROM = re.compile(
    r"^FROM\s+(?:--platform=\S+\s+)?(?P<image>\S+)(?:\s+AS\s+(?P<stage>\S+))?", re.I | re.M
)
_DIGEST = re.compile(r"^[^@\s]+:[^@\s]+@sha256:[0-9a-f]{64}$")


def _external_images(path: Path) -> list[str]:
    stages: set[str] = set()
    images = []
    for match in _FROM.finditer(path.read_text(encoding="utf-8")):
        if match["image"].lower() not in stages:
            images.append(match["image"])
        if match["stage"]:
            stages.add(match["stage"].lower())
    return images


def test_dockerfiles_are_found() -> None:
    assert ROOT / "docker/Dockerfile" in DOCKERFILES


@pytest.mark.parametrize("path", DOCKERFILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_base_images_are_pinned_by_tag_and_digest(path: Path) -> None:
    images = _external_images(path)
    assert images
    for image in images:
        assert _DIGEST.match(image), f"{path.relative_to(ROOT)}: {image} is not digest-pinned"


def test_dependabot_updates_every_dockerfile_directory() -> None:
    config = yaml.safe_load((ROOT / ".github/dependabot.yml").read_text(encoding="utf-8"))
    directories = {
        directory
        for update in config["updates"]
        if update["package-ecosystem"] == "docker"
        for directory in update.get("directories", [update.get("directory")])
    }
    for path in DOCKERFILES:
        assert "/" + str(path.parent.relative_to(ROOT)) in directories
