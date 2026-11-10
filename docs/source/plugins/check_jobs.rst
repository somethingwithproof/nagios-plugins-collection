.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_jobs
==========

Run ``check_jobs --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_jobs
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_jobs [-h] [-v] [-t TIMEOUT] [--json] --url URL

   Check job statuses.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds (default: 30)
     --json                Output results in JSON format
     --url URL             URL to the jobs status API
