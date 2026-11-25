#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_links.py — تطبيق خطة الروابط على قطاع outreach (إضافة فقط).

المهمة
------
``LINK_PLAN.jsonl`` يوفّر لكل مفهوم قائمة روابط مقترحة (مرتّبة تنازليًا بأعلى
درجة تشابه). هذا السكريبت يضيف الروابط المفقودة إلى ملفات
``02_CONCEPTS/01_outreach/*.md`` **فقط**، و**بالإضافة التيارية (append)** حصراً:

  * يفتح الملف بوضع ``'a'`` ولا يعيد كتابته من الصفر.
  * يفحص أن مؤشر الكتابة عند الحجم الأصلي (append يبدأ من EOF فقط).
  * بعد الكتابة، يعيد قراءة الملف ويثبّت أن المحتوى = الأصل البايت-بالبات
    + الكتلة المضافة (دليل صفر حذف مستقل عن git).
  * لا يعدّل سطرًا موجودًا ولا يحذف أي شيء.

السياسة: **صفر حذف — التصحيح = إضافة فقط.**

التحويل المُصدَّر (مستند إلى ``--link-form alias`` في مولّد الخطة)
-----------------------------------------------------------------
    C_<slug>   =>  02_CONCEPTS/<sector>/Concept_<slug>.md
    X_<code>   =>  05_TENSIONS/TENSION_<code>.md

ملاحظة صريحة على القرص: ملفات ``C_*.md`` = 0 مقابل 31,504 ملف
``Concept_*.md``. Obsidian يحلّ ``[[target]]`` بجذع اسم الملف فقط، فصيغة
``alias`` تنتج رابطًا معلّقًا حتمًا؛ يُصدَّر إذن جذع الملف الحقيقي.

الاستعمال
---------
  apply_links.py --dry-run                  # اعرض أول 3 ملفات قبل/بعد (لا يكتب)
  apply_links.py                            # طبّق فعليًا
  apply_links.py --limit 2                  # عالِج ملفين فقط (اختبار)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

CONCEPT_PREFIX = "Concept_"
TENSION_PREFIX = "TENSION_"
ALIAS_CONCEPT = "C_"
ALIAS_TENSION = "X_"

SECTION_HEADING = "## الروابط"

DEFAULT_NB2 = "/root/r/NB2"
DEFAULT_PLAN = "/root/r/V3/03_WORK_BUNDLES/LINK_PLAN.jsonl"
DEFAULT_SCOPE = "02_CONCEPTS/01_outreach"
SCOPE_DIRS = ("05_TENSIONS", "04_TENSIONS")  # أماكن ملفات التوتر على القرص

# الجذر: [[Target]] و [[Target|alias]] — لا نكتب alias، لكنها موجودة نظريًا
WIKILINK_RE = re.compile(r"\[\[([^\]\n]+?)(?:\|[^\]\n]*)?\]\]")
SECTION_RE = re.compile(r"^#{1,6}\s+الروابط\s*$", re.MULTILINE)


class PlanRow:
    """صف خطة واحد مُفلتر للنطاق."""

    __slots__ = ("path", "target", "proposed", "reason")

    def __init__(self, row: dict, nb2: Path) -> None:
        self.path = row["path"]
        self.target = nb2 / self.path
        self.proposed = [str(x) for x in row.get("proposed_links") or []]
        self.reason = row.get("reason", "")


class Stems:
    """فهرس جذور الملفات الحقيقية على القرص (المصدر الوحيد للصلاحية)."""

    def __init__(self) -> None:
        self.concepts: set[str] = set()
        self.tensions: set[str] = set()

    def add_concept(self, stem: str) -> None:
        self.concepts.add(stem)

    def add_tension(self, stem: str) -> None:
        self.tensions.add(stem)

    def has(self, stem: str) -> bool:
        return stem in self.concepts or stem in self.tensions

    def __contains__(self, stem: str) -> bool:
        return self.has(stem)

    def __len__(self) -> int:
        return len(self.concepts) + len(self.tensions)


def index_stems(nb2: Path) -> Stems:
    """فهرس كل جذور ``Concept_*.md`` و``TENSION_*.md`` على القرص.

    يشمل قطاع outreach نفسه: المفاهيم تربط بعضها ببعض داخل القطاع الواحد،
    واستبعاد القطاع كان يجعل كل روابطه الداخلية «غير قابلة للحلّ». استبعاد
    الملف عن نفسه يُعالَج منفصلاً عند البناء.
    """
    stems = Stems()
    concepts_root = nb2 / "02_CONCEPTS"
    if concepts_root.is_dir():
        for p in concepts_root.rglob(CONCEPT_PREFIX + "*.md"):
            stems.add_concept(p.stem)
    for d in SCOPE_DIRS:
        base = nb2 / d
        if base.is_dir():
            for p in base.glob(TENSION_PREFIX + "*.md"):
                stems.add_tension(p.stem)
    return stems


def resolve_link(link: str, stems: Stems) -> str | None:
    """حوّل اسم الخطة إلى جذع ملف حقيقي، أو ``None`` إن لم يُحلَّ."""
    if link.startswith(ALIAS_CONCEPT):
        stem = CONCEPT_PREFIX + link[len(ALIAS_CONCEPT):]
    elif link.startswith(ALIAS_TENSION):
        stem = TENSION_PREFIX + link[len(ALIAS_TENSION):]
    elif link.startswith(CONCEPT_PREFIX) or link.startswith(TENSION_PREFIX):
        stem = link
    else:
        return None
    return stem if stems.has(stem) else None


def load_plan(plan: Path, scope: str, nb2: Path) -> list[PlanRow]:
    """اقرأ JSONL وأبقِ صفوف النطاق فقط."""
    rows: list[PlanRow] = []
    with plan.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = PlanRow(json.loads(line), nb2)
            if row.path.startswith(scope + "/"):
                rows.append(row)
    rows.sort(key=lambda r: r.path)
    return rows


def existing_links(text: str) -> set[str]:
    """الروابط الموجودة أصلاً في الملف (منع التكرار)."""
    return {m.group(1) for m in WIKILINK_RE.finditer(text)}


def build_block(original: bytes, targets: list[str]) -> str:
    """الكتلة المضافة. لا تبدأ بمحتوى يعيد كتابة آخر سطر."""
    lead = "\n" if original.endswith(b"\n") else "\n\n"
    return lead + SECTION_HEADING + "\n" + "".join("- [[%s]]\n" % t for t in targets)


def ends_newline(data: bytes) -> bool:
    return data.endswith(b"\n")


def append_block(path: Path, block: str, dry_run: bool) -> int:
    """أضف الكتلة بالـappend فقط. يرجع عدد الأحرف المضافة."""
    if dry_run:
        return len(block.encode("utf-8"))
    data = path.read_bytes()
    size_before = len(data)
    block_bytes = block.encode("utf-8")
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        pos = fh.tell()
        if pos != size_before:
            raise RuntimeError(
                "%s: مؤشر الكتابة %d != الحجم الأصلي %d — رفض الكتابة"
                % (path, pos, size_before)
            )
        fh.write(block)
        fh.flush()
        os.fsync(fh.fileno())
    after = path.read_bytes()
    if not after.startswith(data):
        raise RuntimeError("%s: الأصل لم يُحفظ بايت-بالبات بعد الإضافة" % path)
    if after != data + block_bytes:
        raise RuntimeError("%s: الناتج != الأصل + الكتلة" % path)
    return len(block_bytes)


def tail_lines(text: str, n: int = 4) -> list[str]:
    lines = text.rstrip("\n").split("\n")
    return lines[-n:]


def verify_scope(nb2: Path, scope: Path) -> int:
    """افحص كل روابط النطاق: العدد، القسم، والحلّ إلى ملف حقيقي."""
    stems = index_stems(nb2)
    files = sorted(scope.glob("*.md"))
    total = 0
    with_section = 0
    unique: set[tuple[str, str]] = set()
    dangling: list[tuple[str, str]] = []
    for p in files:
        text = p.read_text(encoding="utf-8")
        hits = [m.group(1) for m in WIKILINK_RE.finditer(text)]
        total += len(hits)
        if SECTION_RE.search(text):
            with_section += 1
        for t in hits:
            unique.add((p.name, t))
            if t not in stems:
                dangling.append((p.name, t))
    print("النطاق: %s" % scope.relative_to(nb2))
    print("ملفات .md: %d  |  منها بقسم '## الروابط': %d" % (len(files), with_section))
    print("إجمالي ورود الروابط: %d  |  أهداف فريدة: %d" % (total, len({t for _, t in unique})))
    print("جذور مُفهرسة على القرص: %d" % len(stems))
    print("روابط معلّقة (لا تُحلّ ملفًا حقيقيًا): %d" % len(dangling))
    for f, t in dangling[:20]:
        print("   معلّق في %s -> [[%s]]" % (f, t))
    return 1 if dangling else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="أضف روابط الخطة إلى ملفات outreach بالإضافة فقط (صفر حذف)."
    )
    ap.add_argument("--plan", default=DEFAULT_PLAN, help="مسار LINK_PLAN.jsonl")
    ap.add_argument("--nb2", default=DEFAULT_NB2, help="جذر notebook")
    ap.add_argument(
        "--scope", default=DEFAULT_SCOPE, help="مجلد النطاق النسبي داخل nb2"
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="اعرض أول 3 ملفات قبل/بعد دون كتابة"
    )
    ap.add_argument("--limit", type=int, default=0, help="عالِج أول N ملفًا فقط")
    ap.add_argument(
        "--examples", type=int, default=3, help="عدد ملفات --dry-run المعروضة"
    )
    ap.add_argument(
        "--verify",
        action="store_true",
        help="افحص روابط النطاق (العدد والروابط المعلقة) دون كتابة، وأخرج رمز الخروج",
    )
    args = ap.parse_args(argv)

    nb2 = Path(args.nb2)
    scope_rel = args.scope.strip("/")
    scope = nb2 / scope_rel
    plan_path = Path(args.plan)

    if not scope.is_dir():
        print("خطأ: لا نطاق في %s" % scope, file=sys.stderr)
        return 2

    if args.verify:
        return verify_scope(nb2, scope)

    if not plan_path.is_file():
        print("خطأ: لا خطة في %s" % plan_path, file=sys.stderr)
        return 2

    stems = index_stems(nb2)
    rows = load_plan(plan_path, scope_rel, nb2)
    print("النطاق: %s  |  ملفات في الخطة: %d  |  جذور مُفهرسة: %d"
          % (scope_rel, len(rows), len(stems)))

    if args.limit:
        rows = rows[: args.limit]

    written = skipped = 0
    added_links = dropped_unresolvable = dropped_dup = 0
    droptargets: dict[str, list[str]] = {}
    shown = 0
    no_nl_files: list[str] = []
    failures: list[str] = []

    for row in rows:
        target = row.target
        if not target.is_file():
            failures.append("%s (لا ملف)" % row.path)
            continue
        original = target.read_bytes()
        text = original.decode("utf-8")
        have = existing_links(text)
        if SECTION_RE.search(text):
            skipped += 1
            continue

        targets: list[str] = []
        for link in row.proposed:
            stem = resolve_link(link, stems)
            if stem is None:
                dropped_unresolvable += 1
                droptargets.setdefault(row.path, []).append(link)
                continue
            if stem == target.stem:
                dropped_dup += 1
                continue
            if stem in have:
                dropped_dup += 1
                continue
            if stem in targets:
                continue
            targets.append(stem)

        if not targets:
            skipped += 1
            continue

        block = build_block(original, targets)

        if args.dry_run and shown < args.examples:
            shown += 1
            print("\n" + "=" * 74)
            print("[%d/%d] %s" % (shown, min(args.examples, len(rows)), row.path))
            print("بعد آخر سطر من الأصل (%d سطرًا):" % len(text.rstrip('\n').split('\n')))
            for ln in tail_lines(text):
                print("   | " + ln)
            print("-- الكتلة المضافة (append) --")
            for ln in block.rstrip("\n").split("\n"):
                print("   + " + ln)
            print("بعد التطبيق، آخر %d أسطر:" % max(len(targets) + 3, 4))
            for ln in tail_lines(text + block, max(len(targets) + 3, 4)):
                print("   ' " + ln)
            if not ends_newline(original):
                print("   ! الملف بلا فاصل سطر نهائي — يُكتمَل بفصل واحد (إضافة)")

        n = append_block(target, block, args.dry_run)
        if n:
            written += 1
            added_links += len(targets)
            if not ends_newline(original):
                no_nl_files.append(row.path)

    verb = "يُكتب" if args.dry_run else "كُتب"
    print("\n" + "-" * 74)
    print("الملفات %s عليها: %d" % (verb, written))
    print("الروابط %s: %d" % (verb, added_links))
    print("روابط لم تُحلّ ملفًا حقيقيًا (رُفضت): %d" % dropped_unresolvable)
    print("مستبعد (تكرار/ذاتي/القسم قائم): %d" % skipped)
    print("ملفات بلا فاصل سطر نهائي (يُكتمَل بإضافة فصل): %d" % len(no_nl_files))
    for f in no_nl_files:
        print("   - %s" % f)
    for p, links in sorted(droptargets.items()):
        print("   ! %s: %s" % (p, ", ".join(links)))
    for f in failures:
        print("خطأ: %s" % f, file=sys.stderr)
    if failures:
        return 1
    if args.dry_run:
        print("وضع --dry-run: لم تكتب أي بايت.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
