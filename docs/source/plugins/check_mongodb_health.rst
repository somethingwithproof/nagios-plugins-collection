.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_mongodb_health
====================

Run ``check_mongodb_health --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_mongodb_health
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_mongodb_health [-h] [-v] [-t TIMEOUT] [--json] --url URL
                               [--mode {1,2,3}]

   Check MongoDB health status.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds (default: 10)
     --json                Output results in JSON format
     --url URL             URL of the MongoDB health endpoint
     --mode {1,2,3}        Check mode: 1=Migrations+Search, 2=Search+API,
                           3=Migrations+Search (default: 1)
