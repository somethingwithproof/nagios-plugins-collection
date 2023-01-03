# DNS Lookup Script

This script connects to a remote server via ssh and performs a DNS lookup on the specified hostname or IP address. The script also calculates the response time of the DNS query and returns a status based on warning and critical threshold values.

## Requirements

- pynag
- pexpect

## Usage

```./dns_lookup_script.py -R ssh_host -P ssh_password -U ssh_username -s ssh_port -l query_address -p port -T record_type -a expected_address -A dig_arguments -w warning -c critical```


## Arguments

- `-R ssh_host`, `--ssh_host ssh_host`: Ssh remote machine name to connect to (required)
- `-P ssh_password`, `--ssh_password ssh_password`: Ssh remote host password
- `-U ssh_username`, `--ssh_username ssh_username`: Ssh remote username
- `-s ssh_port`, `--ssh_port ssh_port`: Ssh remote host port (default: 22)
- `-l query_address`, `--query_address query_address`: Machine name to lookup (required)
- `-p port`, `--port port`: DNS server port number (default: 53)
- `-T record_type`, `--record_type record_type`: Record type to lookup (default: A)
- `-a expected_address`, `--expected_address expected_address`: An address expected to be in the answer section. If not set, uses whatever was in query address
- `-A dig_arguments`, `--dig_arguments dig_arguments`: Pass the STRING as argument(s) to dig
- `-w warning`, `--warning warning`: Response time warning threshold (seconds)
- `-c critical`, `--critical critical`: Response time critical threshold (seconds)

## Output

The script will output a message and a status code based on the response time of the DNS query and the specified warning and critical thresholds. The output message will also include performance data in the format `time=Xs;

