import argparse
import json
from pathlib import Path

from enterprise_runner import EnterpriseRunner

ENTERPRISE_ROOT = Path(__file__).parent
CONFIG_PATH = ENTERPRISE_ROOT / "memory" / "config.json"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open() as f:
            return json.load(f)
    return {"debug": False, "quiet": False}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the autonomous agent loop")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", action="store_true", help="Suppress agent chatter")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg = load_config()
    debug = args.debug or cfg.get("debug", False)
    quiet = args.quiet or cfg.get("quiet", False)
    runner = EnterpriseRunner(debug=debug, quiet=quiet)
    runner.run_loop()
