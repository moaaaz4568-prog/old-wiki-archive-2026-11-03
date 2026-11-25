#!/usr/bin/env python3
"""Search the TF-IDF index built by build_index.py.

Zero external dependencies — uses only Python stdlib.
Loads /sdcard/Nexus_Brain/rag/index.json.gz
"""

import gzip
import json
import math
import re
import sys
from collections import Counter

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
    'used', 'using', 'like', 'well',
    'في', 'من', 'إلى', 'على', 'عن', 'مع', 'كان', 'هذا', 'هذه', 'ذلك',
    'تلك', 'هو', 'هي', 'هم', 'هن', 'لقد', 'قد', 'لا', 'ما', 'لم', 'لن',
    'إن', 'أن', 'إذا', 'لكن', 'أو', 'ثم', 'بين', 'كل', 'بعض', 'أي',
    'كانت', 'يكون', 'حتى', 'حول', 'أثناء', 'بعد', 'قبل', 'فقط', 'غير',
    'حيث', 'هناك', 'متى', 'كيف', 'هنا', 'أين', 'بينما', 'التي', 'الذي',
    'الذين', 'اللذان', 'اللواتي', 'به', 'له', 'لها', 'منها', 'منه',
    'عليه', 'عليها', 'إليه', 'إليها', 'عند', 'دون', 'بسبب',
}

import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from nexus_config import INDEX_PATH, SOURCE_ROOT, resolve  # noqa: E402

ROOT = SOURCE_ROOT

TOKEN_PATTERN = re.compile(
    r"[^\w\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+"
)


def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = TOKEN_PATTERN.split(text)
    return [t for t in tokens if t and len(t) > 1]


def load_index(path: str) -> dict:
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return json.load(f)


def compute_query_vector(tokens: list[str], vocab: dict, idf: list[float]) -> tuple[dict[int, float], float]:
    if not tokens:
        return {}, 0.0
    tf_raw = Counter(tokens)
    total = len(tokens)
    vector: dict[int, float] = {}
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


def doc_tfidf(doc_vec: dict, idf: list[float], term_id: int) -> float:
    for tf_val, idx in zip(doc_vec['tf'], doc_vec['indices']):
        if idx == term_id:
            return tf_val * idf[idx]
    return 0.0


def doc_norm(doc_vec: dict, idf: list[float]) -> float:
    norm_sq = 0.0
    for tf_val, idx in zip(doc_vec['tf'], doc_vec['indices']):
        tfidf = tf_val * idf[idx]
        norm_sq += tfidf * tfidf
    return math.sqrt(norm_sq)


def cosine_similarity(query_vec: dict[int, float], query_norm: float, doc_vec: dict, idf: list[float], dnorm: float) -> float:
    if query_norm == 0.0 or dnorm == 0.0:
        return 0.0
    dot = 0.0
    for tf_val, idx in zip(doc_vec['tf'], doc_vec['indices']):
        if idx in query_vec:
            dot += query_vec[idx] * (tf_val * idf[idx])
    return dot / (query_norm * dnorm)


def get_preview(filepath: str, max_chars: int = 200, root: str | None = None) -> str:
    """First body line of a document, for display.

    `filepath` is normally absolute (new indexes store absolute paths). If it is
    relative it is re-anchored onto `root` instead of the caller's cwd, which is
    what silently produced empty previews when the index was built elsewhere.
    """
    filepath = resolve(filepath, root)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            in_frontmatter = False
            for line in f:
                stripped = line.strip()
                if stripped == '---':
                    in_frontmatter = not in_frontmatter
                    continue
                if in_frontmatter:
                    continue
                if not stripped:
                    continue
                if stripped.startswith(('#', '[[')):
                    continue
                if len(stripped) > max_chars:
                    return stripped[:max_chars] + '...'
                return stripped
    except Exception:
        pass
    return ''


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
        if score > 0:
            results.append((score, doc['title'], doc['path']))

    results.sort(key=lambda x: -x[0])
    return results[:10]


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 search.py "query here" [-k N]')
        sys.exit(1)

    query = sys.argv[1]

    try:
        index = load_index(INDEX_PATH)
    except FileNotFoundError:
        print(f'Error: Index not found at {INDEX_PATH}')
        print('Run build_index.py first.')
        sys.exit(1)

    results = search(query, index)
    root = index.get('root') or ROOT

    print(f'=== Results for "{query}" ===')
    print()

    if not results:
        print('No results found.')
        return

    for rank, (score, title, path) in enumerate(results, 1):
        preview = get_preview(path, root=root)
        print(f'#{rank} ({score:.3f}) {title}')
        print(f'   {path}')
        if preview:
            print(f'   > {preview}')
        print()


if __name__ == '__main__':
    main()
