.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_aws_cloudwatch
====================

Run ``check_aws_cloudwatch --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_aws_cloudwatch
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_aws_cloudwatch [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                               [--json] --namespace NAMESPACE --metric METRIC
                               [--region REGION]
                               [--statistic {Average,Sum,Maximum,Minimum,SampleCount}]
                               [--period PERIOD] [--minutes-back MINUTES_BACK]
                               [--instance-id INSTANCE_ID]
                               [--db-instance-id DB_INSTANCE_ID]
                               [--function-name FUNCTION_NAME]
                               [--load-balancer-name LOAD_BALANCER_NAME]
                               [--dimensions DIMENSIONS]

   Check AWS CloudWatch metrics plugin.

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
     --namespace NAMESPACE
                           AWS namespace (e.g., AWS/EC2, AWS/RDS, AWS/Lambda,
                           AWS/ELB)
     --metric METRIC       Metric name (e.g., CPUUtilization,
                           DatabaseConnections)
     --region REGION       AWS region (uses default credentials region if not
                           specified)
     --statistic {Average,Sum,Maximum,Minimum,SampleCount}
                           Statistic type (default: Average)
     --period PERIOD       Period in seconds for the metric (default: 300)
     --minutes-back MINUTES_BACK
                           How many minutes back to query (default: 5)
     --instance-id INSTANCE_ID
                           EC2 instance ID (for AWS/EC2 namespace)
     --db-instance-id DB_INSTANCE_ID
                           RDS database instance ID (for AWS/RDS namespace)
     --function-name FUNCTION_NAME
                           Lambda function name (for AWS/Lambda namespace)
     --load-balancer-name LOAD_BALANCER_NAME
                           ELB load balancer name (for AWS/ELB namespace)
     --dimensions DIMENSIONS
                           Custom dimensions in format 'Name=Value,Name=Value'
