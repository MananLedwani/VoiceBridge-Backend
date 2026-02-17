from fastapi import APIRouter, HTTPException, status
from app.models.text_to_text_model import TextToTextTranslationRequest
from app.utils.text_to_text_utils import bhashini_translate
from app.constants.constants import *

text_to_text_router = APIRouter(prefix="/text-to-text")

@text_to_text_router.post("/sanskrit", status_code=status.HTTP_201_CREATED)
def translate_text_to_sanskrit(request: TextToTextTranslationRequest):
    
    try:
        result = bhashini_translate(request.text, TEXT_TO_TEXT_HINDI_CODE, TEXT_TO_TEXT_SANSKRIT_CODE)
        return {"original": request.text, "translated_sanskrit": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@text_to_text_router.post("/hindi", status_code=status.HTTP_201_CREATED)
def translate_text_to_hindi(request: TextToTextTranslationRequest):
    
    try:
        result = bhashini_translate(request.text, TEXT_TO_TEXT_SANSKRIT_CODE, TEXT_TO_TEXT_HINDI_CODE)
        return {"original": request.text, "translated_hindi": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))