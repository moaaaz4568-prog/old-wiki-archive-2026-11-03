#!/usr/bin/env python3
"""Create a small, manually selected reviewed seed from exact raw quotes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

VAULT = Path('/sdcard/NEXUS_LLM_WIKI')
RAW = VAULT / 'raw/new'
OUT = VAULT / 'claims'

SEEDS = [
    ('CLM_SALES_SEED_001', 'sabonagy__How to Make +$100,000Mo with Cold Email, Calls, DMs & SMS (4 Hour SMMA Masterclass)__iHJLlKlKDhk.txt', "outbound strategies include cold calling, cold email, cold LinkedIn, direct messages on Instagram, Twitter, Facebook. So we have separated all of this and it will be inside this video later on. So just be patient. So we're going to cover cold email, social media outreach, cold calling, as well as messaging.", 'direct_quote', 'The speaker groups several outbound channels and says the lesson will cover them; this does not establish that one channel is universally best.'),
    ('CLM_SALES_SEED_002', 'aaronxshepherd__If you only watch one cold email video, make it this (4 hour masterclass)__LzGJ3MQParY.txt', "I've sent more than 20 million cold emails. I've booked thousands [music] of sales calls and I've helped my clients generate more than 45 mil in pipeline revenue.", 'reported_result', 'The speaker reports personal/client outcomes; the excerpt does not independently verify attribution, denominator, time period, or causality.'),
    ('CLM_SALES_SEED_003', 'jaydenleilua1__The Cold Outreach Blueprint That Prints Leads (1+ hours)__hpp8e7NZsDY.txt', "First, we're going to start off with cold email. Number one is going to be building your infrastructure because honestly, nothing else matters if you can't land in the primary inbox. Number two is going to be list building. How you can actually build a list of people who actually want your stuff. Number three is going to be offer creation because you can have the best infrastructure, you can have the best list, but if your offer sounds like a sales pitch, they're not going to read it.", 'direct_quote', 'This is a source framework for cold outreach; it is not a measured causal comparison of infrastructure, list, and offer.'),
    ('CLM_SALES_SEED_004', 'smartleadai__Crafting Irresistible Offers That Book Meetings with Ryan Redmond  #SmartleadOfficeHours__gsOwXJXI_v4.txt', "offer is king. I think the most important thing is always going to be deliverability and then the second most important thing is offer and then that and then everything else kind of goes from there and on every all the AI all the clay enrichment everything helps support the offer and improves the results of conversions but if the offer you know sucks you know no one's going to buy", 'direct_quote', 'This is an attributed opinion from an interview; its priority ordering is context-dependent and has no stated experiment in the excerpt.'),
    ('CLM_SALES_SEED_005', 'matthewlucero__LIVE Cold Email Training  Smartlead.ai Webinar__KKb12zR5O1w.txt', "the point of the email is to get them on the phone because on the phone that's where you can you know go deeper into Discovery you can actually learn about their you know their exact situation", 'direct_quote', 'The speaker describes a purpose for this email workflow; it does not prove that phone calls outperform other conversion paths.'),
    ('CLM_SALES_SEED_006', 'Build a $100k MRR Agency — 14-Hour Masterclass.txt', "don't propose on the first date. All of the markets are currently flooded with people cold emailing. Do you need my service? I get it all the time on LinkedIn DMs of, how can I help you? We should hop on a call. I think that there's mutually beneficial things that we can do together. I have actually stopped connecting with people who send me a DM anywhere around that cuz it drives me insane. So, we've decided to do the opposite. We rarely do any cold emailing unless it's authentic relationship building", 'direct_quote', 'This is a personal operating preference and rationale; it may fit relationship-led outreach and is not a universal ban on first-contact proposals.'),
]

def yaml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)

def main() -> None:
    created = []
    for claim_id, filename, quote, kind, boundary in SEEDS:
        raw = RAW / filename
        text = raw.read_text(encoding='utf-8', errors='replace')
        start = text.find(quote)
        if start < 0:
            raise SystemExit(f'quote not found: {filename} / {claim_id}')
        end = start + len(quote)
        source = next((p for p in (VAULT / 'sources').glob('*.md') if filename in p.read_text(encoding='utf-8', errors='replace')), None)
        source_id = source.stem if source else f'UNREGISTERED_{hashlib.sha256(raw.read_bytes()).hexdigest()[:12]}'
        out = OUT / f'{claim_id}.md'
        out.write_text(
            '---\n'
            f'type: claim\nclaim_id: {claim_id}\n'
            f'statement: {yaml_str("المصدر يقول أو يقرر: " + quote[:220])}\n'
            f'evidence_type: {kind}\nsource_id: {source_id}\n'
            f'locator: {yaml_str(f"chars {start}:{end} (Unicode, zero-based, end-exclusive)")}\n'
            f'evidence_start: {start}\nevidence_end: {end}\n'
            f'evidence_quote: {yaml_str(quote)}\n'
            f'excerpt_sha256: {hashlib.sha256(quote.encode("utf-8")).hexdigest()}\n'
            'scope: seed sales corpus; attributed source statement, not a universal rule.\n'
            f'what_it_does_not_prove: {yaml_str(boundary)}\n'
            'confidence: source_reported\nstatus: reviewed\nextraction_status: reviewed_seed\n'
            'created: 2026-10-08\nupdated: 2026-10-08\n---\n\n'
            '## ملاحظة المراجع\n\n'
            f'{boundary}\n\n'
            f'المصدر الخام: `raw/new/{filename}`\n', encoding='utf-8')
        created.append({'claim_id': claim_id, 'source_id': source_id, 'raw_path': f'raw/new/{filename}', 'evidence_start': start, 'evidence_end': end, 'evidence_type': kind})
    (VAULT / 'collections/sales/seed_claims.json').write_text(json.dumps({'batch': 'sales-seed-1', 'claims': created}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'created': len(created), 'claims': created}, ensure_ascii=False))

if __name__ == '__main__':
    main()
