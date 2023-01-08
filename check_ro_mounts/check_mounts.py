#!/usr/bin/env python3

import os
import sys
import re
import subprocess as sp
import argparse
import datetime
import shlex

# Arg parser
remote_host = ""
remote_username = ""
remote_port = ""
remote_password = ""
mtab_path = ""
partition = ""
exclude = ""
exclude_type = ""

parser = argparse.ArgumentParser(description='check_ro_mounts nagios remote check ')

parser.add_argument('-sh', action="store", dest="sHost", help="SSH Remote host")
parser.add_argument('-su', action="store", dest="sUser", help="SSH Remote user (default: zenoss)")
parser.add_argument('-sp', action="store", dest="sPort", type=int, help="SSH Remote port")
parser.add_argument('-sd', action="store_true", dest="skipdate", help="Disable additional check (echo/cat)", required=False)
parser.add_argument('-mpath', action="store", dest="mtabPath", help="Use this mtab instead (default is /proc/mounts)")
parser.add_argument('-partition', action="append", dest="partFilter", help="Glob pattern of path or partition to check (may be repeated)")
parser.add_argument('-x', action="store", dest="exclude", help="Glob pattern of path or partition to ignore (only works if -partition unspecified)")
parser.add_argument('-X', action="append", dest="exclude_type")

options = parser.parse_args()
remote_host = options.sHost
remote_username = options.sUser
remote_port = options.sPort
mtab_path = options.mtabPath
partition = options.partFilter
exclude = options.exclude
exclude_type = options.exclude_type
skipdate = options.skipdate

# Some check of input data
if not remote_host:
    print("Error: remote_host parameter is required")
    sys.exit(3)

if not remote_username:
    remote_username = "zenoss"

if not remote_port:
    remote_port = 22

if not mtab_path:
    mtab_path = "/proc/mounts"

if partition:
    exclude = None

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
    uh = "%s@%s" % (user,host)
    ssh_proc = sp.Popen(['ssh', uh,     '-p', str(port), cmd], stdout=sp.PIPE, stderr=sp.PIPE)
    output = ssh_proc.stdout.read()
    return output

# Going to get needed data through ssh and process it
SSH_COMMAND = "cat " + mtab_path

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
else:
    # Additional check
    rw_date_ok = True
    date_cmd = "echo test > /tmp/test && rm /tmp/test"
    try:
        result_ssh = execute_ssh_command(date_cmd, remote_host, remote_username, remote_port)
    except Exception as e:
        print("RO_MOUNTS CRITICAL - %s" % e)
        sys.exit(2)
    if "Permission denied" in result_ssh:
        rw_date_ok = False
    if len(ro_mounts) > 0:
        print("RO_MOUNTS CRITICAL - Found %d readonly mounts" % len(ro_mounts))
        sys.exit(2)
    elif not rw_date_ok:
        print("RO_MOUNTS CRITICAL - All %d mounts are writable but date cmd failed" % len(rw_mounts))
        sys.exit(2)
    else:
        print("RO_MOUNTS OK - All %d mounts are writable and date cmd passed" % len(rw_mounts))
        sys.exit(0)

