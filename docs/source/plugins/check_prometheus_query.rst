check_prometheus_query
======================

Run ``check_prometheus_query --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_prometheus_query
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_prometheus_query [-h] [-v] [-t TIMEOUT] [-w WARNING]
                                 [-c CRITICAL] [--json] --server SERVER --query
                                 QUERY [--ca-file CA_FILE]

   Run a PromQL query and threshold the scalar value.

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
     --server SERVER       Prometheus base URL
     --query QUERY         PromQL query returning a scalar
     --ca-file CA_FILE     PEM CA bundle; defaults to system trust
