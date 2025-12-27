"""Tests for k8s node status plugin."""

from unittest.mock import patch

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_k8s_node_status import CheckK8sNodeStatus
from nagios_plugins.services.k8s import NodeSummary


def test_k8s_ok() -> None:
    plugin = CheckK8sNodeStatus()
    summary = NodeSummary(ready=3, not_ready=0, disk_pressure=0, memory_pressure=0, pid_pressure=0)
    with patch(
        "nagios_plugins.plugins.check_k8s_node_status.summarize_nodes", return_value=summary
    ):
        code = plugin.run(["--label", "node-role.kubernetes.io/worker=true"])
        assert code == Status.OK.value


def test_k8s_critical_when_not_ready() -> None:
    plugin = CheckK8sNodeStatus()
    summary = NodeSummary(ready=2, not_ready=1, disk_pressure=0, memory_pressure=0, pid_pressure=0)
    with patch(
        "nagios_plugins.plugins.check_k8s_node_status.summarize_nodes", return_value=summary
    ):
        code = plugin.run([])
        assert code == Status.CRITICAL.value
