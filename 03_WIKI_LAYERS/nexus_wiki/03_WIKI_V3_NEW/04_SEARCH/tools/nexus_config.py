#!/usr/bin/env python3
"""Single source of truth for V3 search-engine paths.

The 2026-09-26 index was built by a tool whose only notion of "where am I" was
`dirname(dirname(dirname(abspath(__file__))))`. That made the corpus root, the
tool location and the index location the same variable, so the index could only
ever be correct on the machine that built it (it stored
`repo=/home/z/my-project/nexus-brain-v2`).

Here the three locations are separated explicitly:

  SOURCE_ROOT  the read-only corpus        -> /root/r/NB2
  V3_ROOT      this tool deployment        -> /root/r/V3
  INDEX_PATH   the generated index         -> /root/r/V3/04_SEARCH/index.json.gz

All three can be overridden by environment variable so the engine can be pointed
at a different corpus without editing code.
"""

import os

# Read-only Nexus Brain corpus (the thing we index).
SOURCE_ROOT = os.path.abspath(
    os.environ.get("NEXUS_SOURCE_ROOT") or "/root/r/NB2"
)

# Where this V3 tool deployment lives (derived from this file, overridable).
V3_ROOT = os.path.abspath(
    os.environ.get("NEXUS_V3_ROOT")
    or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# The generated index.
OUTPUT_PATH_FALLBACK = os.path.join(V3_ROOT, "04_SEARCH", "index.json.gz")
INDEX_PATH = os.path.abspath(os.environ.get("NEXUS_INDEX_PATH") or OUTPUT_PATH_FALLBACK)

# Thread count for the build's read phase. The corpus is I/O-heavy (~230 MB of
# markdown), so this is capped well above the 8-worker default suggested for it.
WORKERS = int(os.environ.get("NEXUS_BUILD_WORKERS") or 8)

# Corpus subtrees, in the order the original tool used.
SOURCE_DIRS = [
    ("terms", os.path.join(SOURCE_ROOT, "01_TERMS")),
    ("concepts", os.path.join(SOURCE_ROOT, "02_CONCEPTS")),
    ("masters", os.path.join(SOURCE_ROOT, "03_MASTERS")),
    ("systems", os.path.join(SOURCE_ROOT, "00_SYSTEMS")),
]

CONCEPTS_DIR = os.path.join(SOURCE_ROOT, "02_CONCEPTS")
MASTERS_DIR = os.path.join(SOURCE_ROOT, "03_MASTERS")
MASTER_GRAPH_PATH = os.path.join(MASTERS_DIR, "MASTER_GRAPH.json")
RAG_DIR = os.path.join(V3_ROOT, "04_SEARCH", "tools")

# Documents smaller than this are not indexed (parity with the original tool).
MIN_SIZE = 50
FILE_GLOBS = ["*.md", "**/*.md"]


def resolve(path: str, root: str | None = None) -> str:
    """Turn a stored index path into an absolute, openable path.

    New indexes store absolute paths. Older/stale ones store paths relative to
    the corpus root that built them, so a relative path is re-anchored onto
    `root` (default: SOURCE_ROOT) instead of being resolved against the caller's
    cwd -- which is what silently produced empty previews before.
    """
    if os.path.isabs(path):
        return path
    base = root or SOURCE_ROOT
    return os.path.normpath(os.path.join(base, path))
