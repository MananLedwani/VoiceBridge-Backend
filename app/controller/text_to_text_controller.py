from fastapi import APIRouter

text_to_text_router = APIRouter(prefix="/text-to-text")

@text_to_text_router.post("/sanskrit")
def translate_text_to_sanskrit():
    pass

@text_to_text_router.post("/hindi")
def translate_text_to_hindi():
    pass