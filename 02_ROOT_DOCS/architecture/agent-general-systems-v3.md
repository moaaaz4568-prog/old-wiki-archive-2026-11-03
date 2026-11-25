# تقرير الأنظمة العامة v3 — 2026-10-10

## الهدف والحالة

- الهدف: تصحيح الميثاق ونظام14، وتأليف أنظمة13 و15–19 وتحديث فهرس الأنظمة؛ عقود تشغيل لا بناء مصادر.
- الحالة الحالية: نطاق التأليف والتحقق المستهدف جاهز للتسليم؛ الأنظمة الستة كتبت، والميثاق ونظام14 والفهرس صُححت، والفحوص المحفوظة نجحت. لا إعلان إغلاق لأي مجال.
- مرجع الحسم: [المواءمة](MULTIDOMAIN_ALIGNMENT_2026-10-10.md) و[ملحق رسائل EF22](USER_MESSAGES_SESSION_EF22.md)، لا خطة agent-multidomain-plan القديمة.
- الخطوة التالية خارج هذه المهمة: مراجعة القائد ومالكي التكامل لتطابق التنفيذ الفعلي مع هذه العقود، دون استنتاج جاهزية المصادر من نجاح فحص الوثائق.
- لا عائق يمنع التأليف. توافق الأدوات وconfig وdone والمهارات خارج هذا النطاق؛ لن يُفترض تحققها.

## القراءة وحدود الملكية

- قُرئ الميثاق القديم كاملًا: 233 سطرًا؛ ونظام14 كاملًا: 766 سطرًا.
- قُرئت `AGENTS.md` و`SCHEMA.md` للويكي، والأنظمة00–12 و99 وفهرس الأنظمة كاملًا.
- ملفات `.opencode/todo.md` و`context.md` و`sync-issues.md` قُرئت لاستعادة السياق؛ تتضمن مسائل سابقة خارج المهمة. `status.md` و`verification-checklist.md` غير موجودين. لم تُعدّل حالات المهمة القديمة أو بنود إنجازها.
- لم يُقرأ config أو done أو Skills أو ملفات المعرفة أو تقارير الوكلاء الجارية. هذا التقرير هو سجل التقدم المخصص لهذا النطاق.
- تعارضات مرصودة قبل التعديل: وصف الميثاق بالاعتماد دون سند؛ ربط done بـMasters؛ منع triage للمجالات المنتظرة؛ جعل النسخة المستقلة اختيارية في14؛ الخلط بين EOF والدليل الدلالي.
- لا subagents، لا Codex، لا بناء مصادر، لا تعديل raw، لا حذف أو نقل ملفات.

## الملفات المصرح بها

الجذر `/sdcard/NEXUS_LLM_WIKI/`، ما لم يذكر خلاف ذلك:

1. `MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md`
2. `systems/13_MULTI_DOMAIN_ARCHITECTURE.md`
3. `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md`
4. `systems/15_DOMAIN_COMPLETION_GATES.md`
5. `systems/16_SEQUENTIAL_AGENT_ORCHESTRATION.md`
6. `systems/17_FOLDER_INDEX_CONTRACT.md`
7. `systems/18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md`
8. `systems/19_NEW_SOURCE_REPROCESSING.md`
9. `systems/INDEX.md`
10. `/root/r/reports/sales-proof/agent-general-systems-v3.md`

## التحقق

شُغّل فحص الارتداد المحفوظ أدناه قبل تعديل العقود: `RESULT: 0/18 checks passed`، exit code=1. كشف غياب الأنظمة الستة، وادعاء اعتماد الميثاق، والسياسة الاختيارية للنسخة وغياب الفصل الدلالي وحقول التكامل. هذا فشل وثائق متوقع وليس اختبار pipeline.

التشغيل الأول بعد التعديل: `18/18`، و10 أمثلة JSON صالحة و84 رابطًا محليًا محلولًا. أضيف بعده مثال Claim مرشح وحقول توقيت القراءة، وأزيل غموض routing الدلالي وhandoff المجال المعلق؛ إعادة الفحص النهائي نجحت `26/26`، exit code=0، مع11 مثال JSON و84 رابطًا محليًا.
واجهت محاولة patch مركبة اختلافًا في سطر مرجعي قديم، فرفضتها الأداة دون تطبيقها؛ أُعيدت في patches أصغر ونجحت. لا فشل كتابة قائم بسببها.

### نتيجة التأليف والمراجعة

- أُنشئت ستة أنظمة ضمن حد70–130 سطرًا:13=121،15=110،16=98،17=96،18=91،19=101، مقاسة بالفحص المحفوظ.
- عُدّل الميثاق ونظام14 وفهرس systems، وأُضيف سجل مراجعة2026-10-10 وأزيلت الأحكام القديمة المتعارضة فعليًا، لا مجرد إضافة تنبيه فوقها.
- أصبحت النسخة المستقلة إلزامية مباشرة تحت done/domain/subdomain مع SHA-256 وmetadata، دون source_refs وسيط أو عد نسخ متكررة كأدلة مستقلة.
- ثُبت التصنيف العام مع قفل المعرفة في مجال واحد، وفصل route_done/source_done/subdomain_extraction_done/domain_terms_complete/domain_done.
- source_done يغلق استخراج ومراجعة الوحدات، لا ينتظر Concept/Master. المصدر المختلط يحفظ مساهماته المنتظرة ولا يدعي اكتماله الكلي أو يفتح مجالًا ثانيًا.
- T لا تمنح إلا لكل مصادر وأقسام snapshot الشامل، وتسبق بدء أي Master؛ candidate terms/Claims تُجمع أثناء القراءة، وConcepts تراجع بعد أدلتها.
- أضيفت حقول JSON للـsnapshots والدفعات والقراءة والوحدات والمصطلحات والمرشحين وroute وcatalog والحالة وdelta والفهرسة، مع أمثلة موسومة غير فعلية.
- ثُبتت معاني R/T/C/K/M/QA، وحفظ الخلاف المدعوم، والفصل بين اعتراض السعر كمبيعات وتصميمه كتسعير، وdelta/invalidation دون reopen صامت.
- روجعت الملفات التسعة بعد تعديلها، وأُصلح اتساق content_unit_ids/content_units وحقول التوقيت والمصائر؛ لا مراجعة مستقلة من وكيل آخر، لأن التفويض ممنوع هنا.

### LSP وحدود دليله

- شُغلت `lsp_diagnostics(file=<absolute-path>)` على كل الملفات العشرة في قائمة الملكية أعلاه.
- أعادت كلها: `{"message":"No diagnostics found. All clean!","status":"clean"}`.
- أعيد الفحص للأنظمة13 و14 و15 بعد اللمسات الأخيرة ونجحت كلها. التقرير يعاد فحصه بعد توثيق النتيجة.
- LSP ونجاح JSON وحل الروابط أدلة بنيوية فقط؛ لا تثبت صحة محتوى المصادر أو QA مستقلًا أو تنفيذ القفل.

### القيود المتبقية والتكامل

- لا اختبار فاشل قائم ضمن فحوص الوثائق المستهدفة. الفشل السابق موثق كمرحلة قبل الإصلاح.
- لم يُشغّل `bulk_ingest.py` أو `wiki_quality.py` أو pipeline أو اختبارات استرجاع معرفية؛ لأنها تتجاوز التأليف وفحص روابط الوثائق إلى قراءة/تشغيل طبقات خارج التكليف.
- لم تُقرأ أو تُعدّل أعمال الوكلاء الجارية في config/done/Skills/المعرفة؛ توافق حقول التنفيذ الفعلية مع أمثلة العقود **غير متحقق هنا**.
- الروابط الـ84 روابط ملفات محلية فعلية داخل الوثائق العشر، لا روابط قوالب الأمثلة أو مسارات مخرجات لم تُبنَ؛ لا fragments أو روابط ويب ضمنها.
- الأنظمة القديمة خارج الملكية لم تُعدّل. يوضح INDEX أولوية13–19 في مواضع اختلاف توقيت Master ونطاق sales وسياسة النسخة والعزل؛ على التنفيذ استهلاك العقد الأحدث.
- لا ادعاء بجرد raw أو مقارنة بصماته في هذه الجلسة؛ الدليل على احترام النطاق هو أن جميع عمليات الكتابة كانت `apply_patch` إلى الملفات العشرة فقط، دون أوامر بناء أو حذف أو نقل.
- مسائل `.opencode/sync-issues.md` القديمة بقيت خارج النطاق؛ لم تُغلق TODO أو علامات مهمة أو حالة مجال بالنيابة عن القائد.

### فحص ارتداد العقود المحفوظ

هذا فحص وثائق فقط: وجود العقود والحقول، طول الأنظمة الجديدة، صلاحية أمثلة JSON واتساق حقولها، وحل روابط الملفات المحلية. لا يحاكي تشغيل pipeline ولا يثبت اكتمال المعرفة. يقرأ الملفات العشرة فقط، ويفحص وجود أهداف الروابط دون قراءة محتواها. الفحوص الإضافية لاتساق الأمثلة أضيفت بعد فحص الارتداد الأساسي ذي18 بندًا.

```python
from pathlib import Path
import json
import re

root = Path('/sdcard/NEXUS_LLM_WIKI')
report = Path('/root/r/reports/sales-proof/agent-general-systems-v3.md')
names = {
    13: '13_MULTI_DOMAIN_ARCHITECTURE.md',
    14: '14_SOURCE_ROUTING_AND_DONE_TREE.md',
    15: '15_DOMAIN_COMPLETION_GATES.md',
    16: '16_SEQUENTIAL_AGENT_ORCHESTRATION.md',
    17: '17_FOLDER_INDEX_CONTRACT.md',
    18: '18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md',
    19: '19_NEW_SOURCE_REPROCESSING.md',
}
paths = {'charter': root / 'MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md',
         'index': root / 'systems/INDEX.md', 'report': report}
paths.update({str(n): root / 'systems' / name for n, name in names.items()})
texts = {k: p.read_text() if p.exists() else '' for k, p in paths.items()}
checks = []
def check(label, ok):
    checks.append(bool(ok))
    print(('PASS' if ok else 'FAIL') + ': ' + label)

check('all ten deliverables exist', all(p.is_file() for p in paths.values()))
check('no unsupported charter approval',
      '**الحالة:** ميثاق تشغيل معتمد' not in texts['charter'])
check('charter timing and state contract', all(t in texts['charter'] for t in
      ['domain_terms_complete', 'candidate Claims', 'R/T/C/K/M/QA',
       'config/processing_order.json', 'config/domain_catalog.json']))
check('routing: mandatory copy and separate semantic reading', all(t in texts['14'] for t in
      ['verified_copy_required', 'independent_byte_exact', 'semantic_segments',
       'eof_reached', 'route_done', 'source_done', 'config/domain_catalog.json']))
check('obsolete optional-copy policy absent', all(t not in texts['14'] for t in
      ['وضع المرجع (الافتراضي)', 'إذا كانت النسخة غير مطلوبة، يكفي المرجع الآمن']))
check('snapshot and batch coverage fields', all(t in texts['15'] for t in
      ['candidate_manifest', 'cutoff', 'domain_snapshot', 'batch', 'disposition']))
check('single state owner and lock fencing', all(t in texts['16'] for t in
      ['config/processing_order.json', 'state_revision', 'fencing_token', 'active_domain']))
check('delta invalidation without silent reopen', all(t in texts['19'] for t in
      ['delta_id', 'invalidated_gates', 'stale', 'reopen', 'domain_terms_complete']))
check('systems index links all seven contracts', all('](' + name + ')' in texts['index']
      for name in names.values()))
for n in [13, 15, 16, 17, 18, 19]:
    count = len(texts[str(n)].splitlines())
    check(f'system {n}: 70-130 lines ({count})', 70 <= count <= 130)
check('revision date on all nine wiki documents', all('2026-10-10' in text
      for key, text in texts.items() if key != 'report'))

json_count = 0
json_errors = []
samples = {}
link_count = 0
link_errors = []
for key, text in texts.items():
    for block in re.findall(r'^```json\n(.*?)^```\s*$', text, re.M | re.S):
        json_count += 1
        try:
            samples.setdefault(key, []).append(json.loads(block))
        except ValueError as exc:
            json_errors.append(f'{key}: {exc}')
    prose = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
    for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', prose):
        if re.match(r'^[a-z]+://', target):
            link_errors.append(f'{key}: unchecked external link {target}')
            continue
        link_count += 1
        if '#' in target:
            link_errors.append(f'{key}: anchor needs explicit verification: {target}')
            continue
        resolved = Path(target) if target.startswith('/') else paths[key].parent / target
        if not resolved.is_file():
            link_errors.append(f'{key}: missing {target}')
check(f'JSON samples parse ({json_count})', json_count >= 7 and not json_errors)
check(f'local Markdown file links resolve ({link_count})', link_count >= 20 and not link_errors)

def sample(key, discriminator):
    return next((s for s in samples.get(key, []) if discriminator in s), {})

route = sample('14', 'copy_policy')
primary = route.get('primary_route', {})
expected_copy = 'done/{}/{}/{}.txt'.format(primary.get('domain'),
    primary.get('subdomain'), route.get('source_id'))
check('route JSON: direct mandatory independent copy',
      route.get('copy_path') == expected_copy
      and route.get('copy_policy') == 'verified_copy_required'
      and route.get('verification_policy') == 'independent_byte_exact'
      and route.get('content_hash') == route.get('copy_sha256')
      and route.get('copy_verification') == {
          'hashes_equal': True, 'bytes_equal': True, 'symlink': False,
          'same_inode': False, 'original_unchanged': True})
check('route JSON: no extraction or synthesis prerequisite',
      route.get('route_status') == 'route_done'
      and route.get('source_extraction_status') == 'not_started'
      and route.get('concept_refs') == [] and route.get('master_refs') == [])

reading = sample('14', 'semantic_segments')
segments = reading.get('semantic_segments', [])
check('reading JSON: IO, contiguous segments and notes separate',
      reading.get('io', {}).get('eof_reached') is True
      and bool(segments) and segments[0]['start'] == 0
      and all(s['start'] < s['end'] for s in segments)
      and all(a['end'] == b['start'] for a, b in zip(segments, segments[1:]))
      and segments[-1]['end'] == reading.get('view', {}).get('length')
      and all({'reader', 'reviewer', 'read_at', 'reviewed_at', 'note',
               'content_unit_ids'} <= set(s) for s in segments)
      and 'notes' in reading)
units = reading.get('content_units', [])
check('reading JSON: all illustrated units have reviewed dispositions',
      bool(units) and {u['unit_id'] for u in units} ==
      {uid for s in segments for uid in s['content_unit_ids']}
      and all({'locator', 'disposition', 'review_ref'} <= set(u) for u in units))
snapshot = sample('15', 'candidate_manifest')
manifest = snapshot.get('candidate_manifest', [])
check('snapshot JSON: batch cannot claim all-domain completion',
      snapshot.get('scope_kind') == 'batch'
      and bool(snapshot.get('parent_snapshot_id'))
      and snapshot.get('eligible_for_T') is False
      and snapshot.get('inventory_complete') is False
      and bool(manifest)
      and len({c['candidate_id'] for c in manifest}) == len(manifest)
      and all({'disposition', 'reason', 'evidence_locators', 'reviewer'} <= set(c)
              for c in manifest)
      and any(c['disposition'] == 'referred_domain' for c in manifest))
term = sample('13', 'term_id')
claim = sample('13', 'claim_id')
check('term and candidate Claim JSON: traceability before synthesis',
      term.get('status') == claim.get('status') == 'candidate'
      and bool(term.get('occurrences'))
      and term.get('concept_refs') == [] and term.get('master_refs') == []
      and {'source_id', 'locator', 'evidence_quote', 'evidence_type', 'scope',
           'confidence', 'review', 'created', 'updated'} <= set(claim)
      and claim.get('evidence_type') == 'example'
      and claim.get('confidence') == 'source_reported')
catalog = sample('18', 'domains')
state = sample('16', 'active_domain')
domain_ids = {'sales', 'outreach', 'pricing_offers', 'content_strategy'}
check('catalog/state JSON: same four domains and one state owner',
      {d['id'] for d in catalog.get('domains', [])} == domain_ids
      and state.get('order') == ['sales', 'outreach', 'pricing_offers', 'content_strategy']
      and set(state.get('domain_states', {})) == domain_ids
      and 'active_domain' not in catalog and state.get('active_domain') is None
      and {'owner_run_id', 'fencing_token', 'lease_until'} <= set(state.get('lock', {})))
delta = sample('19', 'delta_id')
check('delta JSON: queued, stale and explicit invalidation',
      delta.get('coverage_status') == 'stale' and delta.get('schedule') == 'queued'
      and delta.get('impact_status') == 'pending_review'
      and delta.get('reopen_decision_ref') is None
      and set(delta.get('invalidated_gates', [])) == {'R', 'T', 'C', 'K', 'M', 'QA'})
for error in json_errors + link_errors:
    print(error)
print(f'RESULT: {sum(checks)}/{len(checks)} checks passed')
raise SystemExit(0 if all(checks) else 1)
```

أمر التشغيل، دون إنشاء ملف Python أو cache:

```sh
python3 -B -c 'from pathlib import Path; t=Path("/root/r/reports/sales-proof/agent-general-systems-v3.md").read_text(); exec(compile(t.split("```python\n",1)[1].split("\n```",1)[0],"agent-general-systems-v3.md::regression","exec"))'
```
