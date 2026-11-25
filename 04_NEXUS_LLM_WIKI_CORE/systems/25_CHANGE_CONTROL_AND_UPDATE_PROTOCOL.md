# 25 — بروتوكول ضبط التغيير والتحديث

**الإصدار:** `v1.1`  
**المراجعة:** 2026-10-18 — إضافة بوابة قرار سريعة للتمييز بين وصول المصدر وتحديث الدليل والتوثيق والمعرفة؛ لا يثبت العقد وحده تشغيل أي دفعة أو اكتمال أي مجال.  
**النوع:** مواصفة تغيير، توافق، مراجعة، وإبطال صلاحية.  
**المراجع:** [AGENTS](../AGENTS.md)، [SCHEMA](../SCHEMA.md)، [17 — عقد فهارس المجلدات والاسترجاع](17_FOLDER_INDEX_CONTRACT.md)، [19 — وصول مصدر جديد وإعادة المعالجة](19_NEW_SOURCE_REPROCESSING.md)، [20 — نظام تشغيل الويكي](20_WIKI_OPERATING_SYSTEM.md)، و[فهرس الأنظمة](INDEX.md).

> هذا البروتوكول يسجل القرار النهائي، والأثر القابل للفحص، وحدود الصلاحية. لا يطلب ولا يسجل chain-of-thought أو سلسلة الخواطر الداخلية. يكفي تسجيل السؤال التشغيلي، والقرار، ومراجع الدليل، والمخاطر، والخطوة التالية.

## 1. الغرض والنطاق

يمنع هذا النظام أن يتحول وصول مصدر جديد، أو تصحيح معلومة، أو تعديل وثيقة، إلى تغيير صامت يقطع التتبع أو يمدد صلاحية دليل قديم. ويحدد كيف:

1. يُستقبل مصدر أو معلومة جديدة دون المساس بالأصل.
2. يُنشأ `change manifest` يصف ما تغير وما لم يتغير.
3. تُحدَّث وثائق README وAGENTS وSCHEMA والفهارس عند الحاجة، كلٌّ في حد سلطته.
4. تُحفظ الإصدارات والتواريخ والروابط والمسارات ومراجع الأدلة.
5. تُنشأ `delta` ويُراجع أثرها، وتُوسم المخرجات المتأثرة `stale` بدل استعمالها بصمت.
6. يُفحص توافق schema قبل قبول السجلات الجديدة أو إعادة تفسير القديمة.
7. يُراجع التغيير مستقلًا، ثم يُسلَّم بحالة صادقة.

هذا النظام يضبط **التغيير** ولا يستبدل `config/processing_order.json` أو بوابات `R → T → C → K → M → QA`. ولا يملك صلاحية تغيير `raw/` أو فتح مجال معرفي pending أو إعلان `domain_done`. تحديث وثيقة تشغيلية، حتى لو كان صحيحًا وكاملًا في نطاقه، **لا يعني إكمال مجال معرفي**.

## 2. مبادئ غير قابلة للتفاوض

### 2.1 الأصل الخام immutable

- كل ملف داخل `raw/` ثابت: لا تعديل، ولا نقل، ولا إعادة تسمية، ولا استبدال، ولا حذف.
- التصحيح أو النسخة اللاحقة يسجل `source_id` جديدًا وبصمة جديدة، ويربط بالقديم عبر `supersedes` أو `revision_of` في metadata، دون محو الأصل.
- يُسجل `raw_changed: false` في manifest عند عدم التغيير، ويُعد تغير البصمة أو الحجم أو المسار داخل raw finding حرجًا (`raw_integrity_failure`).
- نسخة `done/` المستقلة ليست بديلًا عن raw، ونسخة المصدر ليست Claim أو Concept أو Master.

### 2.2 لا تحديث بلا هوية وحدود

كل تغيير له، قبل الكتابة:

- `change_id` ثابت.
- مالك وReviewer وصلاحية كتابة معلنة.
- نطاق ومسارات قراءة وكتابة محددة.
- `base_revision` أو `base_snapshot_id` يعرف الحالة التي بُني عليها التغيير.
- سبب تشغيلي ونوع تغيير.
- أثر متوقع على الأدلة والروابط والمستهلكين.

إذا غاب المالك أو تعارضت سلطة المستخدم وconfig ووثيقة حاكمة، تكون الحالة `blocked`، ولا يُستبدل النقص بتخمين.

### 2.3 التغيير append-only في التاريخ

لا يُمحى سجل تغيير أو قرار سابق لإخفاء خطأ. عند التصحيح يُضاف سجل جديد مع `supersedes` أو `retry_of` أو `corrects`، وتبقى النسخة السابقة قابلة للرجوع وموسومة بحالتها التاريخية أو `stale` عند فقد الصلاحية الحالية.

### 2.4 لا تمديد صامت للصلاحية

snapshot أو Gate قديمة لا تنطبق تلقائيًا على أحدث مخزون. أي وصول أو تصحيح أو تغير في catalog أو schema يمر عبر تقدير أثر؛ وما لم يُثبت عدم تأثره يبقى `stale` أو `blocked`.

## 3. ثلاث طبقات يجب عدم خلطها

| الطبقة | ما هي | ما تنتجه | ما لا يجوز استنتاجه منها |
|---|---|---|---|
| **Evidence — الدليل** | الأصل أو نسخة ثابتة منه، hash، quote، locator، READ، وسياق المصدر | قابلية الرجوع إلى ما قيل وأين قيل | لا يثبت وحده صحة عامة أو قبول Claim أو اكتمال مجال |
| **Documentation — التوثيق** | README وAGENTS وSCHEMA وINDEX وعقود الأنظمة وسجل التغيير | وصف القواعد، البنية، المسارات، المستهلكين، والإجراءات | لا يخلق دليلًا من عدم، ولا يثبت أن الدفعة شُغلت |
| **Knowledge update — تحديث المعرفة** | Terms وClaims وConcepts وMasters المشتقة من Evidence ومراجعة | معرفة قابلة للاسترجاع مع trace وscope وlimits | لا يصح بلا predecessor وGate مناسب، ولا يعني تلقائيًا `domain_done` |

### 3.1 أمثلة الفصل

- إضافة `README` تشرح مسارًا جديدًا = **تغيير توثيقي**؛ لا تثبت وجود المصدر أو سلامة النسخة.
- وجود quote صحيح في `raw` مع hash وlocator = **دليل**؛ لا يحول العبارة إلى Claim مقبول دون مراجعة.
- قبول Claim جديد وربطه بـConcept = **تحديث معرفة**؛ لا يثبت أن كل مصادر المجال قُرئت.
- نجاح فحص الروابط في INDEX = **فحص ملاحي**؛ لا يثبت القراءة الدلالية أو Gate T أو اكتمال المجال.
- تحديث AGENTS ليقول إن raw immutable = **تثبيت قاعدة**؛ لا يثبت أن raw لم يتغير إلا إذا قيس ذلك في سجل فحص.

## 4. تصنيف التغيير ومتى يبدأ البروتوكول

يجب فتح manifest لكل تغيير مؤثر، ولو كان الناتج ملفًا واحدًا فقط. يستخدم `change_type` في manifest، وتستخدم أحداث المصادر قيم `event_type` المعتمدة في النظام 19.

### 4.1 أنواع التغيير في manifest

| `change_type` | الوصف | المخرج الأول المطلوب |
|---|---|---|
| `new_source` | مصدر لم يكن في snapshot أو manifest السابقة | Source record، hash، manifest، delta |
| `source_revision` | نسخة معدلة أو تصحيح لاحق لمصدر موجود | Source جديد، `supersedes`، delta، impact review |
| `exact_duplicate` | مسار جديد بنفس المحتوى والبصمة | إثبات duplicate و`duplicate_of`؛ لا دليل مستقل جديد |
| `evidence_correction` | تصحيح quote أو locator أو تفسير لموضع الدليل | سجل تصحيح ومراجعة Claims المتأثرة |
| `knowledge_update` | إضافة أو تعديل Term/Claim/Concept/Master | predecessor، review، gate impact |
| `documentation_update` | تعديل README أو AGENTS أو عقد نظام | diff، owner، مراجعة المستهلكين والروابط |
| `schema_change` | تغيير بنية أو enum أو معنى حقل | schema version، migration/compatibility، fixtures |
| `index_update` | إضافة أو تعديل مدخل INDEX أو مسار استرجاع | snapshot، path/link check، retrieval impact |
| `catalog_change` | تغير نطاق domain/subdomain أو ترتيب catalog | delta، invalidation، snapshot جديدة |
| `link_repair` | إصلاح رابط أو anchor أو مسار رجوع | قائمة الروابط قبل/بعد وسبب الإصلاح |

### 4.2 أحداث المصدر المعتمدة

عند تسجيل delta لمصدر، لا تُخترع قيمة جديدة لـ`event_type`. القيم المعتمدة هي:

`new_source|exact_duplicate|source_revision|missed_candidate|catalog_change|evidence_correction`.

أما تغييرات الوثائق والفهارس وschema فتظهر في `change_type`، وتُذكر في `affected_refs` و`invalidated_refs` بحسب أثرها.

### 4.3 بوابة القرار السريعة لإضافة مصدر أو معلومة

استخدم التسلسل التالي قبل أي كتابة؛ فهو يحدد **ما الذي وصل** و**ما الذي يجوز تحديثه** دون خلط الطبقات:

1. **ثبّت الحدث والحدود:** أنشئ `change_id` و`workflow_id`، وسجل المالك، وReviewer، و`base_snapshot_id`، و`cutoff`، ومسارات القراءة والكتابة. إذا كان المالك أو المسار غير واضح فالحالة `blocked`.
2. **صنّف المدخل:**
   - ملف أو نسخة لم تكن في المخزون: `new_source` أو `source_revision`.
   - اقتباس أو موضع أو بصمة يحتاج تصحيحًا: `evidence_correction`.
   - قاعدة تشغيل أو وصف مسار أو فهرس: `documentation_update` أو `index_update`.
   - Term/Claim/Concept/Master جديد مشتق من دليل مراجع: `knowledge_update`.
   - أكثر من طبقة قد تتأثر: افتح manifest واحدًا يذكر الأنواع والاعتماديات، ولا تختصرها في وصف «تحديث عام».
3. **احسب الهوية قبل التفسير:** اقرأ البايتات كما هي، احسب SHA-256، وافحص duplicate/revision. لا تعدّل `raw/`؛ التصحيح مصدر جديد بهوية وبصمة جديدتين، والنسخة المطابقة لا تزيد عدد الأدلة المستقلة.
4. **أنشئ manifest وdelta عند اللزوم:** سجّل مصير كل مرشح، و`affected_refs` بعد المراجعة فقط، و`invalidated_refs` و`stale_refs` تحفظيًا قبل حسم الأثر. المرشح السابق لـ`cutoff` يسجل `missed_candidate` لا وصولًا جديدًا عاديًا.
5. **نفّذ أقل تحديث مسند:**
   - وصول المصدر: Source/hash/route/copy/READ، دون Claims قبل مرحلة الاستخراج.
   - تحديث الدليل: quote/hash/locator وتصحيح lineage، ثم راجع كل Claim/Concept/Master تابع.
   - تحديث التوثيق: حدّث README/AGENTS/SCHEMA/INDEX كلًّا في سلطته فقط، ولا تنسخ حالة config أو معرفة غير متتبعة.
   - تحديث المعرفة: أضف السجلات بمرجع Source/READ/locator وscope وlimits، ثم مرّر البوابات المتأثرة.
6. **افحص المستهلكين:** تحقق من schema والروابط والـanchors والمسار العكسي، ثم افحص downstream. لا تعيد `stale` إلى `pass` بتغيير label فقط؛ يلزم `no-impact` مراجَع أو إعادة معالجة.
7. **افصل التنفيذ عن القبول:** نفذ self-check، ثم Reviewer مستقل، ثم QA/مالك النظام عند الحاجة. سلّم الحالة الفعلية (`delivered` أو `partial` أو `blocked` أو `stale`) ولا تغيّر config أو تعلن `domain_done` من هذا البروتوكول.

| سؤال القرار | الحد الأدنى الذي يُسجل | النتيجة التي لا يجوز تجاوزها |
|---|---|---|
| هل وصل مصدر جديد؟ | Source ID، path، hash، cutoff، مصير المرشح، delta | لا يثبت قراءة المصدر أو اكتمال المجال |
| هل تغيّر الدليل؟ | lineage، quote/locator/hash القديم والجديد، affected refs | لا يحذف الرأي التاريخي ولا يقبل Claim تلقائيًا |
| هل تغيرت وثيقة؟ | diff، version/date، owner، المستهلكون، فحص الروابط | لا يثبت تشغيل corpus أو Gate أو `domain_done` |
| هل أضيفت معرفة؟ | Term/Claim/Concept/Master refs، review، gate impact، scope | لا تُعتمد بلا predecessor ودليل ومراجعة |

## 5. من وصول المصدر إلى التحديث الموثق

### 5.1 مرحلة الاستقبال والتثبيت

1. أنشئ `change_id` و`workflow_id` وسجل وقت الاكتشاف والمنفذ.
2. ثبت `cutoff` و`base_snapshot_id` ونسخة catalog وconfig التي قُرئت.
3. اجرد المسار المعلن قراءةً فقط، وسجل path النسبي والحجم ووقت الاكتشاف.
4. اقرأ البايتات كما هي، واحسب SHA-256 قبل أي parsing أو تطبيع.
5. إذا كان الأصل في `raw/`، تحقق من ثباته وسجل `raw_changed=0`؛ لا تكتب فيه.
6. أنشئ Source record بالقيم المتوافقة مع [SCHEMA](../SCHEMA.md)، ولا تستبدل `Source.status` بحالة workflow تفصيلية.
7. افحص البصمة مقابل المصادر السابقة: التطابق exact duplicate، والاختلاف مصدر أو revision جديد بحسب evidence.

### 5.2 manifest والمصائر

يجب أن يظهر كل مرشح في manifest بمصير واحد واضح، مثل:

`included_domain|referred_domain|duplicate|excluded_out_of_scope|quarantined|unresolved`.

لا يجوز تقليص المقام إلى العناصر التي يسهل استخراجها. المرشح الموجود قبل cutoff ثم اكتُشف لاحقًا يسجل `missed_candidate` وفشل تغطية snapshot السابقة، ولا يعاد وصفه بأنه وصول جديد عادي.

### 5.3 التوجيه والنسخة

- اختر `primary_route` واحدًا وفق catalog؛ secondary references تعود إلى المصدر نفسه ولا تضاعف الدليل.
- أنشئ نسخة مستقلة byte-exact تحت `done/<domain>/<subdomain>/` عند انطباق عقد التوجيه.
- سجل `copy_sha256` و`copy_independence` و`ROUTE_...` و`REF_...`، ثم أنشئ أو حدّث INDEX المحلي ضمن الصلاحية.
- لا تسجل Claim أو Concept في مرحلة route/copy؛ اتركها لخط المعرفة وبواباته.

### 5.4 القراءة والاستخراج والمراجعة

1. أنشئ `READ_*` يربط المصدر والsnapshot والبصمة وview وsegments.
2. افصل سلامة IO (`bytes_read`, EOF، hash) عن القراءة الدلالية؛ EOF لا يثبت الفهم.
3. اجمع Terms وcandidate Claims مع locator وscope و`content_unit_id`، وسجل `definition_gap` بدل التخمين.
4. راجع كل وحدة: Claim، Term، `non_knowledge`، `referred_domain`، duplicate، أو استبعاد مسبب.
5. لا تستخدم candidate Claim لبناء Concept أو Master قبل المراجعة المطلوبة.
6. إذا تأثر Concept أو Master، طبق Gate وretrieval QA في نطاق snapshot الجديدة؛ لا تكتفِ بتعديل الملخص.

### 5.5 الإغلاق المرحلي

إغلاق المصدر أو الوثيقة لا يساوي إغلاق المجال:

- `route_done`: التوجيه والنسخة وmetadata، دون استخراج معرفي.
- `source_domain_extraction_complete`: مساهمة مصدر في مجال/قسم محدد.
- `source_done`: كل وحدات المصدر ومصائرها ومراجعتها ضمن نطاقه.
- `delivered`: تسليم مخرج التغيير وفحوصه ضمن الصلاحية.
- `domain_done`: قرار مستقل يخص snapshot والمجال وكل بواباته؛ لا ينشأ من هذا الملف أو من تحديث README.

## 6. تحديث README وAGENTS وSCHEMA وINDEX

تُراجع هذه الملفات كمستهلكين مختلفين، ولا تُكرر فيها الحقيقة نفسها بصيغ متنافسة. إذا لم يتأثر ملف، يسجل manifest `not_applicable` مع السبب بدل تعديله شكليًا.

| الملف | سلطته | متى يُحدَّث | ما يجب أن يتضمنه التغيير | ما لا يملكه |
|---|---|---|---|---|
| `README.md` | مدخل بشري وشرح سريع | عند تغير طريقة البدء أو خريطة الاستخدام أو مخرج رئيسي | وصف موجز، المسارات الصحيحة، أمر التحقق، الإصدار/التاريخ، روابط العقود | لا يعرّف enum أو يرفع حالة workflow |
| `AGENTS.md` | قواعد التشغيل والصلاحية | عند تغير immutable، الملكية، المسارات المسموحة، أو ترتيب إلزامي | القاعدة المعيارية وحدودها ومرجع النظام التفصيلي | لا ينسخ حالة config أو يثبت تشغيلًا |
| `SCHEMA.md` | شكل السجلات والحقول والـenums | عند إضافة/تغيير حقل أو سجل أو علاقة | version، الحقول، enum، migration، التوافق، أمثلة تعليمية | لا يقرر ترتيب المجال أو يثبت صحة Claim |
| `systems/INDEX.md` | الملاحة ووظيفة الأنظمة | عند إضافة/إعادة تسمية/تغيير وظيفة نظام أو مسار | رابط قابل للحل، الوظيفة، متى يُقرأ، حدود التكامل | لا يعوض المحتوى أو سجل الحالة |

### 6.1 ترتيب آمن لتحديث الوثائق

عند الحاجة إلى تحديث أكثر من ملف:

1. افتح manifest وسجل baseline والمالكين.
2. حدّث SCHEMA أو عقد التشغيل أولًا إذا كان التغيير بنيويًا، أو سجل صراحة أن schema لم تتغير.
3. حدّث AGENTS لتشير إلى القاعدة الحاكمة دون نسخ تفاصيل متعارضة.
4. حدّث README ليعكس الاستخدام الفعلي لا النية المستقبلية.
5. حدّث INDEX بعد تثبيت الأسماء والمسارات والروابط النهائية.
6. افحص جميع المستهلكين والروابط والـanchors، ثم راجع التغيير مستقلًا.

هذا ترتيب توثيقي إرشادي لا يغير ترتيب البوابات المعرفية. لا يملك README أو INDEX صلاحية تجاوز `config/processing_order.json`.

### 6.2 تحديث الوثيقة دون اختراع معرفة

إذا استند تعديل README أو AGENTS إلى تجربة تشغيل، يسجل الأمر والنتيجة كـevidence تشغيلية. وإذا ذكر Claim معرفيًا، يجب أن يعود إلى Source/Claim/locator أو يوسم صراحةً كاقتراح أو فجوة. لا يملأ وصف INDEX فراغًا معرفيًا.

## 7. الإصدار والتاريخ ونسخة الدليل

### 7.1 هوية النسخة

كل وثيقة أو عقد مغير يحتفظ في رأسه، عند انطباقه، بـ:

```yaml
document_id: SYS_25_CHANGE_CONTROL_AND_UPDATE_PROTOCOL
version: v1.0
reviewed: 2026-10-18
status: active|draft|deprecated
change_id: CHG_20261018_example_001
```

القيم أعلاه نموذج؛ لا تُستعمل كدليل تشغيل حقيقي إلا إذا ربطها manifest وسجل مراجعة فعلي.

### 7.2 سياسة الزيادة

- `PATCH` مثل `v1.0.1`: تصحيح لغوي أو رابط أو مثال لا يغير القاعدة أو schema.
- `MINOR` مثل `v1.1`: إضافة قسم أو حقل اختياري متوافق لا يغير معنى الحقول القائمة.
- `MAJOR` مثل `v2.0`: تغيير معنى حقل، enum، مسار إلزامي، أو قاعدة تجعل المستهلك القديم يفسر السجل خطأ.

لا يكفي تغيير رقم الإصدار لإثبات صحة التغيير. يجب أن يذكر manifest `base_version` و`target_version` وسبب الزيادة، وأن يبين هل تغيرت schema أو الروابط أو البوابات.

### 7.3 التاريخ والـcutoff

يُفصل بين:

- `updated` أو `reviewed`: تاريخ تعديل/مراجعة الوثيقة.
- `discovered_at`: وقت اكتشاف المصدر أو الحدث.
- `cutoff`: حد snapshot التي تغطيها المعرفة.
- `effective_at`: وقت نفاذ قاعدة أو schema.

لا يوضع تاريخ مراجعة جديد على وثيقة لم تُراجع فعليًا، ولا يُستخدم تاريخ تحديث README كبديل عن cutoff أو evidence date للمصادر.

## 8. change manifest — العقد الإلزامي

الـmanifest هو فهرس تغيير قابل لإعادة الفحص، وليس ملخصًا إنشائيًا. يحتفظ بمقام الملفات/السجلات قبل وبعد، ويشير إلى الأدلة دون نسخها أو تعديل raw.

### 8.1 القالب

```yaml
manifest_id: CHG_20261018_example_001
change_type: new_source|source_revision|exact_duplicate|evidence_correction|knowledge_update|documentation_update|schema_change|index_update|catalog_change|link_repair
workflow_id: WF_20261018_example
requested_by: user|commander|system_owner
owner: worker-or-team
reviewer: reviewer-or-null
recorded_at: 2026-10-18T10:00:00Z
effective_at: null
reason: "سبب تشغيلي موجز قابل للفحص"
scope:
  kind: source|batch|subdomain|domain|system-docs|schema
  domains: [sales]
  subdomains: []
  allowed_read_paths: []
  allowed_write_paths: []
baseline:
  document_versions: {}
  catalog_revision: null
  schema_version: null
  snapshot_ids: []
  source_ids: []
  source_hashes: {}
  link_check_ref: null
change:
  added: []
  modified: []
  superseded: []
  deprecated: []
  moved: []
  source_event_type: null
  duplicate_of: null
raw_integrity:
  raw_changed: false
  raw_paths_checked: []
  raw_hash_check_ref: null
delta:
  delta_ids: []
  previous_snapshot_id: null
  next_snapshot_id: null
  affected_refs: []
  invalidated_refs: []
  stale_refs: []
  impact_status: pending_review|no_impact_reviewed|reprocess_required|blocked|resolved
compatibility:
  schema_changed: false
  compatibility_level: none|backward_compatible|migration_required|breaking
  migration_ref: null
  old_fixtures_checked: []
  new_fixtures_checked: []
links:
  links_added: []
  links_updated: []
  links_removed: []
  broken_links_before: null
  broken_links_after: null
  anchor_check_ref: null
review:
  self_check_ref: null
  independent_review_ref: null
  checks: []
  findings: []
verification:
  commands: []
  results: []
  measured: {}
  limitations: []
decision:
  state_before: received|scoped|inputs_verified|in_progress|stale|blocked
  state_after: delivered|partial|stale|blocked|failed
  decision_ref: DEC_20261018_example_001
  next_action: "الخطوة التالية والمالك"
  rollback_or_recovery: "إجراء الرجوع أو سبب عدم الحاجة"
```

### 8.2 قواعد manifest

- كل path في `allowed_write_paths` يجب أن يكون داخل النطاق المأذون، ولا يذكر `raw/` كمسار كتابة.
- `affected_refs` لا تُملأ بالتخمين؛ قبل المراجعة يمكن أن تبقى `[]` مع إبقاء invalidation تحفظيًا.
- `stale_refs` تذكر ما فقد صلاحية الاعتماد الحالي، لا ما حُذف.
- العدد في `measured` يذكر المقام والبسط وأداة القياس، أو يوسم `unknown/not_measured`.
- فشل التحقق لا يُخفى خلف `delivered`; الحالة الصحيحة `partial` أو `blocked` أو `failed`.
- لا تُعاد كتابة manifest قديمة بعد التسليم؛ يصدر تصحيح append-only مرتبط بها.

## 9. delta وinvalidation وstale

### 9.1 إنشاء delta

تنشأ delta عندما يحدث أحد الآتي:

1. مصدر جديد بعد cutoff.
2. مصدر كان موجودًا قبل cutoff لكنه غاب من manifest (`missed_candidate`).
3. نسخة مصدر تغيرت أو صُحح دليلها.
4. بصمة مطابقة وصلت من مسار جديد.
5. تغير catalog أو subdomain أو حدود snapshot.
6. تغير schema أو عقد وثيقة يؤثر في تفسير سجل أو مسار استرجاع.

يسجل الحدث `delta_id`، وقت الاكتشاف، candidate/source ID، المسار، hash، snapshot السابقة، affected domains، سبب الأثر، وحالة التقييم. لا تغير delta تاريخ snapshot القديمة ولا تجعل الوصول الجديد جزءًا من لقطة مغلقة بأثر رجعي.

### 9.2 جدول الأثر الأدنى

| الحدث | ما يُراجع | ما لا يتغير تلقائيًا |
|---|---|---|
| `exact_duplicate` | R والفهرس وعدّ المسارات وإثبات `duplicate_of` | عدد المصادر المستقلة، Claims، صلاحية المعرفة بعد إثبات عدم الأثر |
| `new_source` فريد | R وT وC، ثم K/M/QA المتأثرة | لا تبقى T أو Master صالحة لأحدث نطاق بلا مراجعة |
| `source_revision` | source lineage وREAD وClaims/Concepts/Masters التابعة | لا يُستبدل الأصل ولا يُحذف الرأي التاريخي |
| `evidence_correction` | quote/hash/locator، C ثم K/M/QA عند الأثر | لا يُحذف Claim مخالف مدعوم لمجرد أن تصحيحًا أحدث وصل |
| `missed_candidate` | اكتمال snapshot السابقة، R/T وتوابعها | لا يُعاد وصف نقص التغطية كإضافة عادية |
| `catalog_change` | R/T وحدود المجال، الفهارس، وكل Gate متأثر | لا تُعاد كتابة أدلة الإغلاق التاريخية |
| `schema_change` | parser/validators، السجلات المتأثرة، المخرجات والفهارس | لا تُفسر سجلات قديمة بمعنى جديد دون migration أو قرار توافق |
| `documentation_update` | الروابط، المراجع، المستهلكون، وعقود القراءة | لا يُستنتج منه تشغيل أو domain completion |

### 9.3 قواعد `stale`

- `stale` تعني أن الصلاحية الحالية معلقة بسبب تغير قابل للتتبع؛ لا تعني حذف النص التاريخي أو ثبوت خطئه.
- عند وجود delta غير مقيمة، تُوسم التغطية أو Gate المتأثرة `stale` حتى يثبت `no_impact_reviewed` أو تكتمل إعادة المعالجة.
- لا يعاد `stale → pass` بتعديل label فقط؛ يلزم `impact_review` أو snapshot جديدة وفحوصها.
- لا يوجد `reopen` صامت. قرار إعادة الفتح يسجل `from_state`, `target_domain`, السبب، snapshot الجديدة، المالك، القفل، والبوابات المتأثرة.
- المجال pending يمكن استقبال مصدره وتوجيهه، لكن لا يبدأ extraction معرفيًا قبل دوره.
- إذا كان مجال آخر نشطًا، تبقى delta في `queued` أو `blocked` حسب الأثر، ولا يُفتح extraction متوازٍ.
- التأجيل الموثق يحد صلاحية الإغلاق القديم؛ لا يجعل المخزون الجديد مكتملًا.

### 9.4 إغلاق delta

لا تصبح delta `resolved` إلا بأحد دليلين:

1. إعادة معالجة ناجحة: snapshot جديدة، READ/Claims/Reviews والبوابات المتأثرة، والفهارس وretrieval QA.
2. `no-impact` مراجَع: سبب محدد، مراجع الأدلة، فحص المستهلكين، وReviewer مستقل.

مجرد وضعها في queue أو تحديث README لا يحل delta.

## 10. الحفاظ على الروابط والمسارات

### 10.1 قواعد الهوية

- المسارات في metadata نسبية إلى جذر الويكي، وروابط Markdown نسبية إلى موضع الملف الذي يحتويها.
- `source_id`, `claim_id`, `concept_id`, `master_id`, `snapshot_id`, و`workflow_id` هويات مستقرة؛ تغيير path لا يخلق هوية بديلة.
- المسار العام إلى الدليل يكون: `INDEX → domain → subdomain → source/copy → Claim + locator → Concept → Master`، ويلزم المسار العكسي من Master إلى الدليل.
- secondary reference تشير إلى `source_id` نفسه ولا تضاعف عدد الأدلة المستقلة.
- الحقول التي لا مخرجات لها تبقى `[]`؛ لا تُنشأ روابط وهمية لإكمال جدول.

### 10.2 النقل وإعادة التسمية

قبل نقل أو إعادة تسمية ملف:

1. سجل old path وnew path والسبب في manifest.
2. احصر كل upstream/downstream references وMarkdown links وanchors.
3. حافظ على IDs والحقول والـhash؛ لا تعدل raw.
4. حدّث جميع المستهلكين في نطاق واحد أو أنشئ compatibility redirect/stub وفق convention المشروع قبل إزالة المسار القديم.
5. افحص أن الملف الهدف والanchor والمعرف يحلون، ثم سجل الصفر المتوقع للروابط المكسورة.

لا يكفي أن يكون الملف الهدف موجودًا؛ يجب أن يكون fragment/heading المقصود قابلًا للحل. ولا يُنقل `path` من JSON إلى Markdown كما هو دون حساب موقع الفهرس.

### 10.3 فحص الرابط

يسجل الفحص:

- عدد الروابط والمراجع قبل وبعد.
- broken paths وbroken anchors قبل وبعد.
- روابط الأدلة التي تعود إلى source/locator أو تصريح فجوة.
- الملفات غير المفهرسة والمدخلات الزائدة ضمن snapshot.
- أي رابط أزيل وسبب إزالته ومراجعه.

وجود رابط صالح لا يثبت قراءة المصدر أو صحة Claim؛ هو دليل ملاحي فقط.

## 11. توافق schema وتطورها

### 11.1 القاعدة

تظل الحقول والـenums الأصلية في [SCHEMA](../SCHEMA.md) حاكمة. لا تُضاف قيمة جديدة إلى `Source.status` أو `Claim.evidence_type` أو `Claim.confidence` أو `Claim.status` أو حالات Gate بصمت. امتدادات workflow لا تستبدل الحقول الأساسية.

### 11.2 مصفوفة التوافق

| التغيير | التوافق الافتراضي | المطلوب |
|---|---|---|
| حقل اختياري جديد | `backward_compatible` | توثيق field، default/nullable، اختبار parser قديم إن أمكن |
| حقل إلزامي جديد | `migration_required` | migration لجميع السجلات، version bump، fixtures قبل/بعد |
| إضافة enum لا يستخدمها parser القديم | مشروط | فحص المستهلكين؛ لا تعتمد التوافق بمجرد نجاح YAML/JSON |
| تغيير معنى enum أو حقل | `breaking` | إصدار major، migration صريحة، إعادة مراجعة المخرجات المتأثرة |
| إعادة تسمية حقل | `migration_required` | mapping old→new، فترة توافق أو تحويل موثق، لا فقدان قيمة |
| حذف حقل أو سجل | `breaking` | إثبات أن كل المستهلكين انتقلوا، archive/lineage، ومراجعة مستقلة |
| تغيير path فقط مع ثبات ID | مشروط | تحديث الروابط والفهارس وpath map وفحص anchors |
| تغيير parser أو offsets | `migration_required` | إعادة حساب view/quote hash والـlocators المتأثرة |

### 11.3 شروط قبول schema change

قبل قبول التغيير:

1. حدّد `schema_version_before` و`schema_version_after`.
2. اشرح لماذا لا يكفي الإصدار القديم.
3. اذكر السجلات والمستهلكين المتأثرين.
4. أنشئ migration أو compatibility layer إذا لزم، ولا تغيّر القديم في مكانه بلا trace.
5. اختبر fixtures قديمة وجديدة، والحقول null/empty، والقيم الحدية، والفشل المتوقع.
6. افحص أن `source_domain_extraction_complete` لا يحول مساهمة جزئية إلى `source_done`، وأن حالات Gate لا تُستبدل بـ`not_closed` أو `not_evaluated`.
7. راجع README/AGENTS/INDEX إذا تغيرت طريقة التشغيل أو الملاحة، ولا تكتب schema definitions فيها بديلًا عن SCHEMA.

## 12. مراجعة التغيير

### 12.1 فصل الأدوار

- المنفذ ينجز التغيير وself-check.
- Reviewer مستقل يفحص intent، scope، evidence، schema، الروابط، delta، وstale.
- QA أو مالك النظام يتحقق من الفحوص التي تتطلب استقلالًا أو قرار Gate.
- Commander يملك config والقفل وقرار الانتقال؛ لا يعتمد بلا أدلة.

إذا كان المراجع هو المؤلف نفسه ولا توجد صلاحية استثناء مسجلة، تبقى الحالة `review_pending` أو `blocked`.

### 12.2 أسئلة المراجعة

1. هل التغيير داخل المسارات المأذونة وبالمالك الصحيح؟
2. هل raw ثابت بالhash والمسارات، وهل سُجلت نتيجة الفحص؟
3. هل لكل مصدر أو سجل هوية وبصمة ونسخة وتاريخ مناسب؟
4. هل الفرق بين evidence وdocumentation وknowledge update واضح؟
5. هل كل Claim له source/locator/scope/type/limits ومراجعة عند اللزوم؟
6. هل الدليل المخالف محفوظ، وهل المثال منفصل عن القاعدة؟
7. هل أحدث delta وinvalidation وstale ظاهرة؟
8. هل schema متوافق أو توجد migration موثقة؟
9. هل الروابط والـanchors والمسار العكسي قابلة للحل؟
10. هل README وAGENTS وSCHEMA وINDEX محدثة فقط حيث يلزم، دون تكرار متعارض؟
11. هل كل عدد له مقام وبسط وأداة قياس؟
12. هل صياغة التسليم تتجنب `domain_done` و`source_done` غير المثبتين؟

### 12.3 سجل القرار

يرتبط كل قرار انتقال أو إبقاء stale بـ`decision_id` موجز:

```yaml
decision_id: DEC_20261018_example_001
manifest_id: CHG_20261018_example_001
recorded_at: 2026-10-18T12:00:00Z
actor: reviewer
question: "هل يحافظ التغيير على صلاحية المستهلكين؟"
decision: "نعم ضمن system-docs؛ لا يثبت domain completion"
evidence_refs: [CHG_20261018_example_001, LINKCHECK_EXAMPLE]
authority_ref: systems/25_CHANGE_CONTROL_AND_UPDATE_PROTOCOL.md
state_before: review_pending
state_after: delivered
findings: []
next_action: "تحديث INDEX بترخيص منفصل إن كان مطلوبًا"
status: recorded
```

هذا سجل قرار، لا مساحة لعرض بدائل داخلية أو chain-of-thought.

## 13. قالب سجل تغيير قابل للاستخدام

القالب التالي يختلف عن manifest: manifest يصف مجموعة التغيير، وسجل التغيير يشرح ما حدث وماذا أثبتت الفحوص للمراجعة البشرية.

```markdown
## CHG_YYYYMMDD_slug_001 — عنوان موجز

- **النوع:** new_source | source_revision | documentation_update | schema_change | knowledge_update | index_update
- **الحالة:** planned | in_progress | review_pending | delivered | partial | blocked | stale
- **المالك:** ...
- **Reviewer:** ...
- **المطلوب/السبب:** ...
- **النطاق:** source / batch / subdomain / domain / system-docs / schema
- **النسخة الأساسية:** document=`...`; schema=`...`; catalog=`...`; snapshot=`...`
- **النسخة الهدف:** document=`...`; schema=`...`; snapshot=`...`
- **التاريخ:** discovered=`...`; changed=`...`; reviewed=`...`; effective=`...`
- **المسارات المقروءة:** ...
- **المسارات المكتوبة:** ...
- **الأصل الخام:** `raw_changed=0`; فحص=`...`
- **المصادر/السجلات:** `[SRC_...]`, `[CLM_...]`, `[CPT_...]`, `[MSTR_...]`
- **التغييرات:** أُضيف ...؛ عُدّل ...؛ استُبدل ...؛ لم يتغير ...
- **delta/invalidation:** `DELTA_...`; المتأثر=`...`; stale=`...`; سبب=`...`
- **توافق schema:** none | backward_compatible | migration_required | breaking؛ المرجع=`...`
- **الروابط:** قبل=`...`; بعد=`...`; broken paths/anchors=`...`
- **الأدلة:** Source/hash/READ/locator/quote/review refs = ...
- **ما لا يثبته التغيير:** ...
- **الفحوص:**
  - الأمر: `...`
  - النتيجة: pass | fail | partial
  - المقام/البسط أو العينة: ...
- **قرار المراجعة:** قبول | رفض | قبول جزئي | إبقاء stale | blocked
- **الملاحظات والفجوات:** ...
- **الخطوة التالية والمالك:** ...
- **الرجوع/التعافي:** ...
```

## 14. قائمة الفحص قبل التغيير

- [ ] قُرئ التكليف وحددت الملفات المسموحة ومالكها.
- [ ] فُحصت AGENTS وSCHEMA والنظام الأقرب والـsnapshot/config ذات الصلة.
- [ ] أُنشئ `change_id` و`workflow_id` وmanifest قبل الكتابة.
- [ ] حُدد `change_type` وسبب التغيير وbase version/date/cutoff.
- [ ] حُددت `allowed_read_paths` و`allowed_write_paths`، ولا يوجد raw ضمن مسارات الكتابة.
- [ ] ثُبتت hashes والمسارات والروابط والإصدارات قبل التغيير.
- [ ] جرى التفريق بين evidence وdocumentation وknowledge update.
- [ ] حُددت الدلتا المحتملة ومرجع invalidation والمستهلكون downstream.
- [ ] عُرفت schema compatibility ومطلوب migration أو عدمه.
- [ ] حُددت خطة rollback أو recovery دون حذف أصل.
- [ ] إذا كان المصدر جديدًا: ثبت cutoff وmanifest ومصير duplicate/route المتوقع.
- [ ] إذا كان التغيير وثائقيًا: حُددت الملفات التي يلزم تحديثها والتي لا يلزمها.

## 15. قائمة الفحص بعد التغيير

- [ ] كل ملف تغير داخل `allowed_write_paths`؛ لا ملف آخر تغير.
- [ ] `raw_changed=0`، أو سُجل فشل سلامة واضح وتوقفت العملية.
- [ ] source/hash/copy/READ/Claim/Concept/Master refs قابلة للحل عند انطباقها.
- [ ] manifest مكتملة، والـchange log مرتبط بها، ولم يُعدّل سجل تاريخي بصمت.
- [ ] version/date/effective_at صحيحة ولا تخلط cutoff بتاريخ التوثيق.
- [ ] README يعكس الاستخدام الحالي دون ادعاء غير مدعوم.
- [ ] AGENTS يعكس القاعدة المعيارية دون نسخ حالة config.
- [ ] SCHEMA يصف أي حقل/enum/version/migration جديد، أو يثبت `schema_changed=false`.
- [ ] INDEX والـanchors والمسار العكسي والروابط الخارجية ضمن النطاق تعمل.
- [ ] كل delta لها `impact_status`، وكل المتأثرين موسومون stale أو أُثبت عدم تأثرهم.
- [ ] لم يُحوَّل `route_done` إلى `source_done`، ولا `source_done` إلى `domain_done`.
- [ ] تمت مراجعة schema القديمة والجديدة أو fixtures عند تغير schema.
- [ ] شُغلت فحوص الروابط، والـhash، وmanifest، وvalidator المناسب وسُجلت نتائجها.
- [ ] فُصل self-check عن المراجعة المستقلة؛ لا يُعلن QA ذاتيًا.
- [ ] سُجلت الفجوات والمقامات والقيود والقرار والخطوة التالية.

## 16. ما يثبت / ما لا يثبت / ما يجب تسجيله

### 16.1 ما يثبت

- hash ثابت ومطابق مع مسار قابل للحل يثبت هوية المحتوى في لحظة القياس.
- `raw_changed=0` مع فحص مسجل يثبت عدم رصد تعديل في raw ضمن النطاق المفحوص.
- manifest شاملة مع اتحاد مصائر يساوي المرشحين تثبت اكتمال **سجل المصائر**، لا اكتمال المعرفة.
- `READ_*` بsegments متصلة وview وhash يثبت تغطية القراءة المعلنة، لا فهمًا أو قبولًا تلقائيًا.
- Claim مع quote/hash/locator/scope/review يثبت قابلية تتبع ذلك Claim في نطاقه، لا قابلية التعميم.
- فحص الرابط الناجح يثبت الملاحة والرجوع إلى الوجهة، لا صحة النص أو البوابة المعرفية.
- migration واختبارات fixtures الناجحة تثبت توافق المسار الذي فُحص، لا توافق كل مستهلك لم يُفحص.
- `no-impact` المراجَع يثبت سبب إبقاء مخرج محدد صالحًا رغم delta، ضمن حدوده فقط.
- مراجعة مستقلة مع قرار ومراجع تثبت أن التغيير اجتاز review المحدد، لا `domain_done`.

### 16.2 ما لا يثبت

- وجود ملف أو تحديث README أو INDEX لا يثبت أن المصدر قُرئ أو أن المعرفة استخرجت.
- نجاح `tools/wiki_quality.py` أو أي فحص بنيوي لا يثبت القراءة الدلالية أو T/C/K/M/QA ما لم يذكر verifier ذلك صراحة.
- EOF أو مساواة bytes لا تثبت الفهم أو استخراج كل Terms/Claims.
- تطابق اسم ملف أو تشابه مصطلحين لا يثبت duplicate دلاليًا أو merge صحيحًا.
- مثال واحد أو رقم منقول لا يثبت قاعدة عامة أو benchmark أو سببية.
- `route_done` لا يثبت `source_done`، و`source_done` لا يثبت `domain_done`.
- تحديث وثائق التشغيل لا يثبت تشغيل corpus أو إغلاق delta أو اجتياز Gate.
- `version: v1.1` أو تاريخ حديث لا يثبت أن Reviewer فحص التغيير.
- وضع الحالة `resolved` دون impact evidence لا يثبت حل delta.
- وجود Master قديم لا يثبت أن أحدث snapshot أو المصدر الجديد مغطى.

### 16.3 ما يجب تسجيله

- الهوية: `change_id`, `manifest_id`, `workflow_id`, المالك، Reviewer، والنطاق.
- الزمن: `discovered_at`, `recorded_at`, `updated/reviewed`, `cutoff`, و`effective_at` عند انطباقها.
- الأساس والهدف: versions، schema/catalog revisions، snapshot IDs، وhashes.
- المسارات: ما قُرئ، ما كُتب، ما تحقّق، وما مُنع من الكتابة.
- المصدر: source ID، path، content hash، duplicate/revision lineage، copy hash، وroute.
- الأثر: delta IDs، affected/invalidated/stale refs، affected domains/subdomains، وimpact decision.
- التوافق: الحقول/الأحداث المتغيرة، enum، migration، fixtures، والمستهلكون.
- الروابط: before/after، broken paths/anchors، وpath map عند النقل.
- الدليل: READ، content units، quote/quote hash، locator، scope، `what_it_does_not_prove`، وreview refs.
- الفحوص: الأمر، الإصدار، النتيجة، الوقت، المقام والبسط أو العينة، والقيود.
- القرار: state قبل/بعد، سبب pass أو block أو stale، المرجع الحاكم، الخطوة التالية والمالك، وخطة الرجوع.

## 17. حالات تطبيقية مختصرة

### 17.1 مصدر فريد بعد snapshot

يُسجل source جديد وdelta، وتصبح T والتغطية ذات الصلة `stale`. يمكن تنفيذ intake وroute، لكن لا يبدأ Master ولا يُمدد إغلاق قديم حتى تُراجع المساهمة وتُعاد البوابات المتأثرة.

### 17.2 نسخة مطابقة من مسار جديد

يُثبت hash التطابق و`duplicate_of` ومسارات الوصول. لا يزيد مقام الأدلة المستقلة ولا يُعاد استخراج المصدر كمصدر مستقل. بعد مراجعة عدم الأثر يمكن استعادة صلاحية مخرج محدد، مع إبقاء حدث الوصول في التاريخ.

### 17.3 تصحيح quote أو locator

لا يُعدّل Claim المقبول بصمت. يُسجل `evidence_correction`، ويُعاد حساب quote hash والموضع، وتُراجع Claims/Concepts/Masters التي تعتمد عليه. إن فشل التحقق تبقى الحالة `stale` أو `blocked`.

### 17.4 تعديل README فقط

يُسجل كتغيير توثيقي، وتُفحص الروابط والنسخة والتاريخ. لا يُنشأ Source أو Claim، ولا يتغير Gate أو `domain_done`. إذا احتوى README على ادعاء معرفي، يحتاج ذلك الادعاء إلى trace مستقل أو وسم فجوة.

### 17.5 تغيير schema

يُحدد old/new schema version، ويُفحص كل parser/validator والمستهلكين، وتُجرى migration أو تُثبت backward compatibility. لا تُقبل سجلات جديدة بمعنى متغير بينما تبقى السجلات القديمة بلا migration أو status واضح.

## 18. معيار التسليم الصادق

يستخدم التسليم الصيغة التالية:

> **التغيير:** ...؛ **النطاق:** ...؛ **الأساس والهدف:** ...؛ **المخرجات:** ...؛ **raw:** ...؛ **delta/stale:** ...؛ **schema compatibility:** ...؛ **الروابط:** ...؛ **المراجعة:** ...؛ **المقاس:** .../...؛ **الحالة:** ...؛ **ما يثبت:** ...؛ **ما لم يثبت:** ...؛ **الفجوات:** ...؛ **الخطوة التالية والمالك:** ... .

لا تستخدم «اكتمل التحديث» إذا كان المقصود مجرد كتابة ملف. استخدم «تغيرت الوثيقة» أو «سُلّم المخرج ضمن نطاقه» مع ذكر ما لم يُراجع. ولا تستخدم «اكتمل المجال» إلا بقرار المجال وبواباته وsnapshot الشاملة، خارج صلاحية هذا البروتوكول وحده.
