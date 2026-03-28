from models.ollama import get_coding_model
from utils.code_executor import execute_code
from experiments.tracker import save_experiment
from utils.metric_extractor import extract_metrics
from experiments.tracker import save_experiment
llm = get_coding_model()

def coding_agent(query: str):
    prompt = f"""
    You are a Python ML engineer.

    Task:
    {query}

    STRICT RULES:
    - ONLY return executable Python code
    - NO explanations
    - NO text outside code
    - NO markdown (no ```)

    If unsure, still return best possible code.

    Use:
    - sklearn / pandas / numpy
    - Print results

    IMPORTANT:
    Your response MUST start with valid Python code.
    """

    code = llm.invoke(prompt)

    # ❌ REMOVE TEXT BEFORE CODE
    lines = code.split("\n")

    # find first code-like line
    for i, line in enumerate(lines):
        if "import" in line or "from" in line:
            code = "\n".join(lines[i:])
            break

    result = execute_code(code)

    output = result.get("output", "")

    # 🧠 Extract metrics
    metrics = extract_metrics(output)

    if not metrics:
        metrics = {"note": "No metrics detected"}

    # 💾 Save experiment
    save_experiment("auto-run", metrics)

    return result