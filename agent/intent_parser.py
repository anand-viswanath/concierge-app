import json
import dateparser

def parse_intent(raw_json: str) -> dict:
    try:
        parsed = json.loads(raw_json)

        # Normalize the date if present
        if "date" in parsed:
            parsed_date = dateparser.parse(parsed["date"])
            if parsed_date:
                parsed["date"] = parsed_date.strftime("%Y-%m-%d")
            else:
                print("⚠️ Unable to parse date, keeping original.")

        # Validate minimum structure
        if "intent" not in parsed:
            raise ValueError("Missing 'intent' in parsed result.")

        return parsed

    except json.JSONDecodeError:
        print("❌ Failed to parse model output as JSON.")
        return {}
    except Exception as e:
        print(f"❌ Parsing error: {e}")
        return {}