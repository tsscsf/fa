from typing import Any


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

    output: list[Any] = []
    for g in scvs.guidelines():
        decomposed_guideline = gg.generate_sub_guidelines(g, scvs.few_shots())
        json_output = decomposed_guideline.model_dump()
        json_output["framework"] = "SCVS"
        output.append(json_output)
        # Write to a JSON file with pretty printing
        with open("decomposed_guidelines.json", "w") as f:
            json.dump(output, f, indent=4)


if __name__ == "__main__":
    main()
