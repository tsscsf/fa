from pydantic import BaseModel


class LLMResponse(BaseModel):
    response: list[str]
