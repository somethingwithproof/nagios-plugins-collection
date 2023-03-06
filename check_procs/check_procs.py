#!/usr/bin/env python3

# Script dependencies:
# pynag, subprocess

import os
import sys
import re
import argparse
import subprocess
from pynag.Plugins import Plugin, WARNING, CRITICAL, OK, UNKNOWN

# Create the plugin object
plugin = Plugin()

# Configure additional command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("command", type=str, help="Process name or command to scan")
parser.add_argument("-R", "--ssh_host", type=str, required=True, help="SSH remote machine name to connect to")
parser.add_argument("-p", "--ssh_password", type=str, required=False, help="SSH remote host password")
parser.add_argument("-u", "--ssh_username", type=str, required=False, help="SSH remote username")
parser.add_argument("-P", "--ssh_port", type=int, default=22, required=False, help="SSH remote host port (default: 22)")
parser.add_argument("-m", "--metric", type=str, default="PROCS", choices=["PROCS", "VSZ", "RSS", "CPU", "ELAPSED"], help="Check thresholds against metric")
parser.add_argument("-s", "--statusflags", type=str, required=False, help="Only scan for processes that have, in the output of `ps`, one or more of the status flags you specify (for example R,Z,S,RS,RSZDT, plus others based on the output of your `ps` command)")
parser.add_argument("-i", "--ppid", type=int, required=False, help="Only scan for children of the parent process ID indicated")
parser.add_argument("-z", "--vsz", type=int, required=False, help="Only scan for processes with VSZ higher than indicated")
parser.add_argument("-r", "--rss", type=int, required=False, help="Only scan for processes with RSS higher than indicated")
parser.add_argument("-o", "--pcpu", type=int, required=False, help="Only scan for processes with PCPU higher than indicated")
parser.add_argument("-y", "--user", type=str, required=False, help="Only scan for processes with user name or ID indicated")
args = parser.parse_args()

# Internal functions declaration

def transform_lines_into_dict(lineslist):
    result = []
    for each in lineslist:
        if len(each) >= 8:
            newdict = {
                'uid': each[0],
                'pid': each[1],
                'parentpid': each[2],
                'vsz': each[3],
                'rss': each[4],
                'status': each[5],
                'time': each[6],
                'pcpu': each[7],
            }
            result.append(newdict)
    return result

def test_flags(flags_array, process_flags):
    process_flags_array = list(process_flags)
    return any(flag in process_flags_array for flag in flags_array)

def perfdata(value_count):
    return f"|count={value_count}"

# SSH Section
ssh_username = "zenoss"
if args.ssh_username:
    ssh_username = args.ssh_username

SSH_COMMAND = f"ps -C \"{args.command}\" -o uid,pid,ppid,vsz,rss,stat,bsdtime,pcpu,comm"
# Get the PS output and process it
try:
    if args.user:
        user_flag = "-U" if args.user.isdigit() else "-u"
        SSH_COMMAND += f" {user_flag} {args.user}"

ssh_command = f"ssh {ssh_username}@{args.ssh_host} -p {args.ssh_port} '{SSH_COMMAND}'"
ssh_process = subprocess.Popen(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = ssh_process.communicate()

if ssh_process.returncode != 0:
    print("UNKNOWN - SSH command failed: ", stderr.decode("utf-8").strip())
    sys.exit(UNKNOWN)

result_lines = stdout.decode("utf-8").strip().split("\n")[2:]
result = transform_lines_into_dict([re.sub(" +", " ", line).split() for line in result_lines])

# Applying the first filter - status flag, if needed
if args.statusflags:
    flags_arr = args.statusflags.split(",")
    result = [process for process in result if test_flags(flags_arr, process["status"])]

# Applying the second filter - parent pid filter if needed
if args.ppid:
    result = [process for process in result if process["parentpid"] == args.ppid]

# Applying the last numeric filters
if args.vsz:
    result = [process for process in result if int(process["vsz"]) > args.vsz]

if args.rss:
    result = [process for process in result if int(process["rss"]) > args.rss]

if args.pcpu:
    result = [process for process in result if int(float(process["pcpu"])) > args.pcpu]

proc_count = len(result)
warn_limit = plugin['warning']
crit_limit = plugin['critical']

# Here we should check the procs
if plugin['warning']:
    min_count, max_count = map(int, warn_limit.split(":"))
    if min_count > max_count:
        min_count, max_count = max_count, min_count
    if not min_count <= proc_count <= max_count:
        print(f"PROCS WARNING - {proc_count} processes {perfdata(proc_count)}")
        sys.exit(WARNING)

if plugin['critical']:
    min_count, max_count = map(int, crit_limit.split(":"))
    if min_count > max_count:
        min_count, max_count = max_count, min_count
    if not min_count <= proc_count <= max_count:
        print(f"PROCS CRITICAL - {proc_count} processes {perfdata(proc_count)}")
        sys.exit(CRITICAL)

print(f"PROCS OK - {proc_count} processes {perfdata(proc_count)}")
sys.exit(OK)
except Exception as e:
print(f"UNKNOWN - {str(e)}")
sys.exit(UNKNOWN)


