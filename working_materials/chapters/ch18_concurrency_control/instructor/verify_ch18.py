"""Verify Chapter 18 concurrency-control teaching programs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


CHAPTER = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_locks() -> None:
    simulator = load_module("lock_simulator", CHAPTER / "lock_simulator.py")
    scenarios = json.loads(
        (CHAPTER / "lock_scenarios.json").read_text(encoding="utf-8")
    )

    reads = simulator.analyze(scenarios["compatible_reads"])
    assert reads["two_phase"] is True
    assert reads["strict_two_phase"] is True
    assert reads["deadlock_cycle"] is None
    assert reads["events"][:2] == ["GRANT T1 S(A)", "GRANT T2 S(A)"]
    print("PASS compatible shared locks")

    writer = simulator.analyze(scenarios["writer_waits"])
    assert "WAIT T2 X(A) for T1" in writer["events"]
    assert "GRANT-WAITING T2 X(A)" in writer["events"]
    assert writer["deadlock_cycle"] is None
    print("PASS incompatible writer wait and later grant")

    deadlock = simulator.analyze(scenarios["deadlock"])
    assert deadlock["wait_edges"] == ["T1->T2", "T2->T1"]
    assert deadlock["deadlock_cycle"] in (
        ["T1", "T2", "T1"],
        ["T2", "T1", "T2"],
    )
    print("PASS wait-for graph deadlock cycle")

    invalid = simulator.analyze(scenarios["violates_two_phase"])
    assert invalid["two_phase"] is False
    basic = simulator.analyze(scenarios["basic_two_phase_not_strict"])
    assert basic["two_phase"] is True
    assert basic["strict_two_phase"] is False
    print("PASS basic and strict two-phase classifications")


def verify_multiversion() -> None:
    mvcc = load_module("mvcc_demo", CHAPTER / "mvcc_demo.py")
    result = mvcc.demonstration()
    assert result["reader_at_15"] == {"commit_timestamp": 10, "value": 100}
    assert result["reader_at_25"] == {"commit_timestamp": 20, "value": 90}
    assert result["reader_at_35"] == {"commit_timestamp": 30, "value": 120}
    print("PASS multiversion timestamp boundaries")

    skew = result["write_skew"]
    assert skew["t1_allows"] is True and skew["t2_allows"] is True
    assert skew["overlapping_writes"] is False
    assert skew["both_pass_write_write_check"] is True
    assert skew["final"] == {"checking": -100, "savings": 0}
    assert skew["constraint_sum_nonnegative"] is False
    print("PASS snapshot write-skew counterexample")


def main() -> None:
    verify_locks()
    verify_multiversion()


if __name__ == "__main__":
    main()
