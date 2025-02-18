from pydantic import BaseModel


class PromptInput(BaseModel):
    short_description: str | None
    long_description: str | None
    context: str | None
