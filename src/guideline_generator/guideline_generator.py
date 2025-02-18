import json

from llm.llm import LLM
from models.few_shot import FewShotExample
from models.guideline import DecomposedGuideline, Guideline


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

    def _guideline_for_prompt(self, guideline: Guideline) -> dict[str, str]:
        g = guideline.model_dump()
        g_prompt: dict[str, str] = {}
        if g["short"]:
            g_prompt["short_description"] = g["short"]
        if g["long"]:
            g_prompt["long_description"] = g["long"]
        if g["context"]:
            g_prompt["context"] = g["context"]
        return g_prompt

    def _format_prompt(
        self, guideline: Guideline, examples: list[FewShotExample]
    ) -> str:
        # Combine the guideline and examples into one dictionary

        prompt_dict = {
            "guideline": self._guideline_for_prompt(guideline),
            "examples": [example.model_dump() for example in examples],
        }
        # Convert the dictionary to a JSON string
        print(json.dumps(prompt_dict, indent=2))
        return json.dumps(prompt_dict, indent=2)
