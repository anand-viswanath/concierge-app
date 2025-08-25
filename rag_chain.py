from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from llm_factory import get_llm

VS_PATH = "vectorstore"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

SYSTEM = "Answer strictly from the provided context. If unsure, say you don't know. Be concise and cite short source labels."
PROMPT = ChatPromptTemplate.from_template(
    "Context:\n{context}\n\nQuestion: {input}\n\nReturn a brief answer with citations."
)

def _load_vs():
    emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return FAISS.load_local(VS_PATH, emb, allow_dangerous_deserialization=True)

def build_rag_chain():
    llm = get_llm()
    vs = _load_vs()
    retriever = vs.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 8, "score_threshold": 0.2}
    )
    doc_chain = create_stuff_documents_chain(llm, PROMPT)
    return create_retrieval_chain(retriever, doc_chain)
