#!/usr/bin/env python3
"""Register every file under raw/new as a traceable source record.

This is ingestion, not semantic approval: agent-produced Claims remain candidate
until the quality gate and human-readable review promote them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


OPERATIONAL = {"01-setup-commands.md", "02-master-prompt.md", "README.txt", "all_usernames.txt"}
THEMES = {
    "sales": ("sales", "بيع", "مبيعات", "closing", "close", "client", "customer", "عميل", "زبون", "meeting", "مبيعات"),
    "outreach": ("cold", "outreach", "email", "linkedin", "lead", "prospect", "رسالة", "تواصل", "عملاء"),
    "offers_pricing": ("offer", "pricing", "price", "discount", "عرض", "سعر", "تسعير", "خصم"),
    "content": ("content", "video", "reels", "youtube", "tiktok", "instagram", "محتوى", "فيديو", "ريلز", "مشاهدات"),
    "branding": ("brand", "branding", "personal brand", "logo", "identity", "براند", "هوية", "شعار"),
    "agency_operations": ("agency", "operations", "system", "sop", "workflow", "وكالة", "اوبريشن", "سيستم"),
    "automation_ai": ("ai", "claude", "chatgpt", "n8n", "automation", "agent", "أتمتة", "ذكاء اصطناعي"),
    "storytelling": ("story", "storytelling", "hook", "script", "قصص", "قصة", "هوك", "سكريبت"),
}


def q(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def detect_language(text: str) -> str:
    arabic = len(re.findall(r"[\u0600-\u06ff]", text[:20000]))
    latin = len(re.findall(r"[A-Za-z]", text[:20000]))
    if arabic and latin:
        return "mixed"
    return "ar" if arabic else "en" if latin else "unknown"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("/sdcard/NEXUS_LLM_WIKI"))
    parser.add_argument("--date", default=str(date.today()))
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    raw = args.vault / "raw" / "new"
    source_dir = args.vault / "sources"
    manifest_dir = args.vault / "staging" / "manifests"
    source_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted(p for p in raw.rglob("*") if p.is_file() and p.suffix.lower() in {".txt", ".md", ".srt"})
    by_hash: dict[str, list[Path]] = defaultdict(list)
    rows = []
    for path in paths:
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        text = data.decode("utf-8", errors="replace")
        relative = path.relative_to(args.vault).as_posix()
        corpus = f"{path.name}\n{text[:30000]}".casefold()
        themes = [theme for theme, words in THEMES.items() if any(word.casefold() in corpus for word in words)]
        status = "quarantined" if path.name in OPERATIONAL else "processed"
        by_hash[digest].append(path)
        rows.append({"path": path, "relative": relative, "bytes": len(data), "sha256": digest, "text": text, "themes": themes, "status": status, "language": detect_language(text)})
    primary_by_hash = {digest: sorted(items)[0] for digest, items in by_hash.items()}
    manifest_rows = []
    for row in rows:
        primary = primary_by_hash[row["sha256"]]
        duplicate_of = None if row["path"] == primary else primary.relative_to(args.vault).as_posix()
        path_key = hashlib.sha256(row["relative"].encode("utf-8")).hexdigest()[:8]
        source_id = f"SRC_NEW_{row['sha256'][:16]}_{path_key}"
        title = row["path"].stem
        first = " ".join(row["text"].split())[:360]
        source_file = source_dir / f"{source_id}.md"
        body = [
            "---",
            "type: source",
            f"source_id: {q(source_id)}",
            f"title: {q(title)}",
            f"source_path: {q(row['relative'])}",
            f"content_hash: {q('sha256:' + row['sha256'])}",
            f"media_type: {q('transcript' if row['path'].suffix.lower() in {'.txt', '.srt'} else 'other')}",
            f"language: {q(row['language'])}",
            f"status: {q(row['status'])}",
            f"created: {q(args.date)}",
            f"updated: {q(args.date)}",
            f"themes: {q(row['themes'])}",
            f"bytes: {row['bytes']}",
            f"duplicate_of: {q(duplicate_of) if duplicate_of else 'null'}",
            "---",
            "",
            "## إدخال المصدر",
            "",
            f"هذا سجل إدخال آلي للملف `{row['relative']}`. لا يعني `processed` أن كل الادعاءات داخله مقبولة؛ Claims الدلالية تُربط لاحقًا بعد المراجعة.",
            "",
            f"**ملخص أولي غير تحليلي:** {first}",
            "",
            f"**التكرار:** {'نسخة مطابقة للمصدر ' + duplicate_of if duplicate_of else 'المسار الأول لهذه البصمة داخل raw/new.'}",
            "",
        ]
        manifest_rows.append({"source_id": source_id, "source_path": row["relative"], "content_hash": "sha256:" + row["sha256"], "bytes": row["bytes"], "language": row["language"], "status": row["status"], "themes": row["themes"], "duplicate_of": duplicate_of, "source_record": str(source_file.relative_to(args.vault))})
        if not args.no_write:
            source_file.write_text("\n".join(body), encoding="utf-8")
    if not args.no_write:
        manifest_path = manifest_dir / "raw_new_sources.jsonl"
        manifest_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in manifest_rows) + "\n", encoding="utf-8")
        summary = {
            "generated": args.date,
            "files": len(rows),
            "bytes": sum(row["bytes"] for row in rows),
            "unique_hashes": len(by_hash),
            "duplicate_files": sum(len(items) - 1 for items in by_hash.values()),
            "status_counts": {status: sum(row["status"] == status for row in rows) for status in {row["status"] for row in rows}},
            "theme_counts": {theme: sum(theme in row["themes"] for row in rows) for theme in THEMES},
        }
        (manifest_dir / "raw_new_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"files": len(rows), "bytes": sum(row["bytes"] for row in rows), "unique_hashes": len(by_hash)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
