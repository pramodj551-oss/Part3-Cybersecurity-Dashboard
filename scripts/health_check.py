"""CLI health/readiness check for CI and deployment smoke validation."""

from __future__ import annotations

import argparse
import json
import sys

from src.health import health_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate production health/readiness.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    snapshot = health_snapshot()
    if args.as_json:
        print(json.dumps(snapshot, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(snapshot, indent=2, sort_keys=True))

    if snapshot["liveness"]["status"] != "ok":
        return 1
    if snapshot["readiness"]["status"] != "ready":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
