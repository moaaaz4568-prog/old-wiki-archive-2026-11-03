#!/usr/bin/env python3
"""Promote verified staging report candidates into traceable Claim/Concept drafts."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


def frontmatter(fields: list[tuple[str, object]]) -> str:
    lines = ["---"]
    for key, value in fields:
        if isinstance(value, (list, dict)) or value is None:
            rendered = json.dumps(value, ensure_ascii=False)
        elif isinstance(value, str):
            rendered = json.dumps(value, ensure_ascii=False)
        else:
            rendered = str(value)
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines)


def path_key(raw: str) -> str:
    marker = "/raw/new/"
    if marker in raw:
        return "raw/new/" + raw.split(marker, 1)[1]
    return raw.replace("/sdcard/NEXUS_LLM_WIKI/", "")


def block_sections(text: str, pattern: str) -> list[str]:
    starts = list(re.finditer(pattern, text, re.M))
    return [text[m.start() : (starts[i + 1].start() if i + 1 < len(starts) else len(text))] for i, m in enumerate(starts)]


def field(block: str, label: str) -> str | None:
    match = re.search(rf"^- \*\*{re.escape(label)}[^:]*:\*\*\s*(.*)$", block, re.M)
    return match.group(1).strip() if match else None


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if len(value) >= 2 and value[0] in "`“\"" and value[-1] in "`”\"":
        value = value[1:-1]
    return value


def parse_offsets(value: str | None) -> tuple[int, int] | None:
    if not value:
        return None
    m = re.search(r"start\s*=\s*(\d+)\s*,?\s*end\s*=\s*(\d+)", value)
    if not m:
        m = re.search(r"(?:chars|Unicode offset).*?`?(\d+)\s*[:;,]\s*(\d+)", value)
    if not m:
        m = re.search(r"`(\d+)\s*,\s*(\d+)`", value)
    return (int(m.group(1)), int(m.group(2))) if m else None


def map_type(raw: str | None, quote: str) -> tuple[str, str]:
    value = (raw or "").casefold()
    if any(word in value for word in ("quant", "metric", "benchmark", "case", "result", "reported")):
        return "reported_result", "source_reported"
    if any(word in value for word in ("scenario", "example", "story")):
        return "example", "source_reported"
    return "direct_quote", "source_reported"


def load_sources(vault: Path) -> dict[str, dict[str, object]]:
    result = {}
    manifest = vault / "staging" / "manifests" / "raw_new_sources.jsonl"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        result[row["source_path"]] = row
    return result


def add_claim(claims: list[dict[str, object]], row: dict[str, object], prefix: str, number: str, statement: str, raw_type: str, quote: str, offsets: tuple[int, int], scope: str, source_map: dict[str, dict[str, object]], vault: Path) -> None:
    source_path = path_key(str(row["source_path"]))
    source = source_map.get(source_path)
    if not source:
        return
    raw_path = vault / source_path
    text = raw_path.read_text(encoding="utf-8", errors="replace")
    start, end = offsets
    if text[start:end] != quote:
        found = text.find(quote)
        if found < 0:
            return
        start, end = found, found + len(quote)
    evidence_type, confidence = map_type(raw_type, quote)
    claim_id = f"CLM_NEW_{prefix}_{int(number):03d}"
    claims.append({"claim_id": claim_id, "statement": statement, "evidence_type": evidence_type, "source_id": source["source_id"], "source_path": source_path, "locator": f"line 1; chars {start}:{end} (Unicode, zero-based, end-exclusive)", "evidence_start": start, "evidence_end": end, "evidence_quote": quote, "excerpt_sha256": hashlib.sha256(quote.encode("utf-8")).hexdigest(), "scope": scope or "نطاق المصدر كما يرد في التفريغ؛ لا تعميم خارج هذا السياق.", "confidence": confidence, "status": "candidate"})


def parse_sales(text: str, source_map: dict[str, dict[str, object]], vault: Path) -> list[dict[str, object]]:
    claims = []
    for block in block_sections(text, r"^### Claim \d+ —"):
        m = re.search(r"^### Claim (\d+)", block, re.M)
        candidate = field(block, "claim_candidate") or "المصدر يذكر هذا المبدأ أو النتيجة."
        source_path = clean_value(field(block, "source_path"))
        quote = clean_value(field(block, "exact_quote (verbatim)"))
        offsets = parse_offsets(field(block, "Unicode offsets"))
        if m and source_path and quote and offsets:
            add_claim(claims, {"source_path": source_path}, "SALES", m.group(1), candidate, field(block, "evidence_type") or "direct_quote", quote, offsets, "مقتطف من مصدر مبيعات/عرض؛ النطاق والنتيجة يظلان منسوبين للمصدر.", source_map, vault)
    return claims


def parse_cold(text: str, source_map: dict[str, dict[str, object]], vault: Path) -> list[dict[str, object]]:
    claims = []
    table = False
    for line in text.splitlines():
        if line.startswith("| C01"):
            table = True
        if not table or not line.startswith("| C"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        num = re.search(r"(\d+)", cells[0])
        quote = cells[1].strip("“”\"")
        source_path = cells[2].strip("`")
        offsets = parse_offsets(cells[3])
        if num and offsets:
            add_claim(claims, {"source_path": source_path}, "COLD", num.group(1), f"ينص مصدر البريد البارد على: {quote}", cells[4], quote, offsets, "نصيحة أو نتيجة في سياق البريد البارد/التسليم/التوليد؛ الأرقام لا تصبح benchmark تلقائيًا.", source_map, vault)
    return claims


def parse_content(text: str, source_map: dict[str, dict[str, object]], vault: Path) -> list[dict[str, object]]:
    claims = []
    for block in block_sections(text, r"^### C\d+ —"):
        m = re.search(r"^### C(\d+)", block, re.M)
        statement = field(block, "statement") or "المصدر يذكر هذا الإطار أو التوصية."
        source_line = field(block, "source") or ""
        source_path = source_line.split(" — ", 1)[-1].strip().strip("`")
        quote = clean_value(field(block, "quote"))
        offsets = parse_offsets(field(block, "locator"))
        if m and source_path and quote and offsets:
            add_claim(claims, {"source_path": source_path}, "CONTENT", m.group(1), statement, field(block, "evidence_type") or "direct_quote", quote, offsets, field(block, "scope / limitation") or "نطاق المصدر؛ لا تعميم خارج المنصة/السياق الموصوف.", source_map, vault)
    return claims


def write_claim(vault: Path, claim: dict[str, object]) -> None:
    body = [frontmatter([(key, claim[key]) for key in ("type", "claim_id", "statement", "evidence_type", "source_id", "locator", "evidence_start", "evidence_end", "evidence_quote", "excerpt_sha256", "scope", "confidence", "status", "created", "updated")]), "", "## الدليل والحدود", "", "هذا Claim مرشح استخرج من تقرير وكيل بعد التحقق من تطابق المقتطف مع المصدر الخام. لا يعني `candidate` قبول الادعاء أو صحة النتيجة خارج المصدر.", "", f"المصدر: `{claim['source_path']}`.", ""]
    (vault / "claims" / f"{claim['claim_id']}.md").write_text("\n".join(body), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("/sdcard/NEXUS_LLM_WIKI"))
    parser.add_argument("--date", default=str(date.today()))
    args = parser.parse_args()
    source_map = load_sources(args.vault)
    reports = args.vault / "staging" / "agent_outputs"
    claims = []
    claims.extend(parse_sales((reports / "retry_sales.md").read_text(encoding="utf-8"), source_map, args.vault))
    claims.extend(parse_cold((reports / "retry_cold_email.md").read_text(encoding="utf-8"), source_map, args.vault))
    claims.extend(parse_content((reports / "retry_content_brand.md").read_text(encoding="utf-8"), source_map, args.vault))
    seen = set()
    for claim in claims:
        if claim["claim_id"] in seen:
            continue
        seen.add(claim["claim_id"])
        claim["type"] = "claim"
        claim["created"] = args.date
        claim["updated"] = args.date
        write_claim(args.vault, claim)
    output = {"claims_written": len(seen), "source_map": len(source_map), "duplicate_claim_ids": len(claims) - len(seen)}
    (reports / "MERGE_RESULT.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
