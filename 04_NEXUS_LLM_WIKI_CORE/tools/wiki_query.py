#!/usr/bin/env python3
"""Small offline lexical retriever for reviewed Claims and Concepts."""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from wiki_quality import read_record, records


TOKEN = re.compile(r"[\w\u0600-\u06ff]+", re.UNICODE)
ARABIC_MAP = str.maketrans({"إ": "ا", "أ": "ا", "آ": "ا", "ى": "ي", "ؤ": "و", "ئ": "ي"})
STOPWORDS = {"في", "من", "عن", "على", "علي", "الى", "الي", "و", "او", "اي", "هو", "هي", "هذا", "هذه", "ذلك", "تلك", "الذي", "التي", "ما", "لا", "لم", "لن", "ثم", "ان", "انها", "كل", "مع", "ل", "ب", "ف"}


def normalize(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).casefold().translate(ARABIC_MAP)
    return [token for token in TOKEN.findall(text) if len(token) > 1 and token not in STOPWORDS]


def score(query: list[str], data: dict[str, Any], body: str) -> float:
    fields = {
        "title": " ".join(str(data.get(k, "")) for k in ("title", "concept_id")),
        "statement": str(data.get("statement", "")),
        "scope": str(data.get("scope", "")),
        "body": body,
    }
    weights = {"title": 4.0, "statement": 3.0, "scope": 1.5, "body": 0.5}
    return sum(weights[name] * len(set(query) & set(normalize(value))) for name, value in fields.items())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--vault", type=Path, default=Path("/sdcard/NEXUS_LLM_WIKI"))
    parser.add_argument("--include-drafts", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    query_tokens = normalize(args.query)
    candidates = []
    for directory in ("claims", "concepts"):
        for path, data, body in records(args.vault, directory):
            if "__error__" in data or data.get("status") in {"candidate", "rejected"}:
                continue
            if directory == "concepts" and data.get("status") == "draft" and not args.include_drafts:
                continue
            value = score(query_tokens, data, body)
            if value >= 2.0:
                identifier = data.get("claim_id") or data.get("concept_id")
                candidates.append({"score": value, "kind": directory[:-1], "id": identifier, "title": data.get("title") or data.get("statement"), "path": str(path.relative_to(args.vault)), "source_id": data.get("source_id"), "claim_refs": data.get("claim_refs", []), "locator": data.get("locator")})
    candidates.sort(key=lambda item: (-item["score"], item["id"] or ""))
    result = {"query": args.query, "tokens": query_tokens, "insufficient_evidence": not candidates, "results": candidates[: max(1, args.limit)]}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not candidates:
        print("insufficient evidence")
    else:
        for item in result["results"]:
            print(f"{item['score']:.1f}\t{item['kind']}\t{item['id']}\t{item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
