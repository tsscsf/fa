from pydantic import BaseModel


class FewShotExample(BaseModel):
    input: str
    output: list[str]
