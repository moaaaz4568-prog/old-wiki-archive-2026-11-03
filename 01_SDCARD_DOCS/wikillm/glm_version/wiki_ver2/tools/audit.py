#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit.py — بوّاب الجودة لـ wiki_ver2.

يفحص بالـ Python مباشرة (لا grep):
  1. صفر محارف CJK في كل ملف نصي.
  2. كل مجلد دلالي ≤ 900 ملف (حد الفناء).
  3. كل ماستر يحتوي الأقسام §1..§18 (FORMAT_MASTER) — يُفحص فقط عند وجود masters/.
  4. صفر TODO/TBD/placeholder/FIXME في كل ملف نصي.

المخرج: تقرير PASSED/FAILED بأوزان — exit 0 عند النجاح، 1 عند أي فشل.

الاستخدام:
  python3 tools/audit.py /sdcard/wikillm/glm_version/wiki_ver2/
"""

import os
import re
import sys

MAX_FILES_PER_DIR = 900
SECTIONS = ["§%d" % i for i in range(1, 19)]
SKIP_DIRS = {".git", "TRASH", "__pycache__", "node_modules", ".trash"}
TEXT_EXT = {".md", ".txt", ".json", ".py", ".mjs", ".js", ".yaml", ".yml",
            ".toml", ".csv", ".html", ".css"}

# نطاقات CJK: CJK Unified + Extension A/B + Compatibility + رموز وكورية/يابانية
CJK_RE = re.compile(
    "[\u2e80-\u2eff\u3000-\u303f\u3040-\u30ff\u3130-\u318f"
    "\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\ufe30-\ufe4f"
    "\U00020000-\U0002a6df]"
)
TODO_RE = re.compile(r"\b(TODO|TBD|FIXME|placeholder)\b", re.IGNORECASE)
CODE_SPAN_RE = re.compile(r"`[^`]*`")
TERM_LIST_RE = re.compile(
    r"(?i)\b(?:TODO|TBD|FIXME|placeholder)"
    r"(?:\s*/\s*(?:TODO|TBD|FIXME|placeholder))+")

# أوزان البوابات (مجموعها 100)
WEIGHTS = {
    "cjk": 40,
    "max_files": 20,
    "sections": 20,
    "placeholders": 20,
}


def iter_text_files(root):
    """مرور واحد بالقرص — os.walk فقط، بلا glob."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in TEXT_EXT:
                yield os.path.join(dirpath, fn)


def read_text(path):
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as fh:
                return fh.read(), enc
        except (UnicodeDecodeError, OSError):
            continue
    return None, None


def gate_cjk(root):
    """بوابة 1: صفر محارف CJK في كل ملف نصي."""
    violations = []
    for path in iter_text_files(root):
        text, _ = read_text(path)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            m = CJK_RE.search(line)
            if m:
                violations.append("%s:%d محرف CJK: %s U+%04X"
                                  % (path, i, m.group(0), ord(m.group(0))))
                if len(violations) >= 20:
                    return violations
    return violations


def gate_max_files(root):
    """بوابة 2: كل مجلد دلالي ≤ 900 ملف."""
    violations = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        n = len(filenames)
        if n > MAX_FILES_PER_DIR:
            violations.append("%s يحوي %d ملفاً (الحد %d)"
                              % (dirpath, n, MAX_FILES_PER_DIR))
    return violations


def gate_sections(root):
    """بوابة 3: كل ماستر يحوي §1..§18 — تُقاس فقط على ملفات masters/."""
    masters_dir = os.path.join(root, "masters")
    if not os.path.isdir(masters_dir):
        return []  # الموجة 4 لم تُبنَ بعد — البوابة غير قابلة للقياس
    violations = []
    for dirpath, dirnames, filenames in os.walk(masters_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            text, _ = read_text(path)
            if text is None:
                violations.append("%s غير قابل للقراءة" % path)
                continue
            missing = [s for s in SECTIONS if s not in text]
            if missing:
                violations.append("%s ينقصه: %s"
                                  % (path, ", ".join(missing)))
    return violations


def gate_placeholders(root):
    """بوابة 4: صفر TODO/TBD/placeholder حقيقية (لا ذكرها كتوثيق قاعدة)."""
    violations = []
    for path in iter_text_files(root):
        if path.endswith("audit.py") or path.endswith("count.py"):
            continue  # السكربتات نفسها تذكر المصطلحات كأنماط فحص
        text, _ = read_text(path)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            clean = TERM_LIST_RE.sub("", CODE_SPAN_RE.sub("", line))
            if TODO_RE.search(clean):
                violations.append("%s:%d %s" % (path, i, line.strip()[:80]))
                if len(violations) >= 20:
                    return violations
    return violations


def main(argv):
    if len(argv) != 1:
        print("الاستخدام: python3 tools/audit.py <جذر الويكي>", file=sys.stderr)
        return 2
    root = argv[0]
    if not os.path.isdir(root):
        print("ERROR: الجذر غير موجود: %s" % root, file=sys.stderr)
        return 2

    gates = [
        ("cjk", "صفر محارف CJK", gate_cjk),
        ("max_files", "كل مجلد ≤ %d ملفاً" % MAX_FILES_PER_DIR, gate_max_files),
        ("sections", "أقسام §1-§18 في كل ماستر", gate_sections),
        ("placeholders", "صفر TODO/TBD/placeholder", gate_placeholders),
    ]

    print("تقرير التدقيق — الجذر: %s" % root)
    print("=" * 60)
    total_weight = 0
    failed = False
    for key, label, fn in gates:
        violations = fn(root)
        weight = WEIGHTS[key]
        if violations:
            failed = True
            print("FAILED  %-40s (وزن %d)" % (label, weight))
            for v in violations[:10]:
                print("    - %s" % v)
            if len(violations) > 10:
                print("    ... و %d مخالفة أخرى" % (len(violations) - 10))
        else:
            total_weight += weight
            print("PASSED  %-40s (وزن %d)" % (label, weight))
    print("=" * 60)
    verdict = "FAILED" if failed else "PASSED"
    print("الحكم النهائي: %s — النقاط %d/100" % (verdict, total_weight))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
