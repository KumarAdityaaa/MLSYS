from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def get_vector_store():
    embeddings = HuggingFaceEmbeddings()
    
    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    return db