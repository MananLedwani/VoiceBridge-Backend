from fastapi import APIRouter, Response, HTTPException
from app.utils.text_to_speech_utils import bhashini_tts
from app.models.text_to_speech_model import TTSRequest
from app.constants.constants import *

text_to_speech_router = APIRouter(prefix="/text-to-speech")


@text_to_speech_router.post("/sanskrit")
async def translate_text_to_sanskrit_speech(request: TTSRequest):
    try:
        audio_bytes = bhashini_tts(request.text, TEXT_TO_SPEECH_SANSKRIT_CODE)

        if not audio_bytes:
            raise HTTPException(status_code=500, detail="No audio received from Bhashini")

        return Response(content=audio_bytes, media_type="audio/wav")

    except Exception as e:
        print(f"TTS Error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 

@text_to_speech_router.post("/hindi")
async def translate_text_to_hindi_speech(request: TTSRequest):
    try:
        audio_bytes = bhashini_tts(request.text, TEXT_TO_SPEECH_HINDI_CODE)

        if not audio_bytes:
            raise HTTPException(status_code=500, detail="No audio received from Bhashini")

        return Response(content=audio_bytes, media_type="audio/wav")

    except Exception as e:
        print(f"TTS Error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 