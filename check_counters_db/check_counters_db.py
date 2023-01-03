#!/usr/bin/env python3

import subprocess
import shlex

def main():
    cmd1 = """select count(*) from nodes where node_state = 'DOWN';"""
    cmd2 = """select count(*) from active_events where event_code_description = 'Too Many ROS Containers';"""
    cmd3 = """select count(*) from active_events where event_code_description = 'Recovery Failure';"""
    cmd4 = """select count(*) from active_events where event_code_description = 'Stale Checkpoint';"""

    cmd1_prepared = "/opt/vertica/bin/vsql -h vertica01 -U zenoss -w blahbalh -c" + cmd1
    cmd1_prepared = shlex.split(cmd1_prepared)

    cmd2_prepared = "/opt/vertica/bin/vsql -h vertica01 -U zenoss -w blahbalh -c" + cmd2
    cmd2_prepared = shlex.split(cmd2_prepared)

    cmd3_prepared = "/opt/vertica/bin/vsql -h vertica01 -U zenoss -w blahbalh -c" + cmd3
    cmd3_prepared = shlex.split(cmd3_prepared)

    cmd4_prepared = "/opt/vertica/bin/vsql -h vertica01 -U zenoss -w blahbalh -c" + cmd4
    cmd4_prepared = shlex.split(cmd4_prepared)

    vertica = subprocess.run(cmd1_prepared, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result1 = vertica.stdout.decode().strip()

    vertica = subprocess.run(cmd2_prepared, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result2 = vertica.stdout.decode().strip()

    vertica = subprocess.run(cmd3_prepared, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result3 = vertica.stdout.decode().strip()

    vertica = subprocess.run(cmd4_prepared, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result4 = vertica.stdout.decode().strip()

    print("R1:", result1)
    print("R2:", result2)
    print("R3:", result3)
    print("R4:", result4)

if __name__ == '__main__':
    main()

