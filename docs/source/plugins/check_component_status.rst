check_component_status
======================

Run ``check_component_status --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_component_status
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_component_status [-h] --url URL --components COMPONENTS
                                 [COMPONENTS ...] [--warning WARNING]
                                 [--critical CRITICAL] [--timeout TIMEOUT]
                                 [--json] [--verbose]

   Check component status via JSON API

   options:
     -h, --help            show this help message and exit
     --url URL             URL of the API endpoint (without protocol) (default:
                           None)
     --components COMPONENTS [COMPONENTS ...]
                           List of component names to check (default: None)
     --warning WARNING     Warning threshold in minutes for stale updates
                           (default: 10)
     --critical CRITICAL   Critical threshold in minutes for stale updates
                           (default: 2x warning) (default: None)
     --timeout TIMEOUT     Request timeout in seconds (default: 10)
     --json                Output in JSON format (default: False)
     --verbose             Increase verbosity (can be used multiple times)
                           (default: 0)
