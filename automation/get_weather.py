'''
We are using wttr.in for the weather which gives out weather of today or tomorrow
Can configure later.
url = f"https://wttr.in/{city}?format=j1"
response.json()["weather"][0]  # today
response.json()["weather"][1]  # tomorrow
'''

import requests

def get_weather(data):
    city = data.get("city", "your city") or "your city"
    date = data.get("date", "today")

    print(f"🌦️ Fetching weather for {city}...")

    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"📍 Weather: {response.text}")
            return response
        else:
            print("⚠️ Failed to fetch weather.")
            return "Failed"
    except Exception as e:
        print(f"❌ Error fetching weather: {e}")