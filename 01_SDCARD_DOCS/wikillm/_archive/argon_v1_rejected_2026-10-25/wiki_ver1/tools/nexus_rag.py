#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nexus_rag.py — أداة استرجاع (Retrieval) محلية بلا مكتبات خارجية (stdlib فقط).
الوظيفة: بحث ذكي بمصطلح داخل مجلد النسخة (أو مجلد مصادر خارجي اختياري)،
مع إرجاع المقاطع وأرقام الأسطر، ودعم السياق (Context Lines) والحد الأقصى للنتائج.

الاستخدام:
  python3 nexus_rag.py "cold email"                          # بحث في مجلد النسخة
  python3 nexus_rag.py "icebreaker" --root /sdcard/Nexus_Brain/Nexus_Brain/brain
  python3 nexus_rag.py "hook" --context 1 --max 5 --ext .md .txt
  python3 nexus_rag.py --selftest                            # اختبار ذاتي

القواعد: عربية فصحى + مصطلحات إنجليزية، صفر حرف صيني، لا حذف ولا تعديل ملفات — قراءة فقط.
"""
import argparse
import os
import re
import sys

CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
DEFAULT_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_EXTS = (".md", ".txt", ".tsv", ".py")


def iter_files(root, exts):
    """يمشي على الشجرة ويعيد مسارات الملفات المطابقة للامتدادات."""
    if os.path.isfile(root):
        yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            if exts and not name.lower().endswith(tuple(exts)):
                continue
            yield os.path.join(dirpath, name)


def smart_score(line, term):
    """تقييم ذكي للسطر: تطابق كلمة كاملة أقوى من تطابق جزئي، وتكرار يرفع الدرجة."""
    score = 0
    lowered = line.lower()
    t = term.lower()
    # تطابق كلمة كاملة (Word Boundary) — أدق دلالياً
    score += 3 * len(re.findall(r"\b" + re.escape(t) + r"\b", lowered))
    # تطابق جزئي (Substring) — يلتقط المشتقات
    score += 1 * lowered.count(t)
    return score


def search(root, term, context=2, max_results=20, exts=DEFAULT_EXTS, min_score=1):
    """بحث بالمصطلح: يعيد قائمة نتائج (ملف، سطر، درجة، مقطع)."""
    results = []
    for path in iter_files(root, exts):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
        except OSError:
            continue
        hits = []
        for idx, raw in enumerate(lines, start=1):
            s = smart_score(raw, term)
            if s >= min_score:
                hits.append((idx, s, raw.rstrip("\n")))
        if not hits:
            continue
        for idx, s, text in hits:
            start = max(1, idx - context)
            end = min(len(lines), idx + context)
            snippet = "".join(lines[start - 1:end]).rstrip("\n")
            if len(snippet) > 400:
                snippet = snippet[:397] + "..."
            results.append({
                "file": path, "line": idx, "score": s, "text": text.strip()[:200],
                "snippet": snippet,
            })
    results.sort(key=lambda r: (-r["score"], r["file"], r["line"]))
    return results[:max_results]


def selftest():
    """اختبار ذاتي: بحث تجريبي داخل مجلد النسخة نفسها."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    res = search(root, "PLAYBOOK", context=0, max_results=3)
    ok = len(res) >= 3
    print("SELFTEST:", "PASS" if ok else "FAIL", f"({len(res)} نتائج)")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="nexus_rag — استرجاع محلي stdlib فقط")
    ap.add_argument("term", nargs="?", help="المصطلح المبحوث عنه")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="مجلد الجذر للبحث")
    ap.add_argument("--context", type=int, default=2, help="أسطر السياق حول كل نتيجة")
    ap.add_argument("--max", type=int, default=20, help="أقصى عدد نتائج")
    ap.add_argument("--ext", nargs="*", default=list(DEFAULT_EXTS), help="الامتدادات المسموحة")
    ap.add_argument("--selftest", action="store_true", help="اختبار ذاتي")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())
    if not args.term:
        ap.print_help()
        sys.exit(2)

    res = search(args.root, args.term, args.context, args.max, tuple(args.ext))
    print(f"البحث عن: «{args.term}» في {args.root} — النتائج: {len(res)}")
    for r in res:
        flag = " [تحذير: حرف صيني]" if CHINESE_RE.search(r["text"]) else ""
        print(f"\n--- {r['file']}:{r['line']} (درجة {r['score']}){flag}")
        print(r["snippet"])
    if not res:
        print("لا نتائج — جرّب مصطلحاً آخر أو --root مختلف.")
    sys.exit(0 if res else 1)


if __name__ == "__main__":
    main()
