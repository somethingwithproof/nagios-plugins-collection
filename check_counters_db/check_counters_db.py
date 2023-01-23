#!/usr/bin/env python3

"""
Script that connects to a Vertica database, runs 4 SQL queries, and prints the results.

This script uses the latest features of Python, such as context managers, f-strings, list comprehension and tuple unpacking.

Environment Variables:
    - VERTICA_HOST
    - VERTICA_USER
    - VERTICA_PASSWORD

MIT License

Copyright (c) 2023 Thomas Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import psycopg2

def main():
    """ Main function of the script """

    # Get connection details from environment variables
    host = os.environ['VERTICA_HOST']
    user = os.environ['VERTICA_USER']
    password = os.environ['VERTICA_PASSWORD']

    # Connect to the database using context manager
    with psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database='vertica'
    ) as conn:
        with conn.cursor() as cur:
            # Execute the queries using f-strings
            queries = [
                f"select count(*) from nodes where node_state = 'DOWN';",
                f"select count(*) from active_events where event_code_description = 'Too Many ROS Containers';",
                f"select count(*) from active_events where event_code_description = 'Recovery Failure';",
                f"select count(*) from active_events where event_code_description = 'Stale Checkpoint';"
            ]
            results = [cur.execute(query).fetchone()[0] for query in queries]
            # Print the results using tuple unpacking
            for i, result in enumerate(results, start=1):
                print(f"R{i}: {result}")

if __name__ == '__main__':
    main()
