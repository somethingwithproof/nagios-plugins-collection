# Monitor Vertica

This script queries a Vertica database for various statistics and prints the results to the console.

## Requirements

- Python 3
- The `subprocess` and `shlex` modules

## Usage

To run the script, use the following command:
```python3 monitor_vertica.py```


The script will connect to the Vertica database and execute the specified queries, then print the results to the console.

## Configuration

The database connection parameters (hostname, username, password) are hardcoded in the script and can be modified as needed. The queries being executed can also be modified as needed.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.
