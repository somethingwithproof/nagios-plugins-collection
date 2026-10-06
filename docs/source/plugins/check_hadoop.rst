check_hadoop
============

Run ``check_hadoop --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_hadoop
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_hadoop [-h] --url URL [--max-update-minutes MAX_UPDATE_MINUTES]
                       [--timeout TIMEOUT] [--json] [--verbose]

   Check Hadoop cluster health

   options:
     -h, --help            show this help message and exit
     --url URL             URL to the Hadoop cluster status API (default: None)
     --max-update-minutes MAX_UPDATE_MINUTES
                           Maximum allowed minutes since last component update
                           (default: None)
     --timeout TIMEOUT     HTTP request timeout in seconds (default: 30)
     --json                Output in JSON format (default: False)
     --verbose             Increase verbosity (can be used multiple times)
                           (default: 0)
