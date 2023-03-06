#!/usr/bin/env python3

import re
import sys
from typing import List, Dict, Optional
from argparse import ArgumentParser
from dataclasses import dataclass
from getpass import getpass
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException

# Plugin return codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


@dataclass
class Process:
    uid: str
    pid: str
    parent_pid: str
    vsz: str
    rss: str
    status: str
    time: str
    pcpu: str


def transform_lines_into_dict(lineslist: List[str]) -> List[Process]:
    result = []
    for line in lineslist[2:]:
        parts = re.split(r'\s+', line.strip())
        if len(parts) >= 8:
            result.append(Process(
                uid=parts[0],
                pid=parts[1],
                parent_pid=parts[2],
                vsz=parts[3],
                rss=parts[4],
                status=parts[5],
                time=parts[6],
                pcpu=parts[7]
            ))
    return result


def testflags(flags_array: List[str], process_flags: str) -> bool:
    process_flags_array = list(process_flags)
    return any(flag in process_flags_array for flag in flags_array)


def get_ssh_connection(ssh_host: str, ssh_port: int, ssh_username: Optional[str],
                       ssh_password: Optional[str]) -> Optional[SSHClient]:
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        if ssh_password:
            client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
        else:
            client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username)
        return client
    except (AuthenticationException, SSHException) as e:
        print(f"UNKNOWN - {e}")
        sys.exit(UNKNOWN)


def get_processes(ssh_connection: SSHClient, command: str) -> List[Process]:
    stdin, stdout, stderr = ssh_connection.exec_command(command)
    output = stdout.read().decode('utf-8')
    return transform_lines_into_dict(output.splitlines())


def filter_processes(processes: List[Process], status_flags: Optional[List[str]], ppid: Optional[str],
                     vsz: Optional[int], rss: Optional[int], pcpu: Optional[int]) -> List[Process]:
    result = processes
    if status_flags:
        result = [proc for proc in processes if testflags(status_flags, proc.status)]
    if ppid:
        result = [proc for proc in result if proc.parent_pid == ppid]
    if vsz:
        result = [proc for proc in result if int(proc.vsz) > vsz]
    if rss:
        result = [proc for proc in result if int(proc.rss) > rss]
    if pcpu:
        result = [proc for proc in result if int(proc.pcpu) > pcpu]
    return result


def check_processes(processes: List[Process], warning: Optional[str], critical: Optional[str]) -> None:
    proc_count = len(processes)
    warn_limit = parse_limit(warning)
    crit_limit = parse_limit(critical)
    if warning and is_outside_range(proc_count, warn_limit):
        print(f"PROCS WARNING - {proc_count} processes")
        sys.exit(1)
    if critical and is_outside_range(proc_count, crit_limit):
        print(f"PROCS CRITICAL - {proc_count} processes")
        sys.exit(2)
    print(f"PROCS OK - {proc_count} processes")

# SSH Section
ssh_port = args.ssh_port or 22
ssh_username = args.ssh_username or "zenoss"
ssh_password = args.ssh_password
ssh_host = args.ssh_host

ssh_command = f"ssh {ssh_username}@{ssh_host} -p {ssh_port} 'ps -C \"{args.command}\" -o uid,pid,ppid,vsz,rss,stat,bsdtime,pcpu,comm'"
try:
    ssh_output = subprocess.check_output(ssh_command, shell=True, universal_newlines=True)
    processes = parse_output(ssh_output)
    if args.statusflags:
        processes = filter_by_status_flags(processes, args.statusflags.split(","))
    if args.ppid:
        processes = filter_by_parent_pid(processes, args.ppid)
    if args.vsz:
        processes = filter_by_vsz(processes, int(args.vsz))
    if args.rss:
        processes = filter_by_rss(processes, int(args.rss))
    if args.pcpu:
        processes = filter_by_pcpu(processes, int(args.pcpu))
    check_processes(processes, args.warning, args.critical)
except subprocess.CalledProcessError as e:
    print(f"UNKNOWN - {e}")
    sys.exit(3)
except ValueError as e:
    print(f"UNKNOWN - {e}")
    sys.exit(3)
