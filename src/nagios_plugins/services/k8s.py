from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NodeSummary:
    ready: int
    not_ready: int
    disk_pressure: int
    memory_pressure: int
    pid_pressure: int


def summarize_nodes(label_selector: str | None = None, timeout: int = 10) -> NodeSummary:
    try:
        # Optional dependency; import locally
        from kubernetes import client, config  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("kubernetes extra not installed") from e

    try:
        try:
            config.load_incluster_config()
        except Exception:
            config.load_kube_config()
        api = client.CoreV1Api()
        ret = api.list_node(label_selector=label_selector, _request_timeout=timeout)
        ready = not_ready = disk = mem = pid = 0
        for n in ret.items:
            conditions = {c.type: c.status for c in (n.status.conditions or [])}
            if conditions.get("Ready") == "True":
                ready += 1
            else:
                not_ready += 1
            if conditions.get("DiskPressure") == "True":
                disk += 1
            if conditions.get("MemoryPressure") == "True":
                mem += 1
            if conditions.get("PIDPressure") == "True":
                pid += 1
        return NodeSummary(
            ready=ready,
            not_ready=not_ready,
            disk_pressure=disk,
            memory_pressure=mem,
            pid_pressure=pid,
        )
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"k8s API error: {e}") from e
