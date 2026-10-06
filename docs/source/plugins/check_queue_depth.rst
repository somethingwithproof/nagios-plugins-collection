check_queue_depth
=================

Run ``check_queue_depth --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_queue_depth
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_queue_depth [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                            [--json] --queue-url QUEUE_URL [--region REGION]

   Monitor the backlog and in-flight messages of an SQS queue.

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
     --queue-url QUEUE_URL
     --region REGION
