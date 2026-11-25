#!/usr/bin/env python3
"""Promote chunk-agent JSONL candidates after exact source-slice validation."""
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


def map_evidence(value: str) -> tuple[str, str]:
    value = (value or "").casefold()
    if "reported" in value or "metric" in value or "result" in value:
        return "reported_result", "source_reported"
    if "example" in value or "scenario" in value:
        return "example", "source_reported"
    if "hypothesis" in value:
        return "hypothesis", "hypothetical"
    if "inference" in value:
        return "inference", "inferred"
    return "direct_quote", "source_reported"


def read_sources(vault: Path) -> dict[str, dict[str, object]]:
    manifest = vault / "staging" / "manifests" / "raw_new_sources.jsonl"
    result = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        result[row["source_path"]] = row
    return result


def get_quote(row: dict[str, object]) -> tuple[str | None, int | None, int | None]:
    quote = row.get("evidence_quote") or row.get("exact_unicode_slice")
    start = row.get("evidence_start", row.get("slice_start"))
    end = row.get("evidence_end", row.get("slice_end"))
    if not isinstance(quote, str) or not isinstance(start, int) or not isinstance(end, int):
        return None, None, None
    return quote, start, end


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("/sdcard/NEXUS_LLM_WIKI"))
    parser.add_argument("--date", default=str(date.today()))
    args = parser.parse_args()
    sources = read_sources(args.vault)
    out_dir = args.vault / "claims"
    merged = []
    rejected = []
    for chunk in range(1, 5):
        path = args.vault / "staging" / "agent_outputs" / f"chunk_{chunk}.jsonl"
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            row = json.loads(line)
            source_path = normalize_path(str(row.get("source_path", "")))
            source = sources.get(source_path)
            quote, start, end = get_quote(row)
            if not source or quote is None:
                rejected.append({"chunk": chunk, "line": line_number, "id": row.get("claim_id") or row.get("id"), "reason": "source or exact evidence fields missing"})
                continue
            raw_path = args.vault / source_path
            if not raw_path.is_file():
                rejected.append({"chunk": chunk, "line": line_number, "id": row.get("claim_id") or row.get("id"), "reason": "raw source missing"})
                continue
            text = raw_path.read_text(encoding="utf-8", errors="replace")
            if start < 0 or end < start or text[start:end] != quote:
                rejected.append({"chunk": chunk, "line": line_number, "id": row.get("claim_id") or row.get("id"), "reason": "slice mismatch"})
                continue
            digest = hashlib.sha256(quote.encode("utf-8")).hexdigest()
            expected_digest = row.get("excerpt_sha256") or row.get("slice_sha256")
            if expected_digest and digest != expected_digest:
                rejected.append({"chunk": chunk, "line": line_number, "id": row.get("claim_id") or row.get("id"), "reason": "excerpt hash mismatch"})
                continue
            evidence_type, confidence = map_evidence(str(row.get("evidence_type", "")))
            identifier = row.get("claim_id") or row.get("id") or row.get("record_id")
            if not identifier:
                rejected.append({"chunk": chunk, "line": line_number, "reason": "missing id"})
                continue
            claim_id = f"CLM_NEW_{identifier}"
            statement = row.get("statement") or row.get("claim") or quote
            record = {
                "type": "claim", "claim_id": claim_id, "statement": statement,
                "evidence_type": evidence_type, "source_id": source["source_id"],
                "locator": f"line 1; chars {start}:{end} (Unicode, zero-based, end-exclusive)",
                "evidence_start": start, "evidence_end": end, "evidence_quote": quote,
                "excerpt_sha256": digest, "scope": row.get("scope", "نطاق المصدر فقط؛ لا تعميم خارج السياق."),
                "confidence": confidence, "status": "candidate", "created": args.date, "updated": args.date,
                "source_path": source_path,
            }
            out_file = out_dir / f"{claim_id}.md"
            body = ["---"]
            for key in ("type", "claim_id", "statement", "evidence_type", "source_id", "locator", "evidence_start", "evidence_end", "evidence_quote", "excerpt_sha256", "scope", "confidence", "status", "created", "updated"):
                value = record[key]
                body.append(f"{key}: {json.dumps(value, ensure_ascii=False) if isinstance(value, str) else value}")
            body.extend(["---", "", "## الدليل والحدود", "", "هذا Claim مرشح من دفعة agent. تم التحقق من أن النص المقتبس يطابق المصدر الخام حرفيًا وأن بصمة المقتطف صحيحة. لا تعني حالة `candidate` قبول الادعاء خارج المصدر.", "", f"المصدر: `{source_path}`.", ""])
            out_file.write_text("\n".join(body), encoding="utf-8")
            merged.append(record)
    result = {"merged": len(merged), "rejected": len(rejected), "rejected_rows": rejected}
    report = args.vault / "staging" / "agent_outputs" / "CHUNKS_MERGE_RESULT.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"merged": len(merged), "rejected": len(rejected)}, ensure_ascii=False, indent=2))
    return 0 if not rejected else 1


if __name__ == "__main__":
    raise SystemExit(main())
