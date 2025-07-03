import json
import dateparser
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