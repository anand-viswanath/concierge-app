from agent.llm_client import build_prompt, query_llama
from agent.intent_parser import parse_intent

def run_agent(user_input: str) -> dict:
    prompt = build_prompt(user_input)
    print("Prompt to LLaMA:\n", prompt)

    raw_output = query_llama(prompt)
    print("Raw Output from LLaMA:\n", raw_output)

    structured_data = parse_intent(raw_output)
    print("Parsed Intent:\n", structured_data)

    return structured_data