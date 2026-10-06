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

   usage: check_mongodb_health [-h] --url URL [--mode {1,2,3}]
                               [--timeout TIMEOUT] [--json] [--verbose]

   Check MongoDB health status

   options:
     -h, --help         show this help message and exit
     --url URL          URL of the MongoDB health endpoint (default: None)
     --mode {1,2,3}     Check mode: 1=Migrations+Search, 2=Search+API,
                        3=Migrations+Search (default: 1)
     --timeout TIMEOUT  Request timeout in seconds (default: 10)
     --json             Output in JSON format (default: False)
     --verbose          Increase verbosity (can be used multiple times) (default:
                        0)
