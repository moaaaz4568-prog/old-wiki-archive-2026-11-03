# تقرير تشغيل أداة workflow — v3

## حالة العمل

- **الحالة:** قيد التنفيذ؛ لا يُعد هذا الملف شهادة نجاح أو اكتمال مجال.
- **النطاق المأذون:** `tools/wiki_workflow.py`، اختبارات الأداة، `tools/WORKFLOW_USAGE.md`، فهارس الأدوات الضرورية، fixtures تحت `staging/workflow-tests/`، وهذا التقرير وcheckpoint المرتبط به.
- **الممنوع:** لا تعديل `raw/` أو `config/` أو الأنظمة أو المعرفة أو التقارير القديمة، لا حذف، لا Codex ولا subagents، ولا publish على corpus الحقيقي.
- **الهدف:** جعل `inventory` و`status` و`validate-batch` و`publish` تعمل بعقد dry-run افتراضي، مع منع ترقيات المعرفة، والتحقق من النسخ المستقلة والهوية والتغطية والأدلة والمراجعة المستقلة.

## ما تم قبل التعديل

- قُرئت الأداة كاملة، والاختبارات كاملة، و`tools/WORKFLOW_USAGE.md`، و`AGENTS.md`، و`PROJECT_OUTPUT_LOCATION_2026-10-10.md`، و`SCHEMA.md`، والأنظمة 13–19، وملفا config، ومرجع المواءمة وملحق EF22.
- خط الأساس: `python3 -B -m unittest tools.tests.test_wiki_workflow -v` نجح بـ9 اختبارات.
- لم يظهر مستودع Git عند فحص `/sdcard/NEXUS_LLM_WIKI`؛ لن تُبنى نتيجة على commit غير موجود.
- الاختبارات الحالية لا تغطي بعد idempotence، فشل preflight للدفعة كاملة، symlink/hardlink، forged/stale reviewer report، وتفاصيل evidence field names المطلوبة.

## الخطة التالية

1. مراجعة/إصلاح الفجوات المثبتة فقط في الأداة، مع إبقاء dry-run بلا كتابة.
2. توسيع regression tests إلى fixtures معزولة تحت `staging/workflow-tests/`، وبـ`python3 -B`.
3. تصحيح usage إلى batch قابل للنسخ والتشغيل، وتوحيد evidence مع `evidence_start`/`evidence_end`/`quote`/`excerpt_sha256`.
4. تشغيل الاختبارات، `status`، و`inventory` قراءة فعلية، ثم LSP، وتسجيل الأوامر والنتائج هنا وفي checkpoint.

## حدود معلقة

- اختلافات عقد config لا تُرقّى ولا تُعدّل؛ إذا ظهرت تُسجّل كـfinding.
- لا يُستدل من hash أو EOF على قراءة دلالية؛ الأداة تتحقق فقط من أدلة القراءة التي يقدمها agent.

## استئناف Worker — 2026-10-11

- التعليمات الحالية تضيق العمل إلى إصلاحات مثبتة بالأداة والاختبارات ودليلها، وهذا التقرير و`checkpoints/WORKFLOW_RESUME_2026-10-11.md` فقط. لا تحديث لقائمة مهام القائد ولا حالة domain.
- أُعيدت قراءة الأداة (1299 سطرًا)، الاختبارات (242)، الدليل (165)، AGENTS وSCHEMA وسياسة المخرجات والأنظمة 13–19 كاملة؛ وقُرئ الميثاق وملفا config ومنتج `build_sales_full_evidence_ledger.py` دون تشغيله. سجلات الجلسة السابقة أعلاه تبقى تاريخية ولا تنسب قراءاتها إلى هذا الاستئناف.
- لا يوجد `.opencode/` داخل الويكي. سياق المضيف السابق غير متعلق بهذا الإصلاح ولم يُعدّل.
- خط الأساس المنفذ في هذا الاستئناف: `python3 -m unittest discover -s tools/tests -p 'test_*.py' -v` → exit 0، **9/9** في 3.113s. **مخالفة رُصدت في harness القديم:** `TemporaryDirectory.cleanup()` حذف fixtures الاختبار تلقائيًا؛ الأمر بلا `-B` سمح بملفات `__pycache__` داخل tools. لن يتكرر: سيُستخدم `mkdtemp` بلا cleanup، وتبقى fixtures داخل staging، وكل أمر لاحق بـ`-B`. لا حذف لأي corpus.
- `python3 tools/wiki_workflow.py --vault /sdcard/NEXUS_LLM_WIKI status --json` → exit 0، `ok=true`, `writes_performed=0`، sales in_progress والباقي pending. `inventory --json` بنفس البادئة → exit 0 و`ok=true`, `writes_performed=0`. هذه مخرجات الأداة، لا مقارنة قبل/بعد بعدُ. إخراج inventory الطويل حُفظ تلقائيًا بواسطة المضيف خارج جذر المشروع؛ ليس ملفًا طلبت الأداة كتابته، ولن يُستخدم مسار ذلك الأرشيف مرجع تشغيل. ستُلتقط نتائج CLI لاحقًا في الذاكرة ويُطبع ملخص قصير فقط.
- LSP للأداة والاختبارات أعاد `No diagnostics found. All clean!`؛ ليس دليلًا على تشغيل Python type checker. `git_status` للجذر فشل: ليس Git repository.
- فجوات مثبتة بالقراءة: مراجعة المقاطع وهوياتها/أوقاتها غير مفحوصة، غياب semantic_review_status يمر، وحدات evidence/coverage غير مفحوصة، quote الفارغ يمر، أسماء evidence_start/evidence_end لدى المنتج غير مدعومة، independent=true بلا مقارنة المؤلف، وكل وجهة قائمة تُرفض حتى عند الإعادة المطابقة. ستثبت باختبارات RED قبل إصلاحها.
- حدود لن تُبنى هنا: حصر snapshot/استخراج/بوابات معرفية كاملة، محرك تصنيف دلالي، مصادقة حقيقية لهوية reviewer، أو نظام معاملات/قفل متعدد الكتّاب. أي نقص مؤثر يبقى blocked لا PASS عام.
- الخطوة التالية: حفظ fixtures بلا حذف، إضافة regressions وتشغيلها، ثم أصغر إصلاح ممكن وإعادة التحقق.

## التنفيذ والتحقق — Worker — 2026-10-11

### ما تغيّر

- `tools/wiki_workflow.py`: رفض المسارات ذات التطبيع الخفي (`./`/الفواصل المكررة)، تحقق صريح من Unicode code-point/half-open coverage، segments متصلة بلا gap/overlap مع `reader/read_at/reviewer/reviewed_at/note` وأوقات timezone-aware، وحالة semantic review مطلوبة. أضيفت aliases سجل الأدلة `evidence_start/evidence_end/evidence_quote/excerpt_sha256` مع رفض quote الفارغ أو coordinate غير Unicode.
- `tools/wiki_workflow.py`: رصد extraction المتخفي في `coverage.mode`، طلبات T/M على مستوى entry، ومنع source identity من امتلاك primary routes متعارضة. `--apply` يتطلب author معلنًا ومراجعًا مستقلًا بوقت مراجعة وبصمة manifest مطابقة؛ المقارنة تستعمل identity منزوعة المسافات.
- `tools/wiki_workflow.py`: preflight يغطي الوجهات القائمة، يرفض artifact/symlink/hardlink أو metadata tampered، ويعيد تشغيل publish idempotently فقط عند تطابق copy وREF/ROUTE/INDEX؛ لا overwrite، والإعادة تعيد `already_published=true` و`writes_performed=0`. فشل الكتابة المرئي يُسجل ضمن `partial_write` بلا rollback أو حذف.
- `tools/tests/test_wiki_workflow.py`: استبدال `TemporaryDirectory.cleanup()` بـ`mkdtemp` محفوظ تحت `staging/workflow-tests/`، وإضافة regressions للـdry-run tree invariance، path/hash، Unicode، review metadata، evidence aliases، pending extraction، entry T/M، reviewer independence/staleness، preflight، tampering، mocked link guards، partial write، وidempotence. اختبارات symlink/hardlink الحقيقية تُسجل skipped عندما يمنع filesystem إنشاءها، مع بقاء guards ممثلة بـmock.
- `tools/WORKFLOW_USAGE.md`: تحديث العقد القابل للنسخ لحقول coverage/review/evidence والإعادة idempotent وأمر الاختبار `-B`.

### نتيجة RED ثم GREEN

- بعد إضافة regressions وقبل الإصلاح: **27 فشلًا + خطأ واحد** في 31 اختبارًا، منها review metadata غير المفحوصة، evidence aliases، pending mode، route collision، destination idempotence، وparent preflight. هذا إثبات فشل سلوكي لا syntax/import failure.
- بعد الإصلاح النهائي: `python3 -B -m unittest discover -s tools/tests -p 'test_*.py' -v` → exit 0، **33/33 نجح، 2 skipped** (symlink/hardlink creation ممنوعان على filesystem الحالي)، في 34.591s.
- `python3 -B -m py_compile tools/wiki_workflow.py tools/tests/test_wiki_workflow.py` → exit 0 بلا output.
- `lsp_diagnostics` على `tools/wiki_workflow.py` و`tools/tests/test_wiki_workflow.py` و`tools/WORKFLOW_USAGE.md` → `No diagnostics found. All clean!` لكل ملف.

### أوامر القراءة الفعلية

- `set -o pipefail; python3 -B tools/wiki_workflow.py --vault /sdcard/NEXUS_LLM_WIKI status --json | python3 -c ...` → exit 0، `ok=true`, `writes_performed=0`, `current_domain=sales`, `current_domain_status=in_progress`, outreach/pricing/content pending، `errors=[]`.
- `set -o pipefail; python3 -B tools/wiki_workflow.py --vault /sdcard/NEXUS_LLM_WIKI inventory --json | python3 -c ...` → exit 0، `ok=true`, `item_count=1778`, `error_count=0`, `writes_performed=0`, الجذور `new/` و`raw/new/`.
- اختبارات CLI نفسها قارنت snapshot شجرة fixture قبل/بعد لكل `inventory`, `status`, `validate-batch`, و`publish` dry-run؛ لا اختلاف ولا كتابة.
- لم يُشغّل `publish --apply` على `/sdcard/NEXUS_LLM_WIKI` الحقيقي، ولم تُقرأ/تُستخرج دلاليًا مصادر corpus. تطبيق `--apply` اقتصر على temporary fixture داخل `staging/workflow-tests/` التي لا تُحذف وفق سياسة المهمة.

### القيود والنتيجة

- لا يثبت هذا الإصلاح اكتمال أي domain أو T/C/K/M/QA أو `source_done`، ولا يضيف snapshot/Claim/Concept/Master. لا يثبت `reviewer` الحقيقي خارج metadata المعلنة؛ لا توجد مصادقة هوية.
- symlink/hardlink integration الحقيقيان غير قابلين للتنفيذ على mount الحالي (`Permission denied`/`Operation not permitted`)، لذلك بقي الاختباران skipped واستُخدمت guards mocked؛ هذا قيد بيئي مسجل، لا PASS للمنصة.
- لا يوجد Git repository تحت `/sdcard/NEXUS_LLM_WIKI`؛ لم يُنشأ commit. لم تُعدّل `raw/` أو `config/` أو `claims/` أو `concepts/` أو `masters/`، ولم يُحذف أي ملف. التسليم إلى Commander للمراجعة؛ لا تحديث لحالة TODO أو domain.
