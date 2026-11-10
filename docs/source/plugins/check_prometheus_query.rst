.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

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
                                 QUERY [--ca-file PATH] [--insecure]
                                 [--client-cert PATH] [--client-key PATH]
                                 [--max-response-bytes BYTES] [--retries RETRIES]
                                 [--retry-delay SECONDS] [--username USERNAME]
                                 [--password PASSWORD | --password-file PATH]
                                 [--bearer-token BEARER_TOKEN | --bearer-token-file PATH]
                                 [--api-key API_KEY | --api-key-file PATH]
                                 [--api-key-header NAME]

   Run a PromQL query and threshold the scalar value.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 30);
                           the plugin exits UNKNOWN 1 second after it
     -w WARNING, --warning WARNING
                           Warning threshold (plugin-specific)
     -c CRITICAL, --critical CRITICAL
                           Critical threshold (plugin-specific)
     --json                Output results in JSON format
     --server SERVER       Prometheus base URL
     --query QUERY         PromQL query returning a scalar
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
                           $CHECK_PROMETHEUS_QUERY_PASSWORD)
     --password-file PATH  Read password for HTTP basic authentication from PATH
                           (or the file named by
                           $CHECK_PROMETHEUS_QUERY_PASSWORD_FILE)
     --bearer-token BEARER_TOKEN
                           bearer token sent in the Authorization header (visible
                           in the process list; prefer --bearer-token-file or
                           $CHECK_PROMETHEUS_QUERY_BEARER_TOKEN)
     --bearer-token-file PATH
                           Read bearer token sent in the Authorization header
                           from PATH (or the file named by
                           $CHECK_PROMETHEUS_QUERY_BEARER_TOKEN_FILE)
     --api-key API_KEY     API key sent in the --api-key-header header (visible
                           in the process list; prefer --api-key-file or
                           $CHECK_PROMETHEUS_QUERY_API_KEY)
     --api-key-file PATH   Read API key sent in the --api-key-header header from
                           PATH (or the file named by
                           $CHECK_PROMETHEUS_QUERY_API_KEY_FILE)
     --api-key-header NAME
                           Header that carries --api-key (default: X-API-Key)
