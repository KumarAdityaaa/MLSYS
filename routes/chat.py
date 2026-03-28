from fastapi import APIRouter
from pydantic import BaseModel
from agents.orchestrator import orchestrator

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
def chat(req: ChatRequest):
    query = req.query

    result = orchestrator(query)

    print("\n[DEBUG RESULT]\n", result)

    # ✅ Normalize response
    if isinstance(result, dict):
        response = result.get("output") or result.get("response") or str(result)
        agent = result.get("agent", "orchestrator")
    else:
        response = str(result)
        agent = "orchestrator"

    return {
        "response": response,
        "agent": agent
    }