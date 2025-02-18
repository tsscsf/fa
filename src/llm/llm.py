from collections.abc import Iterable

import openai
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion

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
        self.response_format: type[LLMResponse] = DEFAULT_RESPONSE_FORMAT

    def prompt(self, prompt: str) -> LLMResponse:
        messages: Iterable[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        parsed_response: ParsedChatCompletion[LLMResponse] = self._client.beta.chat.completions.parse(
            model=self._model,
            messages=messages,
            response_format=self.response_format,
        )
        # Extract the parsed data from the first choice's message
        parsed_data: LLMResponse | None = parsed_response.choices[0].message.parsed

        # Validate and load it into your LLMResponse pydantic model
        validated_response: LLMResponse = LLMResponse.model_validate(parsed_data)
        return validated_response
