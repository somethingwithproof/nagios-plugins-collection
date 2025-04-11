# MongoDB Health Check Plugin for Nagios

A Nagios plugin to monitor the health of MongoDB instances by querying their status API.

## Features

- Checks MongoDB engine status
- Verifies specific components are in the expected state
- Supports multiple check modes for different levels of validation
- Provides performance metrics for monitoring
- Supports JSON output format
- Handles authentication and SSL connections
- Includes detailed error reporting

## Requirements

- Python 3.8 or higher
- httpx
- rich

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/thomasvincent/nagios-plugins-collection.git
cd nagios-plugins-collection/check_monghealth

# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x check_monghealth_modernized.py
```

### For Nagios

```bash
# Copy the script to the Nagios plugins directory
cp check_monghealth_modernized.py /usr/local/nagios/libexec/check_monghealth

# Make it executable
chmod +x /usr/local/nagios/libexec/check_monghealth
```

## Usage

```bash
./check_monghealth_modernized.py --host HOSTNAME [options]
```

### Command-line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | MongoDB host (required) | - |
| `--port` | MongoDB port | 27017 |
| `--timeout` | Connection timeout in seconds | 5 |
| `--username` | MongoDB username | - |
| `--password` | MongoDB password | - |
| `--ssl` | Use SSL | False |
| `--mode` | Check mode (1: basic, 2: extended, 3: full) | 1 |
| `--json` | Output in JSON format | False |
| `--verbose` | Increase verbosity (can be used multiple times) | 0 |

### Check Modes

1. **Basic (Mode 1)**: Checks `mongrations_current` and `search_reachable`
2. **Extended (Mode 2)**: Checks `search_reachable` and `site_api_reachable`
3. **Full (Mode 3)**: Checks all components (`mongrations_current`, `search_reachable`, and `site_api_reachable`)

### Examples

Basic check:
```bash
./check_monghealth_modernized.py --host mongodb.example.com
```

Extended check with authentication:
```bash
./check_monghealth_modernized.py --host mongodb.example.com --mode 2 --username admin --password secret
```

Full check with SSL and JSON output:
```bash
./check_monghealth_modernized.py --host mongodb.example.com --mode 3 --ssl --json
```

## Output

### Standard Output

```
OK - All MongoDB components are healthy | alive=1 mongrations_current=1 search_reachable=1
```

### JSON Output

```json
{
  "status": "OK",
  "message": "All MongoDB components are healthy",
  "metrics": {
    "alive": 1,
    "mongrations_current": 1,
    "search_reachable": 1
  },
  "details": {
    "alive": true,
    "mongrations_current": true,
    "search_reachable": true,
    "version": "5.0.14"
  }
}
```

## Nagios Configuration

### Command Definition

```
define command {
    command_name    check_mongodb_health
    command_line    $USER1$/check_monghealth --host=$ARG1$ --port=$ARG2$ --mode=$ARG3$
}
```

### Service Definition

```
define service {
    use                     generic-service
    host_name               mongodb-server
    service_description     MongoDB Health
    check_command           check_mongodb_health!mongodb.example.com!27017!1
    notifications_enabled   1
}
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure MongoDB is running and the port is correct
2. **Authentication Failed**: Verify username and password
3. **SSL Error**: Ensure SSL is properly configured on the MongoDB server
4. **Timeout**: Increase the timeout value for slow connections

### Debugging

Use the `--verbose` option to increase logging detail:

```bash
./check_monghealth_modernized.py --host mongodb.example.com --verbose --verbose
```

## License

MIT License - See the LICENSE file for details.
