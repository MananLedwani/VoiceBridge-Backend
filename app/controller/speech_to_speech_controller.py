from fastapi import APIRouter

speech_to_speech_router = APIRouter(prefix="/speech-to-speech")

@speech_to_speech_router.post("/sanskrit")
def translate_speech_to_sanskrit_speech():
    pass 

@speech_to_speech_router.post("/hindi")
def translate_speech_to_hindi_speech():
    pass 

