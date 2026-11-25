# تحديث مداخل النموذج — 2026-10-18

## نطاق التكليف وسجل الاستئناف

- `change_id: CHG_20261018_entrypoints`؛ `workflow_id: WF_20261018_entrypoints`.
- الهدف: مدخل قصير يوجه النموذج إلى ملفات فعلية، مع سجلات قرار وفحص وتسليم وتحديث توثيقي، لا إعادة تشغيل الاستخراج.
- المالك: Worker المنفذ مباشرة؛ المراجعة هنا ذاتية، وليست QA مستقلة. لا Codex أو subagents أو commit أو حذف.
- الكتابة المسموحة فقط: `AGENTS.md`, `SCHEMA.md`, `INDEX.md`, `START_HERE.md` وهذا التقرير.
- لا كتابة في README أو STATUS أو systems أو model_protocols أو config أو طبقات الدليل والمعرفة أو checkpoints.
- الحالة عند فتح السجل: `in_progress`؛ الخطوة التالية: إثبات فشل عقد المدخل، ثم إضافة امتدادات SCHEMA وتحديث المداخل بدفعات `apply_patch`.
- `base_snapshot_id: null` و`fencing_token: null`: مهمة توثيق فقط، لا انتقال مجال أو استرداد قفل. لا تُخترع snapshot معرفية أو صلاحية تنفيذ.

## القراءة والقرارات المحدودة

قُرئت كاملة قبل تعديل المداخل: AGENTS وSCHEMA وINDEX وREADME وSTATUS_FROM_ZERO، وconfig بملفيه، وسياسة موقع المخرجات، والميثاق ومواءمة 2026-10-10 وملحق الرسائل، وخطة ترتيب corpus، وsystems/INDEX والأنظمة 15 و18 و20–25، وmodel_protocols/README وبروتوكولاته الخمسة، وخطة الاستخراج 2026-10-17 والدفعات الثلاث. استُكملت المقاطع التي قصّتها أداة القراءة حتى EOF؛ قراءة JSON هنا فحص لعقد المدخل وحالة المرشح، وليست مراجعة مصدر أو قبول Terms/Claims.

- خطة [ترتيب corpus](CORPUS_DOMAIN_ORDER_PLAN_2026-10-11.md) §§1 و4 و5 تكفي لفصل الهدف الشامل عن config الحالية؛ لم تلزم قراءة مقترح الكتالوج الكامل أو اعتماده.
- config الحالية تعرف أربعة domains؛ لا تتحول مقترحات التوسع إلى مسارات تشغيلية أو معرفة مأذونة بهذا التعديل.
- الدفعات تحمل `candidate_only: true`، ومراجعاتها المعلنة ذاتية؛ لا يُستنتج من ذلك أن مراجعة مستقلة تمت.
- القرار: خرائط وروابط إلى العقود بدل نسخها، وسجلات جديدة اختيارية للقديم ومطلوبة الحقول فقط عند استعمال النوع الجديد.
- بديل مرفوض: تحديث README/config أو إصلاح الأنظمة هنا؛ خارج التكليف. لا رفع لبوابة أو حالة معرفة.

## أخطاء وحدود رُصدت قبل التعديل

1. فشل `git_status` للجذر: `fatal: not a git repository (or any parent up to mount point /mnt)`، exit 128؛ لا توجد baseline Git لهذا المسار، ولم يُنشأ مستودع أو commit.
2. لم توجد `.opencode` داخل الويكي، ولا التقرير الحالي أو START_HERE عند البداية. حالة mission المقروءة في بيئة التشغيل تخص مهام أخرى؛ لم تُغيّر.
3. انتهى الأمر `python3 -B tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json` بمهلة 120000ms دون stdout أو exit code نهائي؛ النتيجة غير مثبتة وليست PASS أو فشلًا دلاليًا. الأمر بلا `--report` أو `--index` ولا مسار إخراج.
4. بعد المهلة شُغّل `pgrep -af '[w]iki_quality.py'`؛ exit 1 بلا عملية مطابقة. لا retry أعمى. سيبقى الفحص العام غير مكتمل إن لم يُعد لاحقًا بنطاق ووقت مناسبين.
5. اختبارات `tools/tests/test_wiki_workflow.py` تكتب fixtures في `staging/workflow-tests/` وفق `setUp`؛ لن تُشغّل ضمن إذن كتابة خمسة ملفات فقط. بديل هذه المهمة فحص توثيقي قراءة فقط محفوظ أدناه.

## توافق systems20–25: تعارضات لا تمنح صلاحيات

| الموضع المقروء | التعارض/الحد | المعالجة ضمن هذا التكليف |
|---|---|---|
| system20 §4.2 | ترتيبه الداخلي يبدأ بالمستخدم ولا يذكر system/developer | يصرّح AGENTS بالهرمية الفعلية: system/developer ثم user ثم repo؛ المرجع الخام لا يصير تعليمات |
| README §ترتيب القراءة، system20 §3، systems/INDEX | ترتيبات بدء مختلفة عن الطلب الحالي | START_HERE يتبع ترتيب المستخدم الحالي؛ بقية الملفات لا تُعدّل |
| system20 §5 وsystem22 §3.2 | صياغة خطية R→T→C، وعبارة تجعل T تمنع القبول، مقابل السماح بمراجعة C/K محليًا قبل T في الميثاق وsystem15 §4 وsystem21 §3.2 | لا صلاحية جديدة: المرشح ليس قبولًا، Concepts بعد مراجعة أدلتها، وأي Master ينتظر T الشاملة |
| system20 §5 و§11؛ system22 §§3.1 و5 و7.1؛ system24 §10.6 | أمثلة `pass_local` وClaim/Concept `blocked/stale` وGate `not_evaluated` لا تطابق enums SCHEMA الأصلية | تبقى workflow/نتائج محلية منفصلة، ولا تضاف إلى Source/Claim/Concept/Gate statuses |
| config/processing_order.json `completion_states.source_done.scope` مقابل system15 §1 وsystem25 §5.5 وSCHEMA | config تصف مساهمة مجال واحد تحت source_done، بينما العقد يميز إكمال كل وحدات المصدر | لا ترقية للمساهمة إلى إكمال المصدر؛ يُذكر النطاق الصريح و`source_domain_extraction_complete`، ولا تعديل config |
| system24 §§5 و9 و13.3 مقابل model_protocols/05 §2 | إلزام revision/token مقابل السماح بـnull عند عدم الانطباق؛ config الحالية لا تعرض حقول القفل التنفيذية المفصلة | null مسبب لتوثيق بلا انتقال فقط؛ أي استئناف كتابة معرفية/نقل ملكية يحتاج المالك وبيانات القفل الفعلية، وإلا blocked |

الامتدادات المقصودة تحيل إلى decision ledger في20، وفحوص21–23، وتسليم24، وmanifest وتوافق25؛ لا تستبدل العقود أو توسع allowed_write_paths. هذه مقارنة نصية ذاتية، لا اعتماد مستقل للأنظمة.

## فحص ارتداد توثيقي محفوظ (قراءة فقط)

من جذر الويكي: `python3 -B -m doctest -v reports/ENTRYPOINT_UPDATE_2026-10-18.md`.
هذا فحص عقد المدخل والروابط، لا verifier للقراءة الدلالية أو لبوابات المعرفة.

```pycon
>>> from pathlib import Path
>>> import hashlib, re
>>> root = Path.cwd()
>>> entry_files = ['AGENTS.md', 'SCHEMA.md', 'INDEX.md', 'START_HERE.md']
>>> record_types = ['decision_record', 'verification_record', 'handoff_record', 'documentation_update_record']
>>> def entry_contract():
...     errors = []
...     start = root / 'START_HERE.md'
...     if not start.is_file():
...         errors.append('START_HERE missing')
...     elif not 60 <= len(start.read_text(encoding='utf-8').splitlines()) <= 100:
...         errors.append('START_HERE length outside 60..100')
...     schema = (root / 'SCHEMA.md').read_text(encoding='utf-8')
...     errors.extend(kind + ' missing' for kind in record_types if '\ntype: ' + kind + '\n' not in schema)
...     index = (root / 'INDEX.md').read_text(encoding='utf-8')
...     errors.extend(name + ' missing from INDEX' for name in ['START_HERE.md', 'STATUS_FROM_ZERO.md', 'SALES_EXTRACTION_2026-10-17_HIGH_TICKET.json', 'SALES_EXTRACTION_2026-10-17_PROPOSAL_FOLLOW_UP.json', 'SALES_EXTRACTION_2026-10-17_DISCOVERY.json'] if name not in index)
...     return errors
>>> entry_contract()
[]
```

## الملفات المضافة/المعدلة والفحوص اللاحقة

لم تُسجّل نتائج لاحقة بعد؛ تُضاف هنا بعد تشغيلها وإعادة القراءة، لا بالتوقع.
