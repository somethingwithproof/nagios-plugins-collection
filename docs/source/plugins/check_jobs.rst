check_jobs
==========

Run ``check_jobs --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_jobs
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_jobs [-h] --url URL [--timeout TIMEOUT] [--json] [--verbose]

   Check job statuses

   options:
     -h, --help         show this help message and exit
     --url URL          URL to the jobs status API (default: None)
     --timeout TIMEOUT  HTTP request timeout in seconds (default: 30)
     --json             Output in JSON format (default: False)
     --verbose          Increase verbosity (can be used multiple times) (default:
                        0)
