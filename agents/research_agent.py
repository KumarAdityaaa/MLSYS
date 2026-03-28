from models.ollama import get_reasoning_model
from memory.vector_store import get_vector_store

llm = get_reasoning_model()
db = get_vector_store()

def query_research(query: str):
    docs = db.similarity_search(query, k=3)
    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
You are an ML expert.

Use the following context to answer the question.
If the context is not relevant, answer from your own knowledge.

Context:
{context}

Question:
{query}

Answer clearly and directly.
NO asking for clarification.
NO vague responses.
Explain in simple terms.
"""

    return llm.invoke(prompt)