from pathlib import Path
from datetime import datetime
import json
import subprocess


def _noop(*args, **kwargs):
    """Utility no-op for disabled debug prints."""
    pass

class EnterpriseRunner:
    """Handles the multi-agent orchestration loop."""

    def __init__(self, model: str = "qwen2.5:14b", *, debug: bool = False, quiet: bool = False):
        self.enterprise_root = Path(__file__).parent
        self.memory_dir = self.enterprise_root / "memory"
        self.prompt_dir = self.enterprise_root / "prompts"
        self.log_dir = self.enterprise_root / "logs"
        self.ollama_model = model
        self.debug = debug
        self.quiet = quiet
        self.log_dir.mkdir(exist_ok=True)

        self._debug_print = print if self.debug else _noop

    def _speak(self, msg: str):
        if not self.quiet:
            print(msg)

    def load_goal(self) -> str:
        with open(self.memory_dir / "goals.json") as f:
            return json.load(f)["current_goal"]

    def call_ollama(self, prompt: str) -> str:
        self._debug_print(f"Calling Ollama with model {self.ollama_model}")
        result = subprocess.run(
            ["ollama", "run", self.ollama_model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._debug_print(result.stderr.decode("utf-8"))
        return result.stdout.decode("utf-8")

    def load_prompt(self, agent_name: str) -> str:
        with open(self.prompt_dir / f"{agent_name}_prompt.txt") as f:
            return f.read()

    def log_agent_output(self, agent_name: str, context: str, output: str):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = self.log_dir / f"{agent_name}_{timestamp}.md"
        with open(filename, "w") as f:
            f.write(f"# Agent: {agent_name}\n")
            f.write(f"## Timestamp: {timestamp}\n\n")
            f.write("### Context\n")
            f.write("```\n" + context.strip() + "\n```\n\n")
            f.write("### Output\n")
            f.write("```\n" + output.strip() + "\n```\n")

    def run_agent(self, agent_name: str, context: str) -> str:
        self._speak(f"\n>>> Running {agent_name}...")
        prompt = self.load_prompt(agent_name)
        self._debug_print(f"Prompt:\n{prompt}")
        full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
        self._debug_print(f"Full prompt:\n{full_prompt}")
        response = self.call_ollama(full_prompt)
        cleaned = response.strip()
        if not self.quiet:
            print(f"\n--- {agent_name} Response ---\n{cleaned}\n")
        else:
            self._debug_print(f"{agent_name} Response:\n{cleaned}")
        self.log_agent_output(agent_name, context, cleaned)
        return cleaned

    def run_loop(self):
        goal = self.load_goal()
        print(f"=== Current Goal: {goal} ===")

        tasks = self.run_agent("planner", goal)
        execution_summary = self.run_agent("executor", tasks)
        reflection = self.run_agent("loopmind", execution_summary)
        self.run_agent("challenger", reflection)

        print("\n=== CYCLE COMPLETE ===")
