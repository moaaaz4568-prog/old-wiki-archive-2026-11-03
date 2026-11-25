# مراجعة `wiki_workflow.py` واختباراته — v1

**التاريخ:** 2026-10-11  
**النطاق المراجع فقط:**

- `/sdcard/NEXUS_LLM_WIKI/tools/wiki_workflow.py`
- `/sdcard/NEXUS_LLM_WIKI/tools/tests/test_wiki_workflow.py`
- عقود الأنظمة `13` إلى `19`

لم أعدّل الأداة أو الاختبار أو أي ملف آخر. الملف الوحيد المكتوب في هذه المهمة هو
هذا التقرير. لم أشغّل `publish --apply` على corpus الحقيقي، ولم أشغّل استخراجًا أو
أغلق أي domain.

## الحكم التنفيذي

**الحكم: BLOCKED قبل تشغيل المصادر بثقة تشغيلية.**

الأداة جيدة كحاجز محلي لسلامة المسار والبايتات والنسخة المستقلة، والاختبارات
الخضراء تثبت مجموعة معتبرة من حالات الرفض والإعادة. لكنها لا تثبت حاليًا أن
الـsnapshot شامل فعلًا، ولا أن route مدعوم بدليل تصنيفي مرتبط به، ولا أن duplicate
يُحفظ كمرجع تابع بدل نسخه كمصدر ثانٍ. كما أن ملفات `ROUTE` و`INDEX` التي تنشئها
لا تستوفي الحد الأدنى الوصفي في النظامين 14 و17، وهناك اختلاف واجهة في تمثيل
حالة المجال بين الأداة وعقد النظام 16. لذلك لا ينبغي تمرير batch مصادر حقيقي أو
طلب T/M اعتمادًا على `ok=true` وحده.

لا يوجد في النتائج أي إعلان `source_done` أو `domain_done` أو PASS لمجال.

## ما تم التحقق منه

### أوامر الاختبار والفحص

| الأمر / الفحص | النتيجة الفعلية |
|---|---|
| `python3 -B -m unittest discover -s tools/tests -p 'test_*.py' -v` | **exit 0، 33/33 PASS، 44.689s**؛ شُغّل على نسخة مطابقة معزولة تحت `/tmp/omnirush/wiki-workflow-review` حتى لا ينشئ الاختبار ملفات داخل الويكي الحقيقي. |
| `python3 -B -m unittest -v tools/tests/test_wiki_workflow.py` | **exit 0، 33/33 PASS، 20.720s** على النسخة المعزولة نفسها. |
| تحليل AST للملفين | `AST_PARSE_OK` للملف المصدر والاختبار. |
| `lsp_diagnostics` على `wiki_workflow.py` | `No diagnostics found. All clean!` |
| `lsp_diagnostics` على `test_wiki_workflow.py` | `No diagnostics found. All clean!` |
| `python3 -B .../wiki_workflow.py --vault ... status` | **exit 0**، `ok=true`، `writes_performed=0`، `sales=in_progress`، وبقية المجالات `pending`. |
| `python3 -B .../wiki_workflow.py --vault ... inventory` | **exit 0**، `ok=true`، **1778** عنصرًا، `errors=[]`، `writes_performed=0`. |
| فحص `code_quality_checker.py` الاستشاري | 1593 سطرًا، 50 دالة، متوسط complexity مقداره 10.7، ودرجات الحجم/التعقيد منخفضة؛ النتيجة الخام `quality_score=0/F` متأثرة ببعض heuristics غير الدقيقة، لكنها تؤكد أن `validate_batch` (262 سطرًا) و`_apply_plans` (130 سطرًا) و`_verify_existing_group` (141 سطرًا) كبيرة وصعبة المراجعة. |

الاختبار المعزول ليس تخفيفًا للنتيجة: نُسخت الملفات المستهدفة كما هي، وشُغّل
الاختبار نفسه مع Python 3.13. سبب العزل أن `setUp` في الاختبار ينشئ
`tools/staging/workflow-tests/runtime-*` في كل حالة ولا يزيله
(`test_wiki_workflow.py:24-30`).

### الأخطاء الفعلية أثناء التحقق

- الأمر الأول `python3 -B -m unittest discover -s tools/tests -p
  'test_wiki_workflow.py' -v` فشل قبل اكتشاف الاختبارات لأن Python اعتبر مجلد
  البداية غير قابل للاستيراد:
  `ImportError: Start directory is not importable: 'tools/tests'`.
  أُعيد التشغيل بالطريقة الصريحة `python3 -B -m unittest -v
  tools/tests/test_wiki_workflow.py`، فنجح 33/33. هذا خطأ harness/طريقة اكتشاف
  وليس فشلًا في حالة اختبار.
- probe مدخل manifest غير صالح في `all_subdomain_ids` (عنصر list غير قابل
  للـhash) لم يرجع JSON خطأ؛ رفع traceback فعليًا:
  `TypeError: unhashable type: 'list'`. هذا مسجل أيضًا كـF-08 أدناه.
- لم تظهر أخطاء فعلية من `status` أو `inventory` الحقيقيين؛ كلاهما exit 0 و`errors=[]`.

### ما يمر فعليًا

الاختبارات والفحص اليدوي يثبتان، ضمن fixtures فقط، ما يلي:

- dry-run للأوامر ومسار عدم الكتابة (`writes_performed=0`).
- قراءة المصدر، SHA-256، الحجم، المسار النسبي، ورفض traversal وsymlink.
- Unicode code-point مع half-open ranges، وفجوات/تداخل التغطية، وmetadata قراءة
  المقطع والأوقات المرتبة.
- exact evidence quote مع offset وhash، بما في ذلك أسماء ledger البديلة.
- قفل extraction للمجال `pending` ومنع طلب T/M من batch جزئية.
- اشتراط reviewer مستقل معلنًا وبصمة manifest مطابقة.
- preflight، عدم overwrite، فحص النسخة byte-exact، idempotent rerun، واكتشاف
  tampering وhardlink/symlink عبر الاختبارات الحقيقية أو guards الممثلة.
- الإبلاغ عن `partial_write` عند فشل الكتابة دون rollback حذف صامت.

هذه نقاط قوة مهمة، لكنها كلها لا تعادل R الشاملة أو T/C/K/M/QA أو اكتمال المجال.

## النتائج المانعة أو عالية الأولوية

### F-01 — P0: يمكن تمرير T على snapshot ناقصة

**الموضع:** `wiki_workflow.py:699-727` و`998-1007`.

`_full_domain_snapshot` يساوي set معرّفات `candidate_manifest` مع
`all_candidate_source_ids`، لكنه لا يثبت أن كل candidate له entry قابل للقراءة
والتوجيه والتغطية، ولا يفحص disposition/reason/evidence، ولا يساوي مجموعة
المعرّفات مع entries التي ستراجع فعليًا. لذلك يكفي إدراج مصدر مفقود في metadata
حتى تعتبر الدفعة snapshot كاملة.

**إعادة الإنتاج التي شُغّلت على جذر مؤقت:** manifest فيه entry واحد `SRC_A`،
بينما `all_candidate_source_ids` و`candidate_manifest` يحتويان `SRC_A` و
`SRC_MISSING`، وكل شروط snapshot الأخرى مستوفاة وطلب `T`. النتيجة الفعلية:

```json
{
  "ok": true,
  "errors": [],
  "summary": {
    "entries": 1,
    "valid_entries": 1,
    "unique_source_ids": 1,
    "full_domain_snapshot": true,
    "t_requested": true,
    "knowledge_requested": true
  }
}
```

هذا يخالف النظام 15:21-29 و63-66 و72-77، والنظام 13:33-39، لأن المقام الشامل
لا يجوز أن يكون قائمة وصفية غير مربوطة بالمصادر والوحدات الفعلية.

**المطلوب قبل المصادر:** مطابقة كاملة بين candidate manifest وentries/source
records، والتحقق من هوية ومسار وحجم وبصمة ومصير ودليل كل candidate، ورفض أي
candidate بلا disposition مراجع أو بلا coverage قابلة للإحالة. يلزم regression
يثبت أن missing candidate لا يمر T أو Master.

### F-02 — P0: منطق duplicate يقبل declarations زائفة وينسخ التكرار

**الموضع:** `wiki_workflow.py:962-972`، ثم `1368-1433`.

الفحص الحالي يعتبر كل source ID له أي قيمة truthy في `duplicate_of` «معلنًا»،
ويشترط بصورة خاطئة أن تكون **كل** هويات البايت المتطابق معلنة كتكرار. النتيجة
المقاسة:

1. مصدر أساسي `SRC_A` بلا `duplicate_of` ومصدر تابع `SRC_B` مع
   `duplicate_of: SRC_A` رُفض بـ `DUPLICATE_HASH_REQUIRES_DECLARATION`؛ وهذا
   يرفض الشكل الصحيح.
2. `SRC_A` مع `duplicate_of: not-a-primary` و`SRC_B` مع
   `duplicate_of: also-not-primary` مرّا بـ `ok=true`، وأنتجا خطة من نسختين.

عند التطبيق، `_apply_plans` ينشئ artifact لكل entry، ويكتب
`"duplicate_of": null` في REF (`wiki_workflow.py:1425-1429`). أي أن declaration
المقبولة تضيع، والتكرار يتحول إلى نسخة مستقلة ظاهريًا. هذا يخالف النظام
14:24-27 و273-295 و529-538، والنظام 19:59-70.

**المطلوب قبل المصادر:** اختيار primary حتمي، التحقق من أن `duplicate_of` يشير
إلى primary موجود وبصمة مطابقة، إبقاء النسخة التابعة كمرجع duplicate لا كنسخة
معرفية/دليل مستقل، حفظ declaration في metadata، وإضافة اختبارات primary/duplicate
الصحيحة والخاطئة والتكرار عبر دفعات أو `done` قائم.

### F-03 — P0: route لا يثبت أن دليل التصنيف مرتبط بالمتن

**الموضع:** `_route_value` في `wiki_workflow.py:617-643`، و`_validate_evidence`
في `539-614`.

الأداة تتحقق من وجود `domain` و`subdomain` في catalog، وتتحقق من quote حرفي عام،
لكنها لا تتحقق من `rationale` أو `confidence` أو `evidence_locators` أو
`body_locator` داخل `primary_route`، ولا تربط quote المدقق بسبب التصنيف. وبذلك
يمكن للـmanifest أن يرسل المصدر إلى domain صالح مع اقتباس صحيح لكنه غير متعلق
بغرض route؛ الأداة لا تصنف من المتن ولا ترفض هذا التناقض.

كذلك لا تقرأ أو تحفظ `secondary_references`: الناتج في
`_apply_plans` يضعها دائمًا `[]` (`wiki_workflow.py:1418`)، وملف ROUTE لا يعرضها.
هذا يخالف النظام 14:20-29 و297-367 و369-389 و640-647، والنظام 18:55-63؛ كما
يخالف قاعدة المصدر متعدد الموضوعات في النظام 13:41-45.

**المطلوب قبل المصادر:** إما تنفيذ verifier صريح لمواضع وأسباب route وربطها
بالنص، أو إعلان واجهة manifest/agent التي تضمن ذلك مع فحص آلي لا يسمح بالمرور
بدونه. يجب حفظ secondary refs ومواضعها بنفس `source_id` دون نسخ ثانية. يلزم
اختبار اسم مضلل/متن واضح، ومصدر متعدد المجالات، وتعادل route ينتج `uncertain`.

### F-04 — P0: artifacts المنشورة لا تستوفي عقد ROUTE وINDEX

**المواضع:** `_route_markdown` في `wiki_workflow.py:1083-1111`،
`_index_markdown` في `1114-1130`، وREF في `1385-1430`.

إعادة نشر fixture ناجحة (`publish_ok=true`) لكن الفحص النصي للملفات كشف:

- `ROUTE_<id>.md` لا يحتوي `bytes_read`/IO audit، أو semantic segment IDs ومراجع
  القراءة، أو `duplicate_state`، أو `secondary_references`، أو `done_artifact`،
  أو جدول G0-G8؛ يحتوي بدلًا من ذلك على قائمة checks مختصرة لا تحمل evidence
  اللازمة لإعادة التحقق.
- `INDEX.md` لا يحتوي رأس catalog/snapshot/state/updated، ولا مدخلات
  `id/kind/path/title/function/scope/coverage_status/upstream_refs/
  downstream_refs/retrieval_questions/limitations/conflict_refs` المطلوبة في
  النظام 17:15-35.
- REF يفتقد مفاتيح العقد الصريحة `content_hash` و`reading_coverage_ref` و
  `concept_refs` و`master_refs`؛ بعض ذلك يمكن تمثيله باسم مكافئ فقط إذا اتُّفق
  على adapter، لكن لا يوجد adapter موثق أو اختبار توافق.

هذا يخالف النظام 14:513-527 و575-648 والنظام 17:8-35 و58-87. وجود النسخة وREF
وROUTE لا يكفي إذا تعذر من artifact نفسه معرفة نطاق القراءة، snapshot، dedup،
الفهرسة، والرجوع إلى الدليل.

**المطلوب قبل المصادر:** تثبيت schema موحد للـROUTE/REF/INDEX، توليد الحقول
الإلزامية من validation لا من نص ثابت، وإضافة snapshot tests أو verifier مستقل
للروابط والحقول وG0-G8. يجب أن تظل الحالات `route_done` و`source_done` و
`domain_done` منفصلة كما تفعل الأداة حاليًا.

### F-05 — P1: واجهة حالة المجال لا تطابق عقد 16، و`status` لا يرفض config ناقصًا

**المواضع:** `_processing_status` و`_current_domain` في
`wiki_workflow.py:228-247`، و`status` في `323-363`.

الأداة تقرأ `current_domain` و`current_domain_status` وقائمة
`domain_states` ذات `domain_id/status`. عقد النظام 16 يعرّف واجهة الحالة
المرجعية باستخدام `active_domain` و`domain_states` كخريطة حالات، مع revision وlock
وfencing token (`16:15-46`). probe بجذر مؤقت مطابق لذلك الشكل أعاد:

```json
{
  "status": {"ok": true, "current_domain": null, "domain_states": [{"domain": "sales", "status": null}]},
  "extraction": {"ok": false, "errors": ["CURRENT_DOMAIN_LOCK"]}
}
```

أي أن حالة active صحيحة حسب العقد تُقرأ كأن لا مجال نشط، بينما `status` نفسه
يعلن `ok=true`. وبالعكس، لا يتحقق `status` من أن order يغطي كل domains في
catalog أو أن top-level status يطابق state الخاص بالمجال. Probe فيه catalog
`sales,outreach` وorder `sales` فقط أعاد أيضًا `ok=true` بلا error، رغم أن النظام
18:83-91 يطلب فحص IDs والترتيب بلا فقد أو تكرار.

**المطلوب قبل المصادر:** اختيار schema واحد أو adapter صريح، فحص revision/lock
والتعارضات، رفض order ناقص أو states مكررة/متعارضة، وعدم السماح بالاستخراج من
حالة لا تطابق الحالة الوحيدة في `processing_order.json`. لا يكفي الاعتماد على
`current_domain` التاريخي دون إثبات توافقه مع عقد 16.

### F-06 — P1: semantic coverage أضعف من سجل القراءة المطلوب

**المواضع:** `_validate_segment_metadata` في `wiki_workflow.py:408-444`، و
`_coverage_ranges` في `447-527`.

التحقق يطلب reader/reviewer/note وأوقاتًا timezone-aware، لكنه لا يطلب هوية
segment (`segment_id`) أو `content_unit_ids` أو `io.bytes_expected/
bytes_read/eof_reached/encoding/decode_replacements` أو خريطة view إلى الأصل.
ولا ينسخ هذه المعلومات إلى ROUTE؛ REF يكتفي بـ
`read_coverage: {"status": "full_unicode_range_checked"}`.

النظام 14:191-243 و234-243 يفرق صراحة بين IO والقراءة الدلالية ويطلب وحدات
محتوى بمصائر ومراجع؛ النظام 13:96-103 يطلب محاسبة كل content unit. تغطية ranges
المتصلة مع note لا تثبت وحدها أن كل وحدة قُرئت واستخرجت أو صُنفت non-knowledge
بسبب مراجع.

**المطلوب قبل المصادر:** تحديد ما إذا كانت هذه الأداة routing-only (وعندها يجب
ألا تسمي metadata الحالية شهادة قراءة) أو توسيع manifest/ROUTE ليحمل سجل القراءة
والوحدات المطلوبة. يلزم اختبار gap في content units وليس ranges فقط.

### F-07 — P1: لا توجد واجهة delta/reprocessing أو عقد orchestration في الأداة

`wiki_workflow.py` لا يقدم delta record أو `stale`/invalidation أو مقارنة cutoff
أو `old_snapshot_id/new_snapshot_id`، ولا يفرض `run_id/role/allowed_write_paths/
expected_state_revision/fencing_token` في عقد تسليم العامل. `inventory` يعيد
جردًا فقط (`254-320`)، و`publish` يكتب artifacts مباشرة.

هذا ليس عيبًا إذا كان المقصود أن تكون الأداة جزءًا محليًا فقط، لكنه **فجوة
تكاملية مانعة لتشغيل المصادر كنظام كامل**: النظام 16:63-79 و81-88 يطلب القفل
والتسليم المتسلسل، والنظام 19:6-18 و47-92 يطلب تسجيل كل وصول جديد وأثره وإبقاء
التغطية stale حتى المراجعة. لا يجوز اعتبار route ناجحًا بديلًا عن delta review
أو reopen transaction.

**المطلوب قبل المصادر:** تحديد المنسق/الأداة المالكة لهذه السجلات، وربط manifest
بـsnapshot/state revision، أو إبقاء التشغيل محصورًا في intake مع تقرير صريح بأن
delta والبوابات الخارجية لم تُنفذ.

## نتائج robustness والاختبار

### F-08 — P2: بعض metadata غير الصالحة تسبب traceback بدل خطأ محكوم

**الموضع:** `wiki_workflow.py:713-717`.

إذا كان `all_subdomain_ids` يحتوي قيمة غير قابلة للـhash مثل list، فإن
`set(all_subdomain_ids)` يرفع `TypeError: unhashable type: 'list'` بدل أن يعيد
JSON فيه `CONFIG/MANIFEST_SHAPE_ERROR`. هذا probe أُعيد على جذر مؤقت. يجب أن
تكون كل مدخلات manifest غير الموثوقة أخطاء قابلة للتقرير، خصوصًا قبل أي apply.

### F-09 — P2: harness الاختبار يكتب fixtures دائمة في شجرة المشروع

**الموضع:** `test_wiki_workflow.py:24-30`.

كل `setUp` ينشئ `staging/workflow-tests/runtime-*` ويتركه. لذلك شغّلت الاختبارات
في نسخة `/tmp` فقط. هذا لا يغير raw، لكنه يخالف عمليًا توقع «اختبار قراءة أولًا بلا
آثار» ويمكن أن يلوث `staging` بسجلات قد يخلطها تشغيل لاحق مع manifests أو evidence
حقيقية. يجب أن يحدد المشروع بوضوح إن كانت fixtures المحفوظة جزءًا من العقد، أو
ينقلها runner إلى مساحة مؤقتة خارج vault مع اختبار عدم التلوث.

### F-10 — قابلية الصيانة: مسارات التحقق والكتابة كبيرة جدًا

فحص الجودة الاستشاري سجل `validate_batch` بطول 262 سطرًا وcomplexity تقديرية 98،
و`_verify_existing_group` و`_apply_plans` بمسارات متعددة للقراءة والتحقق والكتابة.
هذه ليست وحدها سبب رفض تشغيلي، لكنها تزيد احتمال أن تفلت حقول عقد جديدة كما
حدث في F-01 إلى F-06. يلزم تفكيكها إلى validators مستقلة (schema/config,
candidate coverage, route evidence, duplicate, artifact contract) مع اختبارات
لكل validator، لا إصلاح شكلي فقط.

## فجوات الاختبارات الحالية

رغم نجاح 33 اختبارًا، لا يغطي الاختبار الحالي:

1. المسار الإيجابي لـfull `domain_snapshot` مع كل candidates، ولا رفض candidate
   مفقود أو disposition ناقص.
2. duplicate صحيح (primary بلا declaration وduplicate يشير إليه) وduplicate
   زائف أو duplicate عبر دفعة/`done` سابقة، وعدم إنشاء نسخة ثانية.
3. ربط route evidence locators/rationale بالمتن، وsecondary references وuncertain
   عند التعادل.
4. schema ومحتوى ROUTE/REF/INDEX، وG0-G8، وlinks/anchors وretrieval metadata.
5. `active_domain`/revision/lock/fencing وorder الناقص أو states المتعارضة.
6. delta بعد T وقبل Master، ووصول مجال pending أثناء عمل مجال آخر، وحالة stale.
7. مدخلات manifest ذات أنواع غير صحيحة التي يجب أن تعيد JSON error لا traceback.
8. عدم تلويث الويكي عند تشغيل الاختبار من مساره الحقيقي.

## ما لم يُختبر، ولا ينبغي اعتباره PASS

- لم يُشغّل `publish --apply` على `/sdcard/NEXUS_LLM_WIKI` الحقيقي؛ أي تطبيق
  حقيقي كان سيكتب `done/` ولذلك هو خارج تكليف المراجعة.
- لم تُقرأ المصادر دلاليًا ولم تُراجع content units أو Terms/Claims/Concepts.
- لم تُنفذ بوابات R/T/C/K/M/QA أو delta/reprocessing أو lock/CAS متعدد الكتّاب.
- لم تُثبت هوية reviewer خارج الحقول المعلنة في JSON؛ المقارنة النصية لا تعادل
  مصادقة هوية مستقلة.
- خضرة `status` و`inventory` تعني سلامة قراءة config والجرد في لحظة الفحص فقط؛
  لا تعني صحة كل corpus أو اكتمال أي domain.

## قرار التسليم

**لا أوصي بتشغيل مصادر حقيقية أو طلب T/M قبل معالجة F-01 إلى F-06 على الأقل،
وتحديد مالك F-07.** الاختبارات الحالية تصلح baseline محليًا، وليست بوابة قبول
للمصادر. التقرير يسلّم هذه findings إلى Commander دون تعديل الأداة أو الاختبار
أو الحالة التشغيلية.
