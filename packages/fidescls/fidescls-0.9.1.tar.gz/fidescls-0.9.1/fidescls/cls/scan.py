"""
Utility functionality to support the scanning of a database for PII
"""

from collections import defaultdict
from typing import Callable, Dict, List, Union

import click
import pandas as pd
from sqlalchemy.engine.base import Engine
from tqdm import tqdm

from fidescls.cls import content, context
from fidescls.utils import databases as _db

try:
    from fideslang import default_taxonomy
except ModuleNotFoundError:
    raise click.ClickException("Unable to find fidesctl, please install!")


def nested_default_dict() -> defaultdict[defaultdict]:  # type: ignore
    """
    Create an infinitely nestable dictionary
    """
    return defaultdict(nested_default_dict)


def db_context_classify(
    metadata_df: pd.DataFrame,
    data_categories: Union[List, None] = None,
    context_method: Callable = context.cls_similarity,
    method_params: Dict = {},
    hide_progress: bool = False,
) -> defaultdict:
    """
    Perform context classification given a database's schema metadata
    Args:
        metadata_df: dataframe containing database metadata
        data_categories: list of categories to check similarity against (None: uses default taxonomy)
        context_method: method to use when performing context classification
        method_params: context classification method kwargs
        hide_progress: flag to disable displaying of progress bars

    Returns:
        Nested dictionary containing schema:table:column = [classification results]
    """
    if not hide_progress:
        click.secho("Classifying database context...", fg="white")

    if not data_categories:
        taxonomy = default_taxonomy.DEFAULT_TAXONOMY
        data_categories = [i.fides_key for i in taxonomy.data_category]

    context_labels = nested_default_dict()
    for _, row in tqdm(
        metadata_df.iterrows(),
        total=metadata_df.shape[0],
        disable=hide_progress,
        desc="Tables",
        position=0,
    ):
        for column in tqdm(
            row["columns"],
            disable=hide_progress,
            desc="Columns",
            leave=False,
            position=1,
        ):
            context_labels[row["schema"]][row["table"]][column] = [
                i.dict()
                for i in context_method(
                    f"{row['schema']}.{row['table']}.{column}",
                    data_categories,
                    **method_params,
                )
            ]
    return context_labels


def db_content_classify(
    db_engine: Engine,
    metadata_df: pd.DataFrame,
    num_samples: int = 1,
    content_method: Callable = content.classify,
    method_params: dict = {},
    hide_progress: bool = False,
) -> defaultdict[defaultdict]:  # type: ignore
    """
    Perform content classification on a sample dataset taken from tables in a database
    Args:
        db_engine: sqlalchemy database engine
        metadata_df: dataframe containing database metadata
        num_samples: number of samples to take from each table
        content_method: method to use when performing content classification
        method_params: content classification method kwargs
        hide_progress: flag to disable displaying of progress bars

    Returns:
        Nested dictionary containing schema:table:column = [classification results]
    """
    if not hide_progress:
        click.secho(
            f"Classifying database content using {num_samples} sample(s)..", fg="white"
        )

    data_samples_cls = nested_default_dict()
    for _, row in tqdm(
        metadata_df.iterrows(),
        total=metadata_df.shape[0],
        disable=hide_progress,
        desc="Samples",
        leave=False,
    ):
        table_samples = _db.get_table_samples(
            db_engine, ".".join([row["schema"], row["table"]]), num_samples=num_samples
        )
        if table_samples:
            data_samples_cls[row["schema"]][row["table"]] = content_method(
                table_samples, **method_params
            )
        else:
            data_samples_cls[row["schema"]][row["table"]] = {}
    return data_samples_cls


def label_database(
    connection_string: str,
    classify_context: bool = False,
    classify_content: bool = False,
    context_method: Callable = context.cls_similarity,
    content_method: Callable = content.classify,
    context_method_params: Dict = {},
    content_method_params: Dict = {"decision_method": "direct-mapping"},
    num_samples: int = 1,
    quiet: bool = False,
) -> Dict[str, Dict]:
    """
    Perform context and/or content classification on a mysql or postgres database
    Args:
        connection_string:  sqlalchemy compatible database connection string
        classify_context: flag to perform context classification (default: False)
        classify_content: flag to perform content classification (default: True)
        context_method: method to use when performing context classification
        content_method: kwargs to pass to the context classification method
        context_method_params: method kwargs to pass to the context classification method
        content_method_params: method kwargs to pass to the context classification method
        num_samples: number of samples to use when collecting data for content classification
        quiet: flag to disable progress bars and feedback

    Returns:
        Dictionary containing the results for content and/or context classification
        for each column in each table of the database
    """
    # check to see that any inspection is happening
    if not classify_context and not classify_content:
        raise click.exceptions.ClickException("No classification method selected!")

    db_engine = _db.get_engine(connection_string, verbose=True)
    db_metadata = _db.scan_database_metadata(connection_string)
    metadata_df = _db.metadata_to_dataframe(db_metadata)

    dataset_labels = {}
    if classify_context and context_method:
        context_cls_results = db_context_classify(
            metadata_df,
            context_method=context_method,
            method_params=context_method_params,
            hide_progress=quiet,
        )
        dataset_labels["context"] = context_cls_results

    if classify_content and content_method:
        content_cls_results = db_content_classify(
            db_engine,
            metadata_df,
            num_samples=num_samples,
            content_method=content_method,
            method_params=content_method_params,
            hide_progress=quiet,
        )
        dataset_labels["content"] = content_cls_results
    return dataset_labels  # type: ignore
