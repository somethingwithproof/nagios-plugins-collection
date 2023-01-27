#!/usr/bin/env python3

import argparse
import subprocess as sp
import shlex

def transform_ssh_result_into_listofdicts(source_result):
    result = []
    for each in source_result:
        if len(each) >= 6:
            newdict = {}
            newdict['device'] = each[0]
            newdict['mountpoint'] = each[1]
            newdict['type'] = each[2]
            newdict['opts'] = each[3]
            newdict['n1'] = each[4]
            newdict['n2'] = each[5]
            result.append(newdict)
    return result

def execute_ssh_command(cmd, host, user, port):
    ssh_proc = sp.run(['ssh', f"{user}@{host}", '-p', str(port), cmd], capture_output=True)
    output = ssh_proc.stdout
    return output

def check_mounts(remote_host: str, remote_username: str = "zenoss", remote_port: int = 22, mtab_path: str = "/proc/mounts", partition: list = None, exclude: str = None, exclude_type: list = None, skipdate: bool = False):

    if not remote_host:
        print("Error: remote_host parameter is required")
        sys.exit(3)

    if partition:
        exclude = None

    # Going to get needed data through ssh and process it
    SSH_COMMAND = f"cat {mtab_path}"
    try:
        result_ssh = execute_ssh_command(SSH_COMMAND, remote_host, remote_username, remote_port)
        result_lines = result_ssh.split(b'\n')
        result_ssh = []
        for each in result_lines:
            result_ssh.append(shlex.split(each.decode()))
        result_ssh = transform_ssh_result_into_listofdicts(result_ssh)
    except Exception as e:
        print("RO_MOUNTS UNKNOWN - %s" % e)
        sys.exit(3)

    # Check for rw/ro and date
    ro_mounts = []
    rw_mounts = []
    for each in result_ssh:
        if "ro" in each['opts']:
            ro_mounts.append(each)
        else:
            rw_mounts.append(each)

    if skipdate:
        if len(ro_mounts) > 0:
            print("RO_MOUNTS CRITICAL - Found %d readonly mounts" % len(ro_mounts))
            sys.exit(2)
        elif len(rw_mounts) > 0:
            print("RO_MOUNTS OK - All %d mounts are writable" % len(rw_mounts))
            sys.exit(0)
        else:
            print("RO_MOUNTS UNKNOWN - No mounts found")
            sys.exit(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='check_ro_mounts nagios remote check ')

    parser.add_argument('-sh', '--remote_host', help='remote hostname or ip', required=True)
    parser.add_argument('-u', '--remote_username', help='remote username', default='zenoss')
    parser.add_argument('-p', '--remote_port', help='remote ssh port', default=22)
    parser.add_argument('-mp', '--mtab_path', help='path to mtab', default='/proc/mounts')
    parser.add_argument('-pt', '--partition', help='partition to check', action='append')
    parser.add_argument('-ex', '--exclude', help='partition to exclude', default=None)
    parser.add_argument('-ext', '--exclude_type', help='filesystem type to exclude', action='append')
    parser.add_argument('-sd', '--skipdate', help='skip check for recent data', action='store_true')

    args = parser.parse_args()

    check_mounts(remote_host=args.remote_host, remote_username=args.remote_username, remote_port=args.remote_port, mtab_path=args.mtab_path, partition=args.partition, exclude=args.exclude, exclude_type=args.exclude_type, skipdate=args.skipdate)
