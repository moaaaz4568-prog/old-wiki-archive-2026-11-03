# Worker — مواءمة Skills v3 مع عقد 2026-10-10

## النطاق والحالة

- الهدف: إصلاح المهارات الخمس العامة والفهرس، ومواءمة المهارات الثلاث المسموح بها
  `source-ingestion-and-dedup` و`claim-extraction-and-evidence` و
  `master-synthesis-retrieval-gate`، دون تعديل الويكي أو config أو done أو المعرفة.
- المرجعان المقروءان: `MULTIDOMAIN_ALIGNMENT_2026-10-10.md` كاملًا (103 أسطر)،
  و`USER_MESSAGES_SESSION_EF22.md` كاملًا بما فيه الملحق الأحدث (350 سطرًا).
- قُرئت ملفات المهارات الثمانية والفهرس قبل تعديلها. لم تُقرأ مخرجات الوكلاء
  المتزامنة أو تُستخدم كمرجع. التقرير v2 تاريخي ولا يُحدّث في هذه المتابعة.
- الحالة الحالية: تسليم جاهز لمراجعة Commander بعد تطبيق المواءمة عبر
  apply_patch واجتياز الفحوص أدناه. الخطوة التالية مراجعة التكامل لدى القائد؛
  لا عائق داخل نطاق Skills ولا إعلان اكتمال domain.
- التوثيق المرحلي هنا فقط؛ لا تعديل لسجلات مشتركة أو علامات مهام القائد.

## التعارضات المرصودة قبل الإصلاح

1. lifecycle يؤخر نسخة done إلى ما بعد Concepts/Masters ويشترطهما لـsource_done.
2. Terms والوصف في المهارة والمنسق يمنعان تسجيل Claims قبل غلق Terms؛ هذا يخالف
   جمع المصطلحات وcandidate Claims أثناء قراءة المجال النشط.
3. المنسق والتوجيه والفهرسة يمنعون فرز مجالات الانتظار، رغم أن الفرز العام جائز.
4. النسخة المادية اختيارية والمرجع النصي افتراضي؛ المطلوب العكس مع نسخة مستقلة.
5. Master skill لا يفرض all-domain domain_terms_complete حتى للكتاب الصغير،
   ويحمل ادعاءً زمنيًا عن عدم وجود canonical في الويكي لا يصح تعميمه.
6. بعض تصنيفات sales-specific مضللة لمهارات قابلة لإعادة الاستخدام بأمثلة مبيعات.

## دليل red ثم الإصلاح

- نُفذت النسخة الأولية من فحص الارتداد قبل التعديل: فشلت المهارات الثماني، وكانت الخلاصة
  `ALIGNMENT_CHECK=FAIL; failures=125` ورمز الخروج 1. العدد هو فحوص وجود/غياب
  نصوص، وليس 125 عيبًا معرفيًا مستقلًا.
- بعد تطبيق المواءمة نجحت الثماني: `ALIGNMENT_CHECK=PASS; failures=0`.
  أضيفت حراس نصية وفحوص فهرسة أخرى، وأعيد الفحص المحفوظ بعد آخر تبسيط؛ نجح
  مجددًا بالنتيجة نفسها ورمز خروج 0.
- رُفضت محاولة patch للمهارات الثلاث المساندة بسبب سياق أخير غير مطابق؛ أعيدت
  قراءة الملفات الثلاثة وتأكد بقاؤها دون تغيير، ثم أُعيد patch الصحيح بنجاح.
- اختُصرت القوالب المتكررة وترك تعريف البوابات مفصلًا في INDEX، مع عقد مختصر
  صريح في كل Skill. لا تُعاد وثائق الويكي كاملة ولا تُنسب APIs إليها.

## ملفات التسليم والقرارات

المسارات الثمانية أدناه تحت `/sdcard/NEXUS_WIKI_SKILLS/`، وكل تعديل في SKILL.md
الموجود، دون إنشاء مهارات أو scripts جديدة:

| Skill | الأسطر النهائية | التغيير الخاص بالإضافة إلى عقد المواءمة الصريح |
|---|---:|---|
| `domain-discovery-and-routing` | 181 | فرز عالمي، queued مستقل، uncertain للتصنيف، واستئناف قراءة لم تنته بلا عزل تخميني |
| `new-to-done-source-lifecycle` | 246 | نسخة مباشرة مستقلة في subdomain؛ R قبل extraction، وإزالة K/M من شروط source_done |
| `domain-term-inventory` | 222 | manifest كل المرشحين لا المقروءين فقط، تسجيل تدريجي، وT للمجال كله قبل M |
| `sequential-domain-orchestration` | 242 | قفل المعرفة لا الفرز، أدوار التسجيل والمراجعة، K بالأدلة المراجعة وM بعد T العام، queue للـdelta |
| `folder-index-and-handoff` | 226 | فهارس routing للمجالات المنتظرة، أبعاد الحالة منفصلة، وفحص وجود النسخة لا source_refs فقط |
| `source-ingestion-and-dedup` | 83 | فصل الهوية وrouting وextraction، duplicate بلا مضاعفة دليل، عزل السلامة لا ضعف الصلة |
| `claim-extraction-and-evidence` | 92 | candidate Claims أثناء القراءة مع terms، ومراجعة الخلاف دون فرض إجماع |
| `master-synthesis-retrieval-gate` | 120 | منع كل Master قبل all-domain T، إزالة الادعاء الزمني عن canonical، والإبقاء على عقد الكتاب واختبار الاسترجاع |

عُدّل `INDEX.md` (66 سطرًا) بإصدار عقد **2026-10-10** وتعريف R/T/C/K/M/QA
وتمييز source_done وsubdomain_extraction_done وdomain_terms_complete وdomain_done.
بقيت قائمة المهارات 12 مدخلًا؛ غُيّر تصنيف opinion-context-evaluation و
master-synthesis-retrieval-gate إلى `reusable with sales examples`، لا تخصص
مبيعات مضلل. المهارات الأربع الأخرى لم تُعدّل.

مرجع القرارات: المواءمة §§2–3 للفرز والنسخة، §4 للحالات، §5 للجمع المرشح
والخلافات، §6 للتغطية والـdelta، §7 للفهرسة والاسترجاع. الملحق أحدث من التحليل
التاريخي. حيث يحتمل نص قديم استخدام quarantine للغموض، اتُّبع التكليف الأحدث
هنا: uncertain للغموض وquarantine لفساد/تعذر قراءة/هوية، والانتظار queued.

## التحقق المنفّذ فعلًا

1. **quick_validate: 8/8 ناجحة**، لكل Skill معدلة. استُخدم runner Python يستدعي
   الأمر التالي لكل اسم في جدول التسليم، دون shell أو ملفات إضافية:

   ```text
   python3 -B /root/.opencode/skills/skill-authoring/scripts/quick_validate.py /sdcard/NEXUS_WIKI_SKILLS/<skill-name>
   ```

   أعادت التشغيلات الثمانية `exit=0; Skill is valid!` وخلاصة runner
   `QUICK_VALIDATE: 8/8`.
2. **الفحص المحفوظ:** `ALIGNMENT_CHECK=PASS; failures=0`، exit 0 بعد آخر تعديل؛
   يختبر YAML lowercase والاسم والوصف وغياب TODO وplaceholders والقواعد النصية
   وعدم عودة الصيغ القديمة والروابط المحلية والتصنيف في الفهرس.
3. **Markdown:** فُحصت أعمدة الجداول خارج code fences في الملفات الثمانية
   وINDEX، والنتيجة `MARKDOWN_TABLE_CHECK=PASS`، exit 0. قيس عدد الأسطر في
   جدول التسليم من الملفات نفسها في التشغيل ذاته.
4. **LSP:** استُدعيت `lsp_diagnostics` على SKILL.md الثمانية وعلى INDEX؛ أعادت
   `status: clean` و`No diagnostics found. All clean!` لكل ملف.
5. **مراجعة دلالية نصية:** قُرئت الملفات المعدلة كاملة، ثم صُححت بقايا الالتباس
   في وصف المنسق وmanifest المصطلحات وحالة انقطاع القراءة. فُحصت الأوصاف
   والشروط الإيجابية والسلبية، لا مقدمة العقد وحدها.

## حدود النتيجة وما لم يُنفّذ

الفحوص نصية/بنيوية للمهارات، لا محاكاة لاستخراج أو نسخ أو قفل حي، ولا إثبات أن
R/T/C/K/M/QA نُفذت في الويكي. حالات التحقق داخل Skills موسومة كتوقعات لا نتائج.
لا يوجد build لتطبيق تغير هنا؛ لم يُشغّل corpus أو أدوات كتابة wiki أو اختبار
استرجاع معرفي. لم تُقرأ تقارير الوكلاء المتزامنة لتقرير جاهزية التكامل.

لم تكتب أدوات هذه المتابعة في wiki/systems/config/done أو raw أو أي معرفة،
ولم تُعدّل السجلات المشتركة أو التقرير v2 أو قائمة المهام. التقرير الجديد
الوحيد هو هذا الملف. لم يُستخدم Codex أو subagents أو حذف أو commit/push.
لا يُدّعى ثبات ملفات يغيّرها وكلاء آخرون؛ القائد يتحقق من تكامل العقود عند
تسلمه، ولا تُسجل هنا domain_done لأي مجال.

## فحص ارتداد محفوظ — نصي/بنيوي لا اختبار corpus

الكود التالي للقراءة فقط. يفحص وجود قواعد العقد وعدم عودة صيغ التعارض المعروفة،
مع YAML والقوالب والروابط المحلية. اجتيازه لا يثبت تنفيذ R/T/C/K/M/QA في الويكي.

```python
from pathlib import Path
import json
import re
import yaml

root = Path('/sdcard/NEXUS_WIKI_SKILLS')
names = [
    'domain-discovery-and-routing', 'new-to-done-source-lifecycle',
    'domain-term-inventory', 'sequential-domain-orchestration',
    'folder-index-and-handoff', 'source-ingestion-and-dedup',
    'claim-extraction-and-evidence', 'master-synthesis-retrieval-gate',
]
required = [
    '2026-10-10', 'R/T/C/K/M/QA', 'route_done', 'source_done',
    'domain_terms_complete', 'subdomain_extraction_done', 'byte-exact',
    'done/<domain>/<subdomain>/', 'source_refs', 'current_domain',
    'queued', 'candidate Claims', 'scope', 'delta', 'stale',
]
forbidden = [
    'استخدم المرجع النصي الآمن افتراضيًا',
    'وقُبلت مساهماته في Concepts',
    'تشغيل بوابة تمنع Claims ثم Concepts',
    'domain_locked', 'دون تنفيذ\n   مجال لاحق أو نشر route نهائي له',
    'لا يبدأ تصنيف\n   تنفيذي أو قراءة مسبقة',
    'لا تنشئ `INDEX.md` داخل raw أو داخل domain لاحق',
    'بوابة Terms فاشلة أو source غير محسوم: لا Claims',
    'لا يوجد Master `canonical` حاليًا',
    'source_done قبل Terms لأن إغلاق المصدر الكامل يأتي بعد المراحل المعرفية',
    'النسخة الاختيارية', 'terms → claims → concepts → masters',
    'inventory_status: blocked',
]
failures = []
for name in names:
    text = (root / name / 'SKILL.md').read_text(encoding='utf-8')
    local = []
    fm = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    try:
        meta = yaml.safe_load(fm[1]) if fm else None
    except yaml.YAMLError:
        meta = None
    if not isinstance(meta, dict) or set(meta) != {'name', 'description'}:
        local.append('frontmatter')
    elif meta['name'] != name or not isinstance(meta['description'], str) or not meta['description'].strip():
        local.append('name/description')
    if 'TODO' in text.upper():
        local.append('unfinished marker')
    local += [f'missing:{token}' for token in required if token not in text]
    local += [f'stale:{token}' for token in forbidden if token in text]
    if '<wiki_root>' not in text or re.search(r'/(?:root|sdcard|home|Users)/', text):
        local.append('path portability')
    if text.count('```') % 2:
        local.append('unbalanced fences')
    for lang, body in re.findall(r'^```(yaml|json)\n(.*?)^```\s*$', text, re.M | re.S):
        try:
            yaml.safe_load(body) if lang == 'yaml' else json.loads(body)
        except (yaml.YAMLError, json.JSONDecodeError):
            local.append(f'{lang} template')
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if '<' not in link and '://' not in link and not (root / name / link.split('#')[0]).is_file():
            local.append(f'broken link:{link}')
    print(name + ': ' + ('FAIL ' + '; '.join(local) if local else 'PASS'))
    failures += [(name, item) for item in local]
index = (root / 'INDEX.md').read_text(encoding='utf-8')
if '2026-10-10' not in index or 'reusable with sales examples' not in index:
    failures.append(('INDEX', 'version/classification'))
rows = re.findall(r'^\| `([a-z0-9-]+)` \| .*? \| (.*?) \|$', index, re.M)
if len(rows) != 12 or len(dict(rows)) != 12:
    failures.append(('INDEX', 'inventory/duplicate rows'))
for name in ('opinion-context-evaluation', 'master-synthesis-retrieval-gate'):
    if dict(rows).get(name) != 'reusable with sales examples':
        failures.append(('INDEX', 'misleading classification:' + name))
for name in names:
    if index.count('`' + name + '`') != 1:
        failures.append(('INDEX', 'missing/duplicate:' + name))
print(f'ALIGNMENT_CHECK={"FAIL" if failures else "PASS"}; failures={len(failures)}')
raise SystemExit(bool(failures))
```

تشغيل الفحص المحفوظ دون إنشاء script إضافي:

```bash
python3 -B - <<'PY'
from pathlib import Path
import subprocess
import sys
text = Path('/root/r/reports/sales-proof/agent-multidomain-skills-v3.md').read_text(encoding='utf-8')
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
raise SystemExit(subprocess.run([sys.executable, '-B', '-c', code], check=False).returncode)
PY
```
