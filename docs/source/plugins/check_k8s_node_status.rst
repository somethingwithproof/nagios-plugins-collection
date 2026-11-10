.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_k8s_node_status
=====================

Run ``check_k8s_node_status --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_k8s_node_status
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_k8s_node_status [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                                [--json] [--label LABEL]

   Monitor Kubernetes node readiness.

   -w/-c are Nagios ranges for the number of nodes that are not ready (for
   example -w 0 -c 2). Without them any unready node is CRITICAL. Disk,
   memory or PID pressure on any node is always CRITICAL.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 30);
                           the plugin exits UNKNOWN 1 second after it
     -w WARNING, --warning WARNING
                           Warning threshold (Nagios range for the number of
                           unready nodes)
     -c CRITICAL, --critical CRITICAL
                           Critical threshold (Nagios range for the number of
                           unready nodes)
     --json                Output results in JSON format
     --label LABEL         Label selector for nodes
