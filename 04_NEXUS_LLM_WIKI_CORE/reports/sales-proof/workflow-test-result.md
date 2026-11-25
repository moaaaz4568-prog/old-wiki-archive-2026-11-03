# نتيجة اختبار `wiki_workflow.py`

## أمر الاختبار

شُغّل من جذر الويكي `/sdcard/NEXUS_LLM_WIKI`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tools/tests -p 'test_*.py' -v
```

- **Exit code:** `0`
- **النتيجة الإجمالية:** `OK`
- **الزمن:** `40.904s`
- **العدد:** `33` اختبارًا؛ `31` نجح، `0` فشل، و`2` تخطّيا (skipped).

## ما نجح

نجحت فحوص القراءة فقط وعدم الكتابة، وdry-run وCLI، والتحقق من المراجع المستقل
وإنشاء artifacts الخاصة بالـroute، وتصادمات الهوية والبصمات، وتغطية Unicode
والـsemantic-review metadata والفجوات/التداخل، والتحقق من exact evidence
والأسماء البديلة لحقول ledger، وقفل extraction للمجال pending، ورفض بوابتي
`T` و`Master` من الدفعات الجزئية، وفحوص المسارات والبصمات والـprimary routes،
والـpreflight قبل الكتابة، والكتابة الجزئية، وإعادة النشر idempotent، ورفض
التلاعب بالـmanifest أو artifacts، ورفض self-review والتقارير الناقصة أو
القديمة.

## ما فشل أو تخطّى

- لا توجد اختبارات فاشلة.
- `test_rerun_rejects_hardlinked_artifacts` تخطّى لأن نظام الملفات رفض إنشاء
  hard link (`Operation not permitted`).
- `test_source_manifest_and_destination_symlinks_are_rejected` تخطّى لأن نظام
  الملفات رفض إنشاء symlink (`Permission denied`).

## أكبر فجوتين

1. حواجز symlink وhardlink لم تُختبر فعليًا في هذه البيئة؛ نجاح المجموعة لا
   يثبت سلوك هذين المسارين إلا على نظام ملفات يسمح بإنشاء الروابط.
2. الاختبارات تستخدم جذورًا وبيانات اصطناعية مؤقتة ولا تفحص corpus الحقيقي أو
   تكامل manifest حقيقي؛ لذلك لا تثبت اكتمال أي domain ولا إغلاق بوابة `T` أو
   بدء `Master` في بيانات الإنتاج، كما يحذّر دليل الاستخدام صراحةً.

ملاحظة تشغيلية: الاختبار أنشأ fixtures الاختبار الخاصة به تحت
`tools/staging/workflow-tests` وفقًا لـ`setUp` في ملف الاختبارات؛ لم يُعدّل
الكود أو ملفات المصدر الثلاثة المقروءة.
