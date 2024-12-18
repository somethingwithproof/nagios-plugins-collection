#!/usr/bin/env python3
"""
Script for connecting to a Vertica database and executing queries.

This script establishes a connection to a Vertica database using the provided host, user, password, and database name.
It then executes a set of predefined queries and logs the results.

MIT License

Copyright (c) 2024 Thomas Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import logging
from psycopg2 import connect, DatabaseError, OperationalError
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class VerticaConnector:
    """Class for connecting to a Vertica database and executing queries."""

    def __init__(self, host: str, user: str, password: str, database: str):
        """
        Initialize the VerticaConnector instance.

        Args:
            host (str): The host name or IP address of the Vertica database server.
            user (str): The username for the Vertica database.
            password (str): The password for the Vertica database user.
            database (str): The name of the Vertica database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        """
        Connect to the Vertica database.

        Returns:
            psycopg2.extensions.connection: The database connection object.

        Raises:
            DatabaseError: If the connection to the database fails.
        """
        try:
            return connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except OperationalError as e:
            logging.error("Failed to connect to the database: %s", e)
            raise

    def execute_queries(self, queries: List[str]) -> List[int]:
        """
        Execute queries and return the results.

        Args:
            queries (List[str]): The list of queries to execute.

        Returns:
            List[int]: The list of results as integers.

        Raises:
            DatabaseError: If query execution fails.
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    results = []
                    for query in queries:
                        cur.execute(query)
                        result = cur.fetchone()[0]
                        results.append(result)
                        logging.info("Executed query: %s, Result: %s", query, result)
                    return results
        except DatabaseError as e:
            logging.error("Query execution failed: %s", e)
            raise

    def print_results(self, results: List[int]) -> None:
        """
        Log the results.

        Args:
            results (List[int]): The list of results to log.
        """
        for i, result in enumerate(results, start=1):
            logging.info("Result %d: %d", i, result)


def main() -> None:
    """Main function of the script."""

    # Get connection details from environment variables
    host = os.environ.get('VERTICA_HOST')
    user = os.environ.get('VERTICA_USER')
    password = os.environ.get('VERTICA_PASSWORD')

    if not all((host, user, password)):
        logging.error(
            "Missing connection details. Please set the environment variables: VERTICA_HOST, VERTICA_USER, VERTICA_PASSWORD"
        )
        return

    # Create VerticaConnector instance
    vertica_connector = VerticaConnector(host, user, password, 'vertica')

    # Define the queries
    queries = [
        "SELECT COUNT(*) FROM nodes WHERE node_state = 'DOWN';",
        "SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Too Many ROS Containers';",
        "SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Recovery Failure';",
        "SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Stale Checkpoint';"
    ]

    try:
        # Execute the queries and log the results
        results = vertica_connector.execute_queries(queries)
        vertica_connector.print_results(results)
    except Exception as e:
        logging.error("An error occurred: %s", e)


if __name__ == '__main__':
    main()
