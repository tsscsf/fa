import json

from llm.llm import LLM
from models.few_shot import FewShotExample
from models.guideline import DecomposedGuideline, Guideline
from models.prompt import PromptInput


class GuidelineGenerator:
    def __init__(self, llm: LLM) -> None:
        self._llm: LLM = llm

    def generate_sub_guidelines(
        self, guideline: Guideline, few_shots: list[FewShotExample]
    ) -> DecomposedGuideline:
        prompt: str = self._format_prompt(guideline=guideline, examples=few_shots)
        response = self._llm.prompt(prompt)
        return DecomposedGuideline(
            original=guideline, decomposed=response.final_answer, steps=response.steps
        )

    def _guideline_for_prompt(self, guideline: Guideline) -> PromptInput:
        g = guideline.model_dump()
        prompt_input = PromptInput(
            short_description=None,
            long_description=None,
            context=None,
        )
        if g["short"]:
            prompt_input.short_description = g["short"]
        if g["long"]:
            prompt_input.long_description = g["long"]
        if g["context"]:
            prompt_input.context = g["context"]

        return prompt_input

    def _format_prompt(
        self, guideline: Guideline, examples: list[FewShotExample]
    ) -> str:
        # Combine the guideline and examples into one dictionary

        prompt_dict = {
            "guideline": self._guideline_for_prompt(guideline).model_dump(),
            "examples": [example.model_dump() for example in examples],
        }
        # Convert the dictionary to a JSON string
        print(json.dumps(prompt_dict, indent=2))
        return json.dumps(prompt_dict, indent=2)
