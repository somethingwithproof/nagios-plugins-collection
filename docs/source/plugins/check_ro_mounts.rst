.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_ro_mounts
===============

Run ``check_ro_mounts --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_ro_mounts
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_ro_mounts [-h] [-v] [-t TIMEOUT] [--json] [--host HOST]
                          [--ssh-user SSH_USER] [--ssh-port SSH_PORT]
                          [--exclude EXCLUDE]

   Check for read-only mounts.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 30);
                           the plugin exits UNKNOWN 1 second after it
     --json                Output results in JSON format
     --host HOST           Remote host to check over SSH (default: local)
     --ssh-user SSH_USER   SSH username
     --ssh-port SSH_PORT   SSH port (default: 22)
     --exclude EXCLUDE     Comma-separated list of mount points to exclude
