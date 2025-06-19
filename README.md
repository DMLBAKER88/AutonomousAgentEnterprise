# Autonomous Agent Enterprise

This system runs a recursive multi-agent intelligence loop powered by Ollama + Qwen 2.5.

## Running

Use `python run_enterprise.py` to start a cycle.

### Debug and Quiet Modes

Pass command-line flags to control logging:

- `--debug` shows extra internal steps and prompts.
- `--quiet` hides agent chatter and only prints summary output.

Default values can be set in `memory/config.json`:

```json
{
  "debug": false,
  "quiet": false
}
```

CLI flags override these settings.
