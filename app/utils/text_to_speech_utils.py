import requests
import base64
from app.constants.constants import *

def bhashini_tts(text: str, language: str) -> bytes:
    if not text:
        return None

    try:
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {
                            "sourceLanguage": language
                        },
                        "serviceId": TTS_SERVICE_ID,
                        "gender": "male",
                        "samplingRate": 16000
                    }
                }
            ],
            "inputData": {
                "input": [
                    {
                        "source": text
                    }
                ]
            }
        }

        headers = {
            "Authorization": INFERENCE_API_KEY, 
            "Content-Type": "application/json"
        }

        response = requests.post(BHASHINI_INFERENCE_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        audio_content_base64 = data["pipelineResponse"][0]["audio"][0]["audioContent"]
        
        if audio_content_base64:
            return base64.b64decode(audio_content_base64)
        return None

    except Exception as e:
        print(f"Bhashini TTS Failed: {e}")
        raise e