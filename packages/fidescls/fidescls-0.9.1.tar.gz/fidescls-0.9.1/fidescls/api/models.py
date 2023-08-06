"""
API related data models
"""
from typing import Dict, List, Iterable, Optional, Union
from pydantic import BaseModel


class SimilarityOptions(BaseModel):
    """Data model for the similarity method params"""

    possible_targets: Iterable
    top_n: Optional[Union[int, None]] = 1
    remove_stop_words: bool = False


class ContentOptions(BaseModel):
    """Data model for the content paradigm options"""

    language: str = "en"
    model: Optional[Union[str, None]] = None
    decision_method: str = "pass-through"


class ContentPayload(BaseModel):
    """Data model for the content paradigm"""

    data: Union[List, Dict]
    method: str = "default"
    method_params: ContentOptions


class ContextPayload(BaseModel):
    """Data model for the context paradigm"""

    data: Union[str, List]
    method: str = "similarity"
    method_params: SimilarityOptions


class AggregationPayload(BaseModel):
    """Data model for classification aggregation"""

    method: Optional[str]
    method_params: Optional[Dict]


class ClassifyPayload(BaseModel):
    """Data model for classification request payloads"""

    context: Optional[ContextPayload]
    content: Optional[ContentPayload]
    # suppressed for future functionality
    # agg: Optional[AggregationPayload]
