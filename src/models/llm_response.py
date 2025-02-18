from pydantic import BaseModel


class LLMResponse(BaseModel):
    steps: list[str]
    final_answer: list[str]
