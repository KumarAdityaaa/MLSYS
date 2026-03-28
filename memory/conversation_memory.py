memory = []

def add_to_memory(query, response):
    memory.append({
        "query": query,
        "response": str(response)
    })

    # keep last 5 interactions only (lightweight)
    if len(memory) > 5:
        memory.pop(0)


def get_memory():
    context = ""

    for m in memory:
        context += f"""
User: {m['query']}
AI: {m['response']}
"""

    return context