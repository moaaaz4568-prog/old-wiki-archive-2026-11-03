# Nexus LLM Wiki New

هذه مساحة بناء منفصلة لنظام معرفة قابل للتتبع والاسترجاع للنماذج اللغوية. الويكي
القديمة تحت `/sdcard/Nexus_Brain/Nexus_Brain/` مصدر دراسة فقط ولا تُعدَّل من هذا
المشروع. الجذر هو `/sdcard/NEXUS_LLM_WIKI/`.

## الهدف

تحويل المصادر إلى معرفة قابلة للمراجعة، مع الفصل بين:

- ما يقوله المصدر.
- ما ينقله المتحدث أو يبلغه عن تجربته.
- المثال التوضيحي.
- الاستنتاج التحليلي.
- الفرضية أو نتيجة المحاكاة.

الموجة الأولى متعددة المجالات (`sales`، `outreach`، `pricing_offers`،
`content_strategy`)؛ intake عام، لكن العمل المعرفي له مجال نشط واحد في كل مرة.

## الطبقات

```text
new/       صندوق استقبال مستقل
raw/       مصادر غير قابلة للتعديل
done/      نسخة مصدر مباشرة متحققة تحت <domain>/<subdomain>
sources/   سجلات هوية المصدر ومساره وحالته
claims/    ادعاءات ذرية مرتبطة بموضع دليل
concepts/  توليفات مفهومية قابلة للقراءة
masters/   كتب قرار تبدأ بعد بوابة T الشاملة للمجال
indexes/   فهارس مشتقة وقابلة للرجوع
systems/   مواصفات العمليات والبوابات
```

## حالة البناء ومسار الفحص

لا تحتوي هذه الصفحة أعدادًا ثابتة للمصادر أو Claims أو Concepts؛ الأعداد القديمة لا
تُعد حالة حالية. آخر حالة موثقة هي حالة البنية والـconfig في
`config/processing_order.json`: لقطة أولية، والبوابات `not_closed`/`not_evaluated`
حيث لم تُقَس، وليست إعلان إغلاق. يعرض `masters/INDEX.md` أي Master موروث بحالة
`draft`/`partial`؛ يظل مسودة غير معتمدة ولا يُعاد وصفه بأنه غير موجود أو canonical.

لإعادة فحص الحالة الفعلية من القرص استخدم، دون اعتبار الناتج وحده شهادة اكتمال:

```bash
python3 tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json
```

ثم افحص روابط الفهارس ومسارات العودة إلى المصدر والـsnapshot والبوابات وفق
التقرير [مراجعة التكامل](reports/sales-proof/MULTIDOMAIN_INTEGRATION_REVIEW_2026-10-10.md)
والعقود المشار إليها فيه. `wiki_quality.py` فحص بنيوي مساعد؛ لا يثبت وحده القراءة
الدلالية، أو offset الاقتباس، أو T لكل المجال، أو صلاحية Master، أو كل امتدادات
workflow الجديدة.

## موقع كل ملفات المشروع

الجذر الوحيد المعتمد للويكي والأنظمة والتقارير ومخرجات الـAgents هو
`/sdcard/NEXUS_LLM_WIKI/`. لا تُنشأ مخرجات جديدة في `/root/r/`. راجع
`PROJECT_OUTPUT_LOCATION_2026-10-10.md` و`reports/sales-proof/README.md` لسياسة
المسارات وسجل نقل التقارير المرحلية.

## مسار المصدر وترتيب القراءة

يبقى الأصل في `new/` أو `raw/new/`، وبعد route ناجح تُنشأ نسخة مستقلة byte-exact
مباشرة تحت `done/<domain>/<subdomain>/` مع `REF_` و`ROUTE_` و`INDEX.md`. `route_done`
ليس `source_done`، و`source_done` يعني المصدر الكامل لا مساهمة مجال جزئية؛ اسم
المساهمة الجزئية/المكتملة هو `source_domain_extraction_complete`.

ابدأ بـ`SCHEMA.md` ثم `AGENTS.md` ثم
`MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md`. بعد ذلك اقرأ العقد العام في
`systems/13–19` بحسب المهمة، ثم النظام الأساسي المقابل. لا تبدأ أي Master قبل
`domain_terms_complete` (T) لكل مصادر وأقسام snapshot المجال، مع مراجعة Claims و
Concepts التي يعتمد عليها؛ ولا يشترط إجماع مصطنع بين مصادر تختلف باختلاف السياق.

## كيف يكمل نموذج جديد العمل

اتبع ترتيب القراءة المختصر التالي، مع اعتبار كل مسار نسبيًا إلى جذر الويكي:

1. ابدأ بـ [START_HERE.md](START_HERE.md) لفهم خريطة التشغيل والحدود.
2. اقرأ [AGENTS.md](AGENTS.md) لتثبيت الصلاحيات وقواعد المصدر والحالات.
3. راجع [SCHEMA.md](SCHEMA.md) قبل تفسير أي سجل أو كتابة مخرج.
4. اقرأ [النظام 20](systems/20_WIKI_OPERATING_SYSTEM.md)، ثم [النظام 21](systems/21_SOURCE_TO_KNOWLEDGE_PIPELINE.md)، ثم [النظام 22](systems/22_WRITING_AND_EVIDENCE_SYSTEM.md).
5. تابع بـ [النظام 23](systems/23_RETRIEVAL_QA_AND_HONEST_STATUS.md)، ثم [النظام 24](systems/24_AGENT_HANDOFF_AND_RECOVERY.md)، ثم [النظام 25](systems/25_CHANGE_CONTROL_AND_UPDATE_PROTOCOL.md).
6. اختم بـ [بروتوكولات تشغيل النموذج](model_protocols/README.md)، ثم نفّذ المهمة ضمن النطاق المصرح به مع إبقاء الدليل والحالات غير المحسومة ظاهرين.

## الحالة الحالية الموثقة

- **Corpus manifest:** يحتوي `collections/corpus/manifest.jsonl` على 2,541 سجلًا.
- **Config الحالي:** يحدد أربعة domains هي `sales` و`outreach` و`pricing_offers` و`content_strategy`، و`sales` هو المجال النشط.
- **Sales route/copy والاستخراج:** توجد ثلاث نسخ route/copy لـ`sales`، وثلاث extraction batches.
- **حالة النتائج:** نتائج الاستخراج مرشحة `candidate`، وليست اعتمادًا أو اكتمالًا.

README نفسه لا يثبت هذه الأرقام؛ المرجع الفعلي هو الملفات المشار إليها: `collections/corpus/manifest.jsonl` و`config/processing_order.json` وملفات route/copy في `done/sales/` وملفات الدفعات في `collections/sales/extraction_batches/`.
