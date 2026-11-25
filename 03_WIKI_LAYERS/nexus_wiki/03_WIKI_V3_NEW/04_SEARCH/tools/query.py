#!/usr/bin/env python3
"""Full RAG pipeline: search → read → chain → output context.

Usage:
  python3 query.py "how to write outreach email"
  python3 query.py "ازاي اكتب اسكربت outreach" --max-files 10
  python3 query.py "agency systems" --chain 3

Output: structured context block with ALL relevant file contents.
Paste this to Claude for a deep, critical answer.
"""

import gzip
import json
import math
import re
import sys
import glob
import os
from collections import Counter

# ─── Config ───────────────────────────────────────────────────────────
# The index lives with the V3 tool deployment; the documents it points at live in
# the read-only NB2 corpus. These are no longer the same directory, which is the
# bug the 2026-09-26 index suffered from (repo=/home/z/my-project/nexus-brain-v2).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nexus_config import (  # noqa: E402
    CONCEPTS_DIR,
    INDEX_PATH,
    MASTER_GRAPH_PATH,
    MASTERS_DIR,
    SOURCE_ROOT,
    resolve,
)

CORPUS_ROOT = SOURCE_ROOT
TOP_K = 7           # initial results
CHAIN_DEPTH = 2     # how deep to follow wikilinks
MIN_SCORE = 0.001

STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'by', 'with', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'can', 'could', 'may', 'might', 'shall', 'should', 'not', 'no', 'nor',
    'so', 'as', 'if', 'than', 'that', 'this', 'these', 'those', 'it', 'its',
    'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'him', 'his', 'she',
    'her', 'they', 'them', 'their', 'what', 'which', 'who', 'whom', 'when',
    'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
    'most', 'some', 'any', 'such', 'only', 'own', 'same', 'here', 'there',
    'up', 'down', 'about', 'into', 'over', 'again', 'further', 'once',
    'then', 'just', 'also', 'very', 'too', 'really', 'get', 'got', 'use',
    'used', 'using', 'like', 'well', 'make', 'made', 'need', 'know',
    'في', 'من', 'إلى', 'على', 'عن', 'مع', 'كان', 'هذا', 'هذه', 'ذلك',
    'تلك', 'هو', 'هي', 'هم', 'هن', 'لقد', 'قد', 'لا', 'ما', 'لم', 'لن',
    'إن', 'أن', 'إذا', 'لكن', 'أو', 'ثم', 'بين', 'كل', 'بعض', 'أي',
    'كانت', 'يكون', 'حتى', 'حول', 'أثناء', 'بعد', 'قبل', 'فقط', 'غير',
    'حيث', 'هناك', 'متى', 'كيف', 'هنا', 'أين', 'بينما', 'التي', 'الذي',
    'الذين', 'اللذان', 'اللواتي', 'به', 'له', 'لها', 'منها', 'منه',
    'عليه', 'عليها', 'إليه', 'إليها', 'عند', 'دون', 'بسبب',
}

TOKEN_PATTERN = re.compile(r"[^\w\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+")
WIKILINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')


# ─── Tokenizer ────────────────────────────────────────────────────────
def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = TOKEN_PATTERN.split(text)
    return [t for t in tokens if t and len(t) > 1]


# ─── Index Loading ────────────────────────────────────────────────────
def load_index(path: str) -> dict:
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return json.load(f)


# ─── Search Engine ────────────────────────────────────────────────────
def compute_query_vector(tokens: list[str], vocab: dict, idf: list[float]):
    if not tokens:
        return {}, 0.0
    tf_raw = Counter(tokens)
    total = len(tokens)
    vector = {}
    norm_sq = 0.0
    for term, count in tf_raw.items():
        term_id = vocab.get(term)
        if term_id is None:
            continue
        tf_val = count / total
        tfidf = tf_val * idf[term_id]
        vector[term_id] = tfidf
        norm_sq += tfidf * tfidf
    return vector, math.sqrt(norm_sq)


def doc_norm(doc_vec: dict, idf: list[float]) -> float:
    norm_sq = 0.0
    for tf_val, idx in zip(doc_vec['tf'], doc_vec['indices']):
        tfidf = tf_val * idf[idx]
        norm_sq += tfidf * tfidf
    return math.sqrt(norm_sq)


def cosine_similarity(query_vec, query_norm, doc_vec, idf, dnorm) -> float:
    if query_norm == 0.0 or dnorm == 0.0:
        return 0.0
    dot = 0.0
    for tf_val, idx in zip(doc_vec['tf'], doc_vec['indices']):
        if idx in query_vec:
            dot += query_vec[idx] * (tf_val * idf[idx])
    return dot / (query_norm * dnorm)


def search(query: str, index: dict) -> list[tuple[float, str, str]]:
    vocab = index['vocab']
    idf = index['idf']
    documents = index['documents']
    doc_vectors = index['doc_vectors']

    tokens = tokenize(query)
    if not tokens:
        return []

    unknown_terms = [t for t in tokens if t not in vocab]
    non_stop_unknown = [t for t in unknown_terms if t not in STOP_WORDS]
    if non_stop_unknown:
        filtered = [t for t in tokens if t not in STOP_WORDS]
        if filtered and len(filtered) < len(tokens):
            return search(' '.join(filtered), index)

    query_vec, query_norm = compute_query_vector(tokens, vocab, idf)

    results = []
    for i, doc in enumerate(documents):
        dv = doc_vectors[i]
        dnorm = doc_norm(dv, idf)
        score = cosine_similarity(query_vec, query_norm, dv, idf, dnorm)
        if score > MIN_SCORE:
            results.append((score, doc['title'], doc['path']))

    results.sort(key=lambda x: -x[0])
    return results


# ─── Wikilink Extraction ──────────────────────────────────────────────
def extract_wikilinks(text: str) -> list[str]:
    """Extract all [[Concept_Name]] references from text."""
    matches = WIKILINK_PATTERN.findall(text)
    links = []
    for m in matches:
        clean = m.split('|')[0].strip()
        if clean.startswith('Concept_'):
            links.append(clean)
    return links


def find_concept_file(concept_name: str) -> str | None:
    """Find the file path for a concept name (with or without .md)."""
    if not concept_name.endswith('.md'):
        concept_name += '.md'
    path = os.path.join(CONCEPTS_DIR, concept_name)
    if os.path.exists(path):
        return path
    return None


# ─── File Reading ─────────────────────────────────────────────────────
def read_file(filepath: str) -> str | None:
    filepath = resolve(filepath, CORPUS_ROOT)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception:
        return None


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from content."""
    if content.startswith('---'):
        idx = content.find('---', 3)
        if idx != -1:
            return content[idx + 3:].strip()
    return content


# ─── Master Retrieval ─────────────────────────────────────────────────
def find_master_file(master_name: str) -> str | None:
    """Resolve only an active canonical master from MASTER_GRAPH.json."""
    requested = os.path.splitext(os.path.basename(master_name))[0]
    try:
        with open(MASTER_GRAPH_PATH, encoding='utf-8') as f:
            nodes = json.load(f).get('nodes', [])
    except (OSError, json.JSONDecodeError):
        nodes = []
    aliases = {requested, requested if requested.startswith('Master_') else f'Master_{requested}'}
    for node in nodes:
        if node.get('id') in aliases:
            path = os.path.join(MASTERS_DIR, node['path'])
            return path if os.path.isfile(path) else None
    return None


def extract_section(content: str, section_num: int) -> str | None:
    """استخرج قسم §N من محتوى الماستر."""
    # pattern مرن: §4 أو § 4 أو 4.
    patterns = [
        rf'##\s*§\s*{section_num}[\.\s:].*?(?=##\s*§\s*{section_num+1}[\.\s:])',
        rf'##\s*§\s*{section_num}[\.\s:].*?(?=##\s*§?\s*{section_num+1}[\.\s:])',
        rf'##\s*{section_num}[\.\s:].*?(?=##\s*{section_num+1}[\.\s:])',
    ]
    for p in patterns:
        m = re.search(p, content, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return None


def retrieve_master(master_name: str, section: int | None = None):
    """استرجع ماستر كامل أو قسم محدد منه."""
    fpath = find_master_file(master_name)
    if not fpath:
        print(f"❌ Master not found: {master_name}")
        return
    content = read_file(fpath)
    if not content:
        print(f"❌ Could not read: {fpath}")
        return
    title = os.path.basename(fpath)
    plain = strip_frontmatter(content)
    if section:
        sec_content = extract_section(plain, section)
        if sec_content:
            print(f"{'═'*60}")
            print(f"📄 MASTER: {title} | §{section}")
            print(f"📂 {fpath}")
            print(f"{'═'*60}")
            print(sec_content)
            print(f"\n✅ Section §{section}: {len(sec_content.split())} words")
        else:
            print(f"❌ Section §{section} not found in {title}")
            print(f"   Available sections: {re.findall(r'##\s*§?\s*(\d+)', plain)[:20]}")
    else:
        if len(plain) > 15000:
            plain = plain[:15000] + "\n\n[... file truncated at 15000 chars ...]"
        print(f"{'═'*60}")
        print(f"📄 MASTER: {title}")
        print(f"📂 {fpath}")
        print(f"{'═'*60}")
        print(plain)
        print(f"\n✅ Full master: {len(plain.split())} words")


def canonical_master_names() -> set[str]:
    """حمّل أسماء الماسترز المعتمدة من الـ graph (مصدر الحقيقة التشغيلي)."""
    try:
        with open(MASTER_GRAPH_PATH, encoding='utf-8') as f:
            graph = json.load(f)
        return {node['id'] for node in graph.get('nodes', [])}
    except (OSError, json.JSONDecodeError, KeyError):
        return set()


def list_masters(include_all: bool = False):
    """List canonical masters; --all means all active masters, never archive files."""
    patterns = [
        os.path.join(MASTERS_DIR, '**', 'Master_*.md'),
        os.path.join(MASTERS_DIR, '**', 'Specialized_Master_*.md'),
    ]
    masters = sorted({m for pattern in patterns for m in glob.glob(pattern, recursive=True)
                      if '_archive' not in os.path.relpath(m, MASTERS_DIR).split(os.sep)})
    canonical = canonical_master_names()
    if canonical and not include_all:
        masters = [m for m in masters if os.path.splitext(os.path.basename(m))[0] in canonical]
    label = 'all active master files (archive excluded)' if include_all else 'canonical masters'
    print(f"📋 Available {label}: {len(masters)}")
    print(f"{'─'*60}")
    for m in masters:
        rel = os.path.relpath(m, MASTERS_DIR)
        name = os.path.basename(m).replace('.md', '')
        print(f"  {name}  ({rel})")


# ─── Main Query Pipeline ──────────────────────────────────────────────
def query_pipeline(question: str, top_k: int = TOP_K, chain_depth: int = CHAIN_DEPTH, save_path: str | None = None):
    print(f"🔍 Query: {question}")
    print(f"{'='*60}")
    print()

    # Load index
    try:
        index = load_index(INDEX_PATH)
    except FileNotFoundError:
        print(f"ERROR: Index not found at {INDEX_PATH}")
        print("Run build_index.py first.")
        sys.exit(1)

    # Round 1: Search
    results = search(question, index)
    if not results:
        print("No results found for this query.")
        return

    print(f"📊 Found {len(results)} relevant concepts")
    print(f"{'-'*60}")
    for i, (score, title, path) in enumerate(results[:top_k], 1):
        print(f"  #{i} ({score:.3f}) {title}")
    print()

    # Collect files to read: top K from search
    files_to_read = set()
    selected = results[:top_k]
    for _, title, path in selected:
        files_to_read.add(path)

    # Read initial files and extract wikilinks
    round = 1
    found_links = set()

    while round <= chain_depth:
        new_files = set()
        for fpath in list(files_to_read):
            content = read_file(fpath)
            if content is None:
                continue
            plain = strip_frontmatter(content)
            links = extract_wikilinks(plain)
            for link_name in links:
                if link_name not in found_links:
                    found_links.add(link_name)
                    linked_path = find_concept_file(link_name)
                    if linked_path and linked_path not in files_to_read:
                        new_files.add(linked_path)

        if not new_files:
            break

        print(f"🔗 Chain round {round}: found {len(new_files)} linked concepts")
        files_to_read.update(new_files)
        round += 1

    # ── Read and output all files ──
    print(f"{'='*60}")
    print(f"📚 Context: {len(files_to_read)} total files")
    print(f"{'='*60}")
    print()

    # Sort: primary results first, then linked
    primary_paths = [p for _, _, p in selected]
    linked_paths = sorted(f for f in files_to_read if f not in primary_paths)
    ordered_paths = primary_paths + linked_paths

    for idx, fpath in enumerate(ordered_paths, 1):
        content = read_file(fpath)
        if content is None:
            continue
        title = os.path.basename(fpath)
        plain = strip_frontmatter(content)

        # Truncate very long files (>15000 chars)
        if len(plain) > 15000:
            plain = plain[:15000] + "\n\n[... file truncated at 15000 chars ...]"

        print(f"{'─'*60}")
        print(f"📄 FILE {idx}: {title}")
        print(f"{'─'*60}")
        print(plain)
        print()

    total_chars = sum(len(read_file(f) or '') for f in ordered_paths)

    if save_path:
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(f"Query: {question}\n")
            f.write(f"{'='*60}\n\n")
            for idx, fpath in enumerate(ordered_paths, 1):
                content = read_file(fpath)
                if content is None:
                    continue
                title = os.path.basename(fpath)
                plain = strip_frontmatter(content)
                if len(plain) > 15000:
                    plain = plain[:15000] + "\n\n[...truncated...]"
                f.write(f"{'─'*60}\nFILE {idx}: {title}\n")
                f.write(f"{'─'*60}\n")
                f.write(plain)
                f.write("\n\n")
            f.write(f"{'='*60}\n")
        print(f"💾 Saved to {save_path} ({total_chars:,} chars)")

    print(f"{'='*60}")
    print(f"✅ Done. {len(ordered_paths)} files, {total_chars:,} total chars")
    print(f"{'='*60}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 query.py \"your question\" [--max-files N] [--chain N] [--save path.txt]")
        print("  python3 query.py --master Master_Name [--section N]")
        print("  python3 query.py --list-masters")
        print("  python3 query.py --all-masters")
        sys.exit(1)

    # وضع الماستر
    if sys.argv[1] in ('--list-masters', '--all-masters'):
        list_masters(include_all=sys.argv[1] == '--all-masters')
        sys.exit(0)

    if sys.argv[1] == '--master' and len(sys.argv) >= 3:
        master_name = sys.argv[2]
        section = None
        for i, arg in enumerate(sys.argv[3:], 3):
            if arg == '--section' and i + 1 < len(sys.argv):
                section = int(sys.argv[i + 1])
        retrieve_master(master_name, section)
        sys.exit(0)

    # وضع البحث العادي
    question = sys.argv[1]
    top_k = TOP_K
    chain_depth = CHAIN_DEPTH
    save_path = None

    # Parse optional args
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == '--max-files' and i + 1 < len(args):
            top_k = int(args[i + 1])
        elif arg == '--chain' and i + 1 < len(args):
            chain_depth = int(args[i + 1])
        elif arg == '--save' and i + 1 < len(args):
            save_path = args[i + 1]

    query_pipeline(question, top_k, chain_depth, save_path)
