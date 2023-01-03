# Component Checker

This script retrieves the status and updated time of a component from an API and checks if the time since the last update is within a specified limit.

## Usage

```python component_checker.py -url=URL -component=COMPONENT -t=MAX_TIME```


Where:
- `URL` is the URL of the hostname.
- `COMPONENT` is the name of the component.
- `MAX_TIME` is the maximum time (in minutes) since the last update.

## Output

The script will print one of the following messages and exit with the corresponding exit code:

- `OK - Time since last update is less than MAX_TIME minutes`: The time since the last update is within the specified limit.
- `WARNING - Time since last update is greater than MAX_TIME minutes`: The time since the last update is greater than the specified limit.
- `CRITICAL - MESSAGE`: An error occurred while retrieving the status and updated time from the API. `MESSAGE` is the error message.

## Example

```python component_checker.py -url=example.com -component=component1 -t=30```


This will retrieve the status and updated time of the `component1` from the API at `http://example.com/api/component/component1` and check if the time since the last update is within 30 minutes.

