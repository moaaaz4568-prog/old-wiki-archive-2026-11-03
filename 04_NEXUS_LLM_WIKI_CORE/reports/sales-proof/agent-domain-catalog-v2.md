# تقرير Worker — كتالوج المجالات وشجرة الحالات v2

**التاريخ:** 2026-10-10
**النطاق:** كتالوج المجالات وشجرة الحالات فقط
**الحالة:** تم إنشاء الكتالوج والشجرة الأولية؛ لم يُعلن `sales` مكتملًا.

**الهدف الحالي:** تسليم هيكل حالة مفهرس بلا نقل مصادر أو بناء معرفة.
**الخطوة التالية:** مراجعة Commander للمخرجات وللفجوة خارج النطاق؛ اجتاز فحص
العقد المحفوظ أدناه التشغيل الفعلي. تبقى مسؤولية تحديث TODO وإغلاق المجال
للقائد. لم تُعدّل ملفات المهمة القديمة.
**العوائق خارج النطاق:** تغطية manifest لمجموعة `raw/new/` غير موجودة في الملف
المحدد؛ وبوابات إغلاق sales لم تُقيّم في هذه المهمة ولا يجوز افتراض اجتيازها.

## المخرجات

أُنشئت الملفات والمسارات التالية فقط ضمن نطاق التسليم:

- `/sdcard/NEXUS_LLM_WIKI/config/domain_catalog.json`
- `/sdcard/NEXUS_LLM_WIKI/config/processing_order.json`
- `/sdcard/NEXUS_LLM_WIKI/new/README.md`
- `/sdcard/NEXUS_LLM_WIKI/done/README.md`
- شجرة `done/<domain>/` للمجالات الأربعة، وفي كل مجال `INDEX.md`، ومجلدات
  `source_refs/`, `terms/`, `claims/`, `concepts/`, `masters/`, `reports/` مع
  فهارسها.
- مجلدات الـsubdomains المقترحة تحت `source_refs/` فقط، ولكل مجلد `INDEX.md`:
  5 لـ`sales`، و5 لـ`outreach`، و5 لـ`pricing_offers`، و6 لـ`content_strategy`.

لم تُنشأ مصادر أو Claims أو Concepts أو Masters فعلية، ولم تُنقل أي مادة خام.

## ما قُرئ وفُحص

قُرئت الملفات المطلوبة كاملة:

1. `/root/r/reports/sales-proof/USER_MESSAGES_SESSION_EF22.md`
2. `/root/r/reports/sales-proof/agent-domain-selection.md`
3. `/sdcard/NEXUS_LLM_WIKI/MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md`

وفُحص وجود وقراءة:

- `/sdcard/NEXUS_LLM_WIKI/raw/new/` — موجود.
- `/sdcard/NEXUS_LLM_WIKI/raw/SOURCE_MANIFEST.tsv` — موجود، وله 5,169 صف بيانات
  و5,170 سطرًا مع رأس الجدول.
- `/sdcard/Nexus_Brain/nexus_vault/BRAIN_INDEX.md` — موجود؛ يعلن 39 Master
  canonical و26 cluster و32 graph edges.
- فهارس المجالات الأربعة:
  `01_outreach/_index.md`, `02_sales_closing/_index.md`,
  `03_pricing_offers/_index.md`, `04_content_strategy/_index.md` — كلها موجودة
  وقُرئت.

## إحصاء `raw/new/`

جُرد وجود وأسماء/امتدادات الملفات الـ1,776 تحت
`/sdcard/NEXUS_LLM_WIKI/raw/new/`. **هذا جرد ملفات لا قراءة معرفية كاملة**؛
عدد النصوص الخام التي راجعت مضمونها للتصنيف في هذا التسليم: **0**.

| النوع | العدد |
|---|---:|
| `.txt` | 1,772 |
| `.md` | 3 |
| `.srt` | 1 |
| **الإجمالي** | **1,776** |

نتيجة فحص الـmanifest: لا يوجد أي صف يبدأ بـ`raw/new/` في
`SOURCE_MANIFEST.tsv` (`raw_new_manifest_rows=0`). لذلك سُجلت الملفات الـ1,776
بوصفها موجودة في inbox ودون تصنيف جديد في هذا العمل، ولم أزعم مطابقة hash لها
مع ذلك الـmanifest؛ لا توجد صفوف مقابلة تسمح بذلك. لا يعني ذلك غياب سجلات
`sources/` أو manifests أخرى. بقي الإدخال الحالي immutable.

قراءة `file_stats` أظهرت إجمالي 43,757,343 بايت. قراءة الـmanifest عبر فحص TSV
أظهرت 5,169 مسارًا فريدًا، كل صف له 3 أعمدة وحجم رقمي وبصمة صحيحة الشكل؛
لا يعني فحص الشكل تحقق البصمات. لم يُعدّل manifest لتغطية الفجوة.

## قرار الكتالوج والحالة

الترتيب الصارم المسجل هو:

```text
sales → outreach → pricing_offers → content_strategy
```

- `current_domain = sales`
- `sales = in_progress`، و`completion_claim = false`
- `outreach = pending` ومقفل حتى `sales = done`
- `pricing_offers = pending` ومقفل حتى `outreach = done`
- `content_strategy = pending` ومقفل حتى `pricing_offers = done`

أسماء الـsubdomains في الكتالوج وفي مجلدات `source_refs/` **provisional** فقط؛
لا تمثل اعتمادًا نهائيًا ولا إغلاقًا لأي بوابة.

## أدلة المجالات النشطة (canonical)

الأرقام التالية من الفهارس المرجعية الموجودة، وليست إنتاجًا جديدًا أو قياسًا
لأعداد Concepts الفريدة فعليًا. صفة canonical تخص الـVault القديم ولا تُمرر
أي بوابة قبول في الموجة الحالية:

| المجال | الـcluster | Masters نشطة | Concepts المفهرسة |
|---|---|---:|---:|
| `sales` | `02_sales_closing` | 4 | 186 |
| `outreach` | `01_outreach` | 4 | 150 |
| `pricing_offers` | `03_pricing_offers` | 1 | 131 |
| `content_strategy` | `04_content_strategy` | 1 | 161 |

أضيفت إلى `domain_catalog.json` مسارات الـBRAIN_INDEX وفهرس كل cluster وكل
Master canonical ذي الصلة (18 إحالة، منها 15 مسارًا فريدًا)، مع إشارات
body/structure/purpose وقواعد المراجع الثانوية وquarantine وcross-domain review.

- الأساس البنيوي والترتيب: الميثاق §§3–9، وتقرير الاختيار `L5-L21`.
- منشأ أسماء subdomains: تقرير الاختيار `L60-L68`، `L92-L100`، `L119-L127`،
  `L146-L155`. جميع الأسماء الـ21، وحدودها وإشارات التصنيف المصاغة هنا
  **provisional** إلى أن تُراجع أدلة المصادر؛ ليست نتائج تصنيف الـ1,776 ملفًا.
- التغطية المرجعية: `BRAIN_INDEX.md:L9-L65` وفهارس المجالات الأربعة `L7-L10`
  للمبيعات/outreach و`L7` للتسعير/المحتوى. تحقق وجود Masters العشرة بالفعل.
- قُرئت تعليمات الـVault و`SCHEMA.md` ومدقق `tools/wiki_quality.py`، وحُمّلت
  مهارتا `personal-knowledge-base` و`test-authoring` دون تعديل Skills.
- شُغل استكشاف `planner.py --format compact`؛ نتائجه مرشحون لا ترتيب بديل.
  واستُحضر `query.py --master Master_Sales_Conversation --section 17`، فظهر
  تسلسل Discovery/Proposal/Follow-up/Objections، داعمًا لحدود sales المقترحة؛
  لم تُنقل توصياته أو أرقامه إلى Claims أو Masters جديدة.

## اتساق المسارات والمستهلكين

المسار المنطقي `done/<domain>/<subdomain>/` في الميثاق يُمثّل فعليًا هنا بـ
`done/<domain>/source_refs/<subdomain>/` وفق التكليف الحالي. README الاستقبال
وREADME الإغلاق يصرّحان بهذا التطابق. لا توجد مجلدات subdomain خارج source_refs.
السجلات غير المحسومة تبقى في `new/`؛ شجرة done الفارغة ليست إعلان اكتمال.

فهارس `done/<domain>/terms|claims|concepts|masters/` مراجع للأعمال المقبولة
لاحقًا، وليست ترحيلًا أو نسخة canonical ثانية من طبقات جذر الويكي. عُدّلت
شروط الانتقال لتطلب نجاح T/C/K/M صراحةً، وإغلاق جميع subdomains وملاحظاتها
الحرجة، وقبول QA مستقل؛ «إغلاق» بوابة فاشلة لا يُعد نجاحًا. حقول القياس
والمراجع غير المتاحة تظل `null` أو `not_evaluated`، وليس صفرًا أو PASS.

بحث أسماء `domain_catalog` و`processing_order` داخل `tools/*.py` لم يجد
مستهلكًا قائمًا. الملفات **عقد وتشغيل موثق** وليست محرك انتقال تلقائيًا؛ لم
أضف كودًا أو واجهة API. مدقق `wiki_quality.py` يفحص الطبقات الموجودة فقط ولا
يفحص هذه الإعدادات الجديدة؛ لذا فحص العقد أدناه منفصل عنه.

## تحقق JSON وبنية الشجرة

شُغّل تحقق قراءة فقط بعد الإنشاء:

```text
python3 - <<'PY'
import json
from pathlib import Path

wiki = Path('/sdcard/NEXUS_LLM_WIKI')
catalog = json.loads((wiki/'config/domain_catalog.json').read_text())
order = json.loads((wiki/'config/processing_order.json').read_text())
assert [d['domain_id'] for d in catalog['domains']] == ['sales', 'outreach', 'pricing_offers', 'content_strategy']
assert [d['status'] for d in catalog['domains']] == ['in_progress', 'pending', 'pending', 'pending']
assert order['order'] == ['sales', 'outreach', 'pricing_offers', 'content_strategy']
assert order['current_domain'] == 'sales'
assert order['current_domain_status'] == 'in_progress'
assert order['sales_completion_claim'] is False
assert all(s['status'] == 'provisional' for d in catalog['domains'] for s in d['subdomains'])
print('JSON_CHECK=PASS domains=4 statuses=sales:in_progress,others:pending provisional_subdomains=21')
PY
```

النتيجة الفعلية:

```text
JSON_CHECK=PASS domains=4 statuses=sales:in_progress,others:pending provisional_subdomains=21
```

وتحقق بنية قراءة فقط من وجود 53 ملف فهرس/README/JSON متوقعًا، و21 مجلد
subdomain تحت `source_refs/` فقط، ومن عدم وجود أي ملف مصدر فعلي داخل شجرة
`done/`:

```text
TREE_CHECK=PASS expected_files=53 actual_files=53 domains=4 layer_indexes=24 subdomain_indexes=21 source_files_in_done=0
```

كما تحقق الفحص من وجود كل المسارات الكنسية المدرجة في الكتالوج ومن وجود مسارات
الاستقبال والـmanifest؛ النتيجة:

```text
PATH_CHECK=PASS canonical_paths=18 required_inputs=7
```

وفحصت أداة JSON القياسية، وأسماء المسارات، وLSP للملفين JSON:

```text
JSON_TOOL_CHECK=PASS files=2
SAFE_NAME_CHECK=PASS scanned_paths=102
LSP domain_catalog.json: No diagnostics found. All clean!
LSP processing_order.json: No diagnostics found. All clean!
```

**تصحيح في أداة التحقق نفسها:** أول تشغيل لفحص الشجرة أعطى `AssertionError`
بعد PASS للـJSON، لأن assertion خاطئًا اشترط أن تكون كل عناصر `source_refs/`
ملفات `INDEX.md` بدل السماح بمجلدات subdomains المطلوبة. أظهر الفحص التشخيصي
تطابق 53/53 ملفًا وعدم وجود missing/extra. صُحح assertion للتحقق من نوع كل
مجلد وفهرسه، ثم نجح فحص الشجرة والمسارات. لم يكن الفشل عيبًا في الشجرة ولا
يجوز إخفاؤه أو اعتباره فحصًا ناجحًا من أول مرة.

### إعادة فحص العقد من التقرير نفسه (قراءة فقط)

لمنع إنشاء ملف اختبار خارج الملفات المطلوبة، احتُفظ بالفحص التالي داخل التقرير.
يفحص العقد الابتدائي فقط؛ تغير حالة المجال لاحقًا يستلزم تحديث اختبار تلك اللقطة.

```python
# CATALOG_TREE_VERIFY_V2
import copy
import csv
import json
import re
from collections import Counter
from pathlib import Path

wiki = Path('/sdcard/NEXUS_LLM_WIKI')
brain = Path('/sdcard/Nexus_Brain/nexus_vault')
ids = ['sales', 'outreach', 'pricing_offers', 'content_strategy']
statuses = ['in_progress', 'pending', 'pending', 'pending']
layers = ['source_refs', 'terms', 'claims', 'concepts', 'masters', 'reports']

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, ('duplicate_json_key', key)
        result[key] = value
    return result

catalog = json.loads((wiki/'config/domain_catalog.json').read_text(encoding='utf-8'), object_pairs_hook=unique_object)
order = json.loads((wiki/'config/processing_order.json').read_text(encoding='utf-8'), object_pairs_hook=unique_object)
selection = Path('/root/r/reports/sales-proof/agent-domain-selection.md').read_text(encoding='utf-8')
proposed = re.findall(r'^\d+\. `([a-z][a-z0-9_]*)`', selection, re.M)[4:]

def check_contract(catalog, order):
    domains = catalog['domains']
    assert [d['domain_id'] for d in domains] == ids
    assert [d['status'] for d in domains] == statuses
    assert all(d['completion_claim'] is False for d in domains)
    assert catalog['state_authority'] == 'config/processing_order.json'
    assert catalog['source_policy']['raw_inbox_immutable'] is True
    assert catalog['classification_policy']['execution_in_this_task'] is False
    subids = [s['subdomain_id'] for d in domains for s in d['subdomains']]
    assert subids == proposed and len(subids) == len(set(subids)) == 21
    for domain in domains:
        for field in ['title', 'canonical_evidence_paths', 'body_signals', 'structure_signals', 'purpose_signals', 'secondary_references', 'quarantine', 'cross_domain_review']:
            assert domain[field], (domain['domain_id'], field)
        for sub in domain['subdomains']:
            assert re.fullmatch(r'[a-z][a-z0-9_]*', sub['subdomain_id'])
            assert sub['status'] == 'provisional' and sub['title'] and sub['basis']
        assert domain['quarantine']['pending_record_root'] == 'new/'
        assert domain['quarantine']['physical_directory_created'] is False
        assert domain['cross_domain_review']['pending_record_root'] == 'new/'
        assert domain['cross_domain_review']['status'] == 'policy_only_no_items_created'
    assert order['order'] == ids and order['current_domain'] == 'sales'
    assert order['current_domain_status'] == 'in_progress' and order['sales_completion_claim'] is False
    assert order['strict_order'] is True and order['parallel_domain_processing'] is False
    assert order['unknown_or_missing_evidence_blocks_transition'] is True
    assert len(order['next_domain_open_condition']) >= 7
    states = order['domain_states']
    assert [s['domain_id'] for s in states] == ids
    assert [s['status'] for s in states] == statuses
    for i, state in enumerate(states):
        assert state['position'] == i + 1
        assert state['opened'] is (i == 0) and state['locked'] is (i != 0)
        assert state.get('previous_domain') == (ids[i-1] if i else None)
        assert state.get('next_domain') == (ids[i+1] if i < 3 else None)
        gate = state['gate_snapshot']
        for key in ['evaluated_at', 'reviewer', 'closure_record_path', 'all_subdomains_closed', 'open_source_count', 'unresolved_critical_count', 'indexes_verified']:
            assert gate[key] is None, (state['domain_id'], key)
        assert gate['evidence_paths'] == [] and gate['qa_decision'] == 'not_evaluated'
        for key in ['terms', 'claims', 'concepts', 'masters', 'qa_index']:
            assert gate[key] == ('not_closed' if i == 0 else 'locked')
        summary = order['gate_snapshot'][state['domain_id']]
        assert summary['status'] == statuses[i] and summary['complete'] is False

check_contract(catalog, order)
print('CONTRACT_CHECK=PASS domains=4 provisional_subdomains=21 unknown_gates_block_transition')

# Negative cases change in-memory copies only, never files or domain state.
mutants = []
c, o = copy.deepcopy(catalog), copy.deepcopy(order)
c['domains'][0]['status'] = 'done'
mutants.append((c, o))
c, o = copy.deepcopy(catalog), copy.deepcopy(order)
o['domain_states'][1]['opened'] = True
mutants.append((c, o))
c, o = copy.deepcopy(catalog), copy.deepcopy(order)
c['domains'][0]['subdomains'][0]['subdomain_id'] = '../outside'
mutants.append((c, o))
c, o = copy.deepcopy(catalog), copy.deepcopy(order)
o['domain_states'][0]['gate_snapshot']['open_source_count'] = 0
mutants.append((c, o))
for c, o in mutants:
    try:
        check_contract(c, o)
    except AssertionError:
        continue
    raise AssertionError('invalid_snapshot_was_accepted')
print('NEGATIVE_CASES=PASS rejected=4 in_memory_only')

expected_files = {'config/domain_catalog.json', 'config/processing_order.json', 'new/README.md', 'done/README.md'}
canonical_paths = []
for domain in catalog['domains']:
    base = 'done/' + domain['domain_id']
    expected_files.add(base + '/INDEX.md')
    expected_files.update(base + '/' + layer + '/INDEX.md' for layer in layers)
    expected_files.update(base + '/source_refs/' + sub['subdomain_id'] + '/INDEX.md' for sub in domain['subdomains'])
    canonical_paths.extend(domain['canonical_evidence_paths'])
expected_dirs = set()
for rel in expected_files:
    expected_dirs.update(p.as_posix() for p in Path(rel).parents if p.as_posix() != '.')
paths = []
for root in ['config', 'new', 'done']:
    paths.append(wiki/root)
    paths.extend((wiki/root).rglob('*'))
assert all(not p.is_symlink() for p in paths)
actual_files = {p.relative_to(wiki).as_posix() for p in paths if p.is_file()}
actual_dirs = {p.relative_to(wiki).as_posix() for p in paths if p.is_dir()}
assert actual_files == expected_files, (actual_files - expected_files, expected_files - actual_files)
assert actual_dirs == expected_dirs
assert len(actual_files) == 53
assert all(re.fullmatch(r'[a-zA-Z0-9_./]+', p) and '..' not in Path(p).parts for p in actual_files | actual_dirs)
assert all((wiki/p).stat().st_size > 0 for p in actual_files)
assert len(list((wiki/'done').rglob('INDEX.md'))) == 49
assert all('provisional' in p.read_text(encoding='utf-8') for p in (wiki/'done').glob('*/source_refs/*/INDEX.md'))
assert all(Path(p).is_file() and '_archive' not in Path(p).parts for p in canonical_paths)
assert len(canonical_paths) == 18 and len(set(canonical_paths)) == 15
required = [wiki/'raw/new', wiki/'raw/SOURCE_MANIFEST.tsv', brain/'BRAIN_INDEX.md']
required += [brain/d['canonical_cluster']/'_index.md' for d in catalog['domains']]
assert all(p.exists() for p in required)
assert len(required) == 7 and len(paths) == 105
print('TREE_CHECK=PASS files=53 indexes=49 domains=4 subdomain_dirs=21 source_files_in_done=0')
print('PATH_CHECK=PASS canonical_references=18 unique_paths=15 required_inputs=7 safe_paths=105')

links = []
for rel in actual_files:
    if not rel.endswith('.md'):
        continue
    path = wiki/rel
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        assert (path.parent/link).is_file(), (rel, link)
        links.append(link)
assert len(links) >= 30
print('LINK_CHECK=PASS checked=%d' % len(links))

raw_files = [p for p in (wiki/'raw/new').rglob('*') if p.is_file()]
assert len(raw_files) == 1776
assert Counter(p.suffix for p in raw_files) == {'.txt': 1772, '.md': 3, '.srt': 1}
with (wiki/'raw/SOURCE_MANIFEST.tsv').open(encoding='utf-8', newline='') as source:
    reader = csv.DictReader(source, delimiter='\t')
    assert reader.fieldnames == ['relative_path', 'size_bytes', 'sha256']
    rows = list(reader)
assert len(rows) == len({r['relative_path'] for r in rows}) == 5169
assert all(r['size_bytes'].isdigit() and re.fullmatch('[0-9a-f]{64}', r['sha256']) for r in rows)
assert sum(r['relative_path'].startswith('raw/new/') for r in rows) == 0
print('INVENTORY_CHECK=PASS raw_files=1776 manifest_rows=5169 raw_new_rows=0 semantic_body_reviews=0')
```

أمر تشغيل الفحص المحفوظ، بلا ملفات مؤقتة أو عمليات كتابة:

```sh
python3 -B -c 'from pathlib import Path; text = Path("/root/r/reports/sales-proof/agent-domain-catalog-v2.md").read_text(encoding="utf-8"); code = text.split("```python\n# CATALOG_TREE_VERIFY_V2\n", 1)[1].split("\n```", 1)[0]; exec(compile(code, "catalog_tree_verify_v2", "exec"))'
```

نتيجة إعادة الفحص الفعلية (رمز الخروج 0):

```text
CONTRACT_CHECK=PASS domains=4 provisional_subdomains=21 unknown_gates_block_transition
NEGATIVE_CASES=PASS rejected=4 in_memory_only
TREE_CHECK=PASS files=53 indexes=49 domains=4 subdomain_dirs=21 source_files_in_done=0
PATH_CHECK=PASS canonical_references=18 unique_paths=15 required_inputs=7 safe_paths=105
LINK_CHECK=PASS checked=32
INVENTORY_CHECK=PASS raw_files=1776 manifest_rows=5169 raw_new_rows=0 semantic_body_reviews=0
```

### مدقق المشروع القائم (نتيجة محدودة)

شُغّل بالفعل، دون `--index` أو `--report`:

```sh
python3 -B /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json
```

رمز الخروج 0، و`ok=true` و`errors=[]`. فحص 1,781 Source و1,777 Claim و34
Concept وMaster واحدًا حالته draft. هذا تحقق آلي للبصمات/شرائح النص في
السجلات القائمة، وليس قراءة معرفية مني ولا مطابقة مع `SOURCE_MANIFEST.tsv`.
كما لا يثبت نجاح T/C/K/M، ولا يغطي `config/` و`new/` و`done/`؛ لذلك لا يوجد
إعلان PASS للمبيعات أو للموجة كلها. لا توجد حزمة بناء تطبيق جديدة في هذا النطاق.

## حدود وعدم ادعاء

- `sales` ليس مكتملًا؛ لا يوجد سجل إغلاق ولا نجاح T/C/K/M موثق في هذا التسليم.
- لم تُصنّف ملفات `raw/new/` ولم تُنشأ منها معرفة نهائية.
- لم أعدّل `raw/` أو طبقات الجذر `sources/claims/concepts/masters/systems/`
  أو Skills. فهارس الأسماء المماثلة تحت `done/` فقط هي جزء من التكليف الصريح.
- لم أستخدم Codex.
- مجلدات `source_refs/` الفرعية هي نقاط استقبال/تصنيف مستقبلية فقط؛ لا تحتوي
  مصادر منقولة أو نسخًا من الـVault.
