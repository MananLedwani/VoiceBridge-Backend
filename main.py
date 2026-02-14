from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.speech_to_speech_controller import speech_to_speech_router
from app.controller.text_to_speech_controller import text_to_speech_router
from app.controller.speech_to_text_controller import speech_to_text_router
from app.controller.text_to_text_controller import text_to_text_router

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(speech_to_speech_router)
app.include_router(text_to_speech_router)
app.include_router(text_to_speech_router)
app.include_router(text_to_text_router)

@app.get("/health")
def check_health_status():
    return {"status" : "ok"}

