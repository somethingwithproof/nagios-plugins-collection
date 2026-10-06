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

   usage: check_ro_mounts [-h] [--host HOST] [--ssh-user SSH_USER]
                          [--ssh-port SSH_PORT] [--exclude EXCLUDE]
                          [--timeout TIMEOUT] [--json] [--verbose]

   Check for read-only mounts

   options:
     -h, --help           show this help message and exit
     --host HOST          Remote host to check (None for local) (default: None)
     --ssh-user SSH_USER  SSH username (default: None)
     --ssh-port SSH_PORT  SSH port (default: 22)
     --exclude EXCLUDE    Comma-separated list of mount points to exclude
                          (default: None)
     --timeout TIMEOUT    Command timeout in seconds (default: 30)
     --json               Output in JSON format (default: False)
     --verbose            Increase verbosity (can be used multiple times)
                          (default: 0)
