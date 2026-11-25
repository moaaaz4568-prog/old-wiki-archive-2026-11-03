#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
count.py — نظام الأرقام الوحيد لـ wiki_ver2 (single source of numbers).

يجمع COUNTS.json من القرص عبر find/wc (subprocess) — لا رقم يُكتب يدوياً.
وضع --check يقارن بالملف المحفوظ ويوسم كل مخالفة بـ ⚠️ ويخرج بـ exit 1.

الاستخدام:
  python3 tools/count.py                                  # يجمع ويكتب COUNTS.json
  python3 tools/count.py --check                          # مقارنة فقط (لا يكتب)

مبادئ التصميم (موروثة من /root/r/V3_SYS/count.py):
  * لا أختام زمنية في JSON → مخرج مطابق بايت-ببايت عند كل تشغيل.
  * أي مسار غير موجود يُسجَّل {"exists": false} ولا يُخترع له رقم.
  * .git مستثنى من الأرقام الدلالية.
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI_ROOT = os.path.dirname(HERE)
DEFAULT_OUT = os.path.join(HERE, "COUNTS.json")

COUNTED_DIRS = ["systems", "tools", "masters", "concepts", "terms",
                "sources", "indexes"]


def sh(cmd):
    """تشغيل أمر shell وإرجاع stdout نصاً (فارغاً عند الفشل)."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True,
                             text=True, timeout=120)
        return res.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        return ""


def count_files(path, exclude=None):
    """عدّ الملفات في مسار عبر find (بلا .git وملف المخرج نفسه)."""
    if not os.path.isdir(path):
        return None
    cmd = "find %s -path '*/.git' -prune -o" % subprocess.list2cmdline([path])
    if exclude:
        cmd += " -path %s -prune -o" % subprocess.list2cmdline([exclude])
    out = sh(cmd + " -type f -print | wc -l")
    return int(out) if out.isdigit() else 0


def count_md_lines(path, exclude=None):
    """إجمالي أسطر ملفات .md عبر find + wc (بلا glob)."""
    if not os.path.isdir(path):
        return None
    cmd = "find %s -path '*/.git' -prune -o" % subprocess.list2cmdline([path])
    if exclude:
        cmd += " -path %s -prune -o" % subprocess.list2cmdline([exclude])
    out = sh(cmd + " -name '*.md' -print0 | xargs -0 wc -l 2>/dev/null"
             " | tail -1 | awk '{print $1}'")
    return int(out) if out.isdigit() else 0


def count_bytes(path, exclude=None):
    """إجمالي بايتات الملفات عبر find + wc -c (بلا ملف المخرج)."""
    if not os.path.isdir(path):
        return None
    cmd = "find %s -path '*/.git' -prune -o" % subprocess.list2cmdline([path])
    if exclude:
        cmd += " -path %s -prune -o" % subprocess.list2cmdline([exclude])
    out = sh(cmd + " -type f -print0 | xargs -0 wc -c 2>/dev/null"
             " | tail -1 | awk '{print $1}'")
    return int(out) if out.isdigit() else 0


def collect(root, exclude=None):
    """بناء مستند الأرقام من القرص — مرور واحد لكل مجلد معدود."""
    doc = {
        "schema": 1,
        "generator": "tools/count.py",
        "root": root,
    }
    total = count_files(root, exclude)
    doc["total"] = {
        "exists": total is not None,
        "files": total or 0,
        "bytes": count_bytes(root, exclude) or 0,
    }
    doc["dirs"] = {}
    for d in COUNTED_DIRS:
        p = os.path.join(root, d)
        n = count_files(p, exclude)
        entry = {"exists": n is not None}
        if n is not None:
            entry["files"] = n
            if d != "tools":
                entry["md_lines"] = count_md_lines(p, exclude) or 0
        doc["dirs"][d] = entry

    # أسطر كل ملف نظام على حدة (أنظمة SYS_*)
    sys_dir = os.path.join(root, "systems")
    per_sys = {}
    if os.path.isdir(sys_dir):
        out = sh("find %s -name 'SYS_*.md' -print0 | xargs -0 wc -l"
                 % subprocess.list2cmdline([sys_dir]))
        for line in out.splitlines():
            parts = line.strip().rsplit(None, 1)
            if len(parts) == 2 and parts[0].isdigit():
                per_sys[os.path.basename(parts[1])] = int(parts[0])
    doc["systems_lines"] = dict(sorted(per_sys.items()))
    return doc


def flatten(obj, prefix=""):
    flat = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            flat.update(flatten(v, prefix + "/" + str(k)))
    else:
        flat[prefix] = obj
    return flat


def do_check(saved_path, new_doc):
    """مقارنة flat للمستند المحفوظ بالجديد — المخالف يُوسم ⚠️."""
    if not os.path.isfile(saved_path):
        print("CHECK FAIL: لا يوجد ملف محفوظ: %s" % saved_path)
        return 2
    with open(saved_path, "r", encoding="utf-8") as fh:
        saved = json.load(fh)
    a = flatten(saved)
    b = flatten(new_doc)
    keys = sorted(set(a) | set(b))
    diffs = [(k, a.get(k, "<absent>"), b.get(k, "<absent>"))
             for k in keys if a.get(k, "<absent>") != b.get(k, "<absent>")]
    if not diffs:
        print("CHECK OK: مطابق تماماً — لا فروقات. (%d مفتاح مسطّح)" % len(keys))
        return 0
    print("CHECK DIFF: %d فرق من %d مفتاح" % (len(diffs), len(keys)))
    for k, va, vb in diffs:
        print("  ⚠️ %-64s %s -> %s" % (k[-64:], va, vb))
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="نظام الأرقام الوحيد — find/wc عبر subprocess")
    ap.add_argument("--root", default=WIKI_ROOT, help="جذر الويكي")
    ap.add_argument("--out", default=DEFAULT_OUT, help="مسار COUNTS.json")
    ap.add_argument("--check", action="store_true",
                    help="قارن بالملف المحفوظ واطبع الفروقات (لا يكتب JSON)")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        print("ERROR: الجذر غير موجود: %s" % args.root, file=sys.stderr)
        return 2

    doc = collect(args.root, os.path.abspath(args.out))

    if args.check:
        return do_check(args.out, doc)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print("كُتب JSON: %s (%d بايت)" % (args.out, os.path.getsize(args.out)))
    print("  إجمالي الملفات: %d" % doc["total"]["files"])
    for d, v in sorted(doc["dirs"].items()):
        if v["exists"]:
            extra = (" · أسطر md: %d" % v["md_lines"]) if "md_lines" in v else ""
            print("  %-10s %5d ملف%s" % (d, v["files"], extra))
        else:
            print("  %-10s غير موجود" % d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
