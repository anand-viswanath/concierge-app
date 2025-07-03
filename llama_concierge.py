from agent.llm_client import build_prompt, query_llama
from agent.intent_parser import parse_intent

# import functions/API calls
from automation.book_flight import book_flight
from automation.book_restaurant import book_restaurant
from automation.tell_joke import tell_joke
from automation.get_weather import get_weather

def run_agent(user_input: str) -> dict:
    prompt = build_prompt(user_input)
    print("Prompt to LLaMA:\n", prompt)

    raw_output = query_llama(prompt)
    print("Raw Output from LLaMA:\n", raw_output)

    structured_data = parse_intent(raw_output)
    print("Parsed Intent:\n", structured_data)

    #Handle intent to respective function
    intent = structured_data.get("intent")
    if intent ==  "book_flight":
        book_flight(structured_data)
    elif intent == "book_restaurant":
        book_restaurant(structured_data)
    elif intent == "tell_joke":
        tell_joke(structured_data)
    elif intent == "get_weather":
        get_weather(structured_data)
    else:
        print(f"No function found for intent: {intent}")

    return structured_data