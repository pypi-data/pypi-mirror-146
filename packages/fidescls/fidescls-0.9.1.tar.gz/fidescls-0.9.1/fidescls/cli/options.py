"""
Common options and arguments for cli commands
"""

from typing import Callable

import click

from fidescls.cls import config as _cls_config


def decision_method(command: Callable) -> Callable:
    """
    determine which decision method to use
    """
    return click.option(
        "-d",
        "--decision-method",
        "decision_method",
        type=str,
        default="pass-through",
        help="Decision method [pass-through | direct-mapping]",
    )(command)


# language option
def language(command: Callable) -> Callable:
    """
    Add an option for language selection
    """
    return click.option(
        "-l",
        "--language",
        "language",
        type=str,
        default=_cls_config.LANGUAGE,
        help="Text language for NLP processing",
    )(command)


def model(command: Callable) -> Callable:
    """
    Add an option for ml model selection
    """
    return click.option(
        "-m", "--model", "model", default=None, type=str, help="ML model to use"
    )(command)


def top_n(command: Callable) -> Callable:
    """
    Add an option to select the number of classification results to return
    """
    return click.option(
        "-n",
        "--top-n",
        "top_n",
        type=click.IntRange(1, clamp=True),
        default=1,
        help="""Number of results to return from the PII classification process""",
    )(command)


def possible_targets(command: Callable) -> Callable:
    """
    Add an option to provide an array of similarity targets to compare against
    """
    return click.option(
        "-p",
        "--possible-targets",
        "possible_targets",
        type=str,
        nargs=1,
        default="",
        help='Comma separated string containing a list of possible targets (i.e. "target1, target2")',
    )(command)


def remove_stop_words(command: Callable) -> Callable:
    """
    Add an option to provide an array of similarity targets to compare against
    """
    return click.option(
        "-s",
        "--remove-stop-words",
        "remove_stop_words",
        default=False,
        is_flag=True,
        help="Flag to remove stop words when processing",
    )(command)


def use_content(command: Callable) -> Callable:
    """
    Add option flag to use content classification
    """
    return click.option(
        "--content",
        "use_content",
        default=False,
        is_flag=True,
        help="Flag to use content classification",
    )(command)


def use_context(command: Callable) -> Callable:
    """
    Add option flag to use context classification
    """
    return click.option(
        "--context",
        "use_context",
        default=False,
        is_flag=True,
        help="Flag to use context classification",
    )(command)
