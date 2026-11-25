#!/usr/bin/env python3
"""Classify every source record into a sales collection tier without mutating raw."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

VAULT = Path('/sdcard/NEXUS_LLM_WIKI')
OUT = VAULT / 'collections/sales'
HIGH = ('sales', 'selling', 'cold email', 'cold-email', 'outreach', 'closing', 'discovery', 'objection', 'pipeline', 'lead generation', 'sales call', 'مبيعات', 'بيع', 'إغلاق', 'اوتريتش', 'اعتراض', 'قمع المبيعات')
MEDIUM = ('client', 'customer', 'prospect', 'pricing', 'price', 'offer', 'revenue', 'funnel', 'follow-up', 'qualification', 'عميل', 'عملاء', 'تسعير', 'السعر', 'عرض', 'متابعة')
SALES_THEMES = ('sales', 'outreach', 'offers_pricing', 'agency_operations', 'lead_generation', 'closing')

def meta(path: Path) -> dict:
    result = {}
    text = path.read_text(encoding='utf-8', errors='replace')
    for line in text.splitlines()[1:]:
        if line.strip() == '---': break
        m = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
        if m: result[m.group(1)] = m.group(2).strip().strip('"\'')
    themes = re.search(r'themes:\s*\[(.*?)\]', text, re.S)
    result['themes'] = re.findall(r'"([^"]+)"|\'([^\']+)\'', themes.group(1)) if themes else []
    result['themes'] = [a or b for a,b in result['themes']]
    return result

def main():
    rows=[]; counts=Counter(); missing=[]; hash_mismatch=[]
    for record_path in sorted((VAULT/'sources').glob('*.md')):
        try: m=meta(record_path)
        except OSError: continue
        rel=m.get('source_path',''); raw=VAULT/rel
        row={'source_id':m.get('source_id',record_path.stem),'title':m.get('title',''),'source_path':rel,'source_record':str(record_path.relative_to(VAULT)),'status':m.get('status'),'themes':m.get('themes',[])}
        if not raw.is_file():
            row.update({'tier':'missing_source','reason':'source_path does not exist'}); missing.append(row); counts[row['tier']]+=1; rows.append(row); continue
        try: text=raw.read_text(encoding='utf-8',errors='replace')
        except OSError as e:
            row.update({'tier':'unreadable','reason':str(e)}); counts[row['tier']]+=1; rows.append(row); continue
        low=(raw.name+'\n'+text[:200000]).lower()
        theme_hits=[x for x in row['themes'] if x in SALES_THEMES]
        high_hits=sorted({x for x in HIGH if x in low})
        medium_hits=sorted({x for x in MEDIUM if x in low})
        expected=m.get('content_hash','').removeprefix('sha256:')
        actual=hashlib.sha256(raw.read_bytes()).hexdigest()
        if expected and expected != actual: hash_mismatch.append(row['source_id'])
        if theme_hits or len(high_hits)>=2 or any(x in raw.name.lower() for x in HIGH):
            tier='confirmed_sales'
        elif high_hits or len(medium_hits)>=3:
            tier='sales_adjacent'
        else:
            tier='not_sales_candidate'
        row.update({'tier':tier,'theme_hits':theme_hits,'high_signal_hits':high_hits,'medium_signal_hits':medium_hits,'bytes':raw.stat().st_size,'content_sha256':actual})
        counts[tier]+=1; rows.append(row)
    rows.sort(key=lambda x:(x['tier'],x['source_path']))
    now=datetime.now(timezone.utc).isoformat()
    out={'generated_at':now,'policy':'all source records audited; raw immutable; tiers are triage, not semantic acceptance','counts':dict(counts),'hash_mismatch_source_ids':hash_mismatch,'items':rows}
    (OUT/'source_classification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'FULL_COLLECTION_STATUS.md').write_text(
        '# حالة مجموعة مصادر المبيعات الكاملة\n\n'
        f'وقت الفحص: `{now}`\n\n'
        'هذا الفحص مرّ على كل سجلات `sources/` وربطها بالمسار الخام. لا ينقل ولا يحذف raw. التصنيف الآلي يحدد أولوية القراءة ولا يحول المصدر إلى معرفة مقبولة.\n\n'
        + '\n'.join(f'- **{k}: {v}**' for k,v in counts.items()) + '\n\n'
        + f'- سجلات بمسار مفقود: **{len(missing)}**\n- بصمات لا تطابق سجل Source: **{len(hash_mismatch)}**\n\n'
        '## معنى الطبقات\n\n'
        '- `confirmed_sales`: إشارات themes/اسم/محتوى قوية؛ يدخل القراءة الدلالية أولًا.\n'
        '- `sales_adjacent`: قد يفيد المبيعات لكنه يحتاج قراءة سياقية.\n'
        '- `not_sales_candidate`: لا يُقرأ كبيع في الدفعة الأولى، ويظل محفوظًا ويمكن إعادة تصنيفه.\n'
        '- `missing_source`/`unreadable`: مشكلة provenance لا تُخفى.\n',encoding='utf-8')
    print(json.dumps({'counts':dict(counts),'hash_mismatch':len(hash_mismatch),'missing':len(missing)},ensure_ascii=False))

if __name__=='__main__': main()
