---
name: sequential-domain-orchestration
description: "تُستخدم لتنسيق فرز عام للمصادر مع صناعة معرفة في current_domain واحد وجمع terms وcandidate Claims أثناء القراءة. تسمح بـConcepts على أدلة مراجعة، وتمنع أي Master قبل اكتمال مصطلحات المجال كله؛ تضبط queue وdelta وcheckpoints ولا تفتح معرفة التالي قبل domain_done."
---

# التوجيه التسلسلي للمجالات

## عقد 2026-10-10

اقرأ [R/T/C/K/M/QA](../INDEX.md) و`<alignment_path>` والملحق في
`<user_messages_path>`؛ القفل على صناعة المعرفة لا على intake العالمي.

- R/`route_done` جائز لأي domain قبل extraction بعد full semantic read وتصنيف
  ونسخة مستقلة byte-exact متحققة في `done/<domain>/<subdomain>/`. النسخة افتراضية،
  و`source_refs` فهارس ثانوية فقط؛ done تصنيف وليس domain_done.
- الاستخراج والتعميق في `current_domain` فقط؛ الباقي `queued` وليس quarantined.
  quarantine لفساد/تعذر قراءة/هوية، uncertain للتصنيف الغامض، لا لتأجيل العمل.
- اجمع terms وcandidate Claims معًا أثناء القراءة دون انتظار كل المجال، ثم
  راجع الأدلة. Concepts تبدأ بالأدلة المراجعة بلا اختراع تعريفات.
- `source_done` استخراج كامل terms/Claims مع QA، بلا Concepts أو Master.
  `subdomain_extraction_done` لا يجيز Master: يلزم `domain_terms_complete`
  لكل المجال وكل فروعه قبل أي Master حتى الصغير. لا sample أو snapshot تخفي مرشحًا بلا قرار.
- احفظ الخلاف مع scope ولا تستبعد الرأي لمجرد اختلافه. `delta` تجعل التغطية
  `stale` وتحتاج queue ومراجعة أثرها؛ فقط `domain_done` يجيز معرفة التالي، بلا
  مجالين نشطين. لا إنشاء معرفة أو استخدام Codex بواسطة هذا المنسق.

## عقد التشغيل القابل للتهيئة

يقرأ orchestrator إعدادًا صريحًا قبل التشغيل:

```text
WIKI_ROOT                 = <wiki_root>
DOMAIN_SEQUENCE_PATH      = ترتيب المجالات المصرح به
CURRENT_DOMAIN_STATE_PATH = سجل المجال المفتوح
DOMAIN_LOCK_PATH          = مسار القفل المهيأ
STAGE_STATE_ROOT          = مسار حالات المراحل
AGENT_RESULT_ROOT         = مسار نتائج الوكلاء
CHECKPOINT_ROOT           = مسار checkpoints
HANDOFF_ROOT              = مسار handoffs
GATE_CONFIG_PATH          = تعريف بوابات R/T/C/K/M/QA ومراجعها
RUN_ID                    = معرف تشغيل ثابت
```

المسارات placeholders تُحل قبل التشغيل، وسجلات الملفات نسبيّة داخل الجذر؛
القوالب التالية وصف حقول لا سجلات حقيقية. لا تسمح بتغيير ترتيب الميثاق عبر
config محلي غير معتمد. اقرأ تعليمات المشروع وschema والميثاق ونظام التوجيه
كاملًا قبل التخطيط؛ اختلاف القيم أو العقود عائق موثق، لا سبب للتخمين.
لا يستنتج الترتيب من أرقام المجلدات أو أسماء الملفات. يتحقق من أن كل domain في
`DOMAIN_SEQUENCE_PATH` له catalog ومسار وفهرس وحالة معروفة، وإلا يوقف فتحه
ويسجل العائق.

## أدوار Agents وعقود التسليم

استخدم الأدوار التالية أو mapping موثقًا لأدوار مكافئة:

| الدور | المدخلات | المخرج المملوك | ما لا يملكه |
|---|---|---|---|
| `Orchestrator Agent` | config وحالات البوابات | lock، توزيع، حالة، checkpoints، قرار فتح | كتابة المعرفة بالجملة |
| `Intake/Classify Agent` | مصادر وسجلاتها وcatalog | Source/route وdedup وprimary/secondary | Terms أو Claims النهائية |
| `Terms Agent` | المقاطع المقروءة في المجال النشط | inventory تدريجي ثم دليل T للمجال كله | تعليق تسجيل Claims حتى T |
| `Claims Agent` | المقاطع المقروءة في المجال النشط | candidate Claims ثم تسليم C للمراجعة | انتظار T للتسجيل أو تسوية الخلاف قسرًا |
| `Concepts Agent` | Terms وClaims المقبولة | Concepts بحدود وعلاقات وأدلة | Master أو إخفاء الفجوات |
| `Master Agent` | T للمجال كله وC/K للأدلة وبوابة الحاجة | Master أو Masters وحالة coverage | بدء Master صغير بعد فرع فقط |
| `QA/Index Agent` | كل السجلات والروابط وcheckpoints | فحوص مستقلة، indexes، قبول/إرجاع، handoff | تعديل الدليل لإخفاء فشل |

لكل نتيجة استخدم `result_id`, `run_id`, `domain`, `subdomain`, `stage`, `agent_role`,
`input_refs`, `output_refs`, `status`, `checks`, `failures`, `next_action`.
وجود رسالة Agent لا يكفي؛ لا تُحتسب النتيجة دون ملف قابل للفحص.

حدد write allowlist منفصلة لكل Agent، وامنح ملكية واحدة لكل ملف مشترك. لا تجعل
Agent الاستخراج يراجع مخرجه مراجعة قبول نهائية. يستخدم المنسق وسيلة التفويض
المتاحة والمصرح بها فقط، بعد فحص schema الأداة؛ لا يفترض API بعينه. Worker
مكلّف لا ينشئ Agents بدوره ولا يوسع ملكيته. غياب وسيلة التفويض أو فشلها ينتج
blocker وتسليمًا للقائد، لا fallback يكتب به المنسق المعرفة بالجملة.

## القفل التسلسلي

استخدم **قفلًا معرفيًا مشتركًا واحدًا على مستوى الويكي/المهمة** في `DOMAIN_LOCK_PATH`،
لا قفلًا مختلفًا لكل `RUN_ID` يسمح بتشغيل مجالين بالتوازي. اقرأ أي قفل قائم
وتحقق من مالكه قبل محاولة حيازته حصريًا بآلية متحققة في المشروع:

```yaml
run_id: configured-run-id
owner_id: configured-orchestrator-id
state_version: configured-version
sequence_version: configured-version
current_domain: configured-domain
lock_status: held|released|blocked
opened_at: configured-timestamp
current_stage: extraction_review|concepts|masters|qa-close
allowed_next_stage: configured-stage-or-null
next_domain: configured-next-domain-or-null
release_evidence: null-or-checkpoint-ref
```

قواعد القفل:

1. لا يفتح أكثر من domain معرفي واحد حتى بين RUN_ID مختلفة. اسمح بالقراءة
   الدلالية للتصنيف وبنسخ المصادر وفهرسة routing لأي مجال pending، دون Terms
   أو Claims أو Concepts أو Masters له. route_done لا يحرر القفل المعرفي.
2. طبّق ترتيب اعتماد الأدلة، لا حظر تسجيل المرشحين: Terms وClaims المرشحة
   تجمعان أثناء القراءة؛ C يراجع ثم K يستعمل المراجع منها؛ M ينتظر T العام.
3. لا تحرر القفل إلا بقرار QA مستقل يثبت `domain_done` وفق عقد دورة المصدر
   والبوابات المهيأة.
4. عند الفشل، يبقى القفل على المجال الحالي `held` أو `blocked`، وحالة المجال
   مفتوحة. سجّل سبب الإرجاع والمرحلة التي ستُعاد؛ لا تفتح التالي لتجاوز العائق.
5. اكتب checkpoint الإغلاق وتحقق منه قبل تحرير القفل. الانتقال للمجال التالي
   يحتاج حيازة حصرية وفحص نفس `state_version` ومنع lost update، لا الكتابة
   فوق قفل تغير في أثناء الفحص.
6. القفل القديم أو غياب heartbeat لا يثبت موت مالكه. سجّل recovery قرارًا
   صريحًا بعد فحص النتائج والمهام الجارية؛ لا تحرره تلقائيًا بسبب الزمن.

## ترتيب المراحل داخل domain

افصل مسار R العالمي عن مسار المعرفة. داخل النشط يمكن توزيع مصادر مستقلة على
الاستخراج والمراجعة دون الكتابة المتعارضة؛ لا يعني هذا فتح مجال آخر. بوابات
الاعتماد تخص المخرجات التي يعتمد عليها العمل، وليست حظرًا على تدوين candidate.

### المرحلة 0: preflight وفتح domain

- اقرأ الميثاق والschema والـcatalog وعقد الإغلاق.
- تحقق من نظافة lock أو وجود resume صحيح.
- ثبت domain وsubdomains ونطاق العمل والمصادر المتوقعة.
- أنشئ checkpoint افتتاحيًا يحوي baseline والقيود وليس ادعاء نجاح.

### المسار العام: intake وrouting

- شغّل دورة `new-to-done-source-lifecycle` و`domain-discovery-and-routing`.
- ثبت القراءة الكاملة والبصمة وdedup والprimary route والمراجع الثانوية.
- تحقق من النسخة الفعلية في done ثم R؛ لا تنتظر extraction. أبقِ غير النشط
  queued، وافصل uncertain/quarantine بأسبابهما. لا source_done من R وحدها.

### داخل النشط: extraction وreview تدريجيان

- اجمع terms/aliases/relations وcandidate Claims بمواضعها أثناء القراءة؛
  القراءة الجزئية تنتج مرشحين وتغطية جزئية لا إعلان اكتمال.
- افصل direct quote وreported result وexample وinference وhypothesis بحسب schema
  وسجّل scope. راجع C لكل مساهمة والتعريفات بمصادرها، ولا تنتظر T لتوثيق اقتباس.
- source_done بعد استخراج المصدر كاملًا وQA، بلا K/M. جمع مصادر الفرع ومراجعتها
  ينتج subdomain_extraction_done، وجمع كل مصطلحات المجال المراجعة ينتج T.
- احفظ كل مرشح في snapshot مع قرار معلل؛ لا تستبعد unresolved ولا تسمّ عينة
  مجالًا كاملًا. أبقِ غياب تعريف صريح ظاهرًا بدل اختراعه.

### K: Concepts على أدلة مراجعة

- شغّل K على Claims مراجعة ذات تتبع ومصطلحات موثقة للنطاق؛ لا ينتظر T العام.
- اربط كل Concept بحدود وClaims وSources وعلاقات، وأظهر ما لا نعرفه والتعارضات.
- لا ترفع draft إلى accepted لمجرد اكتمال ملفه.

### M: Masters بعد T للمجال كله

- لا تبدأ أي Master حتى الصغير إلا بعد domain_terms_complete لكل المجال
  وكل subdomains، ثم C/K لأدلته والحاجة والتغطية والاسترجاع. كثرة الملفات
  أو إغلاق فرع أو snapshot غير شاملة ليست تصريحًا.
- افصل Index/Navigation عن Master الموضوعي، واحتفظ بحالة draft أو partial عند
  وجود فجوة بدل حشوها.
- لا تُجبر مجالًا كبيرًا على Master واحد ولا تجمع أقسامًا صغيرة بلا سؤال ونطاق
  موثقين. غياب دليل الحاجة إلى Master يبقي Gate M مفتوحة للمراجعة؛ ليس تصريحًا
  بتسجيل `domain_done` أو بتوليف محتوى مختلق لإرضاء العدد.

### QA وإغلاق domain

- شغّل QA/Index مستقلًا عن Agents الاستخراج.
- افحص schema، provenance، الروابط، التعارضات، الفهارس، raw invariants، وحالات
  كل subdomain.
- حدّث indexes وhandoff وسجل الإغلاق، ثم احسب `domain_done` فقط من الشروط
  المقاسة. عند PASS وبانتهاء جميع مهام المجال حرر القفل، وعند FAIL أعد المرحلة
  المناسبة وأعد فحص ما يعتمد عليها. لا تعلن الإغلاق مع Agent ما زال يعمل.

## Checkpoint بعد كل مرحلة

اكتب checkpoint به: checkpoint_id وrun_id وdomain وsubdomain_scope، snapshot
وبصمات input/output، stage وحالتها، counts_measured، checks ونتائجها الفعلية،
failures وunresolved_items وdecisions وagent_results وnext_action وتوقيت القياس.
اربطه بنسخة القفل وqueue وdelta لتجنب استئناف حالة stale كأنها اعتماد جديد.

لا يكتب checkpoint نصًا لم يُقرأ، ولا يحول `passed` لمرحلة إلى `domain_done`.
سجّل كل إعادة تشغيل كإصدار جديد مع رابط إلى السابق.

## الاستئناف والفشل

- عند انقطاع العملية، اقرأ lock وcheckpoint الأخيرين، ثم تحقق من البصمات
  والمسارات قبل الاستئناف.
- عند وصول مصدر أنشئ delta واربطه بـsnapshot المعنية، وعلّم التغطية التابعة
  stale للمخزون الأحدث دون محو الإغلاق التاريخي. إن كان للمجال النشط فادمجه
  وراجع T والمخرجات المتأثرة قبل M أو الإغلاق؛ وإلا route_done ثم queued.
- delta لمجال سابق مغلق تبقى queued مع سبب وأثر وجدولة معلنة، لا يُعاد فتحه
  بالتوازي. راجع أثرها قبل الانتقال التالي؛ إذا نقضت دليلًا يعتمد عليه الإغلاق
  فأوقف الانتقال حتى المعالجة المصرح بها بمجال واحد. المؤجل لا يعد معالجًا.
- عند فشل Agent، سجل `agent_failure` والمخرج الجزئي ومساره والقرار التالي؛ لا
  تستبدل الفشل بادعاء اكتمال.
- عند تعارض بين QA وAgent، يبقى العنصر مفتوحًا حتى يصدر قرار مراجعة مستقل.
- عند غياب صلاحية الكتابة أو مسار نتيجة، أوقف المرحلة وسجل blocker بدل الكتابة
  في مسار بديل غير مهيأ.

## شروط فتح المجال التالي

لا يغير orchestrator `current_domain` إلا إذا كان سجل الإغلاق يثبت:

1. كل subdomain مطلوب مكتمل الاستخراج، مع جميع المرشحين وقراراتهم وT للمجال كله.
2. نجحت T/C/K/M المطلوبة وQA بأدلتها؛ الفجوات غير المراجعة لا تُخفى. الخلاف
   المدعوم المراجع مع scope لا يشترط حسمه إلى رأي واحد لإغلاق المعرفة.
3. لا مصدر تابع حالته new أو قيد المراجعة أو بلا قرار نهائي؛ لا uncertain أو
   quarantine غير محسوم، ولا route أو artifact أو رابط مكسور. بقاء البايتات
   الأصلية في new مقصود ولا يخلط بالحالة المنطقية.
4. فهارس root/domain/subdomain/layer محدثة ومطابقة للملفات.
5. QA مستقل راجع الاسترجاع والروابط والفهارس والتتبع وdelta ثم سلّم handoff؛
   لا يُعلن PASS لمجرد أن script أو جرد ملفات نجح.
6. يوجد سجل `domain_done` موقّع بدور QA ومؤكد من القائد، مع mapping واضح إلى
   `domain.status: done` إن استعمل العقد ذلك. لا يُحقن domain_done في Source
   schema ولا يُطلب تغيير عقد قائم لمجرد اختلاف التسمية.

بعدها فقط:

```text
write closure checkpoint
verify closure, all agent results and lock ownership
release current lock
open next domain from DOMAIN_SEQUENCE_PATH
```

إذا غاب أي شرط، يبقى المجال الحالي مفتوحًا، ويظل المجال التالي مغلقًا حتى لو
كانت له ملفات موجودة.

## حالات تحقق التشغيل — متوقعة وليست نتائج منفذة

- طلب معرفتين في مجالين: واحد فقط يحوز القفل؛ الآخر queued، لكن R له مسموحة.
- رسالة Agent ناجحة دون ملف أو verifier: لا تُحتسب بوابة ناجحة.
- T جزئية: candidate Claims مسموحة وK على أدلة مراجعة مسموحة؛ أي Master ممنوع.
- فرع مكتمل فقط: لا Master صغير؛ source_done بلا Master جائز بعد extraction+QA.
- انقطاع بعد كتابة النتائج وقبل QA: resume يتحقق ولا يقفز للإغلاق.
- `domain_done` قديم مع hash جديد: stale، ولا تحرير قفل اعتمادًا عليه.
- إغلاق مثبت كاملًا: checkpoint ثم تحرير ثم فتح التالي وحده.

## ممنوعات

- لا تشغل معرفة المجال التالي بالتوازي مع domain مقفول؛ الفرز العام مستثنى.
- لا تتجاوز بوابات الاعتماد ولا تحولها إلى حظر على تسجيل المرشحين.
- لا تجعل Orchestrator يكتب المعرفة بدل Agents أصحاب الأدوار.
- لا تعتبر عدد الملفات أو رسائل الوكلاء دليل إغلاق.
- لا تعدل raw أو تخفي failures أو تحذف checkpoints تاريخية.
- لا تستخدم Codex بأي صورة في هذه الدورة.
