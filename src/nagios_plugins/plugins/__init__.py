# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Nagios Plugins Collection.

Each module is one installed command implemented as a
:class:`nagios_plugins.base.NagiosPlugin` subclass, so every command shares the
same options, exit codes, logging and output format. ``pyproject.toml`` lists
the commands.
"""

# The plugins ship with, and are versioned as, the package.
from nagios_plugins import __version__ as __version__

# List all standardized plugins here for easy import and discovery
__all__ = [
    "check_component_status",
    "check_mongodb_health",
    "check_website_status",
    "check_ro_mounts",
    "check_monghealth",
    "check_hadoop",
    "check_jobs",
    "check_dig",
]
