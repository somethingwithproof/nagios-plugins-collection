# ETL Component Status Checker for Nagios

A Nagios plugin to monitor the status of ETL (Extract, Transform, Load) components by querying their status API.

## Features

- Checks ETL component status via JSON API
- Verifies components are in the expected state
- Monitors component update times
- Provides performance metrics for monitoring
- Supports JSON output format
- Handles authentication and SSL connections
- Includes detailed error reporting
- Asynchronous execution for improved performance

## Requirements

- Python 3.8 or higher
- httpx
- rich

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/thomasvincent/nagios-plugins-collection.git
cd nagios-plugins-collection/check_etl

# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x etl_modernized.py
```

### For Nagios

```bash
# Copy the script to the Nagios plugins directory
cp etl_modernized.py /usr/local/nagios/libexec/check_etl

# Make it executable
chmod +x /usr/local/nagios/libexec/check_etl
```

## Usage

```bash
./etl_modernized.py --host HOSTNAME --components COMPONENT1 [COMPONENT2 ...] [options]
```

### Command-line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Hostname of the ETL API server (required) | - |
| `--port` | Port number of the ETL API server | 80 |
| `--timeout` | Timeout in seconds for API requests | 10 |
| `--ssl` | Use HTTPS instead of HTTP | False |
| `--username` | Username for authentication | - |
| `--password` | Password for authentication | - |
| `--components` | List of component names to check (required) | - |
| `-t, --threshold` | Threshold in minutes for checking component update | 10 |
| `--json` | Output in JSON format | False |
| `-v, --verbose` | Increase verbosity (can be used multiple times) | 0 |

### Examples

Basic check:
```bash
./etl_modernized.py --host etl.example.com --components extract transform load
```

Check with authentication and SSL:
```bash
./etl_modernized.py --host etl.example.com --ssl --username admin --password secret --components extract transform load
```

Custom threshold and JSON output:
```bash
./etl_modernized.py --host etl.example.com --components extract transform load --threshold 30 --json
```

## Output

### Standard Output

```
OK - All 3 components are healthy | extract_status=1 extract_age_minutes=5.2 transform_status=1 transform_age_minutes=6.8 load_status=1 load_age_minutes=7.3
```

### JSON Output

```json
{
  "status": "OK",
  "message": "All 3 components are healthy",
  "metrics": {
    "extract_status": 1,
    "extract_age_minutes": 5.2,
    "transform_status": 1,
    "transform_age_minutes": 6.8,
    "load_status": 1,
    "load_age_minutes": 7.3
  },
  "timestamp": "2025-04-11T16:05:23",
  "details": {
    "extract": ["ok", "2025-04-11T16:00:05"],
    "transform": ["ok", "2025-04-11T15:58:30"],
    "load": ["ok", "2025-04-11T15:58:00"]
  }
}
```

## API Requirements

The ETL API should provide component status information at the following endpoint:

```
/api/component/{component_name}
```

The API should return a JSON response with the following structure:

```json
{
  "status": "ok",
  "updated": "2025-04-11T16:00:05"
}
```

Where:
- `status` is either "ok" or "error"
- `updated` is an ISO 8601 formatted timestamp

## Nagios Configuration

### Command Definition

```
define command {
    command_name    check_etl_components
    command_line    $USER1$/check_etl --host=$ARG1$ --components=$ARG2$ --threshold=$ARG3$
}
```

### Service Definition

```
define service {
    use                     generic-service
    host_name               etl-server
    service_description     ETL Components
    check_command           check_etl_components!etl.example.com!extract transform load!10
    notifications_enabled   1
}
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure the ETL API server is running and the port is correct
2. **Authentication Failed**: Verify username and password
3. **SSL Error**: Ensure SSL is properly configured on the ETL API server
4. **Timeout**: Increase the timeout value for slow connections
5. **Invalid Response**: Ensure the API returns the expected JSON format

### Debugging

Use the `--verbose` option to increase logging detail:

```bash
./etl_modernized.py --host etl.example.com --components extract transform load --verbose --verbose
```

## License

MIT License - See the LICENSE file for details.
