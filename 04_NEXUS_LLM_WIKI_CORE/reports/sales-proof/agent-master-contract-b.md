# تقرير Worker — إصلاح عقد الـMaster

التاريخ: 2026-10-09

## النطاق

قُرئت الملفات الأربعة كاملة قبل التعديل:

- `/sdcard/NEXUS_LLM_WIKI/masters/MASTER_ARCHITECTURE.md`
- `/sdcard/NEXUS_LLM_WIKI/masters/INDEX.md`
- `/sdcard/NEXUS_LLM_WIKI/systems/04_MASTER_AUTHORING.md`
- `/sdcard/NEXUS_LLM_WIKI/systems/10_SALES_MASTER_GATE.md`

اقتصر التعديل على التناقضات البنيوية الواضحة في عقد الـMaster: إبقاء الفجوات
ظاهرة، فصل Navigation عن الكتب، توحيد حالات `draft`/`reviewed`/`canonical`،
وربط القبول بسجل الأدلة واختبار الاسترجاع. لم تُضف معرفة مبيعات، ولم تُعدّل
أي ملفات تحت `raw/` أو `claims/` أو `concepts/`.

## diff المنفذ

### `masters/MASTER_ARCHITECTURE.md`

- وُحّدت حالات سجل الـMaster إلى `draft` و`reviewed` و`canonical` و`deprecated`.
- ثُبّت أن `reviewed` يسبق M5، وأن `canonical` لا يصدر إلا بعد M0–M5، بما فيه
  فحص الأدلة والاسترجاع، مع قرار اعتماد صريح.
- سُجل أن `accept_experimental` قرار تقرير لا حالة سجل، ولا يرفع Master إلى
  `canonical`.
- حُفظت قاعدة **إظهار الفجوات** ودُمجت مع قاعدة الحالة الموحدة في دورة البناء.

### `masters/INDEX.md`

- أزيل صف `M_SALES_NAVIGATION` من جدول الكتب المخططة؛ وأضيفت فقرة صريحة بأن
  `INDEX.md` هو Navigation artifact وليس كتابًا ولا يملك عقد Master أو حالة
  اعتماد.
- صُححت حالة الماستر الموجود من `draft/foundation` إلى `draft` حتى تطابق عقد
  الـschema؛ بقيت ملاحظة `foundation` وصفًا لا قيمة حالة.
- وُحّدت قاعدة الحالة: `planned` تسمية تخطيطية وليست status، و`canonical` يتطلب
  M0–M5 وسلامة الأدلة ومقارنة استرجاع مطابقة وقرار اعتماد.

### `systems/04_MASTER_AUTHORING.md`

- أضيفت نفس قائمة الحالات ومعنى `draft`/`reviewed`، مع حجز `canonical` لما بعد
  M0–M5 وفحص الأدلة والاسترجاع والاعتماد الصريح.
- ثُبّت أن المقارنة تكون بخط أساس ثابت وبنفس مجموعة الأسئلة وإعدادات القياس.
- صِيغت قاعدة التقرير بحيث لا يرفع الحالة تلقائيًا إلى `canonical`، ولا يغيّر
  `accept_experimental` حالة السجل، مع إبقاء الفجوات مرئية.

### `systems/10_SALES_MASTER_GATE.md`

- فُصل قرار `accept_experimental` عن `status` في العقد.
- شددت M1 على قابلية حل وفحص `quote/locator/hash/scope` وعلى عدم القبول بلا
  سجل دليل قابل لإعادة الفحص.
- شددت M5 على نفس مجموعة الاختبارات وإعدادات القياس وعلى عدم القبول بلا نتيجة
  استرجاع قابلة لإعادة الفحص.
- وحّدت M6 الانتقال: `draft` قبل اكتمال الفحص، `reviewed` بعد M0–M4، و`canonical`
  فقط بعد M0–M5 واعتماد المسؤول.

## بصمات الملفات

| الملف | SHA-256 قبل | SHA-256 بعد |
|---|---|---|
| `masters/MASTER_ARCHITECTURE.md` | `6b075b6f4b4c634c3c9a94396391058f27b1a2cb5fcf4b0baff045e6dd5580de` | `9ba2c919fdc0fefae41463a55cac54959528c7e972ee95ffac334d84ecdadece` |
| `masters/INDEX.md` | `f3c0995fedbb9d54f20169118237383f2b958a49ed5d87bd88f0269f7d8193e8` | `fb5af5aa6ad955d45b725a4f49f6338ba01b95a6904a2ed5662588737de3715a` |
| `systems/04_MASTER_AUTHORING.md` | `a5b0584eafc5d31f36139d283f8a0282544aee8c5f2054995d80b629d62561e7` | `582e90253f33ed9b81bf572fa2620a08acdf194c907453b76c49436faceeafd3` |
| `systems/10_SALES_MASTER_GATE.md` | `f15897d49c688b4c6aff236deb575b4bc8f579c4719f54241834a965672bc831` | `cead81bbc72ecae6a3c2b2a8ba10a84dac46fb6cf456bdce724b62dce76a23ad` |

## التحقق

### `wiki_quality.py --json`

الأمر:

```bash
python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py \
  --vault /sdcard/NEXUS_LLM_WIKI --json
```

النتيجة: `ok: true`، و`errors: []`، مع:

- `sources`: 1781 (`quarantined=9`, `processed=1772`)
- `claims`: 1777 (`reviewed=93`, `candidate=1684`)
- `concepts`: 34 (`reviewed=27`, `draft=7`)
- `masters`: 1 (`draft=1`)

### فحوص العقد

شُغّل فحص قراءة فقط للتحقق من أن:

- `M_SALES_NAVIGATION` غير موجود داخل جدول كتب المبيعات المخططة.
- الحالة المركبة `draft/foundation` أزيلت من الفهرس.
- نصوص الفجوات، `M0–M5`، الأدلة، والاسترجاع موجودة في الوثائق البنيوية.

النتيجة: `master_contract_checks=PASS`.

كما شُغّل:

```bash
python3 -m py_compile /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py
```

والنتيجة ناجحة، ثم أعاد `lsp_diagnostics` للمشروع: `No diagnostics found. All
clean!`.

## الحكم

تم إصلاح عقد الـMaster في الملفات الأربعة فقط. لا يعني ذلك اعتماد أي Master
حاليًا؛ نتيجة الجودة العامة `PASS` تخص ما يفحصه المدقق، وحالة الـMaster الفعلية
ما زالت `draft` كما يثبت جدول الفهرس ومخرج `wiki_quality.py`.
