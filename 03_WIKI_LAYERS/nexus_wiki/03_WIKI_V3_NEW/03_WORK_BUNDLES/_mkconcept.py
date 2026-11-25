#!/usr/bin/env python3
# _mkconcept.py — كاتب مفهوم V3 بكتابة تدريجية (Write ثم append قسماً قسماً)
# الاستعمال:  python3 _mkconcept.py spec.json   أو   speccat spec.json
# لا يحذف أي ملف. التصحيح = إعادة كتابة الملف نفسهWriting تدرّجياً.
import io, json, os, re, sys, glob

ROOT = "/root/r/V3/02_CONCEPTS"
SECTIONS = ["التعريف", "الآلية", "حدود الفناء", "الشروط", "الدليل", "المصدرية", "التوترات"]


def body_words(text):
    """عدد كلمات المتن دون كتلة YAML — المقياس المعتمد في FORMAT_CONCEPT.md §6"""
    n = 0
    for line in text.splitlines():
        n += len(line.split())
    return n


def yaml_block(s):
    return (
        "---\n"
        "id: C_{slug}\n"
        "type: concept\n"
        "version: V3.0\n"
        "name: {name}\n"
        "sector: {sector}\n"
        "freq_seen: {freq}\n"
        "confidence: {conf}\n"
        "class: {cls}\n"
        "atoms: []\n"
        "tensions: []\n"
        "sources: [{src}]\n"
        "words: 0\n"
        "---\n"
    ).format(
        slug=s["slug"],
        name=s["name"],
        sector=s["sector"],
        freq=s.get("freq_seen", 1),
        conf=s.get("confidence", "med"),
        cls=s.get("class_", "causal"),
        src=s["source_id"],
    )


def build_sections(s):
    out = {}
    out["التعريف"] = s["definition"].strip()
    out["الآلية"] = s["mechanism"].strip()
    out["حدود الفناء"] = "\n".join("- " + b.strip() for b in s["limits"])
    out["الشروط"] = "\n".join("- " + b.strip() for b in s["conditions"])
    dl = []
    for q in s["quotes"]:
        dl.append("- «" + q[0] + "» — `" + q[1] + "`")
    dl.append(s["confidence_line"])
    if s.get("number_line"):
        dl.append(s["number_line"])
    dl.append(s["bias_line"])
    out["الدليل"] = "\n".join(dl)
    out["المصدرية"] = "\n".join(s["provenance"])
    t = s.get("tensions", "0")
    tn = s.get("tensions_note",
                "لا كيانات X_ على القرص (`find /root/r -name 'X_*.md' | wc -l` ⇒ 0)، "
                "فالتوتر يبقى مطالبةً مُوثَّقة داخل `## حدود الفناء` لا إحالة إلى كيان.")
    out["التوترات"] = t + "\n" + tn
    return out


def fix_tensions_note(tn):
    tn = tn.replace("لذلك孩子Candidate", "لذلك مطالب")
    tn = tn.replace("孩子Candidate", "مطالب")
    return tn


def emit(s):
    d = os.path.join(ROOT, s["sector"])
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "C_" + s["slug"] + ".md")
    secs = build_sections(s)
    secs["التوترات"] = fix_tensions_note(secs["التوترات"])

    # 1) Write — YAML + H1 + ## التعريف فقط
    head = yaml_block(s) + "\n# " + s["name"] + "\n\n## التعريف\n"
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(head + secs["التعريف"] + "\n")

    # 2..8) append — قسم بقسم بالترتيب
    for name in SECTIONS[1:]:
        with io.open(path, "a", encoding="utf-8") as f:
            f.write("\n## " + name + "\n" + secs[name] + "\n")

    # 9) patch words: بالقياس على القرص لا بالذاكرة
    txt = io.open(path, encoding="utf-8").read()
    parts = txt.split("---\n")
    body = txt.split("---\n", 2)[2]
    w = body_words(body)
    txt2 = re.sub(r"^words: \d+$", "words: %d" % w, txt, count=1, flags=re.M)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(txt2)

    # 10) فحص البوابات على القرص
    return verify(path, w, s)


def verify(path, w, s):
    t = io.open(path, encoding="utf-8").read()
    r = {}
    r["file"] = path
    r["sections7"] = len(re.findall(
        r"^## (?:التعريف|الآلية|حدود الفناء|الشروط|الليل|المصدرية|التوترات)$".replace("الليل", "الدليل"),
        t, flags=re.M))
    r["D02"] = 1 if re.match(r"^C_[^0-9\s][^\s]*\.md$", os.path.basename(path)) else 0
    r["D11"] = len(re.findall(r"TODO|TBD|XXX", t))
    r["total_wc"] = len(t.split())
    r["words_declared"] = int(re.search(r"^words: (\d+)$", t, flags=re.M).group(1))
    r["D04"] = r["sections7"]
    return r


def main():
    if len(sys.argv) > 1:
        data = io.open(sys.argv[1], encoding="utf-8").read()
    else:
        data = sys.stdin.read()
    specs = json.loads(data)
    if isinstance(specs, dict):
        specs = [specs]
    for s in specs:
        res = emit(s)
        note = lint(s["slug"])
        print("OK  {sections7}/7  words={total_wc} decl={words_declared}  D11={D11}  {slug}{note}".format(
            slug=s["slug"], note=("  <<< " + note if note else ""),
            **{k: res[k] for k in ("sections7", "total_wc", "words_declared", "D11")}))


CJK = re.compile(r"[\u3000-\u9fff\uff00-\uffef\u0400-\u04ff]")
AR = re.compile(r"[\u0600-\u06ff]")
LAT = re.compile(r"[A-Za-z]")


def lint(slug):
    """كاشف فوري للتلوّث النصي داخل المتن الجديد"""
    path = os.path.join(ROOT, glob_sector(slug), "C_" + slug + ".md")
    if not os.path.exists(path):
        return "missing"
    bad = []
    txt = io.open(path, encoding="utf-8").read()
    for i, line in enumerate(txt.splitlines(), 1):
        if line.startswith("- «") or line.startswith("# "):
            continue
        if re.match(r"^[A-Za-z0-9_.-]+: .+\.txt$", line) or "X_*.md" in line:
            continue
        if re.match(r"^(id|type|version|name|sector|freq_seen|confidence|class|atoms|tensions|sources|words):", line):
            continue
        if CJK.search(line):
            bad.append("L%d:CJK" % i)
        elif AR.search(line) and LAT.search(line):
            tok = re.findall(r"[A-Za-z]{2,}", line)
            bad.append("L%d:MIX(%s)" % (i, tok[0] if tok else "?"))
    return ",".join(bad)


def glob_sector(slug):
    for d in os.listdir(ROOT):
        if os.path.exists(os.path.join(ROOT, d, "C_" + slug + ".md")):
            return d
    return ""


if __name__ == "__main__":
    main()
