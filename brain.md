# 🧠 Autonomous Agent Enterprise – Brain Overview

## Purpose
To build a self-evolving, self-correcting, income-generating autonomous AI system using local models and intelligent agents.

## Core Agents
- **Core (Mission Interpreter)** – Reads and distributes long-term goals
- **Planner-One** – Breaks down goals into high-leverage tasks
- **Executor-One** – Simulates or performs those tasks
- **Loopmind-One** – Reflects, logs outcomes, and proposes system mutations
- **Challenger** – Questions everything, identifies drift, and injects chaos-thoughts

## Architecture
- Loop cycles begin in `run_enterprise.py`
- Prompts live in `/prompts/`
- Goals and logs persist in `/memory/`
- Outputs saved per run in `/logs/`

## Current Model
- Qwen 2.5 (14B) running locally via Ollama