# 21 — خط أنابيب المصدر إلى المعرفة

**المراجعة:** 2026-10-18 — مواصفة مراحل متتابعة؛ لا تثبت تشغيل corpus أو اكتمال مجال.  
**النوع:** عقد تحويل قابل للتتبع من الدليل الخام إلى مخرجات الاسترجاع.  
**المراجع:** [13](13_MULTI_DOMAIN_ARCHITECTURE.md)، [14](14_SOURCE_ROUTING_AND_DONE_TREE.md)، [15](15_DOMAIN_COMPLETION_GATES.md)، [17](17_FOLDER_INDEX_CONTRACT.md)، [SCHEMA](../SCHEMA.md).

> كل مرحلة تنتج سجلًا يثبت دخولها وخروجها. لا يجوز القفز من manifest إلى Concept أو من route إلى Master. المرشح يمكن أن يُجمع مبكرًا، لكنه لا يصبح معرفة مراجعة لمجرد وجوده.

## 1. الغرض وقاعدة عدم القفز

خط الأنابيب هو:

```text
raw → manifest → route/copy → read coverage → terms + candidate claims
    → review → concepts → master → retrieval QA
```

المسار السابق لهوية الملف لا يكفي للمسار اللاحق لصحة المعرفة. النسخة في `done/` ليست Claim، ووجود Claim ليس Concept، ووجود Concept ليس Masterًا صالحًا للاسترجاع. كل انتقال يحتاج `predecessor_ref` وقرارًا أو Gate ضمن النطاق نفسه.

الاستقبال العام والتوجيه مسموحان للمجالات الأربعة، بما فيها `pending`. أما جمع المعرفة (`Terms/Claims/Concepts/Masters`) فيقتصر على المجال الذي يملكه `config/processing_order.json` بوصفه المجال النشط. لا يفتح `route_done` استخراج مجال pending.

## 2. المدخلات والمخرجات والملكية

### 2.1 المدخلات

| المدخل | الاستخدام | شرط القبول |
|---|---|---|
| الأصل في `raw/` أو مدخل `new/` | الدليل الوحيد للهوية والمحتوى | مسار نسبي، ثابت، قابل للقراءة، لا تعديل |
| `raw/SOURCE_MANIFEST.tsv` أو manifest تشغيل | حصر المرشحين والمقام | يغطي الجذر والـcutoff، ويذكر المصير لكل مرشح |
| Source records | `source_id`, hash, media type, الحالة | لا تعارض هوية أو بصمة |
| catalog والحالة | route والملكية والقفل | domain/subdomain مسجل، active domain معروف |
| snapshots والـdelta السابقة | حدود القراءة وصلاحية الأدلة | snapshot وcutoff وcatalog revision مثبتة |
| سجلات المراحل السابقة | predecessor وtrace | الحالة والمراجع قابلة للحل |

### 2.2 المخرجات

| المرحلة | المخرج الأساسي | المراجع اللازمة |
|---|---|---|
| raw | لا مخرج كتابي داخل الأصل | `raw_changed=0` أو سجل فشل |
| manifest | سجل مرشح شامل | path، size، hash، candidate/source ID، disposition |
| route/copy | نسخة byte-exact و`ROUTE/REF` | primary route، secondary refs، copy checks |
| read coverage | `READ_*` | IO + view + segments متصلة + مراجعة |
| terms/claims | Terms وcandidate Claims | source/locator/scope/coverage |
| review | `REVIEW_*` ومصائر الوحدات | قرار لكل وحدة وسبب الاستبعاد/الإحالة |
| concepts | Concept بمراجع Claims | الجوهر والآلية والشروط والحدود والأمثلة والخلاف |
| master | Master متناسب مع الحاجة | T وC/K، domain snapshot، retrieval eval |
| retrieval QA | trace واختبار وحكم | سؤال، جواب/امتناع، evidence chain، baseline |

### 2.3 المالك

| الدور | المراحل | القيد |
|---|---|---|
| Intake/classifier | raw→manifest→route/copy | لا يستخرج معرفة pending |
| Reader/extractor | read coverage→terms/claims | المجال النشط والدفعة المأذونة فقط |
| Reviewer | review | لا يغيّر المصدر أو يخفي وحدة صعبة |
| Concept author | concepts | Claims مراجعة، لا تشابه لفظي وحده |
| Master author | master | بعد T الشاملة وdependencies المراجعة |
| QA/index | retrieval QA | مستقل عن مؤلف المخرج، أو يوسم `blocked` |
| Commander | قفل المجال وقرار الانتقال | لا يعتمد بلا أدلة أو معاملة حالة |

## 3. آلة الحالات والبوابات

### 3.1 حالات العنصر في الخط

```text
not_started → in_progress → evidence_ready → review_pending → accepted
                         └→ partial | blocked | failed | stale
partial/blocked/failed → checkpointed → retry أو blocked
stale → impact_review → reprocess أو no_impact_reviewed
```

هذه حالات workflow وليست بدائل عن قيم `Source.status` أو Gate status في `SCHEMA`. يسجل كل سجل `stage`, `state`, `snapshot_id`, `predecessor_refs`, `owner`, و`updated_at`.

### 3.2 شروط الانتقال

| الانتقال | predecessor الإلزامي | لا يمر إذا |
|---|---|---|
| manifest→route | manifest شاملة وhash | مرشح بلا disposition أو path غير آمن |
| route→coverage | route/copy ناجحان | لا نسخة مستقلة أو route غامض |
| coverage→extraction | `READ` extraction في المجال النشط | segments ناقصة أو snapshot stale |
| extraction→review | كل content units لها مصير أولي | وحدة غير مذكورة أو Claim بلا locator |
| review→concepts | Claims/Terms اللازمة `reviewed` | Claim معلّق مستعمل أو تعريف مخمّن |
| concepts→master | Gate T وC/K المطلوبة ناجحة | T ليست شاملة أو dependencies stale |
| master→retrieval QA | Master/index/trace موجودة | مسار رجوع مكسور أو سؤال بلا expected scope |

`source_done` يعني اكتمال وحدات المصدر ومراجعتها ضمن نطاقه؛ لا يتطلب Master. `subdomain_extraction_done` لا يفتح Master. `domain_terms_complete` يتطلب snapshot شاملة لكل مصادر وأقسام المجال، لا دفعة أو top-N.

## 4. مراحل التنفيذ التفصيلية

### 4.1 المرحلة A — `raw`

**المدخلات:** جذور raw/new ومواضعها المعلنة.  
**المخرجات:** لا كتابة في raw؛ جرد قراءة فقط وسجل سلامة تشغيل.  
**المالك:** Intake/classifier.  
**الحالة:** `received` أو `reading_full` على مستوى المصدر.

الخطوات:

1. ثبت الجذر ووقت القطع والحدود، ثم استخدم `os.walk` أو verifier مكافئًا لجرد المسارات.
2. سجل path النسبي، الحجم، الامتداد، ووقت الاكتشاف؛ لا تعتمد اسم الملف كمعرفة.
3. اقرأ البايتات كما هي واحسب SHA-256 قبل التطبيع.
4. افحص الثبات قبل/بعد القراءة؛ أي تغير يصبح `quarantined` بسبب مستقل.

**بوابة الخروج:** لا يوجد تغيير في `raw`، وكل مرشح له هوية أو سبب فشل.  
**توقف:** `source_changed_during_read`, `incomplete_read`, مسار traversal، ملف فارغ/ثنائي غير مدعوم، أو فشل hash.

### 4.2 المرحلة B — `manifest`

**المدخلات:** جرد raw ومصادر/manifest السابقة.  
**المخرجات:** manifest تشغيل شاملة، لا معرفة.  
**المالك:** Intake/classifier؛ يراجعها Commander أو Reviewer حسب التكليف.  
**الحالة:** `planned|in_progress|validated|blocked`.

لكل مرشح يجب تسجيل `candidate_id`, `source_id` إن أمكن، path، size، hash أو null مع سبب، discovered_at، cutoff، disposition، reason، evidence locators، reviewer. المصائر الدنيا: `included_domain`, `referred_domain`, `duplicate`, `excluded_out_of_scope`, `quarantined`, `unresolved`.

**بوابة M0:** اتحاد المصائر يساوي مجموعة المرشحين الأصلية، لا مجرد مساواة العدد.  
**توقف:** مرشح غير ظاهر، duplicate بلا primary متحقق، unresolved مؤثر، أو تقليص المقام إلى عينة.

### 4.3 المرحلة C — `route/copy`

**المدخلات:** manifest validated، catalog، متن المصدر للتصنيف.  
**المخرجات:** primary route واحد، secondary references محددة، نسخة مستقلة byte-exact تحت `done/<domain>/<subdomain>/`، و`REF/ROUTE` metadata.  
**المالك:** Intake/classifier؛ التحقق مستقل إن أمكن.  
**الحالة:** `classified → copy_and_metadata_verified → route_done` أو `uncertain/quarantined`.

الخطوات:

1. اقرأ المتن والهيكل والغرض، وسجل locators لكل عائلة دليل.
2. قارن بالـcatalog؛ إن تعادل مجالان أو غاب subdomain ابق `uncertain`.
3. اختر primary واحدًا؛ secondary يشير إلى نفس `source_id` ولا يضاعف الدليل.
4. انسخ دون تطبيع، احسب hash وحجم النسخة، افحص symlink/hardlink والاستقلال.
5. أنشئ metadata ثم فهرس المسار، ولا تسجل Claim أو Concept هنا.

**بوابة R المحلية:** route evidence + copy hash/bytes + metadata + raw unchanged.  
**توقف:** اسم لا يطابق catalog، route غامض، copy mismatch، overwrite محتمل، أو استدلال من الاسم وحده.

### 4.4 المرحلة D — `read coverage`

**المدخلات:** نسخة/أصل route_done، snapshot، parser/version، domain النشط.  
**المخرجات:** `READ_*` يفصل IO عن القراءة الدلالية.  
**المالك:** Reader/extractor؛ Reviewer يراجع الفهم.  
**الحالة:** `not_started|in_progress|reviewed|complete|blocked|stale`.

يجب أن يسجل `source_sha256`, `snapshot_id`, `batch_id`, bytes expected/read، EOF، stability، view hash، وحدة Unicode code point، segments نصف مفتوحة متصلة من `0` إلى `view.length`، `unread_ranges`, `content_units`, ووقت/هوية reader وreviewer. EOF وhash يثبتان IO فقط؛ لا يثبتان الفهم.

**بوابة R semantic:** لا gaps ولا overlaps في الاتحاد الأساسي، وكل segment له ملاحظة غرض/سياق ومراجعة، وكل وحدة لها `disposition`.  
**توقف:** فجوة دلالية، mapping مفقود لصفحة/PDF/timestamp، replacement chars غير مصرح بها، أو snapshot stale.

### 4.5 المرحلة E — `terms + candidate claims`

**المدخلات:** `READ_*` extraction في المجال النشط.  
**المخرجات:** Terms مرشحة وClaims مرشحة معًا، مرتبطة بـ`content_unit_ids` وlocators.  
**المالك:** Reader/extractor؛ لا يحتاج انتظار T لبدء الجمع.  
**الحالة:** `in_progress|candidate|partial|blocked`.

لكل وحدة يحدد القارئ: مصطلحًا أو أكثر، Claim ذريًا أو أكثر، أو `non_knowledge`/`referred_domain`/`duplicate` بسبب واضح. يسجل المرشحون `status: candidate` ولا يستعملون لبناء Master قبل المراجعة. التعريف غير الموجود يسجل `definition_gap` بدل التخمين.

**بوابة E:** اتحاد الوحدات له مصير، وكل Claim/Term قابل للعودة إلى source/view/locator.  
**توقف:** Claim بلا quote/locator، خلط مجال pending، أو استخدام Master قديم لإكمال الفراغ.

### 4.6 المرحلة F — `review`

**المدخلات:** Terms/Claims candidates وREAD وsource scope.  
**المخرجات:** `REVIEW_*`، قرار لكل وحدة وTerm وClaim، وروابط conflict/merge/rejection.  
**المالك:** Reviewer غير المؤلف إن كان مطلوبًا.  
**الحالة:** `reviewed|partial|blocked|stale`.

يفحص المراجع مطابقة الاقتباس والبصمة والموضع والنطاق ونوع الدليل و`what_it_does_not_prove`. يحفظ الرأي المخالف المدعوم، ولا يحول المثال إلى قاعدة ولا يرفض اختلافًا لمجرد غياب الإجماع.

**بوابة C:** لا Claim مستعمل في Concept بلا review، ولا وحدة مؤثرة بلا مصير.  
**توقف:** quote hash لا يعاد حسابه، locator لا يحل، scope مفقود مؤثر، أو قرار reviewer غير قابل للتعليل بالدليل.

### 4.7 المرحلة G — `concepts`

**المدخلات:** Claims/Terms مراجعة، conflicts، READ، وقائمة الحاجة.  
**المخرجات:** Concept بحالة `draft|reviewed|accepted|disputed|deprecated`، ومراجع claim/source/definition/coverage.  
**المالك:** Concept author؛ Reviewer/QA يختبر الحدود.  
**الحالة:** `draft|review_pending|reviewed|blocked|stale`.

يبني الكاتب مفهومًا من الأدلة لا من تشابه الألفاظ، ويملأ عند الصلة: الجوهر، الآلية، الشروط، الحدود وحالات الفشل، الأمثلة الموسومة، التوترات، التطبيقات، وسجل الأدلة. أي آلية غير مستنبطة من Claims مراجعة تبقى فجوة أو inference موسومًا.

**بوابة K:** trace كامل من كل قسم معرفي إلى Claim مراجعة، مع عرض الشروط والخلافات.  
**توقف:** Concept يضيف قاعدة غير مذكورة، example بلا scope، أو dependency stale.

### 4.8 المرحلة H — `master`

**المدخلات:** `domain_snapshot` شامل، Gate T PASS، Claims/Concepts اللازمة مراجعة، وحاجة استرجاع مثبتة.  
**المخرجات:** Master مناسب للحاجة، بحالة `draft|reviewed|canonical|deprecated`، ومراجع gate/retrieval.  
**المالك:** Master author؛ Commander يصرح بالبداية؛ QA مستقل.  
**الحالة:** `not_started|draft|reviewed|blocked|stale`.

لا يُنشأ Master لمجرد كثرة الملفات أو لملء قسم. يقرر `need_assessment` لماذا لا تكفي Concepts، وما الذي سيستهلكه Master. لا يبدأ حتى `domain_terms_complete` لكل مصادر وأقسام snapshot، حتى لو كان Master صغيرًا.

**بوابة M:** T + dependencies C/K + Master review + retrieval plan.  
**توقف:** T غير شاملة، snapshot قديمة، concept draft مطلوب، أو حاجة التوليف غير مثبتة.

### 4.9 المرحلة I — `retrieval QA`

**المدخلات:** Master/Concept/Claim/Index، retrieval questions، snapshot، baseline، وdelta refs.  
**المخرجات:** `RETRIEVAL_*` trace واختبارات وإجابة/امتناع وحكم QA.  
**المالك:** QA/index مستقل؛ Commander يعتمد الإغلاق.  
**الحالة:** `in_progress|pass|blocked|stale`.

يختبر السؤال المباشر، الدمج، الخلاف، محاولة تعميم مثال، خارج النطاق، والمعلومة المتغيرة. لكل جواب مسار رجوع إلى Claim ثم source/locator/quote hash؛ وعند غياب الدليل يكون الامتناع هو المخرج الصحيح.

**بوابة QA:** traces قابلة للحل، baseline محفوظ، denominator واضح، لا رابط دليل مكسور، ولا delta غير مقيمة.  
**توقف:** إجابة بلا trace، سؤال خارج snapshot عومل كحقيقة، QA مؤلف المخرج، أو status مبني على عدد الملفات فقط.

## 5. حارس عدم القفز

قبل أي كتابة، يفحص المنفذ هذه الشروط الآلية:

```text
required_predecessors(stage) ⊆ completed_predecessors
AND all_input_hashes == recorded_hashes
AND active_domain == assigned_domain عند extraction+
AND no_unresolved_blocker == true
AND output_paths ⊆ allowed_write_paths
```

إذا فشل شرط واحد، يسجل `BLOCK_<stage>_<reason>` ولا ينشئ مخرجًا يوحي بالنجاح. إذا كان المخرج الجزئي مفيدًا، يوضع بحالة `partial` مع `unresolved` ظاهر، لا بحالة قبول.

لا يسمح الحارس بالآتي:

- `manifest → concept` دون `READ`, Terms, Claims, Review.
- `route_done → master` دون snapshot/T/C/K.
- `source_done → domain_done` دون كل subdomains وR/T/C/K/M/QA.
- `candidate Claim → accepted Concept` دون review.
- `batch complete → domain_terms_complete` دون snapshot شامل.

## 6. سجل تشغيل توضيحي

> القيم التالية fixtures تعليمية، وليست سجلات حقيقية.

```yaml
workflow_id: WF_20261018_sales_pipeline_example
stage: review
source_id: SRC_EXAMPLE
domain: sales
snapshot_id: DOMAIN_SNAPSHOT_EXAMPLE
predecessor_refs: [ROUTE_EXAMPLE, READ_EXAMPLE, EXTRACT_EXAMPLE]
owner: reviewer-example
state: partial
inputs:
  read_coverage_ref: READ_EXAMPLE
  term_candidate_count: 4
  claim_candidate_count: 3
outputs:
  reviewed_units: [UNIT_1, UNIT_2]
  unresolved_units: [UNIT_3]
gates:
  R: pass
  T: in_progress
  C: blocked
  K: not_started
  M: not_started
  QA: not_started
blockers: [quote_locator_unverified_UNIT_3]
next_action: "إعادة فحص view والـquote قبل قبول Claim"
```

## 7. فحوص النجاح وأسباب التوقف

### 7.1 فحوص النجاح

- مساواة مجموعة manifest قبل/بعد المصائر، مع إظهار unresolved.
- تطابق المصدر والنسخة في bytes وSHA-256، واستقلالهما عن symlink/hardlink.
- `READ` يغطي view كاملًا بحدود Unicode نصف مفتوحة، ويفصل IO عن semantics.
- كل content unit لها disposition ومراجعها؛ لا Claim يتيم.
- Terms/Claims المرشحة لا تُقدّم على أنها accepted.
- Concept/Master links قابلة للحل إلى الدليل، مع scope/conflict/limits.
- كل Gate مسجل في النطاق الصحيح، مع reviewer وتاريخ وأدلة عند PASS.
- retrieval QA يقيس المقام، ويقبل الامتناع الصحيح، ويسجل trace والـbaseline.

### 7.2 أسباب التوقف

| السبب | الحالة | لا يجوز |
|---|---|---|
| `manifest_incomplete` | blocked | بدء route على مقام ناقص |
| `route_uncertain` | uncertain | نسخ primary أو extraction بالتخمين |
| `copy_integrity_failure` | quarantined/blocked | overwrite أو اعتبار REF نسخة |
| `semantic_gap` | partial/blocked | إعلان source_done |
| `pending_domain` | queued | Terms/Claims/Concepts/Master للمجال المنتظر |
| `candidate_unreviewed` | review_pending | بناء Concept/Master يعتمد عليه |
| `terms_gate_stale` | stale | بدء Master أو next domain |
| `retrieval_trace_missing` | blocked | إجابة تقريرية أو PASS |
| `delta_unassessed` | stale/blocked | تمديد صلاحية snapshot القديمة |

## 8. فحوص التنفيذ المقترحة وحدودها

يمكن للمنفذ استعمال `tools/wiki_quality.py` كفحص بنيوي مساعد، لكن يجب أن يسجل نسخته وأمره وما فحصه. لا يوصف نجاحه بأنه semantic read أو Gate T/C/K/M/QA. الفحوص التي تثبت هذه البوابات يجب أن تعيد حساب المقام والروابط والـlocators والـreviews، وتذكر العينة أو المجموعة الكاملة بوضوح.

## 9. حالة التسليم

صيغة الحالة:

```text
pipeline_status: partial
snapshot: DOMAIN_SNAPSHOT_EXAMPLE
last_completed_stage: review
measured: 2/3 units reviewed
blocked_at: C
reason: quote_locator_unverified_UNIT_3
not_claimed: domain_terms_complete, Master, domain_done
next_owner: reviewer-example
```

لا تعني عبارة «الخط حتى المرحلة X» أن المراحل اللاحقة ناجحة. عند إعادة التشغيل، استخدم `source_id + hash + stage + snapshot` كمفتاح idempotency، وأعد فحص predecessor بدل إعادة الكتابة العمياء.
