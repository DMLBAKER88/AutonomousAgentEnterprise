# 🤖 Agent Overview

This project orchestrates several autonomous agents to evolve the **Autonomous Wealth Engine (AWE)** toward profitability. Each agent has a focused role with clear output expectations. All prompts live in the `prompts/` directory and agent outputs are logged in `logs/`.

## Current Agents

### Core (Mission Interpreter)
* **Role:** Reads `memory/goals.json` and distributes the active goal to the rest of the system.
* **Output:** Plain text goal string.

### Planner-One
* **Role:** Breaks the goal into 3–5 high‑leverage tasks.
* **Prompt:** `prompts/planner_prompt.txt`.
* **Expected Output:** A formatted list of tasks with brief rationale.

### Executor-One
* **Role:** Performs or simulates each task and reports results.
* **Prompt:** `prompts/executor_prompt.txt`.
* **Expected Output:** Clear step‑by‑step actions or outcomes that another agent could verify or continue.

### Loopmind-One
* **Role:** Reflects on the cycle, evaluates success and failure, and proposes system mutations.
* **Prompt:** `prompts/loopmind_prompt.txt`.
* **Expected Output:** Structured reflection covering summary, evaluation, signals of drift, and proposed improvements.

### Challenger
* **Role:** Questions assumptions, highlights risks, and injects contrarian ideas.
* **Prompt:** `prompts/challenger_prompt.txt`.
* **Expected Output:** At least one pointed critique and one chaotic insight to prevent complacency.

### LUX (Synthesizer)
* **Role:** Writes human‑friendly diary updates in `valleylog.md` and integrates insights from other agents.
* **Output:** Glamorous summaries of each cycle.

### Bestie-One
* **Role:** Reviews UX tone and aesthetics to keep outputs readable and on‑brand.
* **Output:** Suggestions for style and clarity.


## Adding New Agents
1. Create a new prompt file in `prompts/` named `<agent>_prompt.txt` describing the role, required context, and output format.
2. Extend `run_enterprise.py` to call the new agent in the desired order using `run_agent("<agent>", context)`.
3. Document the agent in this file under **Current Agents** with its role and output expectations.
4. Commit the prompt and code changes along with an update to `changelog.md`.
5. Ensure the agent respects `governance.md` and logs its output under `logs/`.

## Coding & Prompt Conventions
* Keep agent code in Python and follow the existing pattern in `run_enterprise.py`.
* Prompts should explicitly reference any docs the agent must read (e.g., `manifesto.md`, `system_lifecycle.md`).
* Agents should respond in concise markdown where possible and avoid unnecessary verbosity.
* Every agent invocation is logged via `log_agent_output()` for traceability.
* Agents must abide by the ethical rules in `governance.md` and seek long‑term sustainability.

## Evolving Toward Profitability
Agents collectively push the system to discover opportunities, validate them, build tools, launch experiments, monitor performance, and evolve strategies. Planner-One proposes high‑leverage tasks, Executor-One delivers actionable results, Loopmind-One reflects and suggests improvements, and Challenger keeps the system from stagnating. LUX records the narrative. New profit‑oriented agents—such as Hunter-One or Builder-One—can be added following the steps above. Each cycle should bring the system closer to autonomous revenue while maintaining ethical alignment.
