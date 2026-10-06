check_website_status
====================

Run ``check_website_status --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_website_status
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_website_status [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                               [--json] --url URL [--pattern PATTERN]
                               [--method {GET,HEAD,POST}] [--retries RETRIES]
                               [--retry-delay RETRY_DELAY]

   Check website content, status and response time in seconds.

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
     --url URL
     --pattern PATTERN
     --method {GET,HEAD,POST}
     --retries RETRIES
     --retry-delay RETRY_DELAY
