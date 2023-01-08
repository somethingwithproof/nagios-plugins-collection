#!/usr/bin/env python3

#Script dependencies:
# subprocess, argparse

import os, sys, re
import subprocess as sp
import argparse
import datetime
import shlex

#Arg parser
remote_host = ""
remote_username = ""
remote_port = ""
remote_password = ""
#
mtab_path = ""
partition = ""
exclude = ""
exclude_type = ""


parser = argparse.ArgumentParser(description='check_ro_mounts nagios remote check ')

parser.add_argument('-sh', action="store", dest="sHost", help="SSH Remote host")
parser.add_argument('-su', action="store", dest="sUser", help="SSH Remote user (default: zenoss)")
parser.add_argument('-sp', action="store", dest="sPort", type=int, help="SSH Remote port")
parser.add_argument('-sd', action="store_true", dest="skipdate", help="Disable additional check (echo/cat)", required=False)
parser.add_argument('-mpath', action="store", dest="mtabPath", help = "Use this mtab instead (default is /proc/mounts)")
parser.add_argument('-partition', action="append", dest="partFilter", help="Glob pattern of path or partition to check (may be repeated)")
parser.add_argument('-x', action="store", dest="exclude", help="Glob pattern of path or partition to ignore (only works if -partition unspecified)")
parser.add_argument('-X', action="append", dest="exclude_type")

options = parser.parse_args()
remote_host =       options.sHost
remote_username =   options.sUser
remote_port =       options.sPort
mtab_path =         options.mtabPath
partition =         options.partFilter
exclude =           options.exclude
exclude_type =      options.exclude_type
skipdate =          options.skipdate

#DBGprint skipdate
#DBGsys.exit(1)
#Some check of input data
if not remote_host:
    print "Error: remote_host parameter is required"
    sys.exit(3)

if not remote_username:
    remote_username = "zenoss"

if not remote_port:
    remote_port = 22

if not mtab_path:
    mtab_path = "/proc/mounts"

if partition:
    exclude = None
########################################################################################################################
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
########################################################################################################################
def execute_ssh_command(cmd, host, user, port):
    uh = "%s@%s" % (user,host)
    ssh_proc = sp.Popen(['ssh', uh, '-p', str(port), cmd], stdout=sp.PIPE, stderr=sp.PIPE)
    output = ssh_proc.stdout.read()
    return output
########################################################################################################################
# #Going to get needed data through ssh and process it
SSH_COMMAND = "cat "+mtab_path

try:
    result_ssh = execute_ssh_command(SSH_COMMAND, remote_host, remote_username, remote_port)
    #if "rw" not in result_ssh:
    #    if "ro" not in result_ssh
    #        print "RO_MOUNTS UNKNOWN - Wrong data received from remote host"
    #        sys.exit(3)
    result_lines = result_ssh.split('\n')
    result_ssh = []
    for each in result_lines:
        result_ssh.append(re.sub(' +',' ',each).split())
    result_ssh = transform_ssh_result_into_listofdicts(result_ssh)

    #Partition/path filter
    result_int = []
    if partition:
        for part in partition:
            for each in result_ssh:
                if part in each['device']:
                    result_int.append(each)
        result_ssh = result_int

    #Exclude type filter
    result_int = []
    if exclude_type:
        for etype in exclude_type:
            for each in result_ssh:
                if etype not in each['type']:
                    result_int.append(each)
        result_ssh = result_int

    #Exclude glob pattern filter
    result_int = []
    if exclude:
        for each in result_ssh:
            if exclude not in each['device']:
                result_int.append(each)
        result_ssh = result_int

    #All filters has been applied. Now searching for ro mounts
    ro_mounts_dirs_string = ""
    for each in result_ssh:
        if "ro" in each['opts'].split(','):
            ro_mounts_dirs_string = ro_mounts_dirs_string + each['device'] + ", "
    if len(ro_mounts_dirs_string) >=2:
        ro_mounts_dirs_string = ro_mounts_dirs_string[:-2]

    if ro_mounts_dirs_string != "":
        print "RO_MOUNTS CRITICAL - Found ro mounts: "+ro_mounts_dirs_string
        sys.exit(2)
    else:
        if (not skipdate or skipdate == False):
            #Here we are going to pipe current system date to each filesystem then try to get it back.
            failed_fs = []
            skipped_types = ['proc', 'sys', 'tmpfs', 'devpts', 'pts', 'sysfs', 'devtmpfs', 'fusectl', 'debugfs', 'securityfs', 'rpc_pipefs', 'binfmt_misc', 'usbfs', 'sunrpc', 'none']
            for eachFS in result_ssh:
                if eachFS['type'] not in skipped_types:
                    #print eachFS['mountpoint']
                    current_date = datetime.datetime.now()
                    mp = eachFS['mountpoint']
                    if mp == '/':
                        mp = ''
                        SSH_COMMAND = "sudo echo %s > %s/zenoss_date" % (current_date, mp)
                    else:
                        SSH_COMMAND = "echo %s > %s/zenoss_date" % (current_date, mp)
                    SSH_COMMAND = "echo %s > %s/zenoss_date" % (current_date, mp)
                    result_ssh = execute_ssh_command(SSH_COMMAND, remote_host, remote_username, remote_port)
                    #Here we should check piped date...
                    SSH_COMMAND = 'cat %s/zenoss_date' % (mp)
                    result_ssh = execute_ssh_command(SSH_COMMAND, remote_host, remote_username, remote_port)
                    if str(current_date) in result_ssh:
                        pass
                    else:
                        failed_fs.append(eachFS)
            if (len(failed_fs) == 0):
                print "RO_MOUNTS OK - No ro mounts found"
                sys.exit(0)
            else:
                ro_mounts_string = ''
                for eachFS in failed_fs:
                    ro_mounts_string += ' '
                    ro_mounts_string += eachFS['mountpoint']
                print "RO_MOUNTS CRITICAL - Found ro mounts: %s" % (ro_mounts_string)
        else:
            print "RO_MOUNTS OK - No ro mounts found"
            sys.exit(0)

except None, e:
    print "RO_MOUNTS UNKNOWN - ",e
    sys.exit(3)










































###
