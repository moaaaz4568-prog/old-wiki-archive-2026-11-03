#!/usr/bin/env python3
"""Build a provenance-preserving virtual sales collection from raw/new.

The raw corpus remains immutable. The collection stores paths, hashes, scores,
and generated indexes; it does not move or delete source files.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

VAULT = Path("/sdcard/NEXUS_LLM_WIKI")
RAW = VAULT / "raw/new"
SOURCES = VAULT / "sources"
OUT = VAULT / "collections/sales"

KEYWORDS = {
    "sales": 5, "sell": 5, "selling": 5, "closing": 5, "close": 3,
    "client": 3, "customer": 3, "prospect": 4, "lead": 4, "outreach": 4,
    "cold email": 5, "cold-email": 5, "appointment": 3, "discovery": 4,
    "objection": 4, "proposal": 3, "pricing": 3, "price": 2, "offer": 3,
    "funnel": 3, "conversion": 3, "revenue": 3, "pipeline": 3,
    "مبيعات": 5, "بيع": 5, "عميل": 4, "عملاء": 4, "ليد": 4,
    "اوتريتش": 4, "إيميل": 3, "سعر": 2, "تسعير": 3, "عرض": 2,
    "اعتراض": 4, "اغلاق": 5, "إغلاق": 5, "قمع المبيعات": 5,
}
HIGH_SIGNAL = {
    "sales", "sell", "selling", "closing", "prospect", "lead", "outreach",
    "cold email", "cold-email", "appointment", "discovery", "objection",
    "funnel", "pipeline", "مبيعات", "بيع", "عميل", "عملاء", "ليد",
    "اوتريتش", "إيميل", "اعتراض", "اغلاق", "إغلاق", "قمع المبيعات",
}
EXCLUDE = {"job application", "resume", "cv template", "hiring interview"}
TERM_PATTERNS = {
    "discovery": r"\bdiscovery\b|اكتشاف|تشخيص",
    "objection": r"\bobjection\w*\b|اعتراض",
    "closing": r"\bclos(?:e|ing|ed)\b|إغلاق|اغلاق",
    "cold_email": r"cold[ -]email|البريد البارد|إيميل بارد",
    "offer": r"\boffer\w*\b|عرض",
    "pricing": r"\bpricing\b|\bprice\b|تسعير|السعر",
    "funnel": r"\bfunnel\b|قمع المبيعات",
    "follow_up": r"follow[ -]?up|متابعة",
    "qualification": r"qualif\w*|تأهيل",
    "value": r"\bvalue\b|القيمة",
    "pain": r"\bpain\b|الألم|المشكلة",
}


def frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    out: dict[str, str] = {}
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z_]+):\s*[\"']?(.*?)[\"']?$", line)
        if match:
            out[match.group(1)] = match.group(2)
    return out


def source_lookup() -> dict[str, dict[str, str]]:
    result = {}
    for path in SOURCES.glob("*.md"):
        meta = frontmatter(path)
        if meta.get("source_id"):
            result[meta["source_id"]] = meta
    return result


def score_file(path: Path) -> tuple[int, Counter[str], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    haystack = f"{path.name}\n{text}".lower()
    score = 0
    hits: Counter[str] = Counter()
    for term, weight in KEYWORDS.items():
        count = haystack.count(term.lower())
        if count:
            score += weight * min(count, 5)
            hits[term] = count
    for blocked in EXCLUDE:
        if blocked in haystack:
            score -= 8
    return score, hits, text


def source_id_for(path: Path, lookup: dict[str, dict[str, str]]) -> tuple[str | None, dict[str, str]]:
    rel = str(path.relative_to(VAULT)).replace("\\", "/")
    for sid, meta in lookup.items():
        if meta.get("source_path") == rel:
            return sid, meta
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return None, {"content_hash": f"sha256:{digest}", "source_path": rel, "title": path.name}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lookup = source_lookup()
    rows = []
    terms: Counter[str] = Counter()
    for path in sorted(RAW.rglob("*")):
        if not path.is_file():
            continue
        try:
            score, hits, text = score_file(path)
        except OSError:
            continue
        high_hits = sum(1 for term in HIGH_SIGNAL if term.lower() in f"{path.name}\n{text}".lower())
        filename_high = sum(1 for term in HIGH_SIGNAL if term.lower() in path.name.lower())
        # Generic marketing vocabulary (offer/value/price) is insufficient by itself.
        if score < 5 or (high_hits == 0 and filename_high == 0):
            continue
        sid, meta = source_id_for(path, lookup)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        tier = "strong" if filename_high or high_hits >= 2 else "possible"
        for term, pattern in TERM_PATTERNS.items():
            if re.search(pattern, text, flags=re.I):
                terms[term] += 1
        rows.append({
            "source_id": sid,
            "title": meta.get("title", path.name),
            "path": str(path.relative_to(VAULT)).replace("\\", "/"),
            "sha256": digest,
            "bytes": path.stat().st_size,
            "score": score,
            "tier": tier,
            "keyword_hits": dict(hits),
            "source_record": str((SOURCES / f"{sid}.md").relative_to(VAULT)) if sid else None,
            "reading_status": "candidate_for_full_read",
        })
    rows.sort(key=lambda item: (-item["score"], item["path"]))
    now = datetime.now(timezone.utc).isoformat()
    manifest = {
        "collection_id": "COLL_SALES_20261008",
        "generated_at": now,
        "scope": "sales, outreach, offers, pricing, discovery, closing, follow-up",
        "selection_method": "high-signal sales terms plus weighted keyword score over filename + full UTF-8 text; candidate triage only",
        "raw_policy": "raw/new remains immutable; entries are virtual references",
        "counts": {"all_candidates": len(rows), "strong": sum(r["tier"] == "strong" for r in rows), "possible": sum(r["tier"] == "possible" for r in rows), "weak": sum(r["tier"] == "weak" for r in rows)},
        "items": rows,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "term_inventory.json").write_text(json.dumps({"generated_at": now, "terms": terms.most_common()}, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT / "README.md").open("w", encoding="utf-8") as handle:
        handle.write("# مجموعة مصادر المبيعات\n\n")
        handle.write("هذه مجموعة افتراضية لا تنقل ولا تعدل raw. الملف canonical هو `manifest.json`، وكل عنصر يحفظ المسار والبصمة وسبب الترشيح.\n\n")
        handle.write(f"- تاريخ البناء: `{now}`\n- عدد المرشحين: **{len(rows)}**\n- قوي: **{manifest['counts']['strong']}**\n- محتمل: **{manifest['counts']['possible']}**\n- ضعيف يحتاج مراجعة: **{manifest['counts']['weak']}**\n\n")
        handle.write("## قاعدة القراءة\n\nالترشيح الآلي ليس حكم صلة نهائيًا. اقرأ المرشحين الأقوياء، ثم راجع المحتملين، وسجّل استبعاد الضعفاء بدل حذفهم. لا تستخدم score كدليل معرفي.\n")
    print(json.dumps({"manifest": str(OUT / "manifest.json"), "counts": manifest["counts"], "terms": terms.most_common()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
