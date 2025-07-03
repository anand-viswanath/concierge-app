import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def build_prompt(user_input: str) -> str:
    examples = [
        {
            "input": "Book a flight from Delhi to Mumbai next Monday",
            "output": {
                "intent": "book_flight",
                "from_city": "Delhi",
                "to_city": "Mumbai",
                "date": "next Monday"
            }
        },
        {
            "input": "Reserve a restaurant in Sydney for 7pm Saturday — Japanese cuisine",
            "output": {
                "intent": "book_restaurant",
                "city": "Sydney",
                "time": "7pm",
                "date": "Saturday",
                "cuisine": "Japanese"
            }
        }
    ]
    
    prompt = "Extract structured JSON intent from user input. Use these examples:\n\n"
    for ex in examples:
        prompt += f"User: {ex['input']}\n"
        prompt += f"JSON: {json.dumps(ex['output'], indent=2)}\n\n"

    prompt += f"User: {user_input}\nJSON:"
    return prompt

def query_llama(prompt: str, model: str = "llama2") -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
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