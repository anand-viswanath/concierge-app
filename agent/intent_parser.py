import json
import dateparser
import re
from datetime import datetime

# Expected fields and their types for each intent
INTENT_SCHEMAS = {
    "book_flight": {
        "from_city": str,
        "to_city": str,
        "date": str
    },
    "book_restaurant": {
        "city": str,
        "cuisine": str,
        "date": str,
        "time": str
    },
    "get_weather": {
        "city": str,
        "date": str
    },
    "tell_joke": {
        "joke": str
    }
}

def normalize_date(date_str: str) -> str:
    parsed = dateparser.parse(date_str, settings={"RELATIVE_BASE": datetime.now()})
    if parsed:
        return parsed.strftime("%d-%m-%Y")
    return date_str

def is_placeholder(value):
    return isinstance(value, str) and re.fullmatch(r"(string|none|null)", value.strip(), re.IGNORECASE)

def validate_intent(intent_data):
    intent = intent_data.get("intent")

    if intent == "book_flight":
        if not intent_data.get("from_city") or not intent_data.get("to_city"):
            return False
        if intent_data["from_city"].lower() == intent_data["to_city"].lower():
            return False
        if is_placeholder(intent_data["from_city"]) or is_placeholder(intent_data["to_city"]):
            return False

    elif intent == "book_restaurant":
        if not intent_data.get("city") or not intent_data.get("cuisine"):
            return False
        if intent_data["city"].lower() == intent_data["cuisine"].lower():
            return False
        if is_placeholder(intent_data["city"]) or is_placeholder(intent_data["cuisine"]):
            return False

    elif intent == "get_weather":
        if not intent_data.get("city"):
            return False
        if is_placeholder(intent_data["city"]):
            return False

    elif intent == "tell_joke":
        return True

    return True

def parse_intent(raw_json: str) -> dict:
    try:
        parsed = json.loads(raw_json)

        intent = parsed.get("intent", None)
        if not intent:
            print("⚠️ No 'intent' found. Returning fallback intent.")
            return {
                "intent": "unknown",
                "raw_input": raw_json
            }

        expected_fields = INTENT_SCHEMAS.get(intent, {})
        clean = {"intent": intent}

        for field, expected_type in expected_fields.items():
            value = parsed.get(field, None)

            # Normalize and validate date
            if field == "date" and isinstance(value, str):
                value = normalize_date(value)

            # Type check
            if isinstance(value, expected_type):
                clean[field] = value
            else:
                clean[field] = None  # invalid or missing field
        
        if not validate_intent(clean):
            print("⚠️ Invalid intent payload — falling back to unknown.")
            return {
                "intent": "unknown",
                "raw_input": raw_json
            }

        return clean

    except json.JSONDecodeError:
        print("❌ Failed to parse model output as JSON.")
        return {
            "intent": "unknown",
            "raw_input": raw_json
        }
    except Exception as e:
        print(f"❌ Parsing error: {e}")
        return {
            "intent": "unknown",
            "raw_input": raw_json
        }