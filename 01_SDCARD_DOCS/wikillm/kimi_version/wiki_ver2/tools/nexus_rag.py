#!/usr/bin/env python3
"""nexus_rag — بحث بالمصطلح/القسم عبر grep ذكي، استرجاع مقاطع.

الغرض: البحث في الويكي (domains/ + systems/) بمصطلح أو قسم، إرجاع النتائج
بترتيب الأهم (systems أولاً، ثم domains/MASTER، ثم المصطلحات).

الاستخدام:
  python3 tools/nexus_rag.py "cold email"
  python3 tools/nexus_rag.py "حدّ الفناء" --section
  python3 tools/nexus_rag.py "Pattern Interrupt" --exact
"""

import argparse
import os
import re
import sys
from pathlib import Path


def search(root: Path, query: str, exact: bool = False, section: bool = False) -> list[tuple[Path, int, str]]:
    """إرجاع قائمة (ملف، سطر، نص) مرتّبة بالأهم."""
    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    files = list(root.rglob("*.md"))
    # ترتيب الأهمية: systems/ أولاً، ثم domains/*/MASTER*، ثم البقية
    files.sort(key=lambda p: (0 if "systems/" in str(p) else 1,
                              0 if p.name.upper().startswith("MASTER") else 1,
                              p))
    for p in files:
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if exact:
                if line.strip() == query or re.match(rf"^{re.escape(query)}", line.strip()):
                    results.append((p, i, line.strip()))
            elif section:
                if line.strip().startswith("##") or "§" in line:
                    results.append((p, i, line.strip()))
            elif pattern.search(line):
                results.append((p, i, line.strip()))
    return results


def main():
    parser = argparse.ArgumentParser(description="ابحث في ويكي Nexus")
    parser.add_argument("query", help="المصطلح أو القسم")
    parser.add_argument("--exact", "-e", action="store_true", help="مطابقة حرفية")
    parser.add_argument("--section", "-s", action="store_true", help="فقط العناوين")
    parser.add_argument("--max", "-n", type=int, default=30, help="أقصى عدد نتائج")
    args = parser.parse_args()

    root = Path(__file__).parent.parent.resolve()
    results = search(root, args.query, args.exact, args.section)

    if not results:
        print("لا نتائج.")
        sys.exit(0)

    seen = set()
    printed = 0
    for path, line_no, line in results[: args.max]:
        key = (path, line_no)
        if key in seen:
            continue
        seen.add(key)
        rel = path.relative_to(root)
        print(f"\n[{rel}:{line_no}]")
        print(line)
        printed += 1
        if printed >= args.max:
            break

    print(f"\n--- {printed} نتيجة ---")


if __name__ == "__main__":
    main()
