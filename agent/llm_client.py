import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def build_prompt(user_input: str) -> str:
    SCHEMAS = {
        "book_flight": {
            "from_city": "string",
            "to_city": "string",
            "date": "string"
        },
        "book_restaurant": {
            "city": "string",
            "cuisine": "string",
            "date": "string",
            "time": "string"
        },
        "get_weather": {
            "city": "string",
            "date": "string"
        },
        "tell_joke": {}
    }

    prompt = (
        "You are an AI that extracts a single JSON object matching user intent.\n"
        "Only respond with one valid JSON object and nothing else.\n\n"
    )

    for intent, fields in SCHEMAS.items():
        prompt += f"Intent: {intent}\n{{\n"
        prompt += f'  "intent": "{intent}"'
        for field in fields:
            prompt += f',\n  "{field}": "string"'
        prompt += "\n}\n\n"

    prompt += f"User: {user_input}\n\nJSON:"
    return prompt

def query_llama(prompt: str, model: str = "llama2") -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "stop": ["\n\n"]
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json["response"].strip()
    
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return ""
    except KeyError:
        print("❌ Invalid response format from LLaMA")
        return ""