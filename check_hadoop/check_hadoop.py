#!/usr/bin/env python3

import sys
import json
import subprocess


class HadoopChecker:
    def __init__(self):
        self.version = self.get_hadoop_version()

    def get_hadoop_version(self) -> str:
        try:
            output = subprocess.check_output(['hadoop', 'version'], stderr=subprocess.STDOUT)
            version = output.decode('utf-8').splitlines()[0].split(' ')[1]
        except subprocess.CalledProcessError:
            version = 'unknown'
        return version

    def check_hadoop(self) -> tuple:
        try:
            output = subprocess.check_output(['hadoop', 'health', '-json'], stderr=subprocess.STDOUT)
            health_data = json.loads(output.decode('utf-8'))
        except (subprocess.CalledProcessError, json.decoder.JSONDecodeError):
            return ('UNKNOWN', 'Error running `hadoop health` command')

        status = health_data.get('status', 'UNKNOWN')
        message = health_data.get('message', 'No message returned')

        if status == 'GOOD':
            return ('OK', f'Hadoop {self.version} is healthy: {message}')
        elif status == 'CONCERNING':
            return ('WARNING', f'Hadoop {self.version} is concerning: {message}')
        elif status == 'BAD':
            return ('CRITICAL', f'Hadoop {self.version} is in a bad state: {message}')
        else:
            return ('UNKNOWN', f'Hadoop {self.version} is in an unknown state: {message}')


if __name__ == '__main__':
    hadoop_checker = HadoopChecker()
    status, message = hadoop_checker.check_hadoop()
    print(f'{status} - {message}')
    sys.exit(status)
