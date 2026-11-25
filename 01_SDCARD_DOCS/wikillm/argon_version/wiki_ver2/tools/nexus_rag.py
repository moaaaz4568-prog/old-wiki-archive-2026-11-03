#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nexus_rag.py — اداة استرجاع معرفي ذكية وسريعة تعمل بالمكتبة القياسية فقط (stdlib).
الوظيفة: البحث بالمصطلح واسترجاع المقاطع السياقية ومسارات الملفات وارقام الاسطر.
"""

import argparse
import os
import re
import sys

DEFAULT_ROOTS = [
    "/sdcard/wikillm/argon_version/wiki_ver2",
    "/sdcard/Nexus_Brain/Nexus_Brain/brain",
]
DEFAULT_EXTS = (".md", ".txt")


def iter_candidate_files(roots, exts):
    """يمشي عبر المجلدات المحددة ويعيد مسارات الملفات الصالحة بترتيب ملائم."""
    for root in roots:
        if not os.path.exists(root):
            continue
        if os.path.isfile(root):
            yield root
            continue
        # فرز الملفات لتقديم الملفات الأقرب والأنسب
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for filename in sorted(filenames):
                if filename.startswith("."):
                    continue
                if exts and not filename.lower().endswith(tuple(exts)):
                    continue
                yield os.path.join(dirpath, filename)


def calculate_match_score(line, query_lower):
    """تقييم ذكي لقوة تطابق السطر مع عبارة البحث."""
    line_lower = line.lower()
    if query_lower not in line_lower:
        return 0
    score = 10
    pattern = r"\b" + re.escape(query_lower) + r"\b"
    word_matches = len(re.findall(pattern, line_lower))
    score += word_matches * 5
    if line.strip().startswith("#"):
        score += 8
    return score


def search_rag(query, roots=DEFAULT_ROOTS, context=2, max_results=10, exts=DEFAULT_EXTS):
    """تنفيذ البحث واستخراج المقاطع السياقية المصحوبة بالمسار والسطر."""
    results = []
    query_lower = query.lower()

    for filepath in iter_candidate_files(roots, exts):
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError:
            continue

        for idx, line in enumerate(lines, start=1):
            score = calculate_match_score(line, query_lower)
            if score > 0:
                start_line = max(1, idx - context)
                end_line = min(len(lines), idx + context)
                snippet_lines = lines[start_line - 1:end_line]
                snippet = " ".join(s.strip() for s in snippet_lines if s.strip())
                # تقليص المقطع السياقي لطول عملي ومقروء
                if len(snippet) > 280:
                    snippet = snippet[:277] + "..."
                results.append({
                    "path": filepath,
                    "line": idx,
                    "score": score,
                    "snippet": snippet,
                })
                # اذا جمعنا نتائج وفيرة ذات درجات عالية نكتفي لتسريع الاداء
                if len(results) >= max_results * 5:
                    break
        if len(results) >= max_results * 5:
            break

    results.sort(key=lambda r: (-r["score"], r["path"], r["line"]))
    return results[:max_results]


def main():
    # معالجة اغلاق الانبوب (BrokenPipeError) عند التمرير لـ head
    try:
        parser = argparse.ArgumentParser(description="nexus_rag — اداة الاسترجاع المعرفي الذكي")
        parser.add_argument("query", nargs="?", default="cold email", help="عبارة او مصطلح البحث")
        parser.add_argument("--roots", nargs="*", default=DEFAULT_ROOTS, help="جذور البحث على القرص")
        parser.add_argument("--context", type=int, default=2, help="عدد اسطر السياق المحيطة")
        parser.add_argument("--max", type=int, default=10, help="الحد الاقصى لعدد النتائج")
        parser.add_argument("--exts", nargs="*", default=list(DEFAULT_EXTS), help="الامتدادات المفحوصة")

        args = parser.parse_args()

        results = search_rag(
            query=args.query,
            roots=args.roots,
            context=args.context,
            max_results=args.max,
            exts=args.exts,
        )

        if not results:
            print(f"لم يتم العثور على نتائج تطابق: «{args.query}»")
            sys.exit(1)

        for i, r in enumerate(results, 1):
            print(f"[{i}] {r['path']}:{r['line']} (درجة: {r['score']})")
            print(f"    {r['snippet']}")

    except BrokenPipeError:
        try:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
        except OSError:
            pass
        sys.exit(0)


if __name__ == "__main__":
    main()
