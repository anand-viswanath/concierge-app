from typing import Dict, Any
from importlib import import_module
from rag_tool import rag_tool
from automation.search import wiki_lookup, arxiv_lookup, ddg_search

def _try_import(modname, func):
    try:
        mod = import_module(modname)
        return getattr(mod, func)
    except Exception:
        return None

book_flight = _try_import("automation.book_flight", "book_flight")
book_restaurant = _try_import("automation.book_restaurant", "book_restaurant")
get_weather = _try_import("automation.get_weather", "get_weather")
tell_joke = _try_import("automation.tell_joke", "tell_joke")

def simple_route(text: str) -> Dict[str, Any]:
    tl = text.lower().strip()
    if tl.startswith("wiki") or tl.startswith("wikipedia"):
        return {"intent":"wiki_lookup"}
    if "duckduckgo" in tl or tl.startswith("ddg") or "search" in tl:
        return {"intent":"ddg_search"}
    if "arxiv" in tl:
        return {"intent":"arxiv_lookup"}
    if tl.startswith("book flight") and book_flight:
        return {"intent": "book_flight"}
    if tl.startswith("book restaurant") and book_restaurant:
        return {"intent": "book_restaurant"}
    if "weather" in tl and get_weather:
        return {"intent": "get_weather"}
    if "joke" in tl and tell_joke:
        return {"intent": "tell_joke"}
    if not text:
        return {"intent": "none", "answer": "", "sources": []}
    ans = rag_tool(text)
    return {"intent": "answer_query", **ans}
