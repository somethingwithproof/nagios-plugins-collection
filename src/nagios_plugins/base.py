#!/usr/bin/env python3
"""Base module for Nagios plugins."""

from __future__ import annotations

import argparse
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

install_rich_traceback(show_locals=True)


class Status(Enum):
    """Nagios status codes."""

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    @classmethod
    def from_string(cls, s: str) -> "Status":
        return {
            "OK": cls.OK,
            "WARNING": cls.WARNING,
            "CRITICAL": cls.CRITICAL,
            "UNKNOWN": cls.UNKNOWN,
        }.get(s.upper(), cls.UNKNOWN)

    def __str__(self) -> str:
        return self.name


@dataclass
class CheckResult:
    """Stores check results with status, message, and optional metrics."""

    status: Status
    message: str
    metrics: dict[str, Any] = field(default_factory=dict)
    details: str | None = None
    timestamp: float = field(default_factory=time.time)

    def __str__(self) -> str:
        output = f"{self.status} - {self.message}"
        if self.metrics:
            output += f" | {' '.join(f'{k}={v}' for k, v in self.metrics.items())}"
        if self.details:
            output += f"\n{self.details}"
        return output

    def to_json(self) -> str:
        d = asdict(self)
        d["status"] = self.status.name
        d["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        return json.dumps(d, indent=2)


class NagiosPlugin(ABC):
    """Base class for Nagios plugins with argument parsing, logging, and output formatting."""

    def __init__(self) -> None:
        self.parser = self._create_argument_parser()
        self.console = Console(stderr=True)
        self.logger = logging.getLogger(self.__class__.__name__)
        for h in self.logger.handlers[:]:
            self.logger.removeHandler(h)
        self.logger.addHandler(RichHandler(console=self.console, rich_tracebacks=True))
        self.logger.setLevel(logging.WARNING)
        self.start_time = time.time()

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description=self.__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument("-v", "--verbose", action="count", default=0)
        parser.add_argument("-t", "--timeout", type=int, default=30)
        parser.add_argument("-w", "--warning", help="Warning threshold")
        parser.add_argument("-c", "--critical", help="Critical threshold")
        parser.add_argument("--json", action="store_true", help="JSON output")
        return parser

    def parse_args(self, args: list[str] | None = None) -> argparse.Namespace:
        parsed = self.parser.parse_args(args)
        if parsed.verbose == 1:
            self.logger.setLevel(logging.INFO)
        elif parsed.verbose >= 2:
            self.logger.setLevel(logging.DEBUG)
        return parsed

    @abstractmethod
    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the check. Implement in subclasses."""

    def run(self, args: list[str] | None = None) -> int:
        try:
            parsed = self.parse_args(args)
            result = self.check(parsed)
            print(result.to_json() if parsed.json else str(result))
            return result.status.value
        except Exception as e:
            self.logger.exception("Unhandled exception")
            result = CheckResult(Status.UNKNOWN, f"Error: {e}")
            print(
                result.to_json()
                if "parsed" in locals() and getattr(parsed, "json", False)
                else str(result)
            )
            return Status.UNKNOWN.value


class ThresholdRange:
    """Nagios threshold range (e.g., '10', '10:', '@10:20')."""

    def __init__(
        self, min_val: float | None = None, max_val: float | None = None, inclusive: bool = False
    ):
        self.min_value = min_val
        self.max_value = max_val
        self.inclusive = inclusive

    @classmethod
    def from_string(cls, s: str) -> "ThresholdRange":
        if not s:
            return cls()
        inclusive = s.startswith("@")
        if inclusive:
            s = s[1:]
        if ":" not in s:
            return cls(None, float(s), inclusive)
        parts = s.split(":")
        min_val = float(parts[0]) if parts[0] else None
        max_val = float(parts[1]) if parts[1] else None
        return cls(min_val, max_val, inclusive)

    def check(self, value: float) -> bool:
        """Returns True if value is OK (not in alert state)."""
        if self.inclusive:
            if self.min_value is not None and self.max_value is not None:
                return not (self.min_value < value < self.max_value)
            elif self.min_value is not None:
                return not (value > self.min_value)
            elif self.max_value is not None:
                return not (value < self.max_value)
        else:
            if self.min_value is not None and self.max_value is not None:
                return self.min_value <= value <= self.max_value
            elif self.min_value is not None:
                return value >= self.min_value
            elif self.max_value is not None:
                return value <= self.max_value
        return True

    def __str__(self) -> str:
        prefix = "@" if self.inclusive else ""
        if self.min_value is not None and self.max_value is not None:
            return f"{prefix}{self.min_value}:{self.max_value}"
        elif self.min_value is not None:
            return f"{prefix}{self.min_value}:"
        elif self.max_value is not None:
            return f"{prefix}:{self.max_value}"
        return ""


def threshold_check(
    value: float, warning: str | None = None, critical: str | None = None
) -> Status:
    """Check value against warning/critical thresholds."""
    warn = ThresholdRange.from_string(warning) if warning else None
    crit = ThresholdRange.from_string(critical) if critical else None

    # Handle inverted ranges where critical fully covers warning
    if (
        crit
        and warn
        and crit.inclusive
        and warn.inclusive
        and crit.min_value is not None
        and crit.max_value is not None
        and warn.min_value is not None
        and warn.max_value is not None
        and crit.min_value <= warn.min_value
        and crit.max_value >= warn.max_value
    ):
        if warn.min_value < value < warn.max_value:
            return Status.CRITICAL
        return Status.OK

    if crit and not crit.check(value):
        return Status.CRITICAL
    if warn and not warn.check(value):
        return Status.WARNING
    return Status.OK


# Backward compatibility
def _parse_threshold(s: str) -> tuple[float | None, float | None, bool]:
    r = ThresholdRange.from_string(s)
    return (r.min_value, r.max_value, r.inclusive)


def _is_in_range(value: float, range_tuple: tuple[float | None, float | None, bool]) -> bool:
    return ThresholdRange(*range_tuple).check(value)
