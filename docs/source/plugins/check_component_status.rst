.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_component_status
======================

Run ``check_component_status --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_component_status
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_component_status [-h] [-v] [-t TIMEOUT] [-w WARNING]
                                 [-c CRITICAL] [--json] --url URL --components
                                 COMPONENTS [COMPONENTS ...]

   Check component status and update freshness via a JSON API.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 10);
                           the plugin exits UNKNOWN 1 second after it
     -w WARNING, --warning WARNING
                           Warning threshold in minutes for stale updates
                           (default: 10)
     -c CRITICAL, --critical CRITICAL
                           Critical threshold in minutes for stale updates
                           (default: 2x warning)
     --json                Output results in JSON format
     --url URL             URL of the API endpoint (without protocol)
     --components COMPONENTS [COMPONENTS ...]
                           List of component names to check
