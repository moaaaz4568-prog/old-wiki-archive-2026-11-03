# مراجعة تكامل الويكي متعددة المجالات — 2026-10-10

**الدور:** Reviewer مستقل، قراءة فقط. لم تُعدّل الويكي أو `raw` أو `done` أو
`config` أو Skills. لم تُقرأ ملفات `raw` الكثيرة.

## القرار

**RETURN** — لا يمكن قبول العقد الحالي للتوجيه قبل حسم مالك بوابة R، ومعنى
`source_done`، وعقد metadata/المسارات، وenum الحالات، وحقول cutoff للـdelta.
كما أن التشغيل الفعلي للتوجيه غير مثبت؛ الموجود scaffold وفهارس فقط.

## أكبر الـblockers

### F1 — CRITICAL: R الواحدة تخلط البوابة المحلية بالشاملة

- **المسار/السطر:**
  `config/processing_order.json:43-49,76-80,129-142`؛
  `systems/15_DOMAIN_COMPLETION_GATES.md:68-82`؛
  `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md:629-648`.
- **المتوقع:** اسم/حقل نطاق واضحان، مثل `R_local` لكل مصدر و`R_domain` لتغطية
  كل مرشحي المجال ومساهماته؛ لا يجوز أن يتحول `route_done` إلى شهادة R للمجال.
- **الفعلية:** config يعرّف `R` كـ`global_intake` وبشروط نسخة/مسار مصدر، بينما
  نظام15 يصف R بأنها `routing + source coverage`، ويقول إن R المحلية لمصدر واحد
  ليست R الشاملة. مع ذلك لا يوجد في الحالة إلا مفتاح gate واحد `R`.
- **الأثر:** verifier أو orchestrator لا يستطيع تمييز route محلي ناجح من تغطية
  مجال كاملة؛ قد يمر شرط `domain_done` اعتمادًا على route واحد أو قد تُرفض
  routes الصحيحة باعتبارها ناقصة تغطية.

### F2 — CRITICAL: `source_done` بلا نطاق واحد ثابت

- **المسار/السطر:**
  `config/processing_order.json:58-63`؛
  `systems/13_MULTI_DOMAIN_ARCHITECTURE.md:41-45`؛
  `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md:124-128`؛
  `systems/15_DOMAIN_COMPLETION_GATES.md:6-17`؛
  `done/README.md:20-29`.
- **المتوقع:** إما أن يكون `source_done` إغلاق المصدر كله، أو يُضاف اسم حالة
  مستقل مثل `source_contribution_done` لمساهمة المصدر في المجال النشط، مع بقاء
  الإغلاق الكلي منفصلًا.
- **الفعلية:** config يشترط `complete_source_extraction` لكنه يعلن نطاق الحالة
  `one_source_contribution_to_the_active_domain_snapshot`؛ أما الأنظمة 13–15
  فتقول إن المصدر المختلط لا يكون `source_done` كليًا حتى تُراجع وحداته الأخرى.
  و`done/README` يصفه بأنه اكتمال «مساهمات المصدر».
- **الأثر:** نفس السجل يمكن أن يكون `source_done` في مجال و«غير مكتمل كليًا» في
  النظام العام؛ هذا يفتح احتمال إغلاق مصدر أو مقام تغطية قبل استخراج مساهماته
  الأخرى.

### F3 — CRITICAL: مسار وschema الـroute metadata غير موحدين

- **المسار/السطر:**
  `config/domain_catalog.json:40-54`؛
  `MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md:78-85`؛
  `new/README.md:23-36`؛
  `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md:436-496`.
- **المتوقع:** artifact واحد باسم ومسار وحقول canonical، يستهلكه catalog وREADME
  وverifier معًا، أو adapter موثق وصريح بينهما.
- **الفعلية:** catalog و`new/README` يستخدمان
  `<safe_source_id>.route.json`، بينما الميثاق ونظام14 يستخدمان `REF_<source_id>.json`
  مع `ROUTE_<source_id>.md` إضافي. كما أن catalog يطلب 22 حقلًا؛ قالب REF في
  نظام14 يفتقد 15 حقلًا منها، منها `original_path`، `original_sha256`، الأحجام،
  `primary_domain/subdomain`، `read_coverage`، locators، `source_status` ونسخة
  العقد، ويستخدم بدلها `source_path` و`content_hash` و`primary_route` و
  `source_extraction_status`.
- **الأثر:** سجل route صالح حسب النظام14 قد يفشل schema catalog، أو لا يعثر عليه
  verifier الذي يبحث عن الاسم الآخر؛ لا توجد واجهة تكامل واحدة للنسخة المادية.

### F4 — HIGH: enum الحالات الفعلية لا يطابق enum المعلن

- **المسار/السطر:**
  `config/processing_order.json:43-49,96-109,119-218`؛
  `systems/15_DOMAIN_COMPLETION_GATES.md:84-101`؛
  `systems/16_SEQUENTIAL_AGENT_ORCHESTRATION.md:42-46`؛
  `systems/17_FOLDER_INDEX_CONTRACT.md:80-112`.
- **المتوقع:** enum واحد موثق لكل نوع: gate (`not_started|in_progress|pass|blocked|stale`)
  أو البديل المختار، وحالة domain، وحالة `knowledge_state`، مع mapping صريح.
- **الفعلية:** config يعلن gate statuses بلا `not_closed`، لكن كل gate snapshot
  الفعلي يستخدم `not_closed` و`qa_decision` يستخدم `not_evaluated`. كما أن الحالة
  الحالية في config هي `in_progress|pending`، بينما نظام16 يقرر أن `domain_states`
  تستخدم `pending|active|paused|blocked|done`. قالب الفهرسة يضيف
  `queued|active|reviewed` لـ`knowledge_state` بلا ربط بالحالة الوحيدة.
- **الأثر:** قراءة الحالة الآلية قد ترفض scaffold أو تعتبره pass/unknown، وقد لا
  تتعرف على `sales` بوصفه `active` أو `in_progress`، فتتوقف transitions أو تُفتح
  بقرار خاطئ.

### F5 — HIGH: عقد delta لا يحمل cutoff بما يكفي لإعادة المعالجة

- **المسار/السطر:**
  `config/processing_order.json:91-117`؛
  `systems/15_DOMAIN_COMPLETION_GATES.md:19-29,63-66`؛
  `systems/19_NEW_SOURCE_REPROCESSING.md:15-18,43-55,57-70`.
- **المتوقع:** سجل delta/snapshot canonical يتضمن `delta_id` و`event_type` ووقت
  الاكتشاف والبصمة و`previous_snapshot_id` و`cutoff` وقرار
  `discovered_before_previous_cutoff`، مع أثره وجدولته.
- **الفعلية:** نظام19 يحتاج ويميز هذه القيم، لكن `delta_required_fields` في
  config لا يتضمن `event_type` أو cutoff أو وقت الاكتشاف أو اختبار المرشح السابق
  للـcutoff. و`coverage_snapshot_contract.required_fields` لا يتضمن `cutoff` رغم
  أن نظام15 يجعله جزءًا من snapshot.
- **الأثر:** لا يمكن حتميًا التمييز بين مصدر وصل بعد cutoff ومرشح كان موجودًا ثم
  سقط من manifest؛ وقد لا يُعاد إبطال T/M أو لا يُسجل فشل التغطية في الحالة
  الوحيدة.

## Findings إضافية قابلة للإصلاح

### F6 — MEDIUM: أمثلة subdomain تستخدم IDs غير موجودة في catalog

- **المسار/السطر:** `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md:297-313`؛
  `systems/18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md:33-52`.
- **المتوقع:** كل قيمة تشغيلية في مثال route تكون من `domain_catalog.json`، أو
  تُوسم بوضوح كـplaceholder غير صالح للتنفيذ.
- **الفعلية:** أمثلة النظام14 تعرض `discovery_diagnosis` و`sales_call` و`cold_email`
  و`pricing` و`content_planning`، بينما IDs catalog الفعلية أطول ومختلفة
  (مثل `discovery_and_sales_conversations` و`cold_email_and_message_systems`).
  النص يقول إنها أمثلة، لكنه يقول أيضًا إن catalog عقد إلزامي ولا يسمح بقسم غير
  مسجل.
- **الأثر:** نسخ المثال إلى route ينتج مسارًا لا يحله catalog. من جهة أخرى، فحص
  JSON الفعلي أثبت عدم وجود duplicate داخل IDs الـ22، وترتيب catalog يطابق order؛
  العيب في الأمثلة/الواجهة لا في uniqueness الحالية.

### F7 — HIGH / غير مُثبت تشغيليًا: النسخة المادية لم تُنفذ

- **المسار/السطر:** `config/domain_catalog.json:68-75`؛
  `new/README.md:53-55`؛ `done/README.md:51-53`؛
  `done/sales/objection_handling/INDEX.md:1-8`؛
  `done/sales/source_refs/objection_handling/INDEX.md:1-4`.
- **المتوقع:** عند `route_done` يوجد regular file مستقل فعليًا في
  `done/sales/objection_handling/`، مطابق بالبايت والـSHA-256، مع metadata؛
  `source_refs` يبقى legacy index فقط.
- **الفعلية:** `execution_snapshot` يعلن `source_copies_this_revision: 0`، وفحص
  القرص لهذا المثال وجد `INDEX.md` فقط في المسار المباشر و`INDEX.md` فقط في legacy؛
  لا توجد نسخة مصدر أو route metadata أو route_done. هذا متسق مع تصريح أن هذه
  المراجعة لم تنفذ intake، لكنه يمنع اعتبار التوجيه أو physical-copy gate مجتازًا.

## stale entrypoints وتأثيرها (لم تُعدّل)

| الشدة | المدخل القديم | السطر/التعارض | الأثر إذا قُرئ وحده |
|---|---|---|---|
| MEDIUM | `AGENTS.md` | `1-39`: يذكر raw/schema/links/checkpoint فقط ولا يحيل إلى ميثاق 2026-10-10 أو R/T/C/K/M/QA أو global intake | قد يعتبر فحصًا بنيويًا عامًا كافيًا، ويفوّت النسخة المباشرة وقفل المجال وdelta |
| HIGH | `README.md` | `38-43`: يعلن P2 و5 Sources و15 Claims و4 Concepts، مع أن الحالة الحالية موجة أربعة مجالات وintake عام؛ القياس الحالي للأداة 1781 Source records و1777 Claims | يوجّه العامل إلى نطاق/مقام تاريخي ويخلق انطباع جاهزية أو تغطية غير مطابقين |
| MEDIUM | `SCHEMA.md` | `12-25`: Source schema قديم لا يعرّف أبعاد `route_status`/`source_extraction_status`/copy verification/snapshot/delta | قد يخلط `Source.status` مع حالات workflow أو يرفض metadata الجديدة؛ يلزم bridge صريح لا تغيير enum الأساسي |
| MEDIUM | `systems/00_ARCHITECTURE.md` | `7-13`: المسار القديم Source → Claims → Concept → Master، بلا intake/done/R/T أو serial lock | قد يبدأ استخراجًا أو Master قبل route وT الشاملة |
| HIGH | `systems/01_SOURCE_INGEST.md` | `9-16`: يسمح «مرجعًا غير ناسخ» ويؤخر الحالة إلى ما بعد الاستخراج، ويضع المصدر «المتعارض» في quarantine | تعارض مباشر مع physical copy الإلزامية، و`route_done` قبل extraction، وحفظ الخلاف المدعوم |
| HIGH | `systems/04_MASTER_AUTHORING.md` | `10-20,67-80`: لا يذكر شرط `domain_terms_complete` قبل بدء أي Master؛ claim «لا يوجد canonical حاليًا» غير مؤرخ | قد يبدأ Master صغيرًا بعد Concepts/benchmark محلي؛ claim الحالة قد يصبح stale دون فحص |
| HIGH | `systems/10_SALES_MASTER_GATE.md` | `11-20,62-83`: مدخلات/قبول Master المبيعات بلا all-domain T قبل البدء | مسار مبيعات قد يتجاوز شرط T الشامل الذي يفرضه النظام15 وSkill الـMaster |
| MEDIUM | `systems/11_AGENT_EXECUTION_CONTRACT.md` | `27-61`: نطاق مبيعات، lifecycle قديم، وحالات agent (`validated/partial`) بلا فصل عن current domain/queued أو route/source/domain_done | قد يعامل تسليم Agent أو `processed` كإغلاق، أو يمنع triage العام |
| MEDIUM | `systems/12_ITERATION_AND_RISK_LOOP.md` | `10-22,26-46`: stages قديمة لا تتضمن routing/snapshot/cutoff/delta ولا mapping للبوابات الجديدة | إعادة المعالجة لا تُربط باللقطة أو تجعل stale، ويصعب إثبات أثر الفشل على R/T/M |

## ما اجتاز الفحص وما لم يُثبت

- **اجتياز تكاملي نصي:** `global_intake_routing` مسموح للمجالات pending مع قفل
  المعرفة في مجال واحد في `processing_order.json:5-7,28-39` و`systems/16:8-12`؛
  لا يوجد تعارض حديث يمنع triage العام.
- **اجتياز بوابة Master الحديثة:** config (`processing_order.json:68-89`)،
  نظام15 (`68-81`)، و`master-synthesis-retrieval-gate/SKILL.md:33-46,76-95` كلها
  تشترط T لكل المجال قبل Master الكبير أو الصغير، وتفصل Index/Navigation.
- **اجتياز سياسة الخلاف الحديثة:** `processing_order.json:76-80`،
  `systems/13:105-110`، وSkill الـMaster `76-95,110-118` تحفظ الخلاف ذي الدليل
  والنطاق ولا تشترط إجماعًا. الاستثناء القديم موثق في F8 (`systems/01`).
- **فحص IDs:** أمر Python قرأ JSON بنجاح؛ لا duplicate subdomain IDs، وترتيب
  catalog يطابق order، و`done/sales/objection_handling/` هو المسار المباشر الصحيح.
- **فحص بنيوي خارجي:**
  `python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json`
  أعاد exit 0 و`ok:true` و`errors:[]`، لكنه عدّ سجلات قديمة ولا يفحص semantic
  routing أو physical copies أو coverage. لذلك لا يثبت readiness.
- **LSP:** `lsp_diagnostics` أعاد clean للميثاق، config، `systems/15`، INDEX Skills
  وSkill الـMaster؛ هذا syntax/structure فقط، وليس اختبار pipeline أو semantic read.
- **غير مُختبر:** لم تُنفذ قراءة دلالية لـraw، ولا intake، ولا نسخ byte-exact، ولا
  route verifier، ولا snapshot/claims/concepts/masters/retrieval حقيقي. hash/EOF
  وعد الملفات لا يعوض ذلك.
