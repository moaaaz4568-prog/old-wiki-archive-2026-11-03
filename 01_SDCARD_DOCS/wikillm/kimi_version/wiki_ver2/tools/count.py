#!/usr/bin/env python3
"""count.py — تعداد الويكي بأوامر قابلة للتكرار.

الغرض: مصدر واحد للأرقام. يوفّر:
  --check          : يفحص كل رقم مذكور في الملفات对照 COUNTS.json ويوسم المخالف بـ⚠️
  --files          : عدّ الملفات بالبادئات
  --domains        : عدّ المجالات
  --coverage       : التغطية (%)
  --master         : عدّ الماسترات
  --terms          : عدّ المصطلحات

الاستخدام:
  python3 tools/count.py --check
  python3 tools/count.py --files
  python3 tools/count.py --coverage
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).parent.parent.resolve()


def count_files(base: Path) -> dict[str, int]:
    """عدّ الملفات بالبادئات (S/T/C/X/G/P/M/Y)."""
    counts = defaultdict(int)
    total = 0
    for p in base.rglob("*.md"):
        stem = p.stem
        parts = stem.split("_")
        if parts and parts[0] in "STCXGP MY" and len(parts[0]) == 1:
            counts[parts[0]] += 1
            total += 1
        # قبول صيغة C01-Name / M_Slug
        prefix = stem.split("-")[0] if "-" in stem else ""
        if re.fullmatch(r"[STCXGP MY]\d+", prefix) and prefix[0] in "STCXGP MY":
            counts[prefix[0]] += 1
            total += 1
        elif stem.startswith("M_"):
            counts["M"] += 1
            total += 1
        elif p.name == "INDEX.md":
            counts["I"] += 1
    return {"total": total, **counts}


def count_domains(base: Path) -> int:
    """عدّ المجالات (المجلدات التي تحتوي M_ أو MASTER أو INDEX.md + PLAYBOOKS/TERMS)."""
    domains = set()
    for p in base.rglob("*.md"):
        if p.name.upper().startswith("MASTER") or p.stem.startswith("M_"):
            domains.add(p.parent.name)
        if p.name == "INDEX.md":
            domains.add(p.parent.name)
        if p.parent.name in ("PLAYBOOKS", "TERMS"):
            domains.add(p.parent.parent.name)
    return len(domains)


def coverage_check(base: Path) -> dict:
    """حساب التغطية: نسبة الملفات المغطاة (M_ → C_ → T_)."""
    m_stars = set(p.stem for p in base.rglob("M_*.md"))
    c_links = set()
    for p in base.rglob("*.md"):
        c_links |= set(re.findall(r"\[\[C_[A-Za-z0-9_]+\]\]", p.read_text(errors="ignore")))
    return {"masters": len(m_stars), "concepts_linked": len(c_links)}


def check_counts() -> dict:
    """فحص كل رقم في الملفات对照 COUNTS.json."""
    counts_ref = ROOT / "COUNTS.json"
    if not counts_ref.exists():
        return {"error": "COUNTS.json غير موجود"}
    try:
        counts = json.load(open(counts_ref))
    except Exception:
        return {"error": "COUNTS.json تالف"}

    broken = []
    for p in ROOT.rglob("*.md"):
        text = p.read_text(errors="ignore")
        # استخراج كل رقم في سياق نسبة/عدد
        for match in re.finditer(r"(\d+(?:\.\d+)?)%?\s*(?:من|إلى|فقط|الحد الأدنى|أكبر من|أقل من)", text):
            num = match.group(1)
            if num not in str(counts):
                broken.append(f"{p}:{match.start()}")
    return {"broken": broken, "count": len(broken)}


def main():
    parser = argparse.ArgumentParser(description="تعداد الويكي")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("files")
    sub.add_parser("domains")
    sub.add_parser("coverage")
    args = parser.parse_args()

    if args.cmd == "check":
        res = check_counts()
        if "error" in res:
            print(f"خطأ: {res['error']}")
            sys.exit(1)
        print("broken:", res["count"])
        for b in res["broken"]:
            print("  ⚠️", b)
    elif args.cmd == "files":
        c = count_files(ROOT / "domains")
        print(json.dumps(c, ensure_ascii=False))
    elif args.cmd == "domains":
        print(count_domains(ROOT / "domains"))
    elif args.cmd == "coverage":
        print(json.dumps(coverage_check(ROOT / "domains"), ensure_ascii=False))


if __name__ == "__main__":
    main()
