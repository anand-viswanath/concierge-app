import requests
import dateparser

def normalize_date(raw_date):
    # Clean known modifiers that confuse parsing
    cleaned = raw_date.lower().replace("this ", "").replace("on ", "").strip()
    parsed = dateparser.parse(cleaned, settings={"PREFER_DATES_FROM": "future"})
    if parsed:
        return parsed.strftime("%Y-%m-%d")
    return raw_date  # fallback

def extract_flight_info(user_input):
    examples = """
You are a smart assistant that extracts booking intent and details as structured JSON.
Respond ONLY with JSON. No explanation. No markdown.

Examples:

Input: "Book a flight from Delhi to Mumbai next Monday"
Output:
{
  "intent": "book_flight",
  "from_city": "Delhi",
  "to_city": "Mumbai",
  "date": "next Monday"
}

Input: "I need to fly from Sydney to Perth tomorrow"
Output:
{
  "intent": "book_flight",
  "from_city": "Sydney",
  "to_city": "Perth",
  "date": "tomorrow"
}

Input: "I want to go to Melbourne coming Friday"
Output:
{
  "intent": "book_flight",
  "from_city": "",
  "to_city": "Melbourne",
  "date": "coming Friday"
}

Input: "Book a table at a Mexican restaurant in Sydney at 7pm next Friday"
Output:
{
  "intent": "book_restaurant",
  "cuisine": "Mexican",
  "city": "Sydney",
  "time": "7pm",
  "date": "next Friday"
}

Input: "Reserve an Italian restaurant in Melbourne for 8pm tomorrow"
Output:
{
  "intent": "book_restaurant",
  "cuisine": "Italian",
  "city": "Melbourne",
  "time": "8pm",
  "date": "tomorrow"
}
"""

    prompt = examples + f'\n\nInput: "{user_input}"\nOutput:\n'

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    })

    json_text = response.json().get("response", "")
    print("🧠 Raw Output from LLaMA:\n", json_text)

    # Optional: Try to extract the date string and normalize it
    import json
    try:
        # Extract the JSON substring by taking from the first "{" to the last "}"
        start = json_text.find('{')
        end = json_text.rfind('}') + 1
        json_substring = json_text[start:end]
        parsed_json = json.loads(json_substring)
        raw_date = parsed_json.get("date", "")
        parsed_json["date"] = normalize_date(raw_date)
        return parsed_json
    except Exception as e:
        return {"error": "Failed to parse LLaMA output", "details": str(e)}
    

# Try it
# print(extract_flight_info("Book me a flight from Delhi to Mumbai next Monday"))#
print(extract_flight_info(input("🗣️ Enter your request: ")))