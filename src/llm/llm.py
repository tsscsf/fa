import json
from collections.abc import Iterable

import openai
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion

from models.llm_response import LLMResponse

DEFAULT_RESPONSE_FORMAT = LLMResponse


class LLM:
    def __init__(
        self,
        client: openai.OpenAI,
        model: str = "meta-llama/Llama-3.3-70B-Instruct",
    ):
        self._model: str = model
        self._client: openai.OpenAI = client
        self.response_format = DEFAULT_RESPONSE_FORMAT  # pyright: ignore[reportUnannotatedClassAttribute]

    def _prompt_gpt(self, prompt: str, system_prompt: str) -> LLMResponse:
        messages: Iterable[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        response: ParsedChatCompletion[LLMResponse] = (
            self._client.beta.chat.completions.parse(
                model=self._model,
                messages=messages,
                response_format=self.response_format,
                temperature=0.0,
            )
        )
        parsed_data: LLMResponse | None = response.choices[0].message.parsed
        validated_response: LLMResponse = LLMResponse.model_validate(parsed_data)

        return validated_response

    def _prompt_other(self, prompt: str, system_prompt: str) -> LLMResponse:
        messages: Iterable[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        response: ChatCompletion[LLMResponse] = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            extra_body={"guided_json": self.response_format.model_json_schema()},
            temperature=0.0,
        )
        data = response.choices[0].message
        if data.content is None:
            raise ValueError("Received empty response content")

        # ignore reportAny because we are validating against the pydantic model
        output_json = json.loads(data.content)  # pyright: ignore[reportAny]
        validated_response: LLMResponse = LLMResponse.model_validate(output_json)

        return validated_response

    def prompt(self, prompt: str, system_prompt: str) -> LLMResponse:
        if "gpt" in self._model.lower():
            return self._prompt_gpt(prompt, system_prompt)
        else:
            return self._prompt_other(prompt, system_prompt)
