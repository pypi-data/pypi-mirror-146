"""
Classifier API Endpoint
"""
import logging
from typing import List, Dict, Union

from fastapi import APIRouter

from fidescls.api import config as _aconf, models as _api_models
from fidescls.cls import models as _cls_models, context, content

logger = logging.getLogger(_aconf.LOGGER_NAME)

routers = []
for resource_type in _aconf.RESOURCES:
    router = APIRouter(tags=["Classify", resource_type], prefix=f"/{resource_type}")

    @router.post(f"/{_aconf.CLASSIFY_ENDPOINT}")
    async def classify(
        payload: _api_models.ClassifyPayload,
    ) -> Union[
        None,
        Dict[
            str,
            Union[
                List[_cls_models.ClassifyOutput],
                Dict[str, List[_cls_models.ClassifyOutput]],
            ],
        ],
    ]:
        """
        Perform PII classification
        Args:
            payload: request payload containing fields described in the ClassifyPayload data model

        Returns:
            The result of the classification

        Raises:
            HTTPException of status code
        """
        response: Dict[
            str,
            Union[
                List[_cls_models.ClassifyOutput],
                Dict[str, List[_cls_models.ClassifyOutput]],
            ],
        ] = {}
        if payload.context:
            if payload.context.method == "similarity":
                logger.debug(f"Similarity Request Payload:\n{payload.dict()}")
                context_labels = context.cls_similarity(
                    payload.context.data,
                    possible_targets=payload.context.method_params.possible_targets,
                    top_n=payload.context.method_params.top_n,
                    remove_stop_words=payload.context.method_params.remove_stop_words,
                )
                response["context"] = context_labels
        if payload.content:
            if payload.content.method == "default":
                content_labels = content.classify(
                    payload.content.data,
                    language=payload.content.method_params.language,
                    model=payload.content.method_params.model,
                    decision_method=payload.content.method_params.decision_method,
                )
                response["content"] = content_labels
        return response

    routers.append(router)
