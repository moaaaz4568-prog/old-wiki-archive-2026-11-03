#!/usr/bin/env python3
"""Regression tests for the V3 search index.

Covers the 2026-10-01 failure:
  1. every path stored in the index must be openable on THIS machine
     (the 2026-09-26 index stored paths rooted at /home/z/my-project/... )
  2. the index must actually contain 02_CONCEPTS/terms_26k/ and the
     23 sector directories (previously: 0 of ~29,600 files indexed)
  3. each real query must return a first hit whose file exists

Run:
  python3 test_index_health.py                      # tests V3 index (default)
  python3 test_index_health.py /path/to/index.json.gz
Exit code 0 = all pass, 1 = at least one failure.
"""

import collections
import gzip
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))

DEFAULT_INDEX = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.json.gz"
)

SECTOR_DIRS = [
    "01_outreach", "02_sales_calls", "03_offers_pricing", "04_content_strategy",
    "05_content_production", "06_hooks_retention", "07_branding", "08_mindset",
    "09_agencies_clients", "10_funnels", "11_marketing_ads", "12_growth",
    "13_storytelling", "14_copywriting", "15_platforms_algo", "16_business_models",
    "17_ai_automation", "18_trust_authority", "19_operations_teams",
    "20_productivity_learning", "21_persuasion_psych", "22_finance_legal",
    "99_uncategorized",
]

# The six real-world queries that must resolve to an openable file.
REAL_QUERIES = [
    "اوت ريتش",
    "cold email subject line",
    "حدود الفناء",
    "pattern interrupt",
    "تسعير العرض",
    "accountability",
]

INDEX_PATH = sys.argv.pop(1) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else DEFAULT_INDEX


def load(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


class TestIndexPaths(unittest.TestCase):
    """Test 1: paths must be resolvable from any working directory."""

    @classmethod
    def setUpClass(cls):
        cls.index = load(INDEX_PATH)

    def test_every_path_is_absolute(self):
        bad = [d["path"] for d in self.index["documents"] if not os.path.isabs(d["path"])]
        self.assertEqual([], bad[:5], f"{len(bad)} relative paths (unopenable from other cwd)")

    def test_every_path_is_openable(self):
        missing = [d["path"] for d in self.index["documents"] if not os.path.isfile(d["path"])]
        self.assertEqual([], missing[:5], f"{len(missing)} indexed paths do not exist on disk")

    def test_declared_root_exists(self):
        root = self.index.get("root")
        self.assertTrue(root and os.path.isdir(root), f"root not a directory: {root}")

    def test_documents_and_vectors_align(self):
        self.assertEqual(len(self.index["documents"]), len(self.index["doc_vectors"]))

    def test_no_orphan_stale_prefix(self):
        paths = [d["path"] for d in self.index["documents"]]
        stale = [p for p in paths if "/home/z/" in p]
        self.assertEqual([], stale[:5], "stale /home/z paths still present")


class TestCoverage(unittest.TestCase):
    """Test 2: the real concept corpus must be indexed."""

    @classmethod
    def setUpClass(cls):
        cls.index = load(INDEX_PATH)
        cls.docs = cls.index["documents"]

    def test_terms_26k_is_indexed(self):
        n = sum(1 for d in self.docs if "02_CONCEPTS/terms_26k/" in d["path"])
        self.assertGreater(n, 27000, f"terms_26k only partially indexed: {n}")

    def test_all_23_sectors_indexed(self):
        counts = collections.Counter(
            d["path"].split("/")[1] for d in self.docs
            if d["path"].startswith("/") and "02_CONCEPTS/" in d["path"]
            and d["path"].split("/")[2] != "terms_26k"
        )
        empty = [s for s in SECTOR_DIRS if counts.get(s, 0) == 0]
        self.assertEqual([], empty, f"unindexed sector dirs: {empty}")

    def test_terms_and_systems_indexed(self):
        kinds = collections.Counter(d["kind"] for d in self.docs)
        for kind in ("terms", "concepts", "masters", "systems"):
            self.assertGreater(kinds.get(kind, 0), 0, f"kind {kind} missing from index")

    def test_arabic_corpus_indexed(self):
        n = sum(1 for d in self.docs if any("\u0600" <= c <= "\u06ff" for c in d["title"]))
        self.assertGreater(n, 1000, "Arabic titles look under-indexed")


class TestRealQueries(unittest.TestCase):
    """Test 3: each real query returns an openable top hit."""

    @classmethod
    def setUpClass(cls):
        import search  # noqa: E402  (local tools copy)

        cls.search = search
        cls.index = load(INDEX_PATH)

    def _run(self, q):
        results = self.search.search(q, self.index)
        self.assertTrue(results, f"NO RESULTS for {q!r}")
        score, title, path = results[0]
        return score, title, path

    def test_queries_resolve_to_openable_file(self):
        for q in REAL_QUERIES:
            with self.subTest(query=q):
                score, title, path = self._run(q)
                self.assertGreater(score, 0.0)
                self.assertTrue(
                    os.path.isfile(path), f"{q!r} top hit missing on disk: {path}"
                )

    def test_queries_hit_the_new_corpus(self):
        for q in REAL_QUERIES:
            with self.subTest(query=q):
                _, _, path = self._run(q)
                self.assertTrue(
                    path.startswith("/"), f"{q!r} returned non-absolute path: {path}"
                )


if __name__ == "__main__":
    print(f"Testing index: {INDEX_PATH}", file=sys.stderr)
    result = unittest.main(verbosity=2, exit=False).result
    sys.exit(0 if result.wasSuccessful() else 1)