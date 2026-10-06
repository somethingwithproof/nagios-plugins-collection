.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_monghealth
================

Run ``check_monghealth --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_monghealth
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_monghealth [-h] --host HOST [--port PORT] [--timeout TIMEOUT]
                           [--username USERNAME] [--password PASSWORD] [--ssl]
                           [--mode {1,2,3}] [--json] [--verbose]

   Check MongoDB health

   options:
     -h, --help           show this help message and exit
     --host HOST          MongoDB host (default: None)
     --port PORT          MongoDB port (default: 27017)
     --timeout TIMEOUT    Connection timeout in seconds (default: 5)
     --username USERNAME  MongoDB username (default: None)
     --password PASSWORD  MongoDB password (default: None)
     --ssl                Use SSL (default: False)
     --mode {1,2,3}       Check mode (1: basic, 2: extended, 3: full) (default:
                          1)
     --json               Output in JSON format (default: False)
     --verbose            Increase verbosity (can be used multiple times)
                          (default: 0)
