def book_restaurant(data):
    required_keys = ["city", "cuisine", "date", "time"]
    filtered = {k: v for k, v in data.items() if k in required_keys}
    print(f"🍽️ Reserving a {filtered['cuisine']} restaurant in {filtered['city']} at {filtered['time']} on {filtered['date']}")