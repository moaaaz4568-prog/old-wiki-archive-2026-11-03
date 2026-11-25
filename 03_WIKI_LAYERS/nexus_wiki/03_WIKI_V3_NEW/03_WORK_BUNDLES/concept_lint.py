#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
concept_lint.py — فاحص مفاهيم V3 الطوبولوجي (L1..L7) · stdlib فقط · بلا أي تبعيات.

المرجع البنيوي: /root/r/V3/00_CHARTER/FORMAT_CONCEPT.md
    · أسماء الأقسام السبعة تُقرأ من الميثاق وقت التشغيل (§N `## NAME`)،
      ومجموعة احتياطية مثبّتة في SECTIONS_FALLBACK إن تعذّرت قراءة الميثاق.

الفواحص:
  L1 شوائب المحارف  CJK [\\u4e00-\\u9fff] · Cyrillic [\\u0400-\\u04ff] · Thai [\\u0e00-\\u0e7f]
                     في **المتن فقط** (ما بعد كتلة YAML)، وتُستثنى أسطر الاقتباس
                     المعلَّمة بـ`>` الأولية. كل تطابق يُبلَّغ باسم المحرف وموقعه.
                     تنبيه: الطلب ورد نطاق Thai كـ[\\u0e00-\\u7e7f]، وفيه خطأ مطبعي
                     (\\u7e7f = U+7E7F لا U+0E7F) فيبتلع العربية وCyrillic والشرطة U+2014.
                     الافتراضي هنا كتلة Thai الصحيحة، والنص الحرفي بـ--thai-range spec.
  L2 شريط YAML      FORMAT_CONCEPT §1 يقول «12 حقلاً: 11 إلزامية + name: (إلزامية بـD03)»
                     ⇒ الإلزامي 11 بلا `name` (وD03 يفحص H1 داخل L5)،
                     + `source_file_id` غير فارغ،
                     + `sector` غير فارغ. الغياب يُبلَّغ، والقائمة الفارغة `[]` قيمة
                     مشروعة لـ`atoms`/`tensions` فلا تُعدّ فراغاً.
  L3 حدود الفناء     `## حدود الفناء` موجودة + ≥3 بنود `- ` + كل بند ≥8 كلمات (عدّ بـsplit()).
  L4 الدليل          ≥3 اقتباس، وكل اقتباس يحمل `file_id` أو رقم سطر.
  L5 الأقسام السبعة  السبعة بأسمائها من الميثاق، وبالترتيب (الترتيب تحذير لا فشل).
  L6 words           القيمة في YAML تساوي `len(body.split())`، والحد 250 ≤ w ≤ 600.
  L7 wikilink        ≥1 رابط من نمط `[[Concept_...]]`، وكل رابط يُحلَّل إلى ملف حقيقي
                     بـos.path.exists (فهرس أسماء بلا .md من جذر المفاهيم).

الواجهة:
  --path <dir-or-file>   افتراضي /root/r/NB2/02_CONCEPTS
  --report               جدول L1..L7 | pass/total | file | first-3-problems
  --fail-on L1,L3        خروج 1 إن فشل أيّ من الفواحص المذكورة
  --json out.json        تصدير النتائج كاملة JSON
  --match <glob>         ترشيح اختياري على اسم الملف (أداة عرض، لا يغيّر الفحوص)
  --corpus-root <dir>    جذر حلّ روابط [[...]] (افتراضي: أب المجلد المرقَّم)
  --quiet                بلا جدول (يرافق --json فقط)
  --thai-range strict|spec   نطاق Thai في L1 (افتراضي strict = الكتلة الصحيحة)

لا يحذف ولا يكتب في /sdcard ولا يدفع. مخرجات فقط.
"""

import argparse
import fnmatch
import io
import json
import os
import re
import sys

CHARTER = "/root/r/V3/00_CHARTER/FORMAT_CONCEPT.md"
DEFAULT_PATH = "/root/r/NB2/02_CONCEPTS"

# FORMAT_CONCEPT.md §1 «12 حقلاً: 11 إلزامية + name: (إلزامية بـD03)» ⇒ الإلزامي 11 بلا name.
REQUIRED_YAML = (
    "id", "type", "version", "sector", "freq_seen", "confidence",
    "class", "atoms", "tensions", "sources", "words",
)
NON_EMPTY_YAML = ("source_file_id", "sector")

SECTIONS_FALLBACK = (
    "التعريف", "الآلية", "حدود الفناء", "الشروط", "الدليل", "المصدرية", "التوترات",
)

CHARGE_PATTERNS = (
    ("CJK", re.compile("[\u4e00-\u9fff]")),
    ("Cyrillic", re.compile("[\u0400-\u04ff]")),
    # Thai الحقيقي = الكتلة U+0E00..U+0E7F.
    # الطلب ورد النطاق [\u0e00-\u7e7f] وفيه خطأ مطبعي:
    # الطرف الأعلى \u7e7f يعني U+7E7F لا U+0E7F، فيصير المدى 29,000 نقطة
    # يبتلع العربية (06xx) و Cyrillic (04xx) والشرطة U+2014 (—) الشائعة في كل سطر
    # عربي، و CJK punctuation. لذلك الافتراضي = الكتلة الصحيحة، والنص الحرفي
    # متاح عبر --thai-range spec.
    # الدليل على القرص: 0x0e00 <= 0x2014 <= 0x7e7f  ==>  True
    ("Thai", re.compile("[\u0e00-\u0e7f]")),
)

THAI_SPEC = re.compile("[\u0e00-\u7e7f]")   # النطاق الحرفي كما ورد في الطلب

THAI_RANGE_NOTE = (
    "L1/Thai طُبِّق على الكتلة U+0E00..U+0E7F لا على النطاق الحرفي " + "[\u0e00-\u7e7f]"
    " المذكور في الطلب، لأن الحرفي يبتلع العربية و Cyrillic و U+2014 (—). "
    "لإلغاء التصحيح: --thai-range spec"
)

CH_SECTIONS = "حدود الفناء"
CH_QUOTES = "الدليل"

QUOTE_RE = re.compile(r"^\s*[-*]\s*[«\"“]")
FID_BACKTICK = re.compile(r"`([^`\n]+)`")
FID_NAME = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.\-]*\.(?:txt|md|pdf|vtt|srt|json|jsonl)")
LINE_NO = re.compile(r"(?::|：|\bline\b|\bسطر\b|\bرقم سطر\b)\s*\d+", re.I)
BULLET_RE = re.compile(r"^\s*-\s+\S")
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
WIKILINK_RE = re.compile(r"\[\[([^\]\n]+)\]\]")

WORDS_MIN = 250
WORDS_MAX = 600
FENCE_MIN_BULLETS = 3
FENCE_MIN_WORDS = 8
QUOTES_MIN = 3


# ─────────────────────────── أدوات ───────────────────────────

def read_text(path):
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def split_front_matter(text):
    """(yaml_lines, body, body_offset) — yaml_lines=[] إن لا كتلة YAML."""
    lines = text.splitlines()
    first = 0
    while first < len(lines) and not lines[first].strip():
        first += 1
    if first >= len(lines) or lines[first].strip() != "---":
        return [], lines, 0
    close = None
    for i in range(first + 1, len(lines)):
        if lines[i].strip() == "---":
            close = i
            break
    if close is None:
        return [], lines, 0
    return lines[first + 1:close], lines[close + 1:], close + 1


def parse_yaml(yaml_lines):
    """محرّل YAML سطحي: `key: value` بلا قواميس متداخلة (يحتاج PyYAML غير متاح)."""
    out = {}
    for ln in yaml_lines:
        if not ln.strip() or ln.lstrip().startswith("#") or ln.lstrip().startswith(">"):
            continue
        if ln[:1] in (" ", "\t", "-"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_.\-]*)\s*:\s*(.*)$", ln)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


def is_blank_value(v):
    return v is None or v.strip() in ("", "[]", "{}", "null", "~")


def section_text(body_lines, name):
    """نص قسم `## name` حتى القسم التالي أو نهاية المتن."""
    start = None
    for i, ln in enumerate(body_lines):
        m = H2_RE.match(ln)
        if not m:
            continue
        if m.group(1).strip() == name:
            start = i + 1
            continue
        if start is not None:
            return body_lines[start:i]
    if start is not None:
        return body_lines[start:]
    return None


def h2_order(body_lines):
    return [m.group(1).strip() for m in H2_RE.finditer("\n".join(body_lines))]


def charter_sections():
    """أسماء الأقسام السبعة من الميثاق: `### §N `## NAME``."""
    try:
        txt = read_text(CHARTER)
    except (IOError, OSError):
        return SECTIONS_FALLBACK
    names, seen = [], set()
    for m in re.finditer(r"###\s*§\s*(\d+)\s*`##\s*([^`\n]+?)\s*`", txt):
        name = m.group(2).strip()
        if name and name not in seen:
            seen.add(name)
            names.append(name)
    return tuple(names) if len(names) >= 7 else SECTIONS_FALLBACK


def build_name_index(roots):
    """فهرس أسماء ملفات .md بلا لاحقة — لاختبار os.path.exists على روابط [[...]]."""
    idx = set()
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        try:
            entries = list(os.scandir(root))
        except OSError:
            continue
        for e in entries:
            try:
                is_dir = e.is_dir(follow_symlinks=False)
            except OSError:
                continue
            if is_dir:
                if e.name == "terms_26k" or e.name.startswith((".", "_")):
                    continue
                try:
                    subs = list(os.scandir(e.path))
                except OSError:
                    continue
                for s in subs:
                    if s.name.endswith(".md"):
                        idx.add(s.name[:-3])
            elif e.name.endswith(".md"):
                idx.add(e.name[:-3])
    return idx


def clip(text, limit=150):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


# ─────────────────────────── الفواحص ───────────────────────────

def charge_patterns(thai_range):
    """--thai-range spec ⇒ النطاق الحرفي من الطلب؛ الافتراضي = كتلة Thai الصحيحة."""
    if thai_range == "spec":
        return tuple(("Thai", THAI_SPEC) if lab == "Thai" else (lab, rx)
                     for lab, rx in CHARGE_PATTERNS)
    return CHARGE_PATTERNS


def check_l1(body_lines, offset, problems, thai_range="strict"):
    for i, ln in enumerate(body_lines, 1):
        if ln.lstrip().startswith(">"):
            continue
        for label, rx in charge_patterns(thai_range):
            hits = rx.findall(ln)
            if hits:
                uniq = ", ".join(sorted(set(hits))[:6])
                problems.append("L1 %s سطر %d: [%s]" % (label, i + offset, uniq))


def check_l2(yaml_lines, problems):
    y = parse_yaml(yaml_lines)
    if not yaml_lines:
        problems.append("L2 لا كتلة YAML أصلاً")
        return y
    for key in REQUIRED_YAML:
        if key not in y:
            problems.append("L2 حقل إلزامي مفقود: %s" % key)
    for key in NON_EMPTY_YAML:
        if key not in y:
            problems.append("L2 %s مفقود" % key)
        elif is_blank_value(y[key]):
            problems.append("L2 %s فارغ" % key)
    return y


def check_l3(body_lines, problems):
    sec = section_text(body_lines, CH_SECTIONS)
    if sec is None:
        problems.append("L3 لا يوجد ## %s" % CH_SECTIONS)
        return
    bullets = [b for b in sec if BULLET_RE.match(b)]
    if len(bullets) < FENCE_MIN_BULLETS:
        problems.append("L3 بنود %d < %d" % (len(bullets), FENCE_MIN_BULLETS))
    for b in bullets:
        n = len(b.split())
        if n < FENCE_MIN_WORDS:
            problems.append("L3 بند %d كلمات < %d: %s" % (n, FENCE_MIN_WORDS, clip(b, 60)))


def check_l4(body_lines, problems):
    sec = section_text(body_lines, CH_QUOTES)
    if sec is None:
        problems.append("L4 لا يوجد ## %s" % CH_QUOTES)
        return
    quotes = [q for q in sec if QUOTE_RE.match(q)]
    if len(quotes) < QUOTES_MIN:
        problems.append("L4 اقتباسات %d < %d" % (len(quotes), QUOTES_MIN))
    for q in quotes:
        has_fid = bool(FID_BACKTICK.search(q) or FID_NAME.search(q))
        has_line = bool(LINE_NO.search(q))
        if not has_fid and not has_line:
            problems.append("L4 اقتباس بلا file_id/رقم سطر: %s" % clip(q, 70))


def check_l5(body_lines, wanted, problems, warnings):
    present = h2_order(body_lines)
    for name in wanted:
        if name not in present:
            problems.append("L5 قسم مفقود: ## %s" % name)
    seen = [s for s in present if s in wanted]
    if len(seen) == len(wanted) and tuple(seen) != tuple(wanted):
        warnings.append("ترتيب الأقسام ≠ ترتيب الميثاق: %s" % " ← ".join(seen))


def check_l6(yaml_lines, body_lines, y, problems):
    body = " ".join(body_lines)
    measured = len(body.split())
    declared = y.get("words")
    if declared is None:
        problems.append("L6 حقل words مفقود")
    elif not re.match(r"^\d+$", str(declared).strip()):
        problems.append("L6 words ليس رقماً: %r" % declared)
    elif int(declared) != measured:
        problems.append("L6 words معلن=%d ≠ مقيس=%d" % (int(declared), measured))
    if not (WORDS_MIN <= measured <= WORDS_MAX):
        problems.append("L6 الكلمات %d خارج %d..%d" % (measured, WORDS_MIN, WORDS_MAX))


def check_l7(body_lines, index, self_name, problems):
    links = [m.group(1).split("|")[0].strip() for m in WIKILINK_RE.finditer("\n".join(body_lines))]
    links = [l for l in links if l]
    concept_links = [l for l in links if l.startswith("Concept_")]
    if len(concept_links) < 1:
        problems.append("L7 لا يوجد رابط [[Concept_...]] (%d رابط آخر)" % (len(links) - len(concept_links)))
    for l in links:
        if l == self_name:
            continue
        if l not in index:
            problems.append("L7 رابط معلَّق: [[%s]] لا ملف" % l)


# ─────────────────────────── التحليل لكل ملف ───────────────────────────

def lint_file(path, wanted, index, thai_range="strict"):
    text = read_text(path)
    yaml_lines, body_lines, offset = split_front_matter(text)
    y = parse_yaml(yaml_lines)
    problems, warnings = [], []

    check_l1(body_lines, offset, problems, thai_range)
    check_l2(yaml_lines, problems)
    check_l3(body_lines, problems)
    check_l4(body_lines, problems)
    check_l5(body_lines, wanted, problems, warnings)
    check_l6(yaml_lines, body_lines, y, problems)
    check_l7(body_lines, index, os.path.splitext(os.path.basename(path))[0], problems)

    return {
        "file": os.path.basename(path),
        "path": path,
        "sector": os.path.basename(os.path.dirname(path)) or ".",
        "yaml_fields": len(y),
        "body_words": len(" ".join(body_lines).split()),
        "words_declared": y.get("words"),
        "wikilinks": len(WIKILINK_RE.findall("\n".join(body_lines))),
        "sections": h2_order(body_lines),
        "problems": problems,
        "warnings": warnings,
    }


def collect_files(target, match=None):
    if os.path.isfile(target):
        cands = [target]
    elif os.path.isdir(target):
        cands = []
        for root, dirs, names in os.walk(target):
            dirs[:] = [d for d in dirs if d != "terms_26k" and not d.startswith(".")]
            for n in sorted(names):
                if n.endswith(".md") and (n.startswith("C_") or n.startswith("Concept_")):
                    cands.append(os.path.join(root, n))
    else:
        raise SystemExit("المسار غير موجود: %s" % target)
    if match:
        cands = [p for p in cands if fnmatch.fnmatch(os.path.basename(p), match)]
    return sorted(cands)


# ─────────────────────────── العرض ───────────────────────────

LEVELS = ("L1", "L2", "L3", "L4", "L5", "L6", "L7")


def level_status(res, lvl):
    if any(p.startswith(lvl + " ") for p in res["problems"]):
        return "✗"
    return "✓"


def print_report(results, wanted, thai_range="strict"):
    name_w = max([len("file")] + [len(r["file"]) for r in results]) if results else len("file")
    name_w = min(max(name_w, 20), 46)
    head = "file".ljust(name_w) + "  " + "  ".join(LEVELS) + "   pass  first-3-problems"
    print(head)
    print("-" * len(head))
    for r in results:
        name = r["file"]
        if len(name) > name_w:
            name = name[: name_w - 1] + "…"
        marks = "  ".join(level_status(r, l) for l in LEVELS)
        passed = sum(1 for l in LEVELS if level_status(r, l) == "✓")
        first3 = r["problems"][:3]
        if not first3:
            first3 = r["warnings"][:1]
        print(name.ljust(name_w) + "  " + marks + "   %d/%d  %s" % (passed, len(LEVELS), clip(" | ".join(first3))))
    print("-" * len(head))
    agg = {}
    for l in LEVELS:
        agg[l] = sum(1 for r in results if level_status(r, l) == "✓")
    total = len(results)
    clean = sum(1 for r in results if not r["problems"])
    print("المجموع: files=%d  " % total + "  ".join("%s=%d/%d" % (l, agg[l], total) for l in LEVELS))
    print("ملفات اجتازت الفواحص السبعة كلها: %d/%d" % (clean, total))
    if wanted != SECTIONS_FALLBACK:
        print("أسماء الأقسام مقروءة من: %s" % CHARTER)
    if thai_range != "strict":
        print("⚠ L1/Thai بوضع spec: " + THAI_RANGE_NOTE)
    for r in results:
        for w in r["warnings"]:
            print("  ⚠ %s: %s" % (r["file"], w))


# ─────────────────────────── main ───────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="concept_lint.py — فاحص L1..L7 لمفاهيم V3 (stdlib فقط)",
    )
    ap.add_argument("--path", default=DEFAULT_PATH, help="مجلد أو ملف (افتراضي %s)" % DEFAULT_PATH)
    ap.add_argument("--report", action="store_true", help="جدول L1..L7 | pass/total | file | first-3-problems")
    ap.add_argument("--fail-on", default="", help="قائمة مفصولة بفواصل: L1,L3 ⇒ خروج 1 عند الفشل")
    ap.add_argument("--json", dest="json_out", default="", help="مسار تصدير JSON")
    ap.add_argument("--match", default="", help="ترشيح glob على اسم الملف")
    ap.add_argument("--corpus-root", default="", help="جذر حلّ روابط [[...]]")
    ap.add_argument("--thai-range", choices=("strict", "spec"), default="strict",
                    help="نطاق Thai في L1: strict=الكتلة U+0E00..U+0E7F (افتراضي) · "
                         "spec=النطاق الحرفي [\\u0e00-\\u7e7f] من الطلب (يبتلع العربية و —)")
    ap.add_argument("--quiet", action="store_true", help="بلا جدول")
    args = ap.parse_args(argv)

    target = os.path.abspath(args.path)
    files = collect_files(target, args.match or None)
    if not files:
        sys.stderr.write("لا ملفات C_*/Concept_* تحت %s\n" % target)
        return 2

    if args.corpus_root:
        corpus = os.path.abspath(args.corpus_root)
    else:
        base = target if os.path.isdir(target) else os.path.dirname(target)
        parent = os.path.dirname(base)
        corpus = parent if re.match(r"^\d\d_", os.path.basename(base)) else base
    index = build_name_index([target, corpus])

    wanted = charter_sections()
    results = [lint_file(p, wanted, index, args.thai_range) for p in files]

    if args.report and not args.quiet:
        print_report(results, wanted, args.thai_range)

    if args.json_out:
        payload = {
            "path": target,
            "corpus_root": corpus,
            "charter": CHARTER,
            "sections": list(wanted),
            "levels": list(LEVELS),
            "thai_range": args.thai_range,
            "thai_range_note": THAI_RANGE_NOTE if args.thai_range != "strict" else "",
            "files_scanned": len(results),
            "clean_files": sum(1 for r in results if not r["problems"]),
            "per_level_pass": {
                l: sum(1 for r in results if level_status(r, l) == "✓") for l in LEVELS
            },
            "results": results,
        }
        with io.open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        if not args.quiet:
            print("JSON → %s" % args.json_out)

    wanted_fail = [x.strip().upper() for x in args.fail_on.split(",") if x.strip()]
    unknown = [x for x in wanted_fail if x not in LEVELS]
    if unknown:
        sys.stderr.write("--fail-on:levels unknown: %s (known: %s)\n" % (",".join(unknown), ",".join(LEVELS)))
        return 2
    if wanted_fail:
        failed = [l for l in wanted_fail if any(level_status(r, l) == "✗" for r in results)]
        if failed:
            sys.stderr.write("فشل في: %s\n" % ",".join(failed))
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
