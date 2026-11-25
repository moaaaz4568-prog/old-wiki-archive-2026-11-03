#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nexus_rag.py — بحث بسيط في الويكي (استعلام بالمصطلح أو القسم).

يعيد مقاطع (snippets) مع الملف والسطر — بلا شبكة، بلا توكنات، stdlib فقط.

الاستخدام:
  python3 tools/nexus_rag.py "cold email"
  python3 tools/nexus_rag.py "ماستر" --root /path/to/wiki
  python3 tools/nexus_rag.py "حدود الفناء" --context 2
"""

import argparse
import os
import sys

DEFAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {".git", "TRASH", "__pycache__", "node_modules"}


def iter_md_files(root):
    """os.walk فقط — لا glob (المجلدات الكبيرة تكسر ARG_MAX)."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def search(query, root, context=1, max_hits=50):
    """بحث سطري: يعيد (ملف، رقم السطر، الأسطر المطابقة مع سياقها)."""
    hits = []
    needle = query.lower()
    for path in iter_md_files(root):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            if needle in line.lower():
                start = max(0, i - context)
                end = min(len(lines), i + context + 1)
                snippet = "".join(
                    "%s: %s" % (j + 1, lines[j].rstrip("\n"))
                    for j in range(start, end)
                )
                hits.append((os.path.relpath(path, root), i + 1, snippet))
                if len(hits) >= max_hits:
                    return hits
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description="بحث بالمصطلح في الويكي")
    ap.add_argument("query", help="المصطلح أو نص القسم المطلوب")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="جذر الويكي")
    ap.add_argument("--context", type=int, default=1,
                    help="أسطر السياق قبل/بعد المطابقة")
    ap.add_argument("--max-hits", type=int, default=50,
                    help="أقصى عدد نتائج")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        print("ERROR: الجذر غير موجود: %s" % args.root, file=sys.stderr)
        return 2

    hits = search(args.query, args.root, args.context, args.max_hits)
    if not hits:
        print("لا نتائج لـ «%s» في %s" % (args.query, args.root))
        return 1

    print("النتائج لـ «%s» — %d مطابقة (حد أقصى %d):"
          % (args.query, len(hits), args.max_hits))
    print("=" * 70)
    for rel, lineno, snippet in hits:
        print("%s:%d" % (rel, lineno))
        print("-" * 70)
        print(snippet)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
