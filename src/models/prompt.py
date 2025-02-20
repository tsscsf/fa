from pydantic import BaseModel


class PromptInput(BaseModel):
    short_description: str | None
    long_description: str | None = None
    context: str | None = None
