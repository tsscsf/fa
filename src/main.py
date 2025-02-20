import datetime
import json
import os

import openai
from dotenv import load_dotenv

from frameworks.framework import Framework
from frameworks.s2c2f.s2c2f import S2C2F
from frameworks.scvs.scvs import SCVS
from frameworks.sok.sok import SoK
from guideline_generator.guideline_generator import GuidelineGenerator
from llm.llm import LLM
from models.guideline import DecomposedGuideline

load_dotenv()  # pyright: ignore[reportUnusedCallResult]


def store_generated_guidelines(
    framework: str, guidelines: list[DecomposedGuideline], date: str
) -> None:
    decomposed_guidelines = [g.model_dump() for g in guidelines]
    with open(f"data/{framework}/{date}_generated_guidelines.json", "w") as f:
        json.dump(decomposed_guidelines, f, indent=4)


def decompose(framework: Framework, gg: GuidelineGenerator):
    decomposed_guidelines: list[DecomposedGuideline] = []
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    for g in framework.guidelines():
        decomposed_guideline = gg.generate_sub_guidelines(
            g, framework.few_shots(), framework.system_prompt
        )
        decomposed_guidelines.append(decomposed_guideline)
        store_generated_guidelines(framework.name, decomposed_guidelines, date)


def main():
    scvs = SCVS()
    client = openai.OpenAI(base_url=os.environ.get("OPENAI_API_BASE", None))
    llm = LLM(client)
    gg = GuidelineGenerator(llm)
    s2c2f = S2C2F()
    sok = SoK()

    # decompose(s2c2f, gg)
    # decompose(sok, gg)
    decompose(scvs, gg)


if __name__ == "__main__":
    main()
