"""
Nagios Plugins Collection

A collection of production-ready Nagios monitoring plugins for various services
and infrastructure components.

Plugins included:
- check_procs: Monitor remote processes via SSH
- check_ro_mounts: Detect read-only filesystem mounts
- check_dig: DNS resolution monitoring
- check_hadoop: Hadoop cluster health monitoring
- check_monghealth: MongoDB health monitoring
- check_jobs: Job execution monitoring
- check_website_status: Website availability monitoring
- check_membase: Membase/Couchbase statistics monitoring
"""

__version__ = "2.0.0"
__author__ = "Thomas Vincent"
__email__ = "thomas@thomasvincent.io"

# Nagios exit codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

__all__ = [
    "__version__",
    "OK",
    "WARNING",
    "CRITICAL",
    "UNKNOWN",
]
