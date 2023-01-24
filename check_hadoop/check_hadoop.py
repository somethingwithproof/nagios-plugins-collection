#!/usr/bin/env python3

import os
import sys
import json
import subprocess

# Please note that in order for this script to work correctly, the hadoop command must be in the system's PATH
# and the cluster must be configured for hadoop health command to be able to run.
def check_hadoop() -> tuple:
    """
    Check the status of a Hadoop cluster using the `hadoop health` command.
    
    :return: a tuple of (status, message) where status is one of ('OK', 'WARNING', 'CRITICAL', 'UNKNOWN')
    and message is a string describing the current status of the cluster.
    """
    try:
        output = subprocess.check_output(['hadoop', 'health', '-json'], stderr=subprocess.STDOUT)
        output = output.decode('utf-8')
        health_data = json.loads(output)
    except (subprocess.CalledProcessError, json.decoder.JSONDecodeError):
        return ('UNKNOWN', 'Error running `hadoop health` command')

    status = health_data.get('status', 'UNKNOWN')
    message = health_data.get('message', 'No message returned')

    if status == 'GOOD':
        return ('OK', message)
    elif status == 'CONCERNING
    elif status == 'CONCERNING':
        return ('WARNING', message)
    elif status == 'BAD':
        return ('CRITICAL', message)
    else:
        return ('UNKNOWN', message)


if __name__ == '__main__':
    status, message = check_hadoop()
    print(f'{status} - {message}')
    sys.exit(status)
