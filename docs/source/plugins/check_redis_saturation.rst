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
                                 [-c CRITICAL] [--json] --url URL

   Monitor Redis memory use, evictions and cache hits.

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
     --url URL             Redis URL e.g. redis://host:6379/0
