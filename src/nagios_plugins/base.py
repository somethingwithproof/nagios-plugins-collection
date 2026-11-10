#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Base module for all Nagios plugins.

This module provides a base class for all Nagios plugins to ensure consistent
behavior and enterprise-grade features.
"""

import argparse
import json
import logging
import math
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from decimal import Decimal
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


# Units of measurement accepted by the Nagios Plugin Guidelines.
PERFDATA_UOMS = frozenset({"", "s", "ms", "us", "%", "B", "KB", "MB", "GB", "TB", "c"})


def format_number(value: float) -> str:
    """Format a finite number in plain positional notation, as perfdata requires."""
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    if value.is_integer():
        return str(int(value))
    return format(Decimal(repr(value)), "f")


def _is_number(value: Any) -> bool:
    """Return whether a metric value can be published as perfdata."""
    return isinstance(value, (int, float)) and math.isfinite(value)


def single_line(text: str) -> str:
    """Collapse line breaks and remove the perfdata separator from status text."""
    return " ".join(text.replace("|", "/").splitlines())


@dataclass(frozen=True)
class PerfData:
    """One performance-data value with its optional unit, thresholds and bounds.

    ``warning`` and ``critical`` are Nagios range strings, as passed to ``-w``/``-c``.
    """

    value: float
    uom: str = ""
    warning: str | None = None
    critical: str | None = None
    minimum: float | None = None
    maximum: float | None = None

    def __post_init__(self) -> None:
        """Reject units outside the Nagios Plugin Guidelines."""
        if self.uom not in PERFDATA_UOMS:
            raise ValueError(f"Invalid perfdata unit: {self.uom!r}")


def format_perfdata_label(label: str) -> str:
    """Quote a perfdata label when it contains spaces, ``=`` or quotes."""
    label = single_line(label)
    if any(char in label for char in " ='"):
        return "'" + label.replace("'", "''") + "'"
    return label


def format_perfdata(metrics: dict[str, Any]) -> str:
    """Render metrics as ``'label'=value[UOM];warn;crit;min;max`` items.

    Values that are not finite numbers (strings, ``None``, ``inf``/``nan``) are
    omitted: the guidelines only allow numbers, so they belong in the message.
    """
    items = []
    for label, metric in metrics.items():
        perf = metric if isinstance(metric, PerfData) else PerfData(metric)
        if not _is_number(perf.value):
            continue
        fields = [
            perf.warning or "",
            perf.critical or "",
            "" if perf.minimum is None else format_number(perf.minimum),
            "" if perf.maximum is None else format_number(perf.maximum),
        ]
        while fields and not fields[-1]:
            fields.pop()
        value = format_number(perf.value) + perf.uom
        items.append(f"{format_perfdata_label(label)}={';'.join([value, *fields])}")
    return " ".join(items)


def _json_metric(metric: Any) -> Any:
    """Keep JSON metrics as plain values and replace non-finite numbers with null."""
    if isinstance(metric, PerfData):
        metric = metric.value
    if isinstance(metric, float) and not math.isfinite(metric):
        return None
    return metric


@dataclass
class CheckResult:
    """Data class to store check results."""

    status: Status
    message: str
    metrics: dict[str, Any] = field(default_factory=dict)
    details: str | None = None
    timestamp: float = field(default_factory=time.time)

    def __str__(self) -> str:
        """Return the status line, perfdata and optional long output.

        The first line is always ``STATUS - message[ | perfdata]``; ``details``
        follow as long output with any ``|`` removed so they cannot start perfdata.
        """
        output = f"{self.status} - {single_line(self.message)}"
        perfdata = format_perfdata(self.metrics)
        if perfdata:
            output += f" | {perfdata}"
        if self.details:
            output += "\n" + self.details.replace("|", "/")
        return output

    def to_json(self) -> str:
        """Convert the check result to a JSON string.

        Returns:
            A JSON string representation of the check result.
        """
        result_dict = asdict(self)
        result_dict["status"] = self.status.name
        result_dict["metrics"] = {key: _json_metric(value) for key, value in self.metrics.items()}
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
    """A threshold range as defined by the Nagios Plugin Guidelines.

    ``[@]start:end`` alerts when the value is outside ``start..end`` (both
    endpoints inclusive), or inside it when prefixed with ``@``:

    - ``10`` is ``0:10``: alert when the value is below 0 or above 10.
    - ``10:`` alerts below 10; ``~:10`` alerts above 10.
    - ``10:20`` alerts outside 10..20; ``@10:20`` alerts when 10 <= value <= 20.

    An empty start (``:10``) is accepted for compatibility and, like ``~``, means
    no lower bound. ``None`` bounds are unbounded.
    """

    def __init__(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
        inclusive: bool = False,
    ) -> None:
        """Initialize a threshold range.

        Args:
            min_value: The lower bound, or None for negative infinity.
            max_value: The upper bound, or None for positive infinity.
            inclusive: Whether to alert inside the range (``@``) instead of outside.
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
        text = threshold.strip()
        if not text:
            return cls()

        inclusive = text.startswith("@")
        if inclusive:
            text = text[1:]

        start, separator, end = text.partition(":")
        if not separator:
            start, end = "0", text
        min_value = None if start in ("", "~") else cls._bound(start, "minimum", threshold)
        max_value = None if end == "" else cls._bound(end, "maximum", threshold)
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError(f"Invalid threshold range, start exceeds end: {threshold}")
        return cls(min_value, max_value, inclusive)

    @staticmethod
    def _bound(value: str, label: str, threshold: str) -> float:
        """Parse one finite bound and identify malformed input precisely."""
        try:
            bound = float(value)
        except ValueError as exc:
            raise ValueError(f"Invalid {label} threshold in {threshold!r}: {value}") from exc
        if not math.isfinite(bound):
            raise ValueError(f"Invalid {label} threshold in {threshold!r}: {value}")
        return bound

    def contains(self, value: float) -> bool:
        """Return whether ``start <= value <= end``."""
        above_min = self.min_value is None or value >= self.min_value
        below_max = self.max_value is None or value <= self.max_value
        return above_min and below_max

    def check(self, value: float) -> bool:
        """Return True when the value does not raise an alert for this range."""
        return not self.contains(value) if self.inclusive else self.contains(value)

    def __str__(self) -> str:
        """Return the range in Nagios syntax, suitable for perfdata thresholds."""
        prefix = "@" if self.inclusive else ""
        if self.min_value is None and self.max_value is None and not self.inclusive:
            return ""
        start = "~" if self.min_value is None else format_number(self.min_value)
        end = "" if self.max_value is None else format_number(self.max_value)
        if start == "0" and end:
            return f"{prefix}{end}"
        return f"{prefix}{start}:{end}"


def threshold_check(
    value: float,
    warning: str | None = None,
    critical: str | None = None,
) -> Status:
    """Check a value against Nagios warning and critical ranges.

    Critical is evaluated first, so a value that alerts for both ranges is
    CRITICAL. A NaN value cannot be compared and is UNKNOWN.

    Args:
        value: The value to check.
        warning: The warning range (see :class:`ThresholdRange`).
        critical: The critical range (see :class:`ThresholdRange`).

    Returns:
        The status based on the thresholds.

    Raises:
        ValueError: If a threshold is malformed.
    """
    warn_range = ThresholdRange.from_string(warning) if warning else None
    crit_range = ThresholdRange.from_string(critical) if critical else None
    if math.isnan(value):
        return Status.UNKNOWN
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
