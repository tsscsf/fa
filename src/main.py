import openai

from composer.composer import Composer
from frameworks.scvs.scvs import SCVS
from llm.llm import LLM


def main():
    scvs = SCVS()
    client = openai.OpenAI()
    llm = LLM(client)
    composer = Composer(scvs, llm)
    composer.generate_sub_guidelines()


if __name__ == "__main__":
    main()
