from pydantic import BaseModel


class FewShotExample(BaseModel):
    original: str
    sub_guidelines: list[str]
