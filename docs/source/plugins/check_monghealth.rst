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

   usage: check_monghealth [-h] [-v] [-t TIMEOUT] [--json] --host HOST
                           [--port PORT] [--username USERNAME]
                           [--password PASSWORD | --password-file PATH] [--ssl]
                           [--mode {1,2,3}]

   Check MongoDB health.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 5); the
                           plugin exits UNKNOWN 1 second after it
     --json                Output results in JSON format
     --host HOST           MongoDB host
     --port PORT           MongoDB port (default: 27017)
     --username USERNAME   MongoDB username
     --password PASSWORD   MongoDB password (visible in the process list; prefer
                           --password-file or $CHECK_MONGHEALTH_PASSWORD)
     --password-file PATH  Read MongoDB password from PATH
     --ssl                 Use SSL
     --mode {1,2,3}        Check mode (1: basic, 2: extended, 3: full; default:
                           1)
