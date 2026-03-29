from app.constants.constants import *
import requests
from google import genai

import time

# Global tracker for the time of the last API call
last_api_call_time = 0.0

def enforce_rate_limit():
    global last_api_call_time
    elapsed = time.time() - last_api_call_time
    
    # If less than 4 seconds have passed, sleep for the difference
    if elapsed < 4.0: 
        time.sleep(4.0 - elapsed)
        
    last_api_call_time = time.time()

# The new SDK uses a Client object. 
# It will automatically look for the GEMINI_API_KEY environment variable if not passed explicitly,
# but passing it directly is good practice for clarity.
client = genai.Client(api_key="")

def gemini_translate_sanskrit_to_hindi(text: str) -> str:
    """Translates Sanskrit to Hindi using the new Google GenAI SDK and Gemini 3.1 Pro."""
    prompt = f"""You are an expert Sanskrit to Hindi translator. Translate the given Sanskrit text into natural, accurate Hindi. 
    Provide ONLY the final Hindi translation without any additional explanations, quotes, or formatting.

    Sanskrit: अलसस्य कुतो विद्या, अविद्यस्य कुतो धनम्। अधनस्य कुतो मित्रम्, अमित्रस्य कुतः सुखम्॥
    Translation: अर्लसी को विद्या कहाँ? अनपढ़ को धन कहाँ? धनहीन को मित्र कहाँ? और मित्रहीन को सुख कहाँ?

    Sanskrit: मनोजवं मारुततुल्यवेगं जितेन्द्रियं बुद्धिमतां वरिष्ठम्। वातात्मजं वानरयूथमुख्यं श्रीरामदूतं शरणं प्रपद्ये॥
    Translation: मन की गति और पवन के समान वेग वाले, बुद्धिमानों में श्रेष्ठ, पवनपुत्र श्री रामदूत हनुमान की मैं शरण लेता हूँ।

    Now, translate the following:
    Sanskrit: {text}
    Translation:"""

    try:
        enforce_rate_limit()
        # The new syntax passes the model name directly into the method
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Sanskrit to Hindi translation failed: {str(e)}")


def gemini_translate_hindi_to_sanskrit(text: str) -> str:
    """Translates Hindi to Sanskrit using the new Google GenAI SDK and Gemini 3.1 Pro."""
    prompt = f"""You are an expert Hindi to Sanskrit translator. Translate the given Hindi text into accurate, grammatically correct Sanskrit. 
    Provide ONLY the final Sanskrit translation without any additional explanations, quotes, or formatting.

    Hindi: अर्लसी को विद्या कहाँ? अनपढ़ को धन कहाँ? धनहीन को मित्र कहाँ? और मित्रहीन को सुख कहाँ?
    Translation: अलसस्य कुतो विद्या, अविद्यस्य कुतो धनम्। अधनस्य कुतो मित्रम्, अमित्रस्य कुतः सुखम्॥

    Hindi: मन की गति और पवन के समान वेग वाले, बुद्धिमानों में श्रेष्ठ, पवनपुत्र श्री रामदूत हनुमान की मैं शरण लेता हूँ।
    Translation: मनोजवं मारुततुल्यवेगं जितेन्द्रियं बुद्धिमतां वरिष्ठम्। वातात्मजं वानरयूथमुख्यं श्रीरामदूतं शरणं प्रपद्ये॥

    Now, translate the following:
    Hindi: {text}
    Translation:"""

    try:
        enforce_rate_limit()
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Hindi to Sanskrit translation failed: {str(e)}")


def get_bhashini_config(source_lang: str, target_lang: str):
    try:
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang
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
        print(f"Error fetching Bhashini Config: {e}")
        raise e


def bhashini_translate(text: str, source_lang: str, target_lang: str) -> str:
    if not text:
        return ""

    try:
        config = get_bhashini_config(source_lang, target_lang)

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang
                        },
                        "serviceId": config["service_id"]
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

        response = requests.post(
            config["callback_url"], 
            json=payload, 
            headers=config["auth_headers"]
        )
        response.raise_for_status()
        result = response.json()

        translated_text = result["pipelineResponse"][0]["output"][0]["target"]
        return translated_text

    except Exception as e:
        print(f"Bhashini Translation Failed: {e}")
        raise e
    