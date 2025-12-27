#!/usr/bin/env python3
"""
Deprecated plugin framework shim.

This module is deprecated and kept only for backward compatibility. New plugins
should derive from nagios_plugins.base.NagiosPlugin. Importing this module will
emit a DeprecationWarning.
"""

from __future__ import annotations

import warnings
from typing import Any

# Expose commonly referenced symbols for minimal compatibility
from nagios_plugins.base import CheckResult, Status  # re-export

warnings.warn(
    "nagios_plugins.plugin_framework is deprecated; use nagios_plugins.base.NagiosPlugin",
    DeprecationWarning,
    stacklevel=2,
)


class NagiosPluginFramework:  # pragma: no cover - compatibility shim
    """Deprecated compatibility class.

    This class exists to avoid breaking imports in legacy code. It does not
    provide any functionality. Please migrate to nagios_plugins.base.NagiosPlugin.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        warnings.warn(
            "NagiosPluginFramework is deprecated; migrate to base.NagiosPlugin",
            DeprecationWarning,
            stacklevel=2,
        )
        # No-op


__all__ = ["CheckResult", "Status", "NagiosPluginFramework"]
