"""Check small event timelines against core write-ahead logging requirements."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def check(events: list[dict[str, Any]]) -> dict[str, Any]:
    forced_through = 0
    update_lsns_by_item: dict[str, list[int]] = defaultdict(list)
    transaction_lsns: dict[str, list[int]] = defaultdict(list)
    commit_lsn: dict[str, int] = {}
    violations: list[str] = []

    for position, event in enumerate(events, start=1):
        action = event["action"]
        if action == "CREATE_UPDATE_LOG":
            update_lsns_by_item[event["item"]].append(event["lsn"])
            transaction_lsns[event["transaction"]].append(event["lsn"])
        elif action == "CREATE_COMMIT_LOG":
            transaction_lsns[event["transaction"]].append(event["lsn"])
            commit_lsn[event["transaction"]] = event["lsn"]
        elif action == "FORCE_LOG":
            forced_through = max(forced_through, event["through_lsn"])
        elif action == "FLUSH_DATA":
            needed = update_lsns_by_item[event["item"]]
            if needed and max(needed) > forced_through:
                violations.append(
                    f"event {position}: data {event['item']} flushed before update log"
                )
        elif action == "ACK_COMMIT":
            transaction = event["transaction"]
            needed = transaction_lsns[transaction]
            if transaction not in commit_lsn or not needed or max(needed) > forced_through:
                violations.append(
                    f"event {position}: {transaction} acknowledged before commit log force"
                )
        else:
            raise ValueError(f"Unknown action: {action}")

    return {"valid": not violations, "violations": violations}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "scenario_file",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("wal_scenarios.json"),
    )
    args = parser.parse_args()
    scenarios = json.loads(args.scenario_file.read_text(encoding="utf-8"))
    for name, events in scenarios.items():
        print(f"[{name}]")
        print(json.dumps(check(events), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
