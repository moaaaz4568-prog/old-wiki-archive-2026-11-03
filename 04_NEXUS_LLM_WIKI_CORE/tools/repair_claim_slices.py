#!/usr/bin/env python3
"""Repair only evidence serialization drift for explicitly listed claims."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path("/sdcard/NEXUS_LLM_WIKI")
TARGETS = {
    "CLM_CURATED_CONTENT_POSITIONING_003.md",
    "CLM_CURATED_SALES_006.md",
    "CLM_CURATED_SALES_019.md",
}


def field(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(.*)$", text, re.M)
    value = match.group(1).strip()
    return json.loads(value) if value.startswith('"') else value


def replace_field(text: str, name: str, value: object) -> str:
    rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, str) else str(value)
    return re.sub(rf"^{re.escape(name)}:\s*.*$", f"{name}: {rendered}", text, count=1, flags=re.M)


sources = {}
for line in (ROOT / "staging/manifests/raw_new_sources.jsonl").read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    sources[row["source_id"]] = row["source_path"]

for filename in TARGETS:
    path = ROOT / "claims" / filename
    text = path.read_text(encoding="utf-8")
    source_path = sources[field(text, "source_id")]
    raw = (ROOT / source_path).read_text(encoding="utf-8", errors="replace")
    start = int(field(text, "evidence_start"))
    end = int(field(text, "evidence_end"))
    quote = raw[start:end]
    text = replace_field(text, "evidence_quote", quote)
    text = replace_field(text, "evidence_end", start + len(quote))
    text = replace_field(text, "excerpt_sha256", hashlib.sha256(quote.encode("utf-8")).hexdigest())
    path.write_text(text, encoding="utf-8")
    print(filename, start, start + len(quote))
