#!/usr/bin/env python3
"""build_segment_map.py — ولّد SEGMENT_MAP.json من العدّاد المرجعي.

المصدر الوحيد للأرقام: /root/r/V3_SYS/COUNTS.json (مولَّد بـ V3_SYS/count.py).
لا يُمسح القرص ولا تُنسخ أي ملف — هذا سكربت قراءة فقط + كتابة JSON.

الصيغة المُخرَجة (مطابقة للتكليف حرفياً، بلا مفاتيح زائدة):

    {
      "<sector>": {
        "atoms_count":    <int>,
        "atoms_parts":    ["part_01", ...],
        "concepts_count": <int>
      },
      ...
    }

منطق الدمج:
  · الذرّات   ← nb2.terms_26k.sectors  (عدد)  +  nb2.terms_26k.parts (مفاتيح "sector/part_NN")
  · المفاهيم  ← nb2.concepts_sectors  بعد استبعاد المفاتيح غير-القطاعية
                (`_REPORTS`, `terms_26k`, وأي مفتاح يبدأ بـ `_`)
  · مفتاح القطاع = اتحاد مفتاحَي الطبقتين.
    ⇒ 7 قطاعات ذرّات بلا قطاع مفاهيم (concepts_count = 0)،
      و0 قطاعات مفاهيم بلا قطاع ذرّات (كما في SECTOR_MAP.md §2).

الاستعمال:
    python3 build_segment_map.py                       # يكتب المخرجين الافتراضيين
    python3 build_segment_map.py --out /tmp/map.json    # مخرج واحد مخصّص
    python3 build_segment_map.py --print               # يطبع بلا كتابة
    python3 build_segment_map.py --check               # مقارنة المخرج بـ COUNTS.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

V3_ROOT = Path("/root/r/V3")
COUNTS_PATH = Path("/root/r/V3_SYS/COUNTS.json")
DEFAULT_OUTS = [
    V3_ROOT / "01_ATOMS" / "SEGMENT_MAP.json",
    V3_ROOT / "02_CONCEPTS" / "SEGMENT_MAP.json",
]

# مفاتيح concepts_sectors التي ليست قطاعات
NON_SECTOR_KEYS = {"_REPORTS", "terms_26k"}


def is_sector_key(key: str) -> bool:
    """قطاع = مفتاح لا يبدأ بـ `_` وليس من المفاتيح الخاصة."""
    if key in NON_SECTOR_KEYS:
        return False
    return not key.startswith("_")


def load_counts(path: Path) -> dict:
    if not path.is_file():
        sys.exit(f"FATAL: counts file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def build(counts: dict) -> dict:
    nb2 = counts["nb2"]

    atoms_total = nb2["terms_26k"]["sectors"]
    atom_parts_raw = nb2["terms_26k"]["parts"]
    concepts_raw = nb2["concepts_sectors"]

    # parts: {"01_outreach/part_01": 900, ...}  →  {sector: {part, ...}}
    parts_by_sector: dict[str, set[str]] = {}
    for key in atom_parts_raw:
        sector, _, part = key.rpartition("/")
        if not sector or not part:
            continue
        parts_by_sector.setdefault(sector, set()).add(part)

    sectors = set(atoms_total) | {k for k in concepts_raw if is_sector_key(k)}

    seg_map: dict[str, dict] = {}
    for sector in sorted(sectors):
        seg_map[sector] = {
            "atoms_count": int(atoms_total.get(sector, 0)),
            "atoms_parts": sorted(parts_by_sector.get(sector, ())),
            "concepts_count": int(concepts_raw.get(sector, 0)),
        }
    return seg_map


def write_out(seg_map: dict, outs: list[Path]) -> list[Path]:
    payload = json.dumps(seg_map, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    written = []
    for out in outs:
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as fh:
            fh.write(payload)
        written.append(out)
    return written


def check(seg_map: dict, counts: dict) -> int:
    """قارن SEGMENT_MAP مع العدّاد واطبع الفروقات. 0 = لا فرق."""
    nb2 = counts["nb2"]
    atoms_total = nb2["terms_26k"]["sectors"]
    concepts_raw = {k: v for k, v in nb2["concepts_sectors"].items() if is_sector_key(k)}

    parts_raw = nb2["terms_26k"]["parts"]
    ref_sectors = set(atoms_total) | set(concepts_raw)

    map_atoms = sum(v["atoms_count"] for v in seg_map.values())
    map_parts = sum(len(v["atoms_parts"]) for v in seg_map.values())
    map_concepts = sum(v["concepts_count"] for v in seg_map.values())

    # كل ذرّة تنتمي إلى جزء واحد بالضبط ⇒ atoms_total == terms_26k.files
    # وكل مفتاح "sector/part" يظهر مرة واحدة ⇒ عدد الأقسام == len(parts_raw)
    rows = [
        ("sectors", len(seg_map), len(ref_sectors)),
        ("atoms_total", map_atoms, nb2["terms_26k"]["files"]),
        ("atoms_parts_entries", map_parts, len(parts_raw)),
        ("concepts_total", map_concepts, sum(concepts_raw.values())),
    ]

    diffs = 0
    for label, got, want in rows:
        if got != want:
            diffs += 1
        print(f"{'OK ' if got == want else 'DIFF'} {label:<20} segmap={got:<8} counts={want}")

    # فروقات لكل قطاع على حدة
    for sector in sorted(ref_sectors | set(seg_map)):
        m = seg_map.get(sector)
        if m is None:
            print(f"DIFF missing_sector         {sector}")
            diffs += 1
            continue
        want_atoms = int(atoms_total.get(sector, 0))
        want_parts = len(
            {k.rpartition("/")[2] for k in parts_raw if k.rpartition("/")[0] == sector}
        )
        want_conc = int(concepts_raw.get(sector, 0))
        for field, got, want in (
            ("atoms_count", m["atoms_count"], want_atoms),
            ("atoms_parts", len(m["atoms_parts"]), want_parts),
            ("concepts_count", m["concepts_count"], want_conc),
        ):
            if got != want:
                print(f"DIFF {sector}.{field:<14} segmap={got} counts={want}")
                diffs += 1

    print(f"-- check: {diffs} diff(s)")
    return diffs


def scaffold(seg_map: dict) -> list[Path]:
    """أنشئ مجلدات القطاعات في 01_ATOMS/ و 02_CONCEPTS/ (فارغة + .gitkeep).

    لا يُنسخ أي ملف .md — مجلد فارغ + .gitkeep فقط (قاعدة «لا تنسخ 29,585 ملفاً»).
    · 01_ATOMS/   ⇒ القطاعات التي لها ذرّات   (atoms_count > 0)
    · 02_CONCEPTS/⇒ القطاعات التي لها مفاهيم (concepts_count > 0)
    """
    made = []
    for layer, key in (("01_ATOMS", "atoms_count"), ("02_CONCEPTS", "concepts_count")):
        root = V3_ROOT / layer
        for sector in sorted(seg_map):
            if seg_map[sector][key] <= 0:
                continue
            d = root / sector
            d.mkdir(parents=True, exist_ok=True)
            keep = d / ".gitkeep"
            if not keep.exists():
                keep.write_text("", encoding="utf-8")
            made.append(d)
    return made


def main() -> int:
    ap = argparse.ArgumentParser(description="ولّد SEGMENT_MAP.json من V3_SYS/COUNTS.json")
    ap.add_argument("--counts", default=str(COUNTS_PATH), help="مسار COUNTS.json")
    ap.add_argument("--out", action="append", default=None, help="مخرج مخصّص (قابل للتكرار)")
    ap.add_argument("--print", dest="do_print", action="store_true", help="اطبع بلا كتابة")
    ap.add_argument("--check", action="store_true", help="قارن مع العدّاد بعد البناء")
    ap.add_argument(
        "--scaffold", action="store_true", help="أنشئ مجلدات القطاعات + .gitkeep في 01_ATOMS و 02_CONCEPTS"
    )
    args = ap.parse_args()

    counts = load_counts(Path(args.counts))
    seg_map = build(counts)

    if args.do_print:
        print(json.dumps(seg_map, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        outs = [Path(p) for p in args.out] if args.out else DEFAULT_OUTS
        for p in write_out(seg_map, outs):
            print(f"wrote {p}")

    if args.scaffold:
        made = scaffold(seg_map)
        print(f"scaffold: {len(made)} sector dir(s) + .gitkeep")

    print(
        f"sectors={len(seg_map)} "
        f"atoms={sum(v['atoms_count'] for v in seg_map.values())} "
        f"concepts={sum(v['concepts_count'] for v in seg_map.values())}"
    )

    if args.check:
        return 1 if check(seg_map, counts) else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())