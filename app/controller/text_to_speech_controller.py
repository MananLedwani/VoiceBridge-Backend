from fastapi import APIRouter

text_to_speech_router = APIRouter(prefix="/text-to-speech")


@text_to_speech_router.post("/sanskrit")
def translate_text_to_sanskrit_speech():
    pass 

@text_to_speech_router.post("/hindi")
def translate_text_to_hindi_speech():
    pass