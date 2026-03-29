from pydantic import BaseModel, Field

class TextToTextTranslationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)