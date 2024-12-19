#!/usr/bin/env python3

import sys
import json
import subprocess
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.ERROR)

class HadoopHealthChecker:
    OK = 'OK'
    WARNING = 'WARNING'
    CRITICAL = 'CRITICAL'
    UNKNOWN = 'UNKNOWN'

    def __init__(self, hdfs_warning=90, hdfs_critical=95, verbose=False):
        self.hdfs_warning = hdfs_warning
        self.hdfs_critical = hdfs_critical
        self.verbose = verbose
        self.version = self.get_hadoop_version()
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

    def get_hadoop_version(self) -> str:
        try:
            output = subprocess.check_output(['hadoop', 'version'], stderr=subprocess.PIPE, encoding='utf-8')
            return output.splitlines()[0].split(' ')[1]
        except Exception as e:
            logging.error(f"Error fetching Hadoop version: {e}")
            return 'unknown'

    def check_hadoop(self) -> tuple:
        try:
            output = subprocess.check_output(['hadoop', 'health', '-json'], stderr=subprocess.PIPE, encoding='utf-8')
            health_data = json.loads(output)
            status = health_data.get('status', self.UNKNOWN)
            message = health_data.get('message', 'No message returned')
            return (self.OK if status == 'GOOD' else self.CRITICAL, message)
        except Exception as e:
            logging.error(f"Error checking Hadoop health: {e}")
            return (self.UNKNOWN, str(e))

    def check_hdfs_capacity(self) -> tuple:
        try:
            output = subprocess.check_output(['hdfs', 'dfsadmin', '-report'], stderr=subprocess.PIPE, encoding='utf-8')
            for line in output.splitlines():
                if "DFS Used%" in line:
                    capacity_used = float(line.split()[-2].strip('%'))
                    if capacity_used > self.hdfs_critical:
                        return (self.CRITICAL, f"HDFS capacity is critical: {capacity_used}% used")
                    elif capacity_used > self.hdfs_warning:
                        return (self.WARNING, f"HDFS capacity is warning: {capacity_used}% used")
                    return (self.OK, f"HDFS capacity: {capacity_used}% used")
            return (self.UNKNOWN, "Could not determine HDFS capacity")
        except Exception as e:
            logging.error(f"Error checking HDFS capacity: {e}")
            return (self.UNKNOWN, str(e))

    def check_datanode_status(self) -> tuple:
        try:
            output = subprocess.check_output(['hdfs', 'dfsadmin', '-report'], stderr=subprocess.PIPE, encoding='utf-8')
            for line in output.splitlines():
                if "Live datanodes" in line:
                    live_datanodes = int(line.split(':')[1].strip())
                    if live_datanodes == 0:
                        return (self.CRITICAL, "No live DataNodes found")
                    return (self.OK, f"{live_datanodes} live DataNodes found")
            return (self.UNKNOWN, "Could not determine DataNode status")
        except Exception as e:
            logging.error(f"Error checking DataNode status: {e}")
            return (self.UNKNOWN, str(e))

    def format_output(self, status, message, output_format):
        if output_format == 'json':
            return json.dumps({'status': status, 'message': message}, indent=2)
        return f'{status} - {message}'


def parse_args():
    parser = argparse.ArgumentParser(description='Hadoop Health Checker')
    parser.add_argument('--hdfs-warning', type=int, default=90, help='HDFS warning threshold (default: 90%)')
    parser.add_argument('--hdfs-critical', type=int, default=95, help='HDFS critical threshold (default: 95%)')
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format (default: text)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--check', choices=['hadoop', 'hdfs', 'datanode', 'all'], default='all', help='Select specific checks (default: all)')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    checker = HadoopHealthChecker(hdfs_warning=args.hdfs_warning, hdfs_critical=args.hdfs_critical, verbose=args.verbose)

    checks = {
        'hadoop': checker.check_hadoop,
        'hdfs': checker.check_hdfs_capacity,
        'datanode': checker.check_datanode_status
    }

    if args.check == 'all':
        selected_checks = checks.values()
    else:
        selected_checks = [checks[args.check]]

    results = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda check: check(), selected_checks))

    for status, message in results:
        print(checker.format_output(status, message, args.output))

    exit_code = max(
        ['OK', 'WARNING', 'CRITICAL', 'UNKNOWN'].index(r[0]) for r in results
    )
    sys.exit(exit_code)
