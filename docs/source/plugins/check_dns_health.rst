check_dns_health
================

Run ``check_dns_health --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_dns_health
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_dns_health [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                           [--json] --name NAME [--type TYPE] [--server SERVER]
                           [--tcp]

   Check DNS recursion/authoritative responsiveness and TCP fallback (optional dnspython).

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
     --name NAME           Name to resolve
     --type TYPE           Record type
     --server SERVER       DNS server to query
     --tcp                 Force TCP
