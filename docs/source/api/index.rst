.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

API Reference
=============

This section provides detailed API documentation for the Nagios Plugins Collection.

Base Module
-----------

The :mod:`nagios_plugins.base` module provides the foundation for all Nagios plugins in the collection. It includes the base classes and utilities that ensure consistent behavior across all plugins.

.. automodule:: nagios_plugins.base
   :members:
   :undoc-members:
   :show-inheritance:

Deadline Module
---------------

The :mod:`nagios_plugins.deadline` module ends a run that outlives its
``--timeout`` and kills the child processes it started.

.. automodule:: nagios_plugins.deadline
   :members:
   :show-inheritance:

Utils Module
------------

The :mod:`nagios_plugins.utils` module provides utility functions that are used by multiple plugins.

.. automodule:: nagios_plugins.utils
   :members:
   :undoc-members:
   :show-inheritance:
