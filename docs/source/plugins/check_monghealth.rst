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
                           [--port PORT] [--ssl] [--mode {1,2,3}]
                           [--ca-file PATH] [--insecure] [--client-cert PATH]
                           [--client-key PATH] [--max-response-bytes BYTES]
                           [--retries RETRIES] [--retry-delay SECONDS]
                           [--username USERNAME]
                           [--password PASSWORD | --password-file PATH]
                           [--bearer-token BEARER_TOKEN | --bearer-token-file PATH]
                           [--api-key API_KEY | --api-key-file PATH]
                           [--api-key-header NAME]

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
     --ssl                 Use SSL
     --mode {1,2,3}        Check mode (1: basic, 2: extended, 3: full; default:
                           1)
     --max-response-bytes BYTES
                           Largest response body read, after decompression; a
                           larger one is UNKNOWN (default: 10485760)

   TLS:
     --ca-file PATH        PEM CA bundle (default: the bundled Mozilla CA store
                           or $SSL_CERT_FILE)
     --insecure            Do not verify TLS certificates or hostnames (for
                           testing; prefer --ca-file)
     --client-cert PATH    PEM client certificate for mutual TLS
     --client-key PATH     PEM private key for --client-cert (when not in the
                           same file)

   HTTP retries:
     --retries RETRIES     Retries for transient failures within --timeout
                           (default: 2)
     --retry-delay SECONDS
                           First retry pause, doubled for each retry (default:
                           0.5)

   HTTP authentication:
     --username USERNAME   User name for HTTP basic authentication
     --password PASSWORD   password for HTTP basic authentication (visible in the
                           process list; prefer --password-file or
                           $CHECK_MONGHEALTH_PASSWORD)
     --password-file PATH  Read password for HTTP basic authentication from PATH
                           (or the file named by $CHECK_MONGHEALTH_PASSWORD_FILE)
     --bearer-token BEARER_TOKEN
                           bearer token sent in the Authorization header (visible
                           in the process list; prefer --bearer-token-file or
                           $CHECK_MONGHEALTH_BEARER_TOKEN)
     --bearer-token-file PATH
                           Read bearer token sent in the Authorization header
                           from PATH (or the file named by
                           $CHECK_MONGHEALTH_BEARER_TOKEN_FILE)
     --api-key API_KEY     API key sent in the --api-key-header header (visible
                           in the process list; prefer --api-key-file or
                           $CHECK_MONGHEALTH_API_KEY)
     --api-key-file PATH   Read API key sent in the --api-key-header header from
                           PATH (or the file named by
                           $CHECK_MONGHEALTH_API_KEY_FILE)
     --api-key-header NAME
                           Header that carries --api-key (default: X-API-Key)
