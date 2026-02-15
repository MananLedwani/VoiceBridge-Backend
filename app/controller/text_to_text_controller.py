from fastapi import APIRouter, HTTPException, status
from app.models.text_to_text_model import TextToTextTranslationRequest
from app.utils.text_to_text_utils import perform_text_to_text_translation
from app.constants.constants import *

text_to_text_router = APIRouter(prefix="/text-to-text")

@text_to_text_router.post("/sanskrit", status_code=status.HTTP_201_CREATED)
def translate_text_to_sanskrit(request: TextToTextTranslationRequest):
    
    if not request.text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text cannot be empty")
    
    translation: str = perform_text_to_text_translation(request.text, src_lang=TEXT_TO_TEXT_HINDI_CODE, tgt_lang=TEXT_TO_TEXT_SANSKRIT_CODE)

    return {"original": request.text, "translated_sanskrit": translation}

@text_to_text_router.post("/hindi", status_code=status.HTTP_201_CREATED)
def translate_text_to_hindi(request: TextToTextTranslationRequest):
    
    if not request.text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text cannot be empty")
    
    translation: str = perform_text_to_text_translation(request.text, src_lang=TEXT_TO_TEXT_SANSKRIT_CODE, tgt_lang=TEXT_TO_TEXT_HINDI_CODE)

    return {"original": request.text, "translated_hindi": translation}