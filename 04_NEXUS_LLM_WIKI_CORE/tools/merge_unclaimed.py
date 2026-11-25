#!/usr/bin/env python3
"""Merge unclaimed-agent JSONL into candidate Claims after exact validation."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


def normalize_path(value: str) -> str:
    value = value.strip().strip("`")
    marker = "/raw/new/"
    if marker in value:
        return "raw/new/" + value.split(marker, 1)[1]
    return value


def sources(vault: Path) -> dict[str, dict[str, object]]:
    result = {}
    for line in (vault / "staging/manifests/raw_new_sources.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        result[row["source_path"]] = row
    return result


def get(row: dict[str, object], *keys: str) -> object:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def evidence(value: object) -> tuple[str, str]:
    text = str(value or "").casefold()
    if "reported" in text or "result" in text or "metric" in text:
        return "reported_result", "source_reported"
    if "example" in text or "scenario" in text:
        return "example", "source_reported"
    if "hypothesis" in text:
        return "hypothesis", "hypothetical"
    if "inference" in text:
        return "inference", "inferred"
    return "direct_quote", "source_reported"


def write_claim(vault: Path, record: dict[str, object]) -> None:
    fields = ("type", "claim_id", "statement", "evidence_type", "source_id", "locator", "evidence_start", "evidence_end", "evidence_quote", "excerpt_sha256", "scope", "confidence", "status", "created", "updated")
    lines = ["---"]
    for key in fields:
        value = record[key]
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False) if isinstance(value, str) else value}")
    lines.extend(["---", "", "## الدليل والحدود", "", "Claim مرشح من دفعة agent. تم التحقق من تطابق المقتطف مع المصدر الخام وبصمة المقتطف. الحالة `candidate` لا تعني قبول الادعاء خارج المصدر.", "", f"المصدر: `{record['source_path']}`.", ""])
    (vault / "claims" / f"{record['claim_id']}.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("/sdcard/NEXUS_LLM_WIKI"))
    parser.add_argument("--date", default=str(date.today()))
    args = parser.parse_args()
    source_map = sources(args.vault)
    merged: list[str] = []
    rejected: list[dict[str, object]] = []
    notes = 0
    input_paths = [(2, args.vault / "staging/agent_outputs/unclaimed_2.jsonl"), (3, args.vault / "staging/agent_outputs/unclaimed_3.jsonl"), (4, args.vault / "staging/agent_outputs/unclaimed_4.jsonl"), (1, args.vault / "staging/agent_outputs/U1AUTO.jsonl")]
    for chunk, path in input_paths:
        if not path.is_file():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            row = json.loads(line)
            source_path = normalize_path(str(row.get("source_path", "")))
            source = source_map.get(source_path)
            identifier = str(get(row, "claim_id", "id", "record_id") or f"U{chunk}_{line_number:03d}")
            if "source_note" in row or row.get("record_type") == "source_note":
                notes += 1
                continue
            quote = get(row, "evidence_quote", "exact_unicode_slice")
            start = get(row, "evidence_start", "slice_start")
            end = get(row, "evidence_end", "slice_end")
            if not source or not isinstance(quote, str) or not isinstance(start, int) or not isinstance(end, int):
                rejected.append({"chunk": chunk, "line": line_number, "id": identifier, "reason": "missing source or evidence fields"})
                continue
            raw_path = args.vault / source_path
            if not raw_path.is_file():
                rejected.append({"chunk": chunk, "line": line_number, "id": identifier, "reason": "raw source missing"})
                continue
            text = raw_path.read_text(encoding="utf-8", errors="replace")
            if start < 0 or end < start or text[start:end] != quote:
                rejected.append({"chunk": chunk, "line": line_number, "id": identifier, "reason": "slice mismatch"})
                continue
            digest = hashlib.sha256(quote.encode("utf-8")).hexdigest()
            expected = get(row, "excerpt_sha256", "slice_sha256")
            if expected and digest != expected:
                rejected.append({"chunk": chunk, "line": line_number, "id": identifier, "reason": "excerpt hash mismatch"})
                continue
            evidence_type, confidence = evidence(row.get("evidence_type"))
            statement = get(row, "statement", "claim") or quote
            record = {
                "type": "claim", "claim_id": f"CLM_NEW_{identifier}", "statement": statement,
                "evidence_type": evidence_type, "source_id": source["source_id"],
                "locator": f"line 1; chars {start}:{end} (Unicode, zero-based, end-exclusive)",
                "evidence_start": start, "evidence_end": end, "evidence_quote": quote,
                "excerpt_sha256": digest, "scope": get(row, "scope") or "نطاق المصدر فقط؛ لا تعميم خارج السياق.",
                "confidence": confidence, "status": "candidate", "created": args.date, "updated": args.date,
                "source_path": source_path,
            }
            write_claim(args.vault, record)
            merged.append(record["claim_id"])
    result = {"merged": len(merged), "notes_skipped": notes, "rejected": len(rejected), "rejected_rows": rejected}
    (args.vault / "staging/agent_outputs/UNCLAIMED_MERGE_RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"merged": len(merged), "notes_skipped": notes, "rejected": len(rejected)}, ensure_ascii=False, indent=2))
    return 0 if not rejected else 1


if __name__ == "__main__":
    raise SystemExit(main())
