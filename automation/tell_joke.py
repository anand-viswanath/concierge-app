import requests

def tell_joke(data=None):
    print("🎭 Fetching a joke...")

    # 1. Prefer joke from LLM if available
    if data and "joke" in data:
        print("😂 Joke (from model):", data["joke"])
        return

    # 2. Fallback to joke API
    try:
        response = requests.get(
            "https://icanhazdadjoke.com/",
            headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            joke = response.json().get("joke", "No joke found.")
            print("😂 Joke (from API):", joke)
        else:
            print("⚠️ Failed to fetch joke from API.")
    except Exception as e:
        print(f"❌ Error fetching joke from API: {e}")