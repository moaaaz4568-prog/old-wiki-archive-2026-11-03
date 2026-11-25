#!/usr/bin/env python3
"""audit.py — فحص القوالب والحدود والالتزام بالعقد.

الغرض: فحص شامل لكل ملف في domains/ + systems/ وفقاً للقواعد:
  - C01: البادئة (type / badge / مجلد)
  - C02: صيغة المعرّف <BADGE>_<Slug>.md
  - C04: الأقسام الإلزامية (Concept: 6 أقسام)
  - C11: النظافة (صفر TODO/TBD/XXX)
  - C15: فحص التلوث اللغوي (CJK)

الاستخدام:
  python3 tools/audit.py C01
  python3 tools/audit.py C04
  python3 tools/audit.py C15
  python3 tools/audit.py --all
"""

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent.resolve()
CJK = re.compile("[\u4e00-\u9fff]")


def check_badge(root: Path) -> list[str]:
    """C01: البادئة."""
    results = []
    for p in root.rglob("*.md"):
        if p.name.startswith("INDEX.md") or p.name.startswith("COUNTS"):
            continue
        # القوالب الفارغة (PLAYBOOK_TEMPLATE.md, TERMS_TEMPLATE.md, CONTINGENCY_MATRIX_TEMPLATE.md)
        if p.name.endswith("_TEMPLATE.md"):
            continue
        stem = p.stem
        prefix = None
        for sep in ("_", "-"):
            first = stem.split(sep)[0]
            if re.fullmatch(r"[STCXGP MY]\d*", first):
                prefix = first
                break
        if prefix and prefix[0] in "STCXGP MY":
            continue
        results.append(f"{p.stem}: بادئة غير معروفة ({prefix or stem.split('_')[0]})")
    return results


def check_format(root: Path) -> list[str]:
    """C02: صيغة المعرّف."""
    results = []
    for p in root.rglob("*.md"):
        if p.name.startswith("INDEX.md") or p.name.startswith("COUNTS"):
            continue
        stem = p.stem
        if "_" not in stem and "-" not in stem:
            results.append(f"{p.name}: لا يفصل بين البادئة والمعرّف")
        if "_" not in stem:
            prefix = stem.split("-")[0] if "-" in stem else ""
            if not re.fullmatch(r"[STCXGP MY]\d+", prefix):
                results.append(f"{p.stem}: صيغة المعرّف غير صحيحة")
    return results


def check_concept_sections(root: Path) -> list[str]:
    """C04: الأقسام الإلزامية للماستر (6 أقسام)."""
    required = [
        "## §1 TL;DR",
        "## §4 الآلية",
        "## §8 الجواهر",
        "## §13 الأرقام",
        "## §15 التحليل المستقل",
        "## §17 جدول المفاهيم",
    ]
    results = []
    for p in root.rglob("M_*.md"):
        text = p.read_text(errors="ignore")
        for req in required:
            if req not in text:
                results.append(f"{p.stem}: ناقص {req}")
    return results


def check_cleanliness(root: Path) -> list[str]:
    """C11: النظافة (TODO/TBD/XXX)."""
    results = []
    for p in root.rglob("*.md"):
        if p.name.startswith("INDEX.md") or p.name.startswith("COUNTS"):
            continue
        for kw in ("TODO", "TBD", "XXX"):
            if re.search(rf"[Tt]{kw}", p.read_text(errors="ignore")):
                results.append(f"{p.stem}: يحتوي {kw}")
    return results


def check_cjk(root: Path) -> list[str]:
    """C15: فحص التلوث اللغوي (CJK)."""
    results = []
    for p in root.rglob("*.md"):
        text = p.read_text(errors="ignore")
        matches = CJK.findall(text)
        if matches:
            results.append(f"{p.name}: {len(matches)} محارف CJK")
    return results


def main():
    parser = argparse.ArgumentParser(description="فحص الالتزام بالعقد")
    parser.add_argument("code", nargs="?", choices=["C01", "C02", "C04", "C11", "C15"],
                        help="كود الفحص")
    parser.add_argument("--all", action="store_true", help="كل الفحوصات")
    args = parser.parse_args()

    domains = ROOT / "domains"
    checks = {
        "C01": check_badge,
        "C02": check_format,
        "C04": check_concept_sections,
        "C11": check_cleanliness,
        "C15": check_cjk,
    }
    selected = {args.code: checks[args.code]} if args.code else checks
    total = 0
    for code, fn in selected.items():
        res = fn(domains)
        total += len(res)
        print(f"\n[{code}]: {len(res)} مشكلة")
        for r in res[:50]:
            print(f"  - {r}")

    print(f"\n--- إجمالي: {total} ---")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
