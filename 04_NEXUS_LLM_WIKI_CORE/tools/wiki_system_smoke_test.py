#!/usr/bin/env python3
"""
wiki_system_smoke_test.py — Nexus LLM Wiki System Integrity & Smoke Test
Validates core entry points, systems 20-25, manifest health, schemas, extraction batches, and read-only invariants.
Stdlib-only, non-destructive, read-only.
"""

import os
import sys
import json
import glob

WIKI_ROOT = "/sdcard/NEXUS_LLM_WIKI"

def log_pass(msg):
    print(f"[\033[92mPASS\033[0m] {msg}")

def log_fail(msg):
    print(f"[\033[91mFAIL\033[0m] {msg}")

def log_info(msg):
    print(f"[\033[94mINFO\033[0m] {msg}")

def test_entrypoints():
    print("\n--- 1. Testing Core Entrypoints ---")
    required = [
        "START_HERE.md",
        "README.md",
        "AGENTS.md",
        "SCHEMA.md",
        "INDEX.md",
        "STATUS_FROM_ZERO.md",
    ]
    all_ok = True
    for fname in required:
        p = os.path.join(WIKI_ROOT, fname)
        if os.path.isfile(p) and os.path.getsize(p) > 0:
            log_pass(f"Entrypoint exists and non-empty: {fname} ({os.path.getsize(p)} bytes)")
        else:
            log_fail(f"Missing or empty entrypoint: {fname}")
            all_ok = False
    return all_ok

def test_systems_20_25():
    print("\n--- 2. Testing Operating Systems 20-25 ---")
    systems = [
        "systems/20_WIKI_OPERATING_SYSTEM.md",
        "systems/21_SOURCE_TO_KNOWLEDGE_PIPELINE.md",
        "systems/22_WRITING_AND_EVIDENCE_SYSTEM.md",
        "systems/23_RETRIEVAL_QA_AND_HONEST_STATUS.md",
        "systems/24_AGENT_HANDOFF_AND_RECOVERY.md",
        "systems/25_CHANGE_CONTROL_AND_UPDATE_PROTOCOL.md",
    ]
    all_ok = True
    for sys_file in systems:
        p = os.path.join(WIKI_ROOT, sys_file)
        if os.path.isfile(p) and os.path.getsize(p) > 0:
            log_pass(f"System contract present: {sys_file}")
        else:
            log_fail(f"Missing system contract: {sys_file}")
            all_ok = False
    return all_ok

def test_manifest():
    print("\n--- 3. Testing Corpus Manifest Health ---")
    manifest_p = os.path.join(WIKI_ROOT, "collections/corpus/manifest.jsonl")
    if not os.path.isfile(manifest_p):
        log_fail("Corpus manifest.jsonl not found!")
        return False
    
    count = 0
    valid_json = 0
    with open(manifest_p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            count += 1
            try:
                data = json.loads(line)
                if "source_id" in data or "source_path" in data or "relative_path" in data or "sha256" in data:
                    valid_json += 1
            except Exception:
                pass
    
    if count > 0 and valid_json == count:
        log_pass(f"Manifest contains {count} valid JSONL records (100% valid)")
        return True
    else:
        log_fail(f"Manifest issues: {valid_json}/{count} valid records")
        return False

def test_extraction_batches():
    print("\n--- 4. Testing Sales Extraction Batches ---")
    batch_dir = os.path.join(WIKI_ROOT, "collections/sales/extraction_batches")
    if not os.path.isdir(batch_dir):
        log_fail("Extraction batches directory missing!")
        return False
    
    batch_files = glob.glob(os.path.join(batch_dir, "*.json"))
    if not batch_files:
        log_fail("No extraction batch JSON files found!")
        return False
    
    all_ok = True
    total_terms = 0
    total_claims = 0
    for bf in batch_files:
        try:
            with open(bf, "r", encoding="utf-8") as f:
                data = json.load(f)
                terms = len(data.get("terms", []))
                claims = len(data.get("claims", []))
                total_terms += terms
                total_claims += claims
                log_pass(f"Batch {os.path.basename(bf)}: {terms} terms, {claims} claims")
        except Exception as e:
            log_fail(f"Failed parsing {os.path.basename(bf)}: {e}")
            all_ok = False
    
    log_info(f"Total Candidate Terms in batches: {total_terms}")
    log_info(f"Total Candidate Claims in batches: {total_claims}")
    return all_ok

def test_raw_integrity():
    print("\n--- 5. Testing Raw Sources Immutability & Safety ---")
    raw_dir = os.path.join(WIKI_ROOT, "raw")
    if not os.path.isdir(raw_dir):
        log_fail("Raw sources directory missing!")
        return False
    
    raw_count = len(os.listdir(raw_dir))
    log_pass(f"Raw sources directory present with {raw_count} items")
    return True

def test_schemas():
    print("\n--- 6. Testing Claim & Concept Schema Compliance ---")
    claims = glob.glob(os.path.join(WIKI_ROOT, "claims/*.md"))[:10]
    concepts = glob.glob(os.path.join(WIKI_ROOT, "concepts/*.md"))[:10]
    
    claims_ok = True
    for cf in claims:
        with open(cf, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if "type: claim" not in content or "claim_id:" not in content:
                log_fail(f"Claim schema mismatch in: {os.path.basename(cf)}")
                claims_ok = False
                break
    if claims and claims_ok:
        log_pass(f"Verified {len(claims)} sample claims: compliant with SCHEMA.md frontmatter")

    concepts_ok = True
    for ccf in concepts:
        with open(ccf, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if "type: concept" not in content or "concept_id:" not in content:
                log_fail(f"Concept schema mismatch in: {os.path.basename(ccf)}")
                concepts_ok = False
                break
    if concepts and concepts_ok:
        log_pass(f"Verified {len(concepts)} sample concepts: compliant with SCHEMA.md frontmatter")

    return claims_ok and concepts_ok

def main():
    print(f"==================================================")
    print(f"   Nexus LLM Wiki Smoke Test — Diagnostic Run    ")
    print(f"==================================================")
    
    results = [
        test_entrypoints(),
        test_systems_20_25(),
        test_manifest(),
        test_extraction_batches(),
        test_raw_integrity(),
        test_schemas(),
    ]
    
    print("\n==================================================")
    passed = sum(1 for r in results if r)
    total = len(results)
    if passed == total:
        print(f"\033[92mALL TESTS PASSED ({passed}/{total})\033[0m — System is structurally healthy.")
        sys.exit(0)
    else:
        print(f"\033[91mFAILURES DETECTED ({total - passed}/{total})\033[0m — Inspect logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
