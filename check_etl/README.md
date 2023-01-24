
# Component Checker

This script retrieves the status and updated time of a component from an API and checks if the time since the last update is within a specified limit.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need python 3.8 installed on your local machine in order to run this script.

### Installing

A step by step series of examples that tell you how to get a development env running

1.  Clone or download the repository
2.  Install the required python modules by running `pip install -r requirements.txt`
3.  Run the script by executing `python component_checker.py -url=URL -component=COMPONENT -t=MAX_TIME`

Where:

-   `URL` is the URL of the hostname.
-   `COMPONENT` is the name of the component.
-   `MAX_TIME` is the maximum time (in minutes) since the last update.

## Running the tests

This script does not have any automated tests

## Deployment

This script is intended for use on a local machine for development and testing purposes. It can also be used in a production environment by integrating it with a monitoring system such as Nagios.

## Authors

-   **Thomas Vincent** - _Initial work_

## License

This project is licensed under the MIT License.
