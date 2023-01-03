#!/opt/zenoss/bin/python

#Script dependencies:
# pynag, subprocess

import os,sys, subprocess, re
from pynag.Plugins import WARNING, CRITICAL, OK, UNKNOWN, simple as Plugin
from pexpect import ANSI, fdpexpect, FSM, pexpect, pxssh, screen

def parse_args():
    np = Plugin()

    #Configure additional command line arguments
    np.add_arg("R", "ssh_host", "Ssh remote machine name to connect to", required=True)
    np.add_arg("P", "ssh_password", "Ssh romote host password", required=None)
    np.add_arg("U", "ssh_username", "Ssh remote username", required=None)
    np.add_arg("s", "ssh_port", "Ssh remote host port (default: 22)", required=None)
    np.add_arg("l", "query_address", "Machine name to lookup", required=True)
    np.add_arg("p", "port", "DNS Server port number (default: 53)", required=None)
    np.add_arg("T", "record_type", "Record type to lookup (default: A)", required=None)
    np.add_arg("a", "expected_address", "An address expected to be in the answer section. If not set, uses whatever was in query address", required=None)
    np.add_arg("A", "dig-arguments", "Pass the STRING as argument(s) to dig", required=None)

    #Plugin activation
    np.activate()
    return np

def execute_plugin(ssh_module, dns_module, output_module, ssh_host, ssh_password, ssh_username, ssh_port, query_address, port, record_type, expected_address, dig_arguments, warning, critical):
    #Data gathering
    if query_address:
        CMD_ITEM_4 = query_address

    if  (ssh_host and port):
        CMD_ITEM_2 = "@"+ssh_host
        CMD_ITEM_3 = "-p "+port

    if record_type:
        CMD_ITEM_5 = "-t "+record_type

    if dig_arguments:
        CMD_ITEM_6 = dig_arguments

    #SSH Section
    ssh_port=22
    result_ssh=''
    if ssh_port:
        ssh_port = ssh_port
    else:
        ssh_port = 22

    ssh_username= "zenoss"
    if ssh_username:
        ssh_username = ssh_username
    else:
        ssh_username = "zenoss"

    if not warning:
        warning = 0
    if not critical:
        critical = 0

    def mycheck(value):
        if value > int(critical) and critical:
            output_module.print_and_exit("DNS CRITICAL - "+str(value)+"s response time|time="+str(value)+"s;"+str(float(warning))+";;"+str(float(critical)), CRITICAL)
        if int(warning) == 0 and int(critical) == 0:
            output_module.print_and_exit("DNS CRITICAL - "+str(value)+"s response time|time="+str(value)+"s;"+str(float(warning))+";;"+str(float(critical)), CRITICAL)
        if value in range(int(warning),int(critical),1):
            output_module.print_and_exit("DNS WARNING - "+str(value)+"s response time|time="+str(value)+"s;"+str(float(warning))+";;"+str(float(critical)), WARNING)
        if value < int(warning) and warning:
            output_module.print_and_exit("DNS OK - "+str(value)+"s response time|time="+str(value)+"s;"+str(float(warning))+";;"+str(float(critical)), OK)
        else:
            output_module.print_and_exit("DNS UNKNOWN - "+str(value)+"s response time|time="+str(value)+"s;"+str(float(warning))+";;"+str(float(critical)), UNKNOWN)

    #Login to remote host
    try:
        ssh_module.login(ssh_host, ssh_username, ssh_password, ssh_port)
    except:
        output_module.print_and_exit("SSH login to "+ssh_host+" failed", UNKNOWN)

        #DNS Query
        try:
            result_ssh = ssh_module.run_dns_query(CMD_ITEM_1+CMD_ITEM_2+CMD_ITEM_3+CMD_ITEM_4+CMD_ITEM_5+CMD_ITEM_6)
        except:
            output_module.print_and_exit("DNS query failed", UNKNOWN)

        #Response time calculation
        response_time = dns_module.get_response_time(result_ssh)

        #Check if the expected address is in the answer section
        if expected_address:
            if dns_module.check_expected_address(result_ssh, expected_address):
                mycheck(response_time)
            else:
                output_module.print_and_exit("DNS CRITICAL - expected address not found in answer section", CRITICAL)
        else:
            mycheck(response_time)
    except:
        output_module.print_and_exit("DNS UNKNOWN - "+str(sys.exc_info()[0]), UNKNOWN)

if __name__ == '__main__':
    np = parse_args()
    execute_plugin(ssh_module, dns_module, output_module, np['ssh_host'], np['ssh_password'], np['ssh_username'], np['ssh_port'], np['query_address'], np['port'], np['record_type'], np['expected_address'], np['dig-arguments'], np['warning'], np['critical'])


