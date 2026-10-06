# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Nagios Plugins Collection.

A collection of enterprise-grade Nagios plugins for monitoring various systems.
"""

from __future__ import annotations

try:  # Prefer installed package version when available
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _pkg_version

    try:
        __version__ = _pkg_version("nagios-plugins-collection")
    except PackageNotFoundError:  # e.g. editable installs, docs builds
        __version__ = "0.0.0"
except Exception:  # pragma: no cover - very defensive
    __version__ = "0.0.0"
