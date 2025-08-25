from typing import Dict, Any, List
from rag_chain import build_rag_chain

_RAG = None

def _ensure_chain():
    global _RAG
    if _RAG is None:
        _RAG = build_rag_chain()
    return _RAG

def rag_tool(question: str) -> Dict[str, Any]:
    res = _ensure_chain().invoke({"input": question})
    answer = res.get("answer", "")
    ctx = res.get("context", []) or []
    if not ctx:
        return {
            "answer": ("I don’t have relevant context in my docs for that. "
                    "Add a source to /data and re-run `python ingestion.py`, "
                    "or route this to a web tool."),
            "sources": [],
            "chunks": []
        }
    sources: List[str] = []
    chunks: List[str] = []
    for d in ctx:
        label = d.metadata.get("source") or d.metadata.get("file_path") or d.metadata.get("title") or "doc"
        if label not in sources:
            sources.append(label)
        chunks.append(d.page_content[:500])
    return {"answer": answer, "sources": sources, "chunks": chunks}
