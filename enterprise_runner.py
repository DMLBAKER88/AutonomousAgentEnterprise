import json
import subprocess
from pathlib import Path
from datetime import datetime


class EnterpriseRunner:
    ENTERPRISE_ROOT = Path(__file__).parent
    MEMORY_DIR = ENTERPRISE_ROOT / "memory"
    PROMPT_DIR = ENTERPRISE_ROOT / "prompts"
    LOG_DIR = ENTERPRISE_ROOT / "logs"
    OLLAMA_MODEL = "qwen2.5:14b"

    LOG_DIR.mkdir(exist_ok=True)

    def load_goal(self):
        with open(self.MEMORY_DIR / "goals.json") as f:
            return json.load(f)["current_goal"]

    def call_ollama(self, prompt: str) -> str:
        result = subprocess.run(
            ["ollama", "run", self.OLLAMA_MODEL],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode("utf-8")

    def load_prompt(self, agent_name: str) -> str:
        with open(self.PROMPT_DIR / f"{agent_name}_prompt.txt") as f:
            return f.read()

    def log_agent_output(self, agent_name: str, context: str, output: str):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = self.LOG_DIR / f"{agent_name}_{timestamp}.md"
        with open(filename, "w") as f:
            f.write(f"# Agent: {agent_name}\n")
            f.write(f"## Timestamp: {timestamp}\n\n")
            f.write("### Context\n")
            f.write("```\n" + context.strip() + "\n```\n\n")
            f.write("### Output\n")
            f.write("```\n" + output.strip() + "\n```\n")

    def run_agent(self, agent_name: str, context: str) -> str:
        print(f"\n>>> Running {agent_name}...")
        prompt = self.load_prompt(agent_name)
        full_prompt = f"{prompt}\n\nCONTEXT:\n{context.strip()}"
        response = self.call_ollama(full_prompt)
        print(f"\n--- {agent_name} Response ---\n{response.strip()}\n")
        self.log_agent_output(agent_name, context, response)
        return response.strip()

    def update_outcomes_log(self, reflection_text: str):
        outcomes_path = self.MEMORY_DIR / "outcomes.json"
        if outcomes_path.exists():
            with open(outcomes_path) as f:
                outcomes = json.load(f)
        else:
            outcomes = []
        timestamp = datetime.now().isoformat()
        outcomes.append({"timestamp": timestamp, "reflection_text": reflection_text})
        with open(outcomes_path, "w") as f:
            json.dump(outcomes, f, indent=2)

    def run_loop(self):
        goal = self.load_goal()
        print(f"=== Current Goal: {goal} ===")

        tasks = self.run_agent("planner", goal)
        execution_summary = self.run_agent("executor", tasks)
        reflection = self.run_agent("loopmind", execution_summary)
        self.update_outcomes_log(reflection)
        self.run_agent("challenger", reflection)

        print("\n=== CYCLE COMPLETE ===")


if __name__ == "__main__":
    EnterpriseRunner().run_loop()
