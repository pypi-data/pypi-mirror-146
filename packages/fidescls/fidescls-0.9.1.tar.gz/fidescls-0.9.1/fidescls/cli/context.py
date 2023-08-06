"""
Contains the groups and setup for the CLI.
"""

import click

from fidescls.cli.classify import classify
from fidescls.cli.scan import db
from fidescls.cli import logger as _cli_logger

logger = _cli_logger.config_logger()


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(name="fidescls", context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    The Fidescls command line interface to interact
    with the PII classification functionality
    """
    ctx.ensure_object(dict)


# Add new commands to the cli contex
cli.add_command(classify)
cli.add_command(db)
