#!/usr/bin/env python3
"""route.py — أداة توجيه V3.

وضعان:

  1) `--sector <X>`   → يطبع/routes قطاعاً واحداً: ذرّاته + مفاهيمه + أجزاؤه،
                        مع المسارات الفعلية على القرص (قراءة فقط، بلا نسخ).

  2) `--check`        → يقارن `SEGMENT_MAP.json` بـ `V3_SYS/COUNTS.json`
                        ويطبع كل فرق على حدة. خروج 0 = لا فرق، 1 = فرق.

الاستعمال:
    python3 route.py --sector 01_outreach
    python3 route.py --sector 01_outreach --json
    python3 route.py --sectors
    python3 route.py --check
    python3 route.py --check --json

قاعدة: الأداة **لا تكتب** شيئاً ولا تنسخ ملفاً. `--sector` يطبع مسارات موجودة لا ينشئها.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

V3_ROOT = Path("/root/r/V3")
DEFAULT_MAPS = [
    V3_ROOT / "01_ATOMS" / "SEGMENT_MAP.json",
    V3_ROOT / "02_CONCEPTS" / "SEGMENT_MAP.json",
]
COUNTS_PATH = Path("/root/r/V3_SYS/COUNTS.json")
NB2_ROOT = Path("/root/r/NB2")

ATOMS_DIR = V3_ROOT / "01_ATOMS"
CONCEPTS_DIR = V3_ROOT / "02_CONCEPTS"
MASTERS_DIR = V3_ROOT / "03_MASTERS"
NB2_ATOMS = NB2_ROOT / "02_CONCEPTS" / "terms_26k"
NB2_CONCEPTS = NB2_ROOT / "02_CONCEPTS"

NON_SECTOR_KEYS = {"_REPORTS", "terms_26k"}


def is_sector_key(key: str) -> bool:
    return key not in NON_SECTOR_KEYS and not key.startswith("_")


def load_map(explicit: str | None) -> tuple[dict, Path]:
    candidates = [Path(explicit)] if explicit else DEFAULT_MAPS
    for c in candidates:
        if c.is_file():
            with c.open("r", encoding="utf-8") as fh:
                return json.load(fh), c
    sys.exit("FATAL: SEGMENT_MAP.json not found (looked: " + ", ".join(map(str, candidates)) + ")")


def count_md(path: Path) -> int:
    if not path.is_dir():
        return 0
    n = 0
    for p in path.rglob("*.md"):
        if p.is_file():
            n += 1
    return n


# --------------------------------------------------------------------------- sector


def cmd_sector(args) -> int:
    seg_map, map_path = load_map(args.map)
    name = args.sector

    if name not in seg_map:
        print(f"UNKNOWN sector: {name}", file=sys.stderr)
        print(f"known sectors ({len(seg_map)}): {', '.join(sorted(seg_map))}", file=sys.stderr)
        return 2

    entry = seg_map[name]
    atoms_dir = ATOMS_DIR / name
    concepts_dir = CONCEPTS_DIR / name
    nb2_atoms = NB2_ATOMS / name
    nb2_concepts = NB2_CONCEPTS / name
    master_dir = MASTERS_DIR / name

    doc = {
        "sector": name,
        "segment_map": str(map_path),
        "atoms": {
            "count": entry["atoms_count"],
            "parts": entry["atoms_parts"],
            "v3_dir": str(atoms_dir),
            "v3_dir_exists": atoms_dir.is_dir(),
            "nb2_dir": str(nb2_atoms),
            "nb2_dir_exists": nb2_atoms.is_dir(),
            "nb2_md_on_disk": count_md(nb2_atoms),
            "part_dirs": [str(nb2_atoms / p) for p in entry["atoms_parts"]],
        },
        "concepts": {
            "count": entry["concepts_count"],
            "v3_dir": str(concepts_dir),
            "v3_dir_exists": concepts_dir.is_dir(),
            "nb2_dir": str(nb2_concepts),
            "nb2_dir_exists": nb2_concepts.is_dir(),
            "nb2_md_on_disk": count_md(nb2_concepts),
        },
        "master": {
            "v3_dir": str(master_dir),
            "v3_dir_exists": master_dir.is_dir(),
            "nb2_dir": str(NB2_ROOT / "03_MASTERS" / name),
            "nb2_dir_exists": (NB2_ROOT / "03_MASTERS" / name).is_dir(),
            "nb2_md_on_disk": count_md(NB2_ROOT / "03_MASTERS" / name),
        },
        "read_only": True,
    }

    if args.json:
        print(json.dumps(doc, ensure_ascii=False, indent=2))
        return 0

    a, c, m = doc["atoms"], doc["concepts"], doc["master"]
    print(f"sector           {name}")
    print(f"segment_map      {map_path}")
    print()
    print(f"ATOMS   count={a['count']}  parts={len(a['parts'])}")
    print(f"  v3   {a['v3_dir']}  exists={a['v3_dir_exists']}")
    print(f"  nb2   {a['nb2_dir']}  exists={a['nb2_dir_exists']}  md_on_disk={a['nb2_md_on_disk']}")
    for p in a["part_dirs"]:
        print(f"        part {p}")
    print()
    print(f"CONCEPTS count={c['count']}")
    print(f"  v3   {c['v3_dir']}  exists={c['v3_dir_exists']}")
    print(f"  nb2   {c['nb2_dir']}  exists={c['nb2_dir_exists']}  md_on_disk={c['nb2_md_on_disk']}")
    print()
    print(f"MASTER  v3={m['v3_dir_exists']}  nb2={m['nb2_dir_exists']}  nb2_md_on_disk={m['nb2_md_on_disk']}")
    print()
    if a["count"] and not c["count"]:
        print("note: atom sector with no quintuple concepts (SECTOR_MAP.md §2)")
    if c["count"] and not a["count"]:
        print("note: concept sector with no atoms")
    return 0


# --------------------------------------------------------------------------- check


def cmd_check(args) -> int:
    seg_map, map_path = load_map(args.map)
    counts_path = Path(args.counts)
    if not counts_path.is_file():
        sys.exit(f"FATAL: counts file not found: {counts_path}")
    with counts_path.open("r", encoding="utf-8") as fh:
        counts = json.load(fh)

    nb2 = counts["nb2"]
    atoms_ref = nb2["terms_26k"]["sectors"]
    parts_ref = nb2["terms_26k"]["parts"]
    conc_ref = {k: v for k, v in nb2["concepts_sectors"].items() if is_sector_key(k)}

    diffs: list[str] = []

    def cmp_scalar(label: str, got, want) -> None:
        if got != want:
            diffs.append(f"{label}: segmap={got} counts={want}")

    cmp_scalar("sectors_total", len(seg_map), len(set(atoms_ref) | set(conc_ref)))
    cmp_scalar("atoms_total", sum(v["atoms_count"] for v in seg_map.values()), nb2["terms_26k"]["files"])
    cmp_scalar("atoms_parts_entries", sum(len(v["atoms_parts"]) for v in seg_map.values()), len(parts_ref))
    cmp_scalar("concepts_total", sum(v["concepts_count"] for v in seg_map.values()), sum(conc_ref.values()))

    for sector in sorted(set(atoms_ref) | set(conc_ref) | set(seg_map)):
        m = seg_map.get(sector)
        if m is None:
            diffs.append(f"{sector}: MISSING in SEGMENT_MAP")
            continue
        cmp_scalar(f"{sector}.atoms_count", m["atoms_count"], int(atoms_ref.get(sector, 0)))
        cmp_scalar(
            f"{sector}.atoms_parts",
            len(m["atoms_parts"]),
            len({k.rpartition("/")[2] for k in parts_ref if k.rpartition("/")[0] == sector}),
        )
        cmp_scalar(f"{sector}.concepts_count", m["concepts_count"], int(conc_ref.get(sector, 0)))

    if args.json:
        print(
            json.dumps(
                {
                    "segment_map": str(map_path),
                    "counts": str(counts_path),
                    "sectors": len(seg_map),
                    "atoms_total": sum(v["atoms_count"] for v in seg_map.values()),
                    "concepts_total": sum(v["concepts_count"] for v in seg_map.values()),
                    "diffs": diffs,
                    "ok": not diffs,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1 if diffs else 0

    print(f"segment_map  {map_path}")
    print(f"counts       {counts_path}")
    print(f"sectors={len(seg_map)}  atoms={sum(v['atoms_count'] for v in seg_map.values())}  "
          f"concepts={sum(v['concepts_count'] for v in seg_map.values())}")
    if not diffs:
        print("OK  0 diff(s) — SEGMENT_MAP matches COUNTS.json")
        return 0
    print(f"DIFF {len(diffs)} difference(s):")
    for d in diffs:
        print(f"  DIFF {d}")
    return 1


# --------------------------------------------------------------------------- main


def cmd_sectors(args) -> int:
    seg_map, map_path = load_map(args.map)
    print(f"segment_map {map_path}  ({len(seg_map)} sectors)")
    if args.json:
        print(json.dumps(seg_map, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print(f"{'sector':<26} {'atoms':>8} {'parts':>6} {'concepts':>9}")
    for k in sorted(seg_map):
        v = seg_map[k]
        print(f"{k:<26} {v['atoms_count']:>8} {len(v['atoms_parts']):>6} {v['concepts_count']:>9}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="أداة توجيه V3: قطاع، قوائم، وفحص تطابق")
    ap.add_argument("--sector", help="اسم القطاع (مثال: 01_outreach)")
    ap.add_argument("--sectors", action="store_true", help="اطبع كل القطاعات")
    ap.add_argument("--check", action="store_true", help="SEGMENT_MAP مقابل COUNTS.json")
    ap.add_argument("--map", help="مسار SEGMENT_MAP.json مخصّص")
    ap.add_argument("--counts", default=str(COUNTS_PATH), help="مسار COUNTS.json")
    ap.add_argument("--json", action="store_true", help="مخرج JSON")
    args = ap.parse_args()

    if args.check:
        return cmd_check(args)
    if args.sector:
        return cmd_sector(args)
    if args.sectors:
        return cmd_sectors(args)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())