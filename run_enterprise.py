import json
import subprocess
from datetime import datetime
from pathlib import Path
import argparse

ENTERPRISE_ROOT = Path(__file__).parent
MEMORY_DIR = ENTERPRISE_ROOT / "memory"
PROMPT_DIR = ENTERPRISE_ROOT / "prompts"
LOG_DIR = ENTERPRISE_ROOT / "logs"
CONFIG_PATH = MEMORY_DIR / "config.json"
OLLAMA_MODEL = "qwen2.5:14b"

DEBUG = False
QUIET = False
LOGBOOK_PATH = None
AGENT_SEQUENCE = ["planner", "executor", "loopmind", "challenger"]

LOG_DIR.mkdir(exist_ok=True)

# ----------------------------------------
# Utility + I/O Functions
# ----------------------------------------


def debug_print(msg: str):
    if DEBUG:
        print(msg)


def speak(msg: str):
    if not QUIET:
        print(msg)


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"debug": False, "quiet": False}


def init_logbook() -> Path:
    global LOGBOOK_PATH
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    LOGBOOK_PATH = LOG_DIR / f"logbook_{timestamp}.md"
    with open(LOGBOOK_PATH, "w") as f:
        f.write(f"# 📓 AWE Logbook - {timestamp}\n\n")
    return LOGBOOK_PATH


def log_agent_output(agent_name: str, context_label: str, context: str, output: str):
    if LOGBOOK_PATH is None:
        raise RuntimeError("Logbook not initialized")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGBOOK_PATH, "a") as f:
        f.write(f"## 🤖 Agent: {agent_name}\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        f.write(f"### {context_label}\n{context.strip()}\n\n")
        f.write(f"### 📣 Output\n{output.strip()}\n\n---\n\n")


def append_task_log(entry: dict):
    path = MEMORY_DIR / "task_log.json"
    data = []
    if path.exists():
        with path.open() as f:
            data = json.load(f)
    data.append(entry)
    with path.open("w") as f:
        json.dump(data, f, indent=2)


# ----------------------------------------
# Core Execution Logic
# ----------------------------------------


def load_goal() -> str:
    with open(MEMORY_DIR / "goals.json") as f:
        return json.load(f)["current_goal"]


def load_prompt(agent_name: str) -> str:
    with open(PROMPT_DIR / f"{agent_name}_prompt.txt") as f:
        return f.read()


def call_ollama(prompt: str) -> str:
    debug_print(f"Calling Ollama with model {OLLAMA_MODEL}")
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    debug_print(result.stderr.decode("utf-8"))
    return result.stdout.decode("utf-8")


def run_agent(agent_name: str, context_label: str, context: str) -> str:
    speak(f"\n>>> Running {agent_name}...")
    prompt = load_prompt(agent_name)
    debug_print(f"Prompt:\n{prompt}")
    full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
    debug_print(f"Full prompt:\n{full_prompt}")
    response = call_ollama(full_prompt)
    cleaned = response.strip()
    if not QUIET:
        print(f"\n--- {agent_name} Response ---\n{cleaned}\n")
    else:
        debug_print(f"{agent_name} Response:\n{cleaned}")
    log_agent_output(agent_name, context_label, context, cleaned)
    return cleaned


# ----------------------------------------
# Full Cycle Runner
# ----------------------------------------


def run_cycle() -> None:
    init_logbook()
    goal = load_goal()
    print(f"=== Current Goal: {goal} ===")

    tasks = run_agent("planner", "Goal", goal)
    execution_summary = run_agent("executor", "Task List", tasks)
    reflection = run_agent("loopmind", "Execution Summary", execution_summary)
    challenge = run_agent("challenger", "Reflection", reflection)

    append_task_log(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "goal": goal,
            "tasks": tasks,
            "execution": execution_summary,
            "reflection": reflection,
            "challenge": challenge,
        }
    )

    print("\n=== CYCLE COMPLETE ===")


# ----------------------------------------
# CLI Entrypoint
# ----------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the autonomous agent loop")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", action="store_true", help="Suppress agent chatter")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg = load_config()
    DEBUG = args.debug or cfg.get("debug", False)
    QUIET = args.quiet or cfg.get("quiet", False)
    run_cycle()
