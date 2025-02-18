from pydantic import BaseModel


class Guideline(BaseModel):
    id: str | None
    short: str | None
    long: str | None
    level: str | None
    context: str | None


class DecomposedGuideline(BaseModel):
    original: Guideline
    decomposed: list[str]
    steps: list[str]
