#!/usr/bin/env python3
"""Validate the Nexus LLM Wiki records without modifying raw sources."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from urllib.parse import unquote
from collections import Counter
from pathlib import Path
from typing import Any


FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK = re.compile(r"\]\(([^)]+)\)")
KNOWLEDGE_DIRS = ("sources", "claims", "concepts", "masters")
NON_RECORD_NAMES = {"README.md", "INDEX.md", "MASTER_ARCHITECTURE.md"}


def parse_value(value: str) -> Any:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def read_record(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT.match(text)
    if not match:
        raise ValueError("missing frontmatter")
    fields: dict[str, Any] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = parse_value(value)
    return fields, text


def records(vault: Path, directory: str) -> list[tuple[Path, dict[str, Any], str]]:
    root = vault / directory
    result = []
    if not root.exists():
        return result
    for path in sorted(root.rglob("*.md")):
        if path.name in NON_RECORD_NAMES:
            continue
        try:
            data, text = read_record(path)
            result.append((path, data, text))
        except Exception as exc:  # report malformed records instead of stopping the batch
            result.append((path, {"__error__": str(exc)}, ""))
    return result


def add_error(errors: list[dict[str, str]], path: Path, message: str) -> None:
    errors.append({"path": str(path), "error": message})


def validate(vault: Path) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    groups = {directory: records(vault, directory) for directory in KNOWLEDGE_DIRS}
    by_id: dict[str, tuple[str, Path, dict[str, Any]]] = {}
    for directory, items in groups.items():
        for path, data, _ in items:
            if "__error__" in data:
                add_error(errors, path, data["__error__"])
                continue
            required = {
                "sources": ("type", "source_id", "source_path", "content_hash", "status"),
                "claims": ("type", "claim_id", "statement", "evidence_type", "source_id", "locator", "scope", "confidence", "status"),
                "concepts": ("type", "concept_id", "title", "status", "claim_refs", "source_refs"),
                "masters": ("type", "master_id", "title", "status", "concept_refs", "claim_refs"),
            }[directory]
            for field in required:
                if field not in data or data[field] in ("", None):
                    add_error(errors, path, f"missing field: {field}")
            identifier = data.get(f"{directory[:-1]}_id")
            if identifier:
                if identifier in by_id:
                    add_error(errors, path, f"duplicate id: {identifier}")
                by_id[identifier] = (directory, path, data)
            expected_type = directory[:-1] if directory != "masters" else "master"
            if data.get("type") != expected_type:
                add_error(errors, path, f"type must be {expected_type}")

    sources = {data.get("source_id"): data for _, data, _ in groups["sources"] if "source_id" in data}
    for path, data, _ in groups["sources"]:
        if "__error__" in data:
            continue
        source_path = data.get("source_path")
        if not isinstance(source_path, str) or Path(source_path).is_absolute() or ".." in Path(source_path).parts:
            add_error(errors, path, "source_path must be relative and traversal-free")
            continue
        raw_path = vault / source_path
        if not raw_path.is_file():
            if data.get("status") == "quarantined" and data.get("quarantine_reason"):
                continue
            add_error(errors, path, f"source file missing: {source_path}")
            continue
        actual = hashlib.sha256(raw_path.read_bytes()).hexdigest()
        expected = str(data.get("content_hash", "")).removeprefix("sha256:")
        if actual != expected:
            add_error(errors, path, "content_hash does not match raw source")

    claims = {data.get("claim_id"): data for _, data, _ in groups["claims"] if "claim_id" in data}
    for path, data, _ in groups["claims"]:
        if "__error__" in data:
            continue
        source_id = data.get("source_id")
        if source_id not in sources:
            add_error(errors, path, f"unknown source_id: {source_id}")
            continue
        source_data = sources[source_id]
        raw_path = vault / source_data["source_path"]
        if not raw_path.is_file():
            continue
        raw = raw_path.read_text(encoding="utf-8")
        start, end = data.get("evidence_start"), data.get("evidence_end")
        quote = data.get("evidence_quote")
        if not isinstance(start, int) or not isinstance(end, int) or not isinstance(quote, str):
            add_error(errors, path, "evidence_start/evidence_end/evidence_quote required")
        elif start < 0 or end < start or raw[start:end] != quote:
            add_error(errors, path, "evidence slice does not match source")
        elif hashlib.sha256(quote.encode("utf-8")).hexdigest() != str(data.get("excerpt_sha256", "")):
            add_error(errors, path, "excerpt_sha256 does not match evidence_quote")
        evidence_type, confidence = data.get("evidence_type"), data.get("confidence")
        guards = {
            "example": "source_reported",
            "reported_result": "source_reported",
            "inference": "inferred",
            "hypothesis": "hypothetical",
        }
        if evidence_type in guards and confidence != guards[evidence_type]:
            add_error(errors, path, f"{evidence_type} requires confidence={guards[evidence_type]}")
        if data.get("status") == "accepted" and evidence_type in {"example", "reported_result"}:
            add_error(errors, path, "example/reported_result cannot be accepted without an explicit review policy")

    concepts = {data.get("concept_id"): data for _, data, _ in groups["concepts"] if "concept_id" in data}
    for path, data, _ in groups["concepts"]:
        if "__error__" in data:
            continue
        for ref in data.get("claim_refs", []) if isinstance(data.get("claim_refs"), list) else []:
            if ref not in claims:
                add_error(errors, path, f"unknown claim_ref: {ref}")
        for ref in data.get("source_refs", []) if isinstance(data.get("source_refs"), list) else []:
            if ref not in sources:
                add_error(errors, path, f"unknown source_ref: {ref}")
        if not data.get("claim_refs"):
            add_error(errors, path, "concept must have claim_refs")

    for path, _, text in sum(groups.values(), []):
        if not text:
            continue
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "#")):
                continue
            target_name = unquote(target.split("#", 1)[0])
            try:
                target_path = (path.parent / target_name).resolve()
                exists = target_path.is_file()
            except OSError as exc:
                add_error(errors, path, f"unreadable local link: {target} ({exc.__class__.__name__})")
                continue
            if not exists:
                add_error(errors, path, f"broken local link: {target}")

    counts = {
        directory: {"files": len(items), "statuses": dict(Counter(str(data.get("status")) for _, data, _ in items))}
        for directory, items in groups.items()
    }
    return {"ok": not errors, "vault": str(vault), "counts": counts, "errors": errors}


def build_index(vault: Path, result: dict[str, Any]) -> None:
    entries = []
    for directory in KNOWLEDGE_DIRS:
        for path, data, _ in records(vault, directory):
            if "__error__" not in data:
                entries.append({"kind": directory[:-1] if directory != "masters" else "master", "id": data.get(f"{directory[:-1]}_id"), "title": data.get("title") or data.get("statement"), "status": data.get("status"), "path": str(path.relative_to(vault))})
    entries.sort(key=lambda item: (item["kind"], item["id"] or ""))
    index_dir = vault / "indexes"
    index_dir.mkdir(parents=True, exist_ok=True)
    (index_dir / "catalog.json").write_text(json.dumps({"generated": True, "validation_ok": result["ok"], "counts": result["counts"], "entries": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Catalog", "", f"Validation: {'PASS' if result['ok'] else 'FAIL'}", "", "| kind | id | title | status | path |", "|---|---|---|---|---|"]
    lines.extend(f"| {e['kind']} | {e['id']} | {e['title']} | {e['status']} | `{e['path']}` |" for e in entries)
    (index_dir / "catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("/sdcard/NEXUS_LLM_WIKI"))
    parser.add_argument("--report", type=Path)
    parser.add_argument("--index", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.vault)
    if args.index:
        build_index(args.vault, result)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("# Wiki quality report\n\n```json\n" + rendered + "\n```\n", encoding="utf-8")
    print(rendered if args.json or not args.report else ("PASS" if result["ok"] else "FAIL"))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
