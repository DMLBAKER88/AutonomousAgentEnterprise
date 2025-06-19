import json
import subprocess
from pathlib import Path
import argparse
from datetime import datetime

ENTERPRISE_ROOT = Path(__file__).parent
MEMORY_DIR = ENTERPRISE_ROOT / "memory"
PROMPT_DIR = ENTERPRISE_ROOT / "prompts"
LOG_DIR = ENTERPRISE_ROOT / "logs"
CONFIG_PATH = MEMORY_DIR / "config.json"
OLLAMA_MODEL = "qwen2.5:14b"

DEBUG = False
QUIET = False

LOG_DIR.mkdir(exist_ok=True)


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


def load_goal():
    with open(MEMORY_DIR / "goals.json") as f:
        return json.load(f)["current_goal"]


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
    speak(f"\n>>> Running {agent_name}...")
    prompt = load_prompt(agent_name)
    debug_print(f"Prompt for {agent_name}:\n{prompt}")
    full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
    debug_print(f"Full prompt:\n{full_prompt}")
    response = call_ollama(full_prompt)
    if not QUIET:
        print(f"\n--- {agent_name} Response ---\n{response.strip()}\n")
    else:
        debug_print(f"{agent_name} Response:\n{response.strip()}")
    log_agent_output(agent_name, context, response)
    return response.strip()


def run_loop(debug: bool = False, quiet: bool = False):
    global DEBUG, QUIET
    DEBUG = debug
    QUIET = quiet

    goal = load_goal()
    print(f"=== Current Goal: {goal} ===")

    tasks = run_agent("planner", goal)
    execution_summary = run_agent("executor", tasks)
    reflection = run_agent("loopmind", execution_summary)
    run_agent("challenger", reflection)

    if QUIET:
        print("\n--- Final Reflection ---")
        print(reflection)
    print("\n=== CYCLE COMPLETE ===")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the autonomous agent loop")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", action="store_true", help="Suppress agent chatter")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg = load_config()
    debug = args.debug or cfg.get("debug", False)
    quiet = args.quiet or cfg.get("quiet", False)
    run_loop(debug=debug, quiet=quiet)
