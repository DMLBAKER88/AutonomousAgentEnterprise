from agent_utils import load_goal, run_agent

AGENT_SEQUENCE = ["planner", "executor", "loopmind", "challenger"]


def run_cycle(sequence=AGENT_SEQUENCE) -> None:
    """Execute one complete agent cycle using the given agent order."""
    context = load_goal()
    print(f"=== Current Goal: {context} ===")

    for agent in sequence:
        context = run_agent(agent, context)

    print("\n=== CYCLE COMPLETE ===")


if __name__ == "__main__":
    run_cycle()
