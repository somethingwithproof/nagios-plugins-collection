#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Base module for all Nagios plugins.

This module provides a base class for all Nagios plugins to ensure consistent
behavior and enterprise-grade features.
"""

import argparse
import asyncio
import json
import logging
import math
import os
import sys
import time
from abc import ABC, abstractmethod
from collections.abc import Callable, Coroutine
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, NoReturn

from nagios_plugins.redaction import redact

_LOG_HANDLER_NAME = "nagios_plugins.stderr"


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
        output = f"{self.status} - {single_line(redact(self.message))}"
        perfdata = format_perfdata(self.metrics)
        if perfdata:
            output += f" | {perfdata}"
        if self.details:
            output += "\n" + redact(self.details).replace("|", "/")
        return output

    def to_json(self) -> str:
        """Convert the check result to a JSON string.

        Returns:
            A JSON string representation of the check result.
        """
        result_dict = asdict(self)
        result_dict["status"] = self.status.name
        result_dict["message"] = redact(self.message)
        result_dict["details"] = redact(self.details) if self.details else self.details
        result_dict["metrics"] = {key: _json_metric(value) for key, value in self.metrics.items()}
        result_dict["timestamp"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp)
        )
        return json.dumps(result_dict, indent=2)


def emit(result: CheckResult, as_json: bool = False) -> int:
    """Write the result to stdout and return its exit code."""
    sys.stdout.write((result.to_json() if as_json else str(result)) + "\n")
    return result.status.value


class _RedactingFormatter(logging.Formatter):
    """Mask credentials in log records, including exception tracebacks."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the record, then redact the complete text."""
        return redact(super().format(record))


def configure_logging(verbosity: int = 0) -> None:
    """Route log records to stderr so stdout carries only the plugin result.

    Called once per run after argument parsing, never at import time. Repeated
    calls replace the handler instead of stacking duplicates.

    Args:
        verbosity: 0 logs warnings, 1 adds info, 2 or more adds debug records.
    """
    root = logging.getLogger()
    for handler in root.handlers[:]:
        if handler.get_name() == _LOG_HANDLER_NAME:
            root.removeHandler(handler)
    handler = logging.StreamHandler(sys.stderr)
    handler.set_name(_LOG_HANDLER_NAME)
    handler.setFormatter(_RedactingFormatter("%(levelname)s %(name)s: %(message)s"))
    root.addHandler(handler)
    root.setLevel(
        logging.DEBUG if verbosity >= 2 else logging.INFO if verbosity == 1 else logging.WARNING
    )


class NagiosArgumentParser(argparse.ArgumentParser):
    """Argument parser whose usage errors exit UNKNOWN (3), not argparse's 2.

    Exit code 2 means CRITICAL to Nagios, so a typo in a command definition
    would otherwise page as an outage. ``--help`` still exits 0.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create the parser with no secret options registered."""
        super().__init__(*args, **kwargs)
        self._secrets: list[tuple[str, str, str, bool]] = []

    def error(self, message: str) -> NoReturn:
        """Print an UNKNOWN status line and usage, then exit 3."""
        sys.stdout.write(f"{Status.UNKNOWN} - {self.prog}: {single_line(redact(message))}\n")
        self.print_usage(sys.stderr)
        self.exit(Status.UNKNOWN.value)

    def add_secret_argument(
        self, flag: str, *, env: str, help: str, required: bool = False
    ) -> None:
        """Accept a secret from ``FLAG``, ``FLAG-file PATH`` or the ``env`` variable.

        Command-line values are visible to other local users in the process
        list, so the file and environment forms are preferred; the plain flag
        keeps existing command definitions working. Precedence is flag, then
        file, then environment. Surrounding line breaks are stripped from files.
        """
        dest = flag.lstrip("-").replace("-", "_")
        group = self.add_mutually_exclusive_group()
        group.add_argument(
            flag,
            dest=dest,
            help=f"{help} (visible in the process list; prefer {flag}-file or ${env})",
        )
        group.add_argument(
            f"{flag}-file", dest=f"{dest}_file", metavar="PATH", help=f"Read {help} from PATH"
        )
        self._secrets.append((dest, flag, env, required))

    # typeshed declares parse_known_args as overloads keyed on the namespace
    # type; one implementation covering every overload cannot restate them.
    def parse_known_args(  # type: ignore[override]
        self, args: Any = None, namespace: Any = None
    ) -> tuple[argparse.Namespace, list[str]]:
        """Parse arguments, then resolve secret options from files or the environment."""
        parsed, extras = super().parse_known_args(args, namespace)
        for dest, flag, env, required in self._secrets:
            path = getattr(parsed, f"{dest}_file", None)
            if not getattr(parsed, dest, None) and path:
                try:
                    setattr(parsed, dest, Path(path).read_text(encoding="utf-8").strip("\r\n"))
                except OSError as exc:
                    self.error(f"cannot read {flag}-file {path}: {exc.strerror}")
            if not getattr(parsed, dest, None):
                setattr(parsed, dest, os.environ.get(env) or None)
            if required and not getattr(parsed, dest):
                self.error(f"one of {flag}, {flag}-file or ${env} is required")
        return parsed, extras


def run_async_check(
    args: argparse.Namespace,
    check: Callable[[argparse.Namespace], Coroutine[Any, Any, CheckResult]],
) -> int:
    """Run a standalone plugin's async check and emit its result.

    Shared by the plugins that predate :class:`NagiosPlugin`: configures
    logging, turns any unhandled exception into UNKNOWN and honors ``--json``.
    """
    configure_logging(getattr(args, "verbose", 0))
    try:
        result = asyncio.run(check(args))
    except Exception as exc:  # pylint: disable=broad-except
        logging.getLogger(__name__).exception("Unhandled exception")
        result = CheckResult(Status.UNKNOWN, f"Unhandled exception: {exc}")
    return emit(result, getattr(args, "json", False))


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
        self.logger = logging.getLogger(self.__class__.__name__)
        self.start_time = time.time()

    def _create_argument_parser(self) -> NagiosArgumentParser:
        """Create the argument parser for the plugin.

        Returns:
            The argument parser.
        """
        parser = NagiosArgumentParser(
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
        configure_logging(parsed_args.verbose)
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

        Raises:
            SystemExit: For ``--help`` (0) and usage errors (3), as argparse does.
        """
        parsed_args = self.parse_args(args)
        try:
            result = self.check(parsed_args)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.exception("Unhandled exception")
            result = CheckResult(Status.UNKNOWN, f"Unhandled exception: {e}")
        self.logger.debug("Plugin execution time: %.3f seconds", time.time() - self.start_time)
        return emit(result, parsed_args.json)


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
