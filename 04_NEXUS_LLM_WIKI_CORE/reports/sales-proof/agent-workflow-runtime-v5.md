# تقرير تشغيل أداة workflow — v5

## الحكم الحالي

- **قرار التشغيل:** ما زال `RETURN: insufficient evidence`.
- **نطاق هذا الإصلاح:** الفجوة المثبتة في `workflow-review-v2.md` فقط: جعل دليل
  symlink/hardlink capability-aware، مع fallback دائم يرفض metadata الخطرة دون
  الاعتماد على قدرة الـfilesystem على إنشاء الرابط.
- **ما لم يحدث:** لا `publish --apply` على corpus الحقيقي، ولا قراءة دلالية
  للمصادر، ولا إغلاق domain أو بوابة `T` أو بدء `Master`.

## التغييرات

1. `tools/tests/test_wiki_workflow.py`
   - أصبح اختبار metadata اسمه
     `test_link_metadata_guards_reject_without_link_creation`، ووثيقته توضّح أنه
     fallback مستقل عن إنشاء الروابط.
   - اختبارات إنشاء symlink وhardlink الفعلية أصبحت capability-aware: إذا سمح
     الـfilesystem بإنشاء الرابط، تستمر وتتحقق من الرفض الفعلي؛ وإذا منعه، تسجل
     `SKIP` صريحًا يتضمن نوع خطأ النظام واسم اختبار الـfallback.
   - fallback يحقن metadata مكافئة عبر `_lstat`، ويختبر source وmanifest وreviewer
     وdestination component وartifacts، مع مقارنة snapshot قبل/بعد لإثبات عدم
     الكتابة.
2. `tools/WORKFLOW_USAGE.md`
   - أضيف شرح صريح لمعنى capability-aware و`SKIP`: الـ`SKIP` قيد بيئي وليس PASS
     لمنصة الروابط، والـfallback لا ينشئ روابط.

لم يتغير `tools/wiki_workflow.py` في هذه الدفعة؛ لم تُعدّل `raw/` أو `config/` أو
`claims/` أو `concepts/` أو `masters/`، ولم يُحذف أي ملف.

## سجل PASS / FAIL / SKIP الفعلي

### الاختبارات

الأمر المنفذ من `/sdcard/NEXUS_LLM_WIKI`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tools/tests -p 'test_*.py' -v
```

النتيجة الفعلية:

| الفئة | العدد | الدليل |
|---|---:|---|
| PASS | 31 | كل الاختبارات التي نفذت assertions اكتملت بنجاح، ومنها `test_link_metadata_guards_reject_without_link_creation` |
| FAIL | 0 | لا يوجد فشل |
| SKIP | 2 | اختبار symlink الفعلي واختبار hardlink الفعلي |
| الإجمالي | 33 | `OK (skipped=2)`، exit code `0`، الزمن `37.788s` |

سببَا الـ`SKIP` كما طبعهما unittest:

- symlink: `PermissionError: [Errno 13] Permission denied` عند إنشاء
  `new/link.txt`؛ الاختبار سجّل صراحة أن
  `test_link_metadata_guards_reject_without_link_creation` هو fallback.
- hardlink: `PermissionError: [Errno 1] Operation not permitted` عند إنشاء
  `copy-alias.txt`؛ الاختبار سجّل صراحة أن نفس الاختبار هو fallback.

إذن لا تُعرض اختبارات الرابطين الفعليين كـPASS في هذه البيئة. في المقابل، اختبار
الـfallback نفسه **PASS** ويثبت الرفض من metadata الاصطناعية مع ثبات snapshot
الشجرة وعدم الكتابة. إذا نُقل الاختبار إلى filesystem يسمح بالروابط، فلن يتخطى
الاختباران وسيُتحقق من الكائن الفعلي بدل الاكتفاء بالـmetadata.

### أوامر القراءة فقط

1. `status`

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/wiki_workflow.py \
  --vault /sdcard/NEXUS_LLM_WIKI status --json
```

الملخص الفعلي: **PASS**، `ok=true`، `read_only=true`،
`writes_performed=0`، `current_domain=sales`،
`current_domain_status=in_progress`، و`errors=[]`. ترتيب المجالات المقروء:
`sales`, `outreach`, `pricing_offers`, `content_strategy`.

2. `inventory`

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/wiki_workflow.py \
  --vault /sdcard/NEXUS_LLM_WIKI inventory --json
```

الملخص الفعلي: **PASS**، `ok=true`، `read_only=true`،
`writes_performed=0`، `item_count=1778`، `error_count=0`، والجذور المقروءة
`new/` و`raw/new/`.

### LSP

`lsp_diagnostics` أعاد `No diagnostics found. All clean!` لكل من:

- `tools/wiki_workflow.py` — **PASS**
- `tools/tests/test_wiki_workflow.py` — **PASS**
- `tools/WORKFLOW_USAGE.md` — **PASS**

## ما بقي مانعًا لدفعة source حقيقية

1. الـfilesystem الحالي لا يسمح بإنشاء symlink أو hardlink؛ لذلك يبقى الدليل
   **SKIP** للتكامل الفعلي. الـfallback يثبت أن الحواجز ترفض metadata الخطرة،
   لكنه لا يحول القيد البيئي إلى PASS لمنصة الروابط. يلزم تشغيل الاختبارين
   الفعليين على filesystem يسمح بالروابط للحصول على الدليل المتبقي.
2. لم تُفحص دفعة manifest حقيقية ولم يُنفذ `publish --apply` على corpus الحقيقي؛
   `status` و`inventory` يثبتان قراءة config والجرد في لحظة الفحص فقط، لا صحة
   محتوى corpus ولا اكتمال domain.
3. لم تتم أي semantic reading للمصادر، ولا يمكن استنتاج source/domain completion
   أو `T`/`Master` من hash أو من خضرة الاختبارات.

بناءً عليه، هذه الدفعة تحسن قابلية الإثبات وتمنع إخفاء قيد البيئة، لكنها لا تغيّر
قرار `RETURN` ولا تسمح ببدء source batch حقيقية.
