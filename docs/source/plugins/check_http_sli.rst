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
                         [--latency-warning RANGE] [--latency-critical RANGE]
                         [--error-rate-warning RANGE]
                         [--error-rate-critical RANGE] [--ca-file CA_FILE]

   Probe one or more URLs concurrently and report p50/p95/p99 and error-rate.

   Latency and error rate have separate Nagios ranges. -w/-c are aliases for
   --latency-warning/--latency-critical (p95 in milliseconds).

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 30);
                           the plugin exits UNKNOWN 1 second after it
     -w WARNING, --warning WARNING
                           Warning threshold (plugin-specific)
     -c CRITICAL, --critical CRITICAL
                           Critical threshold (plugin-specific)
     --json                Output results in JSON format
     --url URL             URL to probe (repeatable)
     --samples SAMPLES     Samples per URL
     --latency-warning RANGE
                           p95 latency range in ms for WARNING (alias: -w)
     --latency-critical RANGE
                           p95 latency range in ms for CRITICAL (alias: -c)
     --error-rate-warning RANGE
                           Range for the fraction of failed requests (0-1) for
                           WARNING
     --error-rate-critical RANGE
                           Range for the fraction of failed requests (0-1) for
                           CRITICAL
     --ca-file CA_FILE     PEM CA bundle; defaults to system trust
