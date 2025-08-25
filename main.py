from router import simple_route
import time, json, os
from dotenv import load_dotenv
load_dotenv()
LOG_PATH = os.getenv("RAG_LOG", "rag_logs.jsonl")
def log_event(kind: str, user_text: str, payload: dict):
    try:
        rec = {
            "t": time.time(),
            "mode": kind,              # 'rag' or 'tool:<name>'
            "q": user_text,
            "answer": payload.get("answer") if isinstance(payload, dict) else None,
            "sources": payload.get("sources", []) if isinstance(payload, dict) else [],
        }
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception:
        pass

def dispatch(user_text: str):
    result = simple_route(user_text)
    it = result.get("intent")

    if it == "book_flight":
        from automation.book_flight import book_flight
        res = book_flight({"from_city":"SYD","to_city":"MEL","date":"Friday"})
        print("\n[tool] book_flight →", res)
        log_event("tool:book_flight", user_text, res if isinstance(res, dict) else {})
        return res
    if it == "book_restaurant":
        from automation.book_restaurant import book_restaurant
        res = book_restaurant({"city":"Sydney","cuisine":"Italian","date":"Friday","time":"19:00"})
        print("\n[tool] book_restaurant →", res)
        log_event("tool:book_restaurant", user_text, res if isinstance(res, dict) else {})
        return res
    if it == "get_weather":
        from automation.get_weather import get_weather
        res = get_weather({"city":"Sydney","date":"today"})
        print("\n[tool] get_weather →", res)
        log_event("tool:get_weather", user_text, res if isinstance(res, dict) else {})
        return res
    if it == "tell_joke":
        from automation.tell_joke import tell_joke
        res = tell_joke({})
        print("\n[tool] tell_joke →", res)
        log_event("tool:tell_joke", user_text, res if isinstance(res, dict) else {})
        return res
    from automation.search import wiki_lookup, arxiv_lookup, ddg_search
    if it == "wiki_lookup":
        res = wiki_lookup({"query": user_text.replace("wiki","",1).strip()})
        print("\n[tool] wiki_lookup →", res)
        return res
    if it == "ddg_search":
        res = ddg_search({"query": user_text})
        if res.get("status") == "ok":
            print("\n[DuckDuckGo Results]")
            for i, r in enumerate(res.get("results", []), 1):
                title = r.get("title", "").strip()
                link = r.get("link", "").strip()
                snippet = r.get("snippet", "").strip()
                print(f"{i}. {title}\n   {link}\n   {snippet}\n")
             print("\n[tool] ddg_search →", res)
        else:
            print("\n[ddg_search error]", res.get("message"))
        return res
        return res
    if it == "arxiv_lookup":
        res = arxiv_lookup({"query": user_text})
        print("\n[tool] arxiv_lookup →", res)
        return res    
    if it == "answer_query":
        print("\n--- Answer ---")
        print(result.get("answer",""))
        src = result.get("sources", [])
        if src:
            print("\nSources:", "; ".join(src))
        log_event("rag", user_text, result)
        return result.get("answer","")

    print("No matching intent/tool.")
    return None

if __name__ == "__main__":
    try:
        while True:
            text = input("\nYou: ").strip()
            if not text:
                continue
            if text.lower() in {"exit","quit"}:
                break
            dispatch(text)
    except KeyboardInterrupt:
        pass