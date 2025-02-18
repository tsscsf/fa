from pydantic import BaseModel

from models.prompt import PromptInput


class FewShotExample(BaseModel):
    input: PromptInput
    output: list[str]
