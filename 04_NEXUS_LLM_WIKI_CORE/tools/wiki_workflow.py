#!/usr/bin/env python3
"""Safe, read-first workflow checks for Nexus LLM Wiki source batches.

The command is intentionally limited to routing artifacts.  It never edits
``raw/`` or a source record, and ``publish`` is a dry-run unless ``--apply``
is supplied explicitly.  Knowledge extraction remains subject to the single
active-domain lock and a partial batch can never claim T or start a Master.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_VAULT = Path("/sdcard/NEXUS_LLM_WIKI")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SAFE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
KNOWLEDGE_OPERATION_NAMES = {"extract", "extraction", "knowledge", "author"}
GATE_T_NAMES = {"t", "terms", "domain_terms_complete"}
GATE_MASTER_NAMES = {"m", "master", "masters", "master_authoring"}


class WorkflowError(Exception):
    """A controlled validation or safe-write failure."""


def _error(code: str, message: str, **context: Any) -> dict[str, Any]:
    item: dict[str, Any] = {"code": code, "message": message}
    item.update({key: value for key, value in context.items() if value is not None})
    return item


def _warning(code: str, message: str, **context: Any) -> dict[str, Any]:
    item: dict[str, Any] = {"code": code, "message": message}
    item.update({key: value for key, value in context.items() if value is not None})
    return item


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _display_hash(value: str) -> str:
    return f"sha256:{value}"


def _hash_hex(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise WorkflowError(f"{field} must be a sha256:<64-hex> string")
    candidate = value.removeprefix("sha256:").lower()
    if not HASH_PATTERN.fullmatch(candidate):
        raise WorkflowError(f"{field} must be a sha256:<64-hex> string")
    return candidate


def _path_inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return False
    return True


def _safe_relative(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise WorkflowError(f"{label} must be a non-empty relative path")
    if "\x00" in value or "\\" in value:
        raise WorkflowError(f"{label} contains an unsafe path separator")
    # ``Path.parts`` normalizes ``.`` and repeated separators before this
    # function sees them.  Validate the lexical spelling first so a manifest
    # cannot smuggle traversal-ish paths through that normalization.
    lexical_parts = value.split("/")
    if any(part in {"", ".", ".."} for part in lexical_parts):
        raise WorkflowError(f"{label} must be relative and traversal-free")
    path = Path(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise WorkflowError(f"{label} must be relative and traversal-free")
    return value


def _safe_id(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID_PATTERN.fullmatch(value):
        raise WorkflowError(
            f"{label} must contain only ASCII letters, digits, '.', '_' or '-'; "
            "it must not be a traversal path"
        )
    if value in {".", ".."}:
        raise WorkflowError(f"{label} is not a safe identifier")
    return value


def _relative_vault_path(vault: Path, value: str | Path, *, label: str) -> Path:
    path = Path(value)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise WorkflowError(f"{label} must be traversal-free")
    # Keep the lexical path so lstat can still see a symlink at the user
    # supplied component.  ``resolve()`` is used only for the containment
    # check; returning the resolved target would accidentally hide the link.
    lexical = path if path.is_absolute() else vault / path
    if not _path_inside(vault, lexical):
        raise WorkflowError(f"{label} must remain inside the wiki root")
    return lexical


def _lstat(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _is_symlink(path: Path) -> bool:
    info = _lstat(path)
    return info is not None and stat.S_ISLNK(info.st_mode)


def _assert_no_symlink_components(root: Path, path: Path) -> None:
    """Reject a symlink in every existing component below ``root``."""
    root_resolved = root.resolve(strict=False)
    path_lexical = path if path.is_absolute() else root / path
    try:
        relative = path_lexical.relative_to(root_resolved)
    except ValueError as exc:
        raise WorkflowError("path escapes the wiki root") from exc
    current = root_resolved
    for part in relative.parts:
        current = current / part
        try:
            info = _lstat(current)
        except OSError as exc:
            raise WorkflowError(f"cannot inspect path component: {current}: {exc}") from exc
        if info is not None and stat.S_ISLNK(info.st_mode):
            raise WorkflowError(f"symlink path component is not allowed: {current}")


def _assert_regular_source(vault: Path, relative_path: str) -> Path:
    source = _relative_vault_path(vault, relative_path, label="source path")
    _assert_no_symlink_components(vault, source)
    info = _lstat(source)
    if info is None:
        raise WorkflowError(f"source path does not exist: {relative_path}")
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise WorkflowError(f"source path must be a regular non-symlink file: {relative_path}")
    return source


def _read_stable(source: Path) -> tuple[bytes, os.stat_result, os.stat_result]:
    before = source.stat(follow_symlinks=False)
    data = source.read_bytes()
    after = source.stat(follow_symlinks=False)
    stable_fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns")
    if any(getattr(before, field) != getattr(after, field) for field in stable_fields):
        raise WorkflowError("source_changed_during_read")
    return data, before, after


def _load_json(path: Path, *, label: str) -> tuple[Any, bytes]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise WorkflowError(f"cannot read {label}: {exc}") from exc
    try:
        return json.loads(data.decode("utf-8")), data
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"{label} is not valid UTF-8 JSON: {exc}") from exc


def _config_path(vault: Path, name: str) -> Path:
    path = vault / "config" / name
    _assert_no_symlink_components(vault, path)
    return path


def _load_configs(vault: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    try:
        catalog, _ = _load_json(_config_path(vault, "domain_catalog.json"), label="domain_catalog.json")
        processing, _ = _load_json(
            _config_path(vault, "processing_order.json"), label="processing_order.json"
        )
    except WorkflowError as exc:
        return {}, {}, [_error("CONFIG_READ_ERROR", str(exc))]
    if not isinstance(catalog, dict):
        errors.append(_error("CONFIG_SHAPE_ERROR", "domain_catalog.json must contain an object"))
        catalog = {}
    if not isinstance(processing, dict):
        errors.append(_error("CONFIG_SHAPE_ERROR", "processing_order.json must contain an object"))
        processing = {}
    return catalog, processing, errors


def _catalog_domains(catalog: dict[str, Any]) -> dict[str, dict[str, str]]:
    domains: dict[str, dict[str, str]] = {}
    raw_domains = catalog.get("domains", [])
    if not isinstance(raw_domains, list):
        return domains
    for raw_domain in raw_domains:
        if not isinstance(raw_domain, dict):
            continue
        domain_id = raw_domain.get("domain_id", raw_domain.get("id"))
        if not isinstance(domain_id, str):
            continue
        subdomains: dict[str, str] = {}
        raw_subdomains = raw_domain.get("subdomains", [])
        if isinstance(raw_subdomains, list):
            for raw_subdomain in raw_subdomains:
                if not isinstance(raw_subdomain, dict):
                    continue
                subdomain_id = raw_subdomain.get("subdomain_id", raw_subdomain.get("id"))
                if isinstance(subdomain_id, str):
                    subdomains[subdomain_id] = str(raw_subdomain.get("title", subdomain_id))
        domains[domain_id] = subdomains
    return domains


def _processing_status(processing: dict[str, Any], domain: str) -> str | None:
    states = processing.get("domain_states", [])
    if isinstance(states, list):
        for state in states:
            if isinstance(state, dict) and state.get("domain_id") == domain:
                value = state.get("status")
                if isinstance(value, str):
                    return value
    if processing.get("current_domain") == domain:
        value = processing.get("current_domain_status")
        return value if isinstance(value, str) else None
    return None


def _current_domain(processing: dict[str, Any]) -> tuple[str | None, str | None]:
    current = processing.get("current_domain")
    status = processing.get("current_domain_status")
    if isinstance(current, str):
        return current, status if isinstance(status, str) else _processing_status(processing, current)
    return None, None


def _catalog_revision(catalog: dict[str, Any]) -> Any:
    return _first_present(catalog, ("catalog_revision", "catalog_id", "workflow_contract_version"))


def inventory(vault: Path) -> dict[str, Any]:
    """Return a read-only inventory of ``new/`` and ``raw/new/``."""
    vault = vault.resolve(strict=False)
    items: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    seen: set[str] = set()
    for root_name in ("new", "raw/new"):
        root = vault / root_name
        root_info = _lstat(root)
        if root_info is None:
            continue
        if stat.S_ISLNK(root_info.st_mode):
            errors.append(_error("SYMLINK_ROOT", "inventory root is a symlink", path=root_name))
            continue
        if not stat.S_ISDIR(root_info.st_mode):
            errors.append(_error("INVENTORY_ROOT_INVALID", "inventory root is not a directory", path=root_name))
            continue
        stack = [root]
        while stack:
            current = stack.pop()
            try:
                children = sorted(os.scandir(current), key=lambda entry: entry.name, reverse=True)
            except OSError as exc:
                errors.append(_error("INVENTORY_READ_ERROR", str(exc), path=str(current)))
                continue
            for child in children:
                child_path = Path(child.path)
                try:
                    relative = child_path.relative_to(vault).as_posix()
                except ValueError:
                    errors.append(_error("PATH_ESCAPE", "inventory item escaped the wiki root"))
                    continue
                if relative in seen:
                    continue
                seen.add(relative)
                try:
                    info = child_path.lstat()
                except OSError as exc:
                    errors.append(_error("INVENTORY_STAT_ERROR", str(exc), path=relative))
                    continue
                if stat.S_ISLNK(info.st_mode):
                    errors.append(_error("UNSAFE_SYMLINK", "symlinks are not inventory sources", path=relative))
                elif stat.S_ISDIR(info.st_mode):
                    stack.append(child_path)
                elif stat.S_ISREG(info.st_mode):
                    try:
                        data, before, after = _read_stable(child_path)
                        items.append(
                            {
                                "path": relative,
                                "size_bytes": len(data),
                                "sha256": _display_hash(_sha256_bytes(data)),
                                "stable": before.st_ino == after.st_ino and before.st_mtime_ns == after.st_mtime_ns,
                            }
                        )
                    except (OSError, WorkflowError) as exc:
                        errors.append(_error("INVENTORY_READ_ERROR", str(exc), path=relative))
    items.sort(key=lambda item: item["path"])
    return {
        "ok": not errors,
        "vault": str(vault),
        "read_only": True,
        "writes_performed": 0,
        "roots": ["new/", "raw/new/"],
        "items": items,
        "errors": errors,
    }


def status(vault: Path) -> dict[str, Any]:
    """Read and summarize the two authoritative config files without writing."""
    vault = vault.resolve(strict=False)
    catalog, processing, errors = _load_configs(vault)
    domains = _catalog_domains(catalog)
    order = processing.get("order", [])
    if not isinstance(order, list):
        errors.append(_error("CONFIG_SHAPE_ERROR", "processing_order.order must be a list"))
        order = []
    current_domain, current_status = _current_domain(processing)
    if current_domain is not None and current_domain not in domains:
        errors.append(_error("CURRENT_DOMAIN_UNKNOWN", "current_domain is not in the catalog", domain=current_domain))
    if len(set(order)) != len(order):
        errors.append(_error("ORDER_DUPLICATE", "processing order contains duplicate domains"))
    if any(domain not in domains for domain in order):
        errors.append(_error("ORDER_DOMAIN_UNKNOWN", "processing order contains an unknown domain"))
    domain_states: list[dict[str, Any]] = []
    for domain in order:
        if not isinstance(domain, str):
            continue
        domain_states.append(
            {
                "domain": domain,
                "status": _processing_status(processing, domain),
                "subdomains": sorted(domains.get(domain, {})),
                "knowledge_locked": domain != current_domain,
                "routing_allowed": True,
            }
        )
    return {
        "ok": not errors,
        "vault": str(vault),
        "read_only": True,
        "writes_performed": 0,
        "catalog_revision": _catalog_revision(catalog),
        "order": order,
        "current_domain": current_domain,
        "current_domain_status": current_status,
        "domain_states": domain_states,
        "errors": errors,
    }


def _manifest_entries(manifest: dict[str, Any]) -> list[Any]:
    for key in ("entries", "candidate_manifest", "candidates"):
        if key in manifest:
            value = manifest[key]
            return value if isinstance(value, list) else []
    return []


def _first_present(mapping: dict[str, Any], keys: Iterable[str]) -> Any:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return None


def _range_pair(raw: Any) -> tuple[int, int] | None:
    if isinstance(raw, (list, tuple)) and len(raw) == 2:
        start, end = raw
    elif isinstance(raw, dict):
        start, end = raw.get("start"), raw.get("end")
    else:
        return None
    if isinstance(start, bool) or isinstance(end, bool):
        return None
    if not isinstance(start, int) or not isinstance(end, int):
        return None
    return start, end


def _timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = value.strip()
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _validate_segment_metadata(
    coverage: dict[str, Any], text_length: int
) -> tuple[list[tuple[int, int]], list[dict[str, Any]]]:
    """Validate the reviewed semantic segments required by the workflow contract."""
    errors: list[dict[str, Any]] = []
    raw_segments = coverage.get("semantic_segments")
    if not isinstance(raw_segments, list) or not raw_segments:
        return [], [_error("COVERAGE_REVIEW_METADATA_MISSING", "coverage needs reviewed semantic_segments")]
    ranges: list[tuple[int, int]] = []
    for index, segment in enumerate(raw_segments):
        if not isinstance(segment, dict):
            errors.append(_error("COVERAGE_REVIEW_METADATA_INVALID", "semantic segment must be an object", index=index))
            continue
        pair = _range_pair(segment)
        if pair is None:
            errors.append(_error("COVERAGE_REVIEW_METADATA_INVALID", "semantic segment needs integer start/end", index=index))
            continue
        start, end = pair
        if start < 0 or end <= start or end > text_length:
            errors.append(_error("COVERAGE_REVIEW_METADATA_INVALID", "semantic segment is outside the source view", index=index))
        required_strings = ("reader", "reviewer", "note")
        if any(not isinstance(segment.get(field), str) or not segment[field].strip() for field in required_strings):
            errors.append(_error("COVERAGE_REVIEW_METADATA_INVALID", "semantic segment needs reader, reviewer and note", index=index))
        read_at = _timestamp(segment.get("read_at"))
        reviewed_at = _timestamp(segment.get("reviewed_at"))
        if read_at is None or reviewed_at is None or reviewed_at < read_at:
            errors.append(_error("COVERAGE_REVIEW_METADATA_INVALID", "semantic segment needs ordered timezone-aware read/review timestamps", index=index))
        ranges.append(pair)
    cursor = 0
    for index, (start, end) in enumerate(ranges):
        if start != cursor:
            code = "COVERAGE_OVERLAP" if start < cursor else "COVERAGE_GAP"
            errors.append(_error(code, "semantic segments must be contiguous and non-overlapping", index=index, expected_start=cursor, actual_start=start))
        cursor = max(cursor, end)
    if cursor != text_length:
        errors.append(_error("COVERAGE_GAP", "semantic segments do not reach the end of the source view", expected_end=text_length, actual_end=cursor))
    return ranges, errors


def _coverage_ranges(entry: dict[str, Any], text_length: int) -> tuple[list[tuple[int, int]], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    coverage = _first_present(entry, ("coverage", "read_coverage"))
    if coverage is None:
        coverage = {}
    if not isinstance(coverage, dict):
        return [], [_error("COVERAGE_SHAPE_ERROR", "coverage must be an object")]
    view = coverage.get("view") if isinstance(coverage.get("view"), dict) else {}
    if view.get("unit") != "unicode_codepoint" or view.get("bounds") != "half_open" or view.get("start", 0) != 0:
        errors.append(_error("COVERAGE_COORDINATES_INVALID", "coverage view must use Unicode code points, half-open bounds and start at zero"))
    view_length = _first_present(coverage, ("view_length", "length"))
    if view_length is None:
        view_length = view.get("length", entry.get("view_length"))
    if not isinstance(view_length, int) or isinstance(view_length, bool):
        errors.append(_error("COVERAGE_LENGTH_MISSING", "coverage must declare a Unicode view length"))
        return [], errors
    if view_length != text_length:
        errors.append(
            _error(
                "COVERAGE_LENGTH_MISMATCH",
                "coverage view length does not equal the source Unicode length",
                expected=text_length,
                actual=view_length,
            )
        )
    reviewed_ranges, review_errors = _validate_segment_metadata(coverage, text_length)
    errors.extend(review_errors)
    ranges_raw = _first_present(coverage, ("ranges",))
    if ranges_raw is None:
        ranges_raw = _first_present(entry, ("ranges", "semantic_segments"))
    if ranges_raw is None:
        ranges_raw = reviewed_ranges
    if not isinstance(ranges_raw, list):
        errors.append(_error("COVERAGE_RANGES_MISSING", "coverage must provide ranges or reviewed semantic_segments"))
        return [], errors
    ranges: list[tuple[int, int]] = []
    for index, raw_range in enumerate(ranges_raw):
        pair = _range_pair(raw_range)
        if pair is None:
            errors.append(_error("COVERAGE_RANGE_INVALID", "range must contain integer start/end", index=index))
            continue
        start, end = pair
        if start < 0 or end < 0 or end < start or end > text_length:
            errors.append(_error("COVERAGE_RANGE_INVALID", "range is outside the source view", index=index))
            continue
        if end == start:
            errors.append(_error("COVERAGE_RANGE_EMPTY", "coverage ranges must have positive length", index=index))
            continue
        ranges.append(pair)
    unread = _first_present(coverage, ("unread_ranges",))
    if unread not in (None, [], ()):  # An explicit unread range is never a full read.
        errors.append(_error("COVERAGE_UNREAD", "coverage contains unread ranges"))
    cursor = 0
    for index, (start, end) in enumerate(ranges):
        if start > cursor:
            errors.append(
                _error("COVERAGE_GAP", "semantic coverage has a gap", expected_start=cursor, actual_start=start, index=index)
            )
        elif start < cursor:
            errors.append(
                _error(
                    "COVERAGE_OVERLAP",
                    "semantic coverage ranges overlap or are out of order",
                    expected_start=cursor,
                    actual_start=start,
                    index=index,
                )
            )
        cursor = max(cursor, end)
    if cursor != text_length:
        errors.append(
            _error("COVERAGE_GAP", "semantic coverage does not reach the end of the source view", expected_end=text_length, actual_end=cursor)
        )
    semantic_status = _first_present(coverage, ("semantic_review_status",))
    if semantic_status is None:
        semantic_status = entry.get("semantic_review_status")
    if semantic_status is None:
        errors.append(_error("COVERAGE_NOT_REVIEWED", "semantic coverage must declare a reviewed status"))
    elif semantic_status not in {"reviewed", "complete"}:
        errors.append(_error("COVERAGE_NOT_REVIEWED", "semantic coverage is not reviewed", status=semantic_status))
    return ranges, errors


def _evidence_items(entry: dict[str, Any], route: dict[str, Any]) -> list[Any]:
    for owner in (entry, route):
        for key in ("evidence", "evidence_quotes", "evidence_items"):
            if key in owner:
                value = owner[key]
                return value if isinstance(value, list) else []
    return []


def _validate_evidence(
    entry: dict[str, Any], source_id: str, text: str, route: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    raw_items = _evidence_items(entry, route)
    errors: list[dict[str, Any]] = []
    normalized: list[dict[str, Any]] = []
    if not raw_items:
        errors.append(_error("EVIDENCE_REQUIRED", "each routed source needs at least one exact evidence quote", source_id=source_id))
        return normalized, errors
    for index, raw in enumerate(raw_items):
        if not isinstance(raw, dict):
            errors.append(_error("EVIDENCE_SHAPE_ERROR", "evidence item must be an object", source_id=source_id, index=index))
            continue
        offset = raw.get("quote_offset", raw.get("offset"))
        if not isinstance(offset, dict):
            offset = {
                "start": raw.get("evidence_start", raw.get("start")),
                "end": raw.get("evidence_end", raw.get("end")),
                "unit": raw.get("unit"),
                "bounds": raw.get("bounds"),
            }
        start, end = offset.get("start"), offset.get("end")
        quote = raw.get("quote", raw.get("evidence_quote"))
        unit = offset.get("unit") or "unicode_codepoint"
        bounds = offset.get("bounds") or "half_open"
        if unit != "unicode_codepoint" or bounds != "half_open":
            errors.append(_error("EVIDENCE_COORDINATES_INVALID", "evidence must use Unicode code points and half-open bounds", source_id=source_id, index=index))
            continue
        if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool):
            errors.append(_error("EVIDENCE_OFFSET_INVALID", "evidence needs integer start/end offsets", source_id=source_id, index=index))
            continue
        if start < 0 or end <= start or end > len(text):
            errors.append(_error("EVIDENCE_OFFSET_INVALID", "evidence offset is outside the source", source_id=source_id, index=index))
            continue
        if not isinstance(quote, str):
            errors.append(_error("EVIDENCE_QUOTE_MISSING", "evidence needs a quote string", source_id=source_id, index=index))
            continue
        actual_quote = text[start:end]
        if actual_quote != quote:
            errors.append(
                _error(
                    "EVIDENCE_MISMATCH",
                    "evidence quote is not exact at its Unicode offsets",
                    source_id=source_id,
                    index=index,
                    expected=actual_quote,
                    supplied=quote,
                )
            )
            continue
        supplied_hash = raw.get("quote_hash", raw.get("excerpt_sha256"))
        if supplied_hash is not None:
            try:
                expected_hash = _hash_hex(supplied_hash, "quote_hash")
            except WorkflowError as exc:
                errors.append(_error("EVIDENCE_HASH_INVALID", str(exc), source_id=source_id, index=index))
                continue
            actual_hash = _sha256_bytes(quote.encode("utf-8"))
            if expected_hash != actual_hash:
                errors.append(_error("EVIDENCE_HASH_MISMATCH", "evidence quote hash does not match the quote", source_id=source_id, index=index))
                continue
        if raw.get("source_id") not in (None, source_id):
            errors.append(_error("EVIDENCE_SOURCE_MISMATCH", "evidence source_id differs from the entry", source_id=source_id, index=index))
            continue
        normalized.append(
            {
                "start": start,
                "end": end,
                "unit": "unicode_codepoint",
                "bounds": "half_open",
                "quote": quote,
                "quote_hash": _display_hash(_sha256_bytes(quote.encode("utf-8"))),
                "locator": raw.get("locator", f"chars {start}:{end}"),
            }
        )
    return normalized, errors


def _route_value(entry: dict[str, Any]) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    candidates: list[Any] = []
    for key in ("primary_route", "route", "routes"):
        if key not in entry:
            continue
        raw = entry[key]
        if key == "routes" or isinstance(raw, list):
            if not isinstance(raw, list) or len(raw) != 1:
                errors.append(_error("MULTIPLE_PRIMARY_ROUTES", "each source must have exactly one primary route"))
                continue
            raw = raw[0]
        candidates.append(raw)
    if len(candidates) != 1:
        if not candidates:
            errors.append(_error("PRIMARY_ROUTE_REQUIRED", "each source must have exactly one primary route"))
        elif len(candidates) > 1:
            errors.append(_error("MULTIPLE_PRIMARY_ROUTES", "route and primary_route cannot define multiple primaries"))
        return None, errors
    route = candidates[0]
    if not isinstance(route, dict):
        errors.append(_error("PRIMARY_ROUTE_SHAPE_ERROR", "primary route must be an object"))
        return None, errors
    domain, subdomain = route.get("domain"), route.get("subdomain")
    if not isinstance(domain, str) or not isinstance(subdomain, str):
        errors.append(_error("PRIMARY_ROUTE_INCOMPLETE", "primary route needs domain and subdomain"))
    return route, errors


def _requested_flags(manifest: dict[str, Any], entries: list[Any]) -> tuple[bool, bool, bool, str]:
    values: list[Any] = []
    for key in ("requested_gates", "gates", "gate", "requested_gate", "requested_outputs", "outputs", "artifacts"):
        value = manifest.get(key)
        if isinstance(value, list):
            values.extend(value)
        elif isinstance(value, str):
            values.append(value)
    if manifest.get("terms_gate_requested") is True or manifest.get("domain_terms_complete") is True:
        values.append("T")
    if manifest.get("master_requested") is True or manifest.get("publish_master") is True:
        values.append("master")
    operation = str(manifest.get("operation", manifest.get("mode", manifest.get("kind", "route")))).strip().lower()
    knowledge_requested = operation in KNOWLEDGE_OPERATION_NAMES
    if any(key in manifest for key in ("terms", "claims", "concepts", "masters")):
        knowledge_requested = True
    names = {str(value).strip().lower() for value in values}
    t_requested = bool(names & GATE_T_NAMES)
    master_requested = bool(names & GATE_MASTER_NAMES)
    if t_requested or master_requested:
        knowledge_requested = True
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        entry_operation = str(entry.get("operation", entry.get("mode", ""))).strip().lower()
        entry_coverage = entry.get("coverage")
        if not isinstance(entry_coverage, dict):
            entry_coverage = entry.get("read_coverage") if isinstance(entry.get("read_coverage"), dict) else {}
        coverage_mode = str(entry_coverage.get("mode", "")).strip().lower()
        if (
            entry_operation in KNOWLEDGE_OPERATION_NAMES
            or coverage_mode in KNOWLEDGE_OPERATION_NAMES
            or entry.get("extract") is True
            or any(key in entry for key in ("terms", "claims", "concepts", "masters"))
            or entry.get("source_extraction_status") in {"in_progress", "reviewed", "complete"}
        ):
            knowledge_requested = True
        entry_gate_values: list[Any] = []
        for key in ("requested_gates", "gates", "requested_gate", "requested_outputs", "outputs", "artifacts"):
            value = entry.get(key)
            if isinstance(value, list):
                entry_gate_values.extend(value)
            elif isinstance(value, str):
                entry_gate_values.append(value)
        for value in entry_gate_values:
            normalized = str(value).strip().lower()
            t_requested = t_requested or normalized in GATE_T_NAMES
            master_requested = master_requested or normalized in GATE_MASTER_NAMES
        if entry_gate_values:
            knowledge_requested = True
    return knowledge_requested, t_requested, master_requested, operation


def _full_domain_snapshot(manifest: dict[str, Any], domain: str, catalog_domains: dict[str, dict[str, str]]) -> bool:
    scope_kind = str(manifest.get("scope_kind", "")).strip().lower()
    if scope_kind not in {"domain_snapshot", "full_domain", "full_snapshot"}:
        return False
    if manifest.get("subset") is True or manifest.get("inventory_complete") is not True:
        return False
    if manifest.get("batch_complete") is False:
        return False
    if manifest.get("coverage_status") not in {"complete", "closed", "full"}:
        return False
    unresolved = manifest.get("unresolved_candidates", [])
    if unresolved not in ([], None):
        return False
    all_subdomains = manifest.get("all_subdomain_ids")
    if not isinstance(all_subdomains, list) or set(all_subdomains) != set(catalog_domains.get(domain, {})):
        return False
    candidate_ids = manifest.get("all_candidate_source_ids")
    if not isinstance(candidate_ids, list) or len(candidate_ids) != len(set(candidate_ids)):
        return False
    entries = _manifest_entries(manifest)
    candidate_manifest = manifest.get("candidate_manifest", entries)
    if not isinstance(candidate_manifest, list):
        return False
    manifest_ids = {
        item.get("source_id")
        for item in candidate_manifest
        if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }
    return manifest_ids == set(candidate_ids)


def _path_for_manifest(vault: Path, manifest_path: str | Path) -> Path:
    path = _relative_vault_path(vault, manifest_path, label="manifest path")
    _assert_no_symlink_components(vault, path)
    info = _lstat(path)
    if info is None or not stat.S_ISREG(info.st_mode):
        raise WorkflowError("manifest path must be a regular file inside the wiki root")
    return path


def _validate_reviewer_report(
    vault: Path,
    report_value: str | Path,
    manifest_sha256: str,
    manifest_author: str | None,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    try:
        report_path = _path_for_manifest(vault, report_value)
        report, _ = _load_json(report_path, label="reviewer report")
    except WorkflowError as exc:
        return None, [_error("REVIEWER_REPORT_INVALID", str(exc))]
    if not isinstance(report, dict):
        return None, [_error("REVIEWER_REPORT_SHAPE_ERROR", "reviewer report must contain an object")]
    if report.get("report_type") not in {"independent_reviewer", "independent_review"}:
        errors.append(_error("REVIEWER_NOT_INDEPENDENT", "report_type must identify an independent reviewer report"))
    if report.get("independent") is not True:
        errors.append(_error("REVIEWER_NOT_INDEPENDENT", "reviewer report must declare independent=true"))
    if str(report.get("decision", "")).lower() != "pass":
        errors.append(_error("REVIEWER_NOT_PASS", "reviewer report decision must be pass"))
    reviewer = report.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        errors.append(_error("REVIEWER_MISSING", "reviewer report needs a reviewer identity"))
    elif manifest_author is None:
        errors.append(_error("AUTHOR_MISSING", "manifest needs an author identity so independence can be checked"))
    elif reviewer.strip() == manifest_author.strip():
        errors.append(_error("REVIEWER_NOT_INDEPENDENT", "reviewer must differ from the manifest author"))
    try:
        reported_hash = _hash_hex(report.get("manifest_sha256"), "manifest_sha256")
        if reported_hash != manifest_sha256:
            errors.append(_error("REVIEWER_MANIFEST_MISMATCH", "reviewer report does not cover this exact manifest"))
    except WorkflowError as exc:
        errors.append(_error("REVIEWER_MANIFEST_MISSING", str(exc)))
    if report.get("validation_ok") is not True:
        errors.append(_error("REVIEWER_VALIDATION_MISSING", "reviewer report must record validation_ok=true"))
    reviewed_at = _timestamp(report.get("reviewed_at"))
    if reviewed_at is None:
        errors.append(_error("REVIEWER_METADATA_INVALID", "reviewer report needs a timezone-aware reviewed_at timestamp"))
    return report, errors


def validate_batch(vault: Path, manifest_path: str | Path) -> dict[str, Any]:
    """Validate one manifest without writing any file."""
    vault = vault.resolve(strict=False)
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    manifest_bytes = b""
    manifest: dict[str, Any] = {}
    try:
        path = _path_for_manifest(vault, manifest_path)
        loaded, manifest_bytes = _load_json(path, label="batch manifest")
        if not isinstance(loaded, dict):
            raise WorkflowError("batch manifest must contain an object")
        manifest = loaded
    except WorkflowError as exc:
        return {
            "ok": False,
            "vault": str(vault),
            "manifest": str(manifest_path),
            "manifest_sha256": _display_hash(_sha256_bytes(manifest_bytes)) if manifest_bytes else None,
            "errors": [_error("MANIFEST_READ_ERROR", str(exc))],
            "warnings": [],
            "entries": [],
            "summary": {"entries": 0, "valid_entries": 0},
            "writes_performed": 0,
        }
    catalog, processing, config_errors = _load_configs(vault)
    errors.extend(config_errors)
    domains = _catalog_domains(catalog)
    manifest_sha256 = _sha256_bytes(manifest_bytes)
    entries = _manifest_entries(manifest)
    if not isinstance(manifest.get("batch_id"), str) or not manifest.get("batch_id"):
        errors.append(_error("BATCH_ID_REQUIRED", "manifest needs batch_id"))
    if not isinstance(manifest.get("snapshot_id"), str) or not manifest.get("snapshot_id"):
        errors.append(_error("SNAPSHOT_ID_REQUIRED", "manifest needs snapshot_id"))
    if not entries:
        errors.append(_error("ENTRIES_REQUIRED", "manifest needs a non-empty entries or candidate_manifest list"))
    if manifest.get("domain") is not None and manifest.get("domain") not in domains:
        errors.append(_error("UNKNOWN_DOMAIN", "manifest domain is not in domain_catalog.json", domain=manifest.get("domain")))

    knowledge_requested, t_requested, master_requested, operation = _requested_flags(manifest, entries)
    current_domain, current_status = _current_domain(processing)
    entry_reports: list[dict[str, Any]] = []
    source_ids: dict[str, tuple[str, str]] = {}
    paths: dict[str, tuple[str, str]] = {}
    hashes: dict[str, set[str]] = {}
    routes_by_source: dict[str, tuple[str, str]] = {}
    route_domains: set[str] = set()
    for index, raw_entry in enumerate(entries):
        entry_errors: list[dict[str, Any]] = []
        entry_warnings: list[dict[str, Any]] = []
        if not isinstance(raw_entry, dict):
            errors.append(_error("ENTRY_SHAPE_ERROR", "manifest entry must be an object", index=index))
            entry_reports.append({"index": index, "ok": False, "errors": [_error("ENTRY_SHAPE_ERROR", "entry is not an object")]})
            continue
        entry = raw_entry
        source_id = entry.get("source_id")
        try:
            source_id = _safe_id(source_id, label="source_id")
        except WorkflowError as exc:
            entry_errors.append(_error("SOURCE_ID_INVALID", str(exc), index=index))
            source_id = str(source_id) if source_id is not None else f"<entry-{index}>"
        raw_path = _first_present(entry, ("path", "source_path", "original_path"))
        try:
            relative_path = _safe_relative(raw_path, label="source path")
        except WorkflowError as exc:
            entry_errors.append(_error("PATH_INVALID", str(exc), source_id=source_id))
            relative_path = str(raw_path) if raw_path is not None else ""
        try:
            declared_hash = _hash_hex(
                _first_present(entry, ("content_hash", "source_sha256", "original_sha256")),
                "content_hash",
            )
        except WorkflowError as exc:
            entry_errors.append(_error("HASH_INVALID", str(exc), source_id=source_id))
            declared_hash = ""
        actual_hash = None
        text = ""
        source_size = None
        if relative_path:
            try:
                source = _assert_regular_source(vault, relative_path)
                data, before, after = _read_stable(source)
                actual_hash = _sha256_bytes(data)
                source_size = len(data)
                try:
                    text = data.decode("utf-8")
                except UnicodeDecodeError as exc:
                    entry_errors.append(_error("SOURCE_NOT_UTF8", str(exc), source_id=source_id))
                if actual_hash != declared_hash:
                    entry_errors.append(
                        _error(
                            "HASH_MISMATCH",
                            "manifest hash does not match the source bytes",
                            source_id=source_id,
                            expected=_display_hash(actual_hash),
                            supplied=_display_hash(declared_hash) if declared_hash else None,
                        )
                    )
                if before.st_size == 0:
                    entry_errors.append(_error("EMPTY_SOURCE", "empty sources cannot be routed", source_id=source_id))
                if entry.get("size_bytes") is not None and entry.get("size_bytes") != len(data):
                    entry_errors.append(_error("SIZE_MISMATCH", "manifest size_bytes does not match source bytes", source_id=source_id))
            except (OSError, WorkflowError) as exc:
                entry_errors.append(_error("SOURCE_READ_ERROR", str(exc), source_id=source_id, path=relative_path))
        route, route_errors = _route_value(entry)
        for error in route_errors:
            error.setdefault("source_id", source_id)
        entry_errors.extend(route_errors)
        evidence: list[dict[str, Any]] = []
        if route is not None and text:
            evidence, evidence_errors = _validate_evidence(entry, source_id, text, route)
            entry_errors.extend(evidence_errors)
        elif route is not None:
            entry_errors.append(_error("EVIDENCE_REQUIRED", "evidence cannot be checked without a decoded source", source_id=source_id))
        route_domain = None
        route_subdomain = None
        if route is not None:
            route_domain = route.get("domain")
            route_subdomain = route.get("subdomain")
            route_key = (str(route_domain), str(route_subdomain))
            previous_route = routes_by_source.get(str(source_id))
            if previous_route is not None and previous_route != route_key:
                entry_errors.append(
                    _error(
                        "MULTIPLE_PRIMARY_ROUTES",
                        "one source identity cannot have multiple primary routes",
                        source_id=source_id,
                    )
                )
            else:
                routes_by_source[str(source_id)] = route_key
            if route_domain not in domains:
                entry_errors.append(_error("UNKNOWN_DOMAIN", "route domain is not in the catalog", source_id=source_id, domain=route_domain))
            elif route_subdomain not in domains[route_domain]:
                entry_errors.append(
                    _error(
                        "UNKNOWN_SUBDOMAIN",
                        "route subdomain is not in the catalog",
                        source_id=source_id,
                        domain=route_domain,
                        subdomain=route_subdomain,
                    )
                )
            else:
                route_domains.add(route_domain)
            if manifest.get("domain") is not None and route_domain != manifest.get("domain"):
                entry_errors.append(_error("DOMAIN_MISMATCH", "entry route differs from manifest domain", source_id=source_id))
        if text:
            _, coverage_errors = _coverage_ranges(entry, len(text))
            entry_errors.extend(coverage_errors)
        # A source identity may not map to two different paths or hashes.
        if isinstance(source_id, str) and source_id in source_ids:
            old_path, old_hash = source_ids[source_id]
            if old_path != relative_path or (declared_hash and old_hash != declared_hash):
                entry_errors.append(_error("HASH_COLLISION", "source_id maps to conflicting path or hash", source_id=source_id))
        else:
            source_ids[str(source_id)] = (relative_path, declared_hash)
        if relative_path in paths:
            old_id, old_hash = paths[relative_path]
            if old_id != source_id or (declared_hash and old_hash != declared_hash):
                entry_errors.append(_error("HASH_COLLISION", "path maps to conflicting source identity or hash", path=relative_path))
        else:
            paths[relative_path] = (str(source_id), declared_hash)
        if actual_hash:
            hashes.setdefault(actual_hash, set()).add(str(source_id))
        entry_reports.append(
            {
                "index": index,
                "candidate_id": entry.get("candidate_id"),
                "source_id": source_id,
                "path": relative_path,
                "actual_sha256": _display_hash(actual_hash) if actual_hash else None,
                "size_bytes": source_size,
                "route": route,
                "evidence": evidence,
                "ok": not entry_errors,
                "errors": entry_errors,
                "warnings": entry_warnings,
            }
        )
        errors.extend(entry_errors)
        warnings.extend(entry_warnings)
    for actual_hash, ids in hashes.items():
        if len(ids) > 1:
            duplicate_ids = {str(item.get("source_id")) for item in entries if isinstance(item, dict) and item.get("duplicate_of")}
            if not ids.issubset(duplicate_ids):
                errors.append(
                    _error(
                        "DUPLICATE_HASH_REQUIRES_DECLARATION",
                        "identical bytes must be declared as a duplicate, not independent evidence",
                        sha256=_display_hash(actual_hash),
                        source_ids=sorted(ids),
                    )
                )
    if knowledge_requested:
        if not route_domains:
            errors.append(_error("CURRENT_DOMAIN_LOCK", "knowledge operation has no valid route domain"))
        for domain in sorted(route_domains):
            domain_status = _processing_status(processing, domain)
            if domain_status == "pending":
                errors.append(_error("PENDING_EXTRACTION", "pending domains may be routed but not extracted", domain=domain))
            if current_domain is None or domain != current_domain or current_status not in {"active", "in_progress"}:
                errors.append(
                    _error(
                        "CURRENT_DOMAIN_LOCK",
                        "knowledge extraction is restricted to the configured current active domain",
                        current_domain=current_domain,
                        requested_domain=domain,
                        current_status=current_status,
                    )
                )
    else:
        for domain in sorted(route_domains):
            if _processing_status(processing, domain) == "pending":
                warnings.append(_warning("PENDING_ROUTE_ALLOWED", "pending domain is routeable, but no extraction is authorized", domain=domain))
    requested_domain = manifest.get("domain")
    if requested_domain is None and len(route_domains) == 1:
        requested_domain = next(iter(route_domains))
    full_snapshot = bool(requested_domain and _full_domain_snapshot(manifest, requested_domain, domains))
    if t_requested and not full_snapshot:
        errors.append(_error("T_REQUIRES_FULL_DOMAIN_SNAPSHOT", "T cannot pass for a subset or partial batch", domain=requested_domain))
    if master_requested and not full_snapshot:
        errors.append(_error("MASTER_REQUIRES_FULL_DOMAIN_SNAPSHOT", "Master cannot start from a subset or partial batch", domain=requested_domain))
    if master_requested and full_snapshot:
        terms_status = manifest.get("t_gate_status", manifest.get("terms_gate_status"))
        if terms_status != "pass" and manifest.get("t_gate_passed") is not True:
            errors.append(_error("MASTER_REQUIRES_T", "Master requires an explicitly passed current T gate"))
    if operation in {"route", "routing", "intake", ""} and (t_requested or master_requested):
        warnings.append(_warning("GATE_REQUEST_IS_NOT_PUBLISH", "publish creates routing artifacts only; it never closes T or creates a Master"))
    summary = {
        "entries": len(entries),
        "valid_entries": sum(1 for report in entry_reports if report.get("ok")),
        "unique_source_ids": len(source_ids),
        "unique_hashes": len(hashes),
        "route_domains": sorted(route_domains),
        "operation": operation,
        "knowledge_requested": knowledge_requested,
        "t_requested": t_requested,
        "master_requested": master_requested,
        "full_domain_snapshot": full_snapshot,
    }
    return {
        "ok": not errors,
        "vault": str(vault),
        "manifest": str(manifest_path),
        "manifest_sha256": _display_hash(manifest_sha256),
        "manifest_author": _first_present(manifest, ("author", "created_by", "producer")),
        "batch_id": manifest.get("batch_id"),
        "snapshot_id": manifest.get("snapshot_id"),
        "catalog_revision": _catalog_revision(catalog),
        "current_domain": current_domain,
        "current_domain_status": current_status,
        "entries": entry_reports,
        "summary": summary,
        "errors": errors,
        "warnings": warnings,
        "writes_performed": 0,
        "domain_completion_claim": False,
    }


def _route_copy_name(source_id: str, source_path: str) -> str:
    suffix = Path(source_path).suffix
    if suffix and ("/" in suffix or "\\" in suffix or "\x00" in suffix):
        raise WorkflowError("source extension is unsafe")
    return f"{source_id}{suffix}"


def _ensure_directory_no_symlink(root: Path, relative: Path) -> Path:
    current = root.resolve(strict=False)
    _assert_no_symlink_components(root, current)
    for part in relative.parts:
        if part in {"", ".", ".."}:
            raise WorkflowError("directory path is not traversal-free")
        current = current / part
        info = _lstat(current)
        if info is None:
            current.mkdir()
        elif stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise WorkflowError(f"destination component is not a regular directory: {current}")
    return current


def _exclusive_write(path: Path, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags | nofollow, 0o644)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        # The file remains visible rather than being silently deleted.  This
        # follows the workspace no-delete policy and makes a partial write a
        # reviewable finding.
        raise


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _route_markdown(report: dict[str, Any], reviewer: str, reviewer_report: str | None) -> str:
    route = report.get("route") or {}
    lines = [
        f"# Route {report['source_id']}",
        "",
        "- route_status: `route_done`",
        "- source_extraction_status: `not_started`",
        f"- source_id: `{report['source_id']}`",
        f"- source_path: `{report['path']}`",
        f"- content_hash: `{report['actual_sha256']}`",
        f"- primary_route: `{route.get('domain')}/{route.get('subdomain')}`",
        f"- reviewer: `{reviewer}`",
        f"- independent_reviewer_report: `{reviewer_report or 'not supplied in dry-run'}`",
        "",
        "## Boundary",
        "",
        "This file records routing and copy verification only. It is not a Claim, Concept, Master, source_done, or domain_done record.",
        "",
        "## Exact evidence",
        "",
    ]
    for evidence in report.get("evidence", []):
        quote = str(evidence.get("quote", "")).replace("\n", "\\n")
        lines.append(
            f"- `[{evidence.get('start')},{evidence.get('end')})` "
            f"`{evidence.get('quote_hash')}`: {quote}"
        )
    lines.extend(["", "## Checks", "", "- path: PASS", "- source hash: PASS", "- semantic coverage: PASS", "- exact evidence: PASS", "- one primary route: PASS", "- independent byte-exact copy: PASS", "- symlink/hardlink: PASS", "- raw mutation: false", ""])
    return "\n".join(lines)


def _index_markdown(domain: str, subdomain: str, reports: list[dict[str, Any]]) -> str:
    lines = [
        f"# done/{domain}/{subdomain}",
        "",
        "This local index lists verified route copies. It does not claim source_done, domain_terms_complete, Master readiness, or domain_done.",
        "",
        "| source_id | copy | REF | ROUTE | status | extraction |",
        "|---|---|---|---|---|---|",
    ]
    for report in sorted(reports, key=lambda item: str(item["source_id"])):
        source_id = report["source_id"]
        copy_name = _route_copy_name(source_id, report["path"])
        lines.append(
            f"| `{source_id}` | `{copy_name}` | `REF_{source_id}.json` | `ROUTE_{source_id}.md` | `route_done` | `not_started` |"
        )
    lines.extend(["", "## Scope", "", f"- domain: `{domain}`", f"- subdomain: `{subdomain}`", "- primary copies: one per source identity", "- raw source: unchanged", "- knowledge completion: not asserted", ""])
    return "\n".join(lines)


def _verify_existing_group(
    vault: Path,
    destination: Path,
    group: list[dict[str, Any]],
    validation: dict[str, Any],
    reviewer: str,
    reviewer_path: str | None,
) -> list[dict[str, Any]]:
    """Prove an existing destination is the exact prior publish, without writing."""
    errors: list[dict[str, Any]] = []
    try:
        children = list(destination.iterdir())
    except OSError as exc:
        return [_error("DESTINATION_READ_ERROR", str(exc), path=str(destination.relative_to(vault)))]
    expected_names: set[str] = set()
    for report in group:
        try:
            expected_names.update(
                {
                    _route_copy_name(str(report["source_id"]), str(report["path"])),
                    f"REF_{report['source_id']}.json",
                    f"ROUTE_{report['source_id']}.md",
                }
            )
        except WorkflowError as exc:
            errors.append(_error("DESTINATION_NAME_INVALID", str(exc), source_id=report.get("source_id")))
    expected_names.add("INDEX.md")
    actual_names = {child.name for child in children}
    if actual_names != expected_names:
        errors.append(
            _error(
                "DESTINATION_ARTIFACT_MISMATCH",
                "existing destination does not contain exactly the expected artifacts",
                path=str(destination.relative_to(vault)),
                expected=sorted(expected_names),
                actual=sorted(actual_names),
            )
        )
    for child in children:
        info = _lstat(child)
        if info is None or stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            errors.append(_error("DESTINATION_ARTIFACT_UNSAFE", "existing artifacts must be regular independent files", path=str(child.relative_to(vault))))
    for report in group:
        source_id = str(report["source_id"])
        expected_reviewer = reviewer
        expected_reviewer_path = reviewer_path
        try:
            source = _assert_regular_source(vault, report["path"])
            data, before, after = _read_stable(source)
            actual_hash = _sha256_bytes(data)
            if actual_hash != str(report.get("actual_sha256", "")).removeprefix("sha256:"):
                errors.append(_error("SOURCE_CHANGED_BEFORE_IDEMPOTENT_CHECK", "source changed before idempotent verification", source_id=source_id))
                continue
            copy_path = destination / _route_copy_name(source_id, str(report["path"]))
            copy_info = _lstat(copy_path)
            if copy_info is None or stat.S_ISLNK(copy_info.st_mode) or not stat.S_ISREG(copy_info.st_mode):
                errors.append(_error("DESTINATION_COPY_INVALID", "existing source copy is not a regular file", source_id=source_id))
            elif copy_info.st_nlink != 1 or (copy_info.st_dev, copy_info.st_ino) == (before.st_dev, before.st_ino):
                errors.append(_error("DESTINATION_COPY_NOT_INDEPENDENT", "existing source copy is linked to another file", source_id=source_id))
            elif copy_info.st_size != len(data) or _sha256_path(copy_path) != actual_hash or copy_path.read_bytes() != data:
                errors.append(_error("DESTINATION_COPY_MISMATCH", "existing source copy is not byte-exact", source_id=source_id))
            ref_path = destination / f"REF_{source_id}.json"
            try:
                ref, _ = _load_json(ref_path, label="existing REF artifact")
            except WorkflowError as exc:
                errors.append(_error("DESTINATION_REF_INVALID", str(exc), source_id=source_id))
                ref = None
            route = report.get("route") or {}
            if isinstance(ref, dict):
                if reviewer == "dry-run":
                    stored_reviewer = ref.get("reviewer")
                    stored_reviewer_path = ref.get("reviewer_report")
                    if isinstance(stored_reviewer, str) and stored_reviewer.strip():
                        expected_reviewer = stored_reviewer
                    if isinstance(stored_reviewer_path, str):
                        expected_reviewer_path = stored_reviewer_path
                expected_copy_path = str(copy_path.relative_to(vault))
                expected_fields = {
                    "source_id": source_id,
                    "original_path": report["path"],
                    "source_path": report["path"],
                    "copy_path": expected_copy_path,
                    "original_size_bytes": len(data),
                    "copy_size_bytes": len(data),
                    "original_sha256": _display_hash(actual_hash),
                    "copy_sha256": _display_hash(actual_hash),
                    "copy_policy": "verified_copy_required",
                    "verification_policy": "independent_byte_exact",
                    "artifact_kind": "verified_source_copy_reference",
                    "workflow_contract_version": "2026-10-10",
                    "candidate_id": report.get("candidate_id"),
                    "snapshot_id": validation.get("snapshot_id"),
                    "domain_snapshot_id": validation.get("snapshot_id"),
                    "catalog_revision": validation.get("catalog_revision"),
                    "primary_route": route,
                    "primary_domain": route.get("domain"),
                    "primary_subdomain": route.get("subdomain"),
                    "routing_reason": route.get("rationale", "manifest-reviewed route"),
                    "body_locator": route.get("body_locator"),
                    "structure_locator": route.get("structure_locator"),
                    "purpose_locator": route.get("purpose_locator"),
                    "evidence": report.get("evidence", []),
                    "read_coverage": {"status": "full_unicode_range_checked"},
                    "secondary_references": [],
                    "duplicate_of": None,
                    "route_status": "route_done",
                    "source_extraction_status": "not_started",
                    "source_status": "new",
                    "reviewer": expected_reviewer,
                    "reviewer_report": expected_reviewer_path,
                    "raw_mutation": False,
                    "domain_completion_claim": False,
                    "copy_independence_check": {
                        "hashes_equal": True,
                        "bytes_equal": True,
                        "symlink": False,
                        "hardlink": False,
                        "same_inode": False,
                        "original_unchanged": before.st_ino == after.st_ino and before.st_mtime_ns == after.st_mtime_ns,
                    },
                }
                for key, expected in expected_fields.items():
                    if ref.get(key) != expected:
                        errors.append(_error("DESTINATION_REF_MISMATCH", f"existing REF field {key} differs", source_id=source_id))
                if _timestamp(ref.get("verified_at")) is None:
                    errors.append(_error("DESTINATION_REF_METADATA_INVALID", "existing REF needs verified_at", source_id=source_id))
            elif ref is not None:
                errors.append(_error("DESTINATION_REF_SHAPE_ERROR", "existing REF artifact must contain an object", source_id=source_id))
            route_path = destination / f"ROUTE_{source_id}.md"
            try:
                if route_path.read_bytes() != _route_markdown(report, expected_reviewer, expected_reviewer_path).encode("utf-8"):
                    errors.append(_error("DESTINATION_ROUTE_MISMATCH", "existing ROUTE artifact differs", source_id=source_id))
            except OSError as exc:
                errors.append(_error("DESTINATION_ROUTE_INVALID", str(exc), source_id=source_id))
        except (OSError, WorkflowError) as exc:
            errors.append(_error("DESTINATION_VERIFY_ERROR", str(exc), source_id=source_id))
    if group:
        index_path = destination / "INDEX.md"
        try:
            expected_index = _index_markdown(group[0]["route"]["domain"], group[0]["route"]["subdomain"], group)
            if index_path.read_bytes() != expected_index.encode("utf-8"):
                errors.append(_error("DESTINATION_INDEX_MISMATCH", "existing INDEX artifact differs", path=str(index_path.relative_to(vault))))
        except (KeyError, OSError) as exc:
            errors.append(_error("DESTINATION_INDEX_INVALID", str(exc), path=str(index_path.relative_to(vault))))
    return errors


def _destination_plan(vault: Path, validation: dict[str, Any], reviewer: dict[str, Any] | None, reviewer_path: str | None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    plans: list[dict[str, Any]] = []
    reviewer_name = str((reviewer or {}).get("reviewer", "dry-run"))
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for report in validation.get("entries", []):
        if not report.get("ok"):
            continue
        route = report.get("route") or {}
        key = (str(route.get("domain")), str(route.get("subdomain")))
        groups.setdefault(key, []).append(report)
    for (domain, subdomain), group in sorted(groups.items()):
        try:
            _safe_id(domain, label="domain")
            _safe_id(subdomain, label="subdomain")
        except WorkflowError as exc:
            errors.append(_error("DESTINATION_ID_INVALID", str(exc), domain=domain, subdomain=subdomain))
            continue
        destination = vault / "done" / domain / subdomain
        try:
            _assert_no_symlink_components(vault, destination)
        except WorkflowError as exc:
            errors.append(_error("DESTINATION_SYMLINK", str(exc), path=str(destination.relative_to(vault))))
            continue
        names: set[str] = set()
        group_plans: list[dict[str, Any]] = []
        for report in group:
            try:
                copy_name = _route_copy_name(str(report["source_id"]), str(report["path"]))
            except WorkflowError as exc:
                errors.append(_error("DESTINATION_NAME_INVALID", str(exc), source_id=report.get("source_id")))
                continue
            artifact_names = {copy_name, f"REF_{report['source_id']}.json", f"ROUTE_{report['source_id']}.md"}
            if names & artifact_names:
                errors.append(_error("DESTINATION_COLLISION", "two entries would write the same artifact name", path=str(destination.relative_to(vault))))
            names.update(artifact_names)
            group_plans.append(
                {
                    "domain": domain,
                    "subdomain": subdomain,
                    "destination": destination,
                    "report": report,
                    "copy_name": copy_name,
                    "reviewer": reviewer_name,
                    "reviewer_report": reviewer_path,
                }
            )
        index_name = "INDEX.md"
        if index_name in names:
            errors.append(_error("DESTINATION_COLLISION", "INDEX.md collides with a source artifact"))
        names.add(index_name)
        for plan in group_plans:
            plan["artifact_names"] = sorted(names)
            plan["group_reports"] = group
        destination_info = _lstat(destination)
        if destination_info is not None:
            if not stat.S_ISDIR(destination_info.st_mode) or stat.S_ISLNK(destination_info.st_mode):
                errors.append(_error("DESTINATION_EXISTS", "destination exists but is not a regular directory", path=str(destination.relative_to(vault))))
            else:
                existing_errors = _verify_existing_group(vault, destination, group, validation, reviewer_name, reviewer_path)
                if existing_errors:
                    errors.extend(existing_errors)
                else:
                    for plan in group_plans:
                        plan["already_published"] = True
        plans.extend(group_plans)
    return plans, errors


def _apply_plans(vault: Path, plans: list[dict[str, Any]], validation: dict[str, Any]) -> dict[str, Any]:
    written: list[str] = []
    verified_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    grouped: dict[Path, list[dict[str, Any]]] = {}
    for plan in plans:
        grouped.setdefault(plan["destination"], []).append(plan)
    try:
        for destination, group in grouped.items():
            if all(plan.get("already_published") for plan in group):
                continue
            relative_destination = destination.relative_to(vault)
            _ensure_directory_no_symlink(vault, relative_destination.parent)
            if _lstat(destination) is not None:
                raise WorkflowError(f"destination appeared during publish: {relative_destination}")
            destination.mkdir()
            if _is_symlink(destination):
                raise WorkflowError("destination became a symlink")
            for plan in group:
                report = plan["report"]
                source = _assert_regular_source(vault, report["path"])
                data, before, after = _read_stable(source)
                actual_hash = _sha256_bytes(data)
                if actual_hash != str(report["actual_sha256"]).removeprefix("sha256:"):
                    raise WorkflowError(f"source changed before publish: {report['source_id']}")
                copy_path = destination / plan["copy_name"]
                _exclusive_write(copy_path, data)
                written.append(str(copy_path.relative_to(vault)))
                copy_info = copy_path.lstat()
                if stat.S_ISLNK(copy_info.st_mode) or copy_info.st_ino == before.st_ino and copy_info.st_dev == before.st_dev:
                    raise WorkflowError(f"copy is not independent: {copy_path}")
                if copy_info.st_nlink != 1:
                    raise WorkflowError(f"hardlink copy is not allowed: {copy_path}")
                copy_hash = _sha256_path(copy_path)
                if copy_hash != actual_hash:
                    raise WorkflowError(f"byte-exact copy hash mismatch: {copy_path}")
                route = report.get("route") or {}
                ref = {
                    "schema_version": 1,
                    "artifact_kind": "verified_source_copy_reference",
                    "workflow_contract_version": "2026-10-10",
                    "source_id": report["source_id"],
                    "candidate_id": report.get("candidate_id"),
                    "snapshot_id": validation.get("snapshot_id"),
                    "domain_snapshot_id": validation.get("snapshot_id"),
                    "catalog_revision": validation.get("catalog_revision"),
                    "original_path": report["path"],
                    "source_path": report["path"],
                    "copy_path": str(copy_path.relative_to(vault)),
                    "original_size_bytes": len(data),
                    "copy_size_bytes": copy_info.st_size,
                    "original_sha256": _display_hash(actual_hash),
                    "copy_sha256": _display_hash(copy_hash),
                    "copy_policy": "verified_copy_required",
                    "verification_policy": "independent_byte_exact",
                    "copy_independence_check": {
                        "hashes_equal": copy_hash == actual_hash,
                        "bytes_equal": copy_info.st_size == len(data),
                        "symlink": stat.S_ISLNK(copy_info.st_mode),
                        "hardlink": copy_info.st_nlink != 1,
                        "same_inode": False,
                        "original_unchanged": before.st_ino == after.st_ino and before.st_mtime_ns == after.st_mtime_ns,
                    },
                    "primary_route": route,
                    "primary_domain": route.get("domain"),
                    "primary_subdomain": route.get("subdomain"),
                    "routing_reason": route.get("rationale", "manifest-reviewed route"),
                    "body_locator": route.get("body_locator"),
                    "structure_locator": route.get("structure_locator"),
                    "purpose_locator": route.get("purpose_locator"),
                    "evidence": report.get("evidence", []),
                    "read_coverage": {"status": "full_unicode_range_checked"},
                    "secondary_references": [],
                    "duplicate_of": None,
                    "route_status": "route_done",
                    "source_status": "new",
                    "source_extraction_status": "not_started",
                    "reviewer": plan["reviewer"],
                    "reviewer_report": plan["reviewer_report"],
                    "verified_at": verified_at,
                    "raw_mutation": False,
                    "domain_completion_claim": False,
                }
                ref_path = destination / f"REF_{report['source_id']}.json"
                _exclusive_write(ref_path, _json_bytes(ref))
                written.append(str(ref_path.relative_to(vault)))
                route_path = destination / f"ROUTE_{report['source_id']}.md"
                route_text = _route_markdown(report, plan["reviewer"], plan["reviewer_report"])
                _exclusive_write(route_path, route_text.encode("utf-8"))
                written.append(str(route_path.relative_to(vault)))
            index_path = destination / "INDEX.md"
            index_text = _index_markdown(group[0]["domain"], group[0]["subdomain"], [item["report"] for item in group])
            _exclusive_write(index_path, index_text.encode("utf-8"))
            written.append(str(index_path.relative_to(vault)))
    except (OSError, WorkflowError) as exc:
        # An exclusive write can leave a visible partial artifact before its
        # caller appends the path to ``written`` (for example, fsync failure).
        # Report every artifact that is visibly present; never delete it.
        for plan in plans:
            destination = plan["destination"]
            for name in plan.get("artifact_names", []):
                candidate = destination / name
                if _lstat(candidate) is not None:
                    relative = str(candidate.relative_to(vault))
                    if relative not in written:
                        written.append(relative)
        return {
            "ok": False,
            "applied": False,
            "partial_write": bool(written),
            "written": written,
            "errors": [_error("PUBLISH_WRITE_ERROR", str(exc))],
            "writes_performed": len(written),
            "already_published": False,
            "domain_completion_claim": False,
        }
    already_published = bool(plans) and all(plan.get("already_published") for plan in plans)
    return {
        "ok": True,
        "applied": not already_published,
        "partial_write": False,
        "written": written,
        "errors": [],
        "writes_performed": len(written),
        "already_published": already_published,
        "verified_at": verified_at,
        "domain_completion_claim": False,
    }


def publish(
    vault: Path,
    manifest_path: str | Path,
    *,
    apply: bool = False,
    reviewer_report_path: str | Path | None = None,
) -> dict[str, Any]:
    """Validate and optionally publish direct route artifacts.

    Without ``apply`` this function only returns a plan.  With ``apply`` it
    requires a machine-checkable independent reviewer report and performs all
    destination collision checks before the first write.
    """
    vault = vault.resolve(strict=False)
    validation = validate_batch(vault, manifest_path)
    result: dict[str, Any] = {
        "ok": validation["ok"],
        "applied": False,
        "dry_run": not apply,
        "validation": validation,
        "writes_performed": 0,
        "written": [],
        "errors": list(validation.get("errors", [])),
        "domain_completion_claim": False,
    }
    if not validation["ok"]:
        return result
    reviewer: dict[str, Any] | None = None
    reviewer_path_for_ref: str | None = None
    if apply:
        if reviewer_report_path is None:
            result["ok"] = False
            result["errors"].append(_error("REVIEWER_REPORT_REQUIRED", "--apply requires --reviewer-report"))
            return result
        try:
            reviewer_path = _path_for_manifest(vault, reviewer_report_path)
            reviewer_path_for_ref = str(reviewer_path.relative_to(vault))
        except WorkflowError as exc:
            result["ok"] = False
            result["errors"].append(_error("REVIEWER_REPORT_INVALID", str(exc)))
            return result
        reviewer, reviewer_errors = _validate_reviewer_report(
            vault,
            reviewer_path_for_ref,
            str(validation["manifest_sha256"]).removeprefix("sha256:"),
            validation.get("manifest_author") if isinstance(validation.get("manifest_author"), str) and validation.get("manifest_author").strip() else None,
        )
        if reviewer_errors:
            result["ok"] = False
            result["errors"].extend(reviewer_errors)
            return result
    plans, plan_errors = _destination_plan(vault, validation, reviewer, reviewer_path_for_ref)
    result["plan"] = [
        {
            "source_id": plan["report"]["source_id"],
            "copy_path": str((plan["destination"] / plan["copy_name"]).relative_to(vault)),
            "ref_path": str((plan["destination"] / f"REF_{plan['report']['source_id']}.json").relative_to(vault)),
            "route_path": str((plan["destination"] / f"ROUTE_{plan['report']['source_id']}.md").relative_to(vault)),
            "index_path": str((plan["destination"] / "INDEX.md").relative_to(vault)),
        }
        for plan in plans
    ]
    if plan_errors:
        result["ok"] = False
        result["errors"].extend(plan_errors)
        return result
    if not apply:
        result["ok"] = True
        return result
    applied = _apply_plans(vault, plans, validation)
    result.update(applied)
    result["validation"] = validation
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=DEFAULT_VAULT, help="wiki root (default: /sdcard/NEXUS_LLM_WIKI)")
    subparsers = parser.add_subparsers(dest="command", required=True)
    inventory_parser = subparsers.add_parser("inventory", help="read-only inventory of new/ and raw/new/")
    inventory_parser.add_argument("--json", action="store_true", help="emit JSON (the default output is also JSON)")
    status_parser = subparsers.add_parser("status", help="read current catalog and processing config")
    status_parser.add_argument("--json", action="store_true", help="emit JSON (the default output is also JSON)")
    validate_parser = subparsers.add_parser("validate-batch", help="validate a JSON batch manifest without writing")
    validate_parser.add_argument("--manifest", required=True, type=Path)
    validate_parser.add_argument("--json", action="store_true", help="emit JSON")
    publish_parser = subparsers.add_parser("publish", help="dry-run route publication; --apply enables writes")
    publish_parser.add_argument("--manifest", required=True, type=Path)
    publish_parser.add_argument("--reviewer-report", type=Path)
    publish_parser.add_argument("--apply", action="store_true", help="actually create new route artifacts")
    publish_parser.add_argument("--json", action="store_true", help="emit JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    vault = args.vault.resolve(strict=False)
    if args.command == "inventory":
        result = inventory(vault)
    elif args.command == "status":
        result = status(vault)
    elif args.command == "validate-batch":
        result = validate_batch(vault, args.manifest)
    elif args.command == "publish":
        result = publish(vault, args.manifest, apply=args.apply, reviewer_report_path=args.reviewer_report)
    else:  # pragma: no cover - argparse enforces the choices.
        parser.error("unknown command")
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
