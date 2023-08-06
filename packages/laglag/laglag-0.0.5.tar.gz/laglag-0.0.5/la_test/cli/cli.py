"""kedro is a CLI for managing Kedro projects.
This module implements commands available from the kedro CLI.
"""
import sys
from typing import Sequence

import click
import pkg_resources

from la_test.cli.run_command import predict_run, test_run, train_run
from la_test.cli.starters import create_cli
from la_test.cli.utils import CONTEXT_SETTINGS, CommandCollection

version = "0.0.1"


@click.group(context_settings=CONTEXT_SETTINGS, name="LA")
@click.version_option(version, "--version", "-V", help="Show version and exit")
def cli():  # pragma: no cover
    """LA is a CLI for creating and using LA projects."""
    pass


class LACLI(CommandCollection):
    """A CommandCollection class to encapsulate the KedroCLI command
    loading.
    """

    def __init__(self, commands: Sequence[click.CommandCollection]):
        self._metadata = None  # running in package mode

        super().__init__(
            ("Global commands", commands),
        )

    def main(
        self,
        args=None,
        prog_name=None,
        complete_var=None,
        standalone_mode=True,
        **extra,
    ):
        if self._metadata:
            extra.update(obj=self._metadata)

        args = sys.argv[1:]

        super().main(
            args=args,
            prog_name=prog_name,
            complete_var=complete_var,
            standalone_mode=standalone_mode,
            **extra,
        )


def main():  # pragma: no cover
    """Main entry point. Look for a ``cli.py``, and, if found, add its
    commands to `kedro`'s before invoking the CLI.
    """
    cli.add_command(train_run())
    cli.add_command(test_run())
    cli.add_command(predict_run())
    cli_collection = LACLI(commands=[cli, create_cli])
    cli_collection()


if __name__ == "__main__":
    main()
