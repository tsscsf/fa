import json

import openai
from dotenv import load_dotenv

from frameworks.framework import Framework
from frameworks.s2c2f.s2c2f import S2C2F
from frameworks.scvs.scvs import SCVS
from guideline_generator.guideline_generator import GuidelineGenerator
from llm.llm import LLM
from models.guideline import DecomposedGuideline

load_dotenv()  # pyright: ignore[reportUnusedCallResult]


def store_generated_guidelines(
    framework: str, guidelines: list[DecomposedGuideline]
) -> None:
    with open(f"data/{framework}/generated_guidelines.json", "w") as f:
        json.dump(guidelines, f, indent=4)


def decompose(framework: Framework, gg: GuidelineGenerator):
    for g in framework.guidelines():
        decomposed_guideline = gg.generate_sub_guidelines(g, framework.few_shots())
        store_generated_guidelines(framework.name, [decomposed_guideline])


def main():
    scvs = SCVS()
    client = openai.OpenAI()
    llm = LLM(client)
    gg = GuidelineGenerator(llm)
    s2c2f = S2C2F()

    decompose(s2c2f, gg)
    decompose(scvs, gg)


if __name__ == "__main__":
    main()
