#!/bin/bash

# Author: Thomas Vincent
# Copyright (c) 2023 Thomas Vincent. All rights reserved.
# This script is used to check the status of the Scribe daemon on a remote server via SSH.

# USAGE
# check_scribe SSH_USERNAME SSH_HOST

# Nagios exit codes
readonly NAGIOS_OK=0
readonly NAGIOS_WARNING=1
readonly NAGIOS_CRITICAL=2
readonly NAGIOS_UNKNOWN=3

# Scribe service states mapped to Nagios codes
readonly SCRIBE_OK="ALIVE"
readonly SCRIBE_WARNING="WARNING"
readonly SCRIBE_CRITICAL="[(STARTING)(STOPPING)(STOPPED)(DEAD)(Failed to get status)]"

# Checks if the required number of arguments have been passed
if [ $# -ne 2 ]; then
    echo "Usage: $0 SSH_USERNAME SSH_HOST"
    exit $NAGIOS_UNKNOWN
fi

# Build SSH command to run scribe_ctrl status on remote server
admin_cmd="ssh $1@$2 /usr/sbin/scribe_ctrl status"

# Execute SSH command and capture output in variable
rval=$(eval "$admin_cmd")

# Check output for Scribe service status and return appropriate Nagios exit code
if [[ "$rval" =~ "$SCRIBE_OK" ]]; then
    echo "OK"
    exit $NAGIOS_OK
elif [[ "$rval" =~ "$SCRIBE_WARNING" ]]; then
    echo "WARNING - $rval"
    exit $NAGIOS_WARNING
elif [[ "$rval" =~ "$SCRIBE_CRITICAL" ]]; then
    echo "CRITICAL - $rval"
    exit $NAGIOS_CRITICAL
else
    echo "UNKNOWN - Scribe daemon is in an unknown state: $rval"
    exit $NAGIOS_UNKNOWN
fi
