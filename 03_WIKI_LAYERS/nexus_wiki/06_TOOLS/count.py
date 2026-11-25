#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V3_SYS/count.py — نظام الأرقام الوحيد (single source of numbers).

كل رقم في المشروع يجب أن يولَّد من القرص لا أن يُكتب يدوياً.
هذا السكربت هو المولّد الوحيد للأرقام: بلا شبكة، بلا توكنات، stdlib فقط.

الاستخدام:
  python3 count.py --root /root/r/NB2 \
                   --root /root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI \
                   --out  /root/r/V3_SYS/COUNTS.json

  python3 count.py --out /root/r/V3_SYS/COUNTS.json --check   # مقارنة فقط (لا يكتب JSON)
  python3 count.py --out /root/r/V3_SYS/COUNTS.json --md      # + يولّد COUNTS.md
  python3 count.py --md-only --out /root/r/V3_SYS/COUNTS.json # COUNTS.md فقط

مبادئ التصميم:
  * os.walk فقط — لا glob ولا shell expansion (27k ملف يكسر ARG_MAX).
  * مرور واحد (single pass) لكل جذر: كل رقم في المخرجات من نفس اللقطة،
    فلا يمكن أن تتناقض أرقام من مرحلتين مختلفتين.
  * لا أختام زمنية (timestamps) في المخرجات → المخرج مطابق بايت-ببايت عند كل
    تشغيل (idempotent). شرط ليعمل كـ«نظام أرقام» قابل للتدقيق.
  * أي مسار غير موجود يُسجَّل صراحةً {"exists": false, "files": 0}
    ولا يُخترع له رقم.
  * مسارات .git تُستثنى من الأرقام الدلالية وتُعدّ منفصلة باسمها.
  * المسح النصي متوازٍ (خيوط) لأن القرص I/O-bound والقراءة تُحرّر GIL.
"""

import argparse
import json
import os
import platform
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# ---------------------------------------------------------------------------
# ثوابت
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 3
SCAN_THREADS = 16

# الأقسام الإلزامية في بطاقة المفهوم. تُبحث بترميز utf-8 على البايتات الخام
# (أسرع، ولا ترمي UnicodeDecodeError على الملفات التالفة).
QUINTUPLE_SECTIONS = [
    ("mechanism", "الآلية"),
    ("fence_limits", "حدود الفناء"),
    ("evidence", "الدليل"),
    ("sourcing", "المصدرية"),
    ("tensions", "التوترات"),
]
QUINTUPLE_NEEDLES = [
    (key, "## " + label, ("## " + label).encode("utf-8"))
    for key, label in QUINTUPLE_SECTIONS
]
QUINTUPLE_LABEL = dict(QUINTUPLE_SECTIONS)

# مجلدات NB2 التي تُعدّ إجمالاً.
NB2_COUNTED_DIRS = [
    "00_CHARTER",
    "00_SYSTEMS",
    "01_INVENTORY",
    "01_TERMS",
    "02_CONCEPTS",
    "03_MASTERS",
    "04_SEARCH",
    "05_TENSIONS",
    "06_GLOSSARY",
    "07_PROVENANCE",
    ".nexus_work",
    "TRASH",
]

# مجلدات v1 المطلوبة كـ wiki/<name>، وجذر brain.
V1_WIKI_DIRS = ["concepts", "sources", "entities", "tools", "keywords"]

VCS_DIRS = (".git",)

# توقيتات المراحل (للstdout فقط — لا تُكتب في JSON حتى يبقى المخرج مطابقاً).
TIMINGS = []


def _mark(label, t0):
    TIMINGS.append((label, time.time() - t0))
    return time.time()

NB2_SUBTREES = NB2_COUNTED_DIRS + ["02_CONCEPTS/terms_26k"]
NB2_SUBTREES2 = ["02_CONCEPTS/terms_26k"]
NB2_QUINTUPLE_SCOPE = "02_CONCEPTS"


# ---------------------------------------------------------------------------
# أدوات مساعدة
# ---------------------------------------------------------------------------

def human_bytes(n):
    """بايت → نص مقروء."""
    step = 1024.0
    value = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(value) < step or unit == "TB":
            if unit == "B":
                return "%d B" % int(value)
            return "%.2f %s" % (value, unit)
        value /= step
    return "%d B" % n


def new_subtree():
    return {"exists": False, "files": 0, "md_files": 0, "root_files": 0,
            "children": {}}


def new_blank():
    d = {k: 0 for k, _l, _b in QUINTUPLE_NEEDLES}
    d["_files_scanned"] = 0
    d["_unreadable"] = 0
    return d


def scan_root(root, subtrees=(), subtrees2=(), md_under=None,
              master_subtree=None, master_prefix="Master_"):
    """مرور واحد على الشجرة كلها، وتوزيع كل رقم على المجذور المطلوبة.

    يُرجع dict فيه:
      totals       : أرقام الجذر إجمالاً
      subtrees     : {اسم: {files, md_files, root_files, children:{اسم: عدد}}}
                     حيث children = المجلدات الفرعية المباشرة على عمق 1
      subtrees2    : نفس الشكل لكن children على عمق 2 (مثل <sector>/<part_NN>)
      md_under     : [مسارات .md نسبية] لأجل المسح النصي
      masters      : {"outside": n, "in_archive": n}
    """
    sub = {s: new_subtree() for s in subtrees}
    for s in subtrees:
        if os.path.isdir(os.path.join(root, s)):
            sub[s]["exists"] = True
    sub2 = {s: new_subtree() for s in subtrees2}
    for s in subtrees2:
        if os.path.isdir(os.path.join(root, s)):
            sub2[s]["exists"] = True
    md_list = []
    acc = {"files": 0, "bytes": 0, "md_files": 0, "dirs": 0,
           "vcs_files": 0, "vcs_bytes": 0, "unreadable": 0}
    masters = {"outside": 0, "in_archive": 0, "exists": False}

    if not os.path.isdir(root):
        return {
            "totals": {"exists": False, "files": 0, "md_files": 0, "bytes": 0,
                       "dirs": 0, "vcs_files": 0, "vcs_bytes": 0,
                       "unreadable": 0},
            "subtrees": sub, "subtrees2": sub2, "md_under": md_list,
            "masters": masters,
        }

    if master_subtree and os.path.isdir(os.path.join(root, master_subtree)):
        masters["exists"] = True

    def onerror(_err):
        acc["unreadable"] += 1

    for dirpath, dirnames, filenames in os.walk(root, onerror=onerror,
                                                  followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d not in VCS_DIRS)
        acc["dirs"] += 1
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = "" if rel_dir == "." else rel_dir.replace(os.sep, "/")
        top = rel_dir.split("/")[0] if rel_dir else ""

        if top in VCS_DIRS:
            for name in filenames:
                acc["vcs_files"] += 1
                try:
                    acc["vcs_bytes"] += os.path.getsize(
                        os.path.join(dirpath, name))
                except OSError:
                    acc["unreadable"] += 1
            continue

        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.join(rel_dir, name).replace(os.sep, "/")
            try:
                size = os.path.getsize(full)
            except OSError:
                acc["unreadable"] += 1
                continue
            acc["files"] += 1
            acc["bytes"] += size
            is_md = name.endswith(".md")
            if is_md:
                acc["md_files"] += 1
                md_list.append(rel)

            # توزيع على المجذور الفرعية (عمق 1)
            for s in subtrees:
                if not rel.startswith(s + "/"):
                    continue
                st = sub[s]
                st["files"] += 1
                if is_md:
                    st["md_files"] += 1
                rest = rel[len(s) + 1:]
                child = rest.split("/", 1)[0] if "/" in rest else None
                if child is None:
                    st["root_files"] += 1
                else:
                    st["children"][child] = st["children"].get(child, 0) + 1

            # توزيع على المجذور الفرعية (عمق 2) — sector/part_NN
            for s in subtrees2:
                if not rel.startswith(s + "/"):
                    continue
                st2 = sub2[s]
                st2["files"] += 1
                if is_md:
                    st2["md_files"] += 1
                segs = rel[len(s) + 1:].split("/")
                if len(segs) == 1:
                    st2["root_files"] += 1
                else:
                    key = segs[0] + "/" + segs[1]
                    st2["children"][key] = st2["children"].get(key, 0) + 1

            # عدّ Master_*.md داخل شجرة محددة
            if masters["exists"] and name.startswith(master_prefix) \
                    and name.endswith(".md") and rel.startswith(master_subtree + "/"):
                parts = rel.split("/")[1:]
                if "_archive" in parts:
                    masters["in_archive"] += 1
                else:
                    masters["outside"] += 1

    return {
        "totals": {
            "exists": True,
            "files": acc["files"],
            "md_files": acc["md_files"],
            "bytes": acc["bytes"],
            "dirs": acc["dirs"],
            "vcs_files": acc["vcs_files"],
            "vcs_bytes": acc["vcs_bytes"],
            "unreadable": acc["unreadable"],
        },
        "subtrees": sub,
        "subtrees2": sub2,
        "md_under": md_list,
        "masters": masters,
    }


def _probe_file(path):
    """يقرأ ملفاً واحداً ويعيد (القسم_found_tuple أو None, unreadable)."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return (None, True)
    hits = []
    for i, (_k, _l, needle) in enumerate(QUINTUPLE_NEEDLES):
        hits.append(1 if needle in data else 0)
    return (tuple(hits), False)


def scan_quintuple(root, rel_files, split_prefix=None, threads=SCAN_THREADS):
    """مسح نصي واحد (متوازٍ) لعدّ الأقسام الخمسة.

    split_prefix: إن مُرِّر، تُقسَّم النتائج إلى "داخل البادئة" و"خارجها".
    """
    outside, inside = new_blank(), new_blank()
    inside["_exists"] = os.path.isdir(root)
    outside["_exists"] = inside["_exists"]

    prefix = split_prefix.rstrip("/") if split_prefix else None
    jobs = []
    for rel in rel_files:
        if prefix and (rel == prefix or rel.startswith(prefix + "/")):
            jobs.append((os.path.join(root, rel), inside))
        else:
            jobs.append((os.path.join(root, rel), outside))

    keys = [k for k, _l, _b in QUINTUPLE_NEEDLES]
    if not jobs:
        return outside, inside

    with ThreadPoolExecutor(max_workers=max(1, threads)) as pool:
        results = list(pool.map(lambda j: _probe_file(j[0]), jobs, chunksize=64))
    for (_path, target), (hits, bad) in zip(jobs, results):
        if bad:
            target["_unreadable"] += 1
            continue
        target["_files_scanned"] += 1
        for i, k in enumerate(keys):
            target[k] += hits[i]
    return outside, inside


# ---------------------------------------------------------------------------
# بناء التقارير
# ---------------------------------------------------------------------------

def build_nb2(root, scan):
    out = {"root": root, "exists": scan["totals"]["exists"]}
    if not out["exists"]:
        return out
    t = scan["totals"]
    sub = scan["subtrees"]
    c = root.rstrip("/")

    out["total"] = {
        "files": t["files"] - t["vcs_files"],
        "md_files": t["md_files"],
        "bytes": t["bytes"] - t["vcs_bytes"],
        "dirs": t["dirs"],
        "vcs_files": t["vcs_files"],
        "vcs_bytes": t["vcs_bytes"],
        "unreadable": t["unreadable"],
    }

    # مجلدات معدودة — كلها في subtrees فلا حاجة لأي مرور إضافي
    out["dirs"] = {}
    for d in NB2_COUNTED_DIRS:
        st = sub.get(d)
        out["dirs"][d] = {"exists": bool(st and st["exists"]),
                          "files": st["files"] if st else 0}

    concepts = sub["02_CONCEPTS"]
    out["concepts_sectors"] = dict(sorted(concepts["children"].items()))
    out["concepts_root_files"] = concepts["root_files"]
    out["concepts_total"] = concepts["files"]
    out["concepts_md"] = concepts["md_files"]

    masters = sub["03_MASTERS"]
    out["masters_subdirs"] = dict(sorted(masters["children"].items()))
    out["masters_root_files"] = masters["root_files"]
    out["masters_total"] = masters["files"]

    t26 = sub["02_CONCEPTS/terms_26k"]
    sectors = dict(sorted(t26["children"].items()))
    t26d2 = scan["subtrees2"]["02_CONCEPTS/terms_26k"]
    parts = dict(sorted(t26d2["children"].items()))
    agg = {}
    for k, v in parts.items():
        part = k.rsplit("/", 1)[-1]
        agg[part] = agg.get(part, 0) + v
    out["terms_26k"] = {
        "exists": t26["exists"],
        "files": t26["files"],
        "md_files": t26["md_files"],
        "root_files": t26["root_files"],
        "sectors": sectors,
        "parts": parts,
        "parts_aggregate": dict(sorted(agg.items())),
    }

    # الخماسية: مسح نصي على ملفات 02_CONCEPTS فقط، مقسومة على terms_26k
    scope = NB2_QUINTUPLE_SCOPE
    rel_md = [r for r in scan["md_under"]
              if r.startswith(scope + "/") or r == scope]
    out["_quintuple_scope"] = scope
    outside, inside = scan_quintuple(
        c, rel_md, split_prefix=scope + "/terms_26k")
    out["quintuple_concepts_excl_terms26k"] = outside
    out["quintuple_terms_26k"] = inside
    return out


def build_v1(root, scan):
    out = {"root": root, "exists": scan["totals"]["exists"]}
    if not out["exists"]:
        return out
    t = scan["totals"]
    m = scan["masters"]
    out["total"] = {
        "files": t["files"] - t["vcs_files"],
        "md_files": t["md_files"],
        "bytes": t["bytes"] - t["vcs_bytes"],
        "vcs_files": t["vcs_files"],
    }
    out["nexus_vault_master_md"] = m["outside"]
    out["nexus_vault_master_md_in_archive"] = m["in_archive"]
    out["nexus_vault_master_md_including_archive"] = m["outside"] + m["in_archive"]
    out["nexus_vault_exists"] = m["exists"]

    v = root.rstrip("/")
    wiki_dir = os.path.join(v, "wiki")
    wiki_dir_exists = os.path.isdir(wiki_dir)
    out["wiki"] = {"_wiki_dir_exists": wiki_dir_exists}
    for d in V1_WIKI_DIRS:
        if wiki_dir_exists and os.path.isdir(os.path.join(wiki_dir, d)):
            st = scan["subtrees"].get("wiki/" + d)
            out["wiki"][d] = {"exists": True,
                              "files": st["files"] if st else 0,
                              "resolved_at": "wiki/" + d}
        else:
            st = scan["subtrees"].get(d)
            if st is not None:
                out["wiki"][d] = {"exists": st["exists"], "files": st["files"],
                                  "resolved_at": "<v1_root>/" + d}
            else:
                out["wiki"][d] = {"exists": False, "files": 0}
    b = scan["subtrees"].get("brain")
    out["brain"] = ({"exists": b["exists"], "files": b["files"]} if b
                    else {"exists": False, "files": 0})
    return out


def detect_nb2(roots):
    for r in roots:
        if "NB2" in r.replace("\\", "/").split("/"):
            return r
    return None


def detect_v1(roots):
    for r in roots:
        s = r.replace("\\", "/")
        if "01_ACTIVE_WIKI" in s or s.endswith("ACTIVE_WIKI"):
            return r
    return None


def collect(roots):
    doc = {
        "schema": SCHEMA_VERSION,
        "generator": "V3_SYS/count.py",
        "python": "%d.%d" % sys.version_info[:2],
        "platform": platform.system().lower(),
    }
    nb2_root = detect_nb2(roots)
    v1_root = detect_v1(roots)
    v1_subtrees = ["brain", "nexus_vault"] \
        + V1_WIKI_DIRS + ["wiki/" + d for d in V1_WIKI_DIRS]

    doc["roots"] = {}
    scans = {}
    for r in roots:
        t0 = time.time()
        if r == nb2_root:
            s = scan_root(r, subtrees=NB2_SUBTREES,
                          subtrees2=NB2_SUBTREES2)
        elif r == v1_root:
            s = scan_root(r, subtrees=v1_subtrees,
                          master_subtree="nexus_vault")
        else:
            s = scan_root(r)
        _mark("walk:" + os.path.basename(r), t0)
        scans[r] = s
        t = s["totals"]
        doc["roots"][r] = {
            "exists": t["exists"],
            "files": t["files"] - t["vcs_files"],
            "md_files": t["md_files"],
            "bytes": t["bytes"] - t["vcs_bytes"],
            "dirs": t["dirs"],
            "vcs_files": t["vcs_files"],
            "vcs_bytes": t["vcs_bytes"],
            "unreadable": t["unreadable"],
        }
    _t0 = time.time()
    doc["nb2"] = build_nb2(nb2_root, scans[nb2_root]) if nb2_root else \
        {"root": None, "exists": False}
    _mark("nb2_report+text_scan", _t0)
    doc["v1"] = build_v1(v1_root, scans[v1_root]) if v1_root else \
        {"root": None, "exists": False}
    _mark("v1_report", time.time())
    return doc


# ---------------------------------------------------------------------------
# طباعة الجدول
# ---------------------------------------------------------------------------

def _row(label, value, unit=""):
    print("  %-52s %12s %s" % (label, value, unit))


def print_table(doc):
    print("=" * 78)
    print("V3_SYS — نظام الأرقام (مولّد من القرص، بلا أي رقم مكتوب يدوياً)")
    print("schema v%d · بايثون %s · %s · خيوط المسح النصي: %d"
          % (doc["schema"], doc["python"], doc["platform"], SCAN_THREADS))
    print("=" * 78)

    print("\n[1] إجماليات الجذور")
    print("  %-56s %9s %9s %14s" % ("root", "files", ".md", "bytes"))
    for r, v in sorted(doc["roots"].items()):
        if not v["exists"]:
            print("  %-56s %9s" % (r[:56], "MISSING"))
            continue
        print("  %-56s %9d %9d %14d" % (r[:56], v["files"], v["md_files"],
                                        v["bytes"]))
        if v["vcs_files"]:
            print("  %-56s %9d %9s %14d  (.git — مستثنى من الأرقام الدلالية)"
                  % ("  ↳ vcs", v["vcs_files"], "-", v["vcs_bytes"]))

    nb2 = doc["nb2"]
    if nb2.get("exists"):
        t = nb2["total"]
        print("\n[2] NB2 — الإجمالي")
        _row("ملفات (بلا .git)", t["files"])
        _row(".md", t["md_files"])
        _row("بايت", t["bytes"], human_bytes(t["bytes"]))
        _row("مجلدات", t["dirs"])
        if t["vcs_files"]:
            _row("ملفات داخل .git (مستثناة)", t["vcs_files"])
        if t["unreadable"]:
            _row("ملفات/مجلدات غير مقروءة", t["unreadable"])

        print("\n[3] NB2 — مجلدات معدودة")
        for d, v in sorted(nb2["dirs"].items()):
            _row(d, v["files"] if v["exists"] else "MISSING")

        print("\n[4] NB2/02_CONCEPTS — القطاعات (عمق 1، بلا .git)")
        for k, v in sorted(nb2["concepts_sectors"].items()):
            _row("02_CONCEPTS/" + k, v)
        if nb2["concepts_root_files"]:
            _row("02_CONCEPTS/ (ملفات على الجذر)", nb2["concepts_root_files"])
        _row("02_CONCEPTS (الإجمالي)", nb2["concepts_total"])
        _row("02_CONCEPTS (.md)", nb2["concepts_md"])

        print("\n[5] NB2/03_MASTERS — الملفات لكل مجلد")
        for k, v in sorted(nb2["masters_subdirs"].items()):
            _row("03_MASTERS/" + k, v)
        if nb2["masters_root_files"]:
            _row("03_MASTERS/ (ملفات على الجذر)", nb2["masters_root_files"])
        _row("03_MASTERS (الإجمالي)", nb2["masters_total"])

        t26 = nb2["terms_26k"]
        print("\n[6] NB2/02_CONCEPTS/terms_26k — الإجمالي")
        _row("terms_26k (إجمالي الملفات)", t26["files"])
        _row("terms_26k (.md)", t26["md_files"])
        _row("عدد القطاعات", len(t26["sectors"]))
        _row("عدد مفاتيح part (قطاع/part)", len(t26["parts"]))
        _row("عدد part_NN (تجميعي)", len(t26["parts_aggregate"]))

        print("\n[7] terms_26k — التوزيع على القطاعات")
        for k, v in sorted(t26["sectors"].items()):
            _row("terms_26k/" + k, v)

        print("\n[8] terms_26k — التوزيع على part_NN (لكل قطاع)")
        for k, v in sorted(t26["parts"].items()):
            _row("terms_26k/" + k, v)

        print("\n[9] terms_26k — تجميع part_NN عبر القطاعات")
        for k, v in sorted(t26["parts_aggregate"].items()):
            _row(k, v)

        for label, key in (("خارج terms_26k", "quintuple_concepts_excl_terms26k"),
                           ("داخل terms_26k", "quintuple_terms_26k")):
            q = nb2[key]
            print("\n[10] الخماسية الإلزامية — %s" % label)
            print("      %-34s %9d" % ("ملفات .md ممسوحة", q["_files_scanned"]))
            for k, _l, _b in QUINTUPLE_NEEDLES:
                print("      %-34s %9d" % ("## " + QUINTUPLE_LABEL[k], q[k]))
            if q["_unreadable"]:
                print("      %-34s %9d" % ("(غير قابل للقراءة)", q["_unreadable"]))

    v1 = doc["v1"]
    if v1.get("exists"):
        print("\n[11] v1 (الويكي النشط)")
        _row("nexus_vault Master_*.md (بلا _archive)", v1["nexus_vault_master_md"])
        _row("nexus_vault Master_*.md (داخل _archive)",
             v1["nexus_vault_master_md_in_archive"])
        _row("nexus_vault Master_*.md (المجموع)",
             v1["nexus_vault_master_md_including_archive"])
        print("      wiki/ موجود: %s"
              % ("نعم" if v1["wiki"]["_wiki_dir_exists"] else "لا (الفحص على مستوى v1)"))
        for d in V1_WIKI_DIRS:
            w = v1["wiki"][d]
            if not w["exists"]:
                _row("wiki/" + d, "MISSING")
            else:
                _row("wiki/" + d, w["files"], "<" + w["resolved_at"] + ">")
        b = v1["brain"]
        _row("brain/ (ملفات)", b["files"] if b["exists"] else "MISSING")
    print()


# ---------------------------------------------------------------------------
# markdown
# ---------------------------------------------------------------------------

def gen_md(doc):
    L = []
    a = L.append
    a("# V3_SYS — الأرقام المعتمدة (مولّدة من القرص)")
    a("")
    a("> مصدر واحد للأرقام. كل قيمة أدناه مُقاسة بـ `python3 V3_SYS/count.py`.")
    a("> أي رقم غير موجود هنا = رقم مُختلق. لا تكتب أرقاماً يدوياً.")
    a("")
    a("المولّد: `V3_SYS/count.py` · schema v%d · بايثون %s · %s"
      % (doc["schema"], doc["python"], doc["platform"]))
    a("")

    a("## 1. إجماليات الجذور")
    a("")
    a("| root | files | .md | bytes |")
    a("|---|---:|---:|---:|")
    for r, v in sorted(doc["roots"].items()):
        if not v["exists"]:
            a("| `%s` | **MISSING** | – | – |" % r)
            continue
        a("| `%s` | %d | %d | %d |" % (r, v["files"], v["md_files"], v["bytes"]))
        if v["vcs_files"]:
            a("| ↳ `.git` (مستثنى) | %d | – | %d |"
              % (v["vcs_files"], v["vcs_bytes"]))
    a("")

    nb2 = doc["nb2"]
    if nb2.get("exists"):
        t = nb2["total"]
        a("## 2. NB2")
        a("")
        a("| المقياس | القيمة |")
        a("|---|---:|")
        a("| ملفات (بلا `.git`) | %d |" % t["files"])
        a("| `.md` | %d |" % t["md_files"])
        a("| بايت | %d |" % t["bytes"])
        a("| مجلدات | %d |" % t["dirs"])
        if t["vcs_files"]:
            a("| ملفات داخل `.git` (مستثناة) | %d |" % t["vcs_files"])
        a("")
        a("### 2.1 مجلدات معدودة")
        a("")
        a("| المجلد | الملفات |")
        a("|---|---:|")
        for d, v in sorted(nb2["dirs"].items()):
            a("| `NB2/%s` | %s |"
              % (d, v["files"] if v["exists"] else "**MISSING**"))
        a("")
        a("### 2.2 `02_CONCEPTS`")
        a("")
        a("| المقياس | القيمة |")
        a("|---|---:|")
        a("| إجمالي الملفات | %d |" % nb2["concepts_total"])
        a("| `.md` | %d |" % nb2["concepts_md"])
        a("| ملفات على جذر المجلد | %d |" % nb2["concepts_root_files"])
        a("")
        a("| القطاع (عمق 1) | الملفات |")
        a("|---|---:|")
        for k, v in sorted(nb2["concepts_sectors"].items()):
            a("| `%s` | %d |" % (k, v))
        a("")
        a("### 2.3 `03_MASTERS`")
        a("")
        a("| المجلد | الملفات |")
        a("|---|---:|")
        for k, v in sorted(nb2["masters_subdirs"].items()):
            a("| `%s` | %d |" % (k, v))
        a("| ملفات على جذر المجلد | %d |" % nb2["masters_root_files"])
        a("| **الإجمالي** | %d |" % nb2["masters_total"])
        a("")

        t26 = nb2["terms_26k"]
        a("## 3. `02_CONCEPTS/terms_26k`")
        a("")
        a("| المقياس | القيمة |")
        a("|---|---:|")
        a("| إجمالي الملفات | %d |" % t26["files"])
        a("| `.md` | %d |" % t26["md_files"])
        a("| عدد القطاعات | %d |" % len(t26["sectors"]))
        a("| عدد `part_NN` (تجميعي) | %d |" % len(t26["parts_aggregate"]))
        a("")
        a("### 3.1 التوزيع على القطاعات")
        a("")
        a("| القطاع | الملفات |")
        a("|---|---:|")
        for k, v in sorted(t26["sectors"].items()):
            a("| `%s` | %d |" % (k, v))
        a("")
        a("### 3.2 التوزيع على `part_NN`")
        a("")
        a("| key | الملفات |")
        a("|---|---:|")
        for k, v in sorted(t26["parts"].items()):
            a("| `%s` | %d |" % (k, v))
        a("")
        a("### 3.3 تجميع `part_NN` عبر القطاعات")
        a("")
        a("| part | الملفات |")
        a("|---|---:|")
        for k, v in sorted(t26["parts_aggregate"].items()):
            a("| `%s` | %d |" % (k, v))
        a("")

        qa = nb2["quintuple_concepts_excl_terms26k"]
        qb = nb2["quintuple_terms_26k"]
        a("## 4. الخماسية الإلزامية (مسح نصي)")
        a("")
        a("| القسم | خارج `terms_26k` | داخل `terms_26k` |")
        a("|---|---:|---:|")
        a("| ملفات `.md` ممسوحة | %d | %d |"
          % (qa["_files_scanned"], qb["_files_scanned"]))
        for k, label in QUINTUPLE_SECTIONS:
            a("| `%s` | %d | %d |" % ("## " + label, qa[k], qb[k]))
        a("")

    v1 = doc["v1"]
    if v1.get("exists"):
        a("## 5. v1 (الويكي النشط)")
        a("")
        a("| المقياس | القيمة |")
        a("|---|---:|")
        a("| `nexus_vault` `Master_*.md` (بلا `_archive`) | %d |"
          % v1["nexus_vault_master_md"])
        a("| `nexus_vault` `Master_*.md` (داخل `_archive`) | %d |"
          % v1["nexus_vault_master_md_in_archive"])
        a("| `nexus_vault` `Master_*.md` (المجموع) | %d |"
          % v1["nexus_vault_master_md_including_archive"])
        for d in V1_WIKI_DIRS:
            w = v1["wiki"][d]
            a("| `wiki/%s` | %s |"
              % (d, w["files"] if w["exists"] else "**MISSING**"))
        a("| `brain/` | %d |"
          % (v1["brain"]["files"] if v1["brain"]["exists"] else 0))
        a("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------

def flatten(obj, prefix=""):
    flat = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            flat.update(flatten(v, prefix + "/" + str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            flat.update(flatten(v, prefix + "[%d]" % i))
    else:
        flat[prefix] = obj
    return flat


def do_check(saved_path, new_doc):
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
        print("  %-64s %s -> %s" % (k[-64:], va, vb))
    return 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(here)
    ap = argparse.ArgumentParser(
        description="نظام الأرقام الوحيد — عدّ من القرص (stdlib فقط، بلا glob)")
    ap.add_argument("--root", action="append", default=[],
                    help="مسار جذر (يمكن تكراره)")
    ap.add_argument("--out", default=os.path.join(here, "COUNTS.json"),
                    help="مسار JSON المحفوظ")
    ap.add_argument("--check", action="store_true",
                    help="قارن بالملف المحفوظ واطبع الفروقات فقط (لا يكتب JSON)")
    ap.add_argument("--md", dest="md_out", default=None,
                    help="اكتب ماركداون إلى هذا المسار")
    ap.add_argument("--md-only", action="store_true",
                    help="اكتب COUNTS.md فقط إلى <out dir>/COUNTS.md")
    args = ap.parse_args(argv)

    roots = [r.rstrip("/") for r in (args.root or [
        os.path.join(parent, "NB2"),
        os.path.join(parent, "NEXUS_GITHUB_PACKAGE", "WIKI", "01_ACTIVE_WIKI"),
    ])]

    doc = collect(roots)
    rc = 0

    if args.md_only:
        md_path = os.path.join(os.path.dirname(os.path.abspath(args.out)),
                               "COUNTS.md")
    else:
        md_path = args.md_out

    if args.check:
        rc = do_check(args.out, doc)
        if not md_path:
            return rc

    print_table(doc)

    if TIMINGS:
        print("[timing] مراحل هذا التشغيل (ثانية):")
        for label, secs in TIMINGS:
            print("  %-34s %8.1f" % (label, secs))
        print("  %-34s %8.1f" % ("المجموع", sum(s for _l, s in TIMINGS)))
        print()

    if not args.check:
        out_dir = os.path.dirname(os.path.abspath(args.out))
        if out_dir and not os.path.isdir(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        print("كُتب JSON: %s (%d بايت)" % (args.out, os.path.getsize(args.out)))

    if md_path:
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write(gen_md(doc))
        print("كُتب MD:   %s (%d بايت)" % (md_path, os.path.getsize(md_path)))

    return rc


if __name__ == "__main__":
    sys.exit(main())
