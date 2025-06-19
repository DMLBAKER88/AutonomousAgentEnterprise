import json
import subprocess
from pathlib import Path
from datetime import datetime

ENTERPRISE_ROOT = Path(__file__).parent
MEMORY_DIR = ENTERPRISE_ROOT / "memory"
PROMPT_DIR = ENTERPRISE_ROOT / "prompts"
LOG_DIR = ENTERPRISE_ROOT / "logs"
OLLAMA_MODEL = "qwen2.5:14b"

LOG_DIR.mkdir(exist_ok=True)

def get_recent_task_and_outcome_summaries(n: int = 3) -> str:
    """Return formatted summaries of the last N tasks and outcomes."""
    try:
        with open(MEMORY_DIR / "task_log.json") as f:
            tasks = json.load(f)
    except Exception:
        tasks = []

    try:
        with open(MEMORY_DIR / "outcomes.json") as f:
            outcomes = json.load(f)
    except Exception:
        outcomes = []

    tasks_recent = tasks[-n:] if isinstance(tasks, list) else []
    outcomes_recent = outcomes[-n:] if isinstance(outcomes, list) else []

    summary_lines = ["Tasks:"]
    if tasks_recent:
        summary_lines.extend(f"- {t}" for t in tasks_recent)
    else:
        summary_lines.append("- None")

    summary_lines.append("")
    summary_lines.append("Outcomes:")
    if outcomes_recent:
        summary_lines.extend(f"- {o}" for o in outcomes_recent)
    else:
        summary_lines.append("- None")

    return "\n".join(summary_lines)

def load_goal():
    with open(MEMORY_DIR / "goals.json") as f:
        return json.load(f)["current_goal"]

def call_ollama(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8")

def load_prompt(agent_name: str) -> str:
    with open(PROMPT_DIR / f"{agent_name}_prompt.txt") as f:
        return f.read()

def log_agent_output(agent_name: str, context: str, output: str):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = LOG_DIR / f"{agent_name}_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(f"# Agent: {agent_name}\n")
        f.write(f"## Timestamp: {timestamp}\n\n")
        f.write("### Context\n")
        f.write("```\n" + context.strip() + "\n```\n\n")
        f.write("### Output\n")
        f.write("```\n" + output.strip() + "\n```\n")

def run_agent(agent_name: str, context: str) -> str:
    print(f"\n>>> Running {agent_name}...")
    prompt = load_prompt(agent_name)
    if agent_name == "planner":
        recent = get_recent_task_and_outcome_summaries()
        prompt = prompt.replace("{{INSERT_RECENT_TASKS_AND_OUTCOMES_HERE}}", recent)
    full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
    response = call_ollama(full_prompt)
    print(f"\n--- {agent_name} Response ---\n{response.strip()}\n")
    log_agent_output(agent_name, context, response)
    return response.strip()

def run_loop():
    goal = load_goal()
    print(f"=== Current Goal: {goal} ===")

    tasks = run_agent("planner", goal)
    execution_summary = run_agent("executor", tasks)
    reflection = run_agent("loopmind", execution_summary)
    run_agent("challenger", reflection)

    print("\n=== CYCLE COMPLETE ===")

if __name__ == "__main__":
    run_loop()