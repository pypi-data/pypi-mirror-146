"""
Supports the context classification functionality of fidecls.

Context in this case means metadata about a database such as
schema/table/column name

Analysis of PII through the metadata surrounding a table or
data sample(s)

"""

import logging
from typing import Iterable, List, Union

from fidescls.cls import models as _cls_models
from fidescls.utils import fides_nlp as _nlp


def cls_similarity(
    input_text: Union[str, Iterable],
    possible_targets: Iterable = (),
    top_n: Union[int, None] = 1,
    remove_stop_words: bool = False,
) -> List[_cls_models.ClassifyOutput]:
    """
    Perform similarity classification between an argument and a set of possible targets
    Args:
        input_text: Text for which to check similarity
        possible_targets: list of candidates to compare against
        top_n: number of similar responses to return in descending
        order. If None, all results will be returned
        remove_stop_words: flag to remove stop words from the text

    Returns:
        List of ClassifyOutputs containing the text and top_n most similar possible_targets
    """
    logging.debug("Performing context similarity classification...")

    if not isinstance(input_text, list):
        input_text = [input_text]

    target_docs = {
        possible_target: _nlp.tokenize(
            _nlp.preprocess_text(possible_target, remove_stop_words=remove_stop_words)
        )
        for possible_target in possible_targets
    }

    input_docs = {
        text: _nlp.tokenize(
            _nlp.preprocess_text(text, remove_stop_words=remove_stop_words)
        )
        for text in input_text
    }

    similarities = {}
    for raw_input, input_doc in input_docs.items():
        target_similarities = {}
        for raw_target, target_doc in target_docs.items():
            target_similarities[raw_target] = _nlp.similarity(input_doc, target_doc)
        # grab top n similar entries
        similarities[raw_input] = _nlp.get_top_n_dict(target_similarities, top_n=top_n)

    # format the output to meet the model standard
    formatted_output = []
    for sim_word, similar in similarities.items():
        formatted_output.append(
            _cls_models.ClassifyOutput(
                input=sim_word,
                labels=[
                    _cls_models.MethodOutput(
                        label=label_score[0],
                        score=label_score[1],
                        position_start=None,
                        position_end=None,
                    )
                    for label_score in similar
                ],
            )
        )

    return formatted_output
