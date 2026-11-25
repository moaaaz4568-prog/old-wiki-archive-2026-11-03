# Schema — Nexus LLM Wiki New

> هذا الملف يثبت شكل السجلات والامتدادات. ترتيب التشغيل والبوابات التفصيلية في
> [الميثاق](MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md) و[الأنظمة 13–19](systems/INDEX.md).
> الحقول الإضافية أدناه لا تستبدل الحقول القديمة ولا تغيّر enums `Source` أو `Claim`.

## هوية المساحة

- **المسار:** `/sdcard/NEXUS_LLM_WIKI/`
- **الغرض:** ويكي معرفة قابلة للتتبع والاسترجاع للنماذج اللغوية.
- **حالة المصدر:** الويكي القديمة للقراءة فقط.
- **رابط الإحالة:** مسارات ملفات نسبية من جذر هذه المساحة.

## Source

كل مصدر له سجل في `sources/`:

```yaml
type: source
source_id: SRC_YYYYMMDD_slug
title: عنوان المصدر
source_path: raw/new/original.ext
content_hash: sha256:...
media_type: transcript|article|book|conversation|code|other
language: ar|en|mixed
status: new|processed|quarantined
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

### امتدادات workflow لسجل Source

تظل قيم `status` الأصلية محصورة في `new|processed|quarantined`؛ الحالات التفصيلية
لا تُضاف إليها:

```yaml
route_status: received|reading_full|hashed|duplicate_checked|classified|uncertain|quarantined|copy_and_metadata_verified|route_done
source_extraction_status: not_started|in_progress|reviewed|complete|blocked|stale
primary_domain: sales|outreach|pricing_offers|content_strategy
primary_subdomain: <catalog-id>
route_ref: done/<domain>/<subdomain>/ROUTE_<source_id>.md
copy_ref: done/<domain>/<subdomain>/<source_id>.<ext>
snapshot_refs: [SNAP_...]
read_coverage_refs: [READ_...]
source_domain_extraction_complete:
  - domain: <domain>
    subdomain: <subdomain>
    snapshot_id: SNAP_...
    coverage_ref: READ_...
    status: complete|partial|blocked|stale
    unit_refs: [UNIT_...]
```

`source_done` ليس قيمة بديلة لـ`Source.status`: هو حكم workflow لا يثبت إلا بعد
استخراج ومراجعة **كل وحدات المصدر**. الحقل `source_domain_extraction_complete`
يسمي مساهمة مجال/قسم مكتملة أو جزئية؛ لا يحولها إلى اكتمال المصدر العام.

## Claim

كل Claim ملف مستقل في `claims/` أو سجل قابل للفهرسة بنفس الحقول:

```yaml
type: claim
claim_id: CLM_YYYYMMDD_slug_001
statement: صياغة الادعاء
evidence_type: direct_quote|reported_result|example|inference|hypothesis
source_id: SRC_YYYYMMDD_slug
locator: line 120-128|timestamp 00:12:31|section 3
scope: نطاق التطبيق
confidence: source_reported|supported|inferred|hypothetical|disputed
status: candidate|reviewed|accepted|rejected
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

الحقول التالية امتدادات تتبع لا تغيّر `evidence_type` أو `confidence` أو `status`:

```yaml
evidence_quote: الاقتباس الحرفي عند انطباقه
quote_hash: sha256:<64-hex>
quote_offset:
  unit: unicode_codepoint
  start: 0
  end: 120
  bounds: half_open
definition_refs: [DEF_...]
what_it_does_not_prove: الحد الصريح لما لا يثبته هذا الدليل
read_coverage_ref: READ_...
review_ref: REVIEW_...
```

قبل `reviewed` أو `accepted` يلزم فحص `quote_hash` و`what_it_does_not_prove`
عندما يكون Claim منقولًا أو قابلًا للاقتباس؛ المرشح قد يبقى ناقصًا إلى أن يراجع.
`quote_offset` صفري البداية ويستخدم فهرسة Unicode code points وبحدود نصف مفتوحة
`[start,end)`، لا offsets بايت أو UTF-16. يجب أن يطابق الاقتباس النص في view المرتبطة
بـ`read_coverage_ref`، وأن يكون hash قابلًا لإعادة الحساب. المثال لا يثبت قاعدة عامة.

## Concept

```yaml
type: concept
concept_id: CPT_domain_slug
title: اسم المفهوم
status: draft|reviewed|accepted|disputed|deprecated
claim_refs: [CLM_...]
source_refs: [SRC_...]
related_concepts: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

الامتدادات الاختيارية التي تحفظ مسار التعريف والقراءة:

```yaml
definition_refs: [DEF_...]
read_coverage_refs: [READ_...]
workflow_refs: [WF_...]
conflict_refs: [CLM_...]
```

الأقسام المطلوبة حسب الصلة:

1. الجوهر.
2. الآلية.
3. الشروط.
4. الحدود وحالات الفشل.
5. أمثلة موسومة.
6. التوترات والتعارضات.
7. التطبيقات.
8. سجل الأدلة.

## Master

```yaml
type: master
master_id: MSTR_domain_slug
title: اسم الماستر
status: draft|reviewed|canonical|deprecated
concept_refs: []
claim_refs: []
coverage_status: measured|partial|unknown
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

لا يُنشأ Master جديد قبل بوابة T الشاملة للمجال وفروعه في snapshot مغلقة ومراجعة
Claims/Concepts اللازمة. يمكن أن تبقى مسودة موروثة بحالة `draft` وتغطية `partial`؛
ذلك لا يرفعها إلى اعتماد ولا يثبت اجتياز البوابة.

امتدادات التتبع:

```yaml
domain: <domain>
domain_snapshot_id: DOMAIN_SNAPSHOT_...
gate_refs: [GATE_T_..., GATE_C_..., GATE_K_..., GATE_M_...]
retrieval_eval_ref: RETRIEVAL_...
workflow_refs: [WF_...]
```

## أنواع العلاقات

- `supports`: دليل يدعم Claim أو Concept.
- `contradicts`: تعارض صريح.
- `example_of`: مثال على مفهوم.
- `derived_from`: استنتاج مشتق من Claims.
- `related_to`: علاقة تنقل أو سياق.

لا تُستخدم علاقة عامة عندما تكون العلاقة الأدق متاحة.

## سجل المصطلح (Term)

المصطلح وحدة استخراج مستقلة عن Claim؛ يجوز تسجيل المرشح أثناء القراءة وقبل T، ولا
يُخلط ذلك بقبوله:

```yaml
type: term
term_id: TERM_YYYYMMDD_slug_001
domain: <domain>
subdomain: <subdomain>
snapshot_id: SNAP_...
source_id: SRC_...
source_label: لفظ المصدر
canonical_label: الاسم القياسي أو null
aliases: []
definition: تعريف تشغيلي أو null
definition_refs: [DEF_...]
definition_gap: null
scope: نطاق الاستخدام
occurrences:
  - source_id: SRC_...
    locator: chars 0:12
    quote_offset: {unit: unicode_codepoint, start: 0, end: 12, bounds: half_open}
claim_refs: [CLM_...]
status: candidate|reviewed|merged|rejected
review: {reviewer: null, decision: pending, reason: null}
merge_target: null
concept_refs: []
master_refs: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

`definition_refs` يجب أن تقود إلى مصدر وموضع أو إلى Claim مراجَع؛ لا يملأ الوكيل
التعريف بالتخمين. تشابه اللفظ وحده لا يبرر الدمج.

## تغطية القراءة (Read coverage)

هذا السجل يفصل سلامة IO عن القراءة الدلالية، ويثبت source hash وsnapshot وsegments
المتجاورة:

```yaml
type: read_coverage
coverage_id: READ_YYYYMMDD_slug
source_id: SRC_...
snapshot_id: SNAP_...
batch_id: BATCH_...
source_sha256: sha256:<64-hex>
mode: routing|extraction
io: {bytes_expected: 0, bytes_read: 0, eof_reached: true, stable_after_read: true}
view: {unit: unicode_codepoint, bounds: half_open, start: 0, length: 0, sha256: sha256:<64-hex>, parser_version: v1}
semantic_segments:
  - {segment_id: SEG_..., start: 0, end: 120, reader: agent, reviewer: reviewer, note: سياق وحدود المقطع, content_unit_ids: []}
unread_ranges: []
content_units: []
semantic_review_status: not_started|in_progress|reviewed|blocked|stale
extraction_status: not_started|in_progress|reviewed|complete|blocked|stale
```

تكون الحدود Unicode code point، صفرية، نصف مفتوحة؛ يلزم اتحاد متصل من `0` إلى
`view.length` للقراءة الدلالية الكاملة. `bytes_read == bytes_expected` وEOF يثبتان
IO فقط، ولا يثبتان الفهم أو استخراج كل الوحدات.

## سجل التوجيه والنسخة

```yaml
type: route_record
route_id: ROUTE_...
workflow_id: WF_...
source_id: SRC_...
source_path: new/<file>|raw/new/<file>
content_hash: sha256:<64-hex>
primary_route: {domain: <domain>, subdomain: <subdomain>, evidence_locators: []}
secondary_references: []
copy_path: done/<domain>/<subdomain>/<source_id>.<ext>
copy_sha256: sha256:<64-hex>
copy_independence: {bytes_equal: true, hashes_equal: true, symlink: false, hardlink: false}
route_status: route_done
source_extraction_status: not_started
snapshot_id: SNAP_...
read_coverage_ref: READ_...
```

مسار `done/<domain>/<subdomain>/` هو المسار المباشر؛ metadata لا تستبدل النسخة.
التفاصيل التشغيلية وفحوص G0–G8 في [نظام 14](systems/14_SOURCE_ROUTING_AND_DONE_TREE.md).

## Snapshot وسجل workflow والبوابة

```yaml
type: snapshot
snapshot_id: DOMAIN_SNAPSHOT_...
scope_kind: domain_snapshot|batch|delta
parent_snapshot_id: null
domain: <domain>
catalog_revision: <revision>
cutoff: YYYY-MM-DDThh:mm:ssZ
inventory_roots: [new/, raw/new/]
all_candidate_source_ids: [SRC_...]
included_source_ids: [SRC_...]
secondary_source_references: []
reviewed_exclusions: []
unresolved_candidates: []
all_subdomain_ids: [<all catalog subdomains>]
source_hashes: {}
per_source_read_coverage: {}
per_source_extraction_review: {}
terms_review: {}
delta_refs: []
inventory_complete: false
```

```yaml
type: workflow_record
workflow_id: WF_YYYYMMDD_slug
kind: intake|routing|extraction|review|gate|iteration|handoff
domain: <domain>|global_intake
snapshot_id: SNAP_...
source_ids: [SRC_...]
input_refs: []
output_refs: []
status: planned|in_progress|validated|reported|blocked|failed|partial
evidence_refs: []
```

```yaml
type: gate_record
gate: R|T|C|K|M|QA
scope: source|subdomain|domain|snapshot
domain: <domain>
snapshot_id: DOMAIN_SNAPSHOT_...
status: not_started|in_progress|pass|blocked|stale
evidence_refs: []
reviewer: null
checked_at: null
blockers: []
pending_delta_ids: []
```

حالات سجل البوابة ثابتة كما أعلاه. `not_closed`/`not_evaluated` وصفان لحالة config
أولية لا enum بديل لسجل البوابة ولا سبب لتعديل config هنا. `pass` يلزم مراجع وتاريخ
وأدلة؛ `stale` يربط delta أو تغيّر اللقطة.

## خلافات المصادر وفحص الأداة

لا يشترط consensus بين مصدرين مدعومين لاجتياز المراجعة. يحفظ الطرفان مع السياق
والشروط والثقة، وقد يكون Claim `status: reviewed` و`confidence: disputed`، أو
Concept `disputed`. الذي يمنع الاعتماد هو غياب التتبع أو التقييم أو وجود فجوة غير
معلّمة، لا مجرد وجود خلاف موثق.

`tools/wiki_quality.py` فحص بنيوي مساعد لمسارات وحقول/روابط محددة في نسخته الحالية؛
لا يُدّعى أنه يتحقق من كل امتدادات workflow، أو القراءة الدلالية، أو Unicode
half-open offsets، أو `what_it_does_not_prove`، أو بوابة T/C/K/M/QA. أي ادعاء بهذه
الفحوص يحتاج verifier أو تقريرًا منفصلًا يذكر أمره ودليله.

## سجلات التشغيل والتوثيق القابلة للملاحظة

تقتصر هذه السجلات على أربعة أنواع فقط: `decision_record` و`verification_record`
و`handoff_record` و`documentation_update_record`. تتطلب كل السجلات الحقول
`record_id` و`type` و`created_at` و`owner` و`scope` و`status` و`evidence_refs`.

### `decision_record`

يوثق قرارًا تشغيليًا أو توثيقيًا قابلًا للمراجعة، مع مبرره والبدائل التي نوقشت.

```yaml
record_id: EXAMPLE_DECISION_RECORD_ID
type: decision_record
created_at: EXAMPLE_CREATED_AT
owner: EXAMPLE_OWNER
scope: EXAMPLE_SCOPE
status: EXAMPLE_STATUS
evidence_refs:
  - EXAMPLE_EVIDENCE_REF
decision: EXAMPLE_DECISION
rationale: EXAMPLE_RATIONALE
alternatives_considered:
  - EXAMPLE_ALTERNATIVE
```

### `verification_record`

يوثق ما تم فحصه، ونطاق الفحص ونتيجته والأدلة المرتبطة به، دون استنتاجات غير
مذكورة في السجل.

```yaml
record_id: EXAMPLE_VERIFICATION_RECORD_ID
type: verification_record
created_at: EXAMPLE_CREATED_AT
owner: EXAMPLE_OWNER
scope: EXAMPLE_SCOPE
status: EXAMPLE_STATUS
evidence_refs:
  - EXAMPLE_EVIDENCE_REF
verification_target: EXAMPLE_VERIFICATION_TARGET
checks:
  - EXAMPLE_CHECK
result: EXAMPLE_RESULT
verified_at: EXAMPLE_VERIFIED_AT
```

### `handoff_record`

يوثق تسليم المسؤولية أو السياق بين مالكين، بما في ذلك الخطوات التالية والعوائق
المفتوحة.

```yaml
record_id: EXAMPLE_HANDOFF_RECORD_ID
type: handoff_record
created_at: EXAMPLE_CREATED_AT
owner: EXAMPLE_OWNER
scope: EXAMPLE_SCOPE
status: EXAMPLE_STATUS
evidence_refs:
  - EXAMPLE_EVIDENCE_REF
from_owner: EXAMPLE_FROM_OWNER
to_owner: EXAMPLE_TO_OWNER
handoff_reason: EXAMPLE_HANDOFF_REASON
next_actions:
  - EXAMPLE_NEXT_ACTION
open_blockers:
  - EXAMPLE_OPEN_BLOCKER
```

### `documentation_update_record`

يوثق تحديثًا في محتوى أو بنية التوثيق، ومكانه ونوعه وملخصه، مع الإشارة إلى
السجل السابق عند الحاجة.

```yaml
record_id: EXAMPLE_DOCUMENTATION_UPDATE_RECORD_ID
type: documentation_update_record
created_at: EXAMPLE_CREATED_AT
owner: EXAMPLE_OWNER
scope: EXAMPLE_SCOPE
status: EXAMPLE_STATUS
evidence_refs:
  - EXAMPLE_EVIDENCE_REF
document_path: EXAMPLE_DOCUMENT_PATH
change_kind: EXAMPLE_CHANGE_KIND
sections_affected:
  - EXAMPLE_SECTION
change_summary: EXAMPLE_CHANGE_SUMMARY
supersedes_record_id: EXAMPLE_SUPERSEDES_RECORD_ID
```

هذه السجلات لا تغيّر enums ‏Source/Claim/Term/Concept/Gate، ولا تكشف
chain-of-thought. كما أن `verification` و`status` هنا لا يرفعان بوابات T/C/K/M/QA
تلقائيًا؛ يبقى اجتياز كل بوابة خاضعًا لقواعدها وأدلتها المستقلة.
