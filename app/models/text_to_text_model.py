from pydantic import BaseModel

class TextToTextTranslationRequest(BaseModel):
    text: str