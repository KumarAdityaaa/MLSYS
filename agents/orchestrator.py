from models.ollama import get_reasoning_model
from agents.data_agent import data_agent
from agents.research_agent import query_research
from agents.coding_agent import coding_agent
from memory.conversation_memory import get_memory, add_to_memory

llm = get_reasoning_model()

AGENT_KEYWORDS = {
    "data": ["dataset", "csv", "plot", "visualize", "analyse", "analyze", "pandas", "graph", "chart"],
    "research": ["explain", "what is", "how does", "paper", "concept", "theory", "definition"],
    "code": ["run", "execute", "implement", "train", "build", "code", "model", "script"],
}


# =========================
# DECIDE AGENT (rule-based fallback)
# =========================
def decide_agent(query: str) -> str:
    query_lower = query.lower()

    for agent, keywords in AGENT_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            return agent

    # If no keyword match, ask the LLM
    prompt = f"""
You are an AI orchestrator.

Decide which agent to use for this query.

Available agents:
- data → for dataset analysis, pandas, plots
- research → for papers, PDFs, explanations
- code → for programming, ML models, execution

Query:
{query}

Reply with ONLY one word: data, research, or code
"""
    decision = llm.invoke(prompt).strip().lower()

    # Sanitize LLM response
    for agent in ["data", "research", "code"]:
        if agent in decision:
            return agent

    # Default fallback
    return "research"


# =========================
# ORCHESTRATOR
# =========================
def orchestrator(query: str):
    context = get_memory()

    agent_name = decide_agent(query)

    print(f"\n[ORCHESTRATOR] Routing to: {agent_name}")

    try:
        if agent_name == "data":
            result = data_agent(query)

        elif agent_name == "research":
            result = query_research(query)

        else:
            result = coding_agent(query)

    except Exception as e:
        print(f"[ORCHESTRATOR ERROR] {e}")
        result = {"output": f"Agent failed with error: {str(e)}", "agent": agent_name}

    # Normalize result
    if isinstance(result, dict):
        output = result.get("output") or result.get("response") or str(result)
    else:
        output = str(result)

    # Save to memory
    add_to_memory(query, output)

    print(f"\n[FINAL OUTPUT]\n{output}")

    return {
        "output": output,
        "agent": agent_name
    }