# 23 — أسئلة الاسترجاع وضمان الجودة والحالة الصادقة

**المراجعة:** 2026-10-18 — عقد تشغيل واختبار؛ لا يثبت تشغيل corpus أو اكتمال أي مجال.  
**النوع:** مواصفة retrieval QA، وتتبع الدليل، وقرار الحالة.  
**المراجع:** [05](05_RETRIEVAL_AND_EVALUATION.md)، [15](15_DOMAIN_COMPLETION_GATES.md)، [20](20_WIKI_OPERATING_SYSTEM.md)، [21](21_SOURCE_TO_KNOWLEDGE_PIPELINE.md)، [`AGENTS.md`](../AGENTS.md)، [`SCHEMA.md`](../SCHEMA.md).

> هذا النظام يحدد ما الذي يجوز أن تجيبه الويكي، وما الذي يجب أن تمتنع عنه، وكيف تثبت
> النتيجة. لا يطلب كشف chain-of-thought أو سلسلة الخواطر؛ المطلوب قرار مختصر، ومسار
> دليل قابل للفحص، وحالة وحدود مسجلة.

## 1. الغرض والحدود

يحوّل هذا النظام سؤال الاسترجاع إلى نتيجة قابلة لإعادة الفحص:

```text
سؤال استرجاع
  → تصنيف السؤال وتثبيت النطاق واللقطة
  → مرشحون من Concept/Claim
  → تحقق الحالة والتعارض والحداثة
  → Concept → Claim → Source → locator
  → answer | partial | abstain
  → اختبارات QA
  → مقام/بسط وحكم PASS/RETURN/BLOCKED/STALE
  → status صادق
```

لا يفعل هذا النظام الآتي:

1. لا ينشئ Claim أو Concept أو Master من سؤال غير مدعوم.
2. لا يحول `route_done` أو `source_done` أو نجاح أداة بنيوية إلى `domain_done`.
3. لا يستبدل سجل البوابة في `SCHEMA`: حالات Gate الرسمية هي
   `not_started|in_progress|pass|blocked|stale`.
4. لا يخفض المقام بإسقاط المصادر الصعبة أو أسئلة الامتناع أو الأقسام الفارغة.
5. لا يعلن اكتمال الويكي؛ أقصى ما يثبته هو نطاق اختبار محدد ولقطة محددة.

## 2. عقد سؤال الاسترجاع

### 2.1 تعريف السؤال

سؤال الاسترجاع ليس مجرد نص طلب المستخدم. هو سجل يحدد ما الذي سيعد إجابة صحيحة،
وما نطاق الدليل الذي يجب فحصه، وما الذي يجب أن يحدث عند غيابه. يثبت كل سؤال في
مجموعة تقييم مجمدة (`retrieval_eval_set`) قبل الحكم على النتيجة.

الحد الأدنى للسجل:

```yaml
retrieval_question_id: RQ_20261018_sales_001
question: "ما الشروط التي يذكرها المصدر لتطبيق هذا الأسلوب؟"
question_class: direct|synthesis|conflict|example_boundary|out_of_scope|volatile
domain: sales
snapshot_id: DOMAIN_SNAPSHOT_...
scope:
  concepts: [CPT_...]
  subdomains: [sales_calls]
  cutoff: 2026-10-18T00:00:00Z
expected_scope: "الشروط المذكورة في الأدلة المتاحة داخل اللقطة فقط"
expected_decision: answer|partial|abstain
oracle_refs: [CLM_..., CPT_...]
status: planned|tested|stale
```

`oracle_refs` لا يعني أن الإجابة يجب أن تكرر نصًا مخفيًا؛ هو مرجع المراجع إلى
المواد التي يختبر بها كفاية المسار. لا تُسجل فيه إجابة من دون دليل.

### 2.2 فئات أسئلة الحد الأدنى

يجب أن تتضمن مجموعة الاختبار، عند انطباق نطاق الويكي، الفئات التالية من [05]:

| الفئة | الغرض | الخطر الذي تكشفه |
|---|---|---|
| `direct` | سؤال يطابق Concept أو Claim واحدًا | إحالة خاطئة أو Claim يتيم |
| `synthesis` | سؤال يحتاج دمج أكثر من Concept أو Claim | تركيب آلية لم يثبتها أي دليل منفرد |
| `conflict` | سؤال تتعارض فيه مصادر أو Claims | إخفاء الخلاف أو اختيار طرف بلا سبب |
| `example_boundary` | سؤال يحاول تحويل مثال إلى قاعدة | تعميم غير مصرّح به |
| `out_of_scope` | سؤال خارج snapshot أو domain | إجابة من الذاكرة أو من مجال غير مفتوح |
| `volatile` | سؤال عن معلومة متغيرة زمنيًا | استخدام دليل قديم كأنه حالي |

يمكن إضافة فئات خاصة، لكن لا يجوز حذف فئة لازمة ثم الإبلاغ عن تغطية شاملة لمجموعة
الاختبار. إذا لم تنطبق فئة، يسجل السبب والنطاق بدل إسقاطها صامتًا.

### 2.3 تثبيت النطاق قبل الاسترجاع

قبل البحث عن جواب، يسجل المنفذ:

1. `snapshot_id` ونسخة `catalog` ووقت `cutoff`.
2. الـdomain والـsubdomain والقفل الفعليين، إن كان السؤال معرفيًا.
3. هل السؤال يطلب وصف ما يقوله مصدر معين أم توليفًا على مستوى Concept/Domain.
4. هل المطلوب «الآن» أو تاريخًا محددًا في سؤال متغير.
5. ما العناصر الذرية التي يجب أن يجيب عنها السؤال. لا تعد إجابة طويلة سؤالًا واحدًا
   إذا كان فيها خمس دعاوى مستقلة.
6. ما الذي سيعد فشلًا حرجًا: مثل غياب Claim يثبت النتيجة المركزية أو عدم حل locator.

لا يسمح تشابه الكلمات أو اسم الملف وحده بفتح نطاق جديد. سؤال خارج snapshot يبقى
`out_of_scope`، لا يتحول إلى سؤال داخل النطاق لأن مرشحًا قريبًا ظهر في الفهرس.

## 3. تنفيذ الاسترجاع من الدليل

### 3.1 ترتيب الاختيار

ينفذ QA، بالترتيب، ما يلي:

1. يثبت السؤال واللقطة والنطاق.
2. يرشح Concepts ذات صلة، ثم يقرأ `claim_refs` و`source_refs` بدل الاكتفاء بعنوان
   Concept.
3. يستبعد Claims المرشحة أو المرفوضة أو التي لا تحل مراجعها. Claims ذات
   `status: reviewed|accepted` هي التي يمكن استخدامها بعد فحص نطاقها؛ `candidate` لا
   تبني جوابًا معتمدًا.
4. يفحص `confidence` و`evidence_type` و`scope` و`what_it_does_not_prove`.
5. يفحص حداثة الـsnapshot والـdelta قبل صياغة الجواب.
6. يبني trace لكل دعوى ذرية، ثم يقرر `answer` أو `partial` أو `abstain`.

وجود Concept أو Master لا يكفي. إذا كان Concept `disputed`، فالحل ليس إخفاءه؛
بل عرض الخلاف والسياق أو الامتناع عن الحسم إذا كان السؤال يطلب اختيار طرف واحد.

### 3.2 قاعدة عدم القفز

المسار القياسي لكل دعوى مستخرجة من الويكي هو:

```text
Concept
  → Claim مراجَع
  → Source بهوية وبصمة
  → locator قابل للحل داخل view/READ
  → quote أو اشتقاق معلّم
```

لا يكفي أي من المسارات التالية:

```text
اسم الملف → جواب
Concept → Source بلا Claim
Claim بلا locator → جواب
Quote قريب لغويًا → قبول
Master قديم → سد فجوة المصدر الجديد
```

في سؤال يطلب نقل عبارة من مصدر مباشرة ولا يوجد Concept مناسب، يمكن استخدام
`trace_mode: direct_claim` مع `concept_ref: null` وسبب واضح. لا يسمى ذلك إجابة
Concept-level، ولا يعفي من `Claim → Source → locator`. أما كل جواب توليفي فيلزم
له المسار الكامل `Concept → Claim → Source → locator`.

### 3.3 نقل، توليف، واستنتاج

يفصل سجل الاسترجاع بين:

- **النقل:** ما يقوله المصدر أو Claim حرفيًا، مع `direct_quote` أو
  `reported_result` وlocator.
- **التوليف:** جمع Claims مراجعة متعددة؛ يجب أن يذكر كل Claim الذي ساهم في كل
  دعوى مركبة.
- **الاستنتاج:** نتيجة مشتقة من Claims؛ تسجل `evidence_type: inference` وعلاقة
  `derived_from` ولا تنشئ اقتباسًا وهميًا.
- **الفرضية:** احتمال أو اقتراح؛ تسجل `hypothesis` ولا تقدم كحقيقة.

المثال يظل `evidence_type: example` ويذكر نطاقه. لا يثبت المثال قاعدة عامة، حتى
لو كان النص واضحًا أو تكرر في مصدر واحد.

## 4. قرار answer / partial / abstain

### 4.1 تقسيم السؤال إلى دعاوى ذرية

كل عبارة تقريرية قابلة للتحقق هي دعوى ذرية. إذا سأل المستخدم «ما الآلية والشروط
والحدود؟»، يصبح السؤال ثلاث وحدات على الأقل. يسجل المنفذ لكل وحدة:

```yaml
assertion_id: A_001
required: true
text: "الأسلوب يتطلب الشرط X"
criticality: core|supporting
trace_refs: [TRACE_001]
support: supported|unsupported|disputed|out_of_scope|stale
```

لا تعالج الدعوى غير المدعومة بحذفها من العد ثم تسمية بقية الإجابة كاملة.

### 4.2 `answer`

يكون القرار `answer` عندما:

1. كل الدعاوى الجوهرية المطلوبة في السؤال لها trace صالح.
2. كل trace يحل إلى Claim مراجَع ثم Source وlocator في نطاق السؤال.
3. لا يوجد تعارض مؤثر مخفي أو delta غير مقيم.
4. حدود الدليل متوافقة مع صياغة الجواب؛ لا يوجد تعميم من مثال.
5. اجتازت النتيجة اختبارات quote/schema/link/conflict/coverage المطلوبة.

`answer` يعني أن هذا السؤال أجاب عنه الاختبار في نطاقه، لا أن الويكي كلها صحيحة
أو مكتملة.

### 4.3 `partial`

يكون القرار `partial` عندما يمكن دعم جزء محدد من السؤال ولا يمكن دعم جزء آخر، أو
عندما يوجد تعارض معلّم يمنع جوابًا واحدًا، مع بقاء جزء قابل للعرض. يجب أن يذكر
الجواب صراحة:

- ما الذي يثبته الدليل.
- ما الجزء غير المدعوم أو المتعارض.
- هل الجزء الناقص خارج النطاق، أم بلا Claim، أم stale.
- ما الذي يلزم لاستكماله.

لا تستخدم `partial` كاسم مخفف لـ`answer`، ولا تحوله إلى PASS للمجموعة الكاملة.
إذا كان الجزء غير المدعوم هو الدعوى المركزية، فالأصح `abstain` لا `partial`.

### 4.4 `abstain`

يكون القرار `abstain` عندما لا يوجد دليل كافٍ على الدعوى المطلوبة، أو لا يمكن حل
مسار الدليل، أو السؤال خارج النطاق، أو أصبحت اللقطة قديمة بالنسبة للطلب. الامتناع
الصحيح ليس فشلًا؛ هو مخرج مطلوب يمنع اختلاق المعرفة.

يجب أن يذكر الامتناع سببًا واحدًا أو أكثر من الأسباب القابلة للتتبع، مثل:

```text
insufficient_evidence
missing_locator
unresolved_conflict
out_of_scope
stale_snapshot
unreviewed_claim
coverage_gap
```

لا يبرر `abstain` كتابة جواب تخميني بعده. يمكن ذكر ما هو معروف في سياق منفصل فقط
إذا كان له trace، مع إبقاء الدعوى الأصلية ممتنعًا عنها.

### 4.5 جدول القرار

| حالة الدعاوى المطلوبة | القرار | ما يجب فعله |
|---|---|---|
| كلها مدعومة وtrace صالح | `answer` | قدم جوابًا بالنطاق والروابط |
| بعضها مدعوم وبعضها غير مدعوم، والجزء المركزي قابل للتحديد | `partial` | افصل المدعوم عن الفجوة |
| لا دعوى جوهرية مدعومة، أو الجزء المركزي غير قابل للإثبات | `abstain` | امتنع وسجل السبب |
| Claims متعارضة لكن الطرفين موثقين والسؤال عن الخلاف | `answer` بصيغة خلاف | اعرض الطرفين وشروطهما |
| Claims متعارضة والسؤال يطلب «الحقيقة الوحيدة» بلا معيار حسم | `partial` أو `abstain` | لا تختَر طرفًا بلا دليل إضافي |
| سؤال متغير وcutoff أقدم من المطلوب | `abstain` أو `partial` | اذكر تاريخ الدليل ولا تسميه حاليًا |

## 5. trace-back قابل للفحص

### 5.1 invariants المسار

لكل دعوى في جواب `answer` أو الجزء المدعوم من `partial`:

1. يوجد `concept_ref` إن كانت الدعوى توليفًا مفاهيميًا.
2. كل Concept يشير إلى Claim واحد أو أكثر بحالة `reviewed` أو `accepted`.
3. كل Claim يشير إلى `source_id` صالح في سجل Source.
4. كل Source يملك `locator` قابلًا للحل داخل النسخة/view المرتبطة بـ`READ_*`.
5. كل quote منقول يطابق النص والبصمة والحدود؛ والاستنتاج يشير إلى Claims السابقة
   ولا يتظاهر بأنه اقتباس.
6. يسجل `scope` وما لا يثبته الدليل عند الحاجة.

### 5.2 سجل trace قصير

```yaml
trace_id: TRACE_20261018_001
retrieval_question_id: RQ_20261018_sales_001
assertion_id: A_001
trace_mode: concept_synthesis
concept_ref: CPT_sales_example
claim_refs:
  - claim_id: CLM_20261010_sales_003
    source_id: SRC_20261001_source_a
    locator: line 120-128
    read_coverage_ref: READ_20261018_source_a
    evidence_type: direct_quote
    evidence_quote: "النص الحرفي..."
    quote_hash: sha256:<64-hex>
    quote_offset:
      unit: unicode_codepoint
      start: 120
      end: 145
      bounds: half_open
    scope: "هذا المثال في سياق المكالمات الواردة"
    what_it_does_not_prove: "لا يثبت نجاح الأسلوب في كل الصناعات"
source_id: SRC_20261001_source_a
locator: line 120-128
result: supports
```

لا حاجة لتسجيل سلسلة التفكير الداخلية للوصول إلى `supports`. يكفي تسجيل قرار
قابل للفحص ومراجع الدليل. إذا احتاجت الدعوى أكثر من Claim، يكرر سجل `claim_refs`
لكل Claim، لا يوضع مصدر واحد شكليًا لتغطية بقية الدعوى.

### 5.3 فشل المسار

يصبح trace فاشلًا إذا:

- كان Claim موجودًا لكن `source_id` غير موجود.
- كان المصدر موجودًا لكن locator لا يحل داخل view الصحيحة.
- كان quote hash مختلفًا أو offset خارج `[0, view.length)`.
- كان Concept يشير إلى Claim `candidate` ويعرضه كحقيقة.
- غاب scope المؤثر أو غابت حدود ما لا يثبته الدليل.
- تغيّر المصدر أو snapshot بعد إنشاء trace ولم يُعاد تقييمه.

فشل trace لدعوى مركزية يمنع `answer` ويقود إلى `RETURN` أو `BLOCKED` أو `STALE`
بحسب سبب الفشل.

## 6. اختبارات retrieval QA

كل اختبار يسجل: `test_id`، النطاق، `snapshot_id`، الأداة وإصدارها أو طريقة
الفحص، وقت التنفيذ، المقام، البسط، النتيجة، والأخطاء. لا يكفي قول «اجتاز» دون
تحديد ما فُحص.

### 6.1 اختبار الاقتباس `quote`

**السؤال:** هل الاقتباس هو النص الذي يدعيه Claim فعلًا؟

يفحص:

1. تطابق `evidence_quote` مع view المرتبطة بـ`read_coverage_ref`.
2. صحة `quote_offset` بوحدة Unicode code point وبحدود نصف مفتوحة `[start,end)`.
3. إعادة حساب `quote_hash` ومطابقته.
4. حل `locator` في المصدر والنسخة الصحيحة، لا في ملف مشابه أو Master قديم.
5. وجود `what_it_does_not_prove` عندما يكون النقل قابلًا لتعميم مضلل.

إذا كان `evidence_type: inference`، لا يطلب الفحص اقتباسًا مصطنعًا؛ يطلب Claims
مقدمة قابلة للحل وعلاقة `derived_from` ووسمًا صريحًا بأنه استنتاج.

**الفشل:** quote غير مطابق، hash مختلف، offset خارج الحدود، أو اقتباس مثال مقدم
كقاعدة.

### 6.2 اختبار المخطط `schema`

يفحص أن كل سجل في ناتج retrieval QA، وكل سجل مرجعي استعمله، يطابق `SCHEMA`:

- الحقول الإلزامية موجودة وبالنوع المتوقع.
- enums ثابتة ولا تُستبدل بحالات مخترعة.
- `source_id`, `claim_id`, `concept_id`, `read_coverage_ref` و`gate_refs`
  تحمل صيغًا ومراجع قابلة للحل.
- `locator`, `quote_offset`, `scope` و`what_it_does_not_prove` لا تُملأ بقيم
  وهمية أو عامة.
- `decision` (`answer|partial|abstain`) و`verdict` (`PASS|RETURN|BLOCKED|STALE`)
  حقلا نتيجة تشغيل، وليسا بديلًا عن `Source.status` أو Gate status.

نجاح أداة schema لا يثبت صحة الدليل أو القراءة الدلالية؛ هو يثبت شكل السجل فقط.

### 6.3 اختبار الروابط `link`

يفحص كل مرجع مذكور في النتيجة، لا عينة النجاح فقط:

1. كل `concept_ref` يحل إلى Concept موجود.
2. كل `claim_ref` يحل إلى Claim موجود ومراجعته مناسبة للقرار.
3. كل `source_id` يحل إلى Source، و`source_path` والنسخة مستقلان وصالحان.
4. كل `locator` يحل داخل المصدر/view المحددة، و`READ_*` و`quote_hash` موجودان.
5. كل رابط Markdown أو wikilink في الوثيقة يشير إلى ملف أو عنوان موجود.
6. كل `gate_ref` و`retrieval_eval_ref` و`delta_ref` يحل داخل نطاقه.

الرابط المكسور لا يصبح سليمًا لأن الملف الهدف موجود باسم قريب. يسجل الفحص المرجع
المكسور ومساره، ويمنع PASS إذا كان المرجع مؤثرًا في جواب أو بوابة.

### 6.4 اختبار التعارض `conflict`

يفحص أن الخلاف المدعوم ظاهر بدل دمجه صامتًا:

- يحدد Claims المتعارضة والعلاقة `contradicts` أو `conflict_refs`.
- يحتفظ بسياق كل طرف ونطاقه وlocator وثقته وتاريخه.
- لا يرفض أحد الطرفين لمجرد غياب الإجماع.
- لا يقدم أحد الطرفين بوصفه حقيقة عامة إذا كان الدليل يدعمه في نطاق أضيق.
- إذا كان الخلاف مؤثرًا في سؤال «أيّهما صحيح؟»، تكون النتيجة `partial` أو
  `abstain` ما لم يوجد معيار حسم مدعوم.

وجود تعارض موثق لا يفشل C/K/M تلقائيًا؛ الذي يفشلها هو تعارض مخفي، أو طرف بلا
تتبع، أو جواب يتجاهل أثر الخلاف.

### 6.5 اختبار التغطية `coverage`

التغطية لها مستويان منفصلان:

1. **تغطية القراءة:** `READ_*` يثبت `bytes_read == bytes_expected` وEOF وسلامة
   البصمة من جهة IO، واتحاد segments دلالية متصلة من `0` إلى `view.length` من جهة
   الفهم. EOF وحده ليس قراءة دلالية كاملة.
2. **تغطية التقييم:** مجموعة retrieval questions المجمدة تشمل الفئات والنطاقات
   المطلوبة، وتشمل أسئلة الامتناع والخلاف وخارج النطاق، لا الأسئلة السهلة فقط.

يفشل الاختبار إذا خُفض المقام إلى الملفات أو الأسئلة التي أعادت نتيجة ناجحة، أو
إذا استُخدمت دفعة صغيرة على أنها snapshot شاملة، أو إذا بقي `unread_range` أو
`unresolved_candidate` مؤثر بلا مصير واضح.

### 6.6 اختبار trace والقرار

هذا اختبار جامع يربط كل assertion بالحكم:

- `answer`: كل assertion المطلوبة ذات trace صالح.
- `partial`: كل assertion معروض كمدعوم له trace، وكل assertion غير مدعوم معلّم
  ومفصول عن الجواب.
- `abstain`: لا توجد دعوى تقريرية غير مدعومة؛ السبب مسجل.

لا يحتسب جوابًا صحيحًا لمجرد أن نصه معقول أو أن أقرب Concept مناسب لغويًا.

## 7. المقام والبسط

### 7.1 القاعدة العامة

كل رقم في تقرير QA يذكر:

```yaml
metric: trace_complete_rate
scope: retrieval_eval_set
snapshot_id: DOMAIN_SNAPSHOT_...
unit: assertion
numerator: 17
denominator: 20
ratio: 0.85
excluded: []
measured_at: 2026-10-18T12:00:00Z
```

المقام هو المجتمع المحدد قبل الاختبار، والبسط هو العناصر من المجتمع نفسه التي
حققت الشرط. لا يتغير المقام بعد رؤية النتائج. إذا كان المقام صفرًا، تسجل `N/A`
مع السبب؛ لا تسجل 100%.

### 7.2 المقامات الإلزامية حسب المقياس

| المقياس | المقام | البسط |
|---|---|---|
| تغطية الجرد | كل مرشحي manifest قبل المصائر داخل cutoff | المرشحون ذوو disposition موثق ومراجع |
| تغطية القراءة الدلالية | كل units/segments المطلوبة في snapshot والنطاق | units/segments ذات تغطية ومراجعة ومصير |
| صحة trace | كل الدعاوى الذرية المعروضة في أجوبة التقييم | الدعاوى ذات Concept→Claim→Source→locator صالح |
| اكتمال الاقتباس | كل Claims منقولة أو قابلة للاقتباس المستعملة | Claims ذات quote/offset/hash مطابق |
| حل الروابط | كل الروابط والمراجع المصدرة في الناتج | الروابط التي حلت إلى الهدف الصحيح |
| صحة الإجابة | كل retrieval questions في eval set | الأسئلة التي تطابق قرار oracle وجوابها وحدودها |
| الامتناع الصحيح | كل أسئلة eval المتوقعة غير قابلة للإجابة | الأسئلة التي امتنعت دون ادعاء زائد وبسبب صحيح |
| تغطية الفئات | كل الفئات المطلوبة في عقد مجموعة الاختبار | الفئات التي لها سؤال منفذ ومراجع |
| معالجة التعارض | كل التعارضات المؤثرة المكتشفة في النطاق | التعارضات التي حفظ طرفاها وسياقهما وأثرهما |

لا يجوز استخدام «عدد الملفات» مقامًا لصحة الإجابات، ولا استخدام «عدد الأجوبة»
مقامًا لتغطية المصدر، ولا دمج `partial` و`answer` في بسط واحد دون تعريف المقياس.

### 7.3 مقاييس القرار المقترحة

يمكن تسجيل المقاييس التالية، كل واحد بوحدته الصريحة:

```text
answer_accuracy = correct_answer_questions / all_eval_questions
partial_coverage = supported_atomic_assertions / all_required_atomic_assertions
correct_abstention_rate = correct_abstentions / expected_abstention_questions
trace_coverage = valid_traced_assertions / all_material_assertions
link_resolution = resolved_refs / all_emitted_refs
```

`correct_abstention_rate` لا يبرر إخفاء الأسئلة التي كان ينبغي الإجابة عنها؛ تلك
تبقى في مقام `answer_accuracy`. ويمكن أن تكون الإجابة الممتنعة صحيحة لسؤال خارج
النطاق، وخاطئة لسؤال داخل النطاق له Claim صالح.

### 7.4 حدود القياس

- يذكر كل رقم `scope` و`snapshot_id` ووقت القياس والمراجع المستبعدة.
- لا تخلط نتائج snapshot قديمة مع جديدة في مقام واحد دون delta موثق.
- لا تحول نسبة مرتفعة في مجموعة صغيرة إلى حكم على domain كامل.
- لا تعلن «100%» إذا كان هناك `unknown`, `unresolved`, `not_measured` أو عينة
  غير معلنة في المقام.
- إذا اختلفت أداة بنيوية عن الفحص الدلالي، تعرض النتيجتان منفصلتين مع حدود كل
  أداة؛ لا يختار التقرير الرقم الملائم فقط.

## 8. أحكام PASS / RETURN / BLOCKED / STALE

هذه قيم `verdict` تشغيلية لنتيجة retrieval QA. ليست بديلًا عن enums المصدر أو
البوابة، ولا تضيف قيمة `RETURN` إلى Gate status.

| الحكم | المعنى | شرطه | الإجراء التالي |
|---|---|---|---|
| `PASS` | الاختبار المحدد اجتاز شروطه | كل الاختبارات المطلوبة في النطاق نجحت، والمقام والبسط ومراجع المراجع موجودة، ولا blockers | انشر النتيجة في نطاقها فقط، وسلّمها للمسؤول |
| `RETURN` | المخرج قابل للإصلاح بإعادة العمل | خلل محدد محليًا مثل quote أو رابط أو صياغة scope، ولا يوجد اعتماد خارجي يمنع الإصلاح | أعده إلى مالك المخرج، ولا تسميه قبولًا أو PASS |
| `BLOCKED` | لا يمكن الحكم أو التنفيذ بأمان | مدخل مفقود، owner/reviewer غير متاح، نطاق غامض، فجوة تغطية مؤثرة، أو دليل غير قابل للتحقق | احفظ checkpoint والمانع والمالك والخطوة التالية؛ لا تخمّن |
| `STALE` | حكم سابق فقد صلاحيته | تغير مصدر أو hash أو snapshot أو catalog أو delta تمس الدليل | ألغِ صلاحية الحكم، اربطه بـdelta، وأعد التقييم |

### 8.1 العلاقة مع حالة Gate

| `verdict` | Gate status المناسب عادةً | ملاحظة |
|---|---|---|
| `PASS` | `pass` | فقط إذا كان نطاق الـGate نفسه مكتملًا وله reviewer وتاريخ وأدلة |
| `RETURN` | `in_progress` أو `blocked` | يتحدد بالمانع؛ `RETURN` لا يعني نجاحًا جزئيًا |
| `BLOCKED` | `blocked` | يذكر blocker قابلًا للإزالة أو `external_dependency` |
| `STALE` | `stale` | يذكر `delta_id` أو سبب تغير اللقطة |

نجاح retrieval QA لمجموعة أسئلة لا يرفع T أو C أو K أو M أو QA العامة تلقائيًا.
وبالمثل، PASS لبوابة محلية لا يثبت PASS لنطاق domain أو snapshot أوسع.

### 8.2 متى تكون المشكلة RETURN ومتى BLOCKED؟

- `RETURN`: كل المدخلات متاحة، والمشكلة قابلة للإصلاح داخل المخرج المملوك، مثل
  locator مكتوب خطأ مع بقاء المصدر متاحًا، أو صياغة توحي بتعميم مثال.
- `BLOCKED`: لا يمكن إصلاح النتيجة دون مدخل أو قرار من مالك آخر، مثل مصدر مفقود،
  snapshot غير مثبتة، reviewer مستقل غير متاح، أو تعارض صلاحيات.
- إذا كان التغيير الخارجي قد أفسد حكمًا سابقًا، فالحكم `STALE` أولًا، حتى لو كان
  الإصلاح المتوقع سهلًا.

## 9. صياغة status صادق

### 9.1 الحقول الدنيا

كل تسليم retrieval QA يسجل، بقدر النطاق المأذون:

```yaml
workflow_id: WF_20261018_retrieval_qa_001
retrieval_eval_ref: RETRIEVAL_20261018_001
scope: "sales / DOMAIN_SNAPSHOT_... / 12 questions"
snapshot_id: DOMAIN_SNAPSHOT_...
question_count: 12
question_classes: [direct, synthesis, conflict, example_boundary, out_of_scope, volatile]
last_completed_step: tests
decisions:
  answer: 5
  partial: 3
  abstain: 4
metrics:
  correct_questions: {numerator: 10, denominator: 12, unit: question}
  valid_traces: {numerator: 18, denominator: 20, unit: assertion}
tests:
  quote: pass
  schema: pass
  link: fail
  conflict: pass
  coverage: pass
verdict: RETURN
gate_status: in_progress
blockers: []
not_claimed: [domain_done, wiki_complete, all_sources_processed]
next_owner: qa-index
next_action: "إصلاح الرابط المكسور ثم إعادة فحص link وtrace"
checked_at: 2026-10-18T12:00:00Z
```

### 9.2 صيغة التسليم الدنيا

> **النطاق:** ...؛ **اللقطة:** ...؛ **مجموعة الأسئلة:** ...؛ **القرارات:** ...؛
> **المقاس:** البسط/المقام، بوحدة ...؛ **الاختبارات:** ...؛ **الحكم:** ...؛
> **ما ثبت:** ...؛ **الفجوات:** ...؛ **ما لم يثبت:** ...؛ **المالك والخطوة التالية:** ...

صياغة صحيحة:

> «اجتازت 10 من 12 سؤالًا في مجموعة `RET...` داخل snapshot `DOMAIN...`، مع
> trace صالح لـ18 من 20 دعوى ذرية. فشل رابط واحد، لذلك الحكم `RETURN`. يثبت ذلك
> هذه المجموعة فقط، ولا يثبت `domain_done` أو اكتمال الويكي.»

صياغة غير صحيحة:

> «تمت معالجة الويكي واكتمل الاسترجاع.»

العبارة الثانية محظورة ما لم توجد أدلة إغلاق مستقلة بالنطاق الصحيح، وحتى عند وجود
`domain_done` لا يجوز تحويل إغلاق مجال واحد إلى اكتمال الويكي كلها.

## ما يثبت

يثبت retrieval QA، في النطاق المسجل فقط، ما يلي:

1. أن سؤالًا أو مجموعة أسئلة محددة عولجت وفق snapshot وcutoff معلنين.
2. أن الدعوى المعروضة لها مسار قابل للحل من Concept إلى Claim إلى Source إلى
   locator، أو أنها نقل مباشر موسوم بوضوح ومساره Claim إلى Source إلى locator.
3. أن الاقتباس المرفق يطابق view والبصمة والحدود، عندما يكون الاقتباس منطبقًا.
4. أن الروابط التي فُحصت حلت إلى الأهداف الصحيحة في وقت الفحص.
5. أن الخلافات التي اكتشفها الفحص لم تُخفَ، وأن الامتناع أو الجزء الجزئي سُجلا
   بدل ملء الفراغ بتخمين.
6. أن نسب البسط/المقام تصف المجتمع المعلن، لا مجتمعًا انتقائيًا بعد رؤية النتائج.
7. أن `PASS` يعني نجاح شروط الاختبار المحدد مع reviewer وتاريخ وأدلة، لا نجاح
   كل طبقات الويكي.

## ما لا يثبت

لا يثبت هذا النظام، بمفرده:

1. اكتمال كل مصادر الويكي أو كل subdomains أو كل Terms/Claims.
2. `domain_done` أو اجتياز T/C/K/M/QA العامة من مجرد نجاح أسئلة الاسترجاع.
3. صحة Claim لم يُراجع، أو تعريفًا لا يملك مصدرًا وموضعًا.
4. أن Concept أو Master صالح خارج scope أو بعد cutoff أو بعد ظهور delta.
5. أن نسبة عالية في عينة أو batch تمثل snapshot شاملة.
6. أن EOF أو تطابق hash يثبت الفهم الدلالي أو استخراج كل الوحدات.
7. أن المثال قاعدة، أو أن inference اقتباس مباشر، أو أن غياب التعارض في عينة
   يعني عدم وجوده في corpus.
8. أن `partial` يمكن عرضه كإجابة كاملة، أو أن `RETURN` يساوي PASS.
9. أن أداة `wiki_quality.py` أو أي فحص schema بنيوي وحده يثبت صحة التتبع أو
   القراءة الدلالية أو بوابات T/C/K/M/QA.
10. أن وجود هذا الملف أو أي تقرير حالة يعلن اكتمال الويكي.

## ما يجب تسجيله

### 1. قبل التنفيذ

- `workflow_id` و`retrieval_eval_ref` ومالك المهمة.
- نص كل سؤال وتصنيفه و`expected_scope` و`expected_decision`.
- `snapshot_id` وcatalog revision وcutoff وdomain/subdomain.
- المقام المحدد مسبقًا، وقواعد اعتبار الدعوى مركزية أو مساندة.
- مسارات القراءة والكتابة المسموحة؛ لا يكتب QA في `raw/`.

### 2. أثناء الاسترجاع

- المرشحون المختارون والمستبعدون وسبب الاستبعاد.
- حالة كل Concept وClaim وSource و`READ_*` المستعمل.
- trace لكل assertion، مع source وlocator والاقتباس/hash عند الانطباق.
- scope وconfidence وevidence_type و`what_it_does_not_prove`.
- التعارضات، والـdelta، ومواطن الغموض، دون إخفائها من المقام.

### 3. بعد الفحص

- نتيجة كل اختبار: quote/schema/link/conflict/coverage/trace.
- الأمر أو الأداة وإصدارها ووقت التنفيذ والنطاق والعينة أو المجموعة الكاملة.
- البسط والمقام والوحدة والنسبة، وحالة `N/A` إن كان المقام صفرًا.
- قرار كل سؤال: `answer|partial|abstain` وسبب الامتناع أو النقص.
- `verdict`: `PASS|RETURN|BLOCKED|STALE`، وحالة Gate الرسمية إن وجدت.
- reviewer المستقل، أو سبب عدم توفره.
- `blockers`, `pending_delta_ids`, `not_claimed`, `next_owner`, و`next_action`.
- checkpoint قابل للاستئناف؛ لا يمحى سجل retry أو الحكم السابق.

## 10. قوالب قصيرة

### 10.1 قالب سؤال

```yaml
retrieval_question_id: RQ_...
question: "..."
question_class: direct|synthesis|conflict|example_boundary|out_of_scope|volatile
snapshot_id: DOMAIN_SNAPSHOT_...
scope: "..."
expected_scope: "..."
expected_decision: answer|partial|abstain
oracle_refs: []
```

### 10.2 قالب نتيجة السؤال

```yaml
retrieval_question_id: RQ_...
decision: answer|partial|abstain
assertions:
  - assertion_id: A_...
    text: "..."
    support: supported|unsupported|disputed|out_of_scope|stale
    trace_refs: [TRACE_...]
answer_scope: "..."
limitations: ["..."]
```

### 10.3 قالب سجل فحص

```yaml
test_id: TEST_20261018_link_001
test_kind: quote|schema|link|conflict|coverage|trace
scope: retrieval_eval_set
snapshot_id: DOMAIN_SNAPSHOT_...
tool: "اسم الأداة أو verifier"
tool_version: "..."
unit: reference|claim|assertion|question|segment
numerator: 0
denominator: 0
result: pass|fail|not_measured
failures: []
checked_at: 2026-10-18T12:00:00Z
```

### 10.4 قالب الحكم والحالة

```yaml
verdict: PASS|RETURN|BLOCKED|STALE
gate_status: pass|in_progress|blocked|stale
evidence_refs: [TRACE_..., TEST_...]
measured:
  numerator: 0
  denominator: 0
  unit: "..."
blockers: []
pending_delta_ids: []
not_claimed: [domain_done, wiki_complete]
next_owner: "..."
next_action: "..."
```

### 10.5 قالب status عربي قصير

```text
الحالة: [PASS|RETURN|BLOCKED|STALE].
النطاق: [domain/snapshot/eval-set].
المقاس: [البسط]/[المقام] [الوحدة].
القرار: [answer/partial/abstain]؛ الاختبارات: [quote/schema/link/conflict/coverage].
يثبت: [...]. لا يثبت: [...].
المانع أو الفجوة: [...]. المالك والخطوة التالية: [...].
```

## 11. إجراء التشغيل المختصر

1. جمّد مجموعة الأسئلة والـsnapshot وسجل المقام قبل تشغيل الاسترجاع.
2. صنّف كل سؤال، وحدد الدعاوى الذرية والدعوى المركزية وحدود الإجابة.
3. استرجع Concepts ثم Claims المراجعة، ولا تستخدم المرشحين كحقائق.
4. ابنِ trace قابلًا للحل حتى Source وlocator، وافحص quote/hash عند الانطباق.
5. افحص الحالة والحداثة والتعارض والتغطية قبل صياغة النص.
6. قرر `answer` أو `partial` أو `abstain` لكل سؤال، وسجل السبب.
7. شغّل quote/schema/link/conflict/coverage/trace ضمن النطاق نفسه.
8. احسب البسط والمقام لكل مقياس، ولا تغير المقام بعد ظهور النتيجة.
9. عين `PASS` أو `RETURN` أو `BLOCKED` أو `STALE`، واربطه بحالة Gate الرسمية
   المناسبة دون اختراع enum جديد.
10. سلّم status صادقًا يذكر ما ثبت وما لم يثبت والفجوة والمالك والخطوة التالية.

إذا فشل شرط واحد مؤثر، لا تُكمل الصياغة على أمل أن يصلحها الاتساق اللغوي. احفظ
الأدلة والـcheckpoint، وارجع بالمخرج أو أوقفه أو أبطل صلاحيته بحسب الحكم. الهدف هو
إجابة يمكن تتبعها أو امتناع يمكن تفسيره، لا مظهر اكتمال لا يثبته الدليل.
