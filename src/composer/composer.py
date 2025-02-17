from frameworks.framework import Framework
from llm.llm import LLM
from models.few_shot import FewShotExample
from models.guideline import Guideline


class Composer:
    def __init__(self, framework: Framework, llm: LLM):
        self._framework: Framework = framework
        self._llm: LLM = llm

    def generate_sub_guidelines(self):
        for g in self._framework.guidelines():
            prompt = self.format_prompt(g, self._framework.few_shots())
            print(prompt)
            break

    def _format(self, guideline: Guideline) -> str:
        parts = ["Guideline:"]
        if guideline.short:
            parts.append(guideline.short)
        if guideline.long:
            parts.append(guideline.long)
        if guideline.context:
            parts.append(guideline.context)

        return "\n".join(parts)

    def format_prompt(
        self, guideline: Guideline, examples: list[FewShotExample]
    ) -> str:
        parts = [self._format(guideline)]

        if examples:
            parts.append("Examples:")
            for example in examples:
                parts.append(f"Input: {example.input}")
                parts.append("Output:")
                # Add each output line
                parts.extend(example.output)

        return "\n".join(parts)
