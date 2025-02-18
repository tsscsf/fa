from collections.abc import Iterable

import openai
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion

from models.llm_response import LLMResponse

DEFAULT_SYSTEM_PROMPT = """
You are a guideline decomposition assistant. Your task is to take a given guideline that may contain compound statements or multiple components and break it down into smaller, independent guidelines. Follow these steps:

1. **Analyze the Guideline:** Read the input guideline carefully and identify any compound phrases, conjunctions (like "and", "or", "and/or"), or lists that combine multiple ideas.
2. **Decompose Step-by-Step:** Split the guideline into its individual parts, ensuring that each resulting statement clearly represents a single idea or requirement.
3. **Preserve Meaning:** Make sure that each decomposed guideline retains the intent and meaning of the original statement.
4. **Format the Output:** List each individual guideline on a separate line.

Let's think step by step...
"""
DEFAULT_RESPONSE_FORMAT = LLMResponse


class LLM:
    def __init__(self, client: openai.OpenAI, model: str = "gpt3.5-turbo", system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self._model: str = model
        self._client: openai.OpenAI = client
        self.system_prompt: str = DEFAULT_SYSTEM_PROMPT
        self.response_format = DEFAULT_RESPONSE_FORMAT  # pyright: ignore[reportUnannotatedClassAttribute]

    def prompt(self, prompt: str) -> list[str]:
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

        return validated_response.final_answer
