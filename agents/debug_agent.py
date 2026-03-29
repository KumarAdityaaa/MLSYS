from models.ollama import get_reasoning_model
from utils.code_executor import execute_code

llm = get_reasoning_model()


def debug_agent(code: str, error: str):
    prompt = f"""
You are an expert Python debugger.

The following code has a bug:

CODE:
{code}

ERROR:
{error}

Your job:
1. Identify the bug
2. Return FIXED Python code that actually runs without errors

STRICT RULES:
- Return ONLY raw executable Python code
- First line must be a comment explaining the fix: # Fix: ...
- NO markdown, NO backticks
- The fixed code MUST be complete and actually work
- If a variable is undefined, define it with a sensible value
- If a file is missing, mock the data instead
- Do NOT return the same broken code
"""

    fixed_code = llm.invoke(prompt)
    fixed_code = fixed_code.replace("```python", "").replace("```", "").strip()

    # Extract explanation from first comment line
    lines = fixed_code.split("\n")
    explanation = ""
    for line in lines:
        if line.strip().startswith("# Fix:") or line.strip().startswith("# Explanation:"):
            explanation = line.strip().lstrip("# ").strip()
            break

    result = execute_code(fixed_code)

    return {
        "original_error": error,
        "explanation": explanation,
        "fixed_code": fixed_code,
        "output": result.get("output", ""),
        "image": result.get("image", ""),
        "error": result.get("error", ""),
        "debugged": True
    }