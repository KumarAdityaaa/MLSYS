from models.ollama import get_reasoning_model
from agents.data_agent import data_agent
from agents.research_agent import query_research
from agents.coding_agent import coding_agent
from memory.conversation_memory import get_memory, add_to_memory
llm = get_reasoning_model()


def decide_agent(query: str):
    prompt = f"""
    You are an AI orchestrator.

    Decide which agent to use for this query:

    Available agents:
    - data → for dataset analysis, pandas, plots
    - research → for papers, PDFs, explanations
    - code → for programming, ML models, execution

    Query:
    {query}

    Output ONLY one word:
    data / research / code
    """

    decision = llm.invoke(prompt).strip().lower()

    return decision


def orchestrator(query: str):
    context = get_memory()

    planning_prompt = f"""
    You are an AI orchestrator.

    If question is:
    - conceptual → use research ONLY
    - coding → use code ONLY
    - dataset → use data ONLY

    ONLY use multiple agents if absolutely required.

    Query:
    {query}

    Output:

    step1: agent - task
    """

    plan = llm.invoke(planning_prompt)

    print("\n[PLAN]\n", plan)

    steps = plan.split("\n")

    final_output = ""

    for step in steps:
        if ":" not in step:
            continue

        try:
            _, rest = step.split(":")
            agent_name, task = rest.split("-", 1)

            agent_name = agent_name.strip()
            task = task.strip()

            print(f"[STEP] {agent_name} → {task}")

            if agent_name == "data":
                result = data_agent(task)

            elif agent_name == "research":
                result = query_research(task)

            else:
                result = coding_agent(task)

            final_output += f"\n\n[{agent_name.upper()} RESULT]\n{result}"

        except Exception as e:
            print("Error:", e)

    # 🧠 SAVE MEMORY
    add_to_memory(query, final_output)
    print("\n[FINAL OUTPUT]\n", final_output)

    return {
        "output": final_output,
        "agent": "multi-agent"
    }