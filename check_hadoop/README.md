
# Hadoop Cluster Status Checker

This script is a command-line tool i wrote over a decade ago for a client. This is a clean room implementation of the original script i have written as a personal exercise. The script checks the status of a Hadoop cluster and its components by querying a JSON API. The API URL and (optionally) the maximum allowed time since the last update of each component are specified as command-line arguments. If any component has a status other than "ok", the script will exit with a warning status. If the -t argument is provided, the time since the last update of each component is checked, and if the time since the last update exceeds the value specified with the -t argument, the script will exit with a warning status. If all components have an "ok" status and (if the -t argument is provided) the time since the last update is within the acceptable range, the script will print the memory usage and exit with an "ok" status.

## Getting Started

These instructions will help you to run the script on your local machine for development and testing purposes.

### Prerequisites

You need to have the following packages installed:

-   httpx
-   json
-   datetime

### Installing

You can install the packages using pip:

Copy code

`pip install httpx pip install json pip install datetime`

### Running the script

To run the script, you need to provide the url of the JSON API and (optionally) the maximum allowed time since the last update of each component as command-line arguments.

Copy code

`python3 hadoop.py -url=SOURCE_JSON_URL -t MAX_TIME_SINCE_LAST_UPDATE_IN_MINUTES`

## Built With

-   [httpx](https://www.python-httpx.org/) - The library used for making HTTP requests
-   [json](https://docs.python.org/3/library/json.html) - The library used for parsing JSON data
-   [datetime](https://docs.python.org/3/library/datetime.html) - The library used for working with date and time

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

-   **Thomas Vincent** - _Initial work_

## License

This project is licensed under the MIT License.

## Acknowledgments

-   Inspiration: [Hadoop Cluster Status Checker Script](https://github.com/JulianK/Hadoop-Cluster-Status-Checker-Script)
