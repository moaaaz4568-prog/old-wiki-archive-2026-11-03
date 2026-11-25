# مراجعة موقع المخرجات والترحيل — 2026-10-10

**الدور:** Reviewer مستقل، قراءة وفحص فقط.

**نطاق الكتابة:** هذا التقرير هو الملف الوحيد الذي أُنشئ في هذه المراجعة. لم
أعدّل الويكي أو `raw/` أو `done/` أو `config/` أو أي ملف آخر، ولم أستخدم Codex
أو subagents، ولم أجرِ مراجعة دلالية لملفات `raw/` الكثيرة.

## القرار

**PASS_FOR_CANONICAL_LOCATION**

اجتازت مراجعة الموقع canonical والترحيل جميع الشروط المطلوبة. هذا القرار خاص
بموقع المخرجات وسلامة الترحيل والروابط النشطة، ولا يعني اكتمال أي domain أو
اجتياز بوابات المعرفة R/T/C/K/M/QA.

## الملفات المقروءة

قُرئت سياسة الموقع أولًا:
`PROJECT_OUTPUT_LOCATION_2026-10-10.md`، ثم:

- `AGENTS.md`, `README.md`, `INDEX.md`.
- `config/processing_order.json`, `config/domain_catalog.json`.
- `reports/INDEX.md`, `reports/sales-proof/README.md`.
- `reports/sales-proof/MIGRATION_MANIFEST_2026-10-10.tsv`.
- `systems/INDEX.md`, `systems/13_MULTI_DOMAIN_ARCHITECTURE.md`,
  `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md`,
  `systems/18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md`.
- نسخة `reports/sales-proof/SOURCE_SESSION_EF22.md` للتحقق من وجودها وبصمتها؛
  لم تُقرأ دلاليًا كاملة.

## الأدلة والنتائج

### 1. الجذر canonical

- السياسة تحدد الجذر الوحيد في `PROJECT_OUTPUT_LOCATION_2026-10-10.md:5-9`.
- وتحدد مكان التقارير في `:15-30`، وتوضح أن النسخ القديمة خارج الجذر القانوني
  لا تُستخدم كمسار تشغيل في `:32-49`.
- `AGENTS.md:10-13` و`README.md:54-59` و`INDEX.md:72-74` تؤكد القاعدة نفسها.
- الفحص من القرص أثبت أن `/sdcard/NEXUS_LLM_WIKI/` موجود، وأن ملف التقرير
  canonical نفسه أُنشئ داخل `reports/sales-proof/`.

### 2. manifest الترحيل: 19/19

فحصتُ كل صف بيانات في `MIGRATION_MANIFEST_2026-10-10.tsv:1-20`، لا العنوان
فقط:

```text
manifest_header_fields=['file', 'source_path', 'source_sha256',
 'destination_path', 'destination_sha256', 'size_bytes', 'action']
record_count=19
records_pass=19/19
failures=[]
unique_destination_paths=19/19
all_actions_copied=True
all_manifest_destinations_exist=True
destination_paths_under_canonical_root=True
```

لكل سجل تحققتُ من وجود المصدر والوجهة، وحسبت SHA-256 فعليًا للطرفين، وقارنت
البصمتين بالقيمتين المسجلتين، وقارنت الحجم بالقيمة المسجلة. لا يوجد صف ناقص أو
وجهة مكررة أو اختلاف hash/حجم.

### 3. `SOURCE_SESSION_EF22.md`

- صف النسخة في `MIGRATION_MANIFEST_2026-10-10.tsv:20` موجود ومحدد بحجم
  `792533` وبصمة واحدة للمصدر والوجهة.
- كلا الملفين موجودان على القرص.
- البصمتان الفعليتان متطابقتان مع manifest:
  `70b1315d3c3596a09005d033d82a88e9bd29573f0649f604647936dbe512ce4f`.
- فحص byte comparison أعاد `cmp_source_session_exit=0`.

### 4. JSON والمسارات

- `processing_order.json` و`domain_catalog.json` اجتازا `json.loads`.
- لم يُعثر على أي قيمة تحتوي مرجع تشغيل إلى المسار القديم في أي من الملفين:
  `root_r_refs=[]`.
- `processing_order.json:18` يحيل إلى تقرير داخل الجذر canonical، ونتيجة الفحص
  أكدت أن المرجع موجود.
- في `domain_catalog.json:7-26,87-90`، مراجع الأدلة/الـraw كلها تحت sdcard
  وموجودة. أما مسارات Vault القديمة الظاهرة في `:114-120` وما شابهها فهي
  موجودة فعليًا تحت sdcard، وموسومة في سياسة الملف `:56-60` كمراجع بنيوية فقط؛
  ليست مكان مخرجات ولا بديلًا عن الجذر canonical.
- ترتيب المجالات الأربعة مطابق بين الملفين:

```text
order_catalog_match=True
['sales', 'outreach', 'pricing_offers', 'content_strategy']
```

### 5. الروابط والمراجع النشطة

عرّفتُ الملفات النشطة هنا بأنها ملفات السياسة/الفهرسة/العقود التي طلبها
التكليف، مع ملفات JSON بوصفها مراجع مسارات. فحص Markdown links في 10 ملفات
نشطة أعاد:

```text
active_files=10 markdown_links=81 unresolved_links=0
```

ثم وسّعتُ الفحص إلى 28 ملفًا تشغيليًا (الملفات النشطة ونسخ التقارير المرحلية
المهاجرة، مع استبعاد نسخة جلسة المصدر التاريخية)؛ النتيجة:

```text
files_checked_excluding_historical_source_session=28
markdown_links_checked=95
unresolved_operational_links=0
```

إذًا لا يوجد رابط Markdown تشغيلي مكسور في النطاق النشط المفحوص.

#### فصل الرابط المكسور عن provenance التاريخي

الفحص الأوسع الذي شمل نسخة جلسة المصدر نفسها سجل 97 تطابقًا ظاهريًا غير محلول؛
كلها ظهرت داخل `SOURCE_SESSION_EF22.md`، وهي نسخة مصدر/سجل جلسة وليست تقرير
تشغيل حيًا. الأمثلة تشمل روابط Claims/Concepts قديمة، أسماء ملفات ذاكرة،
ومقطعًا تاريخيًا يحيل إلى ملف في مساحة العمل السابقة. هذه **provenance تاريخية**
داخل سجل منقول، وليست مراجع تشغيل جديدة للمشروع. يؤكد ذلك:

- `reports/sales-proof/README.md:21-22` يعرّف `SOURCE_SESSION_EF22.md` كنسخة
  مصدر للتحقق من الاستخراج.
- `reports/sales-proof/README.md:15` يقرر صراحة أن ظهور المسار القديم داخل
  تقرير قديم لا يجعله مسار تشغيل.
- manifest يفرق بين `source_path` التاريخي و`destination_path` canonical في
  كل صف من `:2-20`.

وعليه لم أخلط هذه الآثار التاريخية مع رابط مكسور في ملف نشط، ولم أُصلح أو أعد
كتابة أي تقرير منقول.

### 6. عدم ادعاء إكمال domain بسبب path migration

لا يوجد ادعاء بأن نقل الملفات أكمل domain:

- `processing_order.json:14-17` يثبت أن `sales_completion_claim` هو `false`.
- حالات المجالات في `processing_order.json:121-217` كلها `domain_done:
  not_closed`، والبوابات `not_closed` أو `not_evaluated`.
- `domain_catalog.json` يضع `completion_claim: false` للمجالات، ويصرح في
  `:68-75` بأن قياس التغطية في هذه اللقطة غير منفذ.
- manifest نفسه يسجل نسخ ملفات فقط (`action=copied`) ولا يحتوي قرار إغلاق
  مجال.
- فحص 19 تقريرًا مهاجرًا بحثًا عن ادعاء إكمال domain أعاد:

```text
reports_checked=19
substantive_domain_completion_hits=0
```

والتطابق الوحيد في فحص واسع كان قالب مسار حرفيًا
`done/<domain>/<subdomain>/`، لا ادعاء إكمال.

## الفحوص التي شُغّلت

1. Parser/تحقق manifest مخصص للقراءة فقط: **19/19 PASS**.
2. `cmp` لنسخة `SOURCE_SESSION_EF22.md`: **exit 0**.
3. JSON parser للملفين: **PASS**؛ لا root-path تشغيلية قديمة.
4. فاحص Markdown links للنطاق النشط: **81/81 محلولة**.
5. فاحص الروابط للنطاق التشغيلي الموسع دون سجل الجلسة التاريخي:
   **95/95 محلولة**.
6. `python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault
   /sdcard/NEXUS_LLM_WIKI --json`: **exit 0**, `ok:true`, `errors:[]`.
   العدادات التي أعادها الفحص: `sources=1781`, `claims=1777`, `concepts=34`,
   `masters=1`; وهذا فحص بنيوي مساعد فقط.
7. التقرير لم يكن موجودًا قبل إنشائه، ثم أُنشئ في المسار canonical فقط. فحص
   LSP للتقرير بعد الإنشاء: **No diagnostics found**.

## ملاحظات غير حاجبة

- مراجع Vault القديمة في `domain_catalog.json` ليست مسارات مخرجات؛ هي مراجع
  بنيوية موجودة ومعلنة كذلك داخل config. لا أعدها فشلًا في شرط «sdcard لا
  المسار القديم» لأنها ليست تحت المسار القديم ولا تُستخدم كمسار report/done.
- نجاح `wiki_quality.py` لا يثبت قراءة دلالية أو اكتمال domain؛ هذا متسق مع
  `README.md:42-52` و`AGENTS.md:93-105` ومع تصميم config نفسه.

## ما لم أختبره عمدًا

- لم أقرأ آلاف ملفات `raw/` دلاليًا ولم أعدّ ذلك دليلًا على اكتمال المعرفة.
- لم أنفذ intake أو route verifier أو نسخ مصادر جديدة.
- لم أتحقق من بوابات R/T/C/K/M/QA أو اختبارات retrieval؛ هذه خارج مراجعة
  موقع المخرجات.
- روابط الأمثلة والقوالب التي تحتوي placeholders مثل `<domain>` ليست روابط
  تنفيذية، ولذلك لم أعدّ غياب ملفاتها finding.

## الملفات المتغيرة

هذا التقرير فقط:

`/sdcard/NEXUS_LLM_WIKI/reports/sales-proof/LOCATION_REVIEW_2026-10-10.md`

لا توجد إصلاحات مقترحة أو تغييرات مطلوبة ضمن نطاق مراجعة الموقع.
