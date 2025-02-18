from pydantic import BaseModel


class Step(BaseModel):
    explanation: str
    output: str


class LLMResponse(BaseModel):
    steps: list[Step]
    final_answer: list[str]

