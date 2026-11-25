# 14 — توجيه المصدر وشجرة `done`

**مراجعة:** 2026-10-10 — [المواءمة](../reports/sales-proof/MULTIDOMAIN_ALIGNMENT_2026-10-10.md) و[ملحق المستخدم](../reports/sales-proof/USER_MESSAGES_SESSION_EF22.md) مرجع الحسم.

> **نوع الملف:** مواصفة تشغيل لمسار الاستقبال والتصنيف والإغلاق.  
> **النطاق:** استقبال ملف من `new/`، قراءته كاملًا، تثبيت هويته، توجيهه إلى
> مجال/قسم، ثم إنشاء نسخة مصدر مستقلة متحققة وroute/reference metadata في شجرة `done/`.  
> **حدود صريحة:** هذا الملف لا ينشئ Source أو Claim أو Concept أو Master، ولا
> ينقل أو يعدّل أو يحذف أي ملف خام، ولا يستخدم Codex.

## 1. الغرض والضمانات غير القابلة للتفاوض

يحول هذا المسار «ملفًا وصل إلى صندوق الاستقبال» إلى **حالة معالجة قابلة
لإعادة التحقق**. لا تعني عملية القراءة وحدها أن المصدر صار معرفة مقبولة، ولا
تعني كتابة سجل في `done/` أن أي ادعاء داخله صحيح أو أن طبقات المعرفة اللاحقة
اجتازت بواباتها.

الضمانات:

1. **المحتوى هو أساس الهوية:** يقرأ المسار النص الكامل، ويحسب SHA-256 على
   البايتات الأصلية قبل أي تطبيع أو استخراج.
2. **الاسم ليس دليل تصنيف:** اسم الملف أو العنوان إشارة مساعدة فقط. يلزم دليل
   من متن المحتوى نفسه لتحديد المجال و`subdomain`.
3. **تكرار قابل للتتبع:** كل تطابق بصمة يسجل كـ`duplicate_of` أو كمجموعة
   تكرار، ولا يحذف المسارات أو يخفيها.
4. **مسار أساسي واحد:** لكل مصدر مقبول للتوجيه مسار `primary` واحد فقط؛ أما
   الزوايا الأخرى فتسجل كمراجع `secondary` دون نسخ المصدر إلى مجلدات متعددة.
5. **الغموض مرئي:** المصدر غير القابل للحسم يبقى `uncertain` في الاستقبال،
   ولا يُدفع إلى `done/` بالتخمين.
6. **العزل عند الخطر:** فشل القراءة، أو عدم ثبات الملف، أو فشل البصمة، أو
   مسار غير آمن يؤدي إلى `quarantine` مع سبب قابل للمراجعة.
7. **`raw/` دليل غير قابل للتغيير:** القراءة والحساب والإشارة مسموحة؛ التعديل
   وإعادة التسمية والنقل والاستبدال والحذف ممنوعة.
8. **`done/` يحتوي المصدر:** نسخة بايتية مستقلة إلزامية، لا مرجعًا وحده ولا symlink أو hardlink؛ يبقى الأصل ثابتًا.
9. **الاكتمال محدد النطاق:** `route_done` للتوجيه، و`source_done` لاستخراج كل وحدات المصدر ومراجعتها، و`domain_done` للمجال؛ لا تُختزل إلى done مبهمة.
10. **التصنيف عام:** يجوز توجيه وفهرسة ونسخ pending؛ التعميق المعرفي للمجال النشط وحده وفق `config/processing_order.json`.
11. **لا اعتماد دائري:** route_done لا ينتظر استخراجًا، وsource_done لا يحتاج Concept أو Master؛ تُربط المخرجات المرجعية لاحقًا.

## 2. خريطة المسارات

الجذر المعياري هو:

```text
/sdcard/NEXUS_LLM_WIKI/
```

| المسار | الوظيفة | السياسة |
|---|---|---|
| `new/` | صندوق استقبال الملفات الجديدة | قراءة، جرد، وبصمة؛ لا يُحذف الأصل من هنا ضمن هذا التشغيل |
| `raw/` | الدليل الخام المرجعي، ومنه `raw/new/` في البنية الحالية | immutable؛ لا تعديل أو نقل أو حذف |
| `sources/` | سجل Source وفق `SCHEMA.md` | يسجل الهوية والبصمة والحالة، ولا يستبدل الدليل |
| `staging/routing/` | سجلات التشغيل، نتائج التصنيف، وملفات الـcheckpoint | مخرجات تشغيلية قابلة للمراجعة |
| `quarantine/` | مراجع العناصر المعزولة وأسباب العزل | لا يحتوي على حذف أو نقل للدليل الأصلي |
| `done/<domain>/<subdomain>/` | نسخة المصدر المتحققة وroute/reference metadata | بعد فحوص التوجيه، لا بعد Masters |

### 2.1 التوافق مع البنية الموجودة

العقد المطلوب هنا يستقبل منطقيًا من:

```text
/sdcard/NEXUS_LLM_WIKI/new/
```

وتدعم البنية الموثقة سابقًا أصولًا تحت المسار التالي، دون إعادة جردها في هذه المراجعة:

```text
/sdcard/NEXUS_LLM_WIKI/raw/new/
```

لذلك:

- إذا كان الإدخال في `new/`، يسجل `source_path` النسبي مثل
  `new/example.txt`، وتبقى نسخة الإدخال في مكانها أثناء دورة التحقق.
- إذا كان الإدخال موجودًا أصلًا في `raw/new/`، يعامل كدليل خام للقراءة فقط،
  ويسجل `source_path` مثل `raw/new/example.txt`. لا ينقل إلى `new/` ولا يعاد
  تسميته لتوحيد الشكل.
- لا ينشئ هذا العقد alias أو symlink بين المسارين تلقائيًا. وجود مسارين لا
  يبرر عدّ المصدر مرتين؛ البصمة هي التي تحسم الهوية.
- المسار في Source أو سجل التوجيه **نسبي إلى جذر الويكي**، ولا يحتوي على
  مسار مطلق أو جزء `..`.

بهذا يصبح `new → done` نسخًا متحققًا مع metadata، لا عملية `move` للدليل ولا مجرد نقل سجل.
لا طبقة `source_refs` وسيطة: `done/<domain>/source_refs/<subdomain>/` ليست بديلًا عن المسار المطلوب.
المراجع الثانوية ونسخ SHA-256 المطابقة لا تزيد عدد المصادر المستقلة أو مقام التغطية.

## 3. الحالات والعقد بين الحالات

`route_status` هو حالة مسار التوجيه، بينما `status` في Source يظل ضمن قيم
`SCHEMA.md`: `new|processed|quarantined`. لا نضيف حالة غير معرّفة إلى عقد
Source.

```text
received
   │
   ▼
reading_full ── فشل سلامة/قراءة ──► quarantined
   │
   ▼
hashed
   │
   ▼
duplicate_checked ── هوية متضاربة/فشل بصمة ──► quarantined
   │
   ▼
classified ── تكرار مُحتمل أو لا مجال/قسم واضح ──► uncertain
   │
   ▼
copy_and_metadata_verified
   │
   ▼
route_done
```

| `route_status` | معنى الحالة | `Source.status` | مكان البقاء |
|---|---|---|---|
| `received` | دخل الجرد ولم تبدأ القراءة الكاملة | `new` | `new/` أو `raw/` كما وجد |
| `reading_full` | القراءة والبصمة قيد التنفيذ | `new` | مكان المصدر الأصلي |
| `duplicate` | بصمة مطابقة لمصدر أساسي متحقق | لا ترفع الحالة بسبب التكرار؛ تربط بسجل الأساسي | المصدر الأصلي + مرجع التكرار |
| `classified` | فُحص المحتوى وثبت مسار أساسي، ولم تُثبت مخرجات `done` بعد | `new` | المصدر الأصلي |
| `uncertain` | القراءة سليمة لكن التصنيف أو التفرد أو نطاق المجال غير محسوم | `new` | `new/` أو `raw/` دون `done/` |
| `quarantined` | مشكلة سلامة أو قراءة أو هوية تمنع المعالجة | `quarantined` | المصدر الأصلي + مرجع في `quarantine/` |
| `route_done` | فحوص التوجيه والنسخة وmetadata ناجحة | `new` حتى اكتمال استخراج المصدر | المصدر الأصلي + نسخة في `done/<domain>/<subdomain>/` |

لا توضع route_done أو source_done في `Source.status`؛ تبقى قيم SCHEMA كما هي، وتحفظ الحالات التفصيلية في metadata.
في التشغيل الجديد يرقى Source إلى processed بعد source_done؛ processed تاريخية وحدها ليست برهانًا على القراءة أو الاستخراج ولا ترحّل صامتًا.
source_done يستلزم استخراج جميع وحدات المحتوى terms/Claims بمواضعها ومراجعتها، لا وجود مخرج توليفي.
المصدر المختلط قد تكمل مساهماته في المجال النشط وتبقى وحداته الأخرى منتظرة؛ لا يسمى source_done كليًا حتى استكمالها في أدوارها.
subdomain_extraction_done يقيس مساهمات القسم في snapshot؛ لا يساوي domain_done ولا يجيز Master قبل domain_terms_complete للمجال كله.

## 4. استقبال المصدر من `new/`

لكل دفعة استقبال ينشئ `Intake/Classify Agent` معرّف تشغيل لا يتغير، مثل:

```text
ROUTE_RUN_YYYYMMDD_HHMMSS_<short-id>
```

ثم ينفذ الخطوات بالترتيب:

### 4.1 الجرد الأولي

1. يثبت الجذور الفعلية المعلنة ويجرد كل مرشحي `new/` و`raw/new/` وأي أصل مسجل داخل حدود snapshot، لا ملفات المجال النشط وحده.
2. يسجل لكل عنصر: المسار النسبي، الاسم، الامتداد، الحجم، ووقت الجرد.
3. يرفض المسار الذي يخرج من جذر الويكي، أو يحتوي `..`، أو يكون symlink إلى
   خارج الجذر. الرفض هنا `quarantined` وليس حذفًا.
4. لا يقرر المجال من هذه المرحلة. العنوان والاسم metadata للهوية، لا نتيجة
   تصنيف.
5. يربط كل مرشح قبل cutoff بـ`candidate_id` وdisposition وسبب ودليل، حتى خارج المجال أو غير المقروء؛ [نظام15](15_DOMAIN_COMPLETION_GATES.md) يحدد المقام والدفعات.
6. لا تستخدم عينة أو top-N بدل inventory شامل؛ batching للجدولة لا لتقليل مقام الإغلاق.

### 4.2 إنشاء الهوية التشغيلية

بعد تثبيت المسار، ينشئ سجل Source مبدئيًا أو يربط بالسجل الموجود، وفق الحد
الأدنى من `SCHEMA.md`:

```yaml
type: source
source_id: SRC_YYYYMMDD_slug
title: عنوان وصفي، لا يقرر المجال وحده
source_path: new/relative-file.ext
content_hash: sha256:<64-hex>
media_type: transcript|article|book|conversation|code|other
language: ar|en|mixed
status: new
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

يمكن أن يكون `source_id` عمليًا مشتقًا من التاريخ وبادئة البصمة ومميز المسار،
مثل `SRC_NEW_<hash-prefix>_<path-prefix>`, بشرط ألا يتصادم مع سجل قائم. لا
يُعاد استخدام `source_id` لمحتوى ذي بصمة مختلفة.

### 4.3 تثبيت الملف أثناء المعالجة

قبل القراءة وبعدها يقارن المسار وحجمه، وتُسجل أي دلالة على تغير الملف أثناء
المعالجة. إذا تغيّر الحجم أو محتوى الملف بين القراءة والحساب والتحقق، لا
يُخمن أي نسخة هي الصحيحة؛ النتيجة `quarantined` بسبب `source_changed_during_read`.

## 5. القراءة الكاملة وحساب البصمة

### 5.1 مبدأ واحد للهوية ومبدأ آخر للنص

- **الهوية:** SHA-256 على كل البايتات الأصلية كما وصلت، لا على عنوان الملف،
  ولا على أول جزء من النص، ولا على نص بعد إزالة المسافات.
- **القراءة الدلالية:** segments متصلة تغطي النص كاملًا مع فهم الغرض والسياق ومراجعة مواضعه. لا يكفي EOF ولا preview أو أول 30,000 محرف لإثباتها.
- **التطبيع:** يجوز إنشاء view مؤقتة للتصنيف (مثل إزالة BOM أو توحيد
  whitespace في الذاكرة)، لكن لا تُكتب فوق المصدر، ولا تستبدل `content_hash`.

### 5.2 سجل القراءة المطلوب

يسجل كل مصدر في سجل التشغيل:

```yaml
read_audit:
  mode: full
  bytes_expected: <stat-size-before>
  bytes_read: <actual-bytes-read>
  eof_reached: true
  line_count: <count-or-null>
  character_count: <count-or-null>
  encoding: utf-8
  decode_replacements: 0
  stable_after_read: true
  sha256: sha256:<64-hex>
```

هذه شروط نجاح **IO فقط**: `bytes_read == bytes_expected` وEOF وثبات الملف وعدم فقد الترميز. لا تعني فهمًا دلاليًا أو اكتشاف كل وحدات المحتوى.

### 5.3 تغطية القراءة الدلالية ووحداتها

المثال JSON يوضح الحقول فقط؛ البصمات والمواضع والملاحظات فيه fixtures لا أدلة قراءة فعلية:

```json
{
  "coverage_id": "READ_EXAMPLE", "source_id": "SRC_EXAMPLE",
  "snapshot_id": "SNAP_EXAMPLE", "batch_id": "BATCH_EXAMPLE",
  "source_sha256": "sha256:<64-hex>", "mode": "extraction", "domain": "sales",
  "io": {"bytes_expected": 180, "bytes_read": 180, "eof_reached": true, "stable_after_read": true},
  "view": {"unit": "unicode_codepoint", "bounds": "half_open", "length": 100, "sha256": "sha256:<64-hex>", "parser_version": "utf8-example", "source_mapping_ref": "MAP_EXAMPLE"},
  "semantic_segments": [
    {"segment_id": "SEG_1", "start": 0, "end": 60, "reader": "example-reader", "read_at": "2026-10-10T00:00:00Z", "reviewer": "example-reviewer", "reviewed_at": "2026-10-10T01:00:00Z", "note": "الغرض والسياق وحدود الفقرة الأولى، مثال حقل", "content_unit_ids": ["UNIT_1"]},
    {"segment_id": "SEG_2", "start": 60, "end": 100, "reader": "example-reader", "read_at": "2026-10-10T00:01:00Z", "reviewer": "example-reviewer", "reviewed_at": "2026-10-10T01:01:00Z", "note": "القيد والسياق في بقية النص، مثال حقل", "content_unit_ids": ["UNIT_2"]}
  ],
  "content_units": [
    {"unit_id": "UNIT_1", "locator": "chars 0:60", "disposition": "extracted_reviewed", "term_ids": ["TERM_EXAMPLE_001"], "claim_ids": ["CLM_EXAMPLE_001"], "review_ref": "REVIEW_EXAMPLE"},
    {"unit_id": "UNIT_2", "locator": "chars 60:100", "disposition": "non_knowledge", "term_ids": [], "claim_ids": [], "reason": "خاتمة تحريرية بلا مضمون معرفي، مثال فقط", "review_ref": "REVIEW_EXAMPLE"}
  ],
  "notes": ["ملاحظات المراجع لا تستبدل segments أو مراجعة الوحدات"],
  "unread_ranges": [], "semantic_review_status": "reviewed",
  "extraction_status": "reviewed", "concept_refs": [], "master_refs": []
}
```

- شروط semantic contiguous segments: أول start=0، وكل end يساوي start التالي، وآخر end=view.length؛ يعالج overlap للمراجعة خارج حساب التغطية ولا يُعد مرتين.
- كل segment موجب الطول ويحمل reader/وقت قراءة وreviewer/وقت مراجعة وملاحظة مضمون؛ البصمة ومواضع الاقتباس ترجع إلى view ثابتة وخريطة الأصل.
- صفحات PDF أو timestamps تحتاج parser/version وخريطة محفوظة للمواضع وتدقيق نقص النص؛ ليست بايتات الملف نصًا دلاليًا تلقائيًا.
- الملاحظات notes لا تثبت التغطية وحدها، وسجل segments بلا قراءة فعلية أو مراجعة مضمون ليس شهادة فهم.
- `mode: routing` يغطي المتن كاملًا بـsegments للتصنيف وفهم الغرض دون تعميق معرفي؛ لا يلزم استخراج Terms/Claims لمجال pending ولا يجوز بناؤها فيه.
- `mode: extraction` في المجال النشط يجمع candidate terms/Claims أثناء القراءة؛ يراجع كل تعريف وخطوة ورقم وشرط ومثال ورأي وحدّ.
- كل وحدة لها مصير مراجع: مستخرجة، مكررة برابط أصلها، غير معرفية بسبب، أو محالة لمجال آخر. الملاحظات المهمة ليست صندوق استبعاد للوحدات الصعبة.
- الإحالة الأخرى تحفظ الموضع والنطاق ولا تستخرج معرفة pending؛ source_done العام يظل جزئيًا حتى مراجعة كل مساهمات المصدر في أدوارها.
- مصطلح/Claim غير محسوم المراجعة أو فجوة semantic تمنع اكتمال الاستخراج؛ خلاف مدعوم مراجع لا يمنعه.
- حقول المرشحين والمراجعة تستوفي [13](13_MULTI_DOMAIN_ARCHITECTURE.md) و[SCHEMA](../SCHEMA.md) و[07](07_SALES_CLAIM_REVIEW.md)، دون انتظار T لتسجيلها.

### 5.4 الملفات غير النصية أو المعيبة

| الحالة | ما يمكن إثباته | القرار |
|---|---|---|
| ملف نصي UTF-8 سليم | سلامة IO؛ القراءة الدلالية تحتاج سجلها | تابع إلى dedup والقراءة والتصنيف |
| نص يحتاج replacement characters | البايتات فقط، والنص الدلالي غير كامل | `quarantined` ما لم توجد سياسة parser موثقة ومتحقق منها |
| ملف فارغ | بصمة ملف فارغ فقط | `quarantined: empty_source` |
| امتداد غير معروف/ملف ثنائي | البصمة قد تكون سليمة لكن لا يوجد نص قابل للقراءة | `quarantined: unsupported_text` |
| خطأ I/O أو EOF مفقود | لا يمكن إثبات اكتمال القراءة | `quarantined: incomplete_read` |

لا يكفي تسجيل `content_hash` لتسميـة مصدر غير مقروء `processed`: البصمة تثبت
هوية البايتات، لا صلاحية قراءة النص.

## 6. كشف التكرار

### 6.1 نطاق المقارنة

يقارن المسار البصمة مع:

1. كل عناصر دفعة الاستقبال الحالية.
2. Source records القائمة، مع إعادة التحقق من الملف المشار إليه إذا كان ذلك
   ممكنًا.
3. manifests السابقة في `staging/manifests/`.
4. أي route/reference موجود في `done/`.

سجل Source قديم يشير إلى مسار مفقود لا يكفي وحده لإثبات duplicate؛ يسجل
`stale_reference` ويذهب إلى مراجعة الهوية بدل دمج المصدرين بالتخمين.

### 6.2 نتائج dedup

| النتيجة | القاعدة | الإجراء |
|---|---|---|
| `unique_hash` | لا توجد بصمة مطابقة | أنشئ مسارًا أساسيًا بعد التصنيف |
| `exact_duplicate` | SHA-256 مطابق حرفيًا | اختر مصدرًا أساسيًا وسجل `duplicate_of` لكل نسخة |
| `same_name_new_hash` | الاسم واحد والبصمة مختلفة | مصدران مختلفان؛ لا يدمجان |
| `possible_normalized_duplicate` | التشابه بعد تطبيع/مقارنة دلالية | لا دمج تلقائي؛ `uncertain` حتى يراجع |
| `identity_conflict` | `source_id` واحد مع بصمتين أو مسارين متعارضين | `quarantined` بسبب تعارض الهوية |

اختلاف البصمة يميز المحتوى، لكنه لا يثبت استقلال الدليل؛ النسخ المترجمة أو المشتقة تحفظ provenance والعلاقة بالأصل إن كانت معلومة.

### 6.3 اختيار المصدر الأساسي

عند التكرار الحرفي، يختار النظام الأساسي بصورة حتمية:

1. سجلًا قائمًا يمكن التحقق من ملفه وبصمته، إن وجد.
2. وإلا، أقدم عنصر مسجل في الدفعة.
3. عند التعادل، المسار النسبي المرتب معجميًا.

لا تحذف النسخ التابعة. يسجل كل منها `duplicate_of: <primary-source-id>`،
ويسجل كذلك `duplicate_paths` عند الحاجة. لا تعاد معالجة المحتوى المكرر
كمحتوى مستقل، ولا تنشأ له Claims مستقلة في هذا المسار.

## 7. ترشيح المجال و`subdomain` من المحتوى

### 7.1 قاموس المجالات التشغيلي

المجالات والأقسام تؤخذ من `config/domain_catalog.json` وفق [18](18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md).
الجدول أمثلة labels فقط، لا حصر catalog قائم ولا أمر بإنشاء أقسام جديدة:

| `domain` | أمثلة `subdomain` تشغيلية |
|---|---|
| `sales` | `discovery_diagnosis`, `sales_call`, `objection_handling`, `negotiation` |
| `outreach` | `cold_email`, `linkedin_outreach`, `lead_generation`, `deliverability` |
| `pricing_offers` | `pricing`, `packaging`, `discounts_guarantees`, `value_proposition` |
| `content_strategy` | `audience_research`, `content_planning`, `storytelling_hooks`, `distribution_analytics` |

catalog عقد إلزامي لا إضافة اختيارية لاحقة. لا ينشئ الوكيل قسمًا أو مجالًا غير مسجل؛ يقدم اقتراحًا للمالك ويبقي الحالة uncertain حتى القرار.
دعم price objections داخل sales؛ تصميم السعر والباقات داخل pricing_offers. المصطلح المشترك لا يحدد الملكية بمفرده.
قراءة التصنيف عامة وpending انتظار فقط؛ حالة التنفيذ تُقرأ من `config/processing_order.json` لا تُنسخ إلى catalog.

### 7.2 عائلات الأدلة

يقرأ الوكيل النص الكامل ويستخرج إشارات من أكثر من عائلة مستقلة:

1. **موضوع المتن:** المصطلحات والعبارات المتكررة في الفقرات، لا كلمة منفردة.
2. **الغرض العملي:** ما المشكلة أو المهمة التي يشرحها المصدر فعلًا؟
3. **البنية:** عناوين وأقسام وتسلسل خطوات يثبت أن الموضوع مركزي لا عابر.
4. **الأفعال والكيانات:** من يفعل ماذا، وعلى أي مرحلة من العملية؟
5. **الحدود والسياق:** ما الذي يستبعده المصدر أو يذكره كموضوع جانبي؟

العنوان واسم الملف عائلة سادسة منخفضة الوزن. يجوز أن يقترحا مرشحًا، لكن لا
يجوز أن يكونا الدليل الوحيد. لا يكفي مثلًا وجود كلمة `offer` في اسم الملف
لتوجيهه إلى `pricing_offers` إذا كان متن المصدر يشرح عملية أخرى.

### 7.3 قاعدة القرار

يسجل سجل التصنيف لكل مرشح:

```yaml
candidate:
  domain: <domain>
  subdomain: <subdomain>
  confidence: high|medium|low
  evidence:
    - family: body_terms|purpose|structure|actions|scope
      locator: line <start>-<end>|char <start>-<end>
      note: سبب قابل للفحص
  negative_evidence: []
```

ويطبق القواعد التالية:

- يلزم سند للغرض وسند للسياق/البنية من المتن بمواضعهما؛ يجوز اجتماعهما في مقطع قصير واضح. هذه جوانب تصنيف لا «مصادر مستقلة» أدليًا.
- يجب أن يكون `primary` هو الغرض الغالب للمصدر، لا أول موضوع ذكره النص.
- إذا تساوى مرشحان، أو كان الدليل الوحيد عنوانًا/اسمًا، أو كان المتن قصيرًا
  بحيث لا يثبت الغرض، فالنتيجة `uncertain`.
- يجوز للمرشح ذي الثقة المتوسطة أن يصبح `primary` فقط إذا كان الفارق عن
  المرشح التالي واضحًا ومسجلًا مع مواضع الدليل؛ وإلا يبقى `uncertain`.
- لا تستخدم نسبة أو عتبة عددية غير معايرة كحقيقة عامة. إذا استُخدم score
  داخلي، يسجل الإصدار والعتبة والعينة التي عايرته في checkpoint.

### 7.4 `primary route` و`secondary references`

`primary_route` هو زوج واحد لا يتكرر:

```yaml
primary_route:
  domain: <domain>
  subdomain: <subdomain>
  confidence: high|medium
  rationale: الغرض الغالب كما ظهر في المتن
  evidence_locators: [line <...>, char <...>]
```

أما `secondary_references` فهي قائمة صفرية أو أكثر، ولا تعني نسخ المصدر أو
تكرار هويته. تُجدول مساهمات كل مجال في دوره فقط، وقد تحتاج استخراج وحدات مختلفة من نفس المصدر. لكل مرجع:

```yaml
secondary_references:
  - domain: <domain>
    subdomain: <subdomain>
    source_id: <same-primary-source-id>
    primary_route_ref: done/<primary-domain>/<primary-subdomain>/REF_<source_id>.json
    reference_type: contextual|supporting|contrast
    confidence: medium|low
    rationale: لماذا توجد صلة ثانوية
    evidence_locators: [line <...>]
```

قواعدها:

1. لا يوضع المصدر في أكثر من مجلد أساسي.
2. المرجع الثانوي يحمل نفس `source_id` وroute الأساسي ومواضع مساهمته، ولا يكرر البايتات أو يُحسب دليلًا مستقلًا.
3. لا يتحول المرجع الثانوي إلى Claim أو Concept تلقائيًا.
4. إن لم توجد صلة ثانوية مدعومة، تكون القائمة `[]` بدل ملئها للتجميل.

## 8. `uncertain` و`quarantine`

### 8.1 `uncertain`

هي حالة **سليمة تقنيًا وغير محسومة دلاليًا**. أمثلتها:

- المحتوى يجمع مجالين بالتساوي ولا يوجد غرض غالب.
- المرشح مبني على الاسم لا على متن قابل للإحالة.
- يوجد `possible_normalized_duplicate` لم يحسمه مراجع.
- المجال أو `subdomain` غير موجود في catalog الموجة الحالية.
- المصدر مقروء لكن النص قصير أو مبتور المعنى دون فشل I/O مثبت.

إجراء الحالة:

1. يبقى المصدر في `new/` أو في موضعه الخام دون نقل.
2. يبقى Source `status: new`، ويسجل `route_status: uncertain`.
3. يكتب سجلًا في `staging/routing/` يبين المرشحين والأدلة الناقصة.
4. لا ينشئ مجلد `done` ولا يضع نسخة نهائية داخله.
5. يعاد إلى الطابور بعد قرار بشري أو وصول سياق جديد، مع إبقاء البصمة
   الأصلية وعدم إعادة استخدام قرار قديم على محتوى متغير.

### 8.2 `quarantine`

هي حالة **فشل يمنع الاعتماد على القراءة أو الهوية**. من أسبابها:

- `source_changed_during_read`.
- `incomplete_read` أو خطأ I/O.
- ترميز غير قابل للقراءة دون سياسة استعادة موثقة.
- ملف فارغ أو ثنائي غير مدعوم.
- مسار خارج الجذر أو symlink غير آمن.
- فشل SHA-256 أو تعارض `source_id`.
- سجل يشير إلى مصدر غير موجود ولا توجد نسخة يمكن التحقق منها.

إجراء الحالة:

1. لا ينقل الوكيل الملف الأصلي إلى `quarantine/` ولا يحذفه.
2. ينشئ **مرجع عزل** فقط، مثل `quarantine/<source_id>.md`، يحوي المسار
   النسبي، البصمة إن توفرت، السبب، وقت العزل، وآخر فحص.
3. يسجل Source `status: quarantined` و`quarantine_reason`.
4. يمنع `primary_route` و`done_artifact` حتى تُحل المشكلة وتُعاد القراءة من
   الملف نفسه أو من نسخة جديدة ذات `source_id` وبصمة جديدة.

العزل ليس وسيلة لإخفاء مصدر ضعيف الصلة أو نسخة مكررة أو رأي مخالف مدعوم؛ تلك حالات تصنيف أو dedup أو مراجعة وتظل مرئية.
`pending` ليس quarantine ولا uncertain بذاته. المجال المنتظر يمكن أن يحقق route_done؛ تعميق معرفته فقط هو المقفل.

## 9. النسخة المستقلة الإلزامية وmetadata في `done/`

### 9.1 شكل الشجرة

بعد فحوص التوجيه المحلية، لا بوابات التوليف، يكون الناتج في مسار أساسي واحد:

```text
done/
  <domain>/
    <subdomain>/
      INDEX.md
      ROUTE_<source_id>.md
      REF_<source_id>.json
      <source_id>.<ext>                # نسخة مستقلة إلزامية
      duplicates/                     # اختياري للتكرارات التابعة
        DUP_<source_id>.md
```

`INDEX.md` فهرس محلي يشرح وظيفة كل ملف وحالته ومصدره. وجود سجل route لا
يغني عن فهرسة مجلد `done` عند تنفيذ العملية الفعلية.

### 9.2 route/reference metadata ملازمة للنسخة

`REF_<source_id>.json` metadata نصية وليست symlink ولا بديلًا عن النسخة. المثال حقول توضيحية لا سجلًا فعليًا:

```json
{
  "schema_version": 1,
  "artifact_kind": "verified_source_copy_reference",
  "source_id": "SRC_EXAMPLE",
  "candidate_id": "ITEM_EXAMPLE",
  "snapshot_id": "SNAP_EXAMPLE",
  "catalog_revision": "example-v1",
  "source_path": "new/example.txt",
  "content_hash": "sha256:<64-hex>",
  "primary_route": {"domain": "sales", "subdomain": "objection_handling", "rationale": "معالجة اعتراض مشترٍ على السعر", "evidence_locators": ["line 1-4"]},
  "secondary_references": [],
  "duplicate_of": null,
  "copy_path": "done/sales/objection_handling/SRC_EXAMPLE.txt",
  "copy_sha256": "sha256:<64-hex>",
  "copy_policy": "verified_copy_required",
  "verification_policy": "independent_byte_exact",
  "copy_verification": {"hashes_equal": true, "bytes_equal": true, "symlink": false, "same_inode": false, "original_unchanged": true},
  "reading_coverage_ref": "READ_ROUTE_EXAMPLE",
  "route_status": "route_done",
  "source_extraction_status": "not_started",
  "reviewer": "example-reviewer",
  "verified_at": "2026-10-10T00:00:00Z",
  "concept_refs": [], "master_refs": [],
  "raw_mutation": false
}
```

شروط المرجع:

- `source_path` نسبي، داخل جذر الويكي، ولا يحتوي `..`.
- يعاد حساب البصمة من المصدر قبل إغلاق المرجع وتطابق القيمة المسجلة.
- لا يشير إلى مسار مؤقت أو إلى ملف سيحذف بعد التشغيل.
- لا يستعمل absolute path أو symlink لتجاوز فحص المسار.
- `secondary_references` عند وجودها تحمل `source_id`, `primary_route_ref`, `domain`, `subdomain`, السبب والمواضع؛ نفس المصدر لا يُعد مرتين.
- حالات النسخة والتوجيه والاستخراج منفصلة، وحقول review/verification تملأ بنتائج فعلية عند التنفيذ لا بنقل المثال.

### 9.3 إنشاء النسخة والتحقق من استقلالها

السياسة الوحيدة `verified_copy_required`: ينشئ الوكيل نسخة بايتية فعلية مباشرة تحت `done/<domain>/<subdomain>/`، ثم:

1. ينسخ دون أي تحويل ترميز أو تطبيع.
2. يحسب SHA-256 للنسخة.
3. يقارنها بالبصمة الأصلية، ويثبت `copy_hash_matches: true`.
4. لا يستبدل نسخة قائمة؛ تعارض الاسم أو البصمة يوقف الإغلاق.
5. يترك المصدر الأصلي في `new/` أو `raw/` دون نقل أو حذف أو تعديل.
6. يفحص lstat ومسار الوجهة الحقيقي ويرفض symlink؛ يقارن `(st_dev, st_ino)` ويرفض hardlink مع الأصل، ولا يختلق فحص استقلال إذا لم تدعمه المنصة.
7. يراجع مطابقة البايتات والحجم وبصمة الأصل قبل/بعد النسخ؛ يسجل أداة الفحص والوقت والنتيجة. فشل أي منها يمنع route_done.
8. إعادة التشغيل تتحقق من النسخة القائمة ثم تعيد استخدامها إذا تطابقت؛ اختلافها finding، لا إذن overwrite ولا إنشاء primary ثانٍ.

النسخة في done لنفس هوية المصدر وليست مصدرًا مستقلًا جديدًا. REF وحده لا يحقق العقد، ولا ينتظر إنشاء النسخة أي Master أو Concept.

### 9.4 سجل route

`ROUTE_<source_id>.md` يثبت القرار لا المعرفة المستخرجة. الحد الأدنى:

- `source_id`, `source_path`, `content_hash`.
- نتيجة IO وأعداد البايتات/الأسطر/الاستبدالات، ومرجع semantic_segments ومراجعها الدلالية بشكل مستقل.
- حالة dedup و`duplicate_of` إن وجدت.
- `primary_route` وأدلة التصنيف بمواضعها.
- `secondary_references` وسبب كل مرجع.
- مسار النسخة المستقلة وبصمتها ونتيجة استقلالها، ومسارات route/reference metadata.
- حالات G0–G8 ووقت تنفيذها.
- ملاحظات الحدود، والفجوات، واسم/دور الوكيل المنفذ.

لا يحتوي route record على Claim أو Concept أو Master، ولا يرفع حالة أي طبقة
معرفية لاحقة. هذا لا يمنع القارئ الاستخراجي في المجال النشط من تسجيل candidate Claims في سجلاتها أثناء القراءة.

### 9.5 التكرار داخل `done`

لا ينشئ duplicate نسخة معرفية ثانية. بعد route_done للمصدر الأساسي، لا انتظار source_done أو Master، يمكن وضع:

```text
done/<primary-domain>/<primary-subdomain>/duplicates/DUP_<duplicate-id>.md
```

وهو مرجع يقول: `duplicate_of`, المسار الأصلي، البصمة، ومسار route الأساسي.
إذا لم يُحسم مسار المصدر الأساسي، يبقى duplicate في `new` بحالة `uncertain`.

## 10. شكل سجلات Source وroute

المثال التالي **قالب توضيحي** للحقول، وليس سجل مصدر فعليًا:

```yaml
---
type: source
source_id: SRC_YYYYMMDD_example
title: عنوان لا يكفي للتصنيف
source_path: new/example.txt
content_hash: sha256:<64-hex>
media_type: other
language: mixed
status: new
created: YYYY-MM-DD
updated: YYYY-MM-DD
route_status: route_done
source_extraction_status: not_started
primary_domain: <domain>
primary_subdomain: <subdomain>
duplicate_of: null
read_mode: full
bytes_read: <n>
decode_replacements: 0
done_artifact: done/<domain>/<subdomain>/SRC_YYYYMMDD_example.ext
reference_metadata: done/<domain>/<subdomain>/REF_SRC_YYYYMMDD_example.json
copy_policy: verified_copy_required
---
```

الحقول الإضافية لا تلغي الحقول الإلزامية في `SCHEMA.md`. في حالة `uncertain`
يبقى `status: new` و`route_status: uncertain` ولا يُملأ `done_artifact`. في
حالة `quarantined` يلزم `quarantine_reason` ولا يُملأ `primary_domain` على
أنه قرار نهائي.

## 11. سجل المخرجات لكل تشغيل

يحفظ التشغيل في `staging/routing/`، دون كتابة المحتوى الخام في السجل:

### 11.1 سجل العناصر

```text
ROUTE_RUN_<run-id>.jsonl
```

سطر واحد لكل عنصر، بالحقول التالية:

```json
{
  "run_id": "ROUTE_RUN_<...>",
  "source_id": "SRC_<...>",
  "intake_path": "new/<...>",
  "source_path": "new/<...>",
  "bytes_expected": 0,
  "bytes_read": 0,
  "eof_reached": false,
  "semantic_reading_coverage_ref": null,
  "sha256": "sha256:<...>",
  "duplicate_state": "not_checked",
  "duplicate_of": null,
  "primary_route": null,
  "secondary_references": [],
  "route_status": "received",
  "source_extraction_status": "not_started",
  "done_artifact": null,
  "checks": {"G0": "NOT_RUN", "G1": "NOT_RUN"},
  "errors": []
}
```

### 11.2 الملخص والـcheckpoint

ينشئ التشغيل أيضًا:

- `ROUTE_RUN_<run-id>_summary.json`: عدد العناصر المستلمة، المقروءة كاملًا،
  البصمات الفريدة، exact duplicates، uncertain، quarantined، primary routes،
  route_done، مجموع البايتات، ونجاح IO والتغطية الدلالية وفحوص النسخ كلٌّ منفصل؛ لا تسمية full_reads من EOF وحده.
- `ROUTE_RUN_<run-id>_checks.md`: جدول G0–G8، الأمر/الأداة، النتيجة، ومسار
  الدليل الناتج.
- checkpoint في `checkpoints/` يربط رقم التشغيل بالمخرجات، ويبين ما بقي في
  `new/` وما عُزل ولماذا. لا يكتب checkpoint ادعاءات عن محتوى لم يقرأه.

### 11.3 ما لا يسجل

- لا يسجل الملخص أن `done` اكتمل بمجرد وجود عدد من الملفات.
- لا يسجل Claim أو Concept أو Master ضمن مخرجات هذا المسار.
- لا يكتب نص المصدر الكامل داخل manifest إلا إذا كانت سياسة منفصلة صريحة
  تسمح بذلك؛ المرجع والبصمة ومواضع الدليل تكفي للتتبع.

## 12. بوابات الفحص

هذه فحوص R المحلية للتوجيه، وليست بديلًا عن R/T/C/K/M/QA للمجال في [15](15_DOMAIN_COMPLETION_GATES.md).
لا يختم route_done إلا بمرور كل فحص إلزامي؛ المراجع الثانوية يمكن أن تكون `[]` صريحة، لا N/A للقراءة أو النسخة.

| البوابة | الفحص | دليل النجاح |
|---|---|---|
| G0 الهوية والمسار | Source ID فريد، path نسبي، بلا traversal | سجل Source + نتيجة path check |
| G1 سلامة IO | EOF، `bytes_read == bytes_expected`، ثبات الملف | `read_audit`، لا برهان فهم |
| G2 البصمة | SHA-256 يحسب من كل البايتات | تطابق hash قبل/بعد |
| G3 التكرار | فحص الدفعة والسجلات و`done` | `duplicate_state` و`duplicate_of` |
| G4 القراءة الدلالية والصلة | segments متصلة + مراجعة الغرض والسياق | semantic coverage وlocators قابلة لإعادة القراءة |
| G5 المسار الأساسي | زوج domain/subdomain واحد في catalog | `primary_route` صالح |
| G6 المراجع الثانوية | كل مرجع له سبب وموضع، أو `[]` | `secondary_references` |
| G7 نسخة مستقلة وmetadata | byte-exact، لا symlink/hardlink، path/hash صحيحان | النسخة إلزامية + REF وROUTE والتحقق من الأصل |
| G8 سلامة الخام والفهرسة | raw inventory قبل/بعد متطابق، وفهرس done محدث | تقرير المقارنة + `INDEX.md` المحلي |

الفشل في G0–G3 أو G7–G8 يمنع `route_done`. الفشل في G4–G6 مع بقاء القراءة
والبصمة سليمتين ينتج `uncertain`، لا تخمينًا ولا مسارًا وهميًا.
نجاحها لا يمنح source_done: يلزمه حصر كل وحدات المحتوى واستخراج terms/Claims ومراجعتها؛ المفاهيم والماستر ليست شروطًا له.

## 13. فحوص عملية مقترحة

الفحوص التالية runbook لتكليف تنفيذي لاحق، وليست أوامر شُغلت في مراجعة2026-10-10. لا بناء مصادر هنا:

1. **فحص عقد الويكي العام:**

   ```bash
   python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py \
     --vault /sdcard/NEXUS_LLM_WIKI --json
   ```

   أمر موثق سابقًا للفحص البنيوي؛ على المنفذ التحقق من واجهته وقراءاته الحالية ضمن صلاحياته.
   حتى نجاح فحص schema لا يكفي لإغلاق G0–G8 أو لإثبات القراءة الدلالية والتغطية الشاملة.

2. **فحص شجرة route:** يقرأ verifier مستقل كل `ROUTE_RUN_*.jsonl` وملفات
   `done/**/REF_*.json`, ويتحقق من أن كل route نهائي له Source واحد، وأن
   `source_path` نسبي، وأن النسخة الفعلية مستقلة ومطابقة للأصل وبصمة المرجع، وأن كل `secondary` يحمل نفس هوية المصدر وله locator.

3. **فحص القراءة:** يفصل IO عن semantic_segments، ويتحقق من اتحاد الحدود بلا فجوات ومن ملاحظات المحتوى والمراجعة وخريطة النص إلى الأصل.
   إعادة حساب hash أو قراءة الملف بالبرنامج لا تثبت الفهم؛ extraction يحتاج مراجعة كل content unit لا Claim واحدة لكل ملف.

4. **فحص `raw`:** ينشئ verifier جردًا قبل التشغيل وبعده (`relative path`,
   `size`, `sha256`) باستخدام `os.walk`، ويقارن المجموعات مساواة تامة. أي
   إضافة أو حذف أو تغيير في `raw/` أثناء التشغيل فشل قاسٍ؛ لا يخفى بإعادة بناء
   manifest.

5. **فحص عدم الاعتماد على الاسم:** يستخدم عينة اختبارية فيها اسم مضلل ومتن
   واضح، ويثبت أن القرار يتبع المتن. كما يستخدم عينة متنها متعادل لإثبات
   إنتاج `uncertain` بدل اختيار أول مرشح.

## 14. حدود الأدوات والسياق التاريخي

الملاحظات التالية سُجلت في إعداد2026-10-09؛ لم يُعد فحص الأدوات أو corpus في مراجعة2026-10-10، فلا تُعامل وصفًا مثبتًا لنسختها الحالية:

- لوحظ وقت الإعداد أن `tools/bulk_ingest.py` يقرأ من `raw/new/` ويحسب SHA-256 للبايتات،
  يجمع التطابقات، ويكتب Source manifests. لكنه يستعمل اسم الملف مع أول جزء
  محدود من النص في `themes`، ولا ينفذ قراءة توجيه كاملة إلى
  `done/<domain>/<subdomain>/`؛ لذلك هو **استقبال/جرد أولي** وليس verifier لهذا
  الملف.
- خيار `--no-write` في `bulk_ingest.py` لا يجب وصفه بأنه dry-run كامل قبل
  التحقق، لأن النسخة المفحوصة آنذاك تنشئ مجلدات `sources/` و`staging/manifests/` قبل
  فحص العلم. لا يستخدم في اختبار «صفر آثار» دون عزل أو إصلاح منفصل.
- لوحظ وقت الإعداد أن `tools/wiki_quality.py` يتحقق من مجلدات المعرفة الأربعة ومسارات Source
  وبصماتها والروابط، لكنه لا يقرأ شجرة `done/` ولا يختبر اعتماد التصنيف على
  المتن. لذلك نجاحه شرط مساعد، وليس إثباتًا لمسار G4–G8.
- إذا وجدت سجلات قديمة تشير إلى ملفات خام مفقودة، يجب تسجيلها كفجوة أو
  quarantine/uncertain وفق سببها، لا إعادة إنشاء الدليل أو حذف السجل لإخفاء
  الفشل.

هذه الملاحظات لا تغيّر أي أداة أو سجل؛ هي حدود يجب أن تظهر في خطة التنفيذ
والـcheckpoint.

## 15. مثال عام داخل `examples` — غير معرفي

> **هذا مثال على شكل القرار فقط، وليس قاعدة عامة، ولا يضيف Domain أو
> Subdomain إلى الـcatalog، ولا ينتج Source/Claim/Concept/Master فعليًا.**

### 15.1 مثال يمكن حسمه

ملف `item-17.txt` يشرح سؤال المشتري عمّا يقارنه قبل الرد على «السعر غالٍ»؛ الغرض محادثة اعتراض لا تصميم سعر.
تصنيفه التوضيحي sales/objection_handling إذا كان مسجلًا في catalog، مع مواضع سبب التصنيف، ثم نسخة المصدر نفسها وmetadata تحت مساره المباشر.
إذا شرح بدلًا منه اختيار نموذج الاشتراك وحدود الباقات، فالغرض pricing_offers؛ لا تقرره كلمة «السعر» وحدها.
وجود إشارات من الغرضين يستلزم primary مدعومًا وsecondary بنفس الهوية؛ التعادل يبقي uncertain.
مصدر outreach واضح أثناء نشاط sales يجوز توجيهه ونسخه، لكنه يبقى pending معرفيًا لا quarantined.

### 15.2 مثال غامض ومعيب

- ملف اسمه `final.txt`، والمتن يقسم المساحة بالتساوي بين عمليتين ولا يثبت
  غرضًا غالبًا: `route_status: uncertain`، ويبقى في `new/`.
- ملف اسمه `data.bin`، تعذر تمثيل محتواه كنص كامل: `route_status: quarantined`
  مع `quarantine_reason: unsupported_text`. لا تنقل أي من الملفين
  ولا تحذفهما.

## 16. سجل مراجعة2026-10-10 والتحقق المستقبلي

- قُرئت نسخة النظام السابقة كاملة (766 سطرًا) قبل التعديل، مع AGENTS وSCHEMA والأنظمة السابقة ذات الصلة.
- استُبدلت سياسة reference-only/النسخة الاختيارية بسياسة نسخة مستقلة إلزامية وmetadata؛ لم تبق السياسة القديمة خيارًا فعالًا.
- فُصلت route_done عن source_done وعن domain_done، وIO EOF عن semantic contiguous segments والملاحظات.
- ثبت intake العام وcatalog والحالة الواحدة، مع قفل استخراج pending وجمع المرشحين أثناء قراءة النشط.
- أبقيت ملاحظات حدود الأدوات كسياق تاريخي، لا نتائج تحقق حديثة؛ أعداد المعرفة القديمة ليست دليلًا لهذه المراجعة.
- هذه المراجعة عقود فقط؛ لا تشغيل intake أو بناء مصادر أو تعديل config/done/Skills/معرفة/raw ولا subagents.
- تقرير الملفات وفحص الارتداد والروابط وLSP: [تقرير الأنظمة v3](../reports/sales-proof/agent-general-systems-v3.md).

عند التنفيذ المخوّل يسجل المنفذ أعدادًا مقاسة منفصلة: جميع المرشحين ومصائرهم، IO الناجح، semantic coverage، البصمات الفريدة، التكرارات، النسخ المتحققة، route_done، والاستخراج المراجع.
يلزم `raw_changed=0` ونسخة مستقلة مطابقة لكل مصدر ذي primary؛ لا يُحسب عدد REF إثباتًا لوجودها.
لا PASS عامًا إن غاب فاحص التوجيه/النسخ أو بقي مرشح مؤثر بلا قرار أو اقتصر الاختبار على preview/EOF.
الوصول الجديد يطلق delta وstale وفق [19](19_NEW_SOURCE_REPROCESSING.md)، لا ترحيلًا صامتًا أو فتح مجال معرفي ثانٍ.

---

**الخلاصة التشغيلية:** اقرأ المصدر كاملًا من `new/` (أو أشر إلى موضعه الخام
القائم)، احسب بصمته من البايتات، اكشف التكرار، صنّفه من المتن، اختر مسارًا
أساسيًا واحدًا وسجل المراجع الثانوية، أبق الغموض uncertain والخطر معزولًا بسبب مستقل، ثم أنشئ نسخة مستقلة متحققة وmetadata في `done/<domain>/<subdomain>/`.
يبقى الأصل ثابتًا؛ route_done لا يعني source_done، ولا يحتاج source_done Master، ولا يبدأ أي Master قبل domain_terms_complete لكل المجال.
