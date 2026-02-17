from app.constants.constants import *
import requests
import base64


def get_bhashini_asr_config(source_lang: str):
    try:
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang
                        }
                    }
                }
            ],
            "pipelineRequestConfig": {
                "pipelineId": PIPELINE_ID
            }
        }

        headers = {
            "userID": USER_ID,
            "ulcaApiKey": ULCA_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(CONFIG_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        service_id = data["pipelineResponseConfig"][0]["config"][0]["serviceId"]

        inference_connect = data["pipelineInferenceAPIEndPoint"]
        callback_url = inference_connect["callbackUrl"]
        
        auth_header_name = inference_connect["inferenceApiKey"]["name"]
        auth_header_value = inference_connect["inferenceApiKey"]["value"]

        return {
            "service_id": service_id,
            "callback_url": callback_url,
            "auth_headers": {
                auth_header_name: auth_header_value,
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        print(f"Error fetching Bhashini ASR Config: {e}")
        raise e


def bhashini_asr(audio_bytes: bytes, source_lang: str, audio_format: str = "flac") -> str:
    if not audio_bytes:
        return ""

    try:
        config = get_bhashini_asr_config(source_lang)

        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang
                        },
                        "serviceId": config["service_id"],
                        "audioFormat": audio_format,
                        "samplingRate": 16000
                    }
                }
            ],
            "inputData": {
                "audio": [
                    {
                        "audioContent": audio_b64
                    }
                ]
            }
        }

        response = requests.post(
            config["callback_url"], 
            json=payload, 
            headers=config["auth_headers"]
        )
        response.raise_for_status()
        result = response.json()

        transcribed_text = result["pipelineResponse"][0]["output"][0]["source"]
        return transcribed_text

    except Exception as e:
        print(f"Bhashini ASR Failed: {e}")
        raise e