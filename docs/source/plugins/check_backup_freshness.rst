check_backup_freshness
======================

Run ``check_backup_freshness --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_backup_freshness
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_backup_freshness [-h] [-v] [-t TIMEOUT] [-w WARNING]
                                 [-c CRITICAL] [--json] --bucket BUCKET
                                 [--prefix PREFIX] [--region REGION]

   Monitor the age of the latest backup object in S3.

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
     --bucket BUCKET
     --prefix PREFIX
     --region REGION
