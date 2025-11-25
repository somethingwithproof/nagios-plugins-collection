"""Pytest configuration and fixtures for nagios-plugins-collection tests."""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_ssh_client():
    """Create a mock SSH client for testing SSH-based plugins."""
    with patch("paramiko.SSHClient") as mock:
        client = MagicMock()
        mock.return_value = client

        # Mock successful connection
        client.connect.return_value = None

        # Mock exec_command with default successful output
        stdin = MagicMock()
        stdout = MagicMock()
        stderr = MagicMock()

        stdout.read.return_value = b""
        stderr.read.return_value = b""

        client.exec_command.return_value = (stdin, stdout, stderr)

        yield client


@pytest.fixture
def mock_httpx_client():
    """Create a mock httpx client for testing HTTP-based plugins."""
    with patch("httpx.Client") as mock:
        client = MagicMock()
        mock.return_value.__enter__.return_value = client

        response = MagicMock()
        response.status_code = 200
        response.text = ""
        response.content = b""
        response.headers = {}
        response.json.return_value = {}

        client.get.return_value = response
        client.post.return_value = response
        client.head.return_value = response

        yield client, response


@pytest.fixture
def sample_ps_output():
    """Sample ps command output for process checking tests."""
    return """UID        PID  PPID    VSZ   RSS STAT     TIME %CPU COMMAND
root         1     0   2396   768 Ss     0:00  0.0 init
root         2     0      0     0 S<     0:00  0.0 kthreadd
nagios    1234     1  10240  5120 Ss     0:01  0.5 nagios
apache    2345     1  51200 25600 S      0:05  1.2 httpd
apache    2346  2345  51200 12800 S      0:02  0.3 httpd
mysql     3456     1 524288 262144 Ssl    5:00 15.0 mysqld
"""


@pytest.fixture
def sample_mounts_output():
    """Sample /proc/mounts output for mount checking tests."""
    return """/dev/sda1 / ext4 rw,relatime,errors=remount-ro 0 0
tmpfs /tmp tmpfs rw,nosuid,nodev 0 0
/dev/sdb1 /data ext4 ro,relatime 0 0
proc /proc proc rw,nosuid,nodev,noexec 0 0
"""


@pytest.fixture
def sample_mongodb_status():
    """Sample MongoDB serverStatus response."""
    return {
        "version": "6.0.12",
        "uptime": 86400,
        "connections": {
            "current": 50,
            "available": 950,
            "totalCreated": 1000,
        },
        "mem": {
            "resident": 512,
            "virtual": 1024,
        },
    }


@pytest.fixture
def sample_hadoop_jmx():
    """Sample Hadoop JMX response."""
    return {
        "beans": [
            {
                "name": "Hadoop:service=NameNode,name=FSNamesystemState",
                "NumLiveDataNodes": 5,
                "NumDeadDataNodes": 0,
                "CapacityTotal": 1099511627776,  # 1TB
                "CapacityUsed": 549755813888,  # 500GB
            }
        ]
    }


@pytest.fixture
def sample_jobs_status():
    """Sample job status JSON response."""
    return {
        "status": "ok",
        "title": "System Status",
        "message": "All systems operational",
        "components": [
            {"name": "database", "status": "ok", "message": ""},
            {"name": "cache", "status": "ok", "message": ""},
            {"name": "api", "status": "ok", "message": ""},
        ],
    }
