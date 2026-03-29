from fastapi import APIRouter, HTTPException, status
from app.models.text_to_text_model import TextToTextTranslationRequest
from app.utils.text_to_text_utils import (
    gemini_translate_hindi_to_sanskrit, 
    gemini_translate_sanskrit_to_hindi
)

text_to_text_router = APIRouter(prefix="/text-to-text")

@text_to_text_router.post("/sanskrit", status_code=status.HTTP_201_CREATED)
def translate_text_to_sanskrit(request: TextToTextTranslationRequest):
    """Translates Hindi text to Sanskrit using Gemini 3.1 Pro."""
    try:
        result = gemini_translate_hindi_to_sanskrit(request.text)
        return {"original": request.text, "translated_sanskrit": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@text_to_text_router.post("/hindi", status_code=status.HTTP_201_CREATED)
def translate_text_to_hindi(request: TextToTextTranslationRequest):
    """Translates Sanskrit text to Hindi using Gemini 3.1 Pro."""
    try:
        result = gemini_translate_sanskrit_to_hindi(request.text)
        return {"original": request.text, "translated_hindi": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))