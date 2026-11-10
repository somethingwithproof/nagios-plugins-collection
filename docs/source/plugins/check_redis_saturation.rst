.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_redis_saturation
======================

Run ``check_redis_saturation --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_redis_saturation
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_redis_saturation [-h] [-v] [-t TIMEOUT] [-w WARNING]
                                 [-c CRITICAL] [--json]
                                 [--url URL | --url-file PATH]
                                 [--blocked-warning RANGE]
                                 [--blocked-critical RANGE]
                                 [--hitratio-warning RANGE]
                                 [--hitratio-critical RANGE]

   Monitor Redis memory saturation, evictions and cache hits.

   -w/-c are Nagios ranges for used_memory as a percentage of maxmemory, a
   gauge that recovers when memory is freed. evicted_keys is a monotonic
   counter since restart, so it is published as perfdata (UOM c) for the
   graphing system to turn into a rate rather than compared with a threshold.
   Blocked clients and the hit ratio alert only when their own ranges are given.

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
     --url URL             Redis URL e.g. redis://:password@host:6379/0 (visible
                           in the process list; prefer --url-file or
                           $CHECK_REDIS_URL)
     --url-file PATH       Read Redis URL e.g. redis://:password@host:6379/0 from
                           PATH
     --blocked-warning RANGE
                           WARNING range for blocked_clients (clients waiting in
                           BLPOP and similar) (default: not checked)
     --blocked-critical RANGE
                           CRITICAL range for blocked_clients (clients waiting in
                           BLPOP and similar) (default: not checked)
     --hitratio-warning RANGE
                           WARNING range for keyspace hit ratio (0-1); for
                           example 0.8: alerts below 0.8 (default: not checked)
     --hitratio-critical RANGE
                           CRITICAL range for keyspace hit ratio (0-1); for
                           example 0.8: alerts below 0.8 (default: not checked)
