from fastapi import APIRouter
from memory.conversation_memory import clear_memory

router = APIRouter()

@router.post("/clear-memory")
def clear_memory_route():
    clear_memory()
    return {"message": "Memory cleared"}