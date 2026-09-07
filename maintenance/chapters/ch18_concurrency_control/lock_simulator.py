"""Simulate small S/X lock schedules for Chapter 18 activities."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def compatible(left: str, right: str) -> bool:
    return left == "S" and right == "S"


def cycle_nodes(edges: set[tuple[str, str]]) -> list[str] | None:
    graph: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()
    for source, target in edges:
        graph[source].append(target)
        nodes.update({source, target})

    state: dict[str, int] = {node: 0 for node in nodes}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        state[node] = 1
        stack.append(node)
        for target in sorted(graph[node]):
            if state[target] == 0:
                found = visit(target)
                if found is not None:
                    return found
            elif state[target] == 1:
                start = stack.index(target)
                return stack[start:] + [target]
        stack.pop()
        state[node] = 2
        return None

    for node in sorted(nodes):
        if state[node] == 0:
            found = visit(node)
            if found is not None:
                return found
    return None


class LockSimulation:
    def __init__(self) -> None:
        self.held: dict[str, list[tuple[str, str]]] = defaultdict(list)
        self.waiting: list[tuple[str, str, str]] = []
        self.released: set[str] = set()
        self.two_phase = True
        self.strict_two_phase = True
        self.events: list[str] = []

    def blockers(self, transaction: str, mode: str, item: str) -> list[str]:
        return sorted(
            holder
            for holder, held_mode in self.held[item]
            if holder != transaction and not compatible(mode, held_mode)
        )

    def request(self, transaction: str, mode: str, item: str) -> None:
        if transaction in self.released:
            self.two_phase = False
        blockers = self.blockers(transaction, mode, item)
        if blockers:
            self.waiting.append((transaction, mode, item))
            self.events.append(
                f"WAIT {transaction} {mode}({item}) for {','.join(blockers)}"
            )
        else:
            self.held[item].append((transaction, mode))
            self.events.append(f"GRANT {transaction} {mode}({item})")

    def unlock(self, transaction: str, item: str, ending: bool = False) -> None:
        released_modes = [
            mode for holder, mode in self.held[item] if holder == transaction
        ]
        if not ending and "X" in released_modes:
            self.strict_two_phase = False
        self.held[item] = [
            (holder, mode)
            for holder, mode in self.held[item]
            if holder != transaction
        ]
        self.released.add(transaction)
        self.events.append(f"RELEASE {transaction} ({item})")
        self.grant_waiting()

    def grant_waiting(self) -> None:
        progress = True
        while progress:
            progress = False
            remaining: list[tuple[str, str, str]] = []
            for transaction, mode, item in self.waiting:
                if not self.blockers(transaction, mode, item):
                    self.held[item].append((transaction, mode))
                    self.events.append(f"GRANT-WAITING {transaction} {mode}({item})")
                    progress = True
                else:
                    remaining.append((transaction, mode, item))
            self.waiting = remaining

    def finish(self, transaction: str, action: str) -> None:
        items = [
            item
            for item, locks in self.held.items()
            if any(holder == transaction for holder, _mode in locks)
        ]
        self.waiting = [entry for entry in self.waiting if entry[0] != transaction]
        self.events.append(f"{action} {transaction}")
        for item in items:
            self.unlock(transaction, item, ending=True)

    def wait_edges(self) -> set[tuple[str, str]]:
        edges: set[tuple[str, str]] = set()
        for transaction, mode, item in self.waiting:
            for blocker in self.blockers(transaction, mode, item):
                edges.add((transaction, blocker))
        return edges

    def run(self, actions: list[dict[str, str]]) -> dict[str, Any]:
        for step in actions:
            transaction = step["transaction"]
            action = step["action"]
            if action == "LOCK":
                self.request(transaction, step["mode"], step["item"])
            elif action == "UNLOCK":
                self.unlock(transaction, step["item"])
            elif action in {"COMMIT", "ABORT"}:
                self.finish(transaction, action)
            else:
                raise ValueError(f"Unknown action: {action}")

        edges = self.wait_edges()
        cycle = cycle_nodes(edges)
        return {
            "events": self.events,
            "two_phase": self.two_phase,
            "strict_two_phase": self.two_phase and self.strict_two_phase,
            "wait_edges": sorted(f"{source}->{target}" for source, target in edges),
            "deadlock_cycle": cycle,
        }


def analyze(actions: list[dict[str, str]]) -> dict[str, Any]:
    return LockSimulation().run(actions)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "scenario_file",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("lock_scenarios.json"),
    )
    args = parser.parse_args()
    scenarios = json.loads(args.scenario_file.read_text(encoding="utf-8"))
    for name, actions in scenarios.items():
        print(f"[{name}]")
        print(json.dumps(analyze(actions), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
