# 15 — بوابات اكتمال المجال والتغطية

**مراجعة:** 2026-10-10 — عقد إغلاق، لا نتيجة إغلاق حالية.
**مدخلات:** [13](13_MULTI_DOMAIN_ARCHITECTURE.md)، [14](14_SOURCE_ROUTING_AND_DONE_TREE.md)، catalog، snapshot، وسجلات القراءة والمراجعة.

## 1. حالات مستقلة

| الحالة | دليلها اللازم | لا تبيح |
|---|---|---|
| `route_done` | تصنيف دلالي + نسخة مستقلة مطابقة + metadata | الاستخراج في مجال pending |
| `source_done` | جميع وحدات المحتوى terms/Claims بمواضعها ومراجعتها ومصائرها | إغلاق المجال تلقائيًا |
| `subdomain_extraction_done` | كل مساهمات مصادر القسم في snapshot استخرجت وجُمعت وروجعت | بدء Master صغير |
| `domain_terms_complete` | مصطلحات كل مصادر وأقسام snapshot الشامل مكتملة المراجعة | إعلان QA أو الاسترجاع ناجحين |
| `domain_done` | R/T/C/K/M/QA + فهارس + سجل إغلاق مرتبط بلقطة | إسقاط اللقطة على مخزون أحدث |

المصدر المختلط يبقى كليًا غير `source_done` إن بقيت وحدات لمجال منتظر؛ تُغلق مساهمته المكتملة للمجال النشط فقط.
لا تتطلب T استخراج بقية المجالات، لكنها تتطلب حصر كل ما يخص المجال الحالي حتى في المصادر ذات المسار الرئيسي الخارجي.

## 2. snapshot شامل لا عينة متنكّرة

- `domain_snapshot` يثبت domain ونسخة catalog وحدود الموضوع وcutoff وجذور الجرد ونسخة manifest وبصمتها.
- يشمل جميع مرشحي الجذور المعلنة قبل cutoff، وكل المصادر المسجلة والإحالات ذات الصلة؛ ليس `strong` وحدها.
- لكل مرشح، حتى خارج المجال، `disposition` وسبب ودليل ومراجع؛ لا تخفيض للمقام بإخفاء المسارات الصعبة.
- القيم: `included_domain`، `referred_domain`، `duplicate`، `excluded_out_of_scope`، `quarantined`، `unresolved`.
- `unresolved` سجل ظاهر لا قرار نهائي؛ غموض قد يؤثر في النطاق أو عزل مادة لازمة يمنع T والإغلاق.
- الاستبعاد قرار نطاق مدعوم، لا مهربًا من مصدر طويل أو دليل مخالف؛ duplicate يشير إلى هوية أساسية متحققة.
- كل subdomain في catalog يظهر، حتى الفارغ، مع إثبات عدم وجود مرشحين؛ لا إنشاء معرفة لملء خانة فارغة.
- دفعة `batch` جزء مسمى بحدوده وparent snapshot؛ نجاحها لا يجعل قسمًا أو مجالًا كاملًا.
- إعلان `domain_terms_complete` محصور في snapshot من نوع `domain_snapshot` شامل، لا batch أو top-N.

## 3. حقول snapshot والدفعة

المثال التالي **دفعة غير مؤهلة للإغلاق**، لا يدعي حصر قسم كامل أو مخزون حقيقي:

```json
{
  "snapshot_id": "BATCH_EXAMPLE_01",
  "scope_kind": "batch",
  "parent_snapshot_id": "DOMAIN_SNAPSHOT_EXAMPLE",
  "domain": "sales",
  "catalog_revision": "example-v1",
  "cutoff": "2026-10-10T00:00:00Z",
  "inventory_roots": ["new/", "raw/new/"],
  "registered_source_inventory_ref": "EXAMPLE_REGISTERED_MANIFEST",
  "candidate_manifest_sha256": "sha256:<64-hex>",
  "candidate_manifest": [
    {"candidate_id": "ITEM_1", "path": "new/a.txt", "source_id": "SRC_A", "discovered_at": "2026-10-09T12:00:00Z", "size_bytes": 180, "content_hash": "sha256:<64-hex>", "disposition": "included_domain", "reason": "مساهمة بيع", "evidence_locators": ["line 1-5"], "reviewer": "example-reviewer"},
    {"candidate_id": "ITEM_2", "path": "new/b.txt", "source_id": "SRC_B", "discovered_at": "2026-10-09T12:01:00Z", "size_bytes": 150, "content_hash": "sha256:<64-hex>", "disposition": "referred_domain", "target_domain": "outreach", "reason": "تواصل أولي فقط", "evidence_locators": ["line 1-4"], "reviewer": "example-reviewer"}
  ],
  "all_subdomain_ids": ["example-subdomain"],
  "included_unique_source_ids": ["SRC_A"],
  "secondary_contribution_source_ids": [],
  "batch_source_ids": ["SRC_A"],
  "batch_segment_bounds": {"SRC_A": ["line 1-5"]},
  "inventory_complete": false,
  "reading_coverage_refs": [],
  "terms_review_refs": [],
  "coverage_status": "partial",
  "eligible_for_T": false
}
```

في اللقطة الشاملة تكون `all_subdomain_ids` مساوية لجميع أقسام المجال في نسخة catalog، لا لقائمة المثال.
كل سجل جرد يحمل وقت الاكتشاف والحجم والبصمة؛ عند تعذر البصمة تسجل `null` مع سبب وفشل سلامة ظاهر.
يغطي manifest كل المرشحين السابقين للحد، وتحفظ مراجع دمج الدفعات واتحادها دون فجوات أو تكرار في العد.
عند الإغلاق يقارن المراجع قائمة المرشحين الأصلية بالمصائر بمساواة المجموعات، لا بمقارنة عددين فقط.

## 4. المعاني الثابتة للبوابات

| البوابة | المعنى | شرط المرور وموانعه |
|---|---|---|
| R | routing + source coverage | حصر المرشحين، مصائرهم، المسارات والنسخ، وcoverage دلالي متصل لكل مساهمة داخلة؛ EOF وحده لا يكفي |
| T | all-domain terms | R + استخراج ومراجعة كل مصطلحات كل المصادر والأقسام في اللقطة الشاملة؛ لا مرشح جوهري بلا مصير |
| C | claims review | كل الوحدات والاقتباسات والمواضع والنوع والنطاق مراجعة؛ لا تعميم مثال أو Claim معلّق مستخدم |
| K | concepts | كل Concept مطلوب يتبع أدلة C المراجعة ويشرح الآلية والحدود والخلافات |
| M | masters + retrieval | بعد T ومراجعة أدلة C/K: الكتب المطلوبة وفق الحاجة، واختبارات الاسترجاع والتوجيه والسلامة |
| QA | independent closure | مراجع غير مؤلف المخرجات يعيد فحص التغطية والتتبع والروابط والفهارس وأثر delta ثم يقرر الإغلاق |

هذه بوابات تقييم، لا حظر لتسجيل candidate terms/Claims أثناء القراءة قبل اكتمال R أو T للمجال.
مراجعة Claims وConcepts المبنية عليها يمكن أن تتقدم محليًا؛ لا يبدأ أي Master قبل T الشاملة.
الخلاف المدعوم ذو نطاق واضح ومصير مراجع لا يمنع C/K/M؛ غياب الدليل أو تقييمه هو المانع.
شهادة R المحلية لنسخة واحدة ليست شهادة R الشاملة؛ يجب تسجيل `scope` لكل نتيجة.

## 5. سجل البوابة والإغلاق

```json
{
  "gate": "T", "scope": "domain", "domain": "sales",
  "snapshot_id": "DOMAIN_SNAPSHOT_EXAMPLE", "snapshot_sha256": "sha256:<64-hex>",
  "status": "blocked", "evidence_refs": [], "reviewer": null,
  "checked_at": null, "blockers": ["coverage_not_verified"],
  "pending_delta_ids": [], "state_revision": 0
}
```

حالات البوابة `not_started|in_progress|pass|blocked|stale`؛ `pass` يلزمه مراجع وتاريخ وأدلة فعلية بلا blockers.
سجل الإغلاق يضم نتائج الست، المقامات والبسوط، subdomains، الملفات المطلوبة، الخلافات، QA، وأثر كل delta.
T شهادة استخراج ومراجعة مصطلحات لا شهادة صحة كل رأي؛ لا تستبدل C أو K.
`domain_done` لا يقبل مخرجًا مطلوبًا بحالة draft/partial أو مخاطرة حرجة أو اختبار استرجاع لم ينفذ.
لا يُفرض Master لكل قسم فارغ؛ يثبت تقييم الحاجة قائمة الكتب المطلوبة ولا يُستخدم لتجاوز طلب التوليف الحقيقي.
يحفظ [16](16_SEQUENTIAL_AGENT_ORCHESTRATION.md) نتيجة الإغلاق في الحالة الوحيدة؛ التقرير لا يغيرها وحده.

## 6. اختبارات الرفض الإلزامية

- عينة اعتراضات مكتملة وباقي أقسام sales غير مقروءة → `batch_complete` فقط؛ T وMaster مرفوضان.
- كل البايتات قُرئت مع فجوة segment دلالي → R فاشلة، ولو بلغت تغطية IO نسبة100%.
- نسخة مطابقة إضافية → تسجل disposition، ولا يرتفع عدد المصادر أو الاستقلال الأدلي.
- candidate Claim سجل أثناء القراءة → مسموح؛ إدخاله Concept قبل مراجعة دليله → مرفوض.
- مصدر تمت مراجعة كل وحداته دون أي Master → يقبل `source_done`، لا `domain_done`.
- وصول مصدر جديد قبل الانتقال → [19](19_NEW_SOURCE_REPROCESSING.md)، لا تجاوز delta ولا إعادة فتح صامتة.
