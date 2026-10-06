check_oauth2_token
==================

Run ``check_oauth2_token --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_oauth2_token
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_oauth2_token [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                             [--json] --token-url TOKEN_URL --client-id CLIENT_ID
                             --client-secret CLIENT_SECRET [--scope SCOPE]
                             [--ca-file CA_FILE]

   Obtain an OAuth2 token and report time-to-expiry; validate scopes if provided.

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
     --token-url TOKEN_URL
     --client-id CLIENT_ID
     --client-secret CLIENT_SECRET
     --scope SCOPE
     --ca-file CA_FILE     PEM CA bundle; defaults to system trust
