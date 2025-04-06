"""Sphinx configuration for nagios-plugins-collection documentation."""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath("../../src"))

# Project information
project = "Nagios Plugins Collection"
copyright_str = "2025, Thomas Vincent"  # Using copyright_str to avoid redefining built-in
author = "Thomas Vincent"
version = "1.0.0"
release = "1.0.0"

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
exclude_patterns = []

# HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = "Nagios Plugins Collection Documentation"
html_logo = None
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

# Todo extension settings
todo_include_todos = True
