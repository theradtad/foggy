"""Main entry point for the Foggy CLI application."""

import sys
from typing import Optional

import click
from click import Context

from foggy.cli.commands import cli_group


def main() -> Optional[int]:
    """Main entry point for the Foggy application.

    This function serves as the primary CLI entry point and delegates
    to the Click command group for handling all CLI interactions.

    Returns:
        Optional exit code from the CLI application. Returns 0 on success
        or None if execution completed normally.

    Raises:
        SystemExit: When Click encounters an error and exits the application.
    """
    try:
        cli_group()
        return 0
    except Exception as e:
        click.echo(f"Fatal error: {e}", err=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
