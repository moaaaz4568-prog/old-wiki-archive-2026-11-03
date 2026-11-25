#!/usr/bin/env python3
"""Build a TF-IDF search index for Nexus Brain.

Originally indexed <repo>/{01_TERMS,02_CONCEPTS,03_MASTERS,00_SYSTEMS} and wrote
<repo>/04_SEARCH/index.json.gz. Two defects made it produce a broken engine:

  1. SOURCE and OUTPUT were both derived from the tool's own location, and
     `documents[].path` was stored *relative to that root*. Consumers
     (search.py / query.py) then resolved those relative paths against the
     caller's cwd, so previews came back empty and file reads returned None.
  2. The 2026-09-26 build ran against the pre-reorganisation layout, so the
     stored paths are flat `02_CONCEPTS/Concept_*.md` entries that no longer
     exist -- 27,745 of 28,250 dangling -- while the 23 sector directories,
     _REPORTS and 03_MASTERS were indexed nowhere at all.

Changes in this copy (see REBUILD_REPORT.md):
  * SOURCE_ROOT (read-only corpus) and OUTPUT_PATH (generated index) are now
    independent, and are taken from nexus_config.py / the environment.
  * `documents[].path` is stored ABSOLUTE, plus `rel_path` for readability, and
    a `root` key records the corpus the index was built from.
  * File reads run on a bounded ThreadPoolExecutor (default 8 workers).
  * Memory is bounded: raw text and per-token lists are never retained. Each
    document keeps only a compact array of (term_id, count) pairs, and the
    JSON is streamed to disk instead of being materialised as one dict+string.

Zero external dependencies -- Python stdlib only.

Usage:
  python3 build_index.py
  NEXUS_SOURCE_ROOT=/path/corpus NEXUS_INDEX_PATH=/path/out.json.gz python3 build_index.py
"""

import gzip
import json
import math
import os
import re
import sys
import time
from array import array
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nexus_config import (  # noqa: E402
    FILE_GLOBS,
    MIN_SIZE,
    OUTPUT_PATH_FALLBACK,
    SOURCE_DIRS,
    SOURCE_ROOT,
    WORKERS,
)

TOKEN_PATTERN = re.compile(r"[^\w\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+")

OUTPUT_PATH = os.environ.get("NEXUS_INDEX_PATH") or OUTPUT_PATH_FALLBACK
BATCH_SIZE = 2000  # bounds how much work is queued ahead of consumption


def tokenize(text: str) -> list:
    text = text.lower()
    tokens = TOKEN_PATTERN.split(text)
    return [t for t in tokens if t and len(t) > 1]


def collect_files() -> list[tuple[str, str]]:
    """Enumerate every indexable .md under each source subtree.

    Returns (kind, abspath) sorted for a deterministic build.
    """
    found: list[tuple[str, str]] = []
    for kind, src_dir in SOURCE_DIRS:
        if not os.path.isdir(src_dir):
            print(f"  ! missing source dir, skipped: {src_dir}")
            continue
        seen: set[str] = set()
        for pattern in FILE_GLOBS:
            # os.walk instead of glob.glob('**'): one directory traversal
            # instead of two overlapping glob walks over ~30k files.
            for dirpath, dirnames, filenames in os.walk(src_dir):
                dirnames.sort()
                for name in filenames:
                    if not name.endswith(".md") or name == "manifest.json":
                        continue
                    full = os.path.join(dirpath, name)
                    if full in seen:
                        continue
                    seen.add(full)
                    found.append((kind, full))
    found.sort(key=lambda item: item[1])
    return found


class Vocabulary:
    """Incremental term -> id map with document frequency.

    Ids are assigned on first sight so per-document vectors can hold plain ints
    instead of ~30M duplicated Python string objects.
    """

    def __init__(self) -> None:
        self.terms: list[str] = []
        self.ids: dict[str, int] = {}
        self.doc_freq: array = array("i")

    def id_of(self, term: str) -> int:
        tid = self.ids.get(term)
        if tid is None:
            tid = len(self.terms)
            self.ids[term] = tid
            self.terms.append(term)
            self.doc_freq.append(0)
        return tid

    def bump(self, tid: int) -> None:
        self.doc_freq[tid] += 1


def index_one(job: tuple[str, str, int]) -> tuple[int, str, str, int, array, array, int]:
    """Read + tokenize one document. Returns compact, text-free data."""
    kind, fpath, position = job
    try:
        size = os.path.getsize(fpath)
    except OSError as exc:
        print(f"  Skipping {os.path.basename(fpath)}: {exc}")
        return None
    try:
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError as exc:
        print(f"  Skipping {os.path.basename(fpath)}: {exc}")
        return None

    tokens = tokenize(content)
    total = len(tokens)
    counts = Counter(tokens)
    del tokens

    return (
        position,
        kind,
        fpath,
        size,
        array("i", (vocab.id_of(t) for t in counts)),  # term ids
        array("i", list(counts.values())),               # counts
        total,
    )


def build_index() -> dict:
    t0 = time.time()
    print(f"Source root : {SOURCE_ROOT}")
    print(f"Output      : {OUTPUT_PATH}")
    print(f"Workers     : {WORKERS}")
    print()

    candidates = collect_files()
    print(f"Candidate .md files: {len(candidates)}")

    # Size filter first so we never read content we will discard.
    jobs: list[tuple[str, str, int]] = []
    documents: list[dict] = []
    too_small = 0
    for kind, fpath in candidates:
        try:
            size = os.path.getsize(fpath)
        except OSError:
            too_small += 1
            continue
        if size < MIN_SIZE:
            too_small += 1
            continue
        position = len(documents)
        documents.append(
            {
                "kind": kind,
                "path": fpath,                                     # absolute, openable
                "rel_path": os.path.relpath(fpath, SOURCE_ROOT),    # readability only
                "title": os.path.basename(fpath),
                "size_bytes": size,
            }
        )
        jobs.append((kind, fpath, position))
    print(f"Indexed     : {len(documents)} files (skipped {too_small} under {MIN_SIZE}B / unreadable)")

    global vocab
    vocab = Vocabulary()

    # Per-document compact vectors, filled in place by document position.
    term_ids: list[array | None] = [None] * len(documents)
    term_counts: list[array | None] = [None] * len(documents)
    totals: list[int] = [0] * len(documents)

    read = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for start in range(0, len(jobs), BATCH_SIZE):
            batch = jobs[start:start + BATCH_SIZE]
            for result in pool.map(index_one, batch):
                if result is None:
                    continue
                position, _kind, _fpath, _size, ids, counts, total = result
                for tid in ids:
                    vocab.bump(tid)
                term_ids[position] = ids
                term_counts[position] = counts
                totals[position] = total
                read += 1
            if read and read % 5000 < len(batch):
                print(f"  ... {read}/{len(jobs)} files ({time.time() - t0:.1f}s)")

    t_read = time.time()
    print(f"Read+tokenized {read} files in {t_read - t0:.1f}s")
    print(f"Vocabulary size: {len(vocab.terms)} (docs: {len(documents)})")

    # Preserve the original vocabulary ordering: most frequent first, then
    # alphabetical. perm[old_id] = new_id.
    order = sorted(range(len(vocab.terms)), key=lambda i: (-vocab.doc_freq[i], vocab.terms[i]))
    perm = array("i", [0] * len(order))
    for new_id, old_id in enumerate(order):
        perm[old_id] = new_id

    vocab_size = len(order)
    N = len(documents)
    terms_sorted = [vocab.terms[i] for i in order]
    idf = [0.0] * vocab_size
    for new_id, old_id in enumerate(order):
        idf[new_id] = math.log(N / vocab.doc_freq[old_id]) if vocab.doc_freq[old_id] else 0.0

    del vocab.ids  # no longer needed; the sorted term list replaces it

    # Free the raw corpora references before writing.
    del candidates, jobs

    t_vec = time.time()
    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    built = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())

    # Streamed JSON: never materialise the whole index as one dict or one string.
    tmp_path = OUTPUT_PATH + ".tmp"
    with gzip.open(tmp_path, "wt", encoding="utf-8", compresslevel=6) as f:
        f.write("{")
        f.write('"built":' + json.dumps(built))
        f.write(',"root":' + json.dumps(SOURCE_ROOT))
        f.write(',"repo":' + json.dumps(SOURCE_ROOT))  # legacy key, kept for add_links/planner
        f.write(',"documents":[')
        for i, doc in enumerate(documents):
            if i:
                f.write(",")
            f.write(json.dumps(doc, ensure_ascii=False))
        f.write('],"vocab_size":' + str(vocab_size))
        f.write(',"vocab":{')
        for i, term in enumerate(terms_sorted):
            if i:
                f.write(",")
            f.write(json.dumps(term, ensure_ascii=False) + ":" + str(i))
        f.write('},"idf":[')
        f.write(",".join(repr(x) for x in idf))
        f.write('],"doc_vectors":[')
        for i in range(N):
            if i:
                f.write(",")
            ids = term_ids[i]
            cnts = term_counts[i]
            total = totals[i]
            if not ids or not total:
                f.write('{"tf":[],"indices":[]}')
                continue
            f.write('{"tf":[')
            f.write(",".join(repr(c / total) for c in cnts))
            f.write('],"indices":[')
            f.write(",".join(str(perm[t]) for t in ids))
            f.write("]}")
        f.write("]}")

    os.replace(tmp_path, OUTPUT_PATH)
    t_end = time.time()

    gz_size = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    by_kind = Counter(doc["kind"] for doc in documents)
    print()
    for kind, _dir in SOURCE_DIRS:
        print(f"  {kind:9s}: {by_kind.get(kind, 0)}")
    print()
    print(f"Vector build+write: {t_end - t_vec:.1f}s")
    print(f"Index size: {gz_size:.2f} MB (gzip)")
    print(f"Total time: {t_end - t0:.1f}s")
    print(f"Index saved to {OUTPUT_PATH}")

    return {
        "built": built,
        "documents": len(documents),
        "vocab_size": vocab_size,
        "bytes": os.path.getsize(OUTPUT_PATH),
        "seconds": round(t_end - t0, 2),
        "read_seconds": round(t_read - t0, 2),
        "by_kind": dict(by_kind),
    }


def _reset_vocab():
    """Create the module-global Vocabulary that index_one() writes into."""
    global vocab
    vocab = Vocabulary()


vocab: Vocabulary
_reset_vocab()


if __name__ == "__main__":
    _reset_vocab()
    stats = build_index()
    print(json.dumps(stats, ensure_ascii=False, indent=2))
