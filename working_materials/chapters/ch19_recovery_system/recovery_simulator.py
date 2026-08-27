"""Simulate basic repeating-history recovery and backup-plus-log restore."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


def records_from_checkpoint(case: dict[str, Any]) -> list[dict[str, Any]]:
    checkpoint_lsn = case["checkpoint_lsn"]
    records = [record for record in case["log"] if record["lsn"] >= checkpoint_lsn]
    if not records or records[0]["type"] != "CHECKPOINT":
        raise ValueError("checkpoint_lsn must identify the first CHECKPOINT record")
    return records


def restart_recovery(case: dict[str, Any]) -> dict[str, Any]:
    records = records_from_checkpoint(case)
    database = deepcopy(case["disk_at_crash"])
    undo_list = set(records[0].get("active", []))
    redo_trace: list[str] = []

    for record in records[1:]:
        record_type = record["type"]
        transaction = record.get("transaction")
        if record_type == "START":
            undo_list.add(transaction)
        elif record_type == "UPDATE":
            database[record["item"]] = record["new"]
            redo_trace.append(
                f"REDO LSN {record['lsn']} {transaction} {record['item']}={record['new']}"
            )
        elif record_type in {"COMMIT", "ABORT"}:
            undo_list.discard(transaction)

    incomplete_after_redo = sorted(undo_list)
    undo_trace: list[str] = []
    compensation_records: list[dict[str, Any]] = []
    for record in reversed(records[1:]):
        transaction = record.get("transaction")
        if transaction not in undo_list:
            continue
        if record["type"] == "UPDATE":
            database[record["item"]] = record["old"]
            undo_trace.append(
                f"UNDO LSN {record['lsn']} {transaction} {record['item']}={record['old']}"
            )
            compensation_records.append(
                {
                    "type": "REDO_ONLY",
                    "transaction": transaction,
                    "item": record["item"],
                    "value": record["old"],
                }
            )
        elif record["type"] == "START":
            compensation_records.append({"type": "ABORT", "transaction": transaction})
            undo_list.remove(transaction)
        if not undo_list:
            break

    return {
        "redo_trace": redo_trace,
        "incomplete_after_redo": incomplete_after_redo,
        "undo_trace": undo_trace,
        "generated_records": compensation_records,
        "final_database": database,
    }


def restore_from_backup(case: dict[str, Any]) -> dict[str, int]:
    database = deepcopy(case["archival_backup"])
    committed: set[str] = {
        record["transaction"]
        for record in case["committed_log_after_backup"]
        if record["type"] == "COMMIT"
    }
    for record in case["committed_log_after_backup"]:
        if record["type"] == "UPDATE" and record["transaction"] in committed:
            database[record["item"]] = record["new"]
    return database


def analyze(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "restart_recovery": restart_recovery(case),
        "backup_plus_committed_log": restore_from_backup(case),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "case_file",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("recovery_case.json"),
    )
    args = parser.parse_args()
    case = json.loads(args.case_file.read_text(encoding="utf-8"))
    print(json.dumps(analyze(case), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
