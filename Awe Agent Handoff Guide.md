# Autonomous Wealth Engine (AWE): Clean System Handoff Document

> **Purpose:** This document is designed to bring any human or large language model (LLM) up to speed on the design, intent, structure, and current state of the *Autonomous Wealth Engine* (AWE) project — a self-evolving, multi-agent system for autonomous strategy, self-reflection, and revenue generation.

---

## 1. SYSTEM OVERVIEW

### Project Codename:

**Autonomous Wealth Engine (AWE)**

### Project Type:

* Autonomous, self-organizing AI agent ecosystem
* Local-first, LLM-driven
* Built in Python using a modular folder structure

### Primary Goal:

To develop a recursive AI system capable of:

* Generating income autonomously
* Creating and evolving its own agents, strategies, and architecture
* Operating continuously with minimal human input
* Retaining alignment with its creator’s values: autonomy, clarity, elegance, and sustainability

### Philosophy:

* The system operates within ethical and legal boundaries
* Encourages experimentation and critique
* Emphasizes sustainable, long-term thinking over short-term hacks

---

## 2. FOLDER + FILE STRUCTURE (Key Paths)

```
AutonomousAgentEnterprise/
├── run_enterprise.py            # Core orchestrator script
├── .venv/                       # Virtual environment
├── prompts/                    # Agent-specific prompt files
│   ├── planner_prompt.txt
│   ├── executor_prompt.txt
│   ├── loopmind_prompt.txt
│   ├── challenger_prompt.txt
├── memory/                     # System-wide memory
│   ├── goals.json              # Current top-level goal
│   ├── task_log.json           # Historical task list with status
│   ├── outcomes.json           # Task outcomes / results
├── logs/                       # Raw per-agent markdown logs
├── valleylog.md                # Human-readable narrative summary (Valley Girl style)
├── manifesto.md                # Philosophy + vision of the system
├── governance.md               # Immutable rules + ethics
├── system_lifecycle.md         # Operational architecture
├── system_checkin_template.md  # Weekly review protocol
├── changelog.md                # Manual version notes
```

---

## 3. CORE AGENTS (As of v0.3)

| Agent        | Role                   | Summary                                                           |
| ------------ | ---------------------- | ----------------------------------------------------------------- |
| Planner-One  | Strategic planner      | Breaks high-level goal into 3–5 high-leverage tasks               |
| Executor-One | Tactical implementer   | Breaks tasks into executable steps; suggests tools + libraries    |
| Loopmind-One | Reflective analyst     | Reviews past cycle, notes entropy or misalignment                 |
| Challenger   | Contrarian disruptor   | Exposes risk, failure points, proposes chaotic or bold pivots     |
| LUX          | Synthesizer + narrator | Integrates insight, updates system, writes `valleylog.md` entries |
| Bestie-One   | UX & aesthetic critic  | Oversees brand tone, user-friendliness, and human readability     |

Future agents may include Hunter-One (profit scouting), Builder-One (automated dev), or Archivist (long-term memory).

---

## 4. CORE LOOP CYCLE

Each run of `run_enterprise.py` triggers:

1. **Planner-One** reads the current goal and sets tasks
2. **Executor-One** creates actionable strategies for each task
3. **Loopmind-One** reflects on cycle quality and systemic risks
4. **Challenger** pushes back with philosophical or structural critique
5. **LUX** integrates and updates `valleylog.md`
6. (In future) Memory updated with task and outcome logs

---

## 5. HUMAN-FACING OUTPUTS

* `valleylog.md` – Digestible, emotionally intelligent summary written in humorous tone for humans
* `logs/*.md` – Raw per-agent markdown logs with timestamps
* `task_log.json` – Objective tracking for tasks and current status
* `outcomes.json` – Outcomes and insights per task

---

## 6. CURRENT GOAL (as of last loop)

```json
{
  "current_goal": "Evolve into a self-improving, profitable autonomous agent system."
}
```

Planner's current focus:

* Develop core algorithm for learning
* Build profitability metrics dashboard
* Analyze user interaction feedback
* Research self-improvement techniques
* Prototype autonomous adaptation features

---

## 7. DESIGN CONSIDERATIONS

* Start verbose, human-friendly
* Add Quiet Mode later if needed (for batch runs or low-verbosity cycles)
* Never sacrifice traceability
* Maintain a single source of truth via the `valleylog.md` and `task_log.json`
* All agents must justify actions in logs

---

## 8. TRANSFER TO NEW AGENT OR LLM

If a new LLM (or human) is taking over as the lead orchestrator, they must:

1. Read `valleylog.md` to understand recent activity
2. Scan `task_log.json` and `outcomes.json`
3. Refer to `manifesto.md` and `governance.md` for alignment
4. Run `run_enterprise.py` to resume the loop
5. Optionally evolve or spawn new agents

---

## 9. FINAL NOTE

This system is designed to operate like an evolving organism. It builds itself, challenges itself, and logs its own story. Your job is not to micromanage — it's to guide, seed, and observe its growth.

Stay recursive. Stay elegant. And always check the valleylog.
