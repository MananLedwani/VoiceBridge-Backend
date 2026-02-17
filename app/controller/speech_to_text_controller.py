from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.speech_to_text_utils import bhashini_asr
from app.constants.constants import *

speech_to_text_router = APIRouter(prefix="/speech-to-text")

@speech_to_text_router.post("/sanskrit")
async def translate_speech_to_sanskrit_text(file: UploadFile = File(...), audio_format: str = WAV_FORMAT):
    try:
        audio_bytes = await file.read()

        transcription = bhashini_asr(audio_bytes, source_lang=SPEECH_TO_TEXT_HINDI_CODE, audio_format=audio_format)

        return {
            "transcription": transcription,
            "language_used": SPEECH_TO_TEXT_HINDI_CODE,
            "provider": "Bhashini"
        }

    except Exception as e:
        print(f"Processing Error: {e}")
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")

@speech_to_text_router.post("/hindi")
async def translate_speech_to_hindi_text(file: UploadFile = File(...), audio_format: str = WAV_FORMAT):
    try:
        audio_bytes = await file.read()

        transcription = bhashini_asr(audio_bytes, source_lang=SPEECH_TO_TEXT_SANSKRIT_CODE, audio_format=audio_format)

        return {
            "transcription": transcription,
            "language_used": SPEECH_TO_TEXT_SANSKRIT_CODE,
            "provider": "Bhashini"
        }

    except Exception as e:
        print(f"Processing Error: {e}")
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}") 