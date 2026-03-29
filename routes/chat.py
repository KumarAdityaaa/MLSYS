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

    if isinstance(result, dict):
        # Handle debug agent response
        if result.get("debugged"):
            explanation = result.get("explanation", "Code had an error — here is the fix.")
            fixed_code = result.get("fixed_code", "")
            output = result.get("output", "")
            error = result.get("error", "")

            # Build a clean readable response
            response = f"{explanation}\n\n"
            if fixed_code:
                response += f"Fixed code:\n{fixed_code}\n\n"
            if output:
                response += f"Output:\n{output}"
            if error:
                response += f"\nStill has error:\n{error}"

            return {
                "response": response.strip(),
                "agent": "debug",
                "debugged": True
            }

        # Normal response
        response = result.get("output") or result.get("response") or str(result)
        agent = result.get("agent", "orchestrator")
    else:
        response = str(result)
        agent = "orchestrator"

    return {
        "response": response,
        "agent": agent,
        "debugged": False
    }