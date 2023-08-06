"""
High level functionality around performing PII classification
"""
import logging
from typing import cast, List, Dict, Union

from presidio_analyzer import RecognizerResult

from fidescls.cls import (
    decision,
    util as _cls_util,
    config as _cls_config,
    models as _cls_models,
)

logger = logging.getLogger(__name__)


def format_method_labels(
    method_result: Union[None, RecognizerResult]
) -> _cls_models.MethodOutput:
    """
    Standardized the format of the recognizer results
    Args:
        method_result: A recognizer result
    """
    if method_result:
        return _cls_models.MethodOutput(
            label=method_result.entity_type,
            score=method_result.score,
            position_start=method_result.start,
            position_end=method_result.end,
        )
    return _cls_models.MethodOutput()


def format_cls_output(
    input_data: Union[List[str], Dict[str, List]],
    cls_output: List[Union[List[RecognizerResult], Dict[str, List[RecognizerResult]]]],
) -> Union[
    List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
]:
    """
    Format the content classifier's output to meet the spec
    Args:
        input_data: The data that was classified
        cls_output: The output of the classifier

    Returns:
        Formatted classification output to conform to the spec
    """
    formatted_output: Union[
        List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
    ]
    labels: Union[None, _cls_models.MethodOutput, List[_cls_models.MethodOutput]]

    if isinstance(cls_output, list) and isinstance(cls_output[0], list):
        formatted_output = []
        for i, input_value in enumerate(input_data):
            labels = [format_method_labels(cls_out) for cls_out in cls_output[i]]
            formatted_output.append(
                _cls_models.ClassifyOutput(input=input_value, labels=labels)
            )
    else:
        formatted_output = {}
        for cls_out in cls_output:
            cls_out_casted = cast(
                Dict[str, Union[str, List[RecognizerResult]]], cls_out
            )
            cls_out_result = cast(
                List[RecognizerResult], cls_out_casted["recognizer_results"]
            )
            cls_out_key = cast(str, cls_out_casted["key"])
            parsed_output = []
            for i, input_value in enumerate(cls_out_casted["value"]):
                if cls_out_result[i]:
                    labels = [
                        format_method_labels(j)
                        if cls_out_result[i]
                        else _cls_models.MethodOutput()
                        for j in cls_out_result[i]
                    ]
                else:
                    labels = [format_method_labels(None)]
                parsed_output.append(
                    _cls_models.ClassifyOutput(input=input_value, labels=labels)
                )
            formatted_output[cls_out_key] = parsed_output
    return formatted_output


def classify(
    data: Union[str, List[str], Dict[str, List]],
    language: str = _cls_config.LANGUAGE,
    model: str = None,
    decision_method: str = "pass-through",
) -> Union[
    List[_cls_models.ClassifyOutput], Dict[str, List[_cls_models.ClassifyOutput]]
]:
    """
    Perform a PII classification on data using the specified model and decision method
    Args:
        data: Data to be classified (list or dictionary)
        language: language for text model purposes. supported: ['en']
        model: specify which model to use. Default (None, "") is the BaseTextClassifier
        decision_method: specify which decision method to use. supported:
            'pass-through': direct pass-through of results from the model
            'direct-mapping': the mapped value described by an entity map

    Returns:
        The output from the classifier in the format dependent on the chosen `decision_method`

    """
    if isinstance(data, str):
        data = [data]
    logger.debug(f"Classifying {data} using decision: {decision_method}")
    if not model:
        cls = _cls_util.BaseTextClassifier()
    else:
        raise NotImplementedError("Only default model supported currently!")

    # perform the classification
    cls_label = cls.classify(data, language=language)

    # format the classification output
    formatted_cls_label = format_cls_output(data, cls_label)

    # implement any decision based on return if requested
    decision_result = decision.decide(formatted_cls_label, decision_method)
    return decision.rank_classification_results(decision_result)
