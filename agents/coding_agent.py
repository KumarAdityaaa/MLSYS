from models.ollama import get_coding_model
from utils.code_executor import execute_code
from experiments.tracker import save_experiment
from utils.metric_extractor import extract_metrics

llm = get_coding_model()


def clean_llm_code(code: str) -> str:
    # Remove markdown
    code = code.replace("```python", "").replace("```", "")

    # Find the first real code line
    lines = code.split("\n")
    start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if any(stripped.startswith(kw) for kw in [
            "import", "from", "def", "class", "print",
            "if", "for", "while", "try", "#", "pd.", "np.", "plt."
        ]):
            start = i
            break

    # Cut trailing explanation lines
    code_lines = lines[start:]
    end = len(code_lines)
    for i in range(len(code_lines) - 1, -1, -1):
        stripped = code_lines[i].strip()
        if stripped and not stripped.startswith("The ") and not stripped.startswith("Note") and not stripped.startswith("This ") and not stripped.startswith("Please "):
            end = i + 1
            break

    cleaned = "\n".join(code_lines[:end]).strip()

    # If the model wrapped everything in try/except, unwrap it
    if cleaned.startswith("try:") or "sys.tracebacklimit" in cleaned:
        unwrapped = []
        for line in cleaned.split("\n"):
            if line.strip().startswith((
                        "try:", "except", "sys.tracebacklimit",
                        "exc_type", "exc_obj", "exc_tb",
                        "f.write", "f.close", "f = open"
                    )) or "/dev/null" in line or "sys.stdout" in line or "sys.stderr" in line:
                        continue
            # Remove one level of indentation (was inside try block)
            if line.startswith("    "):
                unwrapped.append(line[4:])
            else:
                unwrapped.append(line)
        cleaned = "\n".join(unwrapped).strip()

    return cleaned


def coding_agent(query: str):
    prompt = f"""
You are a Python ML engineer.

Task:
{query}

STRICT RULES:
- ONLY return executable Python code
- NO try/except blocks unless the task specifically requires error handling
- NO explanations, NO text outside code
- NO markdown (no ```)
- NO error suppression of any kind
- Do NOT catch or hide errors
- Do NOT redirect sys.stdout or sys.stderr
- Do NOT use /dev/null or any output suppression

Use:
- sklearn / pandas / numpy
- Print results

Your response MUST be valid Python code only. Start with import statements.
"""

    code = llm.invoke(prompt)
    code = clean_llm_code(code)

    print("\n[CODING AGENT CODE]\n", code)

    result = execute_code(code)
    output = result.get("output", "")

    metrics = extract_metrics(output)
    if not metrics:
        metrics = {"note": "No metrics detected"}

    save_experiment("auto-run", metrics)

    return result
