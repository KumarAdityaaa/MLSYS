from fastapi import APIRouter
from memory.conversation_memory import memory

router = APIRouter()

@router.post("/clear-memory")
def clear_memory():
    memory.clear()
    return {"message": "Memory cleared"}