from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

def wiki_lookup(params: dict):
    """
    params = {"query":"LangChain"}
    """
    q = params.get("query")
    if not q:
        return {"status":"error","message":"Missing 'query' param"}
    res = wiki.run(q)
    return {"status":"ok","answer":res}
    
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())

def arxiv_lookup(params: dict):
    """
    params = {"query":"transformer model"}
    """
    q = params.get("query")
    if not q:
        return {"status":"error","message":"Missing 'query' param"}
    res = arxiv.run(q)
    return {"status":"ok","answer":res}

try:
    from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
    _ddg = DuckDuckGoSearchAPIWrapper()
except ImportError:
    _ddg = None
    print("DuckDuckGoSearchAPIWrapper requires the 'ddgs' package. Install with: pip install -U ddgs")

def ddg_search(params: dict):
    q = params.get("query")
    if not q:
        return {"status":"error","message":"Missing 'query'."}
    hits = _ddg.results(q, max_results=int(params.get("k", 5)))
    results = [
        {"title": h.get("title",""), "link": h.get("link",""), "snippet": h.get("snippet","")}
        for h in hits
    ]
    return {"status":"ok","results":results}

