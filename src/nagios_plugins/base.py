#!/usr/bin/env python3
"""Base module for all Nagios plugins.

This module provides a base class for all Nagios plugins to ensure consistent
behavior and enterprise-grade features.
"""

import argparse
import logging
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


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
    metrics: Optional[Dict[str, Any]] = None
    details: Optional[str] = None

    def __str__(self) -> str:
        """Return the string representation of the check result."""
        output = f"{self.status} - {self.message}"
        if self.metrics:
            metrics_str = " ".join(
                f"{key}={value}" for key, value in self.metrics.items()
            )
            output += f" | {metrics_str}"
        if self.details:
            output += f"\n{self.details}"
        return output


class NagiosPlugin(ABC):
    """Base class for all Nagios plugins.

    This class provides common functionality for all Nagios plugins, including:
    - Argument parsing
    - Logging
    - Status handling
    - Performance data
    """

    def __init__(self) -> None:
        """Initialize the plugin."""
        self.parser = self._create_argument_parser()
        self._setup_logging()
        self.start_time = time.time()

    def _setup_logging(self) -> None:
        """Set up logging for the plugin."""
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
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
        return parser

    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """Parse command-line arguments.

        Args:
            args: Command-line arguments to parse. If None, sys.argv[1:] is used.

        Returns:
            The parsed arguments.
        """
        args = self.parser.parse_args(args)
        
        # Set logging level based on verbosity
        if args.verbose == 1:
            self.logger.setLevel(logging.INFO)
        elif args.verbose >= 2:
            self.logger.setLevel(logging.DEBUG)
            
        return args

    @abstractmethod
    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the check.

        Args:
            args: The parsed command-line arguments.

        Returns:
            The check result.
        """

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the plugin.

        Args:
            args: Command-line arguments to parse. If None, sys.argv[1:] is used.

        Returns:
            The exit code.
        """
        try:
            parsed_args = self.parse_args(args)
            result = self.check(parsed_args)
            print(result)
            return result.status.value
        except (ValueError, TypeError, KeyError, IOError) as e:
            self.logger.exception("Error during plugin execution")
            print(f"{Status.UNKNOWN} - Error: {str(e)}")
            return Status.UNKNOWN.value
        except Exception as e:  # pylint: disable=broad-except
            self.logger.exception("Unhandled exception")
            print(f"{Status.UNKNOWN} - Unhandled exception: {str(e)}")
            return Status.UNKNOWN.value
        finally:
            elapsed_time = time.time() - self.start_time
            self.logger.debug("Plugin execution time: %.3f seconds", elapsed_time)


def threshold_check(
    value: float,
    warning: Optional[str] = None,
    critical: Optional[str] = None,
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
    warn_range = _parse_threshold(warning) if warning else None
    crit_range = _parse_threshold(critical) if critical else None

    # Check critical first, then warning
    if crit_range and not _is_in_range(value, crit_range):
        return Status.CRITICAL
    if warn_range and not _is_in_range(value, warn_range):
        return Status.WARNING
    return Status.OK


def _parse_threshold(threshold: str) -> Tuple[Optional[float], Optional[float], bool]:
    """Parse a threshold string into a range.

    Args:
        threshold: The threshold string to parse.

    Returns:
        A tuple of (min, max, inclusive).
    """
    if threshold.startswith("@"):
        inclusive = True
        threshold = threshold[1:]
    else:
        inclusive = False

    if ":" not in threshold:
        # Simple threshold
        value = float(threshold)
        return (None, value, inclusive)
    else:
        # Range
        parts = threshold.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid threshold format: {threshold}")
        
        min_val = float(parts[0]) if parts[0] else None
        max_val = float(parts[1]) if parts[1] else None
        return (min_val, max_val, inclusive)


def _is_in_range(
    value: float, range_tuple: Tuple[Optional[float], Optional[float], bool]
) -> bool:
    """Check if a value is in a range.

    Args:
        value: The value to check.
        range_tuple: A tuple of (min, max, inclusive).

    Returns:
        True if the value is in the range, False otherwise.
    """
    min_val, max_val, inclusive = range_tuple

    if inclusive:
        # Inside the range is bad (inverted logic)
        if min_val is not None and max_val is not None:
            return not (min_val <= value <= max_val)
        elif min_val is not None:
            return not (value >= min_val)
        elif max_val is not None:
            return not (value <= max_val)
        return True
    else:
        # Outside the range is bad
        if min_val is not None and max_val is not None:
            return min_val <= value <= max_val
        elif min_val is not None:
            return value >= min_val
        elif max_val is not None:
            return value <= max_val
        return True
