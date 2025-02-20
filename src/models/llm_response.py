from pydantic import BaseModel


class LLMResponse(BaseModel):
    final_answer: list[str]
