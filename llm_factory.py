import os
import socket
from typing import Optional
try:
    from langchain_ollama import ChatOllama
except Exception:
    ChatOllama = None
try:
    from langchain_groq import ChatGroq
except Exception:
    ChatGroq = None

from dotenv import load_dotenv
load_dotenv()

def _port_open(host: str="127.0.0.1", port: int=11434, timeout: float=0.2) -> bool:
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port)); s.close(); return True
    except Exception:
        return False

def get_llm(model: Optional[str]=None, temperature: float=0.2):
    # model = model or os.getenv("OLLAMA_MODEL", "llama2")
    # if ChatOllama and _port_open():
    #     return ChatOllama(model=model, temperature=temperature)
    groq_key = os.getenv("GROQ_API_KEY")
    if ChatGroq and groq_key:
        return ChatGroq(model_name=os.getenv("GROQ_MODEL","llama-3.1-8b-instant"),
                        groq_api_key=groq_key, temperature=temperature)
    raise RuntimeError("No LLM available. Start Ollama (11434) or set GROQ_API_KEY.")
