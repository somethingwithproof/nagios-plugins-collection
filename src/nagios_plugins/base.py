#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Base module for all Nagios plugins.

This module provides a base class for all Nagios plugins to ensure consistent
behavior and enterprise-grade features.
"""

import argparse
import asyncio
import inspect
import json
import logging
import math
import os
import sys
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, NoReturn

from nagios_plugins.deadline import Deadline, PluginTimeout, hard_remaining
from nagios_plugins.redaction import redact

_LOG_HANDLER_NAME = "nagios_plugins.stderr"
# Root log level by -v count: none, -v, -vv (or more).
_LOG_LEVELS = (logging.WARNING, logging.INFO, logging.DEBUG)


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
    root.setLevel(_LOG_LEVELS[min(max(verbosity, 0), 2)])


def positive_seconds(text: str) -> int:
    """Parse a whole number of seconds greater than zero for ``--timeout``."""
    try:
        seconds = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid seconds: {text!r}") from None
    if seconds < 1:
        raise argparse.ArgumentTypeError(f"must be at least 1 second: {text!r}")
    return seconds


@dataclass(frozen=True)
class SecretOption:
    """A credential option and the places its value may come from.

    Sources in precedence order: ``FLAG VALUE``, ``FLAG-file PATH``, the ``env``
    variable, then a path in the ``<env>_FILE`` variable (the convention
    container platforms use for mounted secrets).
    """

    dest: str
    flag: str
    env: str
    required: bool = False

    @property
    def file_flag(self) -> str:
        """The option that names a file holding the secret."""
        return f"{self.flag}-file"

    @property
    def file_env(self) -> str:
        """The environment variable that names a file holding the secret."""
        return f"{self.env}_FILE"

    def resolve(self, parsed: argparse.Namespace) -> str | None:
        """Return the secret from the first source that supplies one.

        Raises:
            OSError: If a named file cannot be read; ``filename`` identifies it.
        """
        value = getattr(parsed, self.dest, None)
        path = getattr(parsed, f"{self.dest}_file", None)
        if not value and path:
            value = _read_secret(path)
        value = value or os.environ.get(self.env)
        if not value and os.environ.get(self.file_env):
            value = _read_secret(os.environ[self.file_env])
        return value or None


def _read_secret(path: str) -> str:
    """Read a secret file, dropping the line break editors and ``echo`` append."""
    return Path(path).read_text(encoding="utf-8").strip("\r\n")


class NagiosArgumentParser(argparse.ArgumentParser):
    """Argument parser whose usage errors exit UNKNOWN (3), not argparse's 2.

    Exit code 2 means CRITICAL to Nagios, so a typo in a command definition
    would otherwise page as an outage. ``--help`` still exits 0.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create the parser with no secret options or validators registered."""
        super().__init__(*args, **kwargs)
        self._secrets: list[SecretOption] = []
        self._validators: list[Callable[[argparse.Namespace], str | None]] = []

    @property
    def secret_options(self) -> tuple[SecretOption, ...]:
        """The registered secret options, in the order they were added."""
        return tuple(self._secrets)

    def error(self, message: str) -> NoReturn:
        """Print an UNKNOWN status line and usage, then exit 3."""
        sys.stdout.write(f"{Status.UNKNOWN} - {self.prog}: {single_line(redact(message))}\n")
        self.print_usage(sys.stderr)
        self.exit(Status.UNKNOWN.value)

    def add_secret_argument(
        self,
        flag: str,
        *,
        env: str,
        help: str,
        required: bool = False,
        container: argparse._ActionsContainer | None = None,
    ) -> None:
        """Accept a secret from ``FLAG``, ``FLAG-file PATH``, ``$ENV`` or ``$ENV_FILE``.

        Command-line values are visible to other local users in the process
        list, so the file and environment forms are preferred; the plain flag
        keeps existing command definitions working. See :class:`SecretOption`
        for the precedence.

        Args:
            flag: The option, for example ``--password``.
            env: The environment variable that may hold the secret.
            help: What the secret is, used in both options' help.
            required: Whether a missing secret is a usage error.
            container: An argument group to list the options under in ``--help``.
        """
        secret = SecretOption(flag.lstrip("-").replace("-", "_"), flag, env, required)
        group = (container or self).add_mutually_exclusive_group()
        group.add_argument(
            flag,
            dest=secret.dest,
            help=f"{help} (visible in the process list; prefer {flag}-file or ${env})",
        )
        group.add_argument(
            secret.file_flag,
            dest=f"{secret.dest}_file",
            metavar="PATH",
            help=f"Read {help} from PATH (or the file named by ${secret.file_env})",
        )
        self._secrets.append(secret)

    def add_validator(self, validator: Callable[[argparse.Namespace], str | None]) -> None:
        """Check parsed options together; a returned message is a usage error."""
        self._validators.append(validator)

    # typeshed declares parse_known_args as overloads keyed on the namespace
    # type; one implementation covering every overload cannot restate them.
    def parse_known_args(  # type: ignore[override]
        self, args: Any = None, namespace: Any = None
    ) -> tuple[argparse.Namespace, list[str]]:
        """Parse arguments, resolve secrets, then run the cross-option validators."""
        parsed, extras = super().parse_known_args(args, namespace)
        for secret in self._secrets:
            try:
                setattr(parsed, secret.dest, secret.resolve(parsed))
            except OSError as exc:
                self.error(f"cannot read the {secret.flag} file {exc.filename}: {exc.strerror}")
            if secret.required and not getattr(parsed, secret.dest):
                self.error(
                    f"one of {secret.flag}, {secret.file_flag}, ${secret.env} or "
                    f"${secret.file_env} is required"
                )
        for validator in self._validators:
            if problem := validator(parsed):
                self.error(problem)
        return parsed, extras


class NagiosPlugin(ABC):
    """Base class for all Nagios plugins.

    Subclasses register their own options on ``self.parser`` and implement
    :meth:`check`. The base class supplies ``-v``, ``-t``, ``--json`` and, unless
    :attr:`has_thresholds` is false, ``-w``/``-c`` Nagios ranges; it configures
    stderr logging after parsing, turns unhandled exceptions into UNKNOWN and
    writes the single result to stdout.
    """

    #: Default for ``-t/--timeout`` in seconds.
    default_timeout: ClassVar[int] = 30
    #: Whether ``-w``/``-c`` take Nagios ranges; plugins without thresholds set False.
    has_thresholds: ClassVar[bool] = True

    def __init__(self) -> None:
        """Initialize the plugin."""
        self.parser = self._create_argument_parser()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.start_time = time.time()

    @classmethod
    def command_name(cls) -> str | None:
        """Return the installed command name, which is the plugin's module name.

        ``None`` (argparse falls back to ``argv[0]``) when the module runs as a script.
        """
        module = cls.__module__.rpartition(".")[2]
        return None if module == "__main__" else module

    def _create_argument_parser(self) -> NagiosArgumentParser:
        """Create the argument parser with the options every plugin shares.

        Returns:
            The argument parser.
        """
        parser = NagiosArgumentParser(
            prog=self.command_name(),
            description=inspect.getdoc(type(self)),
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
            type=positive_seconds,
            default=self.default_timeout,
            help=(
                f"Timeout in seconds for the whole run (default: {self.default_timeout}); "
                "the plugin exits UNKNOWN 1 second after it"
            ),
        )
        if self.has_thresholds:
            self.add_threshold_arguments(parser)
        parser.add_argument(
            "--json",
            action="store_true",
            help="Output results in JSON format",
        )
        return parser

    def add_threshold_arguments(self, parser: NagiosArgumentParser) -> None:
        """Register ``-w``/``-c`` as Nagios ranges.

        Override to give the thresholds another meaning, as a plugin whose
        established options take plain numbers does.
        """
        parser.add_argument(
            "-w", "--warning", type=nagios_range, help="Warning threshold (plugin-specific)"
        )
        parser.add_argument(
            "-c", "--critical", type=nagios_range, help="Critical threshold (plugin-specific)"
        )

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
        timed_out = CheckResult(
            Status.UNKNOWN, f"Plugin timed out after {parsed_args.timeout} seconds"
        )
        rendered = timed_out.to_json() if parsed_args.json else str(timed_out)
        try:
            with Deadline(parsed_args.timeout, rendered):
                result = self._checked(parsed_args)
        except PluginTimeout:
            self.logger.warning("Run deadline expired")
            result = timed_out
        self.logger.debug("Plugin execution time: %.3f seconds", time.time() - self.start_time)
        return emit(result, parsed_args.json)

    def _checked(self, args: argparse.Namespace) -> CheckResult:
        """Run :meth:`check`, reporting any unhandled exception as UNKNOWN."""
        try:
            return self.check(args)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.exception("Unhandled exception")
            return CheckResult(Status.UNKNOWN, f"Unhandled exception: {e}")


class AsyncNagiosPlugin(NagiosPlugin):
    """Base class for plugins whose check is a coroutine.

    The base class owns the event loop, so subclasses implement only
    :meth:`check_async`.
    """

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Run :meth:`check_async` to completion in a new event loop."""
        return asyncio.run(self._bounded(args))

    async def _bounded(self, args: argparse.Namespace) -> CheckResult:
        """Cancel the check when the run deadline expires.

        Cancellation, unlike an exception from a signal handler, reaches the
        awaiting coroutine even inside ``asyncio.gather(return_exceptions=True)``.
        """
        remaining = hard_remaining()
        if remaining is None:
            return await self.check_async(args)
        bound = asyncio.timeout(remaining)
        try:
            async with bound:
                return await self.check_async(args)
        except TimeoutError:
            if bound.expired():
                raise PluginTimeout from None
            raise

    @abstractmethod
    async def check_async(self, args: argparse.Namespace) -> CheckResult:
        """Perform the check.

        Args:
            args: The parsed command-line arguments.

        Returns:
            The check result.
        """


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


#: Nagios plugin guidelines: CRITICAL > WARNING > UNKNOWN > OK when combining results.
_SEVERITY = {Status.OK: 0, Status.UNKNOWN: 1, Status.WARNING: 2, Status.CRITICAL: 3}


def most_severe(*statuses: Status) -> Status:
    """Return the status that should be reported for several measurements (OK if none)."""
    return max(statuses, key=_SEVERITY.__getitem__, default=Status.OK)


def nagios_range(value: str) -> str:
    """Accept a well-formed Nagios range for an option and return it unchanged.

    A malformed threshold is a configuration error, so it is rejected while
    parsing (exit 3) instead of surfacing after the check has run.

    Raises:
        argparse.ArgumentTypeError: If ``value`` is not a valid range.
    """
    try:
        ThresholdRange.from_string(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"invalid Nagios range {value!r}: {error}") from None
    return value


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
