import argparse
import json
import urllib.request
import urllib.error
import datetime
from typing import Tuple

def parse_args() -> argparse.Namespace:
    """
    Parses command line arguments and returns them as a Namespace object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", required=True, help="URL of the hostname")
    parser.add_argument("-component", required=True, help="Name of the component")
    parser.add_argument("-t", required=True, type=int, help="Max time since last update in minutes")
    return parser.parse_args()

def component_checker(url: str, component: str) -> Tuple[str, Union[datetime.timedelta, str]]:
    """
    Check the status of a component by querying the JSON API.

    :param url: URL of the hostname
    :param component: Name of the component
    :return: a tuple of (status, result) where status is one of ('ok', 'error')
    and result is a timedelta object representing the time since last update for 'ok' status 
    or a string representing the error message for 'error' status
    """
    try:
        request = urllib.request.urlopen(f"http://{url}/api/component/{component}")
        content = request.read().decode()
        json_dict = json.loads(content)
        status = json_dict["status"].lower()
        if status == "ok":
            time_from_json = datetime.datetime.strptime
            time_from_json = datetime.datetime.strptime(json_dict["updated"], "%Y-%m-%d %H:%M:%S")
            time_now = datetime.datetime.now()
            time_delta = time_now - time_from_json
            return (status, time_delta)
        else:
            return (status, json_dict["message"])
    except urllib.error.URLError as e:
        return ("error", str(e))
    except urllib.error.HTTPError as e:
        return ("error", str(e))

def main() -> int:
    """
    The main function of the script.
    """
    args = parse_args()
    status, result = component_checker(args.url, args.component)
    if status == "ok":
        if result.total_seconds() / 60 > args.t:
            print(f"WARNING - Time since last update is greater than {args.t} minutes")
            return 1
        else:
            print(f"OK - Time since last update is less than {args.t} minutes")
            return 0
    elif status == "error":
        print(f"CRITICAL - {result}")
        return 2
    else:
        print(f"CRITICAL - {result}")
        return 2

if __name__ == "__main__":
    sys.exit(main())
