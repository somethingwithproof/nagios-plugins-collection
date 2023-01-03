#!/bin/bash

# This script is used to check the status of nodes and events in a Vertica database.
# It runs four queries to count the number of nodes with a state of 'DOWN', and the number of active events with descriptions of 'Too Many ROS Containers', 'Recovery Failure', and 'Stale Checkpoint'.
# The results of these queries are then printed to the terminal.

USER="zenoss"
PASS="blah"

read -r -d '' cmd1 <<EOF
select count(*) from nodes where node_state = 'DOWN';
EOF

read -r -d '' cmd2 <<EOF
select count(*) from active_events where event_code_description = 'Too Many ROS Containers';
EOF

read -r -d '' cmd3 <<EOF
select count(*) from active_events where event_code_description = 'Recovery Failure';
EOF

read -r -d '' cmd4 <<EOF
select count(*) from active_events where event_code_description = 'Stale Checkpoint';
EOF

vsql_cmd="/opt/vertica/bin/vsql -h vertica01 -U $USER -w $PASS -c"

result1=$(eval "$vsql_cmd" "$cmd1" | sed "s/[^0-9]/ /g" | cut -d' ' -f1)
echo "$result1"

result2=$(eval "$vsql_cmd" "$cmd2" | sed "s/[^0-9]/ /g" | cut -d' ' -f1)
echo "$result2"

result3=$(eval "$vsql_cmd" "$cmd3" | sed "s/[^0-9]/ /g" | cut -d' ' -f1)
echo "$result3"

result4=$(eval "$vsql_cmd" "$cmd4" | sed "s/[^0-9]/ /g" | cut -d' ' -f1)
echo "$result4"
