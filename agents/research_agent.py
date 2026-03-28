from models.ollama import get_reasoning_model
from memory.vector_store import get_vector_store

llm = get_reasoning_model()
db = get_vector_store()

def query_research(query: str):
    docs = db.similarity_search(query, k=3)
    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
    You are an ML expert.

    Answer the question clearly and directly.

    NO asking for clarification.
    NO vague responses.

    Explain in simple terms.

    Question:
    {query}
    """

    return llm.invoke(prompt)