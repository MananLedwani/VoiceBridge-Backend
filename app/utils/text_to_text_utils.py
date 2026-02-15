from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import HTTPException, status
from app.constants.constants import *


print(f"Loading translation model: {TEXT_TO_TEXT_MODEL_NAME}...")

try:
    tokenizer = AutoTokenizer.from_pretrained(TEXT_TO_TEXT_MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(TEXT_TO_TEXT_MODEL_NAME)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")


def perform_text_to_text_translation(text: str, src_lang: str, tgt_lang: str) -> str:
    try:
        tokenizer.src_lang = src_lang
        inputs = tokenizer(text, return_tensors = "pt")

        forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_lang)
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=100
        )
        
        result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Translation error: {str(e)}")
    