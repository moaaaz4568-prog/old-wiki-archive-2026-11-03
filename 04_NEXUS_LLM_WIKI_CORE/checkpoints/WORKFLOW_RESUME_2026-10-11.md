# Checkpoint — workflow runtime v3 — 2026-10-11

## الحالة

- **الحالة:** `in_progress`.
- **النطاق:** تشغيل فعلي محدود لأداة `tools/wiki_workflow.py` وأدلتها؛ لا corpus publish ولا تعديل raw/config/أنظمة/معرفة.
- **آخر خطوة مكتملة:** قراءة العقود والملفات المستهدفة وتشغيل خط أساس الاختبارات.
- **آخر أمر موثق:** `python3 -B -m unittest tools.tests.test_wiki_workflow -v` — **PASS، 9/9**.

## ما قرئ

`AGENTS.md`، `PROJECT_OUTPUT_LOCATION_2026-10-10.md`، `SCHEMA.md`، الأنظمة 13–19، `config/domain_catalog.json`، `config/processing_order.json`، مرجع `MULTIDOMAIN_ALIGNMENT_2026-10-10.md`، ملحق `USER_MESSAGES_SESSION_EF22.md`، والأداة/الاختبارات/دليل الاستخدام كاملة.

## الخطوة التالية عند الاستئناف

فحص فجوات runtime المثبتة، ثم تعديل الأداة والاختبارات والـusage فقط؛ fixtures في
`staging/workflow-tests/`، والتحقق بـ`python3 -B`، ثم تشغيل `status` و`inventory` الحقيقيين
والـLSP. لا تعِد التشغيل على corpus الحقيقي ولا ترفع أي بوابة T/M أو حالة source/domain.

## قيود الاستئناف

- لا semantic read من hash؛ لا يثبت hash إلا هوية البايتات.
- `pending` يمكن توجيهه فقط؛ extraction له مرفوض.
- الدفعة ليست شهادة domain ولا تمرر T/M؛ `source_done` غير مستنتج من route.
- أي IO failure وسط الكتابة يُعاد كتقرير `partial_write` قابل للمراجعة، بلا rollback حذف.

## استئناف Worker الحالي — 2026-10-11

- الهدف: إصلاح runtime محدود دون corpus publish، مع تقرير واحد وcheckpoint واحد داخل الجذر فقط.
- الحالة: `in_progress`؛ آخر دليل حالي 9/9 baseline، وstatus/inventory exit 0، وLSP clean. التفاصيل والقيود في `reports/sales-proof/agent-workflow-runtime-v3.md#استئناف-worker--2026-10-11`.
- اكتُشف أن harness القديم يحذف fixtures تلقائيًا وأن baseline شُغّل دون `-B`؛ يُمنع تكراره. التالي تحويل fixtures إلى `mkdtemp` محفوظ داخل `staging/workflow-tests/`، ثم regressions لمراجعة Unicode/evidence/independence/idempotence قبل الإصلاح.
- النقص الجوهري المحتمل في بوابات المعرفة أو concurrency يبقى blocked؛ لا بناء نظام كبير ولا إعلان قراءة دلالية أو domain completion.

## نتيجة Worker — 2026-10-11

- الحالة: `verified_locally; commander_review_pending`، بلا رفع TODO أو domain state.
- الملفات المعدلة في النطاق: `tools/wiki_workflow.py`، `tools/tests/test_wiki_workflow.py`، `tools/WORKFLOW_USAGE.md`، وهذا التقرير، وهذا checkpoint فقط.
- الدليل النهائي: unittest **33/33 PASS، 2 skipped**؛ `py_compile` exit 0؛ LSP clean للأداة والاختبارات والدليل؛ status/inventory الحقيقيان exit 0 و`writes_performed=0`، inventory `1778` عنصرًا و`errors=0`.
- الإصلاح يثبت dry-run بلا كتابة، path/hash، Unicode coverage، review metadata، exact evidence، pending extraction، منع T/M للدفعة الجزئية، reviewer مستقل، preflight، منع overwrite/link/traversal، partial-write reporting، وidempotent rerun على fixtures فقط.
- القيود: لم يُشغّل publish على corpus الحقيقي؛ لا semantic source read ولا domain completion. symlink/hardlink الحقيقيان skipped بسبب mount، واختبارات guards mocked. لا Git ولا commit، ولا تعديل raw/config/claims/concepts/masters، ولا حذف.
