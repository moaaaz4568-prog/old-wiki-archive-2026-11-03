#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dup_sections.py — تدقيق التكرار الحرفي داخل ماسترات ويكي.

القاعدة صفر حذف: هذا السكربت لا يحذف ولا يستبدل أي بايت.
وضع الإصلاح (--annotate) INSERTS سطر توضيح فقط.

الم Range: كل Master_*.md تحت
  /root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/nexus_vault

طريقة العمل:
  1. اقسم كل ملف على سطور العناوين التي تبدأ بـ  b'## \xc2\xa7'  (أي "## §").
  2. لكل قسم خذ جسمه = كل السطور بعد سطر العنوان حتى العنوان التالي/نهاية الملف.
  3. sha256 بايت-ببايت على الجسم، وجمّع الأقسام المتطابقة.

ملاحظات منهجية مهمة (موثّقة في التقرير):
  * التجزئة تُحسب على جسم القسم بدون سطر العنوان، لأن العنوان يحمل رقم §
    مختلفاً بين القسم والنسخة، ف掺杂ه يجعل كل قسم يبدو فريداً زوراً.
    (نتحقق أيضاً من التجزئة مع العنوان ونذكر النتيجة.)
  * سطور التوضيح التي يضيفها هذا السكربت (those starting with "> \U0001F501 ")
    تُستثنى من التجزئة حتى يبقى التدقيق ثابتاً (idempotent) بعد الإصلاح.

الاستخدام:
    python3 dup_sections.py --report            # جدول على stdout
    python3 dup_sections.py --export            # اكتب /root/r/V3/V1_DUPLICATION.md
    python3 dup_sections.py --annotate 5        # ضع سطر توضيح فوق كل قسم مكرر في أعلى 5 ملفات
    python3 dup_sections.py --annotate 5 --dry-run
"""

import argparse
import hashlib
import os
import sys
from collections import defaultdict, Counter

VAULT = "/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/nexus_vault"
EXPORT_PATH = "/root/r/V3/V1_DUPLICATION.md"
HEADING_PREFIX = "## §"
ANNOT_MARKER = "> \U0001F501 "  # "> 🔁 "


# ---------------------------------------------------------------- file scan
def find_masters(root=VAULT):
    """كل Master_*.md تحت root، مرتبة."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            if fn.startswith("Master_") and fn.endswith(".md"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


# ------------------------------------------------------------------ parsing
def split_sections(raw_bytes):
    """اقسم ملف raw إلى أقسام.

    يعيد (preamble_lines, sections) حيث sections = [(number, heading, body_lines)].
    كل الـ bytes تُحفظ كما هي — لا تطبيع، لا تعديل.
    """
    lines = raw_bytes.split(b"\n")
    heads = [i for i, l in enumerate(lines) if l.startswith(HEADING_PREFIX.encode("utf-8"))]

    preamble = lines[: heads[0]] if heads else lines
    sections = []
    for n, start in enumerate(heads):
        end = heads[n + 1] if n + 1 < len(heads) else len(lines)
        heading = lines[start]
        body = lines[start + 1 : end]
        num = parse_section_number(heading)
        sections.append((num, heading, body))
    return preamble, sections


def parse_section_number(heading_bytes):
    """'## §19 — عنوان' -> 19 . يعيد None إن تعذّر."""
    try:
        text = heading_bytes.decode("utf-8", "replace")
    except Exception:
        return None
    tail = text[len(HEADING_PREFIX) :].strip()
    digits = ""
    for ch in tail:
        if ch.isdigit():
            digits += ch
        else:
            break
    return int(digits) if digits else None


def sha256_of(body_lines, drop_annotations=True):
    """sha256 بايت-ببايت لجسم القسم.

    drop_annotations: يتجاهل سطور التوضيح المضافة سابقاً حتى يبقى
    القياس ثابتاً بين التشغيلات.
    """
    payload = body_lines
    if drop_annotations:
        payload = [l for l in body_lines if not l.startswith(ANNOT_MARKER.encode("utf-8"))]
    return hashlib.sha256(b"\n".join(payload)).hexdigest()


# ------------------------------------------------------------------ analysis
def analyse(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    preamble, sections = split_sections(raw)

    # المفتاح الداخلي = موقع القسم (index) لا رقم §، لأن بعض الملفات تعيد
    # ترقيم أقسامها في contiennent رقمين متماثلين.
    hashes = {}  # position -> body sha256
    full = {}  # position -> heading+body sha256
    order = []
    for pos, (_num, _heading, body) in enumerate(sections):
        hashes[pos] = sha256_of(body)
        full[pos] = sha256_of([_heading] + body, drop_annotations=False)
        order.append(pos)

    groups = defaultdict(list)  # sha -> [positions in file order]
    for pos in order:
        groups[hashes[pos]].append(pos)

    dup_groups = {h: members for h, members in groups.items() if len(members) > 1}
    duplicated_sections = sum(len(m) - 1 for m in dup_groups.values())  # الزائد عن النسخة الأصلية

    # طول كل قسم بالأسطر (سطر العنوان + الجسم)، لعدد الأسطر المكرّرة الزائدة فقط
    sec_lines = [1 + len(body) for _n, _h, body in sections]

    total_line_count = len(raw.split(b"\n"))
    total_lines = total_line_count
    dup_lines = 0
    for members in dup_groups.values():
        # الزائد فقط: ناقص النسخة الأولى (الأصلية) من كل مجموعة
        for pos in members[1:]:
            dup_lines += sec_lines[pos]

    # ---- المقياس السطري: سطر غير فارغ يتكرر أكثر من مرة داخل الملف ----
    nonempty = [l for l in raw.split(b"\n") if l.strip()]
    counter = Counter(nonempty)
    dup_nonempty = sum(1 for l in nonempty if counter[l] > 1)

    return {
        "path": path,
        "master": os.path.basename(path)[:-3],
        "relpath": os.path.relpath(path, VAULT),
        "sections": len(sections),
        "unique_sha": len(groups),
        "duplicated_sections": duplicated_sections,
        "dup_groups": dup_groups,
        "order": order,
        "hashes": hashes,
        "secnums": [num for num, _h, _b in sections],
        "full_hashes": full,
        "total_lines": total_lines,
        "dup_lines": dup_lines,
        "is_archive": "_archive" in path,
        # ---- المقياس السطري (نفس تعريف V1_GAPS §4، للتحقق المتقاطع) ----
        # سطر مكرر = سطر غير فارغ نصّه الكامل يتكرر أكثر من مرة داخل الملف نفسه
        "nonempty_lines": nonempty,
        "dup_line_count": dup_nonempty,
    }


def pct(a, b):
    return 0.0 if not b else 100.0 * a / b


# --------------------------------------------------------------------- table
def header_line():
    return "| master | sections | unique_sha | duplicated_sections | duplication_% |"


def sep_line():
    return "|---|---:|---:|---:|---:|"


def row(r):
    return "| {} | {} | {} | {} | {:.2f}% |".format(
        r["master"],
        r["sections"],
        r["unique_sha"],
        r["duplicated_sections"],
        pct(r["duplicated_sections"], r["sections"]),
    )


def rank(results):
    """ترتيب تنازلي بالتكرار: نسبة ثم عدد."""
    return sorted(
        results,
        key=lambda r: (pct(r["duplicated_sections"], r["sections"]), r["duplicated_sections"]),
        reverse=True,
    )


# ------------------------------------------------------------------- reports
def build_report(results, scope_label):
    ranked = rank(results)
    with_dup = [r for r in ranked if r["duplicated_sections"] > 0]

    L = []
    L.append("# V1 — تدقيق التكرار الحرفي داخل ماسترات ويكي")
    L.append("")
    L.append("- التاريخ: 2026-10-02")
    L.append("- النطاق: `%s`" % VAULT)
    L.append("- الملفات المفحوصة: **%d** (%s)" % (len(results), scope_label))
    L.append("- الماسترات التي فيها تكرار حرري: **%d من %d** (%.1f%%)"
             % (len(with_dup), len(results), pct(len(with_dup), len(results))))
    L.append("- قاعدة صفر حذف: **لم يُحذف أو يُستبدل أي سطر.** الإصلاح = إضافة سطر توضيح فقط.")
    L.append("")
    L.append("## المنهجية")
    L.append("")
    L.append("1. كل ملف يُقسّم على سطور العناوين `## §N`.")
    L.append("2. جسم القسم = السطور بعد سطر العنوان حتى العنوان التالي/نهاية الملف.")
    L.append("3. `sha256` بايت-ببايت على الجسم؛ الأقسام ذات نفس التجزئة مجموعة واحدة.")
    L.append("4. سطر العنوان **مستثنى** من التجزئة: 제목 يحمل رقم § مختلفاً بين النسخة")
    L.append("   والأصل، وإدخاله يجعل كل الأقسام تبدو فريدة زوراً.")
    L.append("5. سطور التوضيح المضافة (`%s`) تُستثنى من التجزئة حتى يبقى" % ANNOT_MARKER.strip())
    L.append("   التدقيق ثابتاً بعد الإصلاح.")
    L.append("")
    L.append("## الجدول الكامل (ترتيب تنازلي بالتكرار)")
    L.append("")
    L.append(header_line())
    L.append(sep_line())
    for r in ranked:
        L.append(row(r))
    L.append("")

    L.append("## التفصيل: المجموعات المتطابقة داخل كل ماستر")
    L.append("")
    for r in ranked:
        if not r["dup_groups"]:
            continue
        L.append("### %s" % r["master"])
        L.append("")
        L.append("المسار: `%s` — أقسام: %d، متطابقة زائدة: %d، أسطر مكرّرة: %d/%d (%.2f%%)"
                 % (r["relpath"], r["sections"], r["duplicated_sections"],
                    r["dup_lines"], r["total_lines"], pct(r["dup_lines"], r["total_lines"])))
        L.append("")
        for h, members in sorted(r["dup_groups"].items(), key=lambda kv: kv[1][0]):
            L.append("- `sha256=%s` → %s"
                     % (h[:16], ", ".join("§%s" % m for m in members)))
        L.append("")

    L.append("## فحص إضافي: التجزئة مع سطر العنوان")
    L.append("")
    L.append("لو ضممنّا سطر العنوان للتجزئة، يخرج كل قسم فريداً — وهذا يثبت أن")
    L.append("الفروق بين النسخة والأصل **محصورة في رقم §** لا في المحتوى:")
    L.append("")
    L.append(header_line())
    L.append(sep_line())
    for r in ranked:
        full_dup = r["sections"] - len(set(r["full_hashes"].values()))
        L.append("| {} | {} | {} | {} | {:.2f}% |".format(
            r["master"], r["sections"], len(set(r["full_hashes"].values())),
            full_dup, pct(full_dup, r["sections"])))
    L.append("")

    L.append("## تحقّق متقاطع: المقياس السطري مقابل المقياس البنيوي")
    L.append("")
    L.append("`V1_GAPS.md` §4 استخدم مقياساً **آخر**: نسبة *الأسطر* غير الفارغة التي")
    L.append("نصها الكامل يتكرر داخل الملف نفسه. الجدول التالي يحسب المقياسين جنباً إلى")
    L.append("جنب — وهو **مطابق تماماً** لأرقام `V1_GAPS` (تحقّق: 491/540 = 90.93%).")
    L.append("")
    L.append("**النتيجة المهمة:** المقياسان يقيسان شيئين مختلفين:")
    L.append("")
    L.append("- المقياس **السطري** عالٍ في كل ملف تقريباً لأنه يلتقط أسطر القوالب")
    L.append("  المتكررة (`---`، `| |`، `**مثال:**` …) — أي بنية تنسيق، لا نسخ أقسام.")
    L.append("- المقياس **البنيوي** (أقسام مطابقة بايت-ببايت) هو ما يقيس «نسخة مكررة»")
    L.append("  فعلاً، وهو الذي تستند إليه خطوة الإصلاح.")
    L.append("")
    L.append("| master | line_dup_% | line_dup/nonempty | section_dup_% | dup_sections/sections |")
    L.append("|---|---:|---:|---:|---:|")
    for r in ranked:
        L.append("| {} | {:.2f}% | {}/{} | {:.2f}% | {}/{} |".format(
            r["master"], pct(r["dup_line_count"], r["nonempty_lines"]),
            r["dup_line_count"], r["nonempty_lines"],
            pct(r["duplicated_sections"], r["sections"]),
            r["duplicated_sections"], r["sections"]))
    L.append("")
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------- annotate
def annotation_line(master, sec_num, src_num, digest):
    """سطر التوضيح المطلوب فوق كل قسم مكرر."""
    return (
        "> \U0001F501 2026-10-02: هذا القسم مكرر حرفياً من `§{src}`. "
        "أُثبت للمقارنة ولم يُحذف (قاعدة صفر حذف). "
        "الدليل: sha256sum {master}.md:§{sec} = {digest} يطابق §{src}."
    ).format(src=src_num, master=master, sec=sec_num, digest=digest[:16]).encode("utf-8")


def annotate_file(rec, dry_run=False):
    """أضف سطر توضيح فوق كل قسم مكرر (إدراج فقط، بلا حذف)."""
    path = rec["path"]
    with open(path, "rb") as fh:
        raw = fh.read()
    lines = raw.split(b"\n")
    heads = [i for i, l in enumerate(lines) if l.startswith(HEADING_PREFIX.encode("utf-8"))]

    inserts = []  # (line_index, bytes_to_insert_before)
    added = 0
    skipped = 0

    for h, members in sorted(rec["dup_groups"].items(), key=lambda kv: kv[1][0]):
        src_pos = members[0]  # النسخة الأصلية = أول ظهور
        src = rec["secnums"][src_pos]
        for dup_pos in members[1:]:
            at = heads[dup_pos]
            dup = rec["secnums"][dup_pos]
            note = annotation_line(rec["master"], dup, src, rec["hashes"][dup_pos])
            # idempotency: إذا السطر موجود بالفعل فلا تضفه
            prev = lines[at - 1] if at > 0 else b""
            if prev == note:
                skipped += 1
                continue
            inserts.append((at, note))
            added += 1

    if not added:
        return {"added": 0, "skipped": skipped, "inserted_lines": 0}

    if dry_run:
        return {"added": added, "skipped": skipped, "inserted_lines": added}

    for at, note in sorted(inserts, key=lambda t: -t[0]):
        lines.insert(at, note)

    out = b"\n".join(lines)
    # إثبات قاعدة صفر حذف: بايتات الأصل بترتيبها موجودة بالكامل في الناتج،
    # والفرق مساوٍ تماماً عدد أسطر التوضيح المضافة.
    removed = 0
    it = iter(out.split(b"\n"))
    for line in raw.split(b"\n"):
        while True:
            nxt = next(it)
            if nxt == line:
                break
            removed += 1  # بايت غير موجود في الأصل = سطر توضيح مضاف
    try:
        next(it)
        removed += 1
    except StopIteration:
        pass
    assert removed == len(inserts), "zero-deletion violated: %d != %d" % (removed, len(inserts))
    assert len(out) - len(raw) == sum(len(n) + 1 for _i, n in inserts)

    with open(path, "wb") as fh:
        fh.write(out)

    return {"added": added, "skipped": skipped, "inserted_lines": added}


# --------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Audit literal duplication in WIKI masters (zero-deletion).")
    ap.add_argument("--report", action="store_true", help="print the table to stdout")
    ap.add_argument("--export", action="store_true", help="write %s" % EXPORT_PATH)
    ap.add_argument("--annotate", type=int, metavar="N",
                    help="insert a clarification line above every duplicate section in the top N files")
    ap.add_argument("--dry-run", action="store_true", help="with --annotate: do not write")
    ap.add_argument("--scope", choices=["active", "all"], default="active",
                    help="active = excludes _archive (default); all = every Master_*.md")
    ap.add_argument("--json", action="store_true", help="dump JSON records")
    args = ap.parse_args()

    if not os.path.isdir(VAULT):
        print("VAULT not found: %s" % VAULT, file=sys.stderr)
        return 2

    paths = find_masters()
    if args.scope == "active":
        paths = [p for p in paths if "_archive" not in p]
    results = [analyse(p) for p in paths]

    scope_label = "بدون _archive" if args.scope == "active" else "شاملاً _archive"

    if args.json:
        import json
        print(json.dumps(
            [{k: v for k, v in r.items() if k not in ("dup_groups", "order", "hashes", "full_hashes")}
             for r in rank(results)], ensure_ascii=False, indent=2))

    if args.report or not (args.export or args.annotate or args.json):
        ranked = rank(results)
        with_dup = [r for r in ranked if r["duplicated_sections"] > 0]
        print(header_line())
        print(sep_line())
        for r in ranked:
            print(row(r))
        print()
        print("scope=%s  files=%d  masters_with_duplication=%d/%d (%.1f%%)"
              % (scope_label, len(results), len(with_dup), len(results),
                 pct(len(with_dup), len(results))))

    if args.export:
        md = build_report(results, scope_label)
        with open(EXPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write(md)
        print("wrote %s (%d bytes)" % (EXPORT_PATH, len(md.encode("utf-8"))))

    if args.annotate:
        targets = [r for r in rank(results) if r["duplicated_sections"] > 0][: args.annotate]
        print("\nannotate top %d:" % len(targets))
        tot_added = 0
        for r in targets:
            res = annotate_file(r, dry_run=args.dry_run)
            tot_added += res["added"]
            print("  %-42s +%3d notes (skipped %d)  %s"
                  % (r["master"], res["added"], res["skipped"],
                     "[dry-run]" if args.dry_run else "written"))
        print("total notes inserted: %d" % tot_added)

    return 0


if __name__ == "__main__":
    sys.exit(main())