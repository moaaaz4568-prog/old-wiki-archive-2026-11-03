# Worker — مواءمة كتالوج المجالات والشجرة v3

## الهدف والنطاق والحالة

- الهدف: تطبيق مرجع المواءمة والملحق الأحدث على `config/` و`new/` و`done/` فقط.
- المرجع: [المواءمة](MULTIDOMAIN_ALIGNMENT_2026-10-10.md) و[ملحق الرسائل](USER_MESSAGES_SESSION_EF22.md)، locator: `current_conversation: expansion_request_after_EF22`.
- الطلب الحالي يخصص quarantine لـ`missing/corrupt/unreadable` فقط؛ وهو أدق وأحدث من صياغة §2 في المواءمة التي ذكرت الغموض كمثال للعزل.
- الحالة الأولية المقاسة: الشجرة v2 تحتوي فهارس legacy تحت source_refs، ولا فهارس للجذور الثلاثة. لم يُقرأ أي raw دلاليًا في هذه المتابعة.
- الوضع الحالي: نُفذت مواءمة config وnew/done واجتاز فحص العقد والشجرة. الخطوة التالية للقائد: مراجعة التسليم وتكامل المستهلكين؛ لا يحدّث Worker TODO أو يغلق مجالًا.
- لا إغلاق للمبيعات، لا subagents، لا تعديل ملفات وكلاء آخرين أو الطبقات الأصلية أو raw أو Skills.

## الفرق عن v2

| المسألة | v2 | v3 |
|---|---|---|
| intake | حظر تصنيف pending | `global_intake_routing` يتيح القراءة والتصنيف والتوجيه والنسخ والتحقق لكل المجالات؛ القفل للعمل المعرفي فقط |
| التأجيل والعزل | ربط pending والغموض بـquarantine | pending مؤجل؛ الغموض uncertain/cross_domain_review؛ quarantine فقط missing/corrupt/unreadable |
| سلطة التصنيف | أسبقية حدود الـVault | الخام body/structure/purpose مع مواضعه يحكم؛ الـVault دليل بنية فقط، بلا شرط قبول معرفته |
| معنى الترتيب | ربطه بنتائج بزنس وعرض مثبت | قرار موجة معرفية فقط، لا شرط بيع فعلي أو ادعاء أن كتابة الويكي تجلب عملاء |
| موضع المصدر | source_refs وفهرسة فقط | `done/<domain>/<subdomain>/` لنسخة مستقلة byte-exact وroute metadata، بلا symlink/hardlink أو إزالة الأصل |
| legacy | مواضع مصدر محتملة | جميع source_refs محفوظة كروابط مباشرة فقط؛ لا نسخة canonical ثانية |
| الاكتمال | اعتماد source_done ضمنيًا على Master | route_done وsource_done وsubdomain_extraction_done وdomain_terms_complete وdomain_done منفصلة؛ source_done بلا Master |
| بدء Master | بوابات عامة دون all-source شرط حاسم | T لكل مصادر المجال وكل subfolders في snapshot شامل حديث، مع C/K اللازمة، حتى لأصغر Master |
| القادم من المصادر | لا سياسة تفصيلية | delta وstale وحفظ الإغلاق التاريخي بلقطته، ومراجعة الأثر قبل انتقال أو تغطية حديثة، تحت قفل مجال واحد |

أضيف `workflow_contract_version=2026-10-10` إلى الملفين، و`route_path_template`
وسياسة النسخ وعقد route metadata. معاني R/T/C/K/M/QA مصرح بها في processing_order.
اللقطة الحالية مبدئية: sales in_progress؛ الباقي pending؛ R/T/C/K/M/QA كلها
not_closed، والعدادات غير المقاسة وsnapshot_id/reviewer/closure_record_path
تظل null. لم تُنشأ هوية مصدر أو route metadata توهم بالإنجاز.

### المسارات التي تغيرت

- تعديل `config/domain_catalog.json` و`config/processing_order.json`.
- إنشاء `config/INDEX.md` و`new/INDEX.md` و`done/INDEX.md` بروابط فعلية.
- تحديث README في new وdone، وفهارس المجالات وطبقاتها والـlegacy.
- إنشاء 21 مجلد subdomain مباشر بالأسماء السابقة **دون إعادة تسمية أو حذف**.
- إضافة `done/sales/negotiation/INDEX.md`: حالة provisional، وسندها النص
  «قسم للتفاوض قسم للاعتراضات» في locator الأحدث، لا معرفة خام مختلقة.
  بذلك أصبح العدد التنظيمي **22 = 21 محفوظة + negotiation**، موزعًا 6/5/5/6.
- أبقيت مجلدات legacy الـ21 كما هي، ولكل منها رابط إلى نظيره المباشر؛ لم
  أنشئ negotiation تحت source_refs. layer dirs فهارس للأصل لا duplicate knowledge.
- تقرير v2 لم يُعدّل؛ نتائجه تاريخية واختباره القديم لم يُعامل عقدًا حاليًا.

### صدق counters والقراءة

- القراءة الدلالية للـraw في هذه المراجعة: **0**؛ التصنيف الفعلي: **0**؛
  النسخ الفعلي: **0**؛ الاستخراج المعرفي: **0**.
- أبقيت 1,776 ملفًا و0 صف بمقدمة raw/new في manifest **كقياس v2 تاريخي فقط**
  مع `measurement_origin` صريح. لم أعد الجرد أو أقرأ raw أو manifest هذه المرة.
- أعداد الـVault القديمة وحقول canonical_evidence_paths محفوظة كمرجع بنيوي
  تاريخي فقط؛ تحققت الاختبارات من وجود المسارات دون قراءة محتواها المعرفي.
- لم يُشغّل `wiki_quality.py` في هذه المتابعة لأنه يقرأ raw والطبقات خارج نطاق
  التصحيح، ولأنه لا يتحقق من config/new/done. لا يُعاد تقديم PASS v2 كفحص جديد.

### قيد خارج النطاق ظاهر للقائد

أظهر فحص أسماء المجلدات في جذر الويكي أن `terms/` غير موجود في هذه اللقطة.
لذلك فهارس done/terms تربط [خريطة الطبقات](/sdcard/NEXUS_LLM_WIKI/config/INDEX.md)
وعقد T بدل اختلاق رابط إلى طبقة غائبة أو إنشاء duplicate knowledge. يجب تعيين
مكان المصطلحات الأصلي في عمل لاحق مصرح قبل إغلاق T؛ لا يمنع هذا تسليم مواءمة
الشجرة لكنه يمنع ادعاء اكتمال المجال. لم أقرأ عمل وكلاء آخرين الجاري لحسمه.

## اختبار العقد المحفوظ — بلا كتابة ملفات

هذا اختبار للقطة الهيكل الحالية، وليس محرك ingest. يشتق أعداد الشجرة من الكتالوج
وفهارس legacy الفعلية؛ لا يستعمل أعداد ملفات v2 كشرط نجاح.

```python
# CATALOG_ALIGNMENT_V3_CHECK
import json
import re
from pathlib import Path

wiki = Path('/sdcard/NEXUS_LLM_WIKI')
def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, ('duplicate_json_key', key)
        result[key] = value
    return result

c = json.loads((wiki/'config/domain_catalog.json').read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
o = json.loads((wiki/'config/processing_order.json').read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
assert c.get('workflow_contract_version') == o.get('workflow_contract_version') == '2026-10-10', 'workflow contract missing or stale'
ids = ['sales', 'outreach', 'pricing_offers', 'content_strategy']
assert [d['domain_id'] for d in c['domains']] == o['order'] == ids
assert [d['status'] for d in c['domains']] == ['in_progress', 'pending', 'pending', 'pending']
assert o['current_domain'] == 'sales' and o['sales_completion_claim'] is False
assert c['route_path_template'] == o['route_path_template'] == 'done/<domain>/<subdomain>/'
for config in (c, o):
    assert config['global_intake_routing']['allowed'] is True
    assert config['global_intake_routing']['pending_domains_allowed'] is True
assert c['vault_reference_policy']['role'] == 'structure_only'
assert c['vault_reference_policy']['routing_authority'] == 'raw_content'
assert c['vault_reference_policy']['knowledge_acceptance_prerequisite'] is False
copy_policy = c['source_copy_policy']
assert copy_policy['mode'] == 'independent_byte_exact' and copy_policy['preserve_raw'] is True
assert copy_policy['symlinks_allowed'] is False and copy_policy['hardlinks_allowed'] is False
assert copy_policy['single_primary_copy'] is True and copy_policy['verify_both_sha256'] is True
assert copy_policy['overwrite_existing'] is False
assert c['source_policy']['raw_new_inventory']['source_bodies_reviewed_by_this_worker'] == 0
assert c['execution_snapshot']['raw_semantic_reads_this_revision'] == 0
assert c['execution_snapshot']['source_copies_this_revision'] == 0
assert o['domain_knowledge_lock']['max_active_domains'] == 1
assert o['domain_knowledge_lock']['excludes_global_intake_routing'] is True
assert set(o['gate_definitions']) == {'R', 'T', 'C', 'K', 'M', 'QA'}
assert o['completion_states']['source_done']['requires_master'] is False
assert o['completion_states']['domain_terms_complete']['all_subdomains_required'] is True
assert o['completion_states']['domain_terms_complete']['all_source_snapshot_required'] is True
assert o['completion_states']['domain_terms_complete']['unresolved_candidate_membership_blocks_completion'] is True
assert o['master_start_condition']['requires_domain_terms_complete'] is True
assert o['master_start_condition']['includes_small_masters'] is True
assert o['master_start_condition']['requires_reviewed_claims_and_concepts'] is True
assert o['revision_policy']['on_new_relevant_source'] == 'mark_coverage_stale_and_create_delta'
assert o['revision_policy']['preserve_historical_closure'] is True
assert o['revision_policy']['block_next_transition_until_delta_review'] is True
assert o['next_domain_open_condition']['requires_state'] == 'domain_done'
assert o['next_domain_open_condition']['routing_does_not_unlock_knowledge'] is True

expected_files = {'config/domain_catalog.json', 'config/processing_order.json', 'config/INDEX.md', 'new/README.md', 'new/INDEX.md', 'done/README.md', 'done/INDEX.md'}
layers = ['source_refs', 'terms', 'claims', 'concepts', 'masters', 'reports']
legacy_count = direct_count = 0
for i, domain in enumerate(c['domains']):
    did = domain['domain_id']
    base = wiki/'done'/did
    state = o['domain_states'][i]
    assert state['domain_id'] == did and state['status'] == domain['status']
    assert state['knowledge_locked'] is (i != 0)
    assert state['routing_allowed'] is True
    assert state['domain_done'] == 'not_closed'
    snapshot = state['gate_snapshot']
    assert snapshot['snapshot_id'] is None and snapshot['reviewer'] is None
    assert snapshot['evaluated_at'] is None and snapshot['evidence_paths'] == []
    assert snapshot['open_source_count'] is None and snapshot['unresolved_critical_count'] is None
    assert snapshot['domain_terms_complete'] == 'not_closed'
    assert set(snapshot['gates']) == set(o['gate_definitions'])
    assert all(v == 'not_closed' for v in snapshot['gates'].values())
    assert set(domain['quarantine']['triggers']) == {'missing', 'corrupt', 'unreadable'}
    assert domain['cross_domain_review']['ambiguity_state'] == 'uncertain'
    subs = {s['subdomain_id'] for s in domain['subdomains']}
    assert len(subs) == len(domain['subdomains'])
    assert all(re.fullmatch(r'[a-z][a-z0-9_]*', sub) for sub in subs)
    assert all(s['status'] == 'provisional' for s in domain['subdomains'])
    legacy = {p.name for p in (base/'source_refs').iterdir() if p.is_dir()}
    assert subs == legacy | ({'negotiation'} if did == 'sales' else set()), 'v2 names must survive'
    actual_subs = {p.name for p in base.iterdir() if p.is_dir()} - set(layers)
    assert actual_subs == subs, (did, actual_subs, subs)
    expected_files.add('done/' + did + '/INDEX.md')
    expected_files.update('done/' + did + '/' + layer + '/INDEX.md' for layer in layers)
    for sub in subs:
        rel = 'done/' + did + '/' + sub + '/INDEX.md'
        expected_files.add(rel)
        assert 'provisional' in (wiki/rel).read_text(encoding='utf-8')
    for sub in legacy:
        rel = 'done/' + did + '/source_refs/' + sub + '/INDEX.md'
        expected_files.add(rel)
        text = (wiki/rel).read_text(encoding='utf-8')
        assert 'legacy' in text and '(../../' + sub + '/INDEX.md)' in text
    for path in domain['canonical_evidence_paths']:
        assert Path(path).is_file()
    direct_count += len(subs)
    legacy_count += len(legacy)

negotiation = next(s for s in c['domains'][0]['subdomains'] if s['subdomain_id'] == 'negotiation')
assert negotiation['evidence']['locator'] == 'current_conversation: expansion_request_after_EF22'
assert c['catalog_change']['current_subdomain_count'] == direct_count
assert c['catalog_change']['retained_subdomain_count'] == legacy_count
assert direct_count - legacy_count == len(c['catalog_change']['added_subdomains']) == 1
entries = [p for root in ('config', 'new', 'done') for p in (wiki/root).rglob('*')]
assert all(not p.is_symlink() for p in entries)
actual_files = {p.relative_to(wiki).as_posix() for p in entries if p.is_file()}
assert actual_files == expected_files, ('unexpected', actual_files - expected_files, 'missing', expected_files - actual_files)
dirs = [wiki/root for root in ('config', 'new', 'done')] + [p for p in entries if p.is_dir()]
assert all((p/'INDEX.md').is_file() for p in dirs)
assert all(re.fullmatch(r'[A-Za-z0-9_./]+', rel) and '..' not in Path(rel).parts for rel in actual_files)
link_count = 0
for rel in actual_files:
    path = wiki/rel
    assert path.stat().st_size > 0
    if path.suffix != '.md':
        continue
    text = path.read_text(encoding='utf-8')
    assert '2026-10-10' in text
    links = re.findall(r'\]\(([^)]+)\)', text)
    assert links, ('unlinked_index', rel)
    for link in links:
        assert (path.parent/link.split('#', 1)[0]).exists(), (rel, link)
        link_count += 1
print('CONTRACT_CHECK=PASS global_intake=true knowledge_current=sales gates=R/T/C/K/M/QA')
print('TREE_CHECK=PASS files=%d directories=%d direct_subdomains=%d legacy_subdomains=%d' % (len(actual_files), len(dirs), direct_count, legacy_count))
print('LINK_CHECK=PASS links=%d raw_semantic_reads=0 source_copies=0' % link_count)
```

التشغيل:

```sh
python3 -B -c 'from pathlib import Path; t=Path("/root/r/reports/sales-proof/agent-domain-catalog-v3.md").read_text(encoding="utf-8"); code=t.split("```python\n# CATALOG_ALIGNMENT_V3_CHECK\n",1)[1].split("\n```",1)[0]; exec(compile(code,"catalog_alignment_v3_check","exec"))'
```

## نتائج التحقق

- **RED قبل تعديل config والشجرة:** اختبار التقرير نفسه فشل برمز 1 عند
  `AssertionError: workflow contract missing or stale`؛ v2 لا يحمل العقد الجديد.
- **GREEN بعد المواءمة:** أعيد تشغيل الأمر المحفوظ، رمز الخروج 0:

```text
CONTRACT_CHECK=PASS global_intake=true knowledge_current=sales gates=R/T/C/K/M/QA
TREE_CHECK=PASS files=78 directories=74 direct_subdomains=22 legacy_subdomains=21
LINK_CHECK=PASS links=264 raw_semantic_reads=0 source_copies=0
```

الأعداد ناتج قراءة الشجرة الحالية؛ expected files مشتقة من المجالات وsubdomains
والـlegacy الحالية، وليست شرطًا hardcoded لـ53 أو49 كما في v2. مجموعة الملفات
مطابقة، كل مجلد له INDEX، لا ملفات مصدر أو route metadata فعلية، لا symlinks،
ولا مصادر أو معرفة مزدوجة تحت legacy/layer dirs. الروابط تحققت بالوجود فقط؛
هذا ليس اختبار استرجاع معرفي أو مراجعة لمضمون الوجهات.

تحقق محلل JSON القياسي نجح للملفين (رمز 0):

```sh
python3 -B -m json.tool /sdcard/NEXUS_LLM_WIKI/config/domain_catalog.json >/dev/null && python3 -B -m json.tool /sdcard/NEXUS_LLM_WIKI/config/processing_order.json >/dev/null
```

أعيد `lsp_diagnostics` فعليًا للملفين JSON، وفهارس جذور config/new/done،
وnew/README وdone/README وهذا التقرير: `No diagnostics found. All clean!` لكل منها.
هذه diagnostics بنيوية وليست دليل اكتمال معرفي. كذلك لم يجد البحث المستهدف
في owned config/done قواعد الحظر القديمة لتصنيف pending أو أسبقية canonical
على التصنيف الخام؛ راجعت النصوص ضمن النطاق فقط.

## حدود التسليم

هذا تصحيح للشجرة والسياسة، لا محرك ingest جديدًا ولا تشغيل مصدر تجريبي.
لم أتحقق عمليًا من نسخ byte-exact لأن النسخ وقراءة raw خارج التكليف الحالي؛
التحقق اختبر وجود سياسة الحماية وعقد metadata وعدم وجود نسخ وهمية فقط.
كل تعديل كان عبر apply_patch في النطاق المسموح وتقرير v3، دون حذف ملفات،
ودون تعديل systems/charter/Skills/raw أو طبقات المصدر والمعرفة الأصلية.
لم تُشغّل Agents فرعية أو Codex، ولم يُعلن نجاح R/T/C/K/M/QA أو domain_done.
