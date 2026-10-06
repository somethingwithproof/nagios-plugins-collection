#!/usr/bin/env python3
"""Base module for all Nagios plugins.

This module provides a base class for all Nagios plugins to ensure consistent
behavior and enterprise-grade features.
"""

import argparse
import json
import logging
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

# Install rich traceback handler for better exception formatting
install_rich_traceback(show_locals=False)


class Status(Enum):
    """Nagios status codes."""

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    @classmethod
    def from_string(cls, status_str: str) -> "Status":
        """Convert a string status to a Status enum.

        Args:
            status_str: The status string to convert.

        Returns:
            The corresponding Status enum.
        """
        status_map = {
            "OK": cls.OK,
            "WARNING": cls.WARNING,
            "CRITICAL": cls.CRITICAL,
            "UNKNOWN": cls.UNKNOWN,
        }
        return status_map.get(status_str.upper(), cls.UNKNOWN)

    def __str__(self) -> str:
        """Return the string representation of the status."""
        return self.name


@dataclass
class CheckResult:
    """Data class to store check results."""

    status: Status
    message: str
    metrics: dict[str, Any] = field(default_factory=dict)
    details: str | None = None
    timestamp: float = field(default_factory=time.time)

    def __str__(self) -> str:
        """Return the string representation of the check result."""
        output = f"{self.status} - {self.message}"
        if self.metrics:
            metrics_str = " ".join(f"{key}={value}" for key, value in self.metrics.items())
            output += f" | {metrics_str}"
        if self.details:
            output += f"\n{self.details}"
        return output

    def to_json(self) -> str:
        """Convert the check result to a JSON string.

        Returns:
            A JSON string representation of the check result.
        """
        result_dict = asdict(self)
        result_dict["status"] = self.status.name
        result_dict["timestamp"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp)
        )
        return json.dumps(result_dict, indent=2)


class NagiosPlugin(ABC):
    """Base class for all Nagios plugins.

    This class provides common functionality for all Nagios plugins, including:
    - Argument parsing
    - Logging
    - Status handling
    - Performance data
    - Output formatting
    """

    def __init__(self) -> None:
        """Initialize the plugin."""
        self.parser = self._create_argument_parser()
        self.console = Console(stderr=True)
        self._setup_logging()
        self.start_time = time.time()

    def _setup_logging(self) -> None:
        """Set up logging for the plugin."""
        self.logger = logging.getLogger(self.__class__.__name__)

        # Remove any existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Add rich handler for better formatting
        handler = RichHandler(console=self.console, rich_tracebacks=True)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.WARNING)

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser for the plugin.

        Returns:
            The argument parser.
        """
        parser = argparse.ArgumentParser(
            description=self.__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Increase verbosity (can be used multiple times)",
        )
        parser.add_argument(
            "-t",
            "--timeout",
            type=int,
            default=30,
            help="Timeout in seconds (default: 30)",
        )
        parser.add_argument(
            "-w",
            "--warning",
            help="Warning threshold (plugin-specific)",
        )
        parser.add_argument(
            "-c",
            "--critical",
            help="Critical threshold (plugin-specific)",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Output results in JSON format",
        )
        return parser

    def parse_args(self, args: list[str] | None = None) -> argparse.Namespace:
        """Parse command-line arguments.

        Args:
            args: Command-line arguments to parse. If None, sys.argv[1:] is used.

        Returns:
            The parsed arguments.
        """
        parsed_args = self.parser.parse_args(args)

        # Set logging level based on verbosity
        if parsed_args.verbose == 1:
            self.logger.setLevel(logging.INFO)
        elif parsed_args.verbose >= 2:
            self.logger.setLevel(logging.DEBUG)

        return parsed_args

    @abstractmethod
    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the check.

        Args:
            args: The parsed command-line arguments.

        Returns:
            The check result.
        """

    def run(self, args: list[str] | None = None) -> int:
        """Run the plugin.

        Args:
            args: Command-line arguments to parse. If None, sys.argv[1:] is used.

        Returns:
            The exit code.
        """
        try:
            parsed_args = self.parse_args(args)
            result = self.check(parsed_args)

            if parsed_args.json:
                sys.stdout.write(result.to_json() + "\n")
            else:
                sys.stdout.write(str(result) + "\n")

            return result.status.value
        except Exception as e:  # pylint: disable=broad-except
            self.logger.exception("Unhandled exception")
            error_result = CheckResult(
                Status.UNKNOWN,
                f"Unhandled exception: {str(e)}",
            )
            if "parsed_args" in locals() and getattr(parsed_args, "json", False):
                sys.stdout.write(error_result.to_json() + "\n")
            else:
                sys.stdout.write(str(error_result) + "\n")
            return Status.UNKNOWN.value
        finally:
            elapsed_time = time.time() - self.start_time
            self.logger.debug("Plugin execution time: %.3f seconds", elapsed_time)


class ThresholdRange:
    """Class to represent a threshold range for Nagios checks."""

    def __init__(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
        inclusive: bool = False,
    ) -> None:
        """Initialize a threshold range.

        Args:
            min_value: The minimum value of the range.
            max_value: The maximum value of the range.
            inclusive: Whether the range is inclusive (inside is bad).
        """
        self.min_value = min_value
        self.max_value = max_value
        self.inclusive = inclusive

    @classmethod
    def from_string(cls, threshold: str) -> "ThresholdRange":
        """Parse a threshold string into a ThresholdRange.

        Args:
            threshold: The threshold string to parse.

        Returns:
            A ThresholdRange object.

        Raises:
            ValueError: If the threshold string is invalid.
        """
        if not threshold:
            return cls()

        inclusive = threshold.startswith("@")
        if inclusive:
            threshold = threshold[1:]

        if ":" not in threshold:
            # Simple threshold
            try:
                value = float(threshold)
                return cls(None, value, inclusive)
            except ValueError as exc:
                raise ValueError(f"Invalid threshold value: {threshold}") from exc
        parts = threshold.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid threshold format: {threshold}")
        return cls(cls._bound(parts[0], "minimum"), cls._bound(parts[1], "maximum"), inclusive)

    @staticmethod
    def _bound(value: str, label: str) -> float | None:
        """Parse one optional bound and identify malformed input precisely."""
        if not value:
            return None
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(f"Invalid {label} threshold: {value}") from exc

    def check(self, value: float) -> bool:
        """Check if a value is within the threshold range.

        Args:
            value: The value to check.

        Returns:
            True if the value is OK (within range for normal, outside for inclusive),
            False otherwise.
        """
        if self.inclusive:
            # Inside the range is bad (inverted logic)
            if self.min_value is not None and self.max_value is not None:
                return not (self.min_value < value < self.max_value)
            elif self.min_value is not None:
                return value <= self.min_value
            elif self.max_value is not None:
                return value >= self.max_value
            return True
        else:
            # Outside the range is bad
            if self.min_value is not None and self.max_value is not None:
                return self.min_value <= value <= self.max_value
            elif self.min_value is not None:
                return value >= self.min_value
            elif self.max_value is not None:
                return value <= self.max_value
            return True

    def __str__(self) -> str:
        """Return the string representation of the threshold range."""
        prefix = "@" if self.inclusive else ""

        if self.min_value is not None and self.max_value is not None:
            return f"{prefix}{self.min_value}:{self.max_value}"
        elif self.min_value is not None:
            return f"{prefix}{self.min_value}:"
        elif self.max_value is not None:
            return f"{prefix}:{self.max_value}"
        return ""


def threshold_check(
    value: float,
    warning: str | None = None,
    critical: str | None = None,
) -> Status:
    """Check a value against warning and critical thresholds.

    Args:
        value: The value to check.
        warning: The warning threshold. Can be a simple number or a range.
        critical: The critical threshold. Can be a simple number or a range.

    Returns:
        The status based on the thresholds.
    """
    # Parse thresholds
    warn_range = ThresholdRange.from_string(warning) if warning else None
    crit_range = ThresholdRange.from_string(critical) if critical else None

    # Special handling when both ranges are inverted and the critical range
    # fully covers the warning range.  In this situation only values that fall
    # inside the (smaller) warning range should escalate to CRITICAL.  Values
    # that are only in the wider critical range are considered OK.
    if (
        crit_range
        and warn_range
        and crit_range.inclusive
        and warn_range.inclusive
        and crit_range.min_value is not None
        and crit_range.max_value is not None
        and warn_range.min_value is not None
        and warn_range.max_value is not None
        and crit_range.min_value <= warn_range.min_value
        and crit_range.max_value >= warn_range.max_value
    ):
        if warn_range.min_value < value < warn_range.max_value:
            return Status.CRITICAL
        return Status.OK

    # Check critical first, then warning
    if crit_range and not crit_range.check(value):
        return Status.CRITICAL
    if warn_range and not warn_range.check(value):
        return Status.WARNING
    return Status.OK


# For backward compatibility
def _parse_threshold(threshold: str) -> tuple[float | None, float | None, bool]:
    """Parse a threshold string into a range.

    Args:
        threshold: The threshold string to parse.

    Returns:
        A tuple of (min, max, inclusive).
    """
    range_obj = ThresholdRange.from_string(threshold)
    return (range_obj.min_value, range_obj.max_value, range_obj.inclusive)


# For backward compatibility
def _is_in_range(value: float, range_tuple: tuple[float | None, float | None, bool]) -> bool:
    """Check if a value is in a range.

    Args:
        value: The value to check.
        range_tuple: A tuple of (min, max, inclusive).

    Returns:
        True if the value is in the range, False otherwise.
    """
    min_val, max_val, inclusive = range_tuple
    range_obj = ThresholdRange(min_val, max_val, inclusive)
    return range_obj.check(value)
