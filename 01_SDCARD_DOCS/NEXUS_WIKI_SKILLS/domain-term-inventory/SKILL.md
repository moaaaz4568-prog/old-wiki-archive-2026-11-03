---
name: domain-term-inventory
description: "تُستخدم لجمع terms وaliases وrelations بالتوازي مع candidate Claims أثناء قراءة المجال النشط، ثم مراجعة جرد جميع مصادر المجال وفروعه لإثبات domain_terms_complete قبل أي Master حتى الصغير. لا تؤخر تسجيل الاقتباسات حتى اكتمال القراءة، ولا تختلق تعريفات أو تعتبر فرعًا أو عينة مجالًا كاملًا."
---

# جرد مصطلحات المجال

## عقد 2026-10-10

اقرأ [R/T/C/K/M/QA](../INDEX.md) و`<alignment_path>` والملحق في
`<user_messages_path>`؛ افصل التسجيل المرشح عن قبول الطبقة.

- R يسمح بـ`route_done` قبل extraction: full semantic read وتصنيف ونسخة
  مستقلة byte-exact متحققة في `done/<domain>/<subdomain>/` هي الافتراضية.
  `source_refs` فهارس ثانوية لا بديل للنسخة؛ `done` لا يعني `domain_done`.
- الفرز العام لأي domain جائز؛ هذه المهارة تستخرج في `current_domain` فقط،
  والباقي `queued` لا quarantine. العزل لفساد/تعذر قراءة/هوية، والغموض uncertain.
- اجمع terms وcandidate Claims أثناء القراءة معًا بمواضع أدلتها؛ لا تنتظر
  قراءة المجال كله. `source_done` استخراج كامل terms/Claims مع QA بلا حاجة
  إلى Concepts أو Master؛ `subdomain_extraction_done` لا يتطلبهما كذلك.
- Concepts تبدأ بالأدلة المراجعة بلا اختراع تعريفات. T=`domain_terms_complete`
  لكل المجال وكل فروعه شرط قبل أي Master حتى الصغير، لا مجرد اكتمال فرع.
  snapshot ليس sample ولا يستبعد مرشحًا بلا قرار. الخلاف محفوظ مع scope.
- وصول `delta` يجعل التغطية `stale`، ويعالج في النشط أو يصطف في queue؛ فقط
  `domain_done` يجيز معرفة التالي، ولا يُفتح مجالان.

## الغرض

ابدأ inventory مرشحًا منذ القراءة الأولى للمجال النشط، واستكمله دون فقد أدلة.
ميّز الاسم القياسي وalias والعلاقة والسياق؛ سجل مواضعها لا معرفة من الذاكرة.

إذا كان manifest القراءة جزئيًا، سجّل مرشحي المقاطع المقروءة فورًا مع حدود
التغطية، ثم استكمل الناقص. لا تسمّ القائمة نهائية من عينة أو preview.
عند تغيّر البصمات أو غياب مصدر، أوقف البوابة وأعده إلى دورة المصدر؛ لا تصحح
الدليل الخام لتجاوز العائق.

## عقد التشغيل القابل للتهيئة

استخدم إعدادًا يصرح بالنطاق دون افتراض أسماء ثابتة:

```text
WIKI_ROOT                 = <wiki_root>
DOMAIN_ID                 = معرف المجال المهيأ
SUBDOMAIN_ID              = معرف القسم أو null عند جرد domain كامل
READING_MANIFEST_PATH     = manifest جميع المرشحين وحالة قراءة كل منهم، لا المكتملين فقط
SOURCE_RECORD_ROOT        = سجلات Source المهيأة
TERM_INVENTORY_ROOT       = مسار inventory المهيأ
TERM_INDEX_PATH           = فهرس الطبقة المهيأ
TERMS_GATE_CONFIG_PATH    = قواعد البوابة وإصدارها
DOMAIN_STATE_PATH         = سجل المجال المفتوح والقفل
RUN_ID                    = معرف تشغيل ثابت
```

القيم placeholders تُحل قبل التشغيل، وكل مسار سجل نسبي داخل `WIKI_ROOT` وآمن
بعد حل الروابط الرمزية. القوالب أدناه تصف الحقول والبدائل، ولا تُحفظ بأسماء
مثالية أو values مفصولة بـ`|` في سجل فعلي. لا تفترض وجود Term schema أو verifier
مركب؛ إن لم يعرّفهما العقد، احفظ inventory في staging المصرح به كمرشح للمراجعة.
اقرأ الميثاق وschema وعقد المجال المهيأ قبل الكتابة. إذا لم يمكن إثبات أن كل
مصدر داخل النطاق قد قُرئ كاملًا، أبقِ inventory جزئيًا وT غير مكتملة مع قائمة
النقص؛ هذا لا يوقف تسجيل مرشحي المقاطع المقروءة.

## تعريف النطاق وقراءة corpus

1. ثبّت `DOMAIN_ID` و`SUBDOMAIN_ID` ونطاقهما وإصدار catalog وmanifest في
   checkpoint، وافحص تطابق domain مع القفل. لا توسع النطاق لمجال آخر لأن
   اسم ملف أو كلمة بدت مرتبطة، ولا تُسقط مصدرًا من النطاق لتسهيل الإغلاق.
2. استخرج قائمة المصادر من `READING_MANIFEST_PATH`، وتحقق من وجود كل Source
   ومن تطابق `source_id` و`content_hash` و`source_path`.
3. اقرأ كل مصدر كاملًا من أول بايت/سطر إلى EOF وفق سياسة القراءة المعتمدة. لا
   تستبدل القراءة الكاملة بالعنوان أو أول جزء أو عدد ثابت من الملفات.
4. سجّل عدد المصادر المتوقع والمقروء، وأي مصدر مفقود أو متغير أو معزول، مع أثر
   ذلك على التغطية. أبقِ `raw/` دون تعديل.
5. افصل بين مفردات المصدر وبين المرادفات التي اقترحها extractor؛ الاقتراح لا
   يصبح مصطلحًا مقبولًا دون provenance ومراجعة.
6. قارِن جرد المصادر الحالي بالـmanifest لكشف مصدر أُضيف أو بقي بلا قرار. لا
   تمنح قراءة subdomain بوابة domain كاملًا؛ لا تنجح بوابة domain حتى تغطي جميع
   أقسامه. في exact duplicates يجوز إعادة استخدام قراءة canonical المتحققة،
   مع إثبات تطابق البايتات وربط جميع المسارات، لا عدّها أدلة مستقلة.
7. اكتب `read_audit` لكل مصدر: hash، EOF، عدد البايتات، المقاطع المقروءة بلا
   فجوات، والترميز/نسخة parser. لا يُعد تشغيل hash أو عدّ الأسطر قراءة دلالية.

## استخراج بطاقة المصطلح

استخدم سجلًا قابلًا للتمديد، وتحقق من مطابقة الحقول لعقد المشروع قبل اعتماده:

```yaml
term_id: TERM_domain_local-id
canonical_label: label-as-observed-or-reviewed
language: ar|en|mixed|unknown
domain: configured-domain
subdomain: configured-subdomain-or-null
definition_status: observed|reviewed|missing|disputed
operational_definition: null-or-source-supported-text
scope: configured-scope
aliases:
  - alias: observed-alias
    alias_type: abbreviation|spelling_variant|translation|acronym|unknown
    status: candidate|reviewed|disputed
    provenance:
      - source_id: configured-source-id
        content_hash: "sha256:<measured-64-hex>"
        locator: "<locator>"
        evidence_quote: "<exact-quote>"
relations: []
provenance:
  - source_id: configured-source-id
    source_path: relative/path/from/wiki-root
    content_hash: "sha256:<measured-64-hex>"
    locator: "<locator>"
    excerpt: exact-short-excerpt-or-reference
    evidence_kind: definition|usage|alias|relation
status: candidate|reviewed|accepted|disputed|blocked
created: configured-date
updated: configured-date
```

اربط provenance بالتعريف والاسم أو alias أو relation المعني، لا بقائمة مصادر
عامة فقط. ثبّت نظام المواضع: line 1-based inclusive أو Unicode offset
zero-based end-exclusive، وتحقق من تطابق الاقتباس حرفيًا مع النص ذي البصمة
المسجلة. إن كان النص مشتقًا فاحفظ parser ومطابقة مواضعه إلى الخام.

### الاسم القياسي والتعريف

- افصل spelling أو ترجمة أو اختصارًا عن الاسم القياسي، وسجّل سبب اختيار
  `canonical_label` ومواضع استعماله.
- لا تكتب تعريفًا من المعرفة العامة لمجرد أن المصطلح مألوف. عند غياب تعريف
  صريح استخدم `definition_status: missing` أو صيغة مرشح موسومة.
- إذا اختلف المعنى بين مصدرين أو سياقين، احتفظ بالتمييز والسياق بدل دمجهما في
  تعريف واحد.

### aliases

سجّل alias فقط مع موضع يدل على أنه يشير إلى المصطلح نفسه في ذلك السياق. لا تدمج
مصطلحين لمجرد التشابه الإملائي، ولا تجعل الترجمة مساوية تلقائيًا إذا اختلف
النطاق. عند الشك استخدم `disputed` أو `candidate` مع سبب قابل للمراجعة.

### relations

يمكن تسجيل علاقة مصطلحية typed مثل `alias_of`, `broader_than`, `narrower_than`,
`related_to`, أو `contrasts_with` إذا كان catalog العلاقات يسمح بها. لكل علاقة
سجّل الطرفين، نوعها، اتجاهها إن كان مهمًا، السياق، وprovenance مستقلًا:

سجل العلاقة يحوي `relation_id`, `relation_type`, `subject_term_id`,
`object_term_id`, `status`, `rationale` وprovenance بنفس عقد بطاقة المصطلح:
source_id وcontent_hash وlocator واقتباس. لا تعِد استخدام provenance المصطلح
للعلاقة إلا إذا كان الموضع يثبت العلاقة نفسها.

العلاقة المقترحة ليست حقيقة مستقلة. لا تسجل `supports` أو `contradicts` بين
مصطلحين إلا إذا كان عقد المشروع يستخدمهما لذلك الغرض وبوجود موضع يثبت المعنى.

## إزالة التكرار والتعارض داخل inventory

1. طبع المقارنة في الذاكرة فقط عند الحاجة، ولا تغير نص المصدر أو بصمته.
2. ميّز بين exact duplicate لسجل term، وalias، وhomonym متشابه الاسم مختلف
   المعنى، ومرشح normalized duplicate.
3. لا تحذف السجل المتعارض. اربط السجلات بمعرفات محلية، واحفظ سبب عدم الدمج.
4. إذا كان مصطلح مركزي بلا provenance، أنشئ فجوة `missing_provenance` وأبقِ
   حالته غير مقبولة.

## بوابة T للمجال كله قبل أي Master

لا تسجل `domain_terms_complete` إلا بعد مراجعة مستقلة وتحقق الآتي وفق الحسم
الأحدث. لا تستخدم pass محلية لفرع بوصفها T للمجال الرئيسي:

- manifest المجال كله يطابق جرد المرشحين في جميع subdomains، مع حدود snapshot
  وتاريخه وبصماته وقرارات الإدراج والاستبعاد المعللة. المصدر غير المقروء أو
  غير المحسوم يبقى في مقام التغطية ويمنع اكتمالها، لا يُسقط لتجميل النسبة.
- كل مصطلح مقبول له `term_id` فريد واسم قياسي ونطاق وحالة واضحة.
- كل تعريف أو alias أو علاقة مقبولة لها source وlocator وhash قابل للحل.
- كل مصطلح مستخرج مراجع وله provenance وتقييم وحدود: تعريف صريح، استعمال فقط،
  أو خلاف موثق. لا تخترع تعريفًا لإغلاق T، ولا تستخدم `missing` بوصفه تعريفًا
  مقبولًا في Concept/Master. المانع هو نقص الاستخراج أو التقييم أو التتبع،
  وليس تعدد تعريفات مشروطة موثقة أو عدم إجماع المصادر.
- لم تُحوّل كلمة من عنوان أو مثال إلى مصطلح مؤسس دون دليل متن.
- لا توجد سجلات مكررة غير محسومة مخفية تحت الاسم نفسه.
- inventory وmanifest وINDEX المحلي متسقة، وcheckpoint يثبت ما قيس.
- حالة البوابة وإصدار القاعدة وتاريخها ومسار التقرير محفوظة.

عند نقص التغطية أبقِ T غير مكتملة، **واستمر في تسجيل candidate Claims والمصطلحات
من الأجزاء المقروءة**. C يراجع مساهمات المصدر، وK يستخدم Claims المراجعة وما
يلزمه من مصطلحات موثقة دون اشتراط T العام. لا يبدأ M قبل T لكل المجال وC/K
للأدلة التي يعتمدها. اكتمال استخراج مصدر أو فرع يمكن إثباته قبل ذلك، ولا يعني
أن Master صغيرًا مسموح. سلّم coverage والفجوات والتقييمات إلى المراجعين.

## مخرجات التشغيل

أنشئ فقط المخرجات المصرح بها في الإعداد، مثل:

- سجلات Terms أو manifest inventory مشتق.
- تقرير تغطية يربط العدد المقاس بالمصادر، لا ادعاء اكتمال من عدد السجلات.
- سجل unresolved/disputed/missing مع provenance المتاح.
- `TERM_INDEX_PATH` محدث، وcheckpoint، وحزمة handoff.

لا تكتب في `raw/`، ولا تعدل Source أو Claim أو Concept أو Master خارج صلاحية
الدور، ولا تنقل النص الكامل إلى inventory بلا سياسة مستقلة.

## إعادة التشغيل والفحص

- استخدم `(DOMAIN_ID, SUBDOMAIN_ID, source_hash_set, ruleset_version)` كمفتاح
  تشغيل. إذا تغيرت مجموعة البصمات أعد الجرد المتأثر وسجّل الإصدار السابق.
- قبل إعلان T، أعد جرد المرشحين لاختبار delta. وصول جديد يجعل الدليل القديم
  stale بالنسبة للمخزون الأحدث: أضف مساهماته وراجعها في المجال النشط، أو اجعله
  queued لمجاله. لا تعمم snapshot القديمة، ولا تبدأ Master على T متقادمة.
- افحص أن كل provenance يحل إلى مصدر موجود وأن locator يعيد النص المتوقع.
- افحص أن كل alias أو relation يشير إلى term ID موجود أو إلى مرشح معلّم.
- قارِن inventory الحالي بالسابق لاكتشاف انجراف الاسم أو التعريف أو العلاقة.
- ثبّت IDs حسب المعنى والنطاق، لا حسب ترتيب السجلات أو التهجئة فقط. إعادة نفس
  corpus تعيد استخدام السجل القائم وتضيف provenance الجديد فقط دون صف مكرر.
- حالات تحقق متوقعة وليست نتائج منفذة: alias متماثل اللفظ مختلف المعنى لا يدمج؛
  علاقة بلا locator تبقى candidate؛ مصدر مطلوب غير مقروء يمنع T لا تسجيل
  مرشحي مصدر آخر؛ فرع كامل لا يسمح بـMaster صغير؛ رأيان مراجعان محفوظان لا
  يُختزلان قسرًا؛ إعادة التشغيل لا تكرر IDs أو provenance.

## ممنوعات

- لا تقرأ عينة وتعلن إغلاق domain أو subdomain.
- لا تخترع تعريفًا أو alias أو relation بلا موضع مصدر.
- لا تساوِ بين المصطلحات لمجرد تشابه التهجئة.
- لا تحذف التعارضات أو السجلات المرفوضة؛ اجعلها مرئية.
- لا تبني Concept من أدلة غير مراجعة أو Master قبل domain_terms_complete.
- لا تعدل `raw/` أو تستبدل مصدر الحقيقة بسجل مشتق.
- لا تستخدم Codex في أي خطوة.
