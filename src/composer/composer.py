from frameworks.framework import Framework
from llm.llm import LLM
from models.few_shot import FewShotExample
from models.guideline import DecomposedGuideline, Guideline


class Composer:
    def __init__(self, framework: Framework, llm: LLM) -> None:
        self._framework: Framework = framework
        self._llm: LLM = llm

    def generate_sub_guidelines(self) -> list[DecomposedGuideline]:
        decomposed_guidelines: list[DecomposedGuideline] = []
        for g in self._framework.guidelines():
            prompt: str = self.format_prompt(guideline=g, examples=self._framework.few_shots())
            response: list[str] = self._llm.prompt(prompt)
            decomposed_guidelines.append(DecomposedGuideline(original=g, decomposed=response))
        return decomposed_guidelines

    def _format_guideline(self, guideline: Guideline) -> str:
        parts: list[str] = ["--Full guideline--"]
        if guideline.short:
            parts.append(f"Short description: {guideline.short}")
        if guideline.long:
            parts.append(f"Long description: {guideline.long}")
        if guideline.context:
            parts.append(f"Context: {guideline.context}")

        return "\n".join(parts)

    def _format_few_shot(self, example: FewShotExample) -> str:
        parts: list[str] = []
        parts.append(f"Input: {example.input}")
        parts.append("Output:")
        # Add each output line
        parts.extend(example.output)

        return "\n".join(parts)

    def format_prompt(
        self, guideline: Guideline, examples: list[FewShotExample]
    ) -> str:
        parts: list[str] = [self._format_guideline(guideline)]

        parts.append("--Few-shot example(s)--")
        for example in examples:
            parts.append(self._format_few_shot(example))

        return "\n".join(parts)
