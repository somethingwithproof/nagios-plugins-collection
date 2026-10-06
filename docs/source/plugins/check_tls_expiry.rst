.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_tls_expiry
================

Run ``check_tls_expiry --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_tls_expiry
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_tls_expiry [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                           [--json] --host HOST [--port PORT]

   Check TLS certificate expiry and basic chain details.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds (default: 30)
     -w WARNING, --warning WARNING
                           Warning threshold (plugin-specific)
     -c CRITICAL, --critical CRITICAL
                           Critical threshold (plugin-specific)
     --json                Output results in JSON format
     --host HOST           Hostname to check
     --port PORT           Port to connect to
