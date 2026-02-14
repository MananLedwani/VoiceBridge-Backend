from fastapi import APIRouter

speech_to_text_router = APIRouter(prefix="/speech-to-text")

@speech_to_text_router.post("/sanskrit")
def translate_speech_to_sanskrit_text():
    pass 

@speech_to_text_router.post("/hindi")
def translate_speech_to_hindi_text():
    pass 