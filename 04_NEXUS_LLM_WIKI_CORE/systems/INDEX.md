# فهرس Systems

**مراجعة الفهرس:** 2026-10-18. الحالة: عقود تشغيل؛ وجود النظام أو نجاح فحصه لا يثبت تنفيذه أو اكتمال أي مجال.

## المرجعية والترتيب

اقرأ [AGENTS](../AGENTS.md) و[SCHEMA](../SCHEMA.md)، ثم [الميثاق المصحح](../MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md)، ثم النظام الأقرب للمهمة.
مرجع المواءمة الأحدث هو [2026-10-10](../reports/sales-proof/MULTIDOMAIN_ALIGNMENT_2026-10-10.md) و[ملحق EF22](../reports/sales-proof/USER_MESSAGES_SESSION_EF22.md)، لا خطة الوكيل القديمة.

## العقود العامة متعددة المجالات

| الملف | الوظيفة | اقرأه عندما تحتاج |
|---|---|---|
| [13_MULTI_DOMAIN_ARCHITECTURE.md](13_MULTI_DOMAIN_ARCHITECTURE.md) | فصل الطبقات وحالات الاكتمال ووحدات المحتوى وعقد المصطلح | فهم المنتجين والمستهلكين دون اعتماد دائري |
| [14_SOURCE_ROUTING_AND_DONE_TREE.md](14_SOURCE_ROUTING_AND_DONE_TREE.md) | intake عام وdedup ونسخة مستقلة وroute metadata وsemantic coverage | توجيه مصدر دون ادعاء انتهاء استخراج معرفته |
| [15_DOMAIN_COMPLETION_GATES.md](15_DOMAIN_COMPLETION_GATES.md) | snapshots الشاملة والدفعات والبوابات R/T/C/K/M/QA | قياس التغطية وتقرير جاهزية التوليف أو الإغلاق |
| [16_SEQUENTIAL_AGENT_ORCHESTRATION.md](16_SEQUENTIAL_AGENT_ORCHESTRATION.md) | الأدوار والملكية والقفل والحالة والتسليم والاستئناف | تنسيق مجال واحد أو انتقال موثق |
| [17_FOLDER_INDEX_CONTRACT.md](17_FOLDER_INDEX_CONTRACT.md) | وظائف الفهارس وروابط الدليل واختبار استرجاعها | جعل الملفات قابلة للفهم والاسترجاع لا مجرد العد |
| [18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md](18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md) | حدود المجالات الأربعة وcatalog وترتيب المعرفة | الفصل بين اعتراض السعر وتصميمه أو حسم مسار مختلط |
| [19_NEW_SOURCE_REPROCESSING.md](19_NEW_SOURCE_REPROCESSING.md) | delta/invalidation وstale والجدولة وإعادة الفتح | وصول مصدر أو اكتشاف مرشح ناقص بعد snapshot |

## أنظمة التشغيل والتوثيق والتحديث (ترتيب القراءة 20 → 25)

الترتيب العام لهذه المجموعة هو **20 ثم 21 ثم 22 ثم 23 ثم 24 ثم 25**. يُقرأ 20 أولًا لتثبيت عقد التشغيل، ثم يُقرأ النظام المتخصص بحسب نوع المهمة؛ وللمراجعة الشاملة تُقرأ الملفات الستة بالترتيب المذكور.

> **تنبيه حالة:** وجود العقود 20–25 في الويكي أو إدراجها في هذا الفهرس لا يثبت تشغيلها فعليًا ولا اكتمال أي مجال؛ يلزم سجل تشغيل وفحوص مستقلة وبوابات مقاسة ضمن نطاقها.

| ترتيب القراءة | الملف | الوظيفة | اقرأه عندما تحتاج |
|---:|---|---|---|
| 1 | [20_WIKI_OPERATING_SYSTEM.md](20_WIKI_OPERATING_SYSTEM.md) | نظام التشغيل الموحد من الطلب إلى التسليم: تثبيت النطاق والملكية والمدخلات والحالات وسجل القرار والأدلة | بدء أي تشغيل أو تسليم، أو تحديد ما يثبت وما لا يثبت |
| 2 | [21_SOURCE_TO_KNOWLEDGE_PIPELINE.md](21_SOURCE_TO_KNOWLEDGE_PIPELINE.md) | خط التحويل من `raw` إلى `manifest` ثم التوجيه والقراءة والمصطلحات والادعاءات والمراجعة والمفاهيم والماستر والاسترجاع، مع حارس عدم القفز | تخطيط مسار مصدر أو فحص predecessor والبوابات بين المراحل |
| 3 | [22_WRITING_AND_EVIDENCE_SYSTEM.md](22_WRITING_AND_EVIDENCE_SYSTEM.md) | عقد كتابة Term/Claim/Concept/Master مع quote/hash/locator/scope، وحدود الدليل والمراجعة ومنع الهلوسة | كتابة المعرفة أو مراجعة التتبع والنطاق والأمثلة والاستنتاجات |
| 4 | [23_RETRIEVAL_QA_AND_HONEST_STATUS.md](23_RETRIEVAL_QA_AND_HONEST_STATUS.md) | مواصفة retrieval QA ومسار `Concept → Claim → Source → locator` وقرارات `answer/partial/abstain` والمقام والبسط والحالة الصادقة | اختبار الاسترجاع أو إصدار status أو تحديد PASS/RETURN/BLOCKED/STALE |
| 5 | [24_AGENT_HANDOFF_AND_RECOVERY.md](24_AGENT_HANDOFF_AND_RECOVERY.md) | عقد الأدوار والملكية والمسارات المسموحة وcheckpoint وhandoff والاسترداد بعد الانقطاع أو الفشل | تكليف Worker/Reviewer/QA أو تسليم العمل واستئنافه بلا تكرار |
| 6 | [25_CHANGE_CONTROL_AND_UPDATE_PROTOCOL.md](25_CHANGE_CONTROL_AND_UPDATE_PROTOCOL.md) | بروتوكول change manifest والإصدارات والتواريخ وdelta/invalidation/stale وتوافق schema وتحديث الوثائق والفهارس | إضافة مصدر أو تصحيح دليل أو تحديث عقد/فهرس أو تقييم أثر تغيير |

## الأنظمة الأساسية والتخصصية السابقة

| الملف | الوظيفة وحد التكامل |
|---|---|
| [00_ARCHITECTURE.md](00_ARCHITECTURE.md) | الطبقات والعلاقات العامة؛ يضيف13 عقود المجالات |
| [01_SOURCE_INGEST.md](01_SOURCE_INGEST.md) | تسجيل Source؛ سياسة الأصل الثابت والنسخة الإلزامية يحكمها14 |
| [02_CLAIM_EXTRACTION.md](02_CLAIM_EXTRACTION.md) | Claim من النص؛ المرشح يسجل أثناء القراءة لا بعد T فقط |
| [03_CONCEPT_AUTHORING.md](03_CONCEPT_AUTHORING.md) | المفهوم من Claims المراجعة، لا من الأسماء وحدها |
| [04_MASTER_AUTHORING.md](04_MASTER_AUTHORING.md) | كتاب المعرفة وعقده؛ لا يبدأ قبل T الشاملة في15 |
| [05_RETRIEVAL_AND_EVALUATION.md](05_RETRIEVAL_AND_EVALUATION.md) | أسئلة الاسترجاع والقياس وحالات الامتناع |
| [06_SALES_SOURCE_COLLECTION.md](06_SALES_SOURCE_COLLECTION.md) | ترشيح القراءة؛ العينات ليست اكتمالًا وحدود المجالات يحكمها18 |
| [07_SALES_CLAIM_REVIEW.md](07_SALES_CLAIM_REVIEW.md) | مطابقة الاقتباس والنطاق ونوع الدليل في المبيعات |
| [08_SALES_OPINION_PLURALISM.md](08_SALES_OPINION_PLURALISM.md) | حفظ الخلاف وشروطه وعدم الحسم دون إجماع مصطنع |
| [09_SALES_CONCEPT_DEPTH.md](09_SALES_CONCEPT_DEPTH.md) | عمق Concept وفصل المثال عن القاعدة |
| [10_SALES_MASTER_GATE.md](10_SALES_MASTER_GATE.md) | قبول Master المبيعات واختباره، بالإضافة إلى شرط T قبل البدء |
| [11_AGENT_EXECUTION_CONTRACT.md](11_AGENT_EXECUTION_CONTRACT.md) | الصلاحيات وتسليم العامل؛ يضيف16 الحالة والقفل العام |
| [12_ITERATION_AND_RISK_LOOP.md](12_ITERATION_AND_RISK_LOOP.md) | إثبات الفشل والإصلاح وعدم الانحدار |
| [99_LESSONS_AND_FAILURES.md](99_LESSONS_AND_FAILURES.md) | دروس وقائية، لا بديلًا عن إصلاح النظام |

## أحكام التكامل الحاكمة في الموجة الحالية

- 13–19 والميثاق المصحح تحكم التوقيت والتوجيه والتغطية في الموجة؛ الأنظمة الأقدم تستخدم فيما لا يتعارض معها، ولم تُعدّل هنا.
- لا تفسر خيار reference في01 على أنه بديل للنسخة في done، ولا تعارض آراء المصادر على أنه سبب quarantine.
- نطاق collection القديم في06 لا يدمج outreach أو تصميم السعر في sales تلقائيًا؛ يعاد توجيه المساهمات وفق18.
- R = routing + source coverage؛ T = all-domain terms؛ C = claims review؛ K = concepts؛ M = masters + retrieval؛ QA = independent closure.
- `config/domain_catalog.json` مرجع النطاق، و`config/processing_order.json` سجل الحالة الوحيد؛ الفهرس ليس بديلًا لأي منهما.
- intake عام حتى للمجالات pending؛ صناعة المعرفة متتابعة، و`source_done` بلا اشتراط Concept/Master.
- `subdomain_extraction_done` لا يبيح أي Master قبل `domain_terms_complete` من snapshot شامل لكل مصادر وأقسام المجال.
- لا تعديل raw أو حذف أو تفويض ذاتي؛ تعليمات المهمة الأحدث تحكم الصلاحية، وتصحيح الأنظمة الحالي بلا subagents أو بناء مصادر.

## تحقق مراجعة الفهرس

أدلة فحص الملفات والروابط وJSON وLSP محفوظة في [تقرير الأنظمة v3](../reports/sales-proof/agent-general-systems-v3.md). لا يُنسب هذا الفحص إلى corpus أو config أو الاختبارات المعرفية.
