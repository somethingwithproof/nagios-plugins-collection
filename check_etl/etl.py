"""
Script: Component Status Checker
Description: This script checks the status of components by querying a JSON API.
Author: Thomas Vincent
Copyright: © 2023 Thomas Vincent
License: MIT License
"""

import argparse
import json
import requests
import datetime
import logging

logger = logging.getLogger(__name__)

class ComponentStatusChecker:
    """
    A class for checking the status of components by querying a JSON API.
    """

    def __init__(self, url):
        """
        Initialize the ComponentStatusChecker with the URL of the hostname.
        :param url: URL of the hostname
        """
        self.url = url

    def get_component_status(self, component):
        """
        Check the status of a component by querying the JSON API.
        :param component: Name of the component
        :return: a tuple of (status, updated) where status is one of ('ok', 'error')
        and updated is the time the component was last updated
        """
        try:
            # Add timeout for security and better error handling
            response = requests.get(
                f"http://{self.url}/api/component/{component}", 
                timeout=10,
                verify=True  # Verify SSL certificates
            )
            if response.status_code == 200:
                json_dict = response.json()
                status = json_dict["status"].lower()
                updated = json_dict["updated"]
                return status, updated
            else:
                logger.error(f"Error fetching component status: HTTP {response.status_code}")
                return "error", None
        except requests.exceptions.Timeout:
            logger.error(f"Connection to {self.url} timed out after 10 seconds")
            return "error", None
        except requests.exceptions.SSLError as e:
            logger.error(f"SSL Error: {e}")
            return "error", None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching component status: {e}")
            return "error", None

    def check_components(self, components, threshold):
        """
        Check the status of the given components and log the results.
        :param components: List of component names
        :param threshold: Threshold in minutes for checking component update
        """
        component_statuses = {}
        for component in components:
            status, updated = self.get_component_status(component)
            component_statuses[component] = (status, updated)

        current_time = datetime.datetime.now()
        for component, (status, updated) in component_statuses.items():
            if status == "ok":
                if updated is not None and (current_time - updated).total_seconds() / 60 > threshold:
                    logger.warning(f"WARNING - Component {component} has not been updated in more than {threshold} minutes")
                else:
                    logger.info(f"OK - Component {component} has been updated within the last {threshold} minutes")
            else:
                logger.critical(f"CRITICAL - Component {component} is in an error state")

def parse_args():
    """
    Parse command-line arguments.
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True, help="URL of the hostname")
    parser.add_argument("--components", nargs="+", type=str, required=True, help="List of component names")
    parser.add_argument("-t", type=int, default=10, help="Threshold in minutes for checking component update")
    return parser.parse_args()

def main():
    """
    The main function of the script.
    :return: Exit code
    """
    args = parse_args()
    checker = ComponentStatusChecker(args.url)
    checker.check_components(args.components, args.t)
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import sys
    sys.exit(main())
