#!/usr/bin/env python3
"""
Plugin Framework for Nagios.

This module provides a base framework for creating standardized Nagios plugins.
It includes common utilities, logging setup, and a consistent interface.
"""

import argparse
import asyncio
import json
import logging
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from rich.console import Console
from rich.logging import RichHandler

from nagios_plugins.base import Status, CheckResult


def setup_logging(name: str, verbose: int = 0) -> logging.Logger:
    """Set up logging with appropriate verbosity.

    Args:
        name: Logger name
        verbose: Verbosity level (0=WARNING, 1=INFO, 2+=DEBUG)

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Set base logging config
    logging.basicConfig(
        level=logging.WARNING,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
        force=True,
    )
    
    # Set level based on verbosity
    if verbose == 1:
        logger.setLevel(logging.INFO)
    elif verbose >= 2:
        logger.setLevel(logging.DEBUG)
    
    return logger


class NagiosPluginFramework(ABC):
    """Base framework for Nagios plugins."""

    def __init__(self, name: str, description: str):
        """Initialize the plugin framework.

        Args:
            name: Plugin name
            description: Plugin description
        """
        self.name = name
        self.description = description
        self.logger = logging.getLogger(name)
        self.console = Console()
        
        # Initialize parser with common arguments
        self.parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        self._add_common_arguments()
        self._add_plugin_arguments()
        
        # For storing parsed arguments
        self.args = None
    
    def _add_common_arguments(self) -> None:
        """Add common arguments to the argument parser."""
        self.parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            help="Timeout in seconds",
        )
        self.parser.add_argument(
            "--json",
            action="store_true",
            help="Output in JSON format",
        )
        self.parser.add_argument(
            "--verbose", "-v",
            action="count",
            default=0,
            help="Increase verbosity (can be used multiple times)",
        )
    
    @abstractmethod
    def _add_plugin_arguments(self) -> None:
        """Add plugin-specific arguments to the argument parser.
        
        This method must be implemented by each plugin.
        """
        pass
    
    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """Parse command-line arguments.

        Args:
            args: Command-line arguments to parse (uses sys.argv if None)

        Returns:
            Parsed arguments
        """
        self.args = self.parser.parse_args(args)
        return self.args
    
    @abstractmethod
    async def check(self) -> CheckResult:
        """Perform the plugin check.
        
        This method must be implemented by each plugin.

        Returns:
            CheckResult with the check result
        """
        pass
    
    def output_result(self, result: CheckResult) -> None:
        """Output the check result.

        Args:
            result: Check result to output
        """
        if self.args and self.args.json:
            print(result.to_json())
        else:
            print(result)
    
    def run(self) -> int:
        """Run the plugin.

        Returns:
            Exit code
        """
        # Parse arguments if not already parsed
        if not self.args:
            self.parse_args()
        
        # Configure logging
        setup_logging(self.name, self.args.verbose)
        
        # Run the check
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.check())
            self.output_result(result)
            return result.status.value
        except Exception as e:
            self.logger.exception("Unhandled error in plugin execution")
            result = CheckResult(
                Status.UNKNOWN,
                f"UNKNOWN - Unhandled error in plugin execution: {str(e)}",
                metrics={"error": 1},
                details=str(e),
            )
            self.output_result(result)
            return Status.UNKNOWN.value


# Example Plugin Implementation
class ExamplePlugin(NagiosPluginFramework):
    """Example Nagios plugin implementation."""
    
    def _add_plugin_arguments(self) -> None:
        """Add plugin-specific arguments."""
        self.parser.add_argument(
            "--host",
            required=True,
            help="Host to check",
        )
        self.parser.add_argument(
            "--warning",
            type=float,
            default=1.0,
            help="Warning threshold",
        )
        self.parser.add_argument(
            "--critical",
            type=float,
            default=5.0,
            help="Critical threshold",
        )
    
    async def check(self) -> CheckResult:
        """Perform the example check."""
        try:
            # Simulated check
            self.logger.info(f"Checking host: {self.args.host}")
            
            # In a real plugin, this would perform an actual check
            value = 0.5  # Example value
            
            # Evaluate thresholds
            if value > self.args.critical:
                return CheckResult(
                    Status.CRITICAL,
                    f"CRITICAL - Value {value} exceeds critical threshold {self.args.critical}",
                    metrics={"value": value},
                )
            elif value > self.args.warning:
                return CheckResult(
                    Status.WARNING,
                    f"WARNING - Value {value} exceeds warning threshold {self.args.warning}",
                    metrics={"value": value},
                )
            else:
                return CheckResult(
                    Status.OK,
                    f"OK - Value {value} is below thresholds",
                    metrics={"value": value},
                )
        
        except Exception as e:
            self.logger.exception("Error in check")
            return CheckResult(
                Status.UNKNOWN,
                f"UNKNOWN - Error: {str(e)}",
                metrics={"error": 1},
                details=str(e),
            )


def main() -> int:
    """Example main function."""
    plugin = ExamplePlugin(
        name="example_plugin",
        description="Example Nagios plugin",
    )
    return plugin.run()


if __name__ == "__main__":
    sys.exit(main())