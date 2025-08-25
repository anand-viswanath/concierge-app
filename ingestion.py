import sys
from pathlib import Path
from typing import List
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_DIR = Path("data")
VS_DIR = Path("vectorstore")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_local_docs() -> list:
    docs = []
    if DATA_DIR.exists():
        docs += DirectoryLoader(str(DATA_DIR), glob="**/*.pdf", loader_cls=PyPDFLoader).load()
        docs += DirectoryLoader(str(DATA_DIR), glob="**/*.md").load()
        docs += DirectoryLoader(str(DATA_DIR), glob="**/*.txt", loader_cls=TextLoader).load()
    return docs

def load_web_docs(urls: List[str]) -> list:
    docs = []
    for u in urls:
        try:
            docs += WebBaseLoader(u).load()
        except Exception as e:
            print(f"[WARN] Skipping URL {u}: {e}")
    return docs

def build_index(urls: List[str]):
    print("Loading documents...")
    docs = load_local_docs() + load_web_docs(urls)
    if not docs:
        print("No documents found in ./data or from URLs. Nothing to index.")
        return
    print(f"Loaded {len(docs)} docs. Splitting...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks. Embedding with {EMBED_MODEL}...")
    emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL, encode_kwargs={"normalize_embeddings": True})
    vs = FAISS.from_documents(chunks, emb)
    VS_DIR.mkdir(exist_ok=True)
    vs.save_local(str(VS_DIR))
    print(f"Saved FAISS index to {VS_DIR}/")

if __name__ == "__main__":
    urls = sys.argv[1:]
    build_index(urls)
