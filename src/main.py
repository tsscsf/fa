import json

import openai
from dotenv import load_dotenv

from frameworks.scvs.scvs import SCVS
from guideline_generator.guideline_generator import GuidelineGenerator
from llm.llm import LLM

load_dotenv()  # pyright: ignore[reportUnusedCallResult]


def main():
    scvs = SCVS()
    client = openai.OpenAI()
    llm = LLM(client)
    gg = GuidelineGenerator(llm)

    for g in scvs.guidelines():
        decomposed_guideline = gg.generate_sub_guidelines(g, scvs.few_shots())

        # Write to a JSON file with pretty printing
        with open("decomposed_guidelines.json", "a") as f:
            json.dump(decomposed_guideline.model_dump(), f, indent=4)


if __name__ == "__main__":
    main()
