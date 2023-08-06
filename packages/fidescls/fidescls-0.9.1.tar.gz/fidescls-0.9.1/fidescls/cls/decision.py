"""
This file holds the decision functionality.  What to do after data goes through the classifier
"""

import logging
from enum import Enum
from typing import cast, Dict, List, Union

from fidescls.cls import entity_map, models as _cls_models


class DecisionTypeEnum(Enum):
    """
    Enum object to capture valid decision types
    """

    PASS_THROUGH = "pass-through"
    DIRECT_MAPPING = "direct-mapping"


def rank_classification_results(
    cls_results: Union[
        List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
    ],
    desc: bool = True,
) -> Union[
    List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
]:
    """
    Order the classification results by classification score
    Args:
        cls_results: The result output from classification
        desc: flag to set ranking order

    Returns:
        the same as the classification output but with the results ranked in order
    """
    if isinstance(cls_results, dict):
        for cls_output in cls_results.values():
            for result in cls_output:
                result.labels.sort(key=lambda x: getattr(x, "score"), reverse=desc)
    else:
        for result in cls_results:
            result.labels.sort(key=lambda x: getattr(x, "score"), reverse=desc)
    return cls_results


def decide(
    cls_result: Union[
        List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
    ],
    decision_method: str,
) -> Union[
    List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
]:
    """
    Determine which decision method to use
    Args:
        cls_result: the classification result from the method used
        decision_method: the choice in decision method to use

    Returns:

    """
    # Get decision method by string
    if decision_method == DecisionTypeEnum.DIRECT_MAPPING.value:
        return direct_mapping(cls_result)
    if decision_method == DecisionTypeEnum.PASS_THROUGH.value:
        return pass_through(cls_result)
    raise ValueError(
        f"Invalid Decision Type. Must be one of {[i.value for i in DecisionTypeEnum]}"
    )


def pass_through(
    cls_result: Union[
        List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
    ]
) -> Union[
    List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
]:
    """
    Raw pass-through of the result from the classifier
    Args:
        cls_result: the result output from a classifier

    Returns:

    """
    return cls_result


def convert_entity_to_category(
    category: str, method_output: _cls_models.MethodOutput
) -> _cls_models.MethodOutput:
    """
    convert a classification method output label to a data category while retaining the output attributes
    Args:
        category: the data category to use as the new label
        method_output: the classification method output with a PII entity label

    Returns:
        the converted classification method output with the data category as its label
    """
    return _cls_models.MethodOutput(
        label=category,
        score=method_output.score,
        position_start=method_output.position_start,
        position_end=method_output.position_end,
    )


def convert_entities_to_categories(
    classify_output: _cls_models.ClassifyOutput,
    entity_category_mapping: Union[Dict, None] = None,
) -> List[_cls_models.MethodOutput]:
    """
    Convert the PII entity labels from a classification result to a mapped alternative
    Args:
        classify_output: the classification result
        entity_category_mapping: the mapping to use to convert the pii entity labels

    Returns:
        List of the newly converted classification method labels
    """
    if not entity_category_mapping:
        entity_category_mapping = entity_map.ENTITIES

    mapped_results = []
    for classification_label in classify_output.labels:
        try:
            mapped_labels = cast(
                List, entity_category_mapping[cast(str, classification_label.label)]
            )
            mapped_results.extend(
                [
                    convert_entity_to_category(label, classification_label)
                    for label in mapped_labels
                ]
            )
        except KeyError:
            mapped_results = []
    return mapped_results


def direct_mapping(
    classification_output: Union[
        List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
    ],
    entity_category_mapping: Union[Dict, None] = None,
) -> Union[
    List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
]:
    """
    make decision based on direct mapping to default fides taxonomy data_categories

    Args:
        classification_output: the result output from a classifier
        entity_category_mapping: dictionary mapping the class labels to data_categories

    Returns:
        classification result with mapped labels
    """
    logging.debug(
        f"Performing direct-mapping on classification results - result type {type(classification_output)}"
    )
    if isinstance(classification_output, dict):
        for classification_results in classification_output.values():
            logging.debug(f"Mapping data categories for {classification_results}")
            for classification_result in classification_results:
                classification_result.labels = convert_entities_to_categories(
                    classification_result,
                    entity_category_mapping=entity_category_mapping,
                )
    else:
        for classification_result in classification_output:
            logging.debug(f"Mapping data categories for {classification_result}")
            classification_result.labels = convert_entities_to_categories(
                classification_result, entity_category_mapping=entity_category_mapping
            )
    return classification_output
