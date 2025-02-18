import json

import openai
from dotenv import load_dotenv

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


def main():
    scvs = SCVS()
    client = openai.OpenAI()
    llm = LLM(client)
    gg = GuidelineGenerator(llm)

    s2c2f = S2C2F()
    for g in s2c2f.guidelines():
        decomposed_guideline = gg.generate_sub_guidelines(g, s2c2f.few_shots())
        store_generated_guidelines(s2c2f.name, [decomposed_guideline])

    for g in scvs.guidelines():
        decomposed_guideline = gg.generate_sub_guidelines(g, scvs.few_shots())
        store_generated_guidelines(scvs.name, [decomposed_guideline])


if __name__ == "__main__":
    main()
