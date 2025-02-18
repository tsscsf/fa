import json

import openai
from dotenv import load_dotenv

from composer.composer import Composer
from frameworks.scvs.scvs import SCVS
from llm.llm import LLM

load_dotenv()  # pyright: ignore[reportUnusedCallResult]


def main():
    scvs = SCVS()
    client = openai.OpenAI()
    llm = LLM(client)
    composer = Composer(scvs, llm)

    decomposed_guidelines = composer.generate_sub_guidelines()

    # Convert Pydantic models to dictionaries
    guidelines_as_dicts = [
        guideline.model_dump() for guideline in decomposed_guidelines
    ]

    # Write to a JSON file with pretty printing
    with open("decomposed_guidelines.json", "w") as f:
        json.dump(guidelines_as_dicts, f, indent=4)


if __name__ == "__main__":
    main()
