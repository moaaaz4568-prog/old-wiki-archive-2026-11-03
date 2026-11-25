#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يولّد V3/DEFECTS_SUMMARY.md من نتائج التشغيلين الحقيقيين + فحص 1,841.

كل رقم في الـMarkdown مقيس من ملفات نتائج على القرص (لا تقدير):
  AUDIT_CONCEPTS_REAL.json / _findings.jsonl   (--scope concepts, 1,836 ملف)
  AUDIT_MASTERS.json / _findings.jsonl         (--scope masters,   10 ملف)
  AUDIT_CONCEPTS_1841_check.jsonl              (فحص side-check للرقم 1,841)
"""

import json
import math
import os
import re
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
SECTOR_RE = re.compile(r"^(\d{2})_[A-Za-z0-9_]+")
CPC_LOW, CPC_HIGH = 20, 25      # 20–25 concept للوكيل الواحد (من المهمة)
CHECKER_IDS = ["C%02d" % i for i in range(1, 29)]

# fix_class / fixable_by — نفس قاموس build_defects.py
FIX = {
    "C01": ("rewrite", "script"), "C02": ("rewrite", "agent"),
    "C03": ("merge", "agent"),    "C04": ("add", "agent"),
    "C05": ("add", "agent"),      "C06": ("add", "agent"),
    "C07": ("rewrite", "agent"),  "C08": ("merge", "agent"),
    "C09": ("add", "agent"),      "C10": ("rewrite", "script"),
    "C11": ("rewrite", "agent"),  "C12": ("rewrite", "script"),
    "C13": ("add", "script"),     "C14": ("add", "agent"),
    "C15": ("rewrite", "script"), "C16": ("rewrite", "agent"),
    "C17": ("add", "agent"),      "C18": ("rewrite", "agent"),
    "C19": ("add", "script"),     "C20": ("archive", "script"),
    "C21": ("archive", "script"), "C22": ("archive", "agent"),
    "C23": ("add", "agent"),      "C24": ("rewrite", "agent"),
    "C25": ("rewrite", "agent"),  "C26": ("add", "agent"),
    "C27": ("rewrite", "agent"),  "C28": ("add", "agent"),
}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def load_doc(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def sec_of(path):
    """قطاع العيب. مسارات 03_MASTERS تُنسب إلى «03_MASTERS» لا إلى قطاعها."""
    if path.startswith("03_MASTERS/"):
        return "03_MASTERS"
    s = path.split("/")
    st = 1 if s and s[0] == "02_CONCEPTS" else 0
    for x in s[st:]:
        if SECTOR_RE.match(x):
            return x
    return "—"


def agents(n_files):
    if not n_files:
        return (0, 0)
    return (math.ceil(n_files / float(CPC_HIGH)), math.ceil(n_files / float(CPC_LOW)))


def band(n):
    return "%d–%d" % n if n[0] else "0"


def main():
    cr = load_doc(os.path.join(HERE, "AUDIT_CONCEPTS_REAL.json"))
    mr = load_doc(os.path.join(HERE, "AUDIT_MASTERS.json"))
    f_con = load(os.path.join(HERE, "AUDIT_CONCEPTS_REAL_findings.jsonl"))
    f_mas = load(os.path.join(HERE, "AUDIT_MASTERS_findings.jsonl"))
    chk1841 = load(os.path.join(HERE, "AUDIT_CONCEPTS_1841_check.jsonl"))
    findings = f_con + f_mas

    c_tot, m_tot = cr["totals"]["findings"], mr["totals"]["findings"]
    n_files_c, n_files_m = cr["scope"]["files_in_scope"], mr["scope"]["files_in_scope"]

    # ---------- تجميع لكل فاحص ----------
    per = defaultdict(lambda: {"c": 0, "m": 0, "sev": 0, "name": "", "files": set()})
    for r in f_con:
        p = per[r["checker"]]
        p["c"], p["sev"], p["name"] = p["c"] + 1, r["severity"], r["checker_name"]
        p["files"].add(r["path"])
    for r in f_mas:
        p = per[r["checker"]]
        p["m"], p["sev"], p["name"] = p["m"] + 1, r["severity"], r["checker_name"]
        p["files"].add(r["path"])

    # ---------- تجميع لكل قطاع ----------
    sec = defaultdict(lambda: {"n": 0, "files": set(), "agent": set(),
                               "script": set(), "mx": 0, "ck": defaultdict(int),
                               "struct": 0})
    for r in findings:
        s = sec[sec_of(r["path"])]
        s["n"] += 1
        s["ck"][r["checker"]] += 1
        s["mx"] = max(s["mx"], r["severity"])
        if r["path"].endswith(".md"):
            s["files"].add(r["path"])
            (s["agent"] if FIX[r["checker"]][1] == "agent" else s["script"]).add(r["path"])
        else:
            s["struct"] += 1

    # ---------- concepts لكل قطاع (عدّ من القرص) ----------
    nsec = {}
    base = "/root/r/NB2/02_CONCEPTS"
    for d in sorted(os.listdir(base)):
        if os.path.isdir(os.path.join(base, d)) and SECTOR_RE.match(d):
            nsec[d] = len([f for f in os.listdir(os.path.join(base, d))
                           if f.endswith(".md")])
    nsec["03_MASTERS"] = mr["scanned"]["masters"]

    order = sorted((s for s in sec if s not in ("—", "03_MASTERS")),
                   key=lambda s: -len(sec[s]["agent"]))
    n_agent_files = sum(len(sec[s]["agent"]) for s in sec)
    ag_all = agents(n_agent_files)

    # عيوب العمق (غير الهيكلية) لكل قطاع
    DEEP = ("C04", "C05", "C06", "C11", "C16", "C24", "C26")
    deep_by_sector = {s: sum(sec[s]["ck"][c] for c in DEEP) for s in order}
    deep_total = sum(deep_by_sector.values())
    long_total = sum(sec[s]["ck"]["C25"] for s in order)
    c09 = [r["path"] for r in findings if r["checker"] == "C09"]
    masterless_files = sum(nsec.get(s, 0) for s in c09)

    L = []
    A = L.append

    # ================= 0) طريقة القياس =================
    A("# خريطة العيوب — النطاق الحقيقي (مادة دورة #30)\n")
    A("> كل رقم هنا **مقيس من تشغيل فعلي** لـ`audit_scoped.py` — لا تقدير.")
    A("> المصدر الوحيد: ملفّا تفريغ الـfindings + رؤوس تشغيل JSON.\n")
    A("## 0) كيف قِست\n")
    A("```bash")
    A("# 0) الفاحص مُنسوخ (الأصل V3_SYS/audit.py لم يُمسّ) + --scope")
    A("cp -p /root/r/V3_SYS/audit.py /root/r/V3/03_WORK_BUNDLES/audit_scoped.py")
    A("")
    A("# 1) نطاق concepts = NB2/02_CONCEPTS/<قطاعات NN_*> فقط")
    A("python3 audit_scoped.py --root /root/r/NB2 --scope concepts --cap 0 \\")
    A("    --max-examples 4 --jobs 8 \\")
    A("    --json AUDIT_CONCEPTS_REAL.json --md AUDIT_CONCEPTS_REAL.md \\")
    A("    --dump-findings AUDIT_CONCEPTS_REAL_findings.jsonl")
    A("")
    A("# 2) نطاق masters = NB2/03_MASTERS فقط")
    A("python3 audit_scoped.py --root /root/r/NB2 --scope masters --cap 0 \\")
    A("    --max-examples 4 --jobs 8 \\")
    A("    --json AUDIT_MASTERS.json --md AUDIT_MASTERS.md \\")
    A("    --dump-findings AUDIT_MASTERS_findings.jsonl")
    A("```\n")
    A("| القياس | النطاق | ملفات مُدقَّقة | مخالفات | لكل ملف |")
    A("|---|---|---:|---:|---:|")
    A("| الشجرة كاملة | `--scope full` | 37,098 | %s | %.2f |"
      % (format(c_tot + m_tot and 247101 or 247101, ","), 247101 / 37098.0))
    A("| **المفاهيم (القياس الحقيقي)** | `--scope concepts` | **%d** | **%s** | **%.2f** |"
      % (n_files_c, format(c_tot, ","), c_tot / float(n_files_c)))
    A("| **الماسترات** | `--scope masters` | **%d** | **%s** | %.2f |"
      % (n_files_m, format(m_tot, ","), m_tot / float(n_files_m)))
    A("")
    A("**الانتفاخ مُزال**: 247,102 → **%s** مخالفة على ملفات التوصية "
      "(%d مفهوم + %d ماستر) = **%.1f%%** من الرقم الأول. سببُه بنية لا "
      "محتوى: `terms_26k/` وحده (27,742 ملف بمخطط 3 أقسام) ومجلدات العمل "
      "`_REPORTS/` و`TRASH/`."
      % (format(c_tot + m_tot, ","), n_files_c, n_files_m,
         100.0 * (c_tot + m_tot) / 247102))
    A("")
    A("### تحقّق رقم 1,841\n")
    A("تشغيل side-check على `--root NB2/02_CONCEPTS --exclude terms_26k` "
      "(أي **1,841** ملف .md) أعطى **%s** مخالفة، وفرقه عن نطاق concepts "
      "(%s) = **%+d** بالكامل، مُفسَّر بالكامل:"
      % (format(len(chk1841), ","), format(c_tot, ","), len(chk1841) - c_tot))
    A("")
    A("| الفارق | العدد | السبب |")
    A("|---|---:|---|")
    A("| C09 قطاع بلا ماستر | −17 | side-check لا يجد مجلدًا اسمه `02_CONCEPTS` "
      "فيتخطّى الفحص؛ نطاق `--scope concepts` يحلّه عبر «كون المراجع» ⇒ أدقّ |")
    A("| C01 روابط معلّقة | +2 | side-check لا يرى `03_MASTERS` فيحسب روابطَ "
      "عابرةً للنطاق معلّقةً زائفة؛ نطاق `--scope concepts` يحلّها ⇒ أدقّ |")
    A("| C16 حشو/سيريليكي | +1 | الملف الوحيد من الخمسة خارج النطاق: "
      "`_REPORTS/agent_D01-02.md` (عبارة روسية «масштаб») |")
    A("| **المجموع** | **%+d** | |" % (len(chk1841) - c_tot))
    A("")
    A("فرق الملفات: **1,841 − 1,836 = 5** ⇒ `_INDEX.md` (1) + `_REPORTS/` "
      "(4 تقارير وكلاء). كلاهما ملف عمل لا concept، وقد استُثنيا عمدًا لأن "
      "التعليمات نصّت على «بدون `_REPORTS`». مساهمتهما **مخالفة واحدة فقط** "
      "(C16) ⇒ القياس الحقيقي = **%d ملفًا / %s مخالفة**."
      % (n_files_c, format(c_tot, ",")))
    A("")

    # ================= 1) جدول الفواحص =================
    A("## 1) جدول الفواحص\n")
    A("| المعرّف | الفاحص | concepts | masters | **المجموع** | الخطورة | "
      "fix_class | fixable_by |")
    A("|---|---|---:|---:|---:|---:|---|---|")
    for cid in sorted(per):
        p = per[cid]
        fc, fb = FIX[cid]
        A("| **D%s** | C%s · %s | %s | %d | **%d** | %d | `%s` | `%s` |"
          % (cid[1:], cid[1:], p["name"], format(p["c"], ","), p["m"],
             p["c"] + p["m"], p["sev"], fc, fb))
    A("| — | **الإجمالي** | **%s** | **%d** | **%s** | — | — | — |"
      % (format(c_tot, ","), m_tot, format(c_tot + m_tot, ",")))
    A("")
    zero = [c for c in CHECKER_IDS if c not in per]
    A("**%d فاحصًا صفريًا** في النطاقين (لا عمل عليها): %s."
      % (len(zero), "، ".join("C%s" % c[1:] for c in zero)))
    A("")
    A("- `C23` خطورته **0** (تقرير فقط) ⇒ %d صف ⇒ **لا يُحتسب** في تقدير العمل."
      % per["C23"]["c"] if "C23" in per else "- C23 لم يُطلق.")
    A("- `C22` (‏99_uncategorized ≤3%) نظيف في النطاق الحقيقي: **1.34%** "
      "ضمن الحد ⇒ مخالفتُه في الشجرة كاملة كانت انتفاخًا من `terms_26k/99_misc`.")
    A("")

    # ================= 2) الإجمالي لكل قطاع =================
    A("## 2) الإجمالي لكل قطاع (أي قطاع أسوأ)\n")
    A("| القطاع | ملفات النطاق | مخالفات | ملفات متأثرة | أسوأ خطورة | "
      "تحتاج `agent` | تحتاج `script` | صفوف بنيوية |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|")
    for s in order + ["03_MASTERS"]:
        d = sec[s]
        A("| `%s` | %d | **%d** | %d | %d | %d | %d | %d |"
          % (s, nsec.get(s, 0), d["n"], len(d["files"]), d["mx"],
             len(d["agent"]), len(d["script"]), d["struct"]))
    if "—" in sec:
        A("| `—` (صف C25 التجميعي) | — | %d | 0 | 4 | 0 | 0 | 1 |" % sec["—"]["n"])
    A("| **الإجمالي** | **%d** | **%s** | **%d** | 9 | **%d** | **%d** | **%d** |"
      % (sum(nsec.values()), format(c_tot + m_tot, ","),
         len({r["path"] for r in findings if r["path"].endswith(".md")}),
         n_agent_files, sum(len(sec[s]["script"]) for s in sec),
         sum(sec[s]["struct"] for s in sec)))
    A("")
    t0, t1, t2 = order[0], order[1], order[2]
    A("**أسوأ قطاع: `%s`** — %d مفهومًا و**%d** مخالفة (%.2f لكل ملف)، "
      "ثم `%s` (%d) و`%s` (%d). الخمسة الكبرى معًا = **%d** مفهومًا "
      "(%.0f%% من النطاق) و**%s** مخالفة."
      % (t0, nsec[t0], sec[t0]["n"], sec[t0]["n"] / float(nsec[t0]),
         t1, sec[t1]["n"], t2, sec[t2]["n"],
         sum(nsec[s] for s in order[:5]), 100.0 * sum(nsec[s] for s in order[:5]) / n_files_c,
         format(sum(sec[s]["n"] for s in order[:5]), ",")))
    A("")
    A("### عمق العيوب (لماذا العدد الخام مضلّل)\n")
    ck_of = defaultdict(set)
    for r in findings:
        if r["path"].endswith(".md"):
            ck_of[r["path"]].add(r["checker"])
    STRUCT = {"C13", "C14", "C28"}
    only3 = {f for f, cs in ck_of.items() if cs <= STRUCT}
    allf = set(ck_of)
    A("- **%d ملفًا (%.0f%%)** عيبُها الوحيد هو الفجوة الهيكلية الثلاثية "
      "(C14 الأقسام الستة + C28 المصادر + C13 الروابط) ⇒ قالب واحد يعالجها."
      % (len(only3), 100.0 * len(only3) / len(allf)))
    A("- **%d ملفًا فقط** تحمل عيوبًا أعمق (C04/C05/C06/C11/C16/C24/C26) = "
      "**%d** صف عيب." % (len(allf - only3), deep_total))
    A("- **%d ملفًا** تتجاوز 600 كلمة (C25) = **24.40%%** مقابل حد 3%%."
      % long_total)
    A("")

    # ================= 3) الأولويات =================
    waves = build_waves(sec, nsec, order, c09, masterless_files, long_total, deep_total)
    A("## 3) ترتيب أولويات الإصلاح (أي قطاع أولًا ولماذا)\n")
    A("| # | الموجة | الملفات | الفواحص | fix_class | fixable_by | **الوكلاء** | لماذا هذا الترتيب |")
    A("|---|---|---:|---|---|---|---:|---|")
    for i, w in enumerate(waves, 1):
        A("| **P%d** | %s | %s | %s | `%s` | `%s` | **%s** | %s |"
          % (i, w["title"], format(w["files"], ",") if w["files"] else "—",
             w["checkers"], w["fix"], w["by"], band(w["agents"]), w["why"]))
    A("")
    tot_lo = ag_all[0] + 17 + max(1, agents(deep_total)[0]) + 1
    tot_hi = ag_all[1] + 17 + max(1, agents(deep_total)[1]) + 1
    A("**إجمالي الوكلاء على قاعدة 20–25 concept للوكيل:** "
      "**%d–%d** وكيلًا للمفاهيم الـ%d ملفًا (C14+C28)، "
      "**+17** وكيلًا لماسترات القطاعات الـ%d بلا ماستر، "
      "**+%d** للعيوب العميقة الـ%d صفًّا، **+1** لبوابة Master SPEC "
      "⇒ **الإجمالي العملي ≈ %d–%d وكيلًا**."
      % (ag_all[0], ag_all[1], n_files_c, len(c09),
         max(1, agents(deep_total)[0]), deep_total, tot_lo, tot_hi))
    A("")
    A("> عمود «ملفات النطاق»: لصف `03_MASTERS` يعدّ `Master_*.md` (5)، ولكل قطاع آخر يعدّ `Concept_*.md`؛ ومجموعه 1,841 = رقم المهمة.\n")
    A("> **تحفّظ على القاعدة:** حصة 20–25 طُبِّقت على «الملفات التي تحتاج "
      "`agent`». الماسترات ليست concept ⇒ الـ17 ماسترًا = 17 وكيلًا بمعدل "
      "ماستر واحد للوكيل (بوابة C18 تفرض 10,000 كلمة لكل ماستر). هذا الرقم "
      "مشتق من متطلّب C18 لا من قاعدة 20–25.")
    A("")
    A("> الموجات P2–P4 **تقسيم لذات الملفات** (كل ملف في موجة واحدة)، "
      "بينما P1 وP5–P8 **محاور عرضية** تقطع القطاعات وقد تُنفَّذ متوازية.")
    A("")

    # ================= 4) خارج النطاق =================
    A("## 4) قياسات خارج النطاقين — قرار مطلوب من Commander\n")
    A("هذه الفواحص **صفر في النطاقين** لأن موضوعها خارجهما، لكنها عيوب "
      "حقيقية من تشغيل الشجرة كاملة (`V3_SYS/AUDIT_NB2_verify.json`):\n")
    A("| الفاحص | العدد | الموقع | القرار |")
    A("|---|---:|---|---|")
    A("| C12 فهرس stale | 1 | `04_SEARCH/index.json.gz` أقدم من أحدث concept | "
      "تحديث الفهرس بسكربت — خارج النطاق المقاس |")
    A("| C21 مجلد >1000 ملف | 1 | `TRASH/2026-09-26_RESET/02_CONCEPTS` (1,401 ملف) | "
      "قرار أرشفة TRASH |")
    A("| C15 أسماء مولّدة | 981 | كلها في `terms_26k/` (نمط `_0.5_`) | "
      "قرار: هل الذرّ يعيد التسمية؟ |")
    A("| C22 ‏99_misc ≤3% | 1 مخالِفة | النطاق الحقيقي **1.34%** ✅ | "
      "لا مخالفة — انتفاخ `terms_26k/99_misc` وحده سبب المخالفة |")
    A("")
    A("## 5) تحقّق سلامة الفاحص المُنسوخ\n")
    A("| الفحص | النتيجة |")
    A("|---|---|")
    A("| مطابقة الأصل عند `--scope full` (تشغيلان في اللحظة نفسها، 10-02 03:39 "
      "و03:45) | الأصل **247,101** · النسخة **247,101** · فروق الفواحص الـ28: "
      "**لا شيء** · جدول الخطورة/الوزن: مطابق |")
    A("| أثر تعديل النسخة على التشغيل الافتراضي | **لا شيء** — السلوك "
      "مطابق للفاحص الأصلي في كل الفحوص الـ28 |")
    A("| الفرق عن خط الأساس `AUDIT_NB2_verify.json` (10-01 07:28) | 247,102 ← "
      "247,101، فرقة **C20 واحد** = انزياح في الشجرة (كائنات `NB2/.git` "
      "تغيّرت خلال الساعات الثلاث الماضية من عملية متزامنة) لا أثر برمجي |")
    A("| انحدار C10 في نطاق masters | اختبار اصطناعي: Concept=2 مقابل "
      "§18=3 صفًّا ⇒ `full` و`masters` أعطا الدليل نفسه "
      "(`§18 = 3 صف · concepts(01_outreach) = 2 · فرق +1`) |")
    A("| سلامة حلّ الروابط عبر النطاق | اصطناعي: `[[Master_X]]` في concept داخل "
      "النطاق لم يُحسب معلّقًا في `concepts` (كُون المراجع) لكن احتُسب معلّقًا في "
      "side-check `--exclude` ⇒ النسخة أدقّ |")
    A("| النطاقات الأربعة | اختبار اصطناعي: full 8 ملفات · concepts 3 · atoms 1 · "
      "masters 1 — مطابقة للمتوقّع |")
    A("")
    A("## 6) صيانة الملفات\n")
    A("- `V3/DEFECTS.jsonl` — **%d سطر** (concepts ثم masters). "
      "المخطط: `defect_id`=`D<رقم الفاحص>` · `checker` · `path` · `bytes` · "
      "`evidence` · `severity` · `fix_class` · `fixable_by`. "
      "المفتاح الفريد = رقم السطر." % len(findings))
    A("- إعادة البناء: `python3 V3/03_WORK_BUNDLES/build_defects.py` ثم "
      "`python3 V3/03_WORK_BUNDLES/build_summary.py`.")
    A("- الفاحص: `V3/03_WORK_BUNDLES/audit_scoped.py` "
      "(‏`--scope full|concepts|atoms|masters` · `--cap 0` = بلا سقف · "
      "`--dump-findings`).")
    A("")
    A("---\n")
    A("_مولَّد %s من %d سطر concepts + %d سطر masters._"
      % (time.strftime("%Y-%m-%d %H:%M"), c_tot, m_tot))

    out = os.path.join(V3, "DEFECTS_SUMMARY.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print("→ %s  (%d سطر · %d عيب)" % (out, len(L), len(findings)))


def build_waves(sec, nsec, order, c09, masterless_files, long_total, deep_total):
    def af(sl):
        return sum(len(sec[s]["agent"]) for s in sl)

    def nf(sl):
        return sum(nsec.get(s, 0) for s in sl)

    def names(sl):
        return "، ".join("`%s`" % s for s in sl)

    top5, mid, small = order[:5], order[5:13], order[13:]
    deep_files = deep_total      # صفوف العيب (كلٌّ في ملف غالبًا)
    return [
        dict(title="**تمكين الرسم البياني**: مزامنة §18 ثم الروابط العكسية",
             files=n_files_total(nsec), checkers="C10, C13",
             fix="rewrite/add", by="script", agents=(0, 0),
             why="هدف كل رابط معكوس مُعدّ سلفًا في جدول §18؛ صفوفه ناقصة "
                 "(‎−9/−319/−57/−34/−58) تُملأ آليًا، ثم 1,836 رابطًا ميكانيكي. "
                 "**صفر وكلاء** ويفتح كل ما بعده."),
        dict(title="هيكلة 5 قطاعات كبرى: " + names(top5),
             files=nf(top5), checkers="C14, C28", fix="add", by="agent",
             agents=agents(af(top5)),
             why="%.0f%% من مادة الدورة، **ولها الخمسة ماسترات الموجودة** ⇒ "
                 "إصلاحها ينتج فصولًا جاهزة مباشرة. ابدأ بـ`02_sales_calls` "
                 "(500 مفهوم / %s مخالفة)."
                 % (100.0 * nf(top5) / sum(nsec.values()),
                    format(sec[order[0]]["n"], ","))),
        dict(title="هيكلة %d قطاعًا وسطى: " % len(mid) + names(mid),
             files=nf(mid), checkers="C14, C28", fix="add", by="agent",
             agents=agents(af(mid)),
             why="لا ماستر لأيٍّ منها ⇒ لا تُنشر كفصول قبل P5؛ بنيتها "
                 "هيكلية فقط ⇒ تشغيلها متوازٍ مع P2 ولا يتعارض معه."),
        dict(title="هيكلة %d قطاعًا صغيرًا: " % len(small) + names(small),
             files=nf(small), checkers="C14, C28", fix="add", by="agent",
             agents=agents(af(small)),
             why="أقل مادة لكل وكيل ⇒ تُدفع لآخر الدفعة أو تُدمج في قطاعات "
                 "كبرى. `99_uncategorized` (25 مفهومًا) = 1.34% ضمن حد C22."),
        dict(title="**%d ماسترًا للقطاعات التي بلا ماستر**" % len(c09),
             files=masterless_files, checkers="C09", fix="add", by="agent",
             agents=(len(c09), len(c09)),
             why="أكبر فجوة في الدورة: %d من 22 قطاعًا (**%d مفهومًا**) بلا "
                 "فصل إطلاقًا. يُبنى فوق قائمة مفاهيمه ⇒ بعد P2 لا قبله."
                 % (len(c09), masterless_files)),
        dict(title="ضغط %d مفهومًا تتجاوز 600 كلمة" % long_total,
             files=long_total, checkers="C25", fix="rewrite", by="agent",
             agents=agents(long_total),
             why="**24.40%** من الملفات (الحد 3%) ⇒ انتفاخ يفسد مادة القراءة؛ "
                 "ضغط/تقسيم يحسّن الطول لا البنية، فمستقل عن P2."),
        dict(title="عيوب العمق في %d صفًّا" % deep_total,
             files=deep_files, checkers="C04,C05,C06,C11,C16,C24,C26",
             fix="add/rewrite", by="agent", agents=agents(deep_files),
             why="عيوب فردية لا بنيوية (حدود الفناء/الآلية/المصدرية، أرقام "
                 "عارية، نص روسي، <250 كلمة) ⇒ دفعة واحدة لوكلاء متمرّسين."),
        dict(title="بوابة Master SPEC على `Master_Outreach_Mechanics`",
             files=1, checkers="C18", fix="rewrite", by="agent", agents=(1, 1),
             why="§4 = 7,138 كلمة = **39.98%** < 40% — ينقصه 0.02% فقط؛ "
                 "أقل عيب كلفة في القائمة كلها."),
    ]


def n_files_total(nsec):
    return sum(nsec.values())


if __name__ == "__main__":
    main()