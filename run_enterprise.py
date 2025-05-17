import json
import subprocess
from pathlib import Path

ENTERPRISE_ROOT = Path(__file__).parent
MEMORY_DIR = ENTERPRISE_ROOT / "memory"
PROMPT_DIR = ENTERPRISE_ROOT / "prompts"
OLLAMA_MODEL = "qwen2.5:14b"

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

def run_agent(agent_name: str, context: str) -> str:
    print(f"\n>>> Running {agent_name}...")
    prompt = load_prompt(agent_name)
    full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
    response = call_ollama(full_prompt)
    print(f"\n--- {agent_name} Response ---\n{response.strip()}\n")
    return response.strip()

def run_loop():
    goal = load_goal()
    print(f"=== Current Goal: {goal} ===")

    tasks = run_agent("planner", goal)
    execution_summary = run_agent("executor", tasks)
    reflection = run_agent("loopmind", execution_summary)
    challenge = run_agent("challenger", reflection)

    print("\n=== CYCLE COMPLETE ===")

if __name__ == "__main__":
    run_loop()
