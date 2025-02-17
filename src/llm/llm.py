from collections.abc import Iterable

import openai
from openai.types.chat import ChatCompletionMessageParam
from openai.types.shared_params.response_format_json_object import (
    ResponseFormatJSONObject,
)

from models.llm_response import LLMResponse

DEFAULT_SYSTEM_PROMPT = """
    The user xxx.
    """
DEFAULT_RESPONSE_FORMAT = LLMResponse


class LLM:
    def __init__(self, client: openai.OpenAI, model: str = "gpt3.5-turbo") -> None:
        self._model: str = model
        self._client: openai.OpenAI = client
        self.system_prompt: str = DEFAULT_SYSTEM_PROMPT
        # Annotate as a type, since DEFAULT_RESPONSE_FORMAT is a class
        self.response_format: type[ResponseFormatJSONObject] = DEFAULT_RESPONSE_FORMAT

    def prompt(self, prompt: str) -> LLMResponse:
        messages: Iterable[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        parsed_response = self._client.beta.chat.completions.parse(
            model=self._model,
            messages=messages,
            response_format=self.response_format,
        )
        # Extract the parsed data from the first choice's message
        parsed_data = parsed_response.choices[0].message.parsed

        # Validate and load it into your LLMResponse pydantic model
        validated_response = LLMResponse.parse_obj(parsed_data)
        return validated_response
