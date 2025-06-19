import json
import subprocess
from pathlib import Path
from datetime import datetime

ENTERPRISE_ROOT = Path(__file__).resolve().parent
MEMORY_DIR = ENTERPRISE_ROOT / "memory"
PROMPT_DIR = ENTERPRISE_ROOT / "prompts"
LOG_DIR = ENTERPRISE_ROOT / "logs"
OLLAMA_MODEL = "qwen2.5:14b"

LOG_DIR.mkdir(exist_ok=True)

def load_goal() -> str:
    """Return the current goal from ``memory/goals.json``."""
    with open(MEMORY_DIR / "goals.json") as f:
        return json.load(f)["current_goal"]

def load_prompt(agent_name: str) -> str:
    """Return the prompt text for a given agent."""
    with open(PROMPT_DIR / f"{agent_name}_prompt.txt") as f:
        return f.read()

def call_ollama(prompt: str) -> str:
    """Execute an Ollama model with the provided prompt."""
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8")

def log_agent_output(agent_name: str, context: str, output: str) -> Path:
    """Write agent interaction details to a markdown log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = LOG_DIR / f"{agent_name}_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(f"# Agent: {agent_name}\n")
        f.write(f"## Timestamp: {timestamp}\n\n")
        f.write("### Context\n")
        f.write("```\n" + context.strip() + "\n```\n\n")
        f.write("### Output\n")
        f.write("```\n" + output.strip() + "\n```\n")
    return filename

def run_agent(agent_name: str, context: str) -> str:
    """Run an agent with the provided context and return its response."""
    print(f"\n>>> Running {agent_name}...")
    prompt = load_prompt(agent_name)
    full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
    response = call_ollama(full_prompt)
    print(f"\n--- {agent_name} Response ---\n{response.strip()}\n")
    log_agent_output(agent_name, context, response)
    return response.strip()
