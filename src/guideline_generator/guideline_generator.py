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
        self._llm.system_prompt = "Decompose the given statements into granular, standalone sub-guidelines. Only decompose statements that can be actionable. If a guideline is already a single statement, retain it unchanged. Do not infer any information that is not present in the original statement. It should be possible to read as sub guideline as a standalone statement without any additional context required. Keep all information and make sure that each sub statement do not change the meaning of the original statement."
        # self._llm.system_prompt = "Decompose short_description and long_description into granular sub-guidelines. Keep only actionable statements—what to do, not how to do it. Keep single actionable statements unchanged. Ignore non-actionable statements. Each guideline should be read as a standalone statement without any context required."
        prompt: str = self._format_prompt(guideline=guideline, examples=few_shots)
        response = self._llm.prompt(prompt)

        # # self._llm.system_prompt = "Decompose the list of statements if they can be turned into sub statements. If not, keep the statement as it is. Keep all information and make sure that each sub statement do not change the meaning of the original statement. Each sub statement should be possible to read as a standalone statement without any additional context required. Do not infer any information that is not present in the original statement."
        # prompt = "\n".join(response.final_answer)
        # response = self._llm.prompt(prompt)

        return DecomposedGuideline(
            original=guideline, decomposed=response.final_answer, steps=[]
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
            # "examples": [example.model_dump() for example in examples],
        }
        # Convert the dictionary to a JSON string
        print(json.dumps(prompt_dict, indent=2))
        return json.dumps(prompt_dict, indent=2)
