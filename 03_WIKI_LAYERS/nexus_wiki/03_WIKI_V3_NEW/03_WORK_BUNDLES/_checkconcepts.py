#!/usr/bin/env python3
# _checkconcepts.py — فحص بوابات D01..D11 على كل مفهوم E9 على القرص
import io, os, re, glob, sys

SRC = {
    "transcript_full_1.txt": "/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/brain/processed/transcript_full_1.txt",
    "The 3 Stages of Your Personal Brand (Full Course).txt":
        "/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/brain/processed/The 3 Stages of Your Personal Brand (Full Course).txt",
}
SRC_CACHE = {}
for k, v in SRC.items():
    SRC_CACHE[k] = io.open(v, encoding="utf-8", errors="replace").read()

files = sorted(glob.glob("/root/r/V3/02_CONCEPTS/*/C_*.md"))
fails = []
stat = dict(files=0, quotes=0, words=0, sectors={})


def sec(txt, name):
    m = re.search(r"^## " + name + r"\n(.*?)(?=^## |\Z)", txt, flags=re.M | re.S)
    return m.group(1) if m else ""


for f in files:
    txt = io.open(f, encoding="utf-8").read()
    b = os.path.basename(f)
    sector = os.path.basename(os.path.dirname(f))
    stat["files"] += 1
    stat["sectors"][sector] = stat["sectors"].get(sector, 0) + 1
    stat["words"] += len(txt.split())
    err = []

    # D01
    if not re.search(r"^type: concept$", txt, flags=re.M):
        err.append("D01 type")
    if not b.startswith("C_"):
        err.append("D01 prefix")
    if not sector.startswith(("01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_", "1",
                              "2")):
        err.append("D01 folder")
    m = re.search(r"^sector: (.+)$", txt, flags=re.M)
    if not m or m.group(1).strip() != sector:
        err.append("D01 sector==folder")
    # D02
    if not re.match(r"^C_[^0-9\s][^\s]*\.md$", b):
        err.append("D02 name")
    if re.search(r"^id: C_", txt, flags=re.M) and not re.search(
            r"^id: (.+)$", txt, flags=re.M).group(1) == b[:-3]:
        err.append("D02 id==file")
    # D03
    if not re.search(r"^name: .+·.+", txt, flags=re.M):
        err.append("D03 name")
    if not re.search(r"^# .+·.+", txt, flags=re.M):
        err.append("D03 H1")
    # D04 = 7
    n = len(re.findall(r"^## (?:التعريف|الآلية|حدود الفناء|الشروط|الدليل|المصدرية|التوترات)$",
                       txt, flags=re.M))
    if n != 7:
        err.append("D04 sections=%d" % n)
    order = [x for x in re.findall(r"^## (.+)$", txt, flags=re.M)]
    if order != ["التعريف", "الآلية", "حدود الفناء", "الشروط", "الدليل", "المصدرية", "التوترات"]:
        err.append("D04 order")
    # D05
    lim = sec(txt, "حدود الفناء")
    lw = len(lim.split())
    if lw < 40 or lw > 120:
        err.append("D05 words=%d" % lw)
    bl = [x for x in lim.splitlines() if x.startswith("- ")]
    if len(bl) < 3:
        err.append("D05 bullets=%d" % len(bl))
    for x in bl:
        if len(x.split()) < 8:
            err.append("D05 bullet<8w")
        if len(x.split()) > 45:
            err.append("D05 bullet>45w")
    # D06
    mech = sec(txt, "الآلية")
    mw = len(mech.split())
    if mw < 80:
        err.append("D06 words=%d" % mw)
    if len(re.findall(r"لأن|لذلك|لذا|فينهار|إذاً|إن كان", mech)) < 1:
        err.append("D06 no-causal")
    if len(re.findall(r"^(اسأل|اكتب|أرسل|استخدم|طبّق)", mech, flags=re.M)) != 0:
        err.append("D06 imperative")
    # D07
    if len(re.findall(r"^sources(_channels)?: *\[\]$", txt, flags=re.M)) != 0:
        err.append("D07 empty sources")
    # D08
    q = [x for x in sec(txt, "الدليل").splitlines() if x.startswith("- «")]
    stat["quotes"] += len(q)
    if len(q) < 3:
        err.append("D08 quotes=%d" % len(q))
    for x in q:
        qt = re.match(r"^- «(.*)» — `(.+)`$", x)
        if not qt:
            err.append("D08 shape")
            continue
        text, fid = qt.group(1), qt.group(2)
        if len(text.split()) > 60:
            err.append("D08 quote>60w")
        if fid not in SRC_CACHE:
            err.append("D08 unknown file_id")
        elif text not in SRC_CACHE[fid]:
            err.append("D08 NOT-VERBATIM")
    dl = sec(txt, "الدليل")
    if "درجة الثقة:" not in dl:
        err.append("D08 confidence line")
    if "⚠️ تحيز المصدر:" not in dl:
        err.append("D08 bias line")
    # D09 -- لا wikilink مطلوب في v3 (D09 يقيس رابطاً صادراً؛ التوترات 0/1..5)
    tsec = sec(txt, "التوترات")
    if len(re.findall(r"^- ", tsec, flags=re.M)) != 0:
        err.append("§7 surface bullets")
    x5 = len(re.findall(r"\[\[X_[^\]]+\]\]", tsec))
    if x5 > 5:
        err.append("§7 X_>5")
    if not re.search(r"^tensions: \[\]$", txt, flags=re.M):
        err.append("§7 tensions field")
    # D10
    w = len(txt.split())
    if w < 250 or w > 600:
        err.append("D10 wc=%d" % w)
    # D11
    if len(re.findall(r"TODO|TBD|XXX", txt)):
        err.append("D11 placeholder")
    # words: مطابق للقياس
    m = re.search(r"^words: (\d+)$", txt, flags=re.M)
    body = txt.split("---\n", 2)[2]
    bw = len(body.split())
    if not m or int(m.group(1)) != bw:
        err.append("words decl=%s meas=%d" % (m.group(1) if m else "?", bw))
    # atoms
    if not re.search(r"^atoms: \[\]$", txt, flags=re.M):
        err.append("atoms field")
    if err:
        fails.append((f, err))

print("FILES=%d  QUOTES=%d  TOTAL_WORDS=%d" % (stat["files"], stat["quotes"], stat["words"]))
print("SECTORS: " + ", ".join("%s=%d" % (k, v) for k, v in sorted(stat["sectors"].items())))
print("FAILING=%d" % len(fails))
for f, e in fails:
    print("  " + f.split("/")[-1] + " :: " + ", ".join(e))
sys.exit(0 if not fails else 2)
