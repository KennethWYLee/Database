"""Verify Chapter 19 recovery teaching programs."""

from __future__ import annotations

import importlib.util
import json
from copy import deepcopy
from pathlib import Path


CHAPTER = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_recovery() -> None:
    recovery = load_module("recovery_simulator", CHAPTER / "recovery_simulator.py")
    case = json.loads((CHAPTER / "recovery_case.json").read_text(encoding="utf-8"))
    result = recovery.restart_recovery(case)

    assert result["redo_trace"] == [
        "REDO LSN 3 T0 A=950",
        "REDO LSN 4 T0 B=2050",
        "REDO LSN 7 T1 C=600",
    ]
    assert result["incomplete_after_redo"] == ["T1"]
    assert result["undo_trace"] == ["UNDO LSN 7 T1 C=700"]
    assert result["generated_records"] == [
        {
            "type": "REDO_ONLY",
            "transaction": "T1",
            "item": "C",
            "value": 700,
        },
        {"type": "ABORT", "transaction": "T1"},
    ]
    assert result["final_database"] == {"A": 950, "B": 2050, "C": 700}
    print("PASS repeating-history redo and incomplete-transaction undo")

    repeated_case = deepcopy(case)
    repeated_case["disk_at_crash"] = deepcopy(result["final_database"])
    repeated = recovery.restart_recovery(repeated_case)
    assert repeated["final_database"] == result["final_database"]
    print("PASS repeated physical recovery reaches the same final values")

    restored = recovery.restore_from_backup(case)
    assert restored == {"A": 950, "B": 2050, "C": 700}
    assert restored == result["final_database"]
    print("PASS archival backup plus committed log restore")


def verify_wal() -> None:
    wal = load_module("wal_checker", CHAPTER / "wal_checker.py")
    scenarios = json.loads(
        (CHAPTER / "wal_scenarios.json").read_text(encoding="utf-8")
    )
    valid = wal.check(scenarios["valid"])
    assert valid == {"valid": True, "violations": []}

    data_first = wal.check(scenarios["invalid_data_before_log"])
    assert data_first == {
        "valid": False,
        "violations": ["event 2: data A flushed before update log"],
    }
    commit_first = wal.check(scenarios["invalid_commit_before_force"])
    assert commit_first == {
        "valid": False,
        "violations": ["event 4: T0 acknowledged before commit log force"],
    }
    print("PASS valid and two invalid write-ahead logging timelines")


def main() -> None:
    verify_recovery()
    verify_wal()


if __name__ == "__main__":
    main()
