#!/usr/bin/env python3
"""Measure the wiki's actual state for the user's explanatory page."""
import json
import hashlib
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from wiki_quality import records

ROOT = Path('/sdcard/NEXUS_LLM_WIKI')


def main():
    groups = {kind: records(ROOT, kind) for kind in ('sources', 'claims', 'concepts', 'masters')}
    sources = {d['source_id']: d for _, d, _ in groups['sources'] if 'source_id' in d}
    claims = {d['claim_id']: d for _, d, _ in groups['claims'] if 'claim_id' in d}
    raw = sorted(p for p in (ROOT / 'raw/new').rglob('*') if p.is_file())
    raw_paths = {p.relative_to(ROOT).as_posix() for p in raw}
    paths_with_claim = set()
    paths_with_review = set()
    paths_in_concept = set()
    referenced_claims = set()
    for d in claims.values():
        sp = sources.get(d.get('source_id'), {}).get('source_path')
        if sp in raw_paths:
            paths_with_claim.add(sp)
            if d.get('status') in ('reviewed', 'accepted'):
                paths_with_review.add(sp)
    cards = []
    for path, d, text in groups['concepts']:
        refs = d.get('claim_refs', [])
        referenced_claims.update(refs)
        for ref in refs:
            sp = sources.get(claims.get(ref, {}).get('source_id'), {}).get('source_path')
            if sp in raw_paths:
                paths_in_concept.add(sp)
        body = text.split('---', 2)[-1]
        title = d.get('title', path.stem)
        group = 'المحتوى والبراند' if 'CONTENT_' in path.stem else 'البريد والتشغيل' if 'OUTBOUND_' in path.stem else 'المبيعات والعروض' if 'SALES_' in path.stem else 'مسودات أولية'
        cards.append({'id': d.get('concept_id'), 'title': title, 'status': d.get('status'), 'group': group,
                      'claimCount': len(refs), 'sourceCount': len(set(d.get('source_refs', []))),
                      'words': len(body.split()), 'lines': len(text.splitlines()),
                      'path': 'NEXUS_LLM_WIKI/' + path.relative_to(ROOT).as_posix()})
    relocation = []
    by_hash = {}
    for p in raw:
        by_hash.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(), []).append(p.relative_to(ROOT).as_posix())
    for sid, d in sources.items():
        sp = d.get('source_path', '')
        if sp and not (ROOT / sp).is_file():
            matches = by_hash.get(str(d.get('content_hash', '')).removeprefix('sha256:'), [])
            relocation.append({'source_id': sid, 'old_path': sp, 'matching_new_paths': matches})
    snapshot = {
        'measuredAt': datetime.now(timezone.utc).isoformat(),
        'rawNewFiles': len(raw), 'rawNewBytes': sum(p.stat().st_size for p in raw), 'uniqueHashes': len(by_hash),
        'duplicateFiles': len(raw) - len(by_hash),
        'counts': {k: {'files': len(v), 'statuses': dict(Counter(d.get('status', 'unknown') for _, d, _ in v))} for k, v in groups.items()},
        'sourcesWithAnyClaim': len(paths_with_claim), 'sourcesWithReviewedClaim': len(paths_with_review),
        'sourcesLinkedToConcept': len(paths_in_concept), 'sourcesWithoutClaim': len(raw_paths - paths_with_claim),
        'claimRefsInConcepts': len(referenced_claims),
        'firstFixedSnippetClaims': sum(d.get('evidence_start') == 0 and d.get('evidence_end') in (400, 430) for d in claims.values()),
        'conceptWordsMedian': statistics.median(c['words'] for c in cards) if cards else 0,
        'conceptWordsMin': min((c['words'] for c in cards), default=0), 'conceptWordsMax': max((c['words'] for c in cards), default=0),
        'completeSourceSemanticPassesProven': 0,
        'completionNote': 'لا يوجد سجل يثبت استخراج جميع الأفكار من أي مصدر ثم اعتماد اكتماله؛ وجود Claim أو حالة processed لا يثبت ذلك.',
        'relocationMatches': relocation, 'concepts': cards,
    }
    (ROOT / 'reports/EXPLAIN_SNAPSHOT_2026-10-07.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in snapshot.items() if k != 'concepts'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
