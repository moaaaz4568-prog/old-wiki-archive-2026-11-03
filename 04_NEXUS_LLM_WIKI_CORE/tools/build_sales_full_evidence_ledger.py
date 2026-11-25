#!/usr/bin/env python3
"""Read every high-priority sales candidate and write a compact evidence ledger.

Ledger rows are candidate evidence, not accepted Claims. Exact offsets and hashes
allow a later semantic reviewer (including Muse) to promote or reject them.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

VAULT=Path('/sdcard/NEXUS_LLM_WIKI')
CLASS=VAULT/'collections/sales/source_classification.json'
OUT=VAULT/'collections/sales/full_evidence_ledger.jsonl'
TRIGGER=re.compile(r'sales|sell|selling|close|closing|lead|prospect|outreach|cold email|discovery|objection|pricing|price|offer|funnel|pipeline|revenue|client|customer|مبيعات|بيع|عميل|إيميل|اعتراض|إغلاق|قمع المبيعات|السعر|تسعير|عرض',re.I)
RESULT=re.compile(r'\b\d+(?:[.,]\d+)?\s*%?|\$\s*\d+|EGP|MRR|revenue|result|clients? in|باع|عملاء',re.I)

def windows(text):
    # Transcript files are frequently one line; split on punctuation while preserving offsets.
    for m in re.finditer(r'[^.!?؟\n]{30,900}(?:[.!?؟]|\n|$)',text):
        raw=m.group(0); quote=raw.strip(); start=m.start()+len(raw)-len(raw.lstrip()); end=start+len(quote)
        if TRIGGER.search(quote): yield start,end,quote

def main():
    data=json.loads(CLASS.read_text(encoding='utf8'))
    total=0; sources=0; types={}
    with OUT.open('w',encoding='utf8') as f:
        for item in data['items']:
            if item.get('tier') not in {'confirmed_sales','sales_adjacent'}: continue
            p=VAULT/item['source_path']
            if not p.is_file(): continue
            text=p.read_text(encoding='utf8',errors='replace'); found=list(windows(text))[:8]
            if found: sources+=1
            for rank,(start,end,quote) in enumerate(found,1):
                et='reported_result' if RESULT.search(quote) else 'candidate_statement'
                row={'ledger_id':f"LEDGER_SALES_{item['source_id']}_{rank:02d}",'source_id':item['source_id'],'source_path':item['source_path'],'source_sha256':item['content_sha256'],'rank_in_source':rank,'evidence_start':start,'evidence_end':end,'evidence_quote':quote,'excerpt_sha256':hashlib.sha256(quote.encode('utf8')).hexdigest(),'candidate_evidence_type':et,'semantic_status':'needs_review','what_it_does_not_prove':'This candidate is not a general rule, benchmark, causal claim, or promise.'}
                f.write(json.dumps(row,ensure_ascii=False)+'\n'); total+=1; types[et]=types.get(et,0)+1
    (OUT.with_suffix('.README.md')).write_text('# سجل الأدلة الكامل للمبيعات\n\nمرّت الأداة على كل مصدر في طبقة الأولوية العالية/المجاورة، واستخرجت نوافذ نصية قابلة لإعادة الفحص. هذه ليست Claims مقبولة؛ كل سطر يحتاج مراجعة دلالية وتحديد statement والنطاق.\n\n'+f'- المصادر التي ظهر فيها دليل مرشح: **{sources}**\n- عدد النوافذ: **{total}**\n- الأنواع الآلية: `{types}`\n',encoding='utf8')
    print(json.dumps({'sources_with_evidence':sources,'ledger_rows':total,'types':types},ensure_ascii=False))
if __name__=='__main__': main()
