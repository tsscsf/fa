from llm.llm import LLM
from models.few_shot import FewShotExample
from models.guideline import DecomposedGuideline, Guideline


class GuidelineGenerator:
    def __init__(
        self,
        llm: LLM,
    ) -> None:
        self._llm: LLM = llm

    def generate_sub_guidelines(
        self, guideline: Guideline, few_shots: list[FewShotExample]
    ) -> DecomposedGuideline:
        prompt: str = self._format_prompt(guideline=guideline, examples=few_shots)
        response = self._llm.prompt(prompt)
        return DecomposedGuideline(
            original=guideline, decomposed=response.final_answer, steps=response.steps
        )

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

    def _format_prompt(
        self, guideline: Guideline, examples: list[FewShotExample]
    ) -> str:
        parts: list[str] = [self._format_guideline(guideline)]

        parts.append("--Few-shot example(s)--")
        for example in examples:
            parts.append(self._format_few_shot(example))

        return "\n".join(parts)
