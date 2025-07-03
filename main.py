from llama_concierge import run_agent

if __name__ == "__main__":
    user_input = input(" Enter your request: ")
    output = run_agent(user_input)
    print("\n Final Output:", output)