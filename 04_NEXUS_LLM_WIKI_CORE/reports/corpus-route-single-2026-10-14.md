# تقرير توجيه corpus — `ROUTE_BATCH_2026-10-14_002`

## الحكم والنطاق

قُرئ المصدر المحدد قراءة توجيهية كاملة حتى EOF، مع مطابقة الحجم والبصمة وإعادة القراءة، ثم سُجّل قرار primary مبني على متن المصدر ومواضع Unicode قابلة لإعادة الفحص. هذه **batch=1 فقط وليست snapshot كاملة**؛ لا تغلق مصدرًا أو subdomain أو domain، ولا تنشئ نسخة في `done/` أو `REF_` أو `ROUTE_<source_id>` نهائية.

الملف التنفيذي للدفعة هو:

```text
collections/corpus/route_batches/ROUTE_BATCH_2026-10-14_002.json
```

ولا تُستخرج في هذه المهمة Terms أو Claims أو Concepts أو Masters. بقيت **بقية 2,540 سجلًا** في `manifest.jsonl` غير مقروءة دلاليًا؛ لا تمثل هذه الدفعة snapshot للمقام العام.

## هوية المصدر وقراءة EOF

| الحقل | القيمة المتحققة |
|---|---|
| `source_id` | `SRC_CORPUS_raw_new_75f570aaf3a23086_89904437aa8b` |
| `source_path` | `raw_new/ Speed in Momentum.txt` |
| ملاحظة الاسم | يوجد **مسافة افتتاحية** قبل `Speed`، وحُفظت في المسار والقراءة دون تطبيع |
| manifest line | 1 |
| bytes expected/read | `10,607 / 10,607` |
| UTF-8 code points | `6,069` |
| lines / line ending | `1` / `none` |
| EOF | PASS |
| إعادة القراءة | `bytes_equal_on_reread=true`, `stable_after_read=true` |
| manifest SHA-256 | `sha256:75f570aaf3a23086263ffaed84ee50c001dffd3c7414d3f8f04b7ec630c6ff9b` |
| SHA-256 المعاد حسابه | مطابق تمامًا |
| decode replacements | `0` |

قراءة المصدر تمت بالبايتات الأصلية عبر المسار الفعلي:

```text
/sdcard/NEXUS_LLM_WIKI/raw/new/ Speed in Momentum.txt
```

ولم يُستخدم اسم الملف وحده في القرار.

## التكرار والهوية

فُحص `manifest.jsonl` كاملًا: **2,541 سجلًا JSON**. وُجدت بصمة المصدر في سجلين:

1. line 1: المصدر المحدد في `raw_new`، و`duplicate_of=null`؛ هو primary المحدد لهذه الدفعة.
2. line 1832: `SRC_CORPUS_nexus_brain_brain_75f570aaf3a23086_368e922a6ac6`، المسار `nexus_brain_brain/processed/ Speed in Momentum.txt`، ومربوط في manifest بـ`duplicate_of` إلى المصدر الأساسي.

هذه المجموعة حجمها 2، لكن `independent_evidence_count=1`. لم تُقرأ النسخة المكررة دلاليًا في هذه المهمة ولا تُحسب مصدرًا مستقلًا ثانيًا. كما أن `source_id` المحدد **غير موجود** في سجلات `ROUTE_BATCH_2026-10-14_001` الخمسة.

## قرار المسار

### Primary: proposal-only

```text
candidate domain:    entrepreneurship_mindset
candidate subdomain: goal_setting_and_momentum
catalog status:      proposal_only_not_in_current_config
confidence:          medium
route status:        classified (provisional batch only)
```

الزوج المرشح موجود في مقترح المجالات غير المعتمد، وليس في `config/domain_catalog.json` الحالي الذي يحوي فقط:

```text
sales · outreach · pricing_offers · content_strategy
```

لذلك سُجل المرشح كـ`proposal_only` دون إضافة domain أو subdomain إلى catalog، ودون اعتباره `route_done` نهائيًا.

الغرض الغالب الذي يثبته المتن هو بناء زخم المؤسس: البدء الآن بدل التأجيل، التعلم بعد الفعل، تقليل التشتت، ثم استخدام الأخطاء والفشل كخطوات تقدم. هذا أقرب إلى `entrepreneurship_mindset/goal_setting_and_momentum` من أي زوج حالي. وجود إرسال emails أو خدمة أو business model هو سياق تطبيقي داخل القصة، لا مركز المصدر.

### أدلة primary الموضعية من المتن

المواضع صفرية البداية وبحدود نصف مفتوحة `[start,end)` بوحدة Unicode code point، و`line 1` مساعد فقط:

| العائلة | الموضع | الاقتباس الحرفي | دلالة التوجيه |
|---|---:|---|---|
| purpose | `chars 0:53; line 1` | «أريد أن أخبركم عن درس مهم جداً لعراقب السبيد والسرعة.» | افتتاح صريح بدرس السرعة والزخم في بناء البزنس. |
| purpose | `chars 206:277; line 1` | «السرعة مهمة ليست فكرة أن تقوم بشيء بكرواتة.  السرعة ليست معناها كرواتة.» | السرعة مبدأ تنفيذ مستمر وليست عجلة سطحية. |
| actions | `chars 1056:1091; line 1` | «اذا كنت تريد ان تبدأ بزنس ابدأ الآن» | الفعل المحوري هو البدء الفوري. |
| structure | `chars 1169:1209; line 1` | «start then learn  don't learn then start» | قاعدة المصدر المركزة: الفعل أولًا ثم التعلم. |
| structure | `chars 1811:1880; line 1` | «اكتشفت بعد كده ان انا مفهاش اكون مشتت مفهاش اعمل كذا نيش في نفس الوقت» | المثال يشرح التعلم من التشتت والتركيز، لا نظام outreach مستقل. |
| scope | `chars 5054:5152; line 1` | «المهم انك تبدأ ما تحاولش تفكر اوي في النيش ما تحاولش تفكر اوي  في بزنس مودل ابدأ كلهم ينفعوا صدقني» | الخلاصة تضع البدء والتعلم قبل حسم كل تفاصيل النيش أو النموذج. |

الاقتباسات وبصمات المقاطع محفوظة في سجل JSON، وفحص مستقل بعد الكتابة أعاد مطابقة كل slice مع النص الخام.

### الأدلة السلبية وحدود الملكية

- لا يشرح المصدر discovery أو qualification أو objection أو closing كمحادثة بيع؛ لذلك لا يكون `sales` primary.
- البريد يظهر ضمن حل مشكلة عدد الأشخاص الذين يرسلون emails، وليس كنظام cold-email أو follow-up مكتمل؛ لذلك يبقى `outreach` إحالة ثانوية.
- ذكر service وbusiness model لا يقدم tiers أو pricing architecture أو ضمانات؛ لذلك ليس `pricing_offers` primary.
- ذكر TikTok والفيديو يخدم مثال جذب أشخاص للعمل، ولا يقدم audience/funnel/distribution strategy؛ لذلك ليس `content_strategy` primary.

## المراجع الثانوية bounded

المراجع التالية لا تنشئ نسخًا ثانية ولا تضاعف وزن المصدر؛ كلها تحمل نفس `source_id` وتشير إلى المواضع نفسها:

| الحالة | الزوج | الثقة | السبب والمواضع |
|---|---|---|---|
| current config | `outreach / outreach_mechanics_and_follow_up` | medium | يذكر «ازاي اجيب ناس تبعت ايميلات» في `chars 2978:3004`، ثم «انا مش عايز افضل انا  ابعت ايميلات» في `chars 3009:3043`; هذه آلية مساعدة داخل تجربة البدء وليست الغرض الغالب. |
| proposal only | `business_models / service_models` | low | يظهر «مثلا لو كنت أعمل خدمة» في `chars 3349:3370` و«بزنس مودل» في `chars 4787:4796`; لا يوجد تصنيف لأنواع النماذج أو شرح monetization. |

لا توجد إحالة ثانوية مدعومة إلى sales أو content_strategy؛ لم تُملأ القائمة للتجميل.

## تغطية القراءة الدلالية

سجل `read_coverage` في JSON يستخدم `mode=routing` فقط؛ `content_unit_ids=[]` و`extraction_status=not_started` عمدًا. المقاطع الأربعة موجبة الطول، متصلة، تغطي كامل view، ولا تحتوي فجوة أو overlap:

| segment | start | end | النطاق |
|---|---:|---:|---|
| `SEG_ROUTE_20261014_002_SRC01_001` | 0 | 1811 | السرعة، البدء الآن، وقاعدة start then learn |
| `SEG_ROUTE_20261014_002_SRC01_002` | 1811 | 3660 | التركيز والنيش، service، وأشخاص إرسال البريد |
| `SEG_ROUTE_20261014_002_SRC01_003` | 3660 | 4929 | problem solving، التعيين والتدريب، والتعلم من الخطأ |
| `SEG_ROUTE_20261014_002_SRC01_004` | 4929 | 6069 | الخلاصة، التعلم من الخسارة، وتسلسل الخطوات |

الاتحاد هو `[0,6069)` بالضبط، و`unread_ranges=[]`. هذه تغطية فهم توجيهي وليست استخراجًا معرفيًا.

## حراس عدم التعديل

تم أخذ pre-hash قبل كتابة المخرجات ثم post-hash بعد الكتابة. القيم متطابقة:

| الأصل المحمي | قبل | بعد | الحكم |
|---|---|---|---|
| `collections/corpus/manifest.jsonl` | 1,614,698 bytes; `sha256:aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3` | نفس الحجم والبصمة | UNCHANGED |
| `config/domain_catalog.json` | 31,397 bytes; `sha256:3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add` | نفس الحجم والبصمة | UNCHANGED |
| المصدر الخام المحدد | 10,607 bytes; `sha256:75f570aaf3a23086263ffaed84ee50c001dffd3c7414d3f8f04b7ec630c6ff9b` | نفس الحجم والبصمة | UNCHANGED |
| `raw/new` tree | 1,776 files; 43,757,343 bytes; `sha256:5ad5c8798e5d248fb20ef47d374b5204b6bbf74722a037cfedaa095e1a56deb2` | نفس count/bytes/tree hash | UNCHANGED |

لم تُعدّل `raw` أو manifest أو config، ولم تُكتب أي ملفات claims/concepts/masters أو Source records. الملفات الجديدة الثلاثة المطلوبة فقط هي:

1. `collections/corpus/route_batches/ROUTE_BATCH_2026-10-14-002.json`
2. `reports/corpus-route-single-2026-10-14.md`
3. `checkpoints/CORPUS_ROUTE_2026-10-14_002.md`

## سجل الفحوص والأدلة

| الفحص | النتيجة الفعلية |
|---|---|
| قراءة Python كاملة للمصدر مع strict UTF-8، stat قبل/بعد، reread، و`read(1)==b''` | PASS: `10,607/10,607`, EOF، stable، reread equal، replacements=0 |
| SHA-256 المصدر مقابل manifest | PASS: مطابق `75f570…c6ff9b` |
| Parsing كامل لـ`manifest.jsonl` | PASS: `2,541` سجلًا، target في L1، hash group في L1 وL1832، وبقية المقام `2,540` |
| عدم تكرار `source_id` مع batch001 | PASS: غير موجود في سجلات `ROUTE_BATCH_2026-10-14-001` الخمسة |
| التحقق من quote locators | PASS: كل primary/secondary quote يطابق `source_text[start:end]`، مع quote SHA-256 محفوظ في JSON |
| semantic segments | PASS: `[0,1811)+[1811,3660)+[3660,4929)+[4929,6069)` بلا gaps/overlaps |
| JSON parsing | PASS عبر `python3 -m json.tool collections/corpus/route_batches/ROUTE_BATCH_2026-10-14-002.json` |
| فحص بنية الدفعة | PASS: `record_count=1`، `semantic_read` أعلى الدفعة فقط، `unread_ranges=[]`، لا extraction units |
| raw pre/post وmanifest/config pre/post | PASS: كل الأحجام والبصمات أعلاه unchanged |
| `lsp_diagnostics` للـJSON والتقرير والcheckpoint | PASS: `No diagnostics found. All clean!` لكل ملف |

لم يُستخدم Codex أو subagents، ولم تُنفذ عملية حذف أو نقل أو overwrite. نجاح الفحوص هنا يثبت سلامة القراءة والتوجيه الموضعي لهذه الدفعة فقط، ولا يثبت route_done النهائي أو source_done أو أي بوابة T/C/K/M/QA.

## القيود والحالة التالية

- `entrepreneurship_mindset/goal_setting_and_momentum` proposal-only؛ قرار اعتماد المسار أو تعديل catalog خارج نطاق Worker.
- `semantic_review_status=reviewed` هو self-check من Worker، وليس مراجعة مستقلة.
- هذه الدفعة لا تمثل snapshot: **batch=1 وليست snapshot كاملة**، و**بقية 2,540 سجلًا لم تُقرأ دلاليًا**.
- لا توجد done copy أو REF/ROUTE نهائية؛ لذلك لا يعلن هذا التقرير `route_done` النهائي.
