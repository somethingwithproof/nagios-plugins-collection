import argparse
import json
import requests
import datetime
from logging import getLogger

logger = getLogger(__name__)

def get_component_status(url, component):
    """
    Check the status of a component by querying the JSON API.

    :param url: URL of the hostname
    :param component: Name of the component
    :return: a tuple of (status, updated) where status is one of ('ok', 'error')
    and updated is the time the component was last updated
    """
    try:
        response = requests.get(f"http://{url}/api/component/{component}")
        if response.status_code == 200:
            json_dict = response.json()
            status = json_dict["status"].lower()
            updated = json_dict["updated"]
            return (status, updated)
        else:
            logger.error(f"Error fetching component status: {response.status_code}")
            return ("error", None)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching component status: {e}")
        return ("error", None)

def main() -> int:
    """
    The main function of the script.
    """
    args = parse_args()
    component_statuses = {}
    for component in args.components:
        status, updated = get_component_status(args.url, component)
        component_statuses[component] = (status, updated)
    for component, (status, updated) in component_statuses.items():
        if status == "ok":
            if (updated is not None) and (datetime.datetime.now() - updated).total_seconds() / 60 > args.t:
                logger.warning(f"WARNING - Component {component} has not been updated in more than {args.t} minutes")
            else:
                logger.info(f"OK - Component {component} has been updated within the last {args.t} minutes")
        else:
            logger.critical(f"CRITICAL - Component {component} is in error state")
    return 0

if __name__ == "__main__":
    sys.exit(main())
