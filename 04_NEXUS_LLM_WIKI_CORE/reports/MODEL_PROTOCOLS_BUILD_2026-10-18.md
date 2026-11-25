# تقرير بناء طبقة بروتوكولات تشغيل النموذج — 2026-10-18

## الحالة والنطاق

تم بناء طبقة بروتوكولات تشغيل نموذج **مستقلة عن النموذج** داخل:

```text
/sdcard/NEXUS_LLM_WIKI/model_protocols/
```

وتم وضع هذا التقرير في المسار المطلوب:

```text
/sdcard/NEXUS_LLM_WIKI/reports/MODEL_PROTOCOLS_BUILD_2026-10-18.md
```

النطاق محصور في إضافة ملفات Markdown البروتوكول والتقرير. لم تُعدّل `raw/` أو
`README.md` أو `AGENTS.md` أو `SCHEMA.md` أو `INDEX.md` أو أي ملف داخل `systems/`.
هذا التقرير يثبت مخرجات هذه المهمة وفحوصها فقط؛ لا يعلن اكتمال الويكي أو أي مجال
معرفي.

## المدخلات التي قُرئت

قُرئت الملفات المطلوبة التالية قبل الكتابة:

- `AGENTS.md`
- `SCHEMA.md`
- `INDEX.md`
- `systems/11_AGENT_EXECUTION_CONTRACT.md`
- `systems/16_SEQUENTIAL_AGENT_ORCHESTRATION.md`
- `STATUS_FROM_ZERO.md`

كما قُرئت `systems/INDEX.md` و`README.md` لفهم خريطة العقود والمسارات. المسار المطلوب
`systems/20_WIKI_OPERATING_SYSTEM.md` **غير موجود على القرص**؛ تم تسجيل ذلك كحد في
هذه المهمة، ولم يُنشأ ملف بديل ولم يُفترض محتواه.

## المخرجات

| المسار | المضمون |
|---|---|
| `model_protocols/README.md` | خريطة البروتوكولات، ترتيب استخدامها، قواعد مشتركة وحدود الإثبات |
| `model_protocols/01_REASONING_LOOP.md` | حلقة: فهم الطلب → تحديد النطاق → حصر القيود → جمع الأدلة → تسجيل الافتراضات → اختيار الإجراء → تنفيذ → تحقق → تقرير، مع Decision Record مختصر |
| `model_protocols/02_SOURCE_ANALYSIS.md` | القراءة الكاملة، فصل أنواع الوحدات، locators، Unicode half-open offsets، ومنع التعميم |
| `model_protocols/03_WRITING_PROTOCOL.md` | الكتابة العربية/بلغة المصدر، فصل Claim/Term/Concept/Master، citation، الثقة، وعدم الاختلاق |
| `model_protocols/04_REVIEW_AND_CORRECTION.md` | المراجعة المستقلة، اختبار الاقتباس، التناقضات، الروابط، schema، PASS/RETURN والتصحيح الشفاف |
| `model_protocols/05_TASK_EXECUTION_AND_REPORTING.md` | اختيار الدور، عقد التكليف، التقسيم والملكية، checkpoints، handoff، فشل الأدوات والتقرير |

## مطابقة المتطلبات

- كل ملف يحتوي الأقسام الصريحة: `ما يثبت الإجراء`، `ما لا يثبته الإجراء`، و`ما يجب
  تسجيله`.
- البروتوكولات model-agnostic، وتمنع ادعاء نقل قدرات نموذج بعينه أو كشف chain-of-thought؛
  البديل هو Decision Record وأدلة قابلة للمراجعة.
- الأمثلة موسومة بأنها محايدة/توضيحية، وتمنع تحويل المثال أو النتيجة المحدودة إلى
  قاعدة عامة.
- الحدود التشغيلية تفصل بين قراءة المصدر، الاستخراج المرشح، المراجعة، والتقرير؛ ولا
  تعتبر رسالة Agent أو EOF أو exit code وحدها إعلان نجاح.
- المراجع إلى `systems/` تستخدم مسارات نسبية من مجلد `model_protocols`، ولم تُعدّل
  العقود المشار إليها.

## التحقق المنفذ والنتائج

### 1. إعادة القراءة بعد الكتابة

أُعيدت قراءة الملفات الستة الجديدة كاملة بأداة القراءة بعد إنشائها. لم تُظهر القراءة
ملفًا مبتورًا أو مسارًا خارج مجلد البروتوكولات ضمن المخرجات المطلوبة.

### 2. فحص مجموعة الملفات والأقسام والروابط

نُفذ فحص Python للقراءة فقط، يتحقق من مجموعة الملفات، ووجود أقسام الإثبات الثلاثة،
وحل الروابط النسبية. الأمر المنفذ:

```bash
python3 - <<'PY'
from pathlib import Path
import re
root = Path('/sdcard/NEXUS_LLM_WIKI')
protocols = root / 'model_protocols'
expected = {
    'README.md',
    '01_REASONING_LOOP.md',
    '02_SOURCE_ANALYSIS.md',
    '03_WRITING_PROTOCOL.md',
    '04_REVIEW_AND_CORRECTION.md',
    '05_TASK_EXECUTION_AND_REPORTING.md',
}
actual = {p.name for p in protocols.iterdir() if p.is_file()}
assert actual == expected
required = ['## ما يثبت الإجراء', '## ما لا يثبته الإجراء', '## ما يجب تسجيله']
for path in protocols.glob('*.md'):
    text = path.read_text(encoding='utf-8')
    assert all(section in text for section in required)
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        if target.startswith(('http://', 'https://', '#')):
            continue
        assert (path.parent / target).resolve().is_file(), (path, target)
print('PASS')
PY
```

النتيجة الفعلية للأمر المرفق:

```text
PASS
```

كما أظهر الفحص التشخيصي التفصيلي المنفذ قبل كتابة التقرير:

```text
exact_protocol_file_set= True
01_REASONING_LOOP.md: required_sections=True
02_SOURCE_ANALYSIS.md: required_sections=True
03_WRITING_PROTOCOL.md: required_sections=True
04_REVIEW_AND_CORRECTION.md: required_sections=True
05_TASK_EXECUTION_AND_REPORTING.md: required_sections=True
README.md: required_sections=True
all_required_sections= True
all_relative_links_resolve= True
```

ومن بين الروابط التي حُلَّت بنجاح، روابط systems التالية:

- `systems/11_AGENT_EXECUTION_CONTRACT.md`
- `systems/16_SEQUENTIAL_AGENT_ORCHESTRATION.md`
- `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md`
- `systems/08_SALES_OPINION_PLURALISM.md`
- `systems/15_DOMAIN_COMPLETION_GATES.md`
- `systems/17_FOLDER_INDEX_CONTRACT.md`

## ما يثبت الإجراء

يثبت هذا التقرير أن الملفات المطلوبة أُنشئت في المسار المصرح به، وأنها قُرئت بعد
الكتابة، وأن الأقسام المطلوبة والروابط النسبية اجتازت الفحص المذكور.

## ما لا يثبته الإجراء

لا يثبت التقرير تشغيل دورة مصادر، أو صحة كل ادعاء في المصادر، أو اجتياز
`wiki_quality.py`، أو إغلاق بوابات `R/T/C/K/M/QA`، أو اعتماد أي Master.

## ما يجب تسجيله

يجب أن يسجل أي تسليم لاحق مسارات الملفات، ونسخة البروتوكولات المقروءة، وأوامر فحص
الروابط والأقسام ونتائجها، والملف المفقود `systems/20_WIKI_OPERATING_SYSTEM.md`، وأي
فحص أو بوابة لم تُنفذ بدل وصف المهمة بأنها مكتملة خارج نطاقها.

## الاختبارات غير المنفذة والقيود

- لم يُشغّل `tools/wiki_quality.py` لأن المخرجات هنا وثائق بروتوكول Markdown وليست
  سجلات Source/Claim/Concept/Master جديدة، ولأن طلب المهمة حصر التحقق بعد الكتابة في
  قراءة الملفات وفحص روابط systems والمسارات ذات الصلة.
- لم يُنشأ أو يُعدّل `systems/20_WIKI_OPERATING_SYSTEM.md` لأن الملف غير موجود ولم
  تكن هناك صلاحية لإنشاء عقد داخل `systems/`.
- لا توجد تغييرات معرفية في `raw/` أو طبقات Claims/Concepts/Masters نتيجة هذه المهمة.

## تسليم العامل

النتيجة المسلّمة: **مخرجات البروتوكولات مكتملة ضمن نطاق الملفات المصرح بها، وفحص
البنية والروابط المنفذ PASS**. هذا حكم على مخرجات هذه المهمة فقط، وليس قرار القائد
بشأن حالة الويكي العامة أو انتقال أي مجال.
