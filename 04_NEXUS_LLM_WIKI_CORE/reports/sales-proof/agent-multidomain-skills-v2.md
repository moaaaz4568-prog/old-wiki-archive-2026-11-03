# تقرير Worker — المهارات العامة متعددة المجالات v2

التاريخ: 2026-10-10

## نطاق التكليف وحالة العمل

النطاق: إنشاء خمس مهارات عامة داخل `/sdcard/NEXUS_WIKI_SKILLS/` وتحديث
`INDEX.md` فقط من الملفات السابقة في حزمة المهارات، دون تعديل أي ملف داخل
`/sdcard/NEXUS_LLM_WIKI/` أو raw أو Terms/Claims/Concepts/Masters. لم يُستخدم
Codex ولم يُفوّض عمل إلى Agents أخرى. تُترك قرارات إغلاق المهمة وتحديث التحقق
في قائمة مهام Commander له أو للمراجع المكلّف.

**التسليم إلى Commander: الملفات الخمسة والفهرس جاهزة للمراجعة؛ الفحوص المطلوبة
نجحت 5/5، مع فحص بنيوي إضافي لكل المهارات 12/12.** الخطوة التالية للـCommander:
مراجعة التسليم وقرار التكامل، لا تشغيل دورة مصادر تلقائيًا. لا يوجد blocker
داخل نطاق تأليف المهارات، ولا يعني هذا التسليم اكتمال أي domain في الويكي.

## الملفات المكتوبة

داخل `/sdcard/NEXUS_WIKI_SKILLS/` أُنشئت هذه الملفات الخمسة فقط:

| الملف النسبي | الأسطر المقاسة | الوظيفة |
|---|---:|---|
| `domain-discovery-and-routing/SKILL.md` | 224 | قراءة كاملة دلالية، عائلات دليل من المتن، primary واحد وsecondary، uncertain/quarantine |
| `new-to-done-source-lifecycle/SKILL.md` | 277 | هوية/hash/dedup، مرجع أو نسخة آمنة، وفصل إغلاق التوجيه عن إغلاق المصدر والقسم والمجال |
| `domain-term-inventory/SKILL.md` | 219 | استكمال القراءة وTerms/aliases/relations بمواضع وبصمات، مع بوابة مانعة قبل الطبقات التالية |
| `sequential-domain-orchestration/SKILL.md` | 253 | أدوار وملكية وقفل مشترك، مراحل متتابعة، checkpoints وفتح التالي بعد domain_done فقط |
| `folder-index-and-handoff/SKILL.md` | 270 | INDEX محلي في المستويات الأربعة، وظيفة وحالة واعتماديات وhandoff قابل للاستئناف |

عُدّل `INDEX.md` وحده من ملفات حزمة المهارات السابقة، بإضافة الخمس وتصنيفها
`general`، وتمييز نسختي `opinion-context-evaluation` و
`master-synthesis-retrieval-gate` اللتين تحويان سياق مبيعات بـ`sales-specific`.
ظلت المهارات العامة السابقة `general` ولم تُعدّل ملفاتها. أصبح الفهرس 12 مدخلًا
بلا تكرار، والخمس الجديدة كلها عامة؛ صيغة المسارات الجديدة placeholders.

خارج حزمة المهارات: أُنشئ هذا التقرير، وأُلحق تحديث استمرارية بقسم مستقل في
`/root/r/.opencode/context.md` وفق تعليمات Worker. لم تُعدّل قائمة المهام أو
`sync-issues.md` أو بيانات مهام سابقة. لم يُنشأ script أو README أو حزمة تثبيت
غير مطلوبة، ولم يُستخدم generator ينشئ أمثلة تحتاج حذفًا لاحقًا.

## القراءة الفعلية

- `USER_MESSAGES_SESSION_EF22.md`: قُرئ كاملًا، 305 أسطر؛ الطلب التاريخي يثبت
  الفهارس ووظيفة Master، ولا ينسب تفاصيل lifecycle إلى رسائل لم تذكرها.
- فهرس المهارات الأصلي: 15 سطرًا، والمهارات السبع كاملة:
  `source-ingestion-and-dedup` (48)، `claim-extraction-and-evidence` (50)،
  `opinion-context-evaluation` (48)، `concept-deepening` (36)،
  `master-synthesis-retrieval-gate` (84)، `evidence-driven-reasoning` (28)،
  `wiki-iteration-and-risk-control` (26).
- الميثاق `MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md`: 233 سطرًا.
- `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md`: 766 سطرًا.
- المراجع المساندة المقروءة: `AGENTS.md` و`SCHEMA.md` وفهرس Systems للويكي،
  وخطة `agent-multidomain-plan.md` وتقارير الأنظمة والتدقيق القائمة.
- ملفات استمرارية المهمة الموجودة قُرئت قبل العمل؛ `status.md` و
  `verification-checklist.md` غير موجودين في `.opencode` عند القراءة.

## قرارات المراجعة الدلالية ومراجعها

- `Source.status` في SCHEMA يقبل `new|processed|quarantined` فقط؛ لا يجوز حقن
  `source_done` أو `domain_done` فيه.
- النظام 14 §§3،9،12 يغلق التوجيه فقط؛ الميثاق §§4،5،8،9 يطلب اكتمال المعالجة
  والبوابات قبل إغلاق المجال. فُصلت الحالتان بلا تخفيف للميثاق: `routing_ready`
  علامة staging في workflow، و`route_status: done` بعد G0–G8 على artifact
  النهائي، و`source_done` إغلاق معالجة معرفية، ثم subdomain/domain closure.
  هذه labels تشغيلية في المهارات وليست ادعاء وجود API أو قيم Source schema
  جديدة. تُحفظ السجلات routing-only القائمة دون تغيير أو رفعها إلى اكتمال معرفة.
- القراءة الكاملة لا تُستبدل بحساب hash آلي أو بمعاينة مقطوعة؛ مواضع النص
  وخريطة التغطية والبصمة مرتبطة. مرجع ذلك نظام 14 §§5،7،8،12.
- المصطلح الجوهري بلا تعريف أو مرجع يمنع Terms gate حتى لو وُضع في gaps؛
  توثيق ملاحظة حرجة لا يحلها. الميثاق §5.1 و§8 هما مرجع المنع.
- قفل المجال مشترك بين `RUN_ID` المختلفة؛ لا تنفيذ للمجال التالي ولا انتقال
  للمرحلة التالية قبل قبول السابقة وQA. مرجع ذلك الميثاق §§2،5،8،9.
- الفهارس لا تعوّض الدليل أو Master؛ لا كتابة INDEX داخل raw، بل مرجع مشتق
  خارجه. مرجع ذلك الميثاق §§6،7 ورسالتا 7 و9 في تقرير EF22.
- تصنيف المهارات السابقة اعتمد محتواها المقروء، لا مجرد استخدامها في المبيعات؛
  لا تُطبق حالاتها التاريخية على بيئة جديدة. الفهرس ينبه أيضًا إلى عدم استعمال
  fallback قديم يناقض فصل دور القائد عن منفذي المعرفة في الميثاق.
- فحص `quick_validate.py` لا يغطي تطابق اسم المجلد أو غياب العلامات أو الدلالة؛
  يُستكمل بفحص خاص موثق ومراجعة العقود، ولا يعلن تشغيلًا معرفيًا ناجحًا.

## التحقق الأولي المنفّذ

شُغّل `python3 /root/.opencode/skills/skill-authoring/scripts/quick_validate.py`
على كل مجلد من الخمسة، وأعاد كل تشغيل `Skill is valid!` دون خطأ.
فحص محلي إضافي للاسم والوصف وfrontmatter والعلامات وفهرسة الخمس أعاد
`CHECK=PASS`. ثم أُعيدت الفحوص بعد المراجعة النهائية كما هو موثق أدناه.

فحص إضافي لأعمدة جداول Markdown فشل على مسودة lifecycle:

```text
new-to-done-source-lifecycle:72: table_columns=4 expected=2
MARKDOWN_TABLE_CHECK=FAIL
```

السبب: فواصل `|` داخل تعداد Source.status في جدول Markdown لم تكن escaped؛
صُححت إلى `\|`. فحص الأعمدة محفوظ ضمن الفحص القابل لإعادة التشغيل أدناه.
هذا فشل تنسيق مسودة؛ إعادة الفحص النهائي اجتازته، وليس عيبًا في corpus.

## نتائج التحقق النهائية المرصودة

| Skill | YAML frontmatter صالح وlowercase | الاسم يطابق المجلد | وصف غير فارغ | بلا TODO | quick_validate | LSP |
|---|---|---|---|---|---|---|
| `domain-discovery-and-routing` | PASS | PASS | PASS | PASS | PASS | clean |
| `new-to-done-source-lifecycle` | PASS | PASS | PASS | PASS | PASS | clean |
| `domain-term-inventory` | PASS | PASS | PASS | PASS | PASS | clean |
| `sequential-domain-orchestration` | PASS | PASS | PASS | PASS | PASS | clean |
| `folder-index-and-handoff` | PASS | PASS | PASS | PASS | PASS | clean |

- أُعيد أمر `python3 /root/.opencode/skills/skill-authoring/scripts/quick_validate.py
  /sdcard/NEXUS_WIKI_SKILLS/<skill-name>` على كل اسم أعلاه؛ أعادت التشغيلات
  الخمسة `Skill is valid!` بنجاح.
- نُفّذ كود الفحص المحفوظ في القسم التالي فعليًا بعد آخر تعديل للمهارات:
  12/12 اجتازت frontmatter/الاسم/الوصف/غياب العلامات، وكل قوالب YAML/JSON
  الإحدى عشرة قابلة للتحليل، ولا أخطاء أعمدة جداول أو fences أو مسارات ثابتة
  في المهارات الخمس والفهرس. انتهى برمز خروج 0:

  ```text
  INDEX: entries=12, new_general=5/5
  SKILLS_CHECK=PASS
  ```

  أُعيد لاحقًا استخراج كود الفحص حرفيًا من هذا التقرير وتشغيله عبر
  `subprocess.run([sys.executable, '-c', code])`؛ أعاد نفس PASS وانتهى بـ
  `RETAINED_REPORT_CHECK_EXIT=0`. يؤكد ذلك قابلية إعادة استخدام الاختبار المحفوظ.

- استُدعيت `lsp_diagnostics` على كل واحد من ملفات SKILL.md الخمسة؛ أعادت
  `status: clean` و`No diagnostics found. All clean!` لكل ملف. هذا ليس بديلًا
  عن فحص YAML أو مراجعة العقد، وليس اختبار سلوك Agent فعلي.
- استُدعيت الأداة كذلك على INDEX وهذا التقرير وأعادت `clean`. جرد الحزمة النهائي
  أظهر الملفات الاثني عشر للمهارات وINDEX فقط، بلا ملفات إضافية في المجلدات الخمسة.
- نُفّذت مراجعة نصية كاملة للمهارات والمستهلكات المشار إليها، مع الحفاظ على
  حالة الغموض وإظهار الفجوات ومنع تجاوز البوابات.

## فحص قابل لإعادة التشغيل

الفحص التالي يقرأ الملفات فقط. يستخدم PyYAML الموجود (`6.0.2` قيس في هذه
الجلسة)، ويفحص المهارات الاثنتي عشرة بنيويًا، ويضيف فحوص القوالب والجداول
والمسارات للمهارات الخمس الجديدة. لا ينفذ lifecycle ولا يقيّم صحة معرفة مجال.

```bash
python3 - <<'PY'
from pathlib import Path
import json
import re
import yaml

root = Path('/sdcard/NEXUS_WIKI_SKILLS')
new_names = [
    'domain-discovery-and-routing',
    'new-to-done-source-lifecycle',
    'domain-term-inventory',
    'sequential-domain-orchestration',
    'folder-index-and-handoff',
]
old_names = [
    'source-ingestion-and-dedup',
    'claim-extraction-and-evidence',
    'opinion-context-evaluation',
    'concept-deepening',
    'master-synthesis-retrieval-gate',
    'evidence-driven-reasoning',
    'wiki-iteration-and-risk-control',
]
failures = []
expected = set(old_names + new_names)
actual = {p.parent.name for p in root.glob('*/SKILL.md')}
if actual != expected:
    failures.append(f'inventory: missing={expected-actual}, extra={actual-expected}')
for name in old_names + new_names:
    path = root / name / 'SKILL.md'
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        failures.append(f'{name}: {exc}')
        continue
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    try:
        metadata = yaml.safe_load(match.group(1)) if match else None
    except yaml.YAMLError as exc:
        metadata = None
        failures.append(f'{name}: invalid YAML: {exc}')
    checks = {
        'frontmatter': isinstance(metadata, dict),
        'lowercase_keys': isinstance(metadata, dict) and set(metadata) == {'name', 'description'},
        'name_matches': isinstance(metadata, dict) and metadata.get('name') == name,
        'description_nonempty': isinstance(metadata, dict)
        and isinstance(metadata.get('description'), str)
        and bool(metadata['description'].strip()),
        'no_todo': 'TODO' not in text.upper(),
    }
    for key, ok in checks.items():
        if not ok:
            failures.append(f'{name}: {key}')
    print(name + ': ' + json.dumps(checks, sort_keys=True))
    if name not in new_names:
        continue
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 40:
        failures.append(f'{name}: invalid skill name')
    if '<wiki_root>' not in text or re.search(r'/(?:root|sdcard|home|Users|opt|tmp)/', text):
        failures.append(f'{name}: path portability')
    if text.count('```') % 2:
        failures.append(f'{name}: unbalanced fences')
    template_count = 0
    for language, body in re.findall(r'^```(yaml|json)\n(.*?)^```\s*$', text, re.M | re.S):
        try:
            yaml.safe_load(body) if language == 'yaml' else json.loads(body)
        except (yaml.YAMLError, json.JSONDecodeError) as exc:
            failures.append(f'{name}: invalid {language} template: {exc}')
        template_count += 1
    fenced = False
    width = None
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith('```'):
            fenced = not fenced
            width = None
            continue
        if fenced:
            continue
        if line.startswith('|'):
            cells = len(re.split(r'(?<!\\)\|', line.strip())) - 2
            if width is None:
                width = cells
            elif cells != width:
                failures.append(f'{name}:{number}: table_columns={cells} expected={width}')
        else:
            width = None
    print(f'  lines={len(text.splitlines())}, words={len(text.split())}, templates={template_count}')

index = (root / 'INDEX.md').read_text(encoding='utf-8')
rows = {}
for line in index.splitlines():
    match = re.match(r'^\| `([a-z0-9-]+)` \| (.*?) \| (general|sales-specific) \|$', line)
    if match:
        if match[1] in rows:
            failures.append(f'INDEX: duplicate {match[1]}')
        rows[match[1]] = match[3]
if set(rows) != expected:
    failures.append('INDEX: entries do not equal skill folders')
if any(rows.get(name) != 'general' for name in new_names):
    failures.append('INDEX: a new skill is not general')
if re.search(r'/(?:root|sdcard|home|Users|opt|tmp)/', index):
    failures.append('INDEX: hardcoded host path')
print(f'INDEX: entries={len(rows)}, new_general={sum(rows.get(n) == "general" for n in new_names)}/5')
for failure in failures:
    print('FAIL:', failure)
print('SKILLS_CHECK=' + ('FAIL' if failures else 'PASS'))
raise SystemExit(bool(failures))
PY
```

## حدود الأدلة

لم تُشغّل دورة استقبال أو استخراج أو توليف، ولم تُجرَ فحوص raw قبل/بعد شاملة؛
لا يُدّعى ذلك من اختبارات Markdown. لم تُحل قضايا الويكي السابقة في
`.opencode/sync-issues.md` لأنها خارج نطاق هذه المهمة.

لم يُشغّل `bulk_ingest.py` أو `wiki_quality.py`: لا يختبران حزمة المهارات هذه
ولا يغطي نجاحهما بواباتها. لم يُشغّل build أو test suite لتطبيق، لأن التغيير
تعليمات Markdown بلا كود تنفيذي أو إعداد تطبيق. حالات التحقق داخل المهارات
عقود متوقعة للمشغّل المستقبلي وليست نتائج معالجة corpus هنا.

حُمّلت مهارتا `skill-authoring` و`skill-testing`. لم تُشغّل سلسلة التقييم legacy
التي تشترط `Name/Tier/README/scripts`؛ ليست عقد المستخدم الذي يطلب lowercase
`name/description` وخمسة SKILL.md فقط. استُخدم المدقق المتاح مع فحص YAML إضافي
ومراجعة العقود، دون ادعاء درجة جودة من أداة لم تُشغّل. لم تُنشأ حزمة zip أو
يُثبت شيء أو يُنفذ حذف أو commit/push.

**القيود المتبقية للـCommander:** توفير config ومسارات فعلية وأداة قفل/verifier
متوافقة قبل أي تشغيل للمهارات؛ هذه التعليمات لا تدعي أن الآليات أو Terms schema
جاهزة في الويكي. تبقى قضايا التكامل القديمة خارج هذا التسليم، ولا يفتح هذا
التقرير domain جديدًا أو يعلن `domain_done` لأي معرفة.
