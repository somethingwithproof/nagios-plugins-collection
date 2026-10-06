.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_log_errors
================

Run ``check_log_errors --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_log_errors
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_log_errors [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                           [--json] --endpoint ENDPOINT --index INDEX
                           [--minutes MINUTES] [--query QUERY]
                           [--ca-file CA_FILE]

   Search ES/OS for error logs in the last N minutes and threshold count/rate.

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
     --endpoint ENDPOINT   ES/OpenSearch endpoint
     --index INDEX         Index or alias
     --minutes MINUTES
     --query QUERY
     --ca-file CA_FILE     PEM CA bundle; defaults to system trust
