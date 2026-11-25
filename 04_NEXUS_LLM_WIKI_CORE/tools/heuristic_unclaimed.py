#!/usr/bin/env python3
"""Conservative fallback extraction for files whose agent pass was unavailable."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path


KEYWORDS = re.compile(r"(?i)(sales|sale|client|customer|offer|price|pricing|content|brand|story|social|agency|business|email|lead|marketing|مبيعات|بيع|عميل|عرض|سعر|محتوى|براند|قصة|وكالة|بزنس|تسويق|مشكلة|حل)")
RESULTS = re.compile(r"(?i)(\$|دولار|جنيه|\d+%|\d+\s*(?:clients?|customers?|meetings?|views?|followers?|دولار|جنيه|عميل|مشاهدة|متابع))")


def source_map(vault: Path) -> dict[str, dict[str, object]]:
    result = {}
    for line in (vault / "staging/manifests/raw_new_sources.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        result[row["source_path"]] = row
    return result


def choose(text: str) -> tuple[str, int, int] | None:
    # Prefer a complete sentence containing a topical keyword, not a title/intro slice.
    sentences = list(re.finditer(r"[^.!?؟\n]{40,900}[.!?؟]", text))
    ranked = []
    for match in sentences:
        quote = match.group(0).strip()
        if len(quote) < 60 or not KEYWORDS.search(quote):
            continue
        penalty = 0 if match.start() > 300 else 2
        result_bonus = -1 if RESULTS.search(quote) else 0
        ranked.append((penalty + result_bonus, -min(len(quote), 500), match.start(), quote))
    if not ranked:
        return None
    _, _, start, quote = sorted(ranked)[0]
    # Recover exact whitespace-preserving slice.
    raw_start = text.find(quote, start)
    return quote, raw_start, raw_start + len(quote)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("/sdcard/NEXUS_LLM_WIKI"))
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--prefix", default="U1AUTO")
    parser.add_argument("--date", default=str(date.today()))
    args = parser.parse_args()
    sm = source_map(args.vault)
    rows = []
    notes = []
    for idx, raw_line in enumerate(args.input.read_text(encoding="utf-8").splitlines(), 1):
        source_path = Path(raw_line).relative_to(args.vault).as_posix()
        source = sm.get(source_path)
        if not source:
            notes.append({"source_path": source_path, "reason": "missing Source record"})
            continue
        text = (args.vault / source_path).read_text(encoding="utf-8", errors="replace")
        chosen = choose(text)
        claim_id = f"{args.prefix}_{idx:03d}"
        if not chosen:
            notes.append({"claim_id": claim_id, "source_path": source_path, "source_note": "لم يُعثر على جملة موضوعية مكتملة؛ لم يُخترع Claim.", "status": "candidate"})
            continue
        quote, start, end = chosen
        evidence_type = "reported_result" if RESULTS.search(quote) else "direct_quote"
        rows.append({"claim_id": claim_id, "source_path": source_path, "statement": f"المصدر يذكر: {quote}", "evidence_type": evidence_type, "evidence_start": start, "evidence_end": end, "evidence_quote": quote, "scope": "اقتباس محافظ من ملف لم يتوفر له استخراج agent؛ لا يتجاوز ما يقوله المصدر.", "confidence": "source_reported", "status": "candidate", "excerpt_sha256": hashlib.sha256(quote.encode()).hexdigest(), "source_sha256": source["content_hash"]})
    out = args.vault / "staging/agent_outputs" / f"{args.prefix}.jsonl"
    out.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows + notes) + "\n", encoding="utf-8")
    report = {"input": len(args.input.read_text(encoding="utf-8").splitlines()), "claims": len(rows), "notes": len(notes), "output": str(out)}
    (out.with_name(out.stem + "_report.md")).write_text("# Heuristic fallback extraction\n\n```json\n" + json.dumps(report, ensure_ascii=False, indent=2) + "\n```\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
