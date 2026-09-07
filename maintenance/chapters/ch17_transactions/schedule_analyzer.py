"""Analyze small educational schedules from schedule_examples.json."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def transactions(schedule: list[dict[str, str]]) -> list[str]:
    return sorted({step["transaction"] for step in schedule})


def conflict_edges(schedule: list[dict[str, str]]) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for left_index, left in enumerate(schedule):
        if left["operation"] not in {"R", "W"}:
            continue
        for right in schedule[left_index + 1 :]:
            if right["operation"] not in {"R", "W"}:
                continue
            if left["transaction"] == right["transaction"]:
                continue
            if left.get("item") != right.get("item"):
                continue
            if "W" in {left["operation"], right["operation"]}:
                edges.add((left["transaction"], right["transaction"]))
    return edges


def topological_order(nodes: list[str], edges: set[tuple[str, str]]) -> list[str] | None:
    outgoing: dict[str, set[str]] = defaultdict(set)
    indegree = {node: 0 for node in nodes}
    for source, target in edges:
        if target not in outgoing[source]:
            outgoing[source].add(target)
            indegree[target] += 1

    ready = sorted(node for node, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for target in sorted(outgoing[node]):
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
                ready.sort()
    return order if len(order) == len(nodes) else None


def read_dependencies(schedule: list[dict[str, str]]) -> list[tuple[str, str, str, int]]:
    """Return writer, reader, item, and read position for observed read-from links."""
    last_writer: dict[str, str] = {}
    links: list[tuple[str, str, str, int]] = []
    for position, step in enumerate(schedule):
        operation = step["operation"]
        item = step.get("item")
        transaction = step["transaction"]
        if operation == "W" and item is not None:
            last_writer[item] = transaction
        elif operation == "R" and item in last_writer:
            writer = last_writer[item]
            if writer != transaction:
                links.append((writer, transaction, item, position))
    return links


def commit_positions(schedule: list[dict[str, str]]) -> dict[str, int]:
    return {
        step["transaction"]: position
        for position, step in enumerate(schedule)
        if step["operation"] == "C"
    }


def recoverability(schedule: list[dict[str, str]]) -> tuple[bool, bool]:
    commits = commit_positions(schedule)
    recoverable = True
    cascadeless = True
    for writer, reader, _item, read_position in read_dependencies(schedule):
        writer_commit = commits.get(writer)
        reader_commit = commits.get(reader)
        if reader_commit is not None and (
            writer_commit is None or writer_commit > reader_commit
        ):
            recoverable = False
        if writer_commit is None or writer_commit > read_position:
            cascadeless = False
    return recoverable, cascadeless


def analyze(schedule: list[dict[str, str]]) -> dict[str, Any]:
    edges = conflict_edges(schedule)
    order = topological_order(transactions(schedule), edges)
    recoverable, cascadeless = recoverability(schedule)
    return {
        "edges": sorted(f"{source}->{target}" for source, target in edges),
        "conflict_serializable": order is not None,
        "serial_order": order,
        "recoverable": recoverable,
        "cascadeless": cascadeless,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "schedule_file",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("schedule_examples.json"),
    )
    args = parser.parse_args()
    schedules = json.loads(args.schedule_file.read_text(encoding="utf-8"))
    for name, schedule in schedules.items():
        print(f"[{name}]")
        print(json.dumps(analyze(schedule), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
