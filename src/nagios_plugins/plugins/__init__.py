"""Nagios Plugins Collection.

This package contains a collection of standardized Nagios plugins
for monitoring various services and systems. All plugins follow a consistent 
interface and use the plugin framework for standardization.

Available plugins:
- check_component_status: Checks component status via a JSON API
- check_mongodb_health: Checks MongoDB health status
- check_website_status: Checks website status and response time
- check_ro_mounts: Checks for read-only mounts
- check_hadoop: Checks Hadoop cluster status
- check_jobs: Checks job status
- check_dig: DNS query checker
- check_procs: Process check
"""

# List all standardized plugins here for easy import and discovery
__all__ = [
    # New standardized plugins
    "check_component_status",
    "check_mongodb_health", 
    "check_website_status",
    "check_ro_mounts",
    
    # Legacy plugins
    "check_monghealth",
    "check_hadoop",
    "check_jobs",
    "check_etl",
    "check_dig",
    "check_procs",
]

# Plugin version
__version__ = "1.0.0"
