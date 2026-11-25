# 24 — عقد تسليم الوكيل والاسترداد

**المراجعة:** 2026-10-18  
**النوع:** عقد تنسيق وتسليم واسترداد قابل لإعادة التشغيل  
**النطاق:** Commander وWorker وReviewer وQA في تشغيلات الويكي  
**المراجع الحاكمة:** `AGENTS.md`، `SCHEMA.md`، والأنظمة 11 و12 و16 و20.

> هذه الوثيقة تحدد كيف يُكلَّف الوكيل، وكيف يملك الملفات، وكيف يثبت ما أنجزه،
> وكيف يُستأنف العمل بعد انقطاع أو فشل. لا تنشئ Snapshot ولا تغيّر `config` ولا
> تمنح أي بوابة `PASS` بمفردها. المطلوب قرارات تشغيلية وأدلة قابلة للفحص، وليس
> كشف chain-of-thought أو سلسلة خواطر داخلية.

---

## 1. الغرض والعقد المختصر

يجب أن يكون كل تشغيل قابلاً للإجابة عن الأسئلة التالية دون الرجوع إلى ذاكرة
الوكيل:

1. من يملك القرار والملف الآن؟
2. ما المجال والـsnapshot والدفعة والوحدات التي يشملها العمل؟
3. ما المسارات المسموح قراءتها وكتابتها، وما المسارات المحظورة؟
4. ما آخر حد آمن تم تثبيته على القرص؟
5. ما الذي ثبت فعلاً، وما الذي لم يثبت، وما الذي يحتاج إلى مالك تالٍ؟
6. هل الفشل نقلٌ أو صلاحية أو مهلة أو schema أو محتوى؟
7. كيف يستأنف وكيل آخر من دون إعادة إنتاج وحدات مقبولة أو الكتابة فوق عمل غير
   مملوك؟

القاعدة التشغيلية الأساسية:

> **الرسالة تقريرٌ عن العمل؛ الملفات والفحوص والحالة المملوكة هي الدليل.**

لا ينتقل التشغيل إلى `validated` أو `delivered` لمجرد أن Agent أرسل رسالة تقول
`done` أو `PASS`. ولا يرفع Worker حالة مجال أو يغير القفل أو يعلن
`domain_done`؛ يسلّم الأدلة والاقتراح فقط، ويملك Commander معاملة الحالة بعد
استكمال الفحوص المستقلة.

---

## 2. مبادئ غير قابلة للتفاوض

1. **نطاق مكتوب قبل الكتابة:** لا يبدأ التنفيذ قبل وجود `run_id` ومالك واضح
   وهدف ودفعة ومسارات قراءة وكتابة ومعايير قبول.
2. **مالك كتابة واحد لكل مسار:** لا يكتب عاملان الملف نفسه أو مجلدين متداخلين
   في الوقت نفسه، حتى لو كانت الكتابة append-only أو قال أحدهما إنه سيكتب
   «سطرًا واحدًا فقط».
3. **الخام immutable:** لا يُعدل أو يُنقل أو يُعاد تسميته أو يُحذف أي ملف في
   `raw/`؛ يثبت أي تصحيح أو نسخة جديدة بهوية وبصمة جديدتين.
4. **مجال معرفي نشط واحد:** لا يسمح بتشغيل Terms/Claims/Concepts/Masters
   لمجال `pending`، ولا بمجالين نشطين أو كتابة معرفية خلفية لمسار آخر.
5. **الحالة لها مالك واحد:** `config/processing_order.json` والقفل وقرار الانتقال
   ملك Commander وحده، وبـrevision و`fencing_token` صالحين.
6. **كل وحدة لها هوية مستقرة:** تستخدم تركيبة مثل
   `snapshot_id + source_id + unit_id + segment_start + segment_end` لمنع
   التكرار والخلط بين محاولتين.
7. **الفشل لا يُخفى:** يبقى `blocked` أو `partial` أو `failed` أو `stale`
   ظاهرًا مع السبب والمالك والخطوة التالية.
8. **الفحص البنيوي ليس فحصًا دلاليًا:** نجاح أداة مثل `tools/wiki_quality.py`
   لا يثبت القراءة الكاملة أو T/C/K/M/QA أو صحة الاقتباس والحدود.
9. **المثال ليس قاعدة:** لا يتحول رقم أو قصة أو مثال إلى Claim عام دون دليل
   مستقل ونطاق صريح.
10. **لا تخمين عند نقص المدخلات:** غياب schema أو صلاحية أو hash أو checkpoint
    يجعل الحالة `blocked`، ولا يبرر إنشاء قيمة بديلة من ذاكرة النموذج.
11. **لا chain-of-thought:** تسجل الخلاصة والقرار والدليل والحدود والخطوة التالية؛
    لا تسجل الخواطر الداخلية أو بدائل التفكير التفصيلية.
12. **الاستئناف متحفظ:** لا تُعاد الوحدة إلا بعد فحص ما إذا كانت مخرجاتها
    موجودة ومكتملة ومثبتة على نفس المدخلات والrevision؛ وجود ملف وحده لا يكفي.

---

## 3. الأدوار والصلاحيات

الأدوار وظائف تشغيلية وليست إذنًا ضمنيًا لفتح مسارات جديدة. يمكن أن يؤدي الشخص
نفسه أكثر من وظيفة فقط إذا بقيت حدود الملكية واختبار الاستقلال واضحة؛ لا يجوز
للمؤلف أن يحسب مراجعته الذاتية QA مستقلًا.

| الدور | يملك ويُنفِّذ | لا يملك ولا يفعل | التسليم الإلزامي |
|---|---|---|---|
| **Commander** | يثبت الطلب والنطاق، يقرأ حالة `config`، يوزع الدفعات، يملك القفل و`state_revision` و`fencing_token`، يفتح ويغلق التكليف، وينفذ انتقال الحالة | لا يخترع دليلًا، ولا يعتمد مخرجًا بلا فحص مستقل، ولا يوسّع مسار Worker أو يملأ فجوة محتوى | تكليف كامل، سجل قرار، توزيع ملكية، قرار انتقال أو `blocked` |
| **Worker** | ينفذ دفعة محددة، يقرأ المدخلات المصرح بها، يكتب فقط مخرجاته وcheckpoints داخل `allowed_write_paths`، ويربط كل وحدة بالدليل | لا يكتب `raw/` أو `config` أو ملفات عامل آخر، لا يستخرج معرفة من مجال `pending`، لا يعلن QA أو `domain_done` | مخرجات مؤرخة وبصمات، قياسات، أوامر وexit codes، checkpoint، وتسليم `READY_FOR_REVIEW` أو `RETURN` |
| **Reviewer** | يراجع كل وحدة ضمن النطاق، يطابق الاقتباس والـlocator والنوع والنطاق، يثبت التوترات والمصائر، ويسجل قرار كل وحدة | لا يمحو الدليل أو يعيد كتابة الخام، لا يحول رأيه إلى مصدر، ولا يراجع مخرجاته كطرف مستقل | سجل مراجعة، قرار لكل وحدة، findings، و`PASS_REVIEW` أو `RETURN` |
| **QA** | يفحص النطاق والروابط والبصمات والـschema والتغطية والـdelta والاسترجاع حسب التكليف، ويصدر hold/pass مستقلًا | لا يوسّع النطاق، ولا يصلح بصمت مخرج Worker، ولا يخفي finding، ولا يرفع حالة المجال بنفسه | QA record بأوامر ونتائج وأدلة وقرار `PASS_QA` أو `RETURN` |

### 3.1 قاعدة الاستقلال

- يجب أن يكون Reviewer غير مؤلف الوحدات التي يراجعها قدر الإمكان.
- يجب أن يكون QA مستقلًا عن مؤلف المخرج؛ إذا لم يتوفر ذلك يسجل
  `review_unavailable` وتبقى الحالة `hold` أو `blocked`.
- مراجعة Worker لملفه مفيدة كفحص ذاتي، لكنها لا تستبدل Reviewer أو QA.
- قد يقبل Commander تسليمًا محليًا، لكنه لا يحوله إلى `domain_done` من رسالة
  أو مراجعة ذاتية.

---

## 4. ملكية الملفات و`allowed_paths`

### 4.1 شكل الملكية

كل تكليف يذكر قائمتين منفصلتين:

- `allowed_read_paths`: مسارات نسبية إلى جذر
  `/sdcard/NEXUS_LLM_WIKI/` يستطيع الدور قراءتها.
- `allowed_write_paths`: ملفات أو مجلدات صريحة يملك الدور الكتابة داخلها.

القواعد التالية إلزامية:

1. لا يجوز استعمال `..` أو wildcard غامض أو مسار غير مذكور في التكليف.
2. يجب أن تكون مسارات الكتابة للعاملين غير متداخلة. امتلاك
   `collections/sales/` يمنع تكليف عامل آخر بأي مسار تحته في نفس الفترة.
3. لا يوجد «مجلد مشترك» للكتابة. حتى السجل المشترك أو ملف `latest.json` يحتاج
   مالكًا واحدًا؛ البديل هو ملف مستقل لكل `run_id` ثم دمج يملكه Commander.
4. التسليم لا يغير الملكية تلقائيًا. يلزم handoff مقبول، توقف الكاتب السابق،
   ومطابقة revision وtoken قبل أن يكتب المالك التالي.
5. لا تُستخدم ملفات مؤقتة خارج جذر الويكي كدليل تسليم. إن أذن التكليف بتخزين
   مؤقت، فيذكر المسار والغرض، ويُنسخ الدليل النهائي إلى مسار مملوك داخل الجذر
   قبل التسليم.
6. لا يعد وجود مسار في `allowed_read_paths` إذنًا بالكتابة، ولا يعد وجود ملف
   في `allowed_write_paths` إذنًا بتعديل مرجع خارجي أو حالة المجال.

### 4.2 ملكية افتراضية مقيدة

هذا الجدول توجيهي عند بناء التكليف؛ القائمة الفعلية في التكليف هي المرجع:

| نوع المسار | المالك الافتراضي | القيد |
|---|---|---|
| `raw/**` | لا أحد | قراءة فقط؛ أي تغير يسجل `raw_integrity_failure` |
| `config/processing_order.json` والقفل | Commander | كتابة حصرية وذرية مع CAS على revision المتوقع |
| `config/domain_catalog.json` | Commander/مالك الإعداد المخول | Worker وReviewer وQA قراءة فقط |
| `done/<domain>/<subdomain>/**` | Worker/مسؤول التوجيه المسمى | نسخة المصدر والـroute تخص دفعة واحدة ولا تُنشأ نسخة بديلة بلا قرار |
| `collections/<domain>/<batch_id>/**` | Worker المعين للدفعة | لا يكتب Worker آخر داخل الدفعة |
| `claims/<domain>/<batch_id>/**` | Worker المعين أو مؤلف Claims المسمى | Claims مرتبطة بمصدر وموضع؛ المراجعة في مسارها الخاص |
| `reviews/<domain>/<batch_id>/**` | Reviewer المعين | لا يكتب المؤلف قرار المراجع |
| `qa/<workflow_id>/**` | QA المعين | سجل مستقل لا يصحح المخرج بصمت |
| `checkpoints/<run_id>/**` | صاحب `run_id` | لا يحررها عامل آخر؛ handoff ينشئ سجلًا جديدًا أو يملك المالك الجديد ملفه |
| `reports/<workflow_id>/**` | الدور المذكور في التكليف | لا يستبدل سجل الحالة أو يعلن بوابة من تلقاء نفسه |

### 4.3 فحص الملكية قبل البداية

لا تبدأ الكتابة إذا تحقق أحد الآتي:

- مسار الكتابة غير موجود في التكليف أو يتداخل مع تكليف حي.
- لا يمكن تحديد صاحب الملف النهائي أو صاحب checkpoint.
- يوجد عامل حي يحمل token قديم أو لا يمكن إثبات توقفه.
- يطلب التكليف الكتابة في `raw/` أو في أحد الجذور المحظورة في `AGENTS.md`.
- التكليف يخلط snapshot أو domain أو revision في دفعة واحدة دون قرار صريح.

في هذه الحالات يسجل Commander أو العامل `ownership_missing` أو
`scope_missing`، وتكون النتيجة `blocked`، لا محاولة إصلاح صامتة.

---

## 5. عقد التكليف (Assignment Contract)

لا يكون التكليف شفهيًا فقط أو موزعًا بين رسائل. يجب أن يحوي على الأقل:

- `workflow_id` و`run_id` و`role`.
- `domain` و`subdomain` إن انطبق و`catalog_revision`.
- `snapshot_id` و`batch_id` و`source_ids`.
- حدود الوحدات أو المقاطع، بوحدات Unicode code point وبحدود نصف مفتوحة
  `[start,end)` عند استعمال segments.
- `expected_state_revision` و`fencing_token` الحاليان.
- `allowed_read_paths` و`allowed_write_paths` و`forbidden_write_paths`.
- المخرج المتوقع، معيار القبول، predecessor gates، وأوامر الفحص المتوقعة.
- مهلة التسليم، مالك التصعيد، وقرار ما يحدث عند التوقف.

إذا غاب أي عنصر حاكم، يسجل العامل `assignment_incomplete` ويعمل فقط في قراءة
تشخيصية مأذونة، أو يرد `RETURN`؛ لا يخترع قيمة أو مسارًا.

### 5.1 الهوية وعدم التكرار

لكل وحدة `unit_key` ثابت. مثال:

```text
<snapshot_id>/<domain>/<batch_id>/<source_id>/<unit_id>/<start>:<end>
```

لا تعتبر محاولتان مختلفتان وحدتين مختلفتين إذا كانتا تعالجان `unit_key` نفسه.
المحاولة الجديدة تستخدم `attempt_id` جديدًا وتربط نفسها بـ`retry_of` أو
`supersedes`، لكنها لا تنشئ Claim ثانية أو نسخة مصدر ثانية لمجرد إعادة التشغيل.

---

## 6. تقسيم الدفعات ومنع الكتابة المشتركة

### 6.1 قواعد التقسيم

1. تُقسّم الدفعات على مصدر أو وحدات مستقرة، لا على عدد أسطر عشوائي يتغير بين
   المحاولات.
2. لكل دفعة manifest يذكر `batch_id`، قائمة `source_ids`، ترتيبًا ثابتًا،
   الوحدات المتوقعة، والمسارات المملوكة.
3. لا تتداخل دفعتان في `unit_key`. إذا لزم تكرار قراءة سياق، يسجل كقراءة
   ثانوية ولا يكتب مخرجًا ثانيًا للوحدة نفسها.
4. لا تخلط مجالين أو snapshotين أو cutoffين أو revisionين في دفعة واحدة.
5. حجم الدفعة صغير بما يكفي لتثبيت checkpoint بعد كل مصدر أو segment؛ الدفعة
   الطويلة التي لا يمكن استرداد موضعها ليست دفعة قابلة للإدارة.
6. لا يبدأ Worker دفعة جديدة قبل أن يثبت Commander أن المجال والقفل والـsnapshot
   صالحون لها.

### 6.2 قاعدة الكاتب الواحد

- يملك Worker واحد الدفعة في لحظة واحدة.
- لا يكتب Reviewer في ملف Worker؛ يكتب سجل مراجعة منفصلًا.
- لا يكتب QA في مخرج Worker؛ يكتب سجل QA وfinding منفصلًا.
- لا يكتب Commander فوق مخرج Worker لتصحيح finding؛ يصدر قرارًا أو تكليف
  إصلاح جديدًا.
- لا يوجد merge ضمني بين عاملين داخل ملف واحد. كل merge عملية جديدة بمالك
  واضح ومدخلات ثابتة وفحص مستقل.
- إذا انتهت حصة عامل أو جلسته، لا تُسلم الملكية برسالة؛ تُثبت الحالة على القرص
  ثم يُغلق التكليف أو يُحوّل رسميًا.

### 6.3 ترتيب الوحدة القابل للإعادة

لكل دفعة ترتيب حتمي:

```text
source_id ↑ → unit_id ↑ → segment.start ↑ → segment.end ↑
```

ينفذ Worker من أول وحدة غير مثبتة بعد فحص checkpoint والمخرجات. لا يختار
«أقرب ملف» أو «آخر ملف ظهر» إذا كان ذلك يغير الترتيب أو يخفي فجوة.

---

## 7. دورة التشغيل والحالة

الدورة العامة المتوافقة مع النظام 20 هي:

```text
received
  → scoped
  → inputs_verified
  → plan_locked
  → in_progress
  → evidence_ready
  → review_pending
  → gates_pending
  → delivered

أي حالة → blocked | failed | paused | stale
blocked/paused → resumed فقط بعد إزالة السبب وتثبيت checkpoint
stale → impact_review → in_progress أو blocked
failed → recovery_classified → retry أو blocked
```

### 7.1 شروط الانتقالات

| الانتقال | الدليل الأدنى | ما لا يكفي |
|---|---|---|
| `received → scoped` | تكليف فيه هدف ومالك ومسارات | رسالة عامة أو اسم ملف فقط |
| `scoped → inputs_verified` | IDs وhashes وsnapshot وconfig المقروء | توقع أن المسار الحالي صحيح |
| `inputs_verified → plan_locked` | batch manifest وpredecessor gates وملكية غير متداخلة | بدء الكتابة ثم تحديد النطاق |
| `plan_locked → in_progress` | token وrevision صالحان وcheckpoint ابتدائي | انتهاء مرحلة التخطيط شفهيًا |
| `in_progress → evidence_ready` | كل وحدة لها مخرج ودليل وقياس أو سبب فجوة | exit code يساوي 0 فقط |
| `evidence_ready → review_pending` | تسليم قابل للقراءة ومسارات وبصمات | قول Worker إن العمل «جاهز» |
| `review_pending → gates_pending` | قرار Reviewer لكل وحدة أو finding واضح | مراجعة عينة بلا مقام |
| `gates_pending → delivered` | فحوص المهمة منفذة ونتائجها محفوظة | نجاح أداة بنيوية واحدة |
| `delivered → domain_done` | معاملة Commander، كل R/T/C/K/M/QA المطلوبة وdelta مقيمة | وجود تقرير أو عدد ملفات |

`delivered` تعني تسليمًا في نطاق التكليف، لا تعني تلقائيًا `source_done` أو
`domain_done` أو `canonical`.

---

## 8. Checkpoint: الحد الآمن للتوقف

### 8.1 متى يُنشأ

ينشئ Worker checkpoint ابتدائيًا قبل أول كتابة، ثم بعد كل مصدر أو segment أو
وحدة قابلة للاستئناف، وعند:

- انتهاء مهلة أو heartbeat.
- إيقاف المستخدم أو انتهاء الجلسة أو حصة الأداة.
- فشل gateway أو auth أو schema أو content.
- تسليم الملكية أو تبديل الدور.
- أي كتابة جزئية لا يمكن ضمان اكتمالها.

لا يسمى checkpoint «آمنًا» إلا بعد أن تكون الكتابة قد ثبتت على القرص، وأمكن
إعادة قراءة المخرج والتحقق من hash أو manifest المرتبط به. لا يُسجل
checkpoint قبل الكتابة ثم يُعامل كأنه يثبت الكتابة.

### 8.2 محتوى checkpoint

يجب أن يذكر checkpoint:

- هوية التشغيل والدور والمالك والوقت.
- `snapshot_id`, `batch_id`, `source_ids`, `state_revision`,
  `fencing_token`, و`catalog_revision`.
- hash المدخلات ونسخة الأداة أو parser عند الحاجة.
- `last_safe_boundary` و`completed_unit_keys`.
- الوحدة الحالية وحالتها: `not_started|in_progress|written|verified|returned`.
- مخرجات كل وحدة مثبتة: المسار، الحجم، hash، ومرجع الدليل.
- الوحدات المتبقية، والفجوات، والـdelta أو التغيرات المكتشفة.
- الأوامر المنفذة، وقتها، exit code، ونتيجة مختصرة قابلة للفحص.
- البوابات: ما اجتازته الدفعة محليًا وما لم يبدأ أو حُجب.
- `next_action` والمالك التالي وسبب التوقف إن وجد.
- `retry_of` أو `supersedes` عند وجود محاولة سابقة.

### 8.3 ترتيب التثبيت عند التوقف

يتبع Worker هذا الترتيب:

1. يوقف إنشاء مخرجات جديدة.
2. يفحص ما كتب حتى اللحظة ويحدد المكتمل والجزئي والمجهول.
3. يكتب checkpoint جديدًا في مساره المملوك، مع hash وexit codes.
4. يرسل تسليمًا يذكر مسار checkpoint، لا مجرد ملخص في الرسالة.
5. يطلب من Commander إغلاق التكليف أو قبول handoff.

إذا تعذر حفظ checkpoint، تكون الحالة `partial` أو `blocked` مع
`checkpoint_write_failure`؛ لا يعلن Worker نهاية آمنة.

---

## 9. Handoff: تسليم الملكية لا نقل الذاكرة

### 9.1 متى يلزم handoff

يلزم handoff صريح عند تغيير Worker أو Reviewer أو QA، أو عند انتقال الدفعة بين
جلسات، أو بعد توقف طويل، أو عند تغيير `fencing_token`، أو عند بقاء وحدات غير
مكتملة بعد timeout.

الرسالة وحدها ليست handoff. يجب أن يوجد سجل handoff على القرص يشير إلى آخر
checkpoint وملفات المخرج.

### 9.2 شروط قبول handoff

لا يقبل المالك الجديد handoff إلا بعد أن:

1. يثبت توقف المالك السابق أو انتهاء عمله وعدم وجود كتابة حية.
2. يقرأ آخر checkpoint ويسجل مسار القراءة في سجل التشغيل.
3. يطابق input hashes وsnapshot وdomain وbatch وcutoff.
4. يفحص أن revision المتوقع و`fencing_token` ما زالا صالحين؛ وإلا يلزم قرار
   Commander وزيادة token وفق القفل.
5. يفحص المخرجات على القرص ويصنف كل وحدة إلى `verified`, `partial`, `unknown`
   أو `not_started`.
6. يعلن `accepted` أو `blocked` مع السبب؛ لا يبدأ الكتابة أثناء بقاء القبول
   معلقًا.

### 9.3 ما ينتقل وما لا ينتقل

ينتقل: الهوية، الحدود، hashes، الوحدات المثبتة، المخرجات، الفجوات، الأوامر،
الفشل، والقرار التالي.  
لا ينتقل: افتراض غير مسجل، ذاكرة محادثة، وعد شفهي، أو «أظن أن هذه الملفات
مكتملة».

### 9.4 القفل والاسترداد

- لا يُفترض أن انتهاء lease يعني موت الكاتب السابق.
- استرداد القفل يحتاج دليل توقف المالك، مراجعة الملفات الجزئية، ثم زيادة
  `fencing_token` و`state_revision` بحسب معاملة Commander.
- التسليم بمفتاح قديم يُرفض حتى لو كانت محتوياته معقولة؛ يُحفظ للتشخيص ولا
  يُعتمد.
- لا يكتب المالك الجديد في مسار المالك السابق حتى يسجل Commander إغلاقًا أو
  handoff مقبولًا.

---

## 10. تصنيف الفشل والاسترداد

يجب أن يذكر كل فشل `failure_class` و`problem_id` و`observed_failure` و`impact`
و`root_cause` بدرجة ثقة و`test_that_would_catch_it` و`preventive_change` ومالكًا
وتاريخ إعادة الفحص. لا تستخدم `failed` العامة إذا أمكن تصنيف السبب.

### 10.1 Gateway/transport failure

هذا فشل في بوابة النقل أو الخدمة أو طبقة orchestration، وليس فشلًا في بوابة
الويكي R/T/C/K/M/QA.

**أمثلة الإشارة:** عدم وصول التكليف، انقطاع الاتصال، استجابة 502/503، queue
rejection، envelope غير صالح من gateway، أو توقف الخدمة قبل معرفة هل وصلت
الكتابة.

**الحالة الافتراضية:** `failed` أو `blocked` حسب ما إذا كانت إعادة المحاولة
ممكنة، مع `gateway_failure`.

**الاسترداد:**

1. لا تستنتج فشل المحتوى من فشل النقل.
2. أعد المحاولة بعد backoff محدود وبنفس `unit_key` وidempotency key؛ لا تنشئ
   وحدة جديدة بسبب رسالة gateway.
3. إذا كانت نتيجة الكتابة مجهولة، افحص checkpoint والملفات والhash قبل retry.
4. بعد عدد المحاولات المسموح به، أوقف الدفعة وسجل `external_dependency`.

**ممنوع:** تكرار التكليف بلا حد، أو إعلان PASS لأن gateway أعاد envelope
صحيحًا، أو الكتابة إلى مسار بديل غير مصرح به.

### 10.2 Auth/permission failure

**أمثلة الإشارة:** 401/403، انتهاء credential، مسار غير مسموح، role لا يملك
الملف، mismatch في `fencing_token`، أو محاولة Worker تعديل `config` أو `raw/`.

**الحالة الافتراضية:** `blocked` مع `auth_failure` أو
`ownership_missing`.

**الاسترداد:**

1. أوقف الكتابة فورًا واحفظ آخر checkpoint إن أمكن.
2. سجل المسار والعملية والهوية التشغيلية دون تسجيل سر أو token سري.
3. صحح التكليف أو الصلاحية عبر Commander؛ لا يتحايل العامل بتغيير المسار أو
   impersonation أو نسخ الملف إلى مكان آخر.
4. بعد تصحيح الصلاحية، أعد فحص الملكية والhash ثم استأنف من آخر حد آمن.

**ممنوع:** retry أعمى؛ فشل auth ليس timeout ولا دليلًا على أن المخرج ناقص.

### 10.3 Timeout/unknown completion failure

**أمثلة الإشارة:** انتهاء command timeout، غياب heartbeat، موت العملية، أو
انتهاء مهلة العميل دون معرفة هل اكتملت الكتابة.

**الحالة الافتراضية:** `partial` أو `blocked` مع `timeout_failure`؛ النتيجة
مجهولة إلى أن تتم المصالحة.

**الاسترداد:**

1. لا تعِد تشغيل الوحدة فورًا.
2. افحص آخر checkpoint، manifest، حجم الملف، hash، وملف الحالة إن كان مملوكًا.
3. صنف الوحدة `verified` فقط إذا تطابقت المخرجات والدليل والمدخلات؛ وإلا
   `partial` أو `unknown`.
4. أعد محاولة غير المثبت فقط بمحاولة جديدة مرتبطة بـ`retry_of` وبنفس
   `unit_key`، وبعد موافقة سياسة الاسترداد.
5. إذا تعذر الحسم، أعد `RETURN` إلى Commander بدل التخمين.

**ممنوع:** اعتبار exit code المفقود نجاحًا أو فشلًا محتوى، أو إنشاء Claim ثانية
قبل المصالحة.

### 10.4 Schema/contract failure

**أمثلة الإشارة:** حقل إلزامي مفقود، enum غير صالح، YAML/JSON غير قابل للقراءة،
مرجع لا يطابق schema، hash أو offset غير صحيح، أو سجل workflow لا يملك
`evidence_refs` المطلوبة.

**الحالة الافتراضية:** `failed` مع `schema_failure`؛ المخرج المتأثر لا يرقى إلى
`evidence_ready`.

**الاسترداد:**

1. اعزل السجل أو المخرج المتأثر واحتفظ به للتشخيص، دون حذف الدليل.
2. سجل validator والأمر والنسخة والـexit code وموقع الحقل الخاطئ.
3. أصلح المنتج في مسار مملوك أو أنشئ تكليف إصلاح منفصلًا؛ لا يصلح Reviewer أو
   QA المنتج بصمت.
4. أعد validator نفسه ثم فحوص التتبع والروابط قبل أي PASS.

**ممنوع:** إسقاط الحقل من التقرير، تحويل `null` إلى قيمة مخمّنة، أو اعتبار
وجود JSON شكليًا دليل schema صحيح.

### 10.5 Content/evidence failure

**أمثلة الإشارة:** مصدر أو segment غير مقروء بالكامل، locator لا يطابق الاقتباس،
Claim بلا مصدر، تعميم مثال، تعارض مخفي، تعريف بلا موضع، coverage gap، قراءة
قديمة بعد delta، أو مخرج لا يجيب معيار القبول الدلالي.

**الحالة الافتراضية:** `partial` أو `blocked`؛ وإذا كان المنتج غير صالح كليًا
فـ`failed` مع `content_failure` أو رمز أدق مثل `missing_evidence` أو
`coverage_gap` أو `stale_delta`.

**الاسترداد:**

1. أعد الوحدة إلى Worker أو Reviewer المسمى مع finding قابل للإعادة.
2. اذكر النص أو الموضع أو الوحدة التي فشلت، والنطاق المتأثر، وما لا يثبته
   الدليل.
3. لا تملأ الفراغ من معرفة عامة ولا تنقل Claim من مصدر آخر بلا ربط جديد.
4. إذا تغير المصدر أو snapshot، ابدأ impact review وسجل `stale` قبل الاستئناف.
5. لا يبدأ Master أو تنتقل بوابة لاحقة قبل تسوية predecessor المطلوبة.

**ممنوع:** استبدال نقص المحتوى بـ`PASS` بنيوي، أو حذف التعارض أو المصدر الذي
يكشف الفجوة.

### 10.6 فصل فشل النقل عن فشل البوابات

يجب تسجيل الحقلين منفصلين:

```yaml
failure_class: gateway_failure
wiki_gate_status:
  R: not_evaluated
  T: not_started
  C: not_started
```

فشل gateway لا يعني أن R أو T أو C فشلت، كما أن `gate_not_passed` ليس
`gateway_failure`. لا يجوز جمعهما في كلمة `error` تفقد سبب الاسترداد.

---

## 11. لا تعلن نجاحًا من رسالة Agent

### 11.1 طبقات الدليل

ترتب الأدلة من الأضعف إلى الأقوى:

1. رسالة أو ملخص Agent.
2. ادعاء أن العملية انتهت أو أن exit code كان 0 دون مخرج قابل للفحص.
3. وجود ملف أو عدد ملفات.
4. ملف بمسار ثابت وhash وحجم وmanifest مطابق.
5. أمر فحص منفذ فعليًا مع stdout وexit code ووقت ونسخة أداة.
6. مراجعة مستقلة تربط كل وحدة بالدليل والـschema والبوابة المطلوبة.
7. معاملة Commander تحدث الحالة بعد فحص QA، مع revision وtoken ومراجع القرار.

لا يلزم اجتماع الأدلة الأعلى لكل تسليم صغير، لكن يجب ألا يصف أي دور دليلًا
ضعيفًا بأنه دليل أقوى مما هو عليه.

### 11.2 معنى الرسائل

- `DONE` في رسالة Worker تعني فقط أن Worker يزعم نهاية محاولته؛ لا تعني قبولًا.
- `PASS_REVIEW` تعني نجاح مراجعة Reviewer ضمن النطاق المحدد، لا QA ولا إغلاقًا.
- `PASS_QA` تعني اجتياز فحوص QA المذكورة فقط؛ لا تغير `processing_order` وحدها.
- `PASS` النهائي لا يصدر إلا إذا حدد الدور نطاقه، ورفق الأدلة، وذكر الفجوات،
  وثبت predecessor gates، وكان القرار مخولًا.
- `RETURN` ليس فشلًا مبهمًا؛ يجب أن يذكر السبب القابل للإزالة والوحدة والمالك
  والخطوة التالية.

### 11.3 مؤشرات النجاح الكاذب

لا تعد أي من الآتي إثباتًا منفردًا:

- رد Agent غير فارغ أو JSON شكله صحيح.
- وصول process إلى EOF أو نهاية stream.
- exit code يساوي 0 من دون فحص المخرج.
- وجود ملف أو تقرير يقول «اكتمل».
- نجاح `wiki_quality.py` وحده.
- عدد Claims أو Concepts بلا مقام واضح وتغطية ومصير كل وحدة.
- `route_done` أو `source_done` لمصدر واحد كدليل `domain_done`.
- نجاح دفعة قديمة بعد تغير snapshot أو delta.

---

## 12. قواعد الاستئناف بلا تكرار

### 12.1 خوارزمية الاستئناف

عند تشغيل Worker جديد أو استعادة جلسة:

1. اقرأ التكليف الحالي وآخر checkpoint وقرار Commander؛ لا تعتمد رسالة قديمة.
2. تحقق من توقف الكاتب السابق ومن القفل و`fencing_token`.
3. طابق `snapshot_id`, `catalog_revision`, hashes، cutoff، و`state_revision`.
4. أعد حساب inventory من القرص للمسارات المملوكة؛ لا تعتمد عدادًا في الذاكرة.
5. لكل `unit_key`:
   - `verified`: تخطّها وسجل سبب التخطي ومرجع الدليل.
   - `written` بلا فحص نهائي: أعد فحصها قبل التخطي؛ إن فشلت فتصبح
     `partial`/`unknown`.
   - `in_progress` أو `partial`: لا تستأنف من منتصف ملف غير موثوق؛ أعد من
     آخر حد آمن أو أنشئ مخرج محاولة جديدًا مرتبطًا بالقديم.
   - `not_started`: نفذها بالترتيب الثابت.
   - `stale`: لا تعيدها على مدخل قديم؛ نفذ impact review أولًا.
6. أنشئ `attempt_id` جديدًا عند إعادة المحاولة، واربطه بـ`retry_of`، ولا تغير
   `unit_key`.
7. اكتب فقط داخل المسارات الجديدة أو المملوكة للمحاولة الحالية؛ لا تستبدل ملفًا
   سابقًا إلا إذا نص التكليف صراحةً على ذلك وكان المالك الحالي يملك الملف.
8. بعد كل وحدة، حدث checkpoint؛ عند النهاية، أرسل تسليمًا يفرق بين skipped
   المثبت وprocessed الجديد.

### 12.2 متى يُعاد العمل

يعاد العمل فقط إذا كان واحد من الآتي صحيحًا:

- لا يوجد مخرج مثبت للوحدة.
- hash المخرج لا يطابق manifest أو المدخل.
- schema أو الدليل أو المراجعة ناقصة.
- snapshot أو delta جعلت النتيجة `stale`.
- Reviewer أو QA أعاد الوحدة بسبب finding محدد.

وجود الملف الصحيح وحده لا يثبت قابلية التخطي؛ ووجود checkpoint قديم وحده لا
يثبت أن الملف نجا من الانقطاع.

### 12.3 المصالحة بعد timeout

إذا انقطع التنفيذ بعد أمر كتابة:

```text
لا retry مباشر
  → اقرأ checkpoint
  → افحص manifest والملف والhash
  → تحقق من الدليل والschema
  → verified: skip مع تسجيل السبب
  → غير ذلك: partial/unknown ثم retry_of جديد
```

لا يجوز إنشاء مخرجين نهائيين للوحدة نفسها ثم اختيار أحدهما بالحدس. إذا وجدت
محاولتان، يسجل Commander العلاقة بينهما وسبب اعتماد واحدة أو إبقائهما للتدقيق.

---

## 13. قوالب التشغيل

القوالب التالية أمثلة عملية. القيم بين `<...>` يجب استبدالها، ولا تُعامل
الأمثلة كسجلات حقيقية أو كإعلان تشغيل.

### 13.1 قالب التكليف

```yaml
kind: assignment
workflow_id: WF_<date>_<slug>
run_id: RUN_<date>_<role>_<id>
role: worker|reviewer|qa
owner: <stable-owner-id>
domain: <sales|outreach|pricing_offers|content_strategy|global_intake>
subdomain: <catalog-id-or-null>
catalog_revision: <revision>
snapshot_id: <SNAP_or_DOMAIN_SNAPSHOT>
batch_id: <BATCH_id>
source_ids: [<SRC_...>]
segments:
  - source_id: <SRC_...>
    unit_id: <UNIT_...>
    start: <unicode-codepoint-start>
    end: <unicode-codepoint-end>
    bounds: half_open
expected_state_revision: <integer>
fencing_token: <integer>
allowed_read_paths:
  - raw/new/<source-file>
  - sources/<source-record>
  - config/domain_catalog.json
allowed_write_paths:
  - collections/<domain>/<batch_id>/
  - checkpoints/<run_id>/
forbidden_write_paths:
  - raw/
  - config/processing_order.json
  - <other-live-run-paths>
predecessor_gates: [S0, R]
acceptance:
  required_outputs: [<output-ref>]
  required_evidence: [source_id, locator, content_hash]
  required_checks: [<command-or-verifier>]
  independent_review_required: true
timeout_policy:
  budget: <duration>
  on_timeout: checkpoint_reconcile_then_retry_or_return
handoff_owner: <commander-id>
status: planned
```

### 13.2 قالب checkpoint

```yaml
kind: checkpoint
checkpoint_id: CHK_<date>_<run_id>_<sequence>
workflow_id: WF_<...>
run_id: RUN_<...>
role: worker|reviewer|qa
owner: <stable-owner-id>
recorded_at: <ISO-8601>
status: in_progress|paused|partial|blocked|failed|validated
domain: <domain>
snapshot_id: <SNAP_...>
batch_id: <BATCH_...>
state_revision: <integer>
fencing_token: <integer>
input_hashes:
  <relative-path>: sha256:<64-hex>
last_safe_boundary:
  source_id: <SRC_...>
  unit_id: <UNIT_...>
  segment: {start: <n>, end: <n>, bounds: half_open}
completed_unit_keys:
  - <stable-unit-key>
unit_status:
  <stable-unit-key>:
    state: verified|written|partial|unknown|not_started|returned
    output_paths: [<relative-path>]
    output_hashes: [sha256:<64-hex>]
    evidence_refs: [<READ_...>, <CLM_...>]
in_progress_unit: <stable-unit-key-or-null>
commands:
  - command: <exact-command>
    started_at: <ISO-8601>
    finished_at: <ISO-8601>
    exit_code: <integer-or-null>
    result_ref: <relative-log-or-null>
findings:
  - problem_id: PRB_<...>
    failure_class: gateway_failure|auth_failure|timeout_failure|schema_failure|content_failure
    status: open|mitigated|verified|accepted_risk
next_action: <one-concrete-action>
next_owner: <owner-id>
retry_of: <run-or-attempt-id-or-null>
```

### 13.3 قالب handoff

```yaml
kind: handoff
handoff_id: HND_<date>_<id>
workflow_id: WF_<...>
from_run_id: RUN_<old>
from_owner: <old-owner>
to_run_id: RUN_<new>
to_owner: <new-owner>
from_role: worker|reviewer|qa
to_role: worker|reviewer|qa
domain: <domain>
snapshot_id: <SNAP_...>
batch_id: <BATCH_...>
source_ids: [<SRC_...>]
checkpoint_ref: checkpoints/<old-run>/CHK_<...>.yaml
input_hashes_verified: true|false
previous_writer_stopped: true|false
expected_state_revision: <integer>
fencing_token: <integer>
ownership_paths:
  read: [<relative-path>]
  write: [<relative-path>]
unit_summary:
  verified: [<unit-key>]
  partial: [<unit-key>]
  unknown: [<unit-key>]
  not_started: [<unit-key>]
unresolved_findings:
  - problem_id: PRB_<...>
    failure_class: <class>
    owner: <owner-id>
    next_action: <action>
acceptance_checks:
  - <command-and-result-ref>
status: offered|accepted|blocked|rejected
accepted_at: <ISO-8601-or-null>
```

### 13.4 قالب التسليم

```yaml
kind: delivery
delivery_id: DLV_<date>_<id>
workflow_id: WF_<...>
run_id: RUN_<...>
role: worker|reviewer|qa
scope:
  domain: <domain>
  snapshot_id: <SNAP_...>
  batch_id: <BATCH_...>
  source_ids: [<SRC_...>]
  unit_keys: [<stable-unit-key>]
read_refs: [<path-or-record-ref>]
output_refs:
  - path: <relative-path>
    sha256: sha256:<64-hex>
    units: [<unit-key>]
evidence_refs: [<READ_...>, <CLM_...>, <REVIEW_...>]
measurements:
  expected_units: <integer>
  verified_units: <integer>
  returned_units: <integer>
  unresolved_units: <integer>
checks:
  - command: <exact-command>
    exit_code: <integer>
    result_ref: <path-or-inline-ref>
gate_status:
  S0: pass|blocked|stale|not_started
  R: pass|blocked|stale|not_started
  T: pass|blocked|stale|not_started
  C: pass|blocked|stale|not_started
  K: pass|blocked|stale|not_started
  M: pass|blocked|stale|not_started
  QA: pass|blocked|stale|not_started
status: reported|partial|blocked|failed
not_proven: [<explicit-limit>]
next_action: <one-concrete-action>
```

### 13.5 قالب `PASS`

يستعمل الدور اسم PASS المقيد بنطاقه. لا يكتب `PASS` عامًا إذا كانت أي وحدة أو
بوابة خارج النطاق أو غير مقيمة.

```text
PASS_<REVIEW|QA|COMMANDER>

النطاق:
- workflow_id: <...>
- run_id / batch_id: <...>
- domain / snapshot_id: <...>
- الوحدات: <مقام واضح>

المثبت:
- المخرجات: <مسارات نسبية دقيقة>
- hashes/manifest: <مراجعها>
- evidence refs: <READ/CLM/REVIEW/GATE>
- raw_changed: 0 أو نتيجة الفحص الفعلية
- ownership check: <نتيجة>

الفحوص:
- الأمر: <exact command>
- الوقت/الإصدار: <...>
- exit code: <...>
- نتيجة QA المستقلة: <مرجع>

البوابات:
- <gate>: pass لأن <دليل محدد>
- غير المقيم: <قائمة صريحة>

الحدود:
- ما لم يثبت: <...>
- الفجوات/المخاطر: <...>

قرار الانتقال:
- اقتراح: <deliver أو hold أو next action>
- صاحب القرار: Commander؛ لا يغير هذا النص config تلقائيًا.
```

### 13.6 قالب `RETURN`

```text
RETURN

التكليف: <workflow_id / run_id / batch_id>
المرسل: <role / owner>
الحالة: blocked|partial|failed|stale
failure_class: gateway_failure|auth_failure|timeout_failure|schema_failure|content_failure
problem_id: PRB_<...>

ما حدث فعليًا:
- الوحدة/المسار: <...>
- الملاحظة القابلة للإعادة: <...>
- الأثر: <...>

ما فُحص:
- checkpoint: <path>
- المدخلات/hashes: <refs>
- الأوامر وexit codes: <refs>
- المخرج الجزئي: <path/hash أو none>

لماذا لا يجوز PASS:
- <gate أو معيار قبول غير محقق>

المطلوب من المالك التالي:
- الإجراء الواحد التالي: <...>
- المالك: <...>
- prerequisite أو صلاحية لازمة: <...>
- هل يلزم retry؟ <نعم/لا؛ retry_of إن وجد>

لا يوجد ادعاء بإكمال الوحدات غير المثبتة.
```

---

## 14. ما يثبت

يعد الدليل مناسبًا فقط بقدر ما يطابق النطاق والنسخة والمالك والبوابة المطلوبة.
الأدلة التالية تثبت ما هو مذكور بينها، لا أكثر:

1. **الملكية:** تكليف محفوظ بقوائم paths غير متداخلة، وrevision وtoken صالحان.
2. **سلامة المدخل:** path وsource ID وhash وsnapshot وcutoff مسجلة ومطابقة.
3. **سلامة الملف:** المخرج موجود على القرص داخل المسار المملوك، وحجمه وhashه
   يطابقان manifest أو سجل الوحدة.
4. **سلامة IO:** `bytes_read == bytes_expected` وEOF وhash القراءة؛ هذا يثبت
   IO فقط، لا الفهم الدلالي.
5. **التغطية:** اتحاد segments المتصلة يثبت نطاق القراءة المذكور، مع تسجيل
   `unread_ranges` إن وجدت.
6. **Claim:** source وlocator وevidence type وscope و`what_it_does_not_prove`
   وقرار المراجعة قابلة للحل والتحقق.
7. **المراجعة:** Reviewer مستقل سجل قرارًا لكل وحدة أو سجل finding صريحًا.
8. **QA:** أوامر QA نفذت فعلاً، ونتائجها وexit codes ووقت التنفيذ ونسخة الأداة
   محفوظة، وQA مستقل عن المؤلف.
9. **الاسترداد:** checkpoint يحدد آخر حد آمن، والوحدات المثبتة، والوحدات
   المجهولة، ومالك الخطوة التالية.
10. **الانتقال:** decision ledger يربط الحالة السابقة والجديدة والأدلة وسبب
    الانتقال، وCommander نفذ معاملة الحالة في revision صحيح.

---

## 15. ما لا يثبت

لا يثبت أي عنصر منفرد من الآتي نجاحًا أو اكتمالًا:

- رسالة Agent، أو كلمة `done`، أو `PASS` بلا مسارات وح hashes وأوامر.
- انتهاء العملية، أو EOF، أو exit code 0 بلا فحص للمخرجات والتغطية.
- وجود ملف، أو تقرير، أو مجلد غير فارغ.
- عدد الملفات أو Claims أو Concepts بلا مقام، snapshot، ومسار قياس من القرص.
- نجاح `tools/wiki_quality.py` أو أي فحص بنيوي مساعد وحده.
- `route_done`، أو `source_done` لمساهمة واحدة، أو checkpoint قديم.
- اجتياز بوابة R أو T وحدها لإثبات C/K/M/QA.
- مرور دفعة قديمة بعد تغير source hash أو delta أو catalog revision.
- مراجعة Worker لنفسه، أو اعتماد Commander بلا QA مستقل عندما تكون الاستقلالية
  مطلوبة.
- الاستنتاج من مثال أو رقم قصة إلى قاعدة عامة.
- retry ناجح بعد timeout إذا لم تتم مصالحة المخرج السابق.
- رد gateway الصحيح أو auth المصحح دون إعادة فحص ownership والمدخلات.
- وجود سجل `processed` دون إثبات كل الوحدات ومصائرها.

---

## 16. ما يجب تسجيله

يسجل صاحب التشغيل فور حدوثه، لا في نهاية الجلسة من الذاكرة:

### 16.1 الهوية والنطاق

- `workflow_id`, `run_id`, `role`, owner، وقت البدء والانتهاء.
- domain/subdomain، `snapshot_id`, `batch_id`, source IDs، cutoff،
  `catalog_revision`.
- `expected_state_revision` و`fencing_token` ومرجع القفل.
- `allowed_read_paths`, `allowed_write_paths`, forbidden paths، وتعارضات الملكية.

### 16.2 الأدلة والقياسات

- paths الدقيقة لكل مخرج، حجمها، hashها، وmanifest.
- المقام والبسط لكل عدد؛ مثل `verified_units / expected_units`.
- source/input hashes وread coverage وsegments وunread ranges.
- Claim/Concept/Master/Review/Gate refs والـlocators القابلة للحل.
- `raw_changed` ونتيجة فحص المسارات خارج النطاق.

### 16.3 الأوامر والفحوص

- الأمر كما نُفذ، working directory، نسخة الأداة أو parser.
- وقت البدء والانتهاء، exit code، stdout/stderr أو مرجع محفوظ لهما.
- العينة أو الشجرة أو manifest الذي فُحص، لا عبارة «تم التحقق» فقط.
- نتيجة كل بوابة: `not_started|in_progress|pass|blocked|stale` مع الدليل.

### 16.4 القرار والفشل

- `decision_id`, السؤال، القرار الموجز، authority ref، الحالة السابقة واللاحقة.
- `problem_id`, `failure_class`, observed failure، impact، root cause والثقة.
- الاختبار الذي كان سيكشف الفشل، preventive change، status، المالك، وموعد
  إعادة التقييم.
- `retry_of`, `supersedes`, `delta_id`، وسبب عدم التخطي عند الاستئناف.

### 16.5 الحدود والتسليم

- آخر checkpoint و`last_safe_boundary`.
- ما تم تخطيه لأنه `verified`، وما أعيد، وما بقي `unknown` أو `partial`.
- ما لم يثبت صراحةً، والمالك والخطوة التالية.
- هل التسليم `READY_FOR_REVIEW` أو `PASS_REVIEW` أو `PASS_QA` أو `RETURN`؛
  لا تستخدم كلمة عامة تخفي مستوى السلطة.

---

## 17. مصفوفة `PASS` و`RETURN` حسب الدور

| الدور | يستطيع إصدار | لا يستطيع إصدار | شرط أساسي |
|---|---|---|---|
| Worker | `READY_FOR_REVIEW` أو `RETURN` | `PASS_QA` و`domain_done` | مخرجاته وcheckpoint والفحوص المحلية |
| Reviewer | `PASS_REVIEW` أو `RETURN` | `PASS_QA` أو تغيير config | قرار لكل وحدة ودليل مستقل عن المؤلف |
| QA | `PASS_QA` أو `RETURN` أو `HOLD` | تغيير الحالة أو توسيع النطاق | فحوص مستقلة كاملة في نطاق التكليف |
| Commander | قرار انتقال أو `PASS` مخول في نطاقه | اختراع evidence أو تجاوز predecessor gate | كل الأدلة والـQA والمعاملة الصحيحة |

عند الشك يستعمل الدور `RETURN` أو `HOLD`، لا `PASS` احتياطيًا. إرجاع العمل
أكثر صدقًا وأقل كلفة من تثبيت نجاح غير قابل للاسترداد.

---

## 18. بروتوكول Commander عند التسليم

عند وصول تسليم أو رسالة Agent، ينفذ Commander الآتي بالترتيب:

1. يطابق `run_id` و`batch_id` وdomain وsnapshot مع التكليف الحالي.
2. يتحقق من أن paths المبلغ عنها ضمن `allowed_write_paths`، ولا يوجد overlap أو
   تعديل خارج النطاق.
3. يقرأ checkpoint والتسليم من القرص، لا من الرسالة وحدها.
4. يعيد قياس المخرج والـmanifest من القرص ويطابق hashes.
5. يفحص الأوامر وexit codes ويحدد ما إذا كان الفحص فعليًا أم ادعاءً.
6. يصنف أي فشل وفق gateway/auth/timeout/schema/content، ويمنع retry الأعمى.
7. يتحقق من predecessor gates والـdelta والاستقلالية.
8. يسجل decision ledger بالحالة السابقة والجديدة والسبب والأدلة.
9. يقرر `accept`, `return`, `hold`, `retry` أو `escalate` ضمن صلاحياته.
10. لا يغير `config/processing_order.json` إلا بمعاملة كتابة حصرية ذرية مع
    revision وtoken الصحيحين.

إذا تعذر تنفيذ خطوة، النتيجة `blocked` مع next action واضح؛ لا تُستبدل الخطوة
بتقدير من محتوى رسالة Agent.

---

## 19. بوابات الاسترداد السريعة

قبل إعادة تشغيل أي دفعة، يجب أن تكون الإجابات التالية مثبتة:

| السؤال | إن كانت الإجابة «لا» |
|---|---|
| هل توقف الكاتب السابق ويمكن إثبات ذلك؟ | `blocked: writer_alive_or_unknown` |
| هل snapshot وinput hashes لم تتغير؟ | `stale` ثم impact review |
| هل revision وtoken صالحان؟ | `auth_failure` أو `ownership_missing` |
| هل checkpoint قابل للقراءة ويحدد حدًا آمنًا؟ | `partial`؛ ابدأ reconciliation محدودًا |
| هل لكل وحدة حالة واضحة؟ | `coverage_gap` أو `unknown_unit_state` |
| هل المخرج المثبت يطابق schema والدليل؟ | `schema_failure` أو `content_failure` |
| هل retry مرتبط بـ`retry_of` ويحافظ على `unit_key`؟ | أوقف الاسترداد، فخطر التكرار قائم |
| هل توجد مراجعة/QA مستقلة عند الحاجة؟ | `review_unavailable` و`hold` |

لا يستمر الاسترداد ما لم تُحل الأسئلة التي تمنع سلامة التكرار أو الملكية.

---

## 20. معيار الإغلاق لهذه الوثيقة التشغيلية

عند تطبيق العقد على تشغيل فعلي، لا يوصف التشغيل بأنه مكتمل إلا إذا كان التسليم
قادرًا على عرض:

- التكليف وملكية الملفات.
- آخر checkpoint وhandoff إن وجد.
- قائمة الوحدات المثبتة وغير المثبتة دون تكرار.
- تصنيف كل failure قائم وإجراء الاسترداد.
- الأدلة والفحوص الفعلية وexit codes.
- قرار Reviewer وQA المستقلين في النطاق المطلوب.
- قرار Commander ومعاملة الحالة، إن كان الانتقال مطلوبًا.
- قائمة صريحة بما لم يثبت.

أما هذا الملف نفسه فهو **عقد مرجعي**؛ وجوده أو نجاح قراءته لا يثبت تشغيل
التكليف أو سلامة القفل أو اكتمال أي مجال أو اجتياز أي Gate.
