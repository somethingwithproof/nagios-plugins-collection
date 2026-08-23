"""Tests for the plugins package export list."""

import importlib

from nagios_plugins import plugins


def test_all_names_are_importable() -> None:
    """Every name in __all__ must resolve, or `import *` raises at runtime."""
    for name in plugins.__all__:
        importlib.import_module(f"nagios_plugins.plugins.{name}")
