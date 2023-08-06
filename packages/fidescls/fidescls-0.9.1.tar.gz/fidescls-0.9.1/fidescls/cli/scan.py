"""
CLI command wrappers for database scanning and classification functionality
"""
import pprint
import json
import click

from fastapi.encoders import jsonable_encoder

from fidescls.cli import options as _opt


@click.group(name="db")
def db() -> None:
    """
    A CLI command group focused on database scanning for classification
    """
    # pylint: disable=invalid-name
    ...


@db.command(name="classify")
@click.pass_context
@_opt.top_n
@_opt.use_context
@_opt.use_content
@click.argument("connection_string", type=str)
@click.option(
    "-f",
    "--filename",
    "file_name",
    type=str,
    nargs=1,
    default="",
    help="filename to save database classification output json",
)
@click.option(
    "-q",
    "--quiet",
    "quiet",
    type=bool,
    default=False,
    help="Disable progress bars and feedback",
)
def classify(
    ctx: click.Context,
    connection_string: str,
    file_name: str,
    use_context: bool,
    use_content: bool,
    top_n: int,
    quiet: bool,
) -> None:
    """
    Classify PII in each column of each table of a database
    """
    from fidescls.cls import scan as _scan

    db_cls_output = _scan.label_database(
        connection_string,
        classify_context=use_context,
        classify_content=use_content,
        num_samples=top_n,
        quiet=quiet,
    )
    if file_name:
        with open(file_name, "w", encoding="utf-8") as output_file:
            json.dump(jsonable_encoder(db_cls_output), output_file)
    else:
        click.secho(pprint.pformat(jsonable_encoder(db_cls_output)), fg="white")
