"""
Base text classification functionality
"""
import logging
from typing import cast, Union, List, Dict

from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_analyzer.nlp_engine import NlpEngineProvider

from fidescls.cls import config as _cconf

logger = logging.getLogger(__name__)


class BatchAnalyzerEngine(AnalyzerEngine):
    """
    Class inheriting from AnalyzerEngine and adds the functionality
    to analyze lists or dictionaries.
    https://microsoft.github.io/presidio/samples/python/batch_processing/#set-up-classes-for-batch-processing
    """

    def __init__(self, small_model: bool = True):
        """
        Use the small english model instead of the default large one for speed
        TODO: make this configurable
        """
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_sm" if small_model else "en_core_web_lg",
                }
            ],
        }
        provider = NlpEngineProvider(nlp_configuration=configuration)
        super().__init__(nlp_engine=provider.create_engine())

    def analyze_list(
        self,
        list_of_texts: List[str],
        language: str = _cconf.LANGUAGE,
        **kwargs: List[str],
    ) -> List[List[RecognizerResult]]:
        """
        Analyze a list of strings

        Args:
            list_of_texts: A list containing strings to be analyzed
            language: language string
            **kwargs: Additional parameters for the `AnalyzerEngine.analyze` method

        Returns:

        """

        list_results = []
        for text in list_of_texts:
            results = (
                self.analyze(text, language, **kwargs) if isinstance(text, str) else []
            )
            list_results.append(results)
        return list_results

    def analyze_dict(
        self,
        input_dict: Dict[str, Union[object, List[object]]],
        language: str = _cconf.LANGUAGE,
        **kwargs: List[str],
    ) -> List[Dict[str, Union[str, List, RecognizerResult]]]:
        """
        Analyze a dictionary of keys (strings) and values (either object or List[object]).
        Non-string values are returned as is.

        Args:
            input_dict: The input dictionary for analysis
            language: language string
            **kwargs: Additional keyword arguments for the `AnalyzerEngine.analyze` method

        Returns:

        """
        results = []
        for key, values in input_dict.items():
            item_result: Union[
                List[None], List[RecognizerResult], List[List[RecognizerResult]]
            ]
            if not values:
                item_result = []
            else:
                if isinstance(values, str):
                    item_result = self.analyze(values, language, **kwargs)
                elif isinstance(values, List):
                    item_result = self.analyze_list(
                        list_of_texts=cast(List[str], values),
                        language=language,
                        **kwargs,
                    )
                else:
                    item_result: List[None] = []  # type: ignore
            results.append(
                {"key": key, "value": values, "recognizer_results": item_result}
            )
        return results


class BaseTextClassifier(BatchAnalyzerEngine):
    """
    Presidio based text PII classifier/analyzer
    """

    def classify(
        self,
        raw_text: Union[str, List[str], Dict[str, List]],
        language: str = _cconf.LANGUAGE,
        **kwargs: List[str],
    ) -> Union[
        List[Union[List[RecognizerResult], Dict[str, List[RecognizerResult]]]],
        List[RecognizerResult],
    ]:
        """
        High level, standardized function call for text classification
        Args:
            raw_text: input data to be classified
            language: language string
            **kwargs: keyword arguments that get passed onto the `AnalyzerEngine.analyze` method

        Returns:

        """
        classify_result: Union[
            List[Union[List[RecognizerResult], Dict[str, List[RecognizerResult]]]],
            List[RecognizerResult],
        ]
        logger.debug(
            f"BaseTextClassifier classify inputs: {raw_text}, {language}, {kwargs}"
        )
        if isinstance(raw_text, list):
            logger.debug("Classifying a list")
            classify_result = self.analyze_list(raw_text, language, **kwargs)
        elif isinstance(raw_text, dict):
            logger.debug("Classifying a dict")
            raw_dict = cast(Dict[str, Union[object, List[object]]], raw_text)
            classify_result = self.analyze_dict(raw_dict, language, **kwargs)
        else:
            logger.debug("Classifying a string")
            classify_result = self.analyze(raw_text, language, **kwargs)

        logger.debug(f"Classify result: {classify_result}")
        return classify_result
