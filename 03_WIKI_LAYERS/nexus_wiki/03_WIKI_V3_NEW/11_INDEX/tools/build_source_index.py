#!/usr/bin/env python3
"""build_source_index.py — فهرس مصادر الـbrain حسب القناة.

يعمل على: /root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/brain
يكتب:     /root/r/V3/07_SOURCES/SOURCE_INDEX.json
وضع: قراءة فقط على المصدر (لا نسخ · لا حذف · لا كتابة داخل NEXUS_GITHUB_PACKAGE).

تعريف «القناة» (Channel)
------------------------
تصدير TheBrain في هذا المجلد غير متجانس، فالقناة تُشتق من الشكل على القرص:
  1) مجلد داخل `brain/processed/`        ⇒ قناة باسم المجلد (مجلد قناة حقيقي)
  2) ملف منقول في جذر `brain/`            ⇒ قناة باسم البادئة قبل أول `__`
                                           (تصدير TheBrain يسمّي الملف `<القناة>__<العنوان>__<المعرّف>.txt`)
  3) ملف بلا `__` ⇒ قناة اصطناعية `_unfiled` (داخل processed/)
     أو `_root_unfiled` (جذر brain/)
  4) `brain/duplicates/` ⇒ قناة `duplicates`

تعريف «غير المستخرج» (unextracted)
-----------------------------------
ملف مصدر **لم يُدرَج** في أي حزمة استخراج `V3/03_WORK_BUNDLES/WB_*.txt`.
حزمة الاستخراج هي وحدها ما يُسلَّم لوكيل استخراج (PROMPT_TEMPLATE.md)،
فما ليس فيها = ما لم يدخل الاستخراج بعد. القياس حرفي: قراءة أسطر
`<عدد الكلمات>\t<مسار abs>` من كل WB_*.txt ثم مطابقة المسارات.

ملاحظة على `inventory_full.json`: غير موجود في التصدير (تحقّق بـ find على
`NEXUS_GITHUB_PACKAGE`) ⇒ الفهرس مبنيّ على مسح مباشر للقرص، لا على ملف جرد.

الاستعمال:
    python3 build_source_index.py
    python3 build_source_index.py --print
    python3 build_source_index.py --top 15
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

BRAIN_ROOT = Path("/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/brain")
V3_ROOT = Path("/root/r/V3")
OUT_PATH = V3_ROOT / "07_SOURCES" / "SOURCE_INDEX.json"
BUNDLE_DIR = V3_ROOT / "03_WORK_BUNDLES"

BUNDLE_LINE = re.compile(r"^\s*(\d+)\t(/[^\t].*)$")
SOURCE_EXTS = {".txt", ".srt", ".md"}


def channel_of(name: str) -> str:
    """اسم القناة لملف منقول: البادئة قبل أول `__`، وإلا `None`."""
    if "__" in name:
        return name.split("__", 1)[0]
    return None


def scan_bundles() -> tuple[set[str], int]:
    """(المسارات المدرجة، عدد الإجماليات) من كل WB_*.txt."""
    bundled: set[str] = set()
    entries = 0
    if not BUNDLE_DIR.is_dir():
        return bundled, entries
    for wb in sorted(BUNDLE_DIR.glob("WB_*.txt")):
        with wb.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = BUNDLE_LINE.match(line.rstrip("\n"))
                if m:
                    bundled.add(m.group(2))
                    entries += 1
    return bundled, entries


def scan_brain(bundled: set[str]) -> tuple[dict, dict]:
    channels: dict[str, dict] = {}

    def slot(name: str, kind: str, path: Path) -> None:
        ch = channels.setdefault(
            name,
            {
                "channel": name,
                "kind": kind,
                "path": str(path),
                "files": 0,
                "bytes": 0,
                "bundled": 0,
                "unextracted": 0,
            },
        )
        try:
            size = os.path.getsize(path)
        except OSError:
            size = 0
        ch["files"] += 1
        ch["bytes"] += size
        if str(path) in bundled:
            ch["bundled"] += 1
        else:
            ch["unextracted"] += 1

    # 1) مجلدات القنوات داخل processed/
    processed = BRAIN_ROOT / "processed"
    if processed.is_dir():
        for entry in sorted(os.listdir(processed)):
            p = processed / entry
            if p.is_dir():
                for root, _dirs, files in os.walk(p):
                    for f in sorted(files):
                        slot(entry, "channel_dir", Path(root) / f)
            elif p.is_file():
                # ملف منقول: قناة حسب البادئة أو _unfiled
                ch = channel_of(entry) or "_unfiled"
                slot(ch, "loose_processed", p)

    # 2) الملفات المنقولة في جذر brain/
    for entry in sorted(os.listdir(BRAIN_ROOT)):
        p = BRAIN_ROOT / entry
        if p.is_file():
            ch = channel_of(entry) or "_root_unfiled"
            slot(ch, "loose_root", p)

    # 3) duplicates/
    dup = BRAIN_ROOT / "duplicates"
    if dup.is_dir():
        for entry in sorted(os.listdir(dup)):
            p = dup / entry
            if p.is_file():
                slot("duplicates", "duplicates", p)

    totals = {
        "channels": len(channels),
        "files": sum(c["files"] for c in channels.values()),
        "bytes": sum(c["bytes"] for c in channels.values()),
        "bundled": sum(c["bundled"] for c in channels.values()),
        "unextracted": sum(c["unextracted"] for c in channels.values()),
    }
    return channels, totals


def main() -> int:
    ap = argparse.ArgumentParser(description="فهرس قنوات brain ← SOURCE_INDEX.json")
    ap.add_argument("--out", default=str(OUT_PATH))
    ap.add_argument("--print", dest="do_print", action="store_true")
    ap.add_argument("--top", type=int, default=0, help="اطبع أكبر N قناة")
    args = ap.parse_args()

    if not BRAIN_ROOT.is_dir():
        sys.exit(f"FATAL: brain root not found: {BRAIN_ROOT}")

    bundled, entries = scan_bundles()
    channels, totals = scan_brain(bundled)

    doc = {
        "schema": 1,
        "generator": "V3/11_INDEX/tools/build_source_index.py",
        "brain_root": str(BRAIN_ROOT),
        "bundle_dir": str(BUNDLE_DIR),
        "channel_rules": {
            "channel_dir": "مجلد داخل brain/processed/",
            "loose_root": "ملف في جذر brain/ — القناة = البادئة قبل أول __",
            "loose_processed": "ملف منقول داخل processed/ — القناة = البادئة أو _unfiled",
            "duplicates": "brain/duplicates/",
        },
        "unextracted_rule": "ملف غير مدرج في أي V3/03_WORK_BUNDLES/WB_*.txt ⇒ لم يدخل الاستخراج",
        "inventory_full_json": "غير موجود — الفهرس من مسح مباشر للقرص",
        "bundled_entries_in_bundles": entries,
        "bundled_distinct_paths": len(bundled),
        "totals": totals,
        "channels": {k: channels[k] for k in sorted(channels)},
    }

    payload = json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if args.do_print:
        print(payload, end="")
    else:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
        print(f"wrote {out}")

    t = totals
    print(
        f"channels={t['channels']} files={t['files']} bytes={t['bytes']} "
        f"bundled={t['bundled']} unextracted={t['unextracted']}"
    )

    if args.top:
        print("\n-- top channels by unextracted --")
        for name, c in sorted(channels.items(), key=lambda kv: -kv[1]["unextracted"])[: args.top]:
            print(f"  {name:<32} files={c['files']:<5} bytes={c['bytes']:<10} unextracted={c['unextracted']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())