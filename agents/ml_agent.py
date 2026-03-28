from models.ollama import get_reasoning_model, get_coding_model
from utils.code_executor import execute_code

reasoning_llm = get_reasoning_model()
coding_llm = get_coding_model()

def ml_agent(query: str):

    if any(word in query for word in ["run", "execute", "dataset", "plot", "train"]):
        
        code_prompt = f"""
        Write Python code for the following task:

        {query}

        IMPORTANT:
        - Return ONLY raw Python code
        - No markdown
        - Include print statements for outputs
        - If plotting, use matplotlib
        """

        code = coding_llm.invoke(code_prompt)

        result = execute_code(code)

        return result

    elif "code" in query or "implement" in query:
        return coding_llm.invoke(query)

    else:
        return reasoning_llm.invoke(query)