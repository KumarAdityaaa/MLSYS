import json
import os

MEMORY_FILE = "memory.json"
MAX_MEMORY = 5


# =========================
# LOAD MEMORY FROM DISK
# =========================
def _load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


# =========================
# SAVE MEMORY TO DISK
# =========================
def _save_memory(memory: list):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        print(f"[MEMORY] Could not save memory: {e}")


# =========================
# ADD TO MEMORY
# =========================
def add_to_memory(query: str, response: str):
    memory = _load_memory()

    memory.append({
        "query": query,
        "response": str(response)
    })

    # Keep last MAX_MEMORY interactions only
    if len(memory) > MAX_MEMORY:
        memory = memory[-MAX_MEMORY:]

    _save_memory(memory)


# =========================
# GET MEMORY
# =========================
def get_memory():
    memory = _load_memory()
    context = ""

    for m in memory:
        context += f"""
User: {m['query']}
AI: {m['response']}
"""

    return context


# =========================
# CLEAR MEMORY
# =========================
def clear_memory():
    _save_memory([])