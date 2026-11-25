#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يبني خريطة العيوب من تشغيلَي audit_scoped.py الفعليَّين.

المدخلات (نتائج تشغيل حقيقية، لا تقديرات):
  AUDIT_CONCEPTS_REAL_findings.jsonl  (--scope concepts)
  AUDIT_MASTERS_findings.jsonl        (--scope masters)

المخرجات:
  ../DEFECTS.jsonl        سطر لكل عيب
  ../DEFECTS_SUMMARY.md   الجداول والأولويات

قاعدة تقدير الوكلاء (من المهمة): 20–25 concept للوكيل الواحد.
"""

import json
import math
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)

CONCEPTS = os.path.join(HERE, "AUDIT_CONCEPTS_REAL_findings.jsonl")
MASTERS = os.path.join(HERE, "AUDIT_MASTERS_findings.jsonl")
OUT_JSONL = os.path.join(V3, "DEFECTS.jsonl")
OUT_MD = os.path.join(V3, "DEFECTS_SUMMARY.md")

# fix_class: add | rewrite | merge | archive   ·   fixable_by: script | agent
FIX = {
    "C01": ("rewrite", "script"),   # [[X]] لا وجود له ⇒ تصحيح الاسم إلى مفهوم قائم
    "C02": ("rewrite", "agent"),    # كعب <300B ⇒ إعادة كتابة
    "C03": ("merge", "agent"),      # تكرار حرفي ⇒ دمج
    "C04": ("add", "agent"),        # بلا دليل/اقتباس ⇒ إضافة
    "C05": ("add", "agent"),        # بلا «حدود الفناء» ⇒ إضافة
    "C06": ("add", "agent"),        # بلا «الآلية» ⇒ إضافة
    "C07": ("rewrite", "agent"),    # ماستر بأقسام <18 ⇒ توسيع
    "C08": ("merge", "agent"),      # اسم مكرر ⇒ دمج
    "C09": ("add", "agent"),        # قطاع بلا ماستر ⇒ بناء ماستر
    "C10": ("rewrite", "script"),   # مزامنة صفوف §18 مع concepts القطاع
    "C11": ("rewrite", "agent"),    # رقم بلا ⚠️/مصدر ⇒ تعليق
    "C13": ("add", "script"),       # رابط عكسي من جدول §18 (ميكانيكي)
    "C14": ("add", "agent"),        # الأقسام الستة الناقصة ⇒ إضافة
    "C15": ("rewrite", "script"),   # إعادة تسمية + تحديث الروابط
    "C16": ("rewrite", "agent"),    # حشو/سيريليكي ⇒ تنظيف
    "C17": ("add", "agent"),        # ماستر بلا حدود فناء ⇒ إضافة
    "C18": ("rewrite", "agent"),    # بوابات Master SPEC ⇒ توسيع
    "C19": ("add", "script"),       # مفاتيح frontmatter ناقصة
    "C20": ("archive", "script"),   # نسخة مطابقة بين مجلدين ⇒ أرشفة النسخة الزائدة
    "C21": ("archive", "script"),   # مجلد >1000 ملف ⇒ تقسيم/أرشفة
    "C22": ("archive", "agent"),    # 99_misc >3% ⇒ إعادة تصنيف
    "C23": ("add", "agent"),        # بلا توترات (تقرير فقط، severity=0)
    "C24": ("rewrite", "agent"),    # <250 كلمة ⇒ توسيع
    "C25": ("rewrite", "agent"),    # >600 كلمة ⇒ ضغط/تقسيم
    "C26": ("add", "agent"),        # بلا «## المصدرية» ⇒ إضافة
    "C27": ("rewrite", "agent"),    # placeholders ⇒ إزالة/إنجاز
    "C28": ("add", "agent"),        # مصادر فارغة ⇒ إضافة مصادر
}

SECTOR_RE = re.compile(r"^(\d{2})_[A-Za-z0-9_]+")
PER_AGENT_MIN, PER_AGENT_MAX = 25, 20     # 25 concept/agent ⇒ أدنى عدد، 20 ⇒ أقصى عدد


def load(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def sector_of(path, evidence=""):
    """قطاع العيب من مساره؛ يُستخرج من الدليل إن لم يكن مسار ملف."""
    if path.startswith("[["):
        m = re.search(r"مثال:\s*(\S+)", evidence or "")
        if m:
            parts = m.group(1).split("/")
            if len(parts) >= 2:
                s = SECTOR_RE.match(parts[1] if parts[0] == "02_CONCEPTS" else parts[0])
                return (s.group(0) if s else parts[-2]), True
        return "—", True
    if path == "(تجميعي)":
        return "—", True
    for part in path.split(":"):                      # C22: مسارات مركّبة
        p = part.strip("/")
        segs = p.split("/")
        start = 1 if segs and segs[0] in ("02_CONCEPTS", "03_MASTERS") else 0
        for seg in segs[start:]:
            if SECTOR_RE.match(seg):
                return seg, True
    return "—", True


def main():
    concepts = load(CONCEPTS)
    masters = load(MASTERS)

    defects = []
    for scope, rows in (("concepts", concepts), ("masters", masters)):
        for r in rows:
            cid = r["checker"]
            fix_class, fixable_by = FIX[cid]
            sec, structural = sector_of(r["path"], r["evidence"])
            defects.append({
                "defect_id": "D%s" % cid[1:],
                "checker": cid,
                "path": r["path"],
                "bytes": r["bytes"],
                "evidence": r["evidence"],
                "severity": r["severity"],
                "fix_class": fix_class,
                "fixable_by": fixable_by,
            })

    with open(OUT_JSONL, "w", encoding="utf-8") as fh:
        for d in defects:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")

    # ---- تجميعات ----
    by_checker = defaultdict(lambda: {"n": 0, "sev": 0, "name": "", "fix": "", "by": "",
                                      "files": set(), "scopes": set()})
    for scope, rows in (("concepts", concepts), ("masters", masters)):
        for r in rows:
            c = by_checker[r["checker"]]
            c["n"] += 1
            c["sev"] = r["severity"]
            c["name"] = r.get("checker_name", r.get("name", ""))
            c["fix"] = FIX[r["checker"]][0]
            c["by"] = FIX[r["checker"]][1]
            c["files"].add(r["path"])
            c["scopes"].add(scope)

    by_sector = defaultdict(lambda: {"n": 0, "files": set(), "agent_files": set(),
                                     "script_files": set(), "sev": 0, "wsum": 0,
                                     "checks": defaultdict(int), "maxsev": 0})
    for scope, rows in (("concepts", concepts), (("masters"), masters)):
        for r in rows:
            sec, _ = sector_of(r["path"], r["evidence"])
            s = by_sector[sec]
            s["n"] += 1
            s["files"].add(r["path"])
            s["checks"][r["checker"]] += 1
            if r["severity"] > 0:
                s["wsum"] += r["severity"]
                s["maxsev"] = max(s["maxsev"], r["severity"])
            if FIX[r["checker"]][1] == "agent":
                s["agent_files"].add(r["path"])
            else:
                s["script_files"].add(r["path"])

    # عدد concepts لكل قطاع (من القرص —的真实数)
    counts = {}
    cc = os.path.join("/root/r/NB2/02_CONCEPTS")
    if os.path.isdir(cc):
        for d in sorted(os.listdir(cc)):
            full = os.path.join(cc, d)
            if os.path.isdir(full) and SECTOR_RE.match(d):
                counts[d] = len([f for f in os.listdir(full) if f.endswith(".md")])

    meta = {
        "n_concepts_findings": len(concepts),
        "n_masters_findings": len(masters),
        "n_total": len(defects),
        "n_sector_files": sum(counts.values()),
        "counts": counts,
        "by_checker": by_checker,
        "by_sector": by_sector,
    }
    with open(os.path.join(HERE, "_defects_meta.json"), "w", encoding="utf-8") as fh:
        json.dump({k: (dict(v) if isinstance(v, defaultdict) else v)
                   for k, v in meta.items() if k != "by_sector"}, fh,
                  ensure_ascii=False, indent=2, default=str)

    # ---- جدول ملخّص sectors للطباعة ----
    print("scope files:", meta["n_sector_files"])
    print("concepts findings:", len(concepts), " masters findings:", len(masters),
          " total:", len(defects))
    print("\n%-24s %6s %6s %6s %6s %6s %5s" %
          ("sector", "concepts", "defects", "files", "agentF", "scrF", "agents"))
    rows_out = []
    for sec, s in by_sector.items():
        af, sf = len(s["agent_files"]), len(s["script_files"])
        amin = math.ceil(af / float(PER_AGENT_MAX)) if af else 0
        amax = math.ceil(af / float(PER_AGENT_MIN)) if af else 0
        rows_out.append((s["wsum"], sec, s["n"], len(s["files"]), af, sf, amin, amax,
                         s["maxsev"], dict(s["checks"]), counts.get(sec, 0)))
    for wsum, sec, n, nf, af, sf, amin, amax, mx, ck, nc in sorted(rows_out, reverse=True):
        print("%-24s %6d %6d %6d %6d %6d %5s" %
              (sec, nc, n, nf, af, sf, ("%d-%d" % (amin, amax)) if af else "-"))
    print("\nDEFECTS.jsonl →", OUT_JSONL)
    print("meta →", os.path.join(HERE, "_defects_meta.json"))
    return by_sector, by_checker, rows_out


if __name__ == "__main__":
    main()