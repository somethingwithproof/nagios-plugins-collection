# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Sphinx configuration for nagios-plugins-collection documentation."""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath("../../src"))

# Project information
project = "Nagios Plugins Collection"

# Copyright
copyright_str = "2025, Thomas Vincent"
author = "Thomas Vincent"

# Resolve version dynamically; fall back for in-tree builds without an installed package
try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _pkg_version

    try:
        release = version = _pkg_version("nagios-plugins-collection")
    except PackageNotFoundError:
        release = version = "0.0.0"
except Exception:  # very defensive
    release = version = "0.0.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

# HTML output
html_theme = "sphinx_rtd_theme"
html_static_path: list[str] = ["_static"]
html_title = "Nagios Plugins Collection Documentation"
html_logo = "_static/logo.svg"
html_favicon = None

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Sphinx note rendering
todo_include_todos = True
