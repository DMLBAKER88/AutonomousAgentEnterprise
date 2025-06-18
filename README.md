# Autonomous Agent Enterprise

This system runs a recursive multi-agent intelligence loop powered by Ollama + Qwen 2.5.

Each cycle logs agent outputs under `logs/enterprise.log` and records a summary
in `memory/task_log.json` for persistence across runs.
