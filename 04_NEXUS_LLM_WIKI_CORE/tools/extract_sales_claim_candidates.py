#!/usr/bin/env python3
"""Create auditable candidate Claim files for the first sales reading batch."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

VAULT = Path("/sdcard/NEXUS_LLM_WIKI")
MANIFEST = VAULT / "collections/sales/manifest.json"
OUT = VAULT / "collections/sales/claim_candidates"
CLAIMS = VAULT / "claims"
TRIGGERS = re.compile(
    r"sales|sell|selling|close|closing|lead|prospect|outreach|cold email|"
    r"discovery|objection|pricing|price|offer|funnel|pipeline|revenue|"
    r"مبيعات|بيع|عميل|عملاء|إيميل|اعتراض|إغلاق|قمع المبيعات|السعر|تسعير",
    re.I,
)
RESULTS = re.compile(r"\b\d+(?:[.,]\d+)?\s*%?|\$\s*\d+|EGP|MRR|revenue|result|clients? in|باع|عملاء", re.I)


def classify(quote: str) -> str:
    if RESULTS.search(quote):
        return "reported_result"
    if re.search(r"example|مثال|for instance|على سبيل", quote, re.I):
        return "example"
    return "direct_quote"


def sentences(text: str):
    # Works for transcripts stored as one very long line; offsets remain exact.
    for match in re.finditer(r"[^.!?؟\n]{35,600}(?:[.!?؟]|\n|$)", text):
        quote = match.group(0).strip()
        start = match.start() + (len(match.group(0)) - len(match.group(0).lstrip()))
        end = start + len(quote)
        if TRIGGERS.search(quote):
            yield start, end, quote


def yaml(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    created = []
    # First batch: enough to test the pipeline without claiming corpus completion.
    for index, item in enumerate(data["items"][:120], start=1):
        path = VAULT / item["path"]
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        found = list(sentences(text))[:4]
        for local, (start, end, quote) in enumerate(found, start=1):
            sid = item.get("source_id") or f"UNREGISTERED_{item['sha256'][:12]}"
            claim_id = f"CLM_SALES_BATCH1_{index:03d}_{local:02d}"
            claim_path = OUT / f"{claim_id}.md"
            evidence_hash = hashlib.sha256(quote.encode("utf-8")).hexdigest()
            evidence_type = classify(quote)
            claim_path.write_text(
                "---\n"
                f"type: claim\nclaim_id: {claim_id}\n"
                f"statement: {yaml('Candidate: the source states or discusses: ' + quote[:240])}\n"
                f"evidence_type: {evidence_type}\nsource_id: {sid}\n"
                f"source_path: {item['path']}\nlocator: {yaml(f'chars {start}:{end} (Unicode, zero-based, end-exclusive)')}\n"
                f"evidence_start: {start}\nevidence_end: {end}\n"
                f"evidence_quote: {yaml(quote)}\nexcerpt_sha256: sha256:{evidence_hash}\n"
                "scope: candidate extracted from sales triage batch; semantic scope requires review.\n"
                "confidence: source_reported\nstatus: candidate\n"
                "extraction_status: partial\nwhat_it_does_not_prove: Not a general benchmark, causal law, or promise.\n"
                "created: 2026-10-08\nupdated: 2026-10-08\n---\n\n"
                "## مراجعة مطلوبة\n\n"
                "هذا Claim مرشح آليًا. يجب أن يراجع مراجع بشري موضعه، ويعيد صياغة statement بما يطابق قوة النص، ويحدد المصدر/الجمهور/الشرط وما لا يثبته.\n",
                encoding="utf-8",
            )
            created.append({"claim_id": claim_id, "source_id": sid, "path": str(claim_path.relative_to(VAULT)), "evidence_type": evidence_type, "source_path": item["path"], "start": start, "end": end})
    (OUT / "README.md").write_text(
        "# مرشحو Claims — دفعة مبيعات 1\n\n"
        "هذه الملفات ناتجة عن استخراج آلي من أعلى 120 مرشحًا في manifest. حالتها candidate وpartial عمدًا؛ لا تُعامل كمعرفة مقبولة حتى تمر بالمراجعة الدلالية.\n\n"
        f"عدد الملفات: {len(created)}\n",
        encoding="utf-8",
    )
    (OUT / "index.json").write_text(json.dumps({"batch": "sales-1", "count": len(created), "claims": created}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"created": len(created), "out": str(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
