# 22 — نظام الكتابة والدليل

**المراجعة:** 2026-10-18 — عقد صياغة وتتبّع؛ لا يثبت صحة أي Claim فعلي.  
**النوع:** مواصفة كتابة Term/Claim/Concept/Master ومراجعتها دون هلوسة.  
**المراجع:** [SCHEMA](../SCHEMA.md)، [13](13_MULTI_DOMAIN_ARCHITECTURE.md)، [02](02_CLAIM_EXTRACTION.md)، [03](03_CONCEPT_AUTHORING.md)، [04](04_MASTER_AUTHORING.md)، [21](21_SOURCE_TO_KNOWLEDGE_PIPELINE.md).

> يسجل الكاتب النتيجة القابلة للفحص: النص، الدليل، الموضع، النطاق، نوع الدليل، حدود ما لا يثبته، وقرار المراجعة. لا يُطلب كشف chain-of-thought؛ لا تُستبدل الفجوة بتخمين داخلي.

## 1. الغرض وحدود الصلاحية

يمنع هذا النظام انتقال عبارات المصدر إلى معرفة تقريرية بلا أثر قابل للرجوع. يفرق بين:

- **Term:** لفظ أو وحدة تسمية تحتاج سياقًا وتعريفًا، وليست قاعدة.
- **Claim:** جملة ذرية منسوبة إلى دليل محدد، مع نوع وثقة ونطاق.
- **Concept:** شرح منظم يجمع Claims مراجعة ويعرض الآلية والشروط والحدود والخلافات.
- **Master:** توليف مطلوب فوق Concepts/Claims بعد Gate T الشاملة واختبارات الاسترجاع.

لا يملك هذا الملف `raw/` أو `config/processing_order.json`. لا يرفع حالة المجال، ولا يجيز Master pending، ولا يحول القديم في Vault إلى دليل خام جديد. كل مخرج يظل في حالة المسودة أو المرشح حتى يمر مراجعته وبوابته.

## 2. المدخلات والمخرجات والمالكون

### 2.1 المدخلات

| المدخل | الاستخدام | شرط التحقق |
|---|---|---|
| مصدر ثابت أو نسخة `done` | النص المرجعي | `source_id` وSHA-256 قابلان للحل |
| `READ_*` | view والsegments والـcontent units | حدود Unicode متصلة ومراجعة عند الإغلاق |
| snapshot وdomain lock | النطاق والزمن والملكية | المجال نشط عند extraction، snapshot غير stale |
| Term/Claim candidates | مادة المراجعة | locator وscope أوليان أو فجوة معلنة |
| SCHEMA والـcatalog | أسماء الحقول والحالات | لا enum جديد بلا قرار schema مستقل |
| conflicts وdelta | حدود الصلاحية | لا دليل قديم يُستخدم كحديث دون أثر |

### 2.2 المخرجات

- Term records بحالة `candidate|reviewed|merged|rejected`، وتعريف أو `definition_gap`.
- Claim records بحالة `candidate|reviewed|accepted|rejected`، ودليل quote/hash/locator/scope.
- `REVIEW_*` يثبت مطابقة الدليل وقرار كل وحدة، بما فيها `non_knowledge` و`referred_domain`.
- Concept files/records بحالة SCHEMA ومراجع Claims/مصادر/خلافات.
- Master files/records بحالة `draft|reviewed|canonical|deprecated` ومراجع gates/retrieval.
- فحص أو تقرير يثبت ما تم اعتماده وما بقي مرشحًا أو disputed أو stale.

### 2.3 المالك والحاجز

| المخرج | الكاتب | المراجع الإلزامي | حاجز الصلاحية |
|---|---|---|---|
| Term/Claim candidate | Reader/extractor | لاحقًا Reviewer | المجال النشط، لا قبول مبكر |
| Term/Claim reviewed | Reviewer | QA عند الإغلاق | دليل وموقع ونطاق |
| Concept | Concept author | Reviewer/QA | Claims مراجعة |
| Master | Master author | QA مستقل | Gate T + C/K + retrieval |
| evidence ledger | كل مالك للقرار | Commander/QA | append-only أو revision واضح |

إذا لم يوجد Reviewer مستقل عندما تشترطه المهمة، تبقى الحالة `review_pending` أو `blocked`؛ لا يعوضها تلخيص الكاتب لنفسه.

## 3. الحالات والبوابات

### 3.1 حالات العناصر

```text
candidate → reviewed → accepted
candidate → rejected
candidate/reviewed → disputed | stale | blocked
term candidate → merged (مع merge_target ومصير الأصل)
concept draft → reviewed → accepted أو disputed/deprecated
master draft → reviewed → canonical أو deprecated
```

`disputed` لا يعني أن الدليل مرفوض؛ يعني أن طرفي الخلاف وسياقهما محفوظان. `stale` يعني أن delta أو snapshot أو المصدر تغير، وليس أن النص التاريخي حُذف.

### 3.2 البوابات

| البوابة | معيارها في الكتابة | ما يمنع المرور |
|---|---|---|
| E | كل content unit لها مصير، وكل candidate traceable | وحدة صعبة مخفية أو Claim يتيم |
| T | كل Terms وdefinition gaps في snapshot الشاملة لها قرار ومراجعة | مصطلح جوهري غير محسوم أو مقام ناقص |
| C | Claims ذرية، quote/hash/locator/scope/type مراجع | اقتباس غير مطابق، تعميم مثال، scope مجهول مؤثر |
| K | Concept مبني فقط على Claims C ويعرض الآلية والحدود والخلاف | معلومة بلا Claim، أو تعريف لفظي بدل آلية |
| M | Master بعد T وC/K وبحاجة توليف واختبار retrieval | T stale، Master مطلوب غير مراجع، trace ناقص |
| QA | مراجع مستقل يفحص الروابط والتتبع والـdelta | QA ذاتي أو finding حرج غير محلول |

لا يمنع Gate T تسجيل candidate Terms/Claims أثناء القراءة؛ يمنع قبولها أو بدء Master قبل اكتماله.

## 4. كتابة Term

### 4.1 القاعدة

المصطلح يسجل ما قاله المصدر وما يحتاجه التعريف، لا ما يتوقعه الكاتب. اللفظ قد يكون عربيًا أو إنجليزيًا، لكن `canonical_label` لا يُملأ من تشابه شكلي فقط.

### 4.2 الحقول الدنيا

```yaml
type: term
term_id: TERM_20261018_example_001
domain: sales
subdomain: discovery_and_sales_conversations
snapshot_id: SNAP_EXAMPLE
source_id: SRC_EXAMPLE
source_label: "qualified sales call"
canonical_label: null
aliases: []
definition: null
definition_refs: []
definition_gap: "المصدر يستعمل اللفظ دون تعريف تشغيلي مستقل"
scope: "وصف مكالمة مؤهلة في سياق المصدر، لا معيارًا عامًا للتأهيل"
occurrences:
  - source_id: SRC_EXAMPLE
    locator: "chars 120:141"
    quote_offset: {unit: unicode_codepoint, start: 120, end: 141, bounds: half_open}
claim_refs: [CLM_20261018_example_001]
status: candidate
review: {reviewer: null, decision: pending, reason: null}
merge_target: null
concept_refs: []
master_refs: []
created: 2026-10-18
updated: 2026-10-18
```

### 4.3 فحوص Term

- `source_label` يطابق لفظ المصدر أو يذكر التطبيع بوضوح.
- `occurrences` تتضمن موضعًا قابلًا لإعادة القراءة، لا رقم صفحة غير مفسر.
- `definition` إما مدعوم بموضع/Claim مراجع أو `null` مع `definition_gap`.
- الدمج يحتاج معنى وسياقًا متوافقين؛ إذا اختلف المعنى، يبقى المصطلحان مستقلين.
- `merge_target` لا يمحو الألفاظ أو المواضع أو سجل الرفض.

**التوقف:** تشابه لفظي بلا سياق، تعريف مخمّن، source ID غير قابل للحل، أو محاولة اعتبار term inventory العددي قاموسًا نهائيًا.

## 5. كتابة Claim

### 5.1 الذرية والبيان

الـClaim جملة واحدة قدر الإمكان، تعبر عن وحدة يمكن دعمها أو رفضها منفردة. إذا احتوت الجملة على سبب ونتيجة وشرط ورقم يحتاج كل منها دليلًا مستقلًا أو تفكيكًا إلى Claims. لا تزيد الصياغة قوة الدليل:

- «المصدر يذكر...» عند نقل تقرير المؤلف.
- «يظهر في المثال...» عند مثال.
- «يُستنتج من Claims ...» عند inference.
- «لا يمكن الحسم...» عند hypothesis أو فجوة.

### 5.2 نوع الدليل والثقة

| `evidence_type` | ما يكتبه | ما لا يثبته تلقائيًا |
|---|---|---|
| `direct_quote` | عبارة منقولة حرفيًا | صحتها خارج المصدر أو تعميمها |
| `reported_result` | نتيجة يرويها المصدر مع صاحب التقرير وسياقه | قياسًا مستقلًا أو سببية عامة |
| `example` | حالة أو نصيحة داخل مثال موسوم | قاعدة أو معدلًا عامًا |
| `inference` | استنتاج مشتق من Claims مراجعة وروابط `derived_from` | اقتباسًا مباشرًا من المصدر |
| `hypothesis` | احتمال أو سؤال لم يحسمه الدليل | حقيقة أو توصية معتمدة |

تظل `confidence` مثل `source_reported|supported|inferred|hypothetical|disputed` منفصلة عن `status`. قد يكون Claim `reviewed` مع `confidence: disputed` إذا راجع الطرفان دون حسم.

### 5.3 الاقتباس والـhash والـlocator

الحد الأدنى لClaim منقول:

```yaml
type: claim
claim_id: CLM_20261018_example_001
statement: "المصدر يذكر أنه حجز أكثر من 4000 مكالمة مبيعات."
evidence_type: reported_result
source_id: SRC_EXAMPLE
locator: "line 120-128"
scope: "تقرير المتحدث عن تجربته؛ الفترة والسوق غير مذكورين في المقطع"
confidence: source_reported
status: candidate
quote_hash: sha256:<64-hex>
quote_hash_algorithm: sha256_utf8_exact_quote
quote_offset:
  unit: unicode_codepoint
  start: 3150
  end: 3182
  bounds: half_open
definition_refs: []
what_it_does_not_prove: "لا يثبت معدل التحويل أو السببية أو قابلية التعميم"
read_coverage_ref: READ_EXAMPLE
review_ref: null
created: 2026-10-18
updated: 2026-10-18
```

قواعد التحقق:

1. `quote_offset` صفري البداية وبحدود `[start,end)` على view ثابتة بوحدة Unicode code point؛ لا offsets بايت أو UTF-16.
2. `evidence_quote` هو النص الحرفي الذي يعاد حساب hash له وفق الخوارزمية المسجلة؛ لا يعاد تنسيقه أو ترجمتُه قبل hashing.
3. `locator` البشري (`line`, `section`, `timestamp`, أو `chars`) يظل قابلًا للحل عبر parser/version وخريطة المصدر.
4. يجب أن يطابق الاقتباس النص في `read_coverage_ref`، لا ملخصًا أو نسخة مترجمة غير مربوطة.
5. قبل `reviewed` أو `accepted` يفحص Reviewer hash والحدود و`what_it_does_not_prove` عند انطباق الاقتباس.

إذا تعذر hash أو mapping، يبقى Claim `candidate` أو `blocked`؛ لا يملأ الهاش بقيمة placeholder في سجل يدعي المراجعة.

## 6. النطاق، المثال، الاستنتاج، والخلاف

### 6.1 scope

يشمل scope عند توفره: الجمهور، الحالة/القناة، الشروط، الزمن، السوق/الجغرافيا، العملة، المقام، مرحلة العملية، الاستثناءات، وما يقوله النص عن عدم الانطباق. عند غياب عنصر مؤثر يكتب `not_stated` أو `unknown`، لا يُستنتج من الثقافة العامة أو من عنوان الملف.

### 6.2 المثال ليس قاعدة

كل مثال يوضع في قسم `examples` أو `evidence_type: example` ويذكر:

- أنه مثال أو حالة مذكورة.
- نطاقه وسياقه والفاعل إن كان معروفًا.
- `what_it_does_not_prove: لا يثبت قاعدة عامة` عندما يلزم.
- Claim مستقل إن ادعى المصدر قاعدة أخرى فعلًا؛ لا تستخرج القاعدة من المثال وحده.

### 6.3 inference

الاستنتاج يجوز فقط عندما:

1. كل premise Claims مراجع.
2. العلاقة مسجلة (`derived_from`) ومصاغة بدرجة قوة لا تتجاوز premises.
3. يوسم `evidence_type: inference` و`confidence: inferred`.
4. يذكر ما بقي غير مثبت، ولا يوضع كـ`direct_quote` أو `source_reported`.

الاستنتاج من غياب النص، أو من تشابه المصطلح، أو من Master قديم بلا trace ليس inference مقبولًا؛ هو فجوة أو `hypothesis`.

### 6.4 conflict

عند خلاف مصدرين أو مقطعين:

- ينشأ Claim مستقل لكل طرف مع موضعه وسياقه.
- تسجل علاقة `contradicts` أو `conflict_refs`، ويُحفظ الطرفان.
- تذكر الشروط والزمن والجمهور والاختلاف في التعريف قبل الحكم بالتناقض.
- لا يشترط consensus لاعتماد المراجعة؛ المطلوب trace وتقييم واضح.
- يوسم Concept `disputed` أو Claim `confidence: disputed` عند بقاء الخلاف.

حذف الطرف المخالف لتبسيط Master فشل في المراجعة، لا حل للخلاف.

## 7. كتابة Concept

### 7.1 المدخلات والمخرج والحالة

**المدخلات:** Claims `reviewed` أو `accepted`، Terms ذات صلة، READ، روابط conflicts، وsnapshot.  
**المخرج:** Concept محدد النطاق بمراجع `claim_refs`, `source_refs`, `definition_refs`, `read_coverage_refs`, `conflict_refs`.  
**المالك:** Concept author؛ المراجع يختبر الدليل والحدود.  
**الحالات:** `draft|reviewed|accepted|disputed|deprecated|blocked|stale`.

### 7.2 بنية الكتابة

عند صلة القسم، يضم Concept:

1. **الجوهر:** تعريف مقيد ومراجع.
2. **الآلية:** كيف تعمل الفكرة، وكل خطوة إلى Claim.
3. **الشروط:** متى تنطبق، وما الذي يجب توفره.
4. **الحدود وحالات الفشل:** ما لا تغطيه الأدلة ومتى تفشل.
5. **أمثلة موسومة:** منفصلة عن القاعدة.
6. **التوترات والتعارضات:** الطرفان ومراجع كل طرف.
7. **التطبيقات:** ما يقتصر على نص المصدر، وما هو inference موسوم.
8. **سجل الأدلة:** قائمة Claim/locator/quote hash قابلة للرجوع.

**بوابة K:** لا فقرة تقريرية بلا Claim مراجعة أو وسم inference/hypothesis، ولا رابط عام يحل محل locator.

## 8. كتابة Master

### 8.1 شروط البدء

يجب أن يملك Master author:

- `domain_snapshot` شاملًا غير stale.
- Gate T `pass` لكل المصادر والأقسام، بما فيها المصائر المبررة.
- Claims/Concepts اللازمة بحالة مراجعة وروابط محلولة.
- `need_assessment` يثبت أن مجموعة Concepts تحتاج توليفًا مستقلًا.
- خطة أسئلة retrieval وحدود الامتناع.

لا يبدأ Master صغير أو تخصصي قبل T. وجود Master موروث `draft/partial` يبقيه مسودة ولا يفتح Master جديدًا تلقائيًا.

### 8.2 شروط الكتابة

- يميز بين ما تقوله المصادر وما يلخصه الكاتب وما يستنتجه.
- يضع خلافات المصادر وشروطها، ولا يصنع رأيًا موحدًا بلا سند.
- لا يضيف رقمًا أو benchmark أو توصية غير مربوطة بـClaim.
- يحافظ على روابط الرجوع Master→Concept→Claim→Source/locator.
- يحدد ما لا يغطيه، وما يحتاج امتناعًا في retrieval.

**بوابة M:** Master review + retrieval trace؛ **بوابة QA:** مراجع غير المؤلف، فحص الروابط والـdelta والاختبارات.

## 9. قواعد عدم الهلوسة القابلة للتنفيذ

قبل كتابة أي جملة تقريرية، اسأل في السجل لا في التفكير المخفي:

```text
هل توجد source_id وread_coverage وlocator؟
هل النص يثبت نوع الجملة نفسه؟
هل scope مكتمل أو معلن كـunknown؟
هل الجملة مثال/تقرير/استنتاج/فرضية وموسومة؟
هل هناك Claim مخالف أو delta يجب عرضه؟
```

إذا كانت إجابة أي سؤال «لا»:

- لا تملأ الفراغ من المعرفة العامة.
- اكتب `null`, `definition_gap`, `unresolved`, أو `what_it_does_not_prove` المناسب.
- سجل سبب التوقف ومخرج الامتناع أو الحالة `candidate/blocked`.
- لا تستخدم عدد الملفات، تكرار اللفظ، أو وجود Master قديم كبديل للدليل.

لا تعدّ الترجمة أو إعادة الصياغة اقتباسًا؛ يجب إبقاء النص الأصلي واللغة والموضع. لا تُنسب معلومة إلى «المصدر» إذا كان ما لديك مجرد تفسير الكاتب.

## 10. فحوص النجاح وأسباب التوقف

### 10.1 فحوص النجاح

- كل Term له لفظ مصدر وscope وoccurrences أو سبب واضح للفجوة.
- كل Claim ذري وله source/locator/quote hash عند انطباقه، ونوع وثقة وحدود.
- كل Definition يقود إلى source/locator أو Claim مراجع؛ لا تعريف مخمّن.
- كل مثال موسوم ولا يظهر في النص كقاعدة عامة بلا دليل مستقل.
- كل inference يربط premises مراجعًا ويعلن درجته وحدوده.
- كل conflict يحفظ الطرفين وسياقهما وعلاقة التناقض.
- كل Concept يتتبع إلى Claims C، وكل Master إلى Concept/Claim وgates.
- لا حالة `accepted|canonical` مع `review_ref` فارغ أو دليل غير قابل للحل.
- الفحص يعيد حساب quote hash وoffsets على view نفسها.

### 10.2 أسباب التوقف

| السبب | الحالة الناتجة | القرار |
|---|---|---|
| `quote_mismatch` | blocked/rejected | أعد القراءة، لا تصحح الاقتباس بالتخمين |
| `locator_unresolved` | candidate/blocked | ثبت parser/map أو امتنع |
| `scope_missing` | candidate/review_pending | لا تعمم |
| `definition_gap` | term candidate | لا تملأ التعريف |
| `example_overgeneralized` | Claim rejected أو bounded | افصل المثال عن القاعدة |
| `unsupported_inference` | hypothesis/blocked | اربط premises أو احذف الجملة من المخرج |
| `conflict_hidden` | blocked | أظهر الطرفين والحدود |
| `stale_evidence` | stale | أعد تقييم delta |
| `master_before_T` | blocked | لا تبدأ Master |
| `self_review_only` | review_pending | اطلب Reviewer مستقلًا |

## 11. أمثلة سجلات المراجعة

> أمثلة تعليمية، لا Claim حقيقي ولا دليل corpus فعلي.

### 11.1 قرار Claim

```yaml
review_id: REVIEW_20261018_example_001
claim_id: CLM_20261018_example_001
checks:
  source_resolves: true
  locator_resolves: true
  quote_hash_recomputed: true
  scope_present: true
  evidence_type_matches_text: true
  what_it_does_not_prove_present: true
decision: reviewed
confidence: source_reported
reason: "المقطع يذكر النتيجة بصيغة تقرير المتحدث، ولا يقدم مقامًا أو معدل تحويل."
reviewer: reviewer-example
reviewed_at: 2026-10-18T11:00:00Z
```

### 11.2 Concept مع فجوة معلنة

```yaml
concept_id: CPT_sales_example
status: reviewed
claim_refs: [CLM_20261018_example_001]
source_refs: [SRC_EXAMPLE]
definition_refs: []
conflict_refs: []
coverage: partial
limitations:
  - "لا يثبت الرقم قابلية التعميم أو فعالية الطريقة."
unresolved:
  - "الفترة الزمنية غير مذكورة في المصدر."
review_ref: REVIEW_CONCEPT_EXAMPLE
```

## 12. صيغة تسليم الكاتب

```text
artifact: Claim|Term|Concept|Master
scope: source/snapshot/domain
status: candidate|reviewed|accepted|draft|canonical|disputed|blocked|stale
evidence: [source_id, read_coverage_ref, locator, quote_hash]
measured_checks: ...
gaps_and_limits: ...
not_claimed: ...
review_owner: ...
next_gate: C|K|M|QA|none
```

لا يُكتب «موثق» إذا كان المقصود «مذكورًا في المصدر» دون مراجعة. ولا يُكتب «قاعدة» لمجرد أن المصدر قدم مثالًا. ما لا يمكن إثباته يبقى معلنًا كفجوة أو امتناع، وهو مخرج صحيح للنظام.
