#!/usr/bin/env bash

# This script is used to check the status of nodes and events in a Vertica database.
# It runs four queries to count the number of nodes with a state of 'DOWN', and the number of active events with descriptions of 'Too Many ROS Containers', 'Recovery Failure', and 'Stale Checkpoint'.
# The results of these queries are then printed to the terminal.

set -euo pipefail

readonly VERTICA_HOST='vertica01'
readonly VERTICA_USER='zenoss'
readonly VERTICA_PASS='blah'

readonly SQL_QUERY_1="SELECT COUNT(*) FROM nodes WHERE node_state = 'DOWN';"
readonly SQL_QUERY_2="SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Too Many ROS Containers';"
readonly SQL_QUERY_3="SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Recovery Failure';"
readonly SQL_QUERY_4="SELECT COUNT(*) FROM active_events WHERE event_code_description = 'Stale Checkpoint';"

main() {
  local result1 result2 result3 result4

  result1=$(vsql -h "$VERTICA_HOST" -U "$VERTICA_USER" -w "$VERTICA_PASS" -c "$SQL_QUERY_1" | awk '{print $3}')
  echo "Result 1: $result1"

  result2=$(vsql -h "$VERTICA_HOST" -U "$VERTICA_USER" -w "$VERTICA_PASS" -c "$SQL_QUERY_2" | awk '{print $3}')
  echo "Result 2: $result2"

  result3=$(vsql -h "$VERTICA_HOST" -U "$VERTICA_USER" -w "$VERTICA_PASS" -c "$SQL_QUERY_3" | awk '{print $3}')
  echo "Result 3: $result3"

  result4=$(vsql -h "$VERTICA_HOST" -U "$VERTICA_USER" -w "$VERTICA
