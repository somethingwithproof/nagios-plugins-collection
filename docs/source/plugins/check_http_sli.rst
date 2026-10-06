.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_http_sli
==============

Run ``check_http_sli --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_http_sli
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_http_sli [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                         [--json] --url URL [--samples SAMPLES]
                         [--ca-file CA_FILE]

   Probe one or more URLs concurrently and report p50/p95/p99 and error-rate.

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
     --url URL             URL to probe (repeatable)
     --samples SAMPLES     Samples per URL
     --ca-file CA_FILE     PEM CA bundle; defaults to system trust
