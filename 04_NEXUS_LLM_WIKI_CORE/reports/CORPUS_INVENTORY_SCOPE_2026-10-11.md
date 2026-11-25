# جرد نطاق corpus على القرص

## الحالة والنطاق

- **نوع العملية:** جرد قراءة فقط؛ لم تُعدّل ملفات المصدر أو تُنقل أو تُعاد تسميتها أو تُحذف.
- **ملف التقرير الوحيد المكتوب:** `/sdcard/NEXUS_LLM_WIKI/reports/CORPUS_INVENTORY_SCOPE_2026-10-11.md`.
- **وقت القياس الفعلي (UTC):** `2026-10-13T05:38:49.780729Z`.
- **المسارات المجردة:** المسارات الستة المحددة في الطلب فقط، مع كل الأدلة الفرعية داخل كل مسار.
- **حدود الدلالة:** هذا جرد للقرص، وليس قراءة معرفية أو dedup أو route أو تسجيل هوية/بصمة مصدر، ولا يعلن اكتمال أي domain.

قُرئت قبل الجرد وثيقة نطاق corpus المطلوبة، وتعليمات المشروع التي تفرق بين `raw/` immutable، والنسخ القديمة/المرجعية، وطبقات الويكي والمخرجات. ووفقًا لذلك، فإن `raw/legacy/*` نسخ مراجعة خام، و`/sdcard/Nexus_Brain/brain/` مصدر قديم/مرجعي خارج مشروع الويكي الجديد، بينما `nexus_vault/` طبقة ويكي نشطة ومخرجاتها وأدواتها.

## منهجية العد

1. عُدّت الملفات النظامية العادية (regular files) عوديًا، بما فيها الملفات المخفية وكل الملفات داخل الأدلة الفرعية.
2. الحجم هو مجموع `st_size` بالبايت لكل ملف معدود؛ لم تُحتسب أحجام الأدلة نفسها.
3. عُدّت الامتدادات بحروف صغيرة من اللاحقة الأخيرة لاسم الملف؛ `[بدون امتداد]` تعني عدم وجود لاحقة.
4. لم تُتبع الروابط الرمزية. لم توجد روابط رمزية أو أخطاء قراءة في أي مسار من المسارات الستة وقت القياس.
5. عُدّ الملف Manifest إذا احتوى اسم ملفه، بحساسية غير معتبرة لحالة الأحرف، على الكلمة `manifest`؛ ثم سُجل مساره النسبي وحجمه.

## ملخص المسارات

| التصنيف | المسار | موجود؟ | النوع | عدد الملفات | إجمالي الحجم (بايت) | تقريبًا MiB |
|---|---|---:|---|---:|---:|---:|
| مصدر خام جديد | `/sdcard/NEXUS_LLM_WIKI/raw/new/` | نعم | دليل | 1,776 | 43,757,343 | 41.730 |
| مصدر خام — نسخة مراجعة قديمة | `/sdcard/NEXUS_LLM_WIKI/raw/legacy/brain/` | نعم | دليل | 0 | 0 | 0.000 |
| مصدر خام — نسخ مراجعة للمحادثات | `/sdcard/NEXUS_LLM_WIKI/raw/legacy/chats/` | نعم | دليل | 39 | 6,148,975 | 5.864 |
| مصدر خام — سياق | `/sdcard/NEXUS_LLM_WIKI/raw/context/` | نعم | دليل | 3 | 252,610 | 0.241 |
| مصدر قديم/مرجعي أصلي | `/sdcard/Nexus_Brain/brain/` | نعم | دليل | 564 | 19,680,572 | 18.769 |
| مخرجات/ويكي نشطة وأدواتها | `/sdcard/Nexus_Brain/nexus_vault/` | نعم | دليل | 159 | 24,885,393 | 23.733 |

### إجماليات حسب الطبقة

| الطبقة | المسارات الداخلة | الملفات | الحجم (بايت) | تقريبًا MiB |
|---|---|---:|---:|---:|
| المصادر الخام في مشروع `NEXUS_LLM_WIKI` | `raw/new`، `raw/legacy/brain`، `raw/legacy/chats`، `raw/context` | 1,818 | 50,158,928 | 47.835 |
| المصدر القديم/المرجعي | `Nexus_Brain/brain` | 564 | 19,680,572 | 18.769 |
| المخرجات/الويكي النشطة | `Nexus_Brain/nexus_vault` | 159 | 24,885,393 | 23.733 |
| **كل المسارات الستة** | — | **2,541** | **94,724,893** | **90.337** |

## تفصيل الامتدادات

الأرقام في الخلايا بصيغة: **عدد الملفات / الحجم بالبايت**.

| المسار | الامتدادات الموجودة |
|---|---|
| `/sdcard/NEXUS_LLM_WIKI/raw/new/` | `.txt`: 1,772 / 43,677,800؛ `.srt`: 1 / 42,748؛ `.md`: 3 / 36,795 |
| `/sdcard/NEXUS_LLM_WIKI/raw/legacy/brain/` | لا توجد ملفات |
| `/sdcard/NEXUS_LLM_WIKI/raw/legacy/chats/` | `.md`: 30 / 4,063,458؛ `.txt`: 7 / 999,190؛ `.zip`: 2 / 1,086,327 |
| `/sdcard/NEXUS_LLM_WIKI/raw/context/` | `.txt`: 2 / 240,489؛ `.md`: 1 / 12,121 |
| `/sdcard/Nexus_Brain/brain/` | `.txt`: 560 / 19,601,029؛ `.srt`: 1 / 42,748؛ `.md`: 3 / 36,795 |
| `/sdcard/Nexus_Brain/nexus_vault/` | `.md`: 114 / 10,849,016؛ `.js`: 5 / 7,801,839؛ `.css`: 9 / 5,842,361؛ `.json`: 25 / 292,537؛ `.py`: 3 / 67,760؛ `.pyc`: 1 / 31,878؛ `.canvas`: 1 / 2؛ `[بدون امتداد]`: 1 / 0 |

## جرد Manifest

وُجدت **11 ملفات Manifest** في المسارات الستة كلها؛ جميعها داخل `nexus_vault/`. لم يوجد ملف يحمل `manifest` في أي من مسارات المصادر الخام الأربعة أو في `/sdcard/Nexus_Brain/brain/`.

| المسار النسبي داخل `nexus_vault/` | الحجم (بايت) | الملاحظة التصنيفية |
|---|---:|---|
| `.obsidian/plugins/obsidian-excalidraw-plugin/manifest.json` | 463 | Manifest إضافة Obsidian |
| `.obsidian/plugins/obsidian-mind-map/manifest.json` | 194 | Manifest إضافة Obsidian |
| `.obsidian/plugins/obsidian-tasks-plugin/manifest.json` | 517 | Manifest إضافة Obsidian |
| `.obsidian/plugins/omnisearch/manifest.json` | 366 | Manifest إضافة Obsidian |
| `.obsidian/plugins/templater-obsidian/manifest.json` | 756 | Manifest إضافة Obsidian |
| `.obsidian/themes/Minimal/manifest.json` | 199 | Manifest سمة Obsidian |
| `.obsidian/themes/Obuntu/manifest.json` | 110 | Manifest سمة Obsidian |
| `.obsidian/themes/Things/manifest.json` | 151 | Manifest سمة Obsidian |
| `.obsidian/themes/Wasp/manifest.json` | 139 | Manifest سمة Obsidian |
| `.obsidian/themes/Willemstad/manifest.json` | 136 | Manifest سمة Obsidian |
| `_master_manifest_clean.json` | 84,461 | Manifest مشروع/ماستر داخل vault |

## الفصل بين الطبقات

### 1. المصادر الخام

المسارات الأربعة تحت `/sdcard/NEXUS_LLM_WIKI/raw/` هي طبقة المصدر الخام immutable بحسب تعليمات المشروع. `raw/new/` هو صندوق المصادر الجديدة، و`raw/legacy/brain/` و`raw/legacy/chats/` نسخ مراجعة، و`raw/context/` يحتوي سياقًا خامًا. مسار `raw/legacy/brain/` **موجود لكنه فارغ من الملفات العادية** وقت القياس؛ وجود أدلته الفرعية لا يضيف ملفات إلى العدد.

### 2. الويكي/المصادر القديمة المرجعية

`/sdcard/Nexus_Brain/brain/` خارج جذر `NEXUS_LLM_WIKI` ويحتوي 564 ملفًا من مواد قديمة (مع أدلة `duplicates/` و`processed/` ضمن الجرد). عومل هنا كمصدر قديم/مرجعي أصلي، لا كطبقة مخرجات جديدة. لم يُجرد المسار الآخر `/sdcard/Nexus_Brain/Nexus_Brain/` لأن الطلب حدد `brain/` و`nexus_vault/` فقط.

### 3. المخرجات

`/sdcard/Nexus_Brain/nexus_vault/` يحتوي 159 ملفًا مشتقًا/تشغيليًا للويكي النشطة، منها Markdown وJSON وفهارس/ماسترز، إضافة إلى CSS/JS/Python وملفات حالة وملفات Obsidian. يشمل العدد كل ما هو موجود فعليًا تحت المسار وقت القياس، بما في ذلك الأدلة المخفية و`_archive/` و`__pycache__/`؛ لا يعني وجود هذه الملفات أن كل محتوى الويكي مصدر نشط أو أن أي domain مكتمل. لا تُعامل `_archive/` كمصدر نشط.

## ملاحظات وحدود

- الجرد لم يقرأ محتوى كل ملف ولم يتحقق من صحة JSON أو البصمات أو التطابق البايتي أو التكرار.
- لم تُستخرج Terms أو Claims أو Concepts أو Masters، ولم يُنفذ route أو dedup أو أي معالجة معرفية.
- لم تُحتسب الأدلة أو المجلدات كملفات، ولم تُتبع الروابط الرمزية؛ القياس سجل صفر روابط رمزية وصفر أخطاء قراءة.
- الأرقام لقطة قرص في وقت القياس المذكور، وليست سجلًا ثابتًا لحالة مستقبلية.
- هذا التقرير لا يثبت `source_done` أو `domain_done` ولا يعلن اكتمال أي مجال.
