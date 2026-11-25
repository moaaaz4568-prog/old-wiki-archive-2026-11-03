---
name: folder-index-and-handoff
description: "تُستخدم لفهرسة root وdomain وsubdomain وlayer وتسليم handoff يفصل تصنيف المصدر ونسخته عن اكتمال استخراج المعرفة أو المجال. تتتبع route_done وqueue وتغطية المرشحين وdelta؛ لا تجعل source_refs بديلًا لملف المصدر، ولا تمنح اكتمال فرع تصريحًا لبدء Master."
---

# فهارس المجلدات وحزمة التسليم

## عقد 2026-10-10

اقرأ [R/T/C/K/M/QA](../INDEX.md) و`<alignment_path>` والملحق في
`<user_messages_path>`؛ الفهرس يصف حالة مثبتة ولا يصنع الدليل.

- `route_done` جائز قبل extraction بعد full semantic read وتصنيف ونسخة
  مستقلة byte-exact متحققة في `done/<domain>/<subdomain>/` افتراضيًا. الملف
  المادي مطلوب؛ `source_refs` فهارس ثانوية فقط وdone لا تعني domain_done.
- الفرز وفهرسة النسخ لأي domain جائزان؛ معرفة `current_domain` فقط تنفذ،
  والباقي `queued` لا quarantined. quarantine لفساد/تعذر قراءة/هوية؛ الغموض uncertain.
- تُفهرس terms وcandidate Claims أثناء القراءة فور تسجيلها دون انتظار المجال
  كله، مع مواضعها وحالتها. Concepts من أدلة مراجعة ولا اختراع تعريفات.
- `source_done` استخراج كامل terms/Claims مع QA، لا يحتاج Concepts أو Master.
  `subdomain_extraction_done` لا يسمح بـMaster صغير: يلزم `domain_terms_complete`
  لكل المجال وكل فروعه قبل أي Master، بلا sample أو snapshot تخفي مرشحًا بلا قرار.
- الخلافات تحفظ مع scope، لا استبعاد لمجرد الرأي. `delta` تجعل التغطية `stale`
  وتحتاج queue معلنة؛ فقط `domain_done` يجيز المعرفة في التالي، بلا مجالين.

## الغرض

صف في INDEX وظيفة الملف وحالته ومراجعه واعتمادياته، وفي handoff ما تم وما لم
يتم وما ينبغي استئنافه. لا تحوّل الملاحة إلى Claim أو Concept أو Master.

لا تكتب في `raw/` بهذه المهارة. حدّث الفهارس والمراجع المشتقة فقط، وبصلاحية
المسار المهيأ.

## عقد التشغيل القابل للتهيئة

عرّف المسارات والقواعد قبل التعديل:

```text
WIKI_ROOT                  = <wiki_root>
ROOT_INDEX_PATH            = مسار INDEX.md الجذري المهيأ
DOMAIN_ROOT                = مسار مجلدات domains المهيأ
SUBDOMAIN_ROOT             = مسار مجلدات subdomains المهيأ
LAYER_NAMES                = أسماء الطبقات المعتمدة في هذا المشروع
HANDOFF_ROOT               = مسار حزم التسليم المهيأ
STATE_STORE_PATH           = مصدر حالات التشغيل المهيأ
DEPENDENCY_CONFIG_PATH     = عقد الاعتماد والبوابات
RUN_ID                     = معرف تشغيل ثابت
```

استخدم `INDEX.md` اسمًا للفهرس المحلي في root وكل domain وsubdomain وlayer؛
config يحدد مواضع هذه المجلدات والطبقات الفعلية لا مسارات تثبيت مفروضة. إذا
كان للمشروع فهرس قديم باسم آخر فاحتفظ به واربطه، ولا تُنشئ فهرسين متعارضين
كمصدر حالة. لا تعِد تنظيم ملفات المعرفة أو نقلها لإنشاء شجرة شكلية جديدة.

القيم هنا placeholders تُستبدل قبل نشر سجل، والبدائل المفصولة بـ`|` ليست قيمة
فعلية. افحص أن paths المخزنة نسبية داخل `WIKI_ROOT` بلا traversal، وأن المسار
الفعلي بعد حل symlinks داخل الجذر. روابط Markdown تُحسب من موقع INDEX الذي
يحتويها وفق resolver المشروع، لا بخلطها مع `source_path` النسبي إلى الجذر.

## مستويات الفهرس الأربعة

أنشئ فهرسًا محليًا في كل مستوى مطلوب، ولا تعتمد على فهرس الأب بدل فهرس المجلد:

يشمل ذلك new وdone وstaging المصرح بها. نسخة المصدر نفسها موجودة داخل subdomain
المصنف، لا مجرد REF أو فهرس في source_refs. **استثناء immutable:** لا تكتب
`INDEX.md` جديدًا في raw ولا تعدّل فهرسًا داخله؛ افهرس الخام من سجل مشتق خارجه
مع مساره وبصمته. إن كان تعديل فهرس مطلوب خارج ملكية الدور فسجّل dependency
وسلّمها إلى المالك بدل تجاوزه.

| المستوى | ما يجب أن يوضحه INDEX المحلي |
|---|---|
| root | غرض الويكي وحدودها، المجالات وترتيبها والقفل المعرفي، فهارسها وحالاتها، السياسات وcatalog وstate، dependencies وhandoff والاستئناف |
| domain | نطاق المجال، subdomains وفهارسها، snapshot كل المرشحين وقراراتهم، المصادر والمخرجات، أدلة R/T/C/K/M/QA وblockers وdomain_done إن ثبت |
| subdomain | Source IDs ومسارات الأصل والنسخة وبصماتها، route_done والاستخراج منفصلان، subdomain_extraction_done لا يجيز Master، فهارس الطبقات وowner والبوابة التالية والفجوات |
| layer | كل ملف أو سجل ووظيفته وحالته ومصادره واعتمادياته وآخر تحقق؛ يشمل Terms وClaims وConcepts وMasters دون نسخ معرفتها |

لكل حالة mapping إلى سجلها، لا إلى Source.status كيفما اتفق. يذكر كل مستوى
checkpoint وhandoff الخاصين به، لا يعتمد على فهرس الأب بدل فهرسه المحلي.

## قالب مدخل الملف

استخدم جدولًا أو YAML حسب convention المشروع، بشرط عدم إسقاط الحقول التالية:

```yaml
path: relative/path/from/wiki-root
artifact_id: configured-artifact-id
kind: source|route|term|claim|concept|master|index|checkpoint|handoff
function: وظيفة تشغيلية محددة
scope: root|domain|subdomain|layer
status_scope: routing|extraction|domain_terms|domain_closure
status: "<measured-status>"
copy_path: "done/<domain>/<subdomain>/<source_id>.<ext>"
content_hash: "sha256:<measured-64-hex>"
knowledge_state: queued|active|reviewed
source_refs: []
evidence_refs: []
dependencies:
  - relative/path/or-artifact-id
owner_role: configured-agent-role
previous_gate: gate-id-or-null
next_gate: gate-id-or-null
last_verified: configured-timestamp
verification_ref: checkpoint-or-report-id
notes: حدود أو فجوات ظاهرة
```

هذه حقول فهرس تشغيلي، لا امتداد مفترض لـSource/Claim/Concept/Master schema.
استخدم مفردات الحالة الفعلية في `STATE_STORE_PATH` مع `status_scope` الذي يوضح
هل المقصود routing أم content أم source/subdomain/domain closure. حالة التوجيه
`done` لا تعني `source_done`؛ لا تحول `draft` إلى `done` أو `accepted` بلا gate.
وسوم نطاق Skill ليست اعتمادًا معرفيًا. تُوسم المهارة العامة التي تتضمن أمثلة
مبيعات `reusable with sales examples`، لا sales-specific لمجرد المثال.

## إجراء إنشاء أو تحديث INDEX

1. اقرأ تعليمات الويكي وschema والـcharter وstate store وعقد handoff. حدد
   المستوى الذي يملكه الدور قبل لمس أي ملف.
2. اجرد الملفات الفعلية في نطاق المجلد، وقارنها بالـINDEX السابق وبالـmanifests.
   أضف العناصر المفقودة كحالة غير مفحوصة، ولا تحذف مدخلًا تاريخيًا لإخفاء فرق.
   لا تعرض ملفًا متوقعًا كأنه موجود؛ افصل expected/missing عن الملفات الموجودة،
   وسجّل المصدر المفقود مع السبب دون إنشاء محتواه بالتخمين.
3. حلّ كل path من الجذر المهيأ، وتحقق من عدم وجود traversal أو symlink غير
   مصرح. علّم الرابط المكسور بوضوح مع الإجراء التالي.
4. لكل مدخل، اكتب الوظيفة التي يثبتها عقد الملف، والحالة من state store، ومراجع
   source/evidence/checkpoint، والاعتماديات وبوابة الانتقال.
5. اربط فهرس المستوى الأب بفهرس الأبناء، واربط layer index بملفاتها، دون تكرار
   النص الكامل أو تحويل الفهرس إلى ملخص معرفة.
6. سجّل `RUN_ID` ووقت التحقق وإصدار القواعد. اجعل إعادة التشغيل تعيد نفس النتيجة
   إذا لم تتغير مجموعة الملفات أو الحالات.
7. افحص الفهرس بعد الكتابة، ثم أنشئ checkpoint يبين العدد المتوقع والمدرج وغير
   المفهرس والمكسور.

لا تنشئ INDEX داخل raw. يجوز فهرس routing ونسخ done لمجال pending وإظهارها
route_done مع knowledge_state queued؛ هذا لا يصرح باستخراج معرفته. لا تُنسب
حالة الملف المصنف إلى حالة المجال المعرفية.

## حزمة handoff

أنشئ حزمة تسليم مشتقة في `HANDOFF_ROOT` عند نهاية مرحلة أو subdomain أو domain:

تحتوي الحزمة: handoff_id وrun_id، domain/subdomain/layer والمرحلة والحالة،
completed/pending، blockers بأسبابها ومالكيها، inputs/outputs بمعرفاتها
ومساراتها وبصماتها، dependencies، gates مع evidence_ref لكل نتيجة، الأوامر
والفحوص المنفذة والنتائج وما لم يُختبر، next_agent_role وnext_action والتوقيت.

اجعل handoff يذكر ما لم يُنجز وما لم يُقَس، لا يكتفي بقائمة نجاحات. لا يعلن
`domain_done` من handoff وحده؛ يجب أن يشير إلى سجل الإغلاق وQA الذي أثبته.
احفظ نسخ catalog/gates وhash المدخلات والمخرجات المهمة، ومالك القفل الحالي،
ومسارات الكتابة المسموحة، والعمل الجاري، وكيفية الاستئناف من أول gate غير
مكتملة. استلام Agent التالي للحزمة لا يساوي قبولها؛ يعيد حل الأدلة ويقر الاستلام
أو يردها بسبب صريح.

## الاعتماديات والبوابات

لكل ملف أو مجلد، أظهر اعتمادًا ذا نطاق لا سهمًا يوهم بمنع المرشحين:

```text
R: copy verified -> route_done (أي domain)
النشط: reading -> terms + candidate Claims -> review/QA -> source_done
C المراجعة -> K؛ all-domain T + C/K ذات الصلة -> M
المخرجات المطلوبة + QA/استرجاع/فهارس -> domain_done -> معرفة المجال التالي
```

إذا كان عنصر يعتمد على قرار domain سابق، اربطه بـdomain وcheckpoint لا بعبارة
عامة. إذا كانت dependency مفقودة أو حالتها أقدم من المدخل، استخدم `blocked` أو
`review` بدل الادعاء أن المخرج نهائي. فرّق بين dependency تشغيلية ومرجع دليل
حتى لا يبدو index كأنه يثبت صحة المحتوى.

## فحوص الفهرس والتسليم

نفّذ verifier مستقلًا، وسجّل النتيجة:

1. كل مدخل يدّعي وجود ملف يحل إليه؛ كل ملف في النطاق مفهرس أو موسوم `unindexed`.
   وجود `unindexed` أو missing/blocker يمنع اجتياز بوابة الفهرسة النهائية؛ إظهاره
   يحفظ الحالة ولا يحوّل FAIL إلى PASS.
2. كل path نسبي وآمن، ولا توجد مسارات مكررة لمعرف واحد بلا تفسير.
3. كل حالة في الفهرس تطابق state store والـcheckpoint الأخير.
4. كل source/evidence/checkpoint/handoff reference قابل للحل.
5. كل dependency وبوابة تملك حالة ومالكًا وإجراءً تالياً عند الفشل.
6. route_done وsource_done وsubdomain_extraction_done وdomain_terms_complete
   وdomain_done لا تندمج في خانة done مبهمة؛ لكل منها سجلها ولقطتها ودليلها.
7. root index يطابق domain indexes، وكل domain index يطابق subdomain indexes.
8. لا توجد روابط إلى `raw/` تتطلب تعديلًا أو نقلًا، ولا تغير جرد `raw` نتيجة
   تحديث الفهارس.

## إعادة التشغيل والتاريخ

- استخدم مفتاحًا حتميًا للمدخل `(path, artifact_id, state_version)`، وحدّث
  المدخل بدل تكراره عندما تكون الهوية والحالة نفسهما.
- احتفظ بسجل تغييرات الفهرس أو diff/checkpoint حسب سياسة المشروع؛ لا تمسح سبب
  انتقال الحالة.
- ثبّت وقت التحقق من دليل التشغيل بدل تغييره بلا فحص في كل إعادة. تحقق من
  نسخة INDEX قبل الكتابة؛ عند تعديل متزامن أعد القراءة وادمج المدخلات المملوكة
  فقط، ولا تمسح عمل Agent آخر. تحديث الأب لا يُسند إلى أكثر من مالك في الوقت نفسه.
- عند تغير ملف أو dependency، حدّث المستوى الأدنى المتأثر ثم الأبناء والأب،
  وأعد فحص handoff الذي يعتمد عليه.
- أظهر كل وصول جديد في delta، وسم تغطية snapshot التابعة stale للمخزون الأحدث.
  اذكر المرشحين غير المحسومين والقرارات وجدولة queue ومالكها. النشط يعالج delta
  الخاصة به؛ غير النشط ينتظر دون فتحه بالتوازي أو تقديم المؤجل كمكتمل.
- قبل انتقال معرفي جديد تحقق من مراجعة أثر delta على الإغلاق؛ لا يعمم snapshot
  قديم أو يُحذف مرشح من الفهرس لتقليل مقام التغطية.
- عند استئناف Agent جديد، ابدأ بقراءة root index ثم domain ثم subdomain ثم layer
  وhandoff الأخير، ولا تعتمد على رسالة جلسة سابقة غير محفوظة.

## حالات تحقق handoff — متوقعة وليست نتائج منفذة

- ملف موجود بلا صف: سجّله غير مفحوص، وبوابة الفهرسة تبقى مفتوحة حتى يراجع.
- صف done مع source/hash مفقود: FAIL لا تصحيح الدليل لإرضاء الفهرس.
- اعتماد غير مقبول أو تغير hash بعد QA: blocked/review وإعادة فحص المتأثر.
- إعادة نفس inputs/state version: لا صفوف مكررة ولا تغيير حالة تلقائي.
- فهرس root وحده بلا فهارس فرعية: تسليم ناقص، وليس تغطية للشجرة.
- مصدر في source_refs بلا نسخة مباشرة في done/subdomain: R ناقصة.
- مجال queued ونسخته متحققة: route_done صحيح ولا معرفة نشطة له.
- source_done بلا Master مع استخراج ومراجعة كاملة: صحيح؛ Master بعد فرع فقط: ممنوع.
- مرشح غير محسوم غير مدرج في snapshot: يمنع T، لا يخفيه نجاح اختبار روابط.

## ممنوعات

- لا تجعل `INDEX.md` بديلًا عن Source أو Claim أو Concept أو Master.
- لا تدرج وظيفة لم يثبتها عقد الملف، ولا تملأ الحالة من وجود الملف فقط.
- لا تحذف فجوة أو رابطًا مكسورًا أو dependency متعارضة من أجل مظهر نظيف.
- لا تعدل `raw/` أو النصوص المعرفية من دور الفهرسة.
- لا تعتبر handoff أو index دليلًا مستقلًا على صحة الادعاء.
- لا تستخدم مسارات مطلقة أو symlink غير مصرح أو placeholders غير محلولة في
  index منشور.
- لا تستخدم Codex في الفهرسة أو التحقق.
