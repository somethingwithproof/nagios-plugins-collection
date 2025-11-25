"""
Base classes and utilities for Nagios plugins.

This module provides common functionality used by all plugins in the collection.
"""

import argparse
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Dict, List, Optional, Tuple


class Status(IntEnum):
    """Nagios plugin exit status codes."""
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


@dataclass
class CheckResult:
    """Result of a Nagios plugin check."""
    status: Status
    message: str
    perfdata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Format the result as Nagios output."""
        status_name = self.status.name
        output = f"{status_name} - {self.message}"

        if self.perfdata:
            perf_parts = []
            for key, value in self.perfdata.items():
                if isinstance(value, dict):
                    # Full perfdata format: value;warn;crit;min;max
                    val = value.get("value", 0)
                    warn = value.get("warn", "")
                    crit = value.get("crit", "")
                    min_val = value.get("min", "")
                    max_val = value.get("max", "")
                    unit = value.get("unit", "")
                    perf_parts.append(f"{key}={val}{unit};{warn};{crit};{min_val};{max_val}")
                else:
                    perf_parts.append(f"{key}={value}")
            output += " | " + " ".join(perf_parts)

        return output

    def exit(self) -> None:
        """Print result and exit with appropriate code."""
        print(str(self))
        sys.exit(self.status)


@dataclass
class ThresholdRange:
    """
    Nagios threshold range parser.

    Supports the standard Nagios range format:
    - 10       -> 0 <= x <= 10
    - 10:      -> 10 <= x
    - ~:10     -> x <= 10
    - 10:20    -> 10 <= x <= 20
    - @10:20   -> NOT (10 <= x <= 20), alert if inside range
    """
    start: Optional[float] = None
    end: Optional[float] = None
    inside: bool = False  # If True, alert when INSIDE range

    @classmethod
    def parse(cls, range_str: Optional[str]) -> Optional["ThresholdRange"]:
        """Parse a Nagios range string into a ThresholdRange object."""
        if not range_str:
            return None

        inside = False
        if range_str.startswith("@"):
            inside = True
            range_str = range_str[1:]

        if ":" in range_str:
            parts = range_str.split(":", 1)
            start = None if parts[0] == "~" else float(parts[0]) if parts[0] else 0
            end = None if not parts[1] else float(parts[1])
        else:
            start = 0
            end = float(range_str)

        return cls(start=start, end=end, inside=inside)

    def check(self, value: float) -> bool:
        """
        Check if value triggers an alert.

        Returns True if the value is outside the acceptable range (triggers alert).
        """
        in_range = True

        if self.start is not None and value < self.start:
            in_range = False
        if self.end is not None and value > self.end:
            in_range = False

        # If inside=True (@prefix), alert when IN range; otherwise alert when OUT of range
        return in_range if self.inside else not in_range


class NagiosPlugin(ABC):
    """Abstract base class for Nagios plugins."""

    name: str = "check_plugin"
    version: str = "1.0.0"
    description: str = "Nagios plugin"

    def __init__(self) -> None:
        self.parser = self._create_parser()
        self._add_common_arguments()
        self._add_arguments()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        return argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

    def _add_common_arguments(self) -> None:
        """Add common arguments shared by all plugins."""
        self.parser.add_argument(
            "-V", "--version",
            action="version",
            version=f"%(prog)s {self.version}",
        )
        self.parser.add_argument(
            "-v", "--verbose",
            action="count",
            default=0,
            help="Increase verbosity (can be specified multiple times)",
        )
        self.parser.add_argument(
            "-t", "--timeout",
            type=int,
            default=30,
            help="Plugin timeout in seconds (default: 30)",
        )

    @abstractmethod
    def _add_arguments(self) -> None:
        """Add plugin-specific arguments. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def check(self, args: argparse.Namespace) -> CheckResult:
        """
        Perform the check. Must be implemented by subclasses.

        Args:
            args: Parsed command-line arguments

        Returns:
            CheckResult with status, message, and optional perfdata
        """
        pass

    def run(self, argv: Optional[List[str]] = None) -> None:
        """Parse arguments and run the check."""
        try:
            args = self.parser.parse_args(argv)
            result = self.check(args)
            result.exit()
        except KeyboardInterrupt:
            print("UNKNOWN - Plugin interrupted by user")
            sys.exit(Status.UNKNOWN)
        except Exception as e:
            print(f"UNKNOWN - Plugin error: {e}")
            sys.exit(Status.UNKNOWN)


def get_env_or_arg(env_var: str, arg_value: Optional[str], default: Optional[str] = None) -> Optional[str]:
    """
    Get a value from environment variable or argument.

    Priority: argument > environment variable > default
    """
    if arg_value:
        return arg_value
    return os.environ.get(env_var, default)
