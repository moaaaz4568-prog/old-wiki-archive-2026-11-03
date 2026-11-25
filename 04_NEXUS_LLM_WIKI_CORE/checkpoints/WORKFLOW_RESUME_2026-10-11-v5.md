# Checkpoint — workflow runtime v5 — 2026-10-11

## الحالة

- **الحالة:** `in_progress; commander_review_pending`.
- **الهدف:** معالجة فجوة التقرير `workflow-review-v2.md` الخاصة باختبارات
  symlink/hardlink دون تشغيل publish على corpus الحقيقي.
- **القرار المحفوظ:** `RETURN: insufficient evidence`؛ لم يتغير.

## ما تم

- عُدّل `tools/tests/test_wiki_workflow.py` فقط لإضافة fallback واضح لا يحتاج
  إنشاء روابط، ولجعل اختبارات إنشاء الروابط الفعلية capability-aware مع أسباب
  `SKIP` صريحة.
- عُدّل `tools/WORKFLOW_USAGE.md` فقط لتوثيق معنى الـfallback والفرق بين `SKIP`
  وقبول منصة الروابط.
- لم يتغير `tools/wiki_workflow.py`، ولم تُمس `raw/` أو `config/` أو `claims/`
  أو `concepts/` أو `masters/`، ولم يحدث حذف.

## آخر تحقق موثق

الأمر:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tools/tests -p 'test_*.py' -v
```

النتيجة: **PASS 31، FAIL 0، SKIP 2، الإجمالي 33**، `OK (skipped=2)`، exit
code `0`، في `37.788s`.

- اختبار fallback `test_link_metadata_guards_reject_without_link_creation`:
  **PASS**، وsnapshot الشجرة ثابت أثناء حالات metadata المحقونة.
- symlink الفعلي: **SKIP** بسبب `PermissionError [Errno 13] Permission denied`.
- hardlink الفعلي: **SKIP** بسبب `PermissionError [Errno 1] Operation not permitted`.

أوامر القراءة فقط:

- `status --json`: **PASS**، `ok=true`، `read_only=true`،
  `writes_performed=0`، `sales/in_progress`، `errors=[]`.
- `inventory --json`: **PASS**، `ok=true`، `read_only=true`،
  `writes_performed=0`، `1778` عنصرًا، `0` أخطاء.

LSP: **PASS** و`No diagnostics found. All clean!` للأداة والاختبارات ودليل
الاستخدام.

## القيود والخطوة التالية

- الـSKIP الفعلي للروابط ما زال قيدًا بيئيًا؛ لا يُعاد تصنيفه PASS. يلزم بيئة
  filesystem تسمح بإنشاء symlink/hardlink لإغلاق هذا الدليل التكاملّي.
- لم يُشغّل `publish --apply` على `/sdcard/NEXUS_LLM_WIKI` الحقيقي، ولم تُقرأ
  المصادر دلاليًا، ولم يُثبت اكتمال domain أو `T` أو `Master`.
- الخطوة التالية للمراجعة: Commander يقرر ما إذا كان دليل الـfallback كافيًا
  لإغلاق فجوة تقرير v2، أو يطلب تشغيلًا على filesystem داعم قبل أي source batch.
