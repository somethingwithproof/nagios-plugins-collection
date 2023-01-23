# Monitor Vertica

This script queries a Vertica database for various statistics and prints the results to the console. It uses the `psycopg2` library to connect to the database and execute the specified queries.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3
- psycopg2 library

### Installing

To install the dependencies, you can use the `requirements.txt` file by running:
pip install -r requirements.txt


### Configuration

The database connection parameters (hostname, username, password) are passed as environment variables and can be modified as needed. The queries being executed can also be modified as needed in the script.

### Running the script

To run the script, use the following command: 
python3 monitor_vertica.py

The script will connect to the Vertica database using the environment variables and execute the specified queries, then print the results to the console.

### Running the tests

To run the tests, you can use the `tox` command in the project directory.

## Deployment

The script can be deployed in the same way as it is run locally, but with the appropriate environment variables set.

## Built With

* [psycopg2](https://pypi.org/project/psycopg2/) - The library used to connect to the Vertica database

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](https://github.com/yourusername/repo/blob/branch/LICENSE) file for details.
