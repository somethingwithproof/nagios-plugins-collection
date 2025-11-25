"""Tests for the check_procs plugin."""

import pytest
from unittest.mock import MagicMock, patch

from nagios_plugins.base import Status
from nagios_plugins.check_procs import CheckProcs, Process


class TestProcess:
    """Tests for the Process dataclass."""

    def test_process_creation(self):
        """Test creating a Process instance."""
        proc = Process(
            uid="root",
            pid="1",
            parent_pid="0",
            vsz="2396",
            rss="768",
            status="Ss",
            time="0:00",
            pcpu="0.0",
            command="init",
        )
        assert proc.uid == "root"
        assert proc.pid == "1"
        assert proc.command == "init"


class TestCheckProcs:
    """Tests for the CheckProcs plugin."""

    @pytest.fixture
    def plugin(self):
        """Create a CheckProcs instance for testing."""
        return CheckProcs()

    def test_parse_ps_output(self, plugin, sample_ps_output):
        """Test parsing ps command output."""
        processes = plugin._parse_ps_output(sample_ps_output.splitlines())

        # Should have 6 processes (header line is skipped)
        assert len(processes) == 6

        # Check first process
        assert processes[0].uid == "root"
        assert processes[0].pid == "1"
        assert processes[0].command == "init"

        # Check a process with higher CPU
        mysqld = next(p for p in processes if p.command == "mysqld")
        assert mysqld.pcpu == "15.0"

    def test_filter_by_status(self, plugin, sample_ps_output):
        """Test filtering processes by status flags."""
        processes = plugin._parse_ps_output(sample_ps_output.splitlines())

        # Filter for sleeping processes (S flag)
        sleeping = plugin._filter_processes(processes, status_flags=["S"])
        assert len(sleeping) > 0
        assert all("S" in p.status for p in sleeping)

        # Filter for zombie processes (Z flag) - none in sample
        zombies = plugin._filter_processes(processes, status_flags=["Z"])
        assert len(zombies) == 0

    def test_filter_by_ppid(self, plugin, sample_ps_output):
        """Test filtering processes by parent PID."""
        processes = plugin._parse_ps_output(sample_ps_output.splitlines())

        # Filter for children of PID 1
        children = plugin._filter_processes(processes, ppid="1")
        assert len(children) > 0
        assert all(p.parent_pid == "1" for p in children)

    def test_filter_by_vsz(self, plugin, sample_ps_output):
        """Test filtering processes by VSZ."""
        processes = plugin._parse_ps_output(sample_ps_output.splitlines())

        # Filter for processes with VSZ > 50000
        large_vsz = plugin._filter_processes(processes, vsz_min=50000)
        assert len(large_vsz) > 0
        assert all(int(p.vsz) > 50000 for p in large_vsz)

    def test_filter_by_cpu(self, plugin, sample_ps_output):
        """Test filtering processes by CPU usage."""
        processes = plugin._parse_ps_output(sample_ps_output.splitlines())

        # Filter for processes with CPU > 1%
        high_cpu = plugin._filter_processes(processes, pcpu_min=1.0)
        assert len(high_cpu) > 0
        assert all(float(p.pcpu) > 1.0 for p in high_cpu)

    @patch("nagios_plugins.check_procs.HAS_PARAMIKO", True)
    def test_check_ok(self, plugin, mock_ssh_client, sample_ps_output):
        """Test check returns OK when within thresholds."""
        with patch.object(plugin, "_get_ssh_connection", return_value=mock_ssh_client):
            mock_ssh_client.exec_command.return_value[1].read.return_value = (
                sample_ps_output.encode()
            )

            args = MagicMock()
            args.host = "testhost"
            args.port = 22
            args.username = "nagios"
            args.password = None
            args.identity_file = None
            args.timeout = 30
            args.command = None
            args.status_flags = None
            args.ppid = None
            args.vsz = None
            args.rss = None
            args.pcpu = None
            args.warning = "10"
            args.critical = "20"

            result = plugin.check(args)

            assert result.status == Status.OK
            assert "processes" in result.message

    @patch("nagios_plugins.check_procs.HAS_PARAMIKO", True)
    def test_check_warning(self, plugin, mock_ssh_client, sample_ps_output):
        """Test check returns WARNING when exceeding warning threshold."""
        with patch.object(plugin, "_get_ssh_connection", return_value=mock_ssh_client):
            mock_ssh_client.exec_command.return_value[1].read.return_value = (
                sample_ps_output.encode()
            )

            args = MagicMock()
            args.host = "testhost"
            args.port = 22
            args.username = "nagios"
            args.password = None
            args.identity_file = None
            args.timeout = 30
            args.command = None
            args.status_flags = None
            args.ppid = None
            args.vsz = None
            args.rss = None
            args.pcpu = None
            args.warning = "3"  # Sample has 6 processes
            args.critical = "10"

            result = plugin.check(args)

            assert result.status == Status.WARNING

    @patch("nagios_plugins.check_procs.HAS_PARAMIKO", True)
    def test_check_critical(self, plugin, mock_ssh_client, sample_ps_output):
        """Test check returns CRITICAL when exceeding critical threshold."""
        with patch.object(plugin, "_get_ssh_connection", return_value=mock_ssh_client):
            mock_ssh_client.exec_command.return_value[1].read.return_value = (
                sample_ps_output.encode()
            )

            args = MagicMock()
            args.host = "testhost"
            args.port = 22
            args.username = "nagios"
            args.password = None
            args.identity_file = None
            args.timeout = 30
            args.command = None
            args.status_flags = None
            args.ppid = None
            args.vsz = None
            args.rss = None
            args.pcpu = None
            args.warning = "2"
            args.critical = "3"  # Sample has 6 processes

            result = plugin.check(args)

            assert result.status == Status.CRITICAL
