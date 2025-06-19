# Autonomous Agent Enterprise

This system runs a recursive multi-agent intelligence loop powered by Ollama + Qwen 2.5.

Each cycle:
- Runs a sequence of intelligent agents to plan, execute, reflect, and challenge
- Logs agent outputs in markdown format under `logs/`
- Records a summary in `memory/task_log.json` and `outcomes.json` for persistence across runs

---

## 🚀 Running

Use the command:

```bash
python run_enterprise.py
```

to start a new cycle.

---

## 🛠 Debug and Quiet Modes

You can pass command-line flags to control verbosity:

- `--debug`: shows extra internal steps and prompt content
- `--quiet`: hides agent chatter, only prints final summaries

Example:

```bash
python run_enterprise.py --debug
```

---

## ⚙️ Config File

Default verbosity settings can be stored in `memory/config.json`:

```json
{
  "debug": false,
  "quiet": false
}
```

🧠 CLI flags override config file settings.

---

## 📚 Logs and Memory

- Raw agent interactions are saved in timestamped `.md` files under `logs/`
- Each cycle's tasks, reflections, and outcomes are recorded in:
  - `memory/task_log.json`
  - `memory/outcomes.json`
  - `memory/mutations.json` (if proposed)

This lets the system improve itself recursively over time.

---

## 👁️ Human-Facing Outputs

- `valleylog.md` is a narrative log, written by the LUX agent
- `AGENTS.md` describes each agent's role, prompt style, and expectations
- `manifesto.md`, `governance.md`, and `system_lifecycle.md` define the system's long-term vision and ethical alignment

---

## 💡 Want to Contribute?

Start by reading:

- `manifesto.md` – system philosophy  
- `governance.md` – immutable ethics  
- `system_lifecycle.md` – loop logic

Then run the system, observe the logs, and propose improvements!

Stay recursive.
