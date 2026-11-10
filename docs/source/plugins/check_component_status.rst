.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

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

   usage: check_component_status [-h] [-v] [-t TIMEOUT] [-w WARNING]
                                 [-c CRITICAL] [--json] --url URL --components
                                 COMPONENTS [COMPONENTS ...] [--ca-file PATH]
                                 [--insecure] [--client-cert PATH]
                                 [--client-key PATH] [--retries RETRIES]
                                 [--retry-delay SECONDS] [--username USERNAME]
                                 [--password PASSWORD | --password-file PATH]
                                 [--bearer-token BEARER_TOKEN | --bearer-token-file PATH]
                                 [--api-key API_KEY | --api-key-file PATH]
                                 [--api-key-header NAME]

   Check component status and update freshness via a JSON API.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 10);
                           the plugin exits UNKNOWN 1 second after it
     -w WARNING, --warning WARNING
                           Warning threshold in minutes for stale updates
                           (default: 10)
     -c CRITICAL, --critical CRITICAL
                           Critical threshold in minutes for stale updates
                           (default: 2x warning)
     --json                Output results in JSON format
     --url URL             URL of the API endpoint (without protocol)
     --components COMPONENTS [COMPONENTS ...]
                           List of component names to check

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
                           $CHECK_COMPONENT_STATUS_PASSWORD)
     --password-file PATH  Read password for HTTP basic authentication from PATH
                           (or the file named by
                           $CHECK_COMPONENT_STATUS_PASSWORD_FILE)
     --bearer-token BEARER_TOKEN
                           bearer token sent in the Authorization header (visible
                           in the process list; prefer --bearer-token-file or
                           $CHECK_COMPONENT_STATUS_BEARER_TOKEN)
     --bearer-token-file PATH
                           Read bearer token sent in the Authorization header
                           from PATH (or the file named by
                           $CHECK_COMPONENT_STATUS_BEARER_TOKEN_FILE)
     --api-key API_KEY     API key sent in the --api-key-header header (visible
                           in the process list; prefer --api-key-file or
                           $CHECK_COMPONENT_STATUS_API_KEY)
     --api-key-file PATH   Read API key sent in the --api-key-header header from
                           PATH (or the file named by
                           $CHECK_COMPONENT_STATUS_API_KEY_FILE)
     --api-key-header NAME
                           Header that carries --api-key (default: X-API-Key)
