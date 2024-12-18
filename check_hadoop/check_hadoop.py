#!/usr/bin/env python3

import sys
import json
import subprocess
import logging
import argparse

# Configure logging
logging.basicConfig(filename='hadoop_checker.log', level=logging.ERROR)

class HadoopHealthChecker:
    OK = 'OK'
    WARNING = 'WARNING'
    CRITICAL = 'CRITICAL'
    UNKNOWN = 'UNKNOWN'

    def __init__(self):
        self.version = self.get_hadoop_version()

    def get_hadoop_version(self) -> str:
        try:
            output = subprocess.check_output(['hadoop', 'version'], 
                                             stderr=subprocess.PIPE, 
                                             encoding='utf-8')
            version = output.splitlines()[0].split(' ')[1]
        except subprocess.CalledProcessError as e:
            logging.error(f"Error getting Hadoop version: {e}") 
            version = 'unknown'
        return version

    def check_hadoop(self) -> tuple:
        try:
            output = subprocess.check_output(['hadoop', 'health', '-json'], 
                                             stderr=subprocess.PIPE, 
                                             encoding='utf-8')
            health_data = json.loads(output)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running 'hadoop health': {e}")
            return (self.UNKNOWN, f"Error running 'hadoop health': {e.stderr}")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON output: {e}")
            return (self.UNKNOWN, "Error decoding JSON output from 'hadoop health'")

        status = health_data.get('status', self.UNKNOWN)
        message = health_data.get('message', 'No message returned')

        if status == 'GOOD':
            return (self.OK, f'Hadoop {self.version} is healthy: {message}')
        elif status == 'CONCERNING':
            return (self.WARNING, f'Hadoop {self.version} is concerning: {message}')
        elif status == 'BAD':
            return (self.CRITICAL, f'Hadoop {self.version} is in a bad state: {message}')
        else:
            return (self.UNKNOWN, f'Hadoop {self.version} is in an unknown state: {message}')

    def check_hdfs_capacity(self) -> tuple:
        try:
            output = subprocess.check_output(['hdfs', 'dfsadmin', '-report'],
                                             stderr=subprocess.PIPE,
                                             encoding='utf-8')
            # (Simplified) Parse output to find capacity information
            for line in output.splitlines():
                if "DFS Used%" in line:
                    capacity_used_percent = float(line.split()[-2].rstrip('%')) 
                    break
            else:
                return (self.UNKNOWN, "Could not determine HDFS capacity")

            if capacity_used_percent > 90: 
                return (self.WARNING, f"HDFS capacity is high: {capacity_used_percent}% used")
            else:
                return (self.OK, f"HDFS capacity: {capacity_used_percent}% used")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking HDFS capacity: {e}")
            return (self.UNKNOWN, f"Error checking HDFS capacity: {e.stderr}")


    def check_datanode_status(self) -> tuple:
        try:
            output = subprocess.check_output(['hdfs', 'dfsadmin', '-report'],
                                             stderr=subprocess.PIPE,
                                             encoding='utf-8')
            # (Simplified) Parse output to find live datanodes
            for line in output.splitlines():
                if "Live datanodes" in line:
                    live_datanodes = int(line.split(':')[1].strip())
                    break
            else:
                return (self.UNKNOWN, "Could not determine live DataNodes")

            if live_datanodes == 0:
                return (self.CRITICAL, "No live DataNodes found!")
            else:
                return (self.OK, f"{live_datanodes} live DataNodes found")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking DataNode status: {e}")
            return (self.UNKNOWN, f"Error checking DataNode status: {e.stderr}")

    def format_output(self, status, message):
        return f'{status} - {message}' 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check Hadoop health')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    hadoop_checker = HadoopHealthChecker()

    if args.verbose:
        print(f"Hadoop Version: {hadoop_checker.version}")

    status, message = hadoop_checker.check_hadoop()
    print(hadoop_checker.format_output(status, message))

    hdfs_status, hdfs_message = hadoop_checker.check_hdfs_capacity()
    print(hadoop_checker.format_output(hdfs_status, hdfs_message))

    datanode_status, datanode_message = hadoop_checker.check_datanode_status()
    print(hadoop_checker.format_output(datanode_status, datanode_message))

    # Exit with the most severe status
    exit_code = {
        HadoopHealthChecker.OK: 0,
        HadoopHealthChecker.WARNING: 1,
        HadoopHealthChecker.CRITICAL: 2,
        HadoopHealthChecker.UNKNOWN: 3
    }.get(status, 3)  # Default to UNKNOWN if status is not found

    sys.exit(exit_code)
