"""Tests for the check_ro_mounts plugin."""

import pytest
from unittest.mock import MagicMock, patch

from nagios_plugins.base import Status
from nagios_plugins.check_ro_mounts import CheckROMounts, Mount


class TestMount:
    """Tests for the Mount dataclass."""

    def test_mount_creation(self):
        """Test creating a Mount instance."""
        mount = Mount(
            device="/dev/sda1",
            mountpoint="/",
            fstype="ext4",
            options="rw,relatime",
        )
        assert mount.device == "/dev/sda1"
        assert mount.mountpoint == "/"
        assert mount.fstype == "ext4"

    def test_is_readonly_false(self):
        """Test is_readonly returns False for rw mount."""
        mount = Mount(
            device="/dev/sda1",
            mountpoint="/",
            fstype="ext4",
            options="rw,relatime,errors=remount-ro",
        )
        assert mount.is_readonly is False

    def test_is_readonly_true(self):
        """Test is_readonly returns True for ro mount."""
        mount = Mount(
            device="/dev/sdb1",
            mountpoint="/data",
            fstype="ext4",
            options="ro,relatime",
        )
        assert mount.is_readonly is True


class TestCheckROMounts:
    """Tests for the CheckROMounts plugin."""

    @pytest.fixture
    def plugin(self):
        """Create a CheckROMounts instance for testing."""
        return CheckROMounts()

    def test_parse_mounts(self, plugin, sample_mounts_output):
        """Test parsing mount output."""
        mounts = plugin._parse_mounts(sample_mounts_output.splitlines())

        assert len(mounts) == 4

        # Check first mount
        assert mounts[0].device == "/dev/sda1"
        assert mounts[0].mountpoint == "/"
        assert mounts[0].fstype == "ext4"
        assert mounts[0].is_readonly is False

        # Check read-only mount
        ro_mount = next(m for m in mounts if m.mountpoint == "/data")
        assert ro_mount.is_readonly is True

    def test_filter_mounts_by_type(self, plugin, sample_mounts_output):
        """Test filtering mounts by filesystem type."""
        mounts = plugin._parse_mounts(sample_mounts_output.splitlines())

        # Exclude tmpfs
        filtered = plugin._filter_mounts(mounts, exclude_types=["tmpfs"])
        assert len(filtered) == 3
        assert not any(m.fstype == "tmpfs" for m in filtered)

    def test_filter_mounts_by_include(self, plugin, sample_mounts_output):
        """Test filtering mounts by include list."""
        mounts = plugin._parse_mounts(sample_mounts_output.splitlines())

        # Include only specific mounts
        filtered = plugin._filter_mounts(mounts, include=["/", "/data"])
        assert len(filtered) == 2
        assert set(m.mountpoint for m in filtered) == {"/", "/data"}

    def test_filter_mounts_by_exclude(self, plugin, sample_mounts_output):
        """Test filtering mounts by exclude list."""
        mounts = plugin._parse_mounts(sample_mounts_output.splitlines())

        # Exclude specific mounts
        filtered = plugin._filter_mounts(mounts, exclude=["/proc"])
        assert len(filtered) == 3
        assert not any(m.mountpoint == "/proc" for m in filtered)

    @patch("subprocess.run")
    def test_check_ok_all_rw(self, mock_run, plugin):
        """Test check returns OK when all mounts are read-write."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="/dev/sda1 / ext4 rw,relatime 0 0\n/dev/sdb1 /data ext4 rw,noatime 0 0\n",
        )

        args = MagicMock()
        args.host = "testhost"
        args.username = "nagios"
        args.port = 22
        args.mtab_path = "/proc/mounts"
        args.include = None
        args.exclude = None
        args.exclude_type = None
        args.warning = 0
        args.critical = 1
        args.timeout = 30

        result = plugin.check(args)

        assert result.status == Status.OK
        assert "read-write" in result.message

    @patch("subprocess.run")
    def test_check_critical_ro_mount(self, mock_run, plugin, sample_mounts_output):
        """Test check returns CRITICAL when read-only mounts are found."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=sample_mounts_output,
        )

        args = MagicMock()
        args.host = "testhost"
        args.username = "nagios"
        args.port = 22
        args.mtab_path = "/proc/mounts"
        args.include = None
        args.exclude = None
        args.exclude_type = ["tmpfs", "proc"]  # Filter virtual filesystems
        args.warning = 0
        args.critical = 1
        args.timeout = 30

        result = plugin.check(args)

        assert result.status == Status.CRITICAL
        assert "read-only" in result.message
        assert "/data" in result.message

    @patch("subprocess.run")
    def test_check_warning_threshold(self, mock_run, plugin, sample_mounts_output):
        """Test check returns WARNING when exceeding warning threshold."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=sample_mounts_output,
        )

        args = MagicMock()
        args.host = "testhost"
        args.username = "nagios"
        args.port = 22
        args.mtab_path = "/proc/mounts"
        args.include = None
        args.exclude = None
        args.exclude_type = ["tmpfs", "proc"]
        args.warning = 1  # 1 RO mount triggers warning
        args.critical = 2  # 2 RO mounts trigger critical
        args.timeout = 30

        result = plugin.check(args)

        assert result.status == Status.WARNING

    @patch("subprocess.run")
    def test_check_ssh_failure(self, mock_run, plugin):
        """Test check returns UNKNOWN on SSH failure."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Connection refused",
        )

        args = MagicMock()
        args.host = "testhost"
        args.username = "nagios"
        args.port = 22
        args.mtab_path = "/proc/mounts"
        args.include = None
        args.exclude = None
        args.exclude_type = None
        args.warning = 0
        args.critical = 1
        args.timeout = 30

        result = plugin.check(args)

        assert result.status == Status.UNKNOWN
