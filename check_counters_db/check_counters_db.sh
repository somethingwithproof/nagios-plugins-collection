#!/usr/bin/env bash

# Vertica Database Status Checker
# This script checks the status of nodes and events in a Vertica database.
# It runs four queries to count the number of nodes with a state of 'DOWN',
# and the number of active events with descriptions of 'Too Many ROS Containers',
# 'Recovery Failure', and 'Stale Checkpoint'. The results are printed to the terminal.

# Copyright (c) 2023 Thomas Vincent

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Set error handling
set -euo pipefail

# Define environment variables
export VERTICA_HOST='vertica01'
export VERTICA_USER='zenoss'
export VERTICA_PASS='blah'

# Define SQL queries
sql_query_1="SELECT COUNT(*) FROM nodes WHERE node_state = 'DOWN';"
sql_query_2="SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Too Many ROS Containers';"
sql_query_3="SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Recovery Failure';"
sql_query_4="SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Stale Checkpoint';"

# Function to run queries and print results
run_query() {
    local result=$(vsql -h "$VERTICA_HOST" -U "$VERTICA_USER" -w "$VERTICA_PASS" -c "$1")
    echo "Result for $1: $result"
}

# Run queries and print results
run_query "$sql_query_1"
run_query "$sql_query_2"
run_query "$sql_query_3"
run_query "$sql_query_4"
