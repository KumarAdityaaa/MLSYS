from models.ollama import get_coding_model
from utils.code_executor import execute_code

llm = get_coding_model()

DATA_PATH = "data.csv"


# =========================
# MAIN DATA AGENT
# =========================
def data_agent(query: str):
    prompt = f"""
You are a data analyst.

The dataset is stored in 'data.csv'.

Task:
{query}

Write Python code using:
- pandas
- matplotlib
- seaborn

Rules:
- Always load dataset using: pd.read_csv('data.csv')
- If plotting → save image as 'output.png'
- Print useful outputs
- ONLY return executable Python code
"""

    # 🔥 Generate code
    code = llm.invoke(prompt)

    # 🧼 Clean markdown (VERY IMPORTANT)
    code = code.replace("```python", "").replace("```", "").strip()

    print("\n[DATA AGENT CODE]\n", code)

    # ⚡ Execute code
    result = execute_code(code)

    return {
        "code": code,
        "output": result.get("output"),
        "image": result.get("image"),
    }


# =========================
# AUTO INSIGHTS
# =========================
def data_insights():
    import pandas as pd

    df = pd.read_csv(DATA_PATH)

    summary = df.describe().to_string()

    prompt = f"""
    You are a data analyst.

    Dataset: data.csv

    Task:
    {query}

    STRICT RULES:
    - ONLY return Python code
    - NO explanations
    - NO markdown
    - MUST use pandas

    If plotting:
    - use matplotlib/seaborn
    - save as output.png

    Your response MUST be valid Python code.
    """

    return llm.invoke(prompt)