#!/usr/bin/env python3
"""Regression tests for the read-first wiki workflow tool."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import wiki_workflow  # noqa: E402


class WikiWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        # Retain synthetic fixtures: the project explicitly forbids deletion.
        fixtures = TOOLS.parent / "staging" / "workflow-tests"
        fixtures.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix="runtime-", dir=fixtures))
        (self.root / "config").mkdir()
        (self.root / "new").mkdir()
        catalog = {
            "catalog_revision": "test-v1",
            "domains": [
                {
                    "domain_id": "sales",
                    "subdomains": [{"subdomain_id": "objection_handling"}],
                },
                {
                    "domain_id": "outreach",
                    "subdomains": [{"subdomain_id": "cold_email"}],
                },
            ],
        }
        processing = {
            "order": ["sales", "outreach"],
            "current_domain": "sales",
            "current_domain_status": "in_progress",
            "domain_states": [
                {"domain_id": "sales", "status": "in_progress"},
                {"domain_id": "outreach", "status": "pending"},
            ],
        }
        (self.root / "config/domain_catalog.json").write_text(
            json.dumps(catalog), encoding="utf-8"
        )
        (self.root / "config/processing_order.json").write_text(
            json.dumps(processing), encoding="utf-8"
        )

    def _source(self, name: str = "source.txt", text: str = "اسأل عن المشكلة قبل اقتراح الحل.") -> tuple[str, str, str]:
        path = self.root / "new" / name
        path.write_text(text, encoding="utf-8")
        source_id = "SRC_" + Path(name).stem
        return source_id, path.relative_to(self.root).as_posix(), text

    def _entry(
        self,
        source_id: str,
        relative_path: str,
        text: str,
        *,
        domain: str = "sales",
        subdomain: str = "objection_handling",
        ranges: list[list[int]] | None = None,
        quote: str | None = None,
    ) -> dict[str, object]:
        if quote is None:
            quote = text[: min(8, len(text))]
        end = len(quote)
        return {
            "candidate_id": "ITEM_" + source_id,
            "source_id": source_id,
            "path": relative_path,
            "content_hash": "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "primary_route": {
                "domain": domain,
                "subdomain": subdomain,
                "rationale": "الغرض الظاهر من متن المصدر",
                "body_locator": f"chars 0:{end}",
                "evidence_locators": [f"chars 0:{end}"],
            },
            "coverage": {
                "view": {"unit": "unicode_codepoint", "bounds": "half_open", "start": 0, "length": len(text)},
                "semantic_segments": [
                    {
                        "start": start, "end": end,
                        "reader": "reader-test", "read_at": "2026-10-10T00:00:00Z",
                        "reviewer": "coverage-qa", "reviewed_at": "2026-10-10T01:00:00Z",
                        "note": "مقطع اصطناعي لا يثبت قراءة أي مصدر حقيقي",
                    }
                    for start, end in (ranges if ranges is not None else [[0, len(text)]])
                ],
                "unread_ranges": [],
                "semantic_review_status": "reviewed",
            },
            "evidence": [
                {
                    "quote_offset": {"unit": "unicode_codepoint", "bounds": "half_open", "start": 0, "end": end},
                    "quote": quote,
                    "quote_hash": "sha256:" + hashlib.sha256(quote.encode("utf-8")).hexdigest(),
                }
            ],
        }

    def _manifest(self, entries: list[dict[str, object]], **extra: object) -> Path:
        manifest = {
            "schema_version": 1,
            "batch_id": "BATCH_TEST",
            "snapshot_id": "SNAP_TEST",
            "operation": "route",
            "author": "author-test",
            "scope_kind": "batch",
            "inventory_complete": False,
            "coverage_status": "partial",
            "entries": entries,
        }
        manifest.update(extra)
        path = self.root / "staging" / "batch.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _codes(self, result: dict[str, object]) -> set[str]:
        return {
            str(item.get("code"))
            for item in result.get("errors", [])
            if isinstance(item, dict)
        }

    def _review(self, manifest: Path, **extra: object) -> Path:
        report = {
            "report_type": "independent_reviewer", "independent": True,
            "decision": "pass", "reviewer": "qa-test", "validation_ok": True,
            "reviewed_at": "2026-10-11T00:00:00Z",
            "manifest_sha256": "sha256:" + hashlib.sha256(manifest.read_bytes()).hexdigest(),
        }
        report.update(extra)
        path = self.root / "reports/review.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(report), encoding="utf-8")
        return path

    def _snapshot(self) -> dict[str, tuple]:
        snapshot = {}
        for path in [self.root, *self.root.rglob("*")]:
            info = path.lstat()
            data = path.read_bytes() if stat.S_ISREG(info.st_mode) else None
            snapshot[path.relative_to(self.root).as_posix()] = (
                info.st_mode, info.st_ino, info.st_nlink, info.st_size, info.st_mtime_ns,
                hashlib.sha256(data).hexdigest() if data is not None else None,
            )
        return snapshot

    def _publish_fixture(self) -> tuple[Path, Path, Path]:
        entry = self._entry(*self._source(text="\ufeffنص 😀\r\nA\u0301\n"))
        manifest = self._manifest([entry])
        review = self._review(manifest)
        result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
        self.assertTrue(result["ok"], result["errors"])
        return manifest, review, self.root / "done/sales/objection_handling"

    def test_inventory_is_read_only(self) -> None:
        self._source()
        before = sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob("*"))
        result = wiki_workflow.inventory(self.root)
        after = sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob("*"))
        self.assertTrue(result["ok"])
        self.assertTrue(result["read_only"])
        self.assertEqual(result["writes_performed"], 0)
        self.assertEqual(before, after)

    def test_publish_defaults_to_dry_run(self) -> None:
        source_id, relative_path, text = self._source()
        manifest = self._manifest([self._entry(source_id, relative_path, text)])
        result = wiki_workflow.publish(self.root, manifest)
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["writes_performed"], 0)
        self.assertFalse((self.root / "done").exists())

    def test_apply_requires_independent_report_and_writes_exact_route_artifacts(self) -> None:
        source_id, relative_path, text = self._source()
        manifest = self._manifest([self._entry(source_id, relative_path, text)])
        without_report = wiki_workflow.publish(self.root, manifest, apply=True)
        self.assertFalse(without_report["ok"])
        self.assertIn("REVIEWER_REPORT_REQUIRED", self._codes(without_report))
        self.assertFalse((self.root / "done").exists())

        report_path = self._review(manifest)
        result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=report_path)
        self.assertTrue(result["ok"])
        output = self.root / "done/sales/objection_handling"
        copy_path = output / f"{source_id}.txt"
        self.assertEqual(copy_path.read_bytes(), (self.root / relative_path).read_bytes())
        self.assertEqual((output / f"REF_{source_id}.json").exists(), True)
        self.assertEqual((output / f"ROUTE_{source_id}.md").exists(), True)
        self.assertEqual((output / "INDEX.md").exists(), True)
        self.assertNotEqual(copy_path.stat().st_ino, (self.root / relative_path).stat().st_ino)
        self.assertFalse(copy_path.is_symlink())
        self.assertEqual(copy_path.stat().st_nlink, 1)
        self.assertEqual(sorted(p.name for p in output.iterdir()), ["INDEX.md", f"REF_{source_id}.json", f"ROUTE_{source_id}.md", f"{source_id}.txt"])

    def test_hash_collision_is_rejected(self) -> None:
        first_id, first_path, first_text = self._source("first.txt", "النص الأول كامل.")
        _, second_path, second_text = self._source("second.txt", "النص الثاني مختلف.")
        first = self._entry(first_id, first_path, first_text)
        second = self._entry(first_id, second_path, second_text)
        result = wiki_workflow.validate_batch(self.root, self._manifest([first, second]))
        self.assertFalse(result["ok"])
        self.assertIn("HASH_COLLISION", self._codes(result))

    def test_coverage_gap_is_rejected(self) -> None:
        source_id, relative_path, text = self._source(text="0123456789")
        entry = self._entry(source_id, relative_path, text, ranges=[[0, 4], [5, 10]])
        result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
        self.assertFalse(result["ok"])
        self.assertIn("COVERAGE_GAP", self._codes(result))

    def test_evidence_mismatch_is_rejected(self) -> None:
        source_id, relative_path, text = self._source(text="الاقتباس الصحيح")
        entry = self._entry(source_id, relative_path, text, quote="غير مطابق")
        result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
        self.assertFalse(result["ok"])
        self.assertIn("EVIDENCE_MISMATCH", self._codes(result))

    def test_pending_extraction_is_rejected_but_route_is_not(self) -> None:
        source_id, relative_path, text = self._source()
        entry = self._entry(
            source_id,
            relative_path,
            text,
            domain="outreach",
            subdomain="cold_email",
        )
        route_manifest = self._manifest([entry])
        route_result = wiki_workflow.validate_batch(self.root, route_manifest)
        self.assertTrue(route_result["ok"])
        extraction_manifest = self._manifest([entry], operation="extraction")
        extraction_result = wiki_workflow.validate_batch(self.root, extraction_manifest)
        self.assertFalse(extraction_result["ok"])
        self.assertIn("PENDING_EXTRACTION", self._codes(extraction_result))

    def test_subset_does_not_pass_t(self) -> None:
        source_id, relative_path, text = self._source()
        entry = self._entry(source_id, relative_path, text)
        manifest = self._manifest([entry], requested_gates=["T"])
        result = wiki_workflow.validate_batch(self.root, manifest)
        self.assertFalse(result["ok"])
        self.assertIn("T_REQUIRES_FULL_DOMAIN_SNAPSHOT", self._codes(result))

    def test_subset_does_not_start_master(self) -> None:
        source_id, relative_path, text = self._source()
        entry = self._entry(source_id, relative_path, text)
        manifest = self._manifest([entry], requested_outputs=["master"])
        result = wiki_workflow.validate_batch(self.root, manifest)
        self.assertFalse(result["ok"])
        self.assertIn("MASTER_REQUIRES_FULL_DOMAIN_SNAPSHOT", self._codes(result))

    def test_cli_read_only_commands_do_not_change_tree_or_bytes(self) -> None:
        manifest = self._manifest([self._entry(*self._source())])
        before = self._snapshot()
        for arguments in (["inventory"], ["status"], ["validate-batch", "--manifest", str(manifest)], ["publish", "--manifest", str(manifest)]):
            with self.subTest(command=arguments[0]):
                process = subprocess.run([sys.executable, "-B", str(TOOLS / "wiki_workflow.py"), "--vault", str(self.root), *arguments], capture_output=True, text=True)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(json.loads(process.stdout)["writes_performed"], 0)
                self.assertEqual(self._snapshot(), before)

    def test_unicode_coverage_rejects_wrong_units_bounds_lengths_and_overlaps(self) -> None:
        source = self._source(text="أ😀e\u0301\r\nZ")
        cases = [
            ({"unit": "byte"}, None, "COVERAGE_COORDINATES_INVALID"),
            ({"unit": "utf16"}, None, "COVERAGE_COORDINATES_INVALID"),
            ({"bounds": "inclusive"}, None, "COVERAGE_COORDINATES_INVALID"),
            ({"start": 1}, None, "COVERAGE_COORDINATES_INVALID"),
            ({"length": len(source[2].encode("utf-8"))}, None, "COVERAGE_LENGTH_MISMATCH"),
            ({}, [[0, 4], [3, len(source[2])]], "COVERAGE_OVERLAP"),
            ({}, [[0, 0], [0, len(source[2])]], "COVERAGE_RANGE_EMPTY"),
        ]
        for view, ranges, code in cases:
            with self.subTest(view=view, ranges=ranges):
                entry = self._entry(*source, ranges=ranges)
                entry["coverage"]["view"].update(view)
                result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
                self.assertIn(code, self._codes(result))

    def test_semantic_review_status_cannot_be_omitted(self) -> None:
        entry = self._entry(*self._source())
        entry["coverage"].pop("semantic_review_status")
        result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
        self.assertIn("COVERAGE_NOT_REVIEWED", self._codes(result))

    def test_each_segment_requires_review_metadata(self) -> None:
        source = self._source()
        for field in ("reader", "reviewer", "read_at", "reviewed_at", "note"):
            with self.subTest(field=field):
                entry = self._entry(*source)
                entry["coverage"]["semantic_segments"][0].pop(field)
                result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
                self.assertIn("COVERAGE_REVIEW_METADATA_INVALID", self._codes(result))

    def test_segment_review_times_must_be_valid_and_ordered(self) -> None:
        source = self._source()
        for value in ("not-a-date", "2026-10-11", "2026-10-09T01:00:00Z"):
            with self.subTest(value=value):
                entry = self._entry(*source)
                entry["coverage"]["semantic_segments"][0]["reviewed_at"] = value
                result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
                self.assertIn("COVERAGE_REVIEW_METADATA_INVALID", self._codes(result))

    def test_empty_evidence_is_not_a_quote(self) -> None:
        entry = self._entry(*self._source(), quote="")
        result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
        self.assertIn("EVIDENCE_OFFSET_INVALID", self._codes(result))

    def test_evidence_coordinates_and_hash_are_checked(self) -> None:
        source = self._source(text="أ😀e\u0301")
        for field, value, code in (("unit", "utf16", "EVIDENCE_COORDINATES_INVALID"), ("bounds", "inclusive", "EVIDENCE_COORDINATES_INVALID"), ("quote_hash", "sha256:" + "0" * 64, "EVIDENCE_HASH_MISMATCH")):
            with self.subTest(field=field):
                entry = self._entry(*source)
                evidence = entry["evidence"][0]
                (evidence if field == "quote_hash" else evidence["quote_offset"])[field] = value
                result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
                self.assertIn(code, self._codes(result))

    def test_existing_ledger_evidence_field_names_are_supported(self) -> None:
        entry = self._entry(*self._source(text="أ😀e\u0301\r\n"))
        evidence = entry["evidence"][0]
        entry["evidence"] = [{"evidence_start": 0, "evidence_end": len(evidence["quote"]), "evidence_quote": evidence["quote"], "excerpt_sha256": evidence["quote_hash"]}]
        result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
        self.assertTrue(result["ok"], result["errors"])

    def test_path_and_hash_failures_are_rejected_without_writes(self) -> None:
        source = self._source()
        for field, value, code in (("path", "../outside.txt", "PATH_INVALID"), ("path", str(self.root / source[1]), "PATH_INVALID"), ("path", "new/./source.txt", "PATH_INVALID"), ("path", "new//source.txt", "PATH_INVALID"), ("path", "new/missing.txt", "SOURCE_READ_ERROR"), ("content_hash", "sha256:" + "0" * 64, "HASH_MISMATCH"), ("source_id", "../escape", "SOURCE_ID_INVALID")):
            with self.subTest(field=field, value=value):
                entry = self._entry(*source)
                entry[field] = value
                manifest = self._manifest([entry])
                before = self._snapshot()
                result = wiki_workflow.validate_batch(self.root, manifest)
                self.assertIn(code, self._codes(result))
                self.assertEqual(before, self._snapshot())

    def test_multiple_primary_routes_for_same_source_are_rejected(self) -> None:
        source = self._source()
        entries = [self._entry(*source), self._entry(*source, domain="outreach", subdomain="cold_email")]
        result = wiki_workflow.validate_batch(self.root, self._manifest(entries))
        self.assertFalse(result["ok"])

    def test_pending_extraction_cannot_hide_in_coverage_mode(self) -> None:
        entry = self._entry(*self._source(), domain="outreach", subdomain="cold_email")
        entry["coverage"]["mode"] = "extraction"
        result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
        self.assertIn("PENDING_EXTRACTION", self._codes(result))

    def test_entry_level_gate_requests_cannot_bypass_partial_batch_guard(self) -> None:
        entry = self._entry(*self._source())
        entry["requested_gates"] = ["T", "M"]
        result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
        self.assertTrue({"T_REQUIRES_FULL_DOMAIN_SNAPSHOT", "MASTER_REQUIRES_FULL_DOMAIN_SNAPSHOT"} <= self._codes(result))

    def test_apply_rejects_self_review_or_missing_author(self) -> None:
        entry = self._entry(*self._source())
        for author, reviewer in ((None, "qa-test"), ("qa-test", "qa-test"), (" qa-test ", "qa-test")):
            with self.subTest(author=author, reviewer=reviewer):
                manifest = self._manifest([entry], author=author)
                review = self._review(manifest, reviewer=reviewer)
                before = self._snapshot()
                result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
                self.assertFalse(result["ok"])
                self.assertEqual(before, self._snapshot())

    def test_apply_rejects_stale_or_incomplete_reviewer_reports(self) -> None:
        manifest = self._manifest([self._entry(*self._source())])
        for extra in ({"independent": False}, {"decision": "blocked"}, {"validation_ok": False}, {"reviewer": " "}, {"manifest_sha256": "sha256:" + "0" * 64}, {"reviewed_at": None}):
            with self.subTest(extra=extra):
                review = self._review(manifest, **extra)
                before = self._snapshot()
                result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
                self.assertFalse(result["ok"])
                self.assertEqual(before, self._snapshot())

    def test_publish_rerun_reuses_verified_artifacts_without_writing(self) -> None:
        manifest, review, output = self._publish_fixture()
        self.assertEqual((output / "SRC_source.txt").read_bytes(), (self.root / "new/source.txt").read_bytes())
        before = self._snapshot()
        result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
        self.assertTrue(result["ok"], result["errors"])
        self.assertTrue(result["already_published"])
        self.assertEqual(result["writes_performed"], 0)
        self.assertEqual(before, self._snapshot())

    def test_rerun_rejects_changed_manifest_and_structured_ref_tampering(self) -> None:
        manifest, review, output = self._publish_fixture()
        ref_path = output / "REF_SRC_source.json"
        original = ref_path.read_bytes()
        original_record = json.loads(original)
        for value in ([], {**original_record, "evidence": []}, {**original_record, "copy_independence_check": {}}, {**original_record, "snapshot_id": "another-snapshot"}):
            with self.subTest(value=value):
                ref_path.write_text(json.dumps(value), encoding="utf-8")
                before = self._snapshot()
                result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
                self.assertFalse(result["ok"])
                self.assertEqual(before, self._snapshot())
        ref_path.write_bytes(original)
        changed = json.loads(manifest.read_bytes())
        changed["snapshot_id"] = "another-snapshot"
        manifest.write_text(json.dumps(changed), encoding="utf-8")
        review = self._review(manifest)
        before = self._snapshot()
        result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
        self.assertFalse(result["ok"])
        self.assertEqual(before, self._snapshot())

    def test_link_metadata_guards_reject_without_link_creation(self) -> None:
        """Exercise link rejection from lstat metadata without filesystem links.

        Some mounts reject both ``symlink`` and ``link`` creation.  This test is
        deliberately independent of those capabilities: it supplies the same
        metadata that a real link would expose and proves that the workflow
        refuses it without changing the fixture tree.  The capability-aware
        tests below remain the evidence for real link objects when the mount
        permits creating them.
        """
        from types import SimpleNamespace

        manifest, review, output = self._publish_fixture()
        real_lstat = wiki_workflow._lstat
        targets = [self.root / "new/source.txt", manifest, review, output.parent, output / "SRC_source.txt", output / "REF_SRC_source.json", output / "ROUTE_SRC_source.md", output / "INDEX.md"]
        for target in targets:
            for kind in ("symlink", "hardlink") if target.parent == output else ("symlink",):
                with self.subTest(path=target.name, kind=kind):
                    def unsafe_lstat(path):
                        info = real_lstat(path)
                        if path == target:
                            return SimpleNamespace(st_mode=stat.S_IFLNK if kind == "symlink" else info.st_mode, st_nlink=2)
                        return info

                    before = self._snapshot()
                    with patch.object(wiki_workflow, "_lstat", side_effect=unsafe_lstat):
                        result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
                    self.assertFalse(result["ok"])
                    self.assertEqual(before, self._snapshot())

    def test_publish_dry_run_after_apply_rechecks_without_writing(self) -> None:
        manifest, _, _ = self._publish_fixture()
        before = self._snapshot()
        result = wiki_workflow.publish(self.root, manifest)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["writes_performed"], 0)
        self.assertEqual(before, self._snapshot())

    def test_rerun_rejects_tampered_copy_and_metadata_without_overwrite(self) -> None:
        manifest, review, output = self._publish_fixture()
        for name in ("SRC_source.txt", "REF_SRC_source.json", "ROUTE_SRC_source.md", "INDEX.md"):
            with self.subTest(name=name):
                path = output / name
                original = path.read_bytes()
                path.write_bytes(original + b"tampered")
                before = self._snapshot()
                result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
                self.assertFalse(result["ok"])
                self.assertEqual(before, self._snapshot())
                path.write_bytes(original)

    def test_source_manifest_and_destination_symlinks_are_rejected_when_supported(self) -> None:
        source = self._source()
        try:
            (self.root / "new/link.txt").symlink_to(self.root / source[1])
        except OSError as exc:
            self.skipTest(
                "SKIP: symlink creation is unsupported by this filesystem "
                f"({type(exc).__name__}: {exc}); "
                "test_link_metadata_guards_reject_without_link_creation is the metadata fallback"
            )
        entry = self._entry(*source)
        entry["path"] = "new/link.txt"
        result = wiki_workflow.validate_batch(self.root, self._manifest([entry]))
        self.assertIn("SOURCE_READ_ERROR", self._codes(result))
        manifest = self._manifest([self._entry(*source)])
        link = self.root / "staging/link.json"
        link.symlink_to(manifest)
        self.assertFalse(wiki_workflow.validate_batch(self.root, link)["ok"])
        (self.root / "done").symlink_to(self.root / "new", target_is_directory=True)
        review = self._review(manifest)
        before = self._snapshot()
        self.assertFalse(wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)["ok"])
        self.assertEqual(before, self._snapshot())

    def test_rerun_rejects_hardlinked_artifacts_when_supported(self) -> None:
        manifest, review, output = self._publish_fixture()
        try:
            os.link(output / "SRC_source.txt", self.root / "copy-alias.txt")
        except OSError as exc:
            self.skipTest(
                "SKIP: hardlink creation is unsupported by this filesystem "
                f"({type(exc).__name__}: {exc}); "
                "test_link_metadata_guards_reject_without_link_creation is the metadata fallback"
            )
        before = self._snapshot()
        self.assertFalse(wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)["ok"])
        self.assertEqual(before, self._snapshot())

    def test_preflight_rejects_blocked_parent_before_any_writes(self) -> None:
        manifest = self._manifest([self._entry(*self._source())])
        review = self._review(manifest)
        (self.root / "done").write_bytes(b"not a directory")
        before = self._snapshot()
        result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
        self.assertFalse(result["ok"])
        self.assertEqual(before, self._snapshot())

    def test_entire_batch_preflight_precedes_first_write(self) -> None:
        entries = [self._entry(*self._source("a.txt", "first"), domain="outreach", subdomain="cold_email"), self._entry(*self._source("b.txt", "second"))]
        manifest = self._manifest(entries)
        review = self._review(manifest)
        (self.root / "done/sales/objection_handling").mkdir(parents=True)
        before = self._snapshot()
        result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
        self.assertFalse(result["ok"])
        self.assertEqual(before, self._snapshot())

    def test_first_write_failure_reports_partial_artifacts(self) -> None:
        manifest = self._manifest([self._entry(*self._source())])
        review = self._review(manifest)
        with patch.object(wiki_workflow.os, "fsync", side_effect=OSError("synthetic disk error")):
            result = wiki_workflow.publish(self.root, manifest, apply=True, reviewer_report_path=review)
        self.assertFalse(result["ok"])
        self.assertTrue(result["partial_write"])
        self.assertTrue((self.root / "done/sales/objection_handling/SRC_source.txt").exists())


if __name__ == "__main__":
    unittest.main()
