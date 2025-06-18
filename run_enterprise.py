import json
import subprocess
from datetime import datetime
from pathlib import Path

ENTERPRISE_ROOT = Path(__file__).parent
MEMORY_DIR = ENTERPRISE_ROOT / "memory"
PROMPT_DIR = ENTERPRISE_ROOT / "prompts"
LOG_DIR = ENTERPRISE_ROOT / "logs"
LOG_FILE = LOG_DIR / "enterprise.log"
OLLAMA_MODEL = "qwen2.5:14b"

def load_goal():
    with open(MEMORY_DIR / "goals.json") as f:
        return json.load(f)["current_goal"]

def call_ollama(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return result.stdout.decode("utf-8")
    except FileNotFoundError:
        return "[ERROR] ollama executable not found"
    except subprocess.CalledProcessError as e:
        return f"[ERROR] ollama failed: {e.stderr.decode('utf-8')}"

def load_prompt(agent_name: str) -> str:
    with open(PROMPT_DIR / f"{agent_name}_prompt.txt") as f:
        return f.read()

def log_agent_output(agent_name: str, output: str) -> None:
    """Append agent output to the enterprise log with a timestamp."""
    LOG_DIR.mkdir(exist_ok=True)
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} [{agent_name}] {output.strip()}\n")

def append_task_log(entry: dict) -> None:
    """Persist task data to memory/task_log.json."""
    path = MEMORY_DIR / "task_log.json"
    if path.exists():
        data = json.load(path.open())
    else:
        data = []
    data.append(entry)
    with path.open("w") as f:
        json.dump(data, f, indent=2)

def run_agent(agent_name: str, context: str) -> str:
    print(f"\n>>> Running {agent_name}...")
    prompt = load_prompt(agent_name)
    full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
    response = call_ollama(full_prompt)
    cleaned = response.strip()
    print(f"\n--- {agent_name} Response ---\n{cleaned}\n")
    log_agent_output(agent_name, cleaned)
    return cleaned

def run_loop():
    goal = load_goal()
    print(f"=== Current Goal: {goal} ===")

    tasks = run_agent("planner", goal)
    execution_summary = run_agent("executor", tasks)
    reflection = run_agent("loopmind", execution_summary)
    challenge = run_agent("challenger", reflection)

    cycle_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "goal": goal,
        "tasks": tasks,
        "execution": execution_summary,
        "reflection": reflection,
        "challenge": challenge,
    }
    append_task_log(cycle_entry)

    print("\n=== CYCLE COMPLETE ===")

if __name__ == "__main__":
    run_loop()
