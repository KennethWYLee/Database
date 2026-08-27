"""Demonstrate version visibility and snapshot write skew."""

from __future__ import annotations

import json
from typing import Any


def visible_version(
    versions: list[dict[str, int]], start_timestamp: int
) -> dict[str, int]:
    visible = [
        version
        for version in versions
        if version["commit_timestamp"] <= start_timestamp
    ]
    if not visible:
        raise ValueError("No committed version is visible")
    return max(visible, key=lambda version: version["commit_timestamp"])


def write_skew() -> dict[str, Any]:
    initial = {"checking": 100, "savings": 200}
    withdrawal = 200

    t1_snapshot = initial.copy()
    t2_snapshot = initial.copy()
    t1_allows = sum(t1_snapshot.values()) - withdrawal >= 0
    t2_allows = sum(t2_snapshot.values()) - withdrawal >= 0

    t1_write_set = {"checking"}
    t2_write_set = {"savings"}
    overlapping_writes = bool(t1_write_set & t2_write_set)

    final = initial.copy()
    if t1_allows:
        final["checking"] -= withdrawal
    if t2_allows:
        final["savings"] -= withdrawal

    return {
        "initial": initial,
        "t1_allows": t1_allows,
        "t2_allows": t2_allows,
        "overlapping_writes": overlapping_writes,
        "both_pass_write_write_check": t1_allows
        and t2_allows
        and not overlapping_writes,
        "final": final,
        "constraint_sum_nonnegative": sum(final.values()) >= 0,
    }


def demonstration() -> dict[str, Any]:
    versions = [
        {"commit_timestamp": 10, "value": 100},
        {"commit_timestamp": 20, "value": 90},
        {"commit_timestamp": 30, "value": 120},
    ]
    return {
        "versions": versions,
        "reader_at_15": visible_version(versions, 15),
        "reader_at_25": visible_version(versions, 25),
        "reader_at_35": visible_version(versions, 35),
        "write_skew": write_skew(),
    }


def main() -> None:
    print(json.dumps(demonstration(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
