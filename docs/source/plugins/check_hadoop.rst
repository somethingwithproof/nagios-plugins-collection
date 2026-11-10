.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_hadoop
============

Run ``check_hadoop --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_hadoop
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_hadoop [-h] [-v] [-t TIMEOUT] [--json] --url URL
                       [--max-update-minutes MAX_UPDATE_MINUTES]

   Check Hadoop cluster health.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds (default: 30)
     --json                Output results in JSON format
     --url URL             URL to the Hadoop cluster status API
     --max-update-minutes MAX_UPDATE_MINUTES
                           Maximum allowed minutes since last component update
