import pytest
import subprocess

"""
Test the main() function of the hadoop.py script.

The test scenarios are as follows:

1. No command-line arguments are provided (should exit with status code 3 and print usage information).
2. An invalid URL is provided (should exit with status code 2 and print an error message).
3. An URL that returns invalid JSON data is provided (should exit with status code 2 and print an error message).
4. An URL that returns valid JSON data but with a Hadoop status other than "ok" is provided (should exit with status code 1 and print a warning message).
5. An URL that returns valid JSON data with component statuses "ok" and with a time since last update within the acceptable range (specified with the -t argument) is provided (should exit with status code 0 and print the memory usage).
6. An URL that returns valid JSON data with component statuses "ok" and with a time since last update outside the acceptable range (specified with the -t argument) is provided (should exit with status code 1 and print a warning message).
"""


def test_main():
    # Test with no arguments
    result = subprocess.run(["python", "hadoop.py"], capture_output=True)
    assert result.returncode == 3
    assert "Usage:" in result.stderr.decode()
    
    # Test with invalid URL
    result = subprocess.run(["python", "hadoop.py", "-url=invalid_url"], capture_output=True)
    assert result.returncode == 2
    assert "CRITICAL - Could not retrieve JSON data from specified URL" in result.stderr.decode()
    
    # Test with invalid JSON data
    result = subprocess.run(["python", "hadoop.py", "-url=http://example.com"], capture_output=True)
    assert result.returncode == 2
    assert "CRITICAL - Could not retrieve JSON data from specified URL" in result.stderr.decode()
    
    # Test with valid JSON data but Hadoop status other than "ok"
    result = subprocess.run(["python", "hadoop.py
    # Test with valid JSON data but component status other than "ok"
    result = subprocess.run(["python", "hadoop.py", "-url=http://borovcov.ru/api/component/hadoop"], capture_output=True)
    assert result.returncode == 1
    assert "WARNING - component" in result.stderr.decode()
    
    # Test with valid JSON data, component statuses "ok", and time since last update within acceptable range
    result = subprocess.run(["python", "hadoop.py", "-url=http://borovcov.ru/api/component/hadoop", "-t=60"], capture_output=True)
    assert result.returncode == 0
    assert "OK - mem:" in result.stdout.decode()
    
    # Test with valid JSON data, component statuses "ok", and time since last update outside acceptable range
    result = subprocess.run(["python", "hadoop.py", "-url=http://borovcov.ru/api/component/hadoop", "-t=1"], capture_output=True)
    assert result.returncode == 1
    assert "WARNING - Component" in result.stderr.decode()
