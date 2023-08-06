"""
Classification related data models
"""
from typing import List, Optional, Union

from pydantic import BaseModel


class MethodOutput(BaseModel):
    """Classification method output data model"""

    label: Optional[Union[str, List]]
    score: Optional[float]
    position_start: Optional[Union[int, None]] = None
    position_end: Optional[Union[int, None]] = None


class ClassifyOutput(BaseModel):
    """Classification output data model"""

    input: str
    labels: List[MethodOutput]
