#!/usr/bin/env python3
"""
check_ro_mounts.py

Description:
A script to check the mount points on a remote host for read-only mounts.

Author:
Thomas Vincent

License:
MIT License
"""

import argparse
import subprocess as sp
import shlex
import sys


def transform_ssh_result_into_list_of_dicts(source_result):
    """
    Transforms the SSH result into a list of dictionaries.

    Args:
        source_result (list): List of SSH result lines.

    Returns:
        list: List of dictionaries with transformed SSH results.
    """
    result = []
    for each in source_result:
        if len(each) >= 6:
            new_dict = {
                'device': each[0],
                'mountpoint': each[1],
                'type': each[2],
                'opts': each[3],
                'n1': each[4],
                'n2': each[5]
            }
            result.append(new_dict)
    return result


def execute_ssh_command(cmd, host, user, port):
    """
    Executes an SSH command and captures the output.

    Args:
        cmd (str): Command to execute.
        host (str): Remote hostname or IP address.
        user (str): Remote username.
        port (int): Remote SSH port.

    Returns:
        list: List of output lines.
    """
    ssh_proc = sp.run(['ssh', f"{user}@{host}", '-p', str(port), cmd], capture_output=True)
    output = ssh_proc.stdout.decode().splitlines()
    return output


def check_mounts(remote_host: str, remote_username: str = "zenoss", remote_port: int = 22,
                 mtab_path: str = "/proc/mounts", partition: list = None, exclude: str = None,
                 exclude_type: list = None, skip_date: bool = False):
    """
    Checks the mount points on a remote host for read-only mounts.

    Args:
        remote_host (str): Remote hostname or IP address.
        remote_username (str, optional): Remote username. Defaults to "zenoss".
        remote_port (int, optional): Remote SSH port. Defaults to 22.
        mtab_path (str, optional): Path to mtab. Defaults to "/proc/mounts".
        partition (list, optional): Partition to check. Defaults to None.
        exclude (str, optional): Partition to exclude. Defaults to None.
        exclude_type (list, optional): Filesystem type to exclude. Defaults to None.
        skip_date (bool, optional): Skip check for recent data. Defaults to False.
    """
    if not remote_host:
        print("Error: remote_host parameter is required")
        sys.exit(3)

    if partition:
        exclude = None

    # Get needed data through SSH and process it
    ssh_command = f"cat {mtab_path}"
    try:
        result_ssh = execute_ssh_command(ssh_command, remote_host, remote_username, remote_port)
        result_ssh = [shlex.split(line) for line in result_ssh]
        result_ssh = transform_ssh_result_into_list_of_dicts(result_ssh)
    except Exception as e:
        print("RO_MOUNTS UNKNOWN - %s" % e)
        sys.exit(3)

    # Check for rw/ro and date
    ro_mounts = [mount for mount in result_ssh if "ro" in mount['opts']]
    rw_mounts = [mount for mount in result_ssh if "ro" not in mount['opts']]

    if skip_date:
        if len(ro_mounts) > 0:
            print(f"RO_MOUNTS CRITICAL - Found {len(ro_mounts)} readonly mounts")
            sys.exit(2)
        elif len(rw_mounts) > 0:
            print(f"RO_MOUNTS OK - All {len(rw_mounts)} mounts are writable")
            sys.exit(0)
        else:
            print("RO_MOUNTS UNKNOWN - No mounts found")
            sys.exit(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='check_ro_mounts nagios remote check ')

    parser.add_argument('-sh', '--remote_host', help='remote hostname or IP', required=True)
    parser.add_argument('-u', '--remote_username', help='remote username', default='zenoss')
    parser.add_argument('-p', '--remote_port', help='remote SSH port', default=22, type=int)
    parser.add_argument('-mp', '--mtab_path', help='path to mtab', default='/proc/mounts')
    parser.add_argument('-pt', '--partition', help='partition to check', action='append')
    parser.add_argument('-ex', '--exclude', help='partition to exclude', default=None)
    parser.add_argument('-ext', '--exclude_type', help='filesystem type to exclude', action='append')
    parser.add_argument('-sd', '--skip_date', help='skip check for recent data', action='store_true')

    args = parser.parse_args()

    check_mounts(remote_host=args.remote_host, remote_username=args.remote_username, remote_port=args.remote_port,
                 mtab_path=args.mtab_path, partition=args.partition, exclude=args.exclude,
                 exclude_type=args.exclude_type, skip_date=args.skip_date)
