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

# Path to the aggregated logbook for the current run
LOGBOOK_PATH = None

def init_logbook() -> Path:
    """Create a markdown logbook for this run and return its path."""
    global LOGBOOK_PATH
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    LOGBOOK_PATH = LOG_DIR / f"logbook_{timestamp}.md"
    with open(LOGBOOK_PATH, "w") as f:
        f.write(f"# 📓 AWE Logbook - {timestamp}\n\n")
    return LOGBOOK_PATH

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

def log_agent_output(agent_name: str, context_label: str, context: str, output: str):
    """Append a nicely formatted log entry to the run logbook."""
    if LOGBOOK_PATH is None:
        raise RuntimeError("Logbook has not been initialized")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGBOOK_PATH, "a") as f:
        f.write(f"## 🤖 Agent: {agent_name}\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        f.write(f"### {context_label}\n")
        f.write(context.strip() + "\n\n")
        f.write("### 📣 Output\n")
        f.write(output.strip() + "\n\n")
        f.write("---\n\n")

def run_agent(agent_name: str, context_label: str, context: str) -> str:
    print(f"\n>>> Running {agent_name}...")
    prompt = load_prompt(agent_name)
    full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
    response = call_ollama(full_prompt)
    print(f"\n--- {agent_name} Response ---\n{response.strip()}\n")
    log_agent_output(agent_name, context_label, context, response)
    return response.strip()

def run_loop():
    init_logbook()
    goal = load_goal()
    print(f"=== Current Goal: {goal} ===")

    tasks = run_agent("planner", "Goal", goal)
    execution_summary = run_agent("executor", "Task List", tasks)
    reflection = run_agent("loopmind", "Execution Summary", execution_summary)
    run_agent("challenger", "Reflection", reflection)

    print("\n=== CYCLE COMPLETE ===")

from enterprise_runner import EnterpriseRunner

if __name__ == "__main__":
    EnterpriseRunner().run_loop()
