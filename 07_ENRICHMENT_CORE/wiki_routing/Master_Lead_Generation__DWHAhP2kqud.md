---
target_master: Master_Lead_Generation.md
source_shortcode: DWHAhP2kqud
index_format: table2
next_row: n/a (الفهرس غير مرقّم — max_row = 0، تُلحق الصفوف بلا أرقام)
concepts: 2
applied: false
---

## صفوف الفهرس المقترحة

| [[Concept_Queue_Builder_Filter_Logic]] | خمس قواعد فلترة تفرز الليدز إلى طابورَي InMail وConnection بـ regex على المسمّى الوظيفي |
| [[Concept_Lead_Queue_Schema]] | بنية جدول الليدز: تبويبات وأعمدة ومعرّفات طابور بصيغة im_/cn_YYYYMMDD_NNN |

## المفاهيم الكاملة

### Concept_Queue_Builder_Filter_Logic — منطق فرز الليدز: خمس قواعد وregex صانع القرار

مصدره الشريحة 5 من كاروسيل «HOW TO GET UNLIMITED LEADS using LinkedIn + Claude Code»، وتحديداً **برومبت Claude Code الظاهر كاملاً على الشاشة** لبناء `linkedin_queue_builder.py` — سكربت يقرأ الليدز من تبويب مصدر في Google Sheet ويملأ طابورَين.

**قواعد الفلترة الخمس كما وردت مرقّمة حرفياً:**

1. **`Must have email (for deduplication)`** — لا بد من وجود إيميل. وسببه المعلن ليس التواصل بل **إزالة التكرار**: الإيميل هو المفتاح الفريد للـ dedupe، لا رابط LinkedIn.
2. **`Must have LinkedIn URL containing "linkedin.com"`** — لا بد أن يحتوي الرابط على النطاق نفسه (فحص وجود لا فحص صحة).
3. **`Not already in the target queue (dedupe by email)`** — ألا يكون موجوداً سلفاً في **الطابور الهدف** تحديداً، والمقارنة بالإيميل.
4. **`If mode is "inmail" — must be a decision-maker`** بمطابقة المسمّى الوظيفي على أنماط regex. **القائمة الحرفية الكاملة:** `owner` · `president` · `ceo` · `chief executive` · `founder` · `partner` · `general manager` · `gm` · `dealer principal` · `vp` · `vice president` · `director`.
5. **`All others go to Connection Queue as Priority 2 (bulk)`** — كل من سواهم يذهب إلى طابور التواصل بأولوية ثانية.

**الفكرة المعمارية الجوهرية:** الفرز ليس «مؤهّل / غير مؤهّل» بل **توجيه إلى قناتين بكلفتين مختلفتين**. صاحب القرار يستحق رسالة InMail المكلفة والمخصّصة؛ ومن دونه لا يُرمى بل يُحوَّل إلى طلب تواصل جماعي رخيص (`bulk`). هذا يمنع إهدار الرصيد المكلف على غير صانع القرار، ويمنع في الوقت نفسه فقدان الليد كلياً.

**دلالة قائمة الـregex:** وجود `dealer principal` (مسمّى خاص بوكالات السيارات) و`general manager`/`gm` يكشف أن القائمة **مضبوطة على قطاع بعينه** لا عامّة. وهذا نفسه الدرس القابل للنقل: قائمة صانعي القرار **تُكتب لكل نيتش على حدة**، ونسخها كما هي إلى قطاع آخر يفرز خطأ.

**واجهة سطر الأوامر كما وردت حرفياً — وهي جزء من التصميم لا تفصيل تقني:**
- `--mode inmail|connect` — أي طابور يُملأ.
- `--source "Tab Name"` — تبويب المصدر.
- `--limit N` — الحدّ الأقصى من الليدز، **الافتراضي 100**.
- `--dry-run` — معاينة بلا كتابة.
- `--status` — عرض أعماق الطوابير وتحليل المصادر.

وجود `--dry-run` و`--status` قبل التشغيل الحقيقي هو ما يفصل نظاماً تشغيلياً عن سكربت: **تعاين قبل أن تكتب، وتقيس عمق الطابور قبل أن تضيف.**

**تحفّظات أمانة:**
- **الأولوية 1 لا يُصرَّح بمصدرها في قواعد الفلترة الخمس** — تظهر فقط في مسار آخر (ردّ الإيميل البارد المصنَّف يُضاف إلى `Queue P1`). أي أن P1 محجوزة للِيد الدافئ لا لصانع القرار البارد. هذا استنتاج من تجاور شريحتين، ولا نص يجمعهما.
- قاعدة 2 تفحص وجود السلسلة `linkedin.com` فقط، **ولا تتحقق من صحة الملف الشخصي ولا من كونه حياً**.
- **لا رقم أداء لأي قاعدة:** لا نسبة قبول اتصال، لا معدّل رد InMail، لا كم ليد مرّ من كم. المنشور يصف التصميم لا نتائجه.
- الشرائح المقروءة 00–06 من 12، فبقية النظام (التشغيل الفعلي والمتصفح الوكيل) **غير مرئية**.

المصدر: DWHAhP2kqud.

### Concept_Lead_Queue_Schema — مخطّط جدول الليدز: أربعة تبويبات وأعمدة مسمّاة ومعرّفات مؤرّخة

نفس المصدر (الشريحة 5). التعليمة الافتتاحية: `Open Claude Code → paste the spreadsheet prompt`، وClaude يبني **أربعة تبويبات**: `Sample Leads` · `Blacklist` · `InMail Queue` · `Connection Queue`. ثم: `Replace sample leads with your real list.`

**بنية التبويبات كما وردت حرفياً:**

- **تبويب المصدر `Sample Leads`** بأعمدة محدَّدة بحرف العمود: `first_name (B)` · `last_name (C)` · `email (D)` · `job_title (E)` · `company_name (F)` · `website (G)` · `linkedin_url (I)`.
- **تبويب `InMail Queue`:** `queue_id` · `added_at` · `first_name` · `last_name` · `email` · `company_name` · `job_title` · `linkedin_url` · `source_tab` · `status` · `processed_at` · `message_sent` · `notes`.
- **تبويب `Connection Queue`:** `queue_id` · `added_at` · `priority` · `classification` · `first_name` · `last_name` · `email` · `company_name` · `job_title` · `linkedin_url` · `email_context` · `status` · `processed_at` · `message_sent` · `notes`.

**الفرق الجوهري بين الطابورين هو ثلاثة أعمدة زائدة في Connection Queue: `priority` و`classification` و`email_context`.** وهذه الثلاثة هي بالضبط ما يجعل الطابور قابلاً لاستقبال الليد الدافئ العائد من ردّ الإيميل: الأولوية تُقدّمه، والتصنيف يحمل درجة حرارته، و`email_context` يحمل نصّ سياق الرد ليُستخدم في تخصيص الرسالة. أي أن **بنية الجدول هي التي تسمح بالتخصيص لاحقاً** — لا يمكن أن يخصّص النظام ما لم يخزّنه العمود.

**صيغة معرّفات الطابور حرفياً:** `im_YYYYMMDD_001 for InMail, cn_YYYYMMDD_001 for Connection. Status starts as "pending".`
المعرّف يحمل بادئة القناة + تاريخ اليوم + تسلسلاً، فهو **قابل للفرز والتتبّع زمنياً بلا جدول إضافي**، والحالة الابتدائية موحّدة `pending`.

**أعمدة دورة الحياة الثلاثة المتكرّرة في الطابورين:** `status` · `processed_at` · `message_sent` — وهي ما يحوّل الجدول من قائمة إلى **آلة حالات**: ما وضعه الآن، متى عولج، وما نصّ ما أُرسل فعلاً. عمود `message_sent` تحديداً هو ما يمكّن مراجعة ما أُرسل لاحقاً ونسبه إلى النتيجة.

**تبويب `Blacklist`** موجود ضمن الأربعة، وهو الحارس ضد التواصل مع من يجب استثناؤه.

**تحفّظات أمانة:**
- **أعمدة تبويب `Blacklist` غير معروضة إطلاقاً**، ولا كيفية فحصها في منطق الفلترة — القواعد الخمس **لا تذكر Blacklist** رغم وجود التبويب. فجوة صريحة في المصدر لم أملأها.
- أعمدة المصدر تقفز من `(G)` إلى `(I)` — العمود `H` غير مذكور، ولا تفسير في الصورة.
- **المصادقة كما وردت:** `Google Sheets auth: Use google.oauth2.credentials.Credentials from token.json with spreadsheets scope.` — الاسم فقط، بلا شرح إنشاء `token.json`.
- لا حجم أقصى للجدول ولا ذكر لحدود Google Sheets عند التوسّع.

المصدر: DWHAhP2kqud.

## ملاحظات أمانة على هذا الـ patch
- فهرس هذا الماستر جدول عمودين بصيغة `| [[Concept_X]] | وصف قصير |` **غير مرقّم** (`max_row = 0`)، فالصفوف تُلحق بلا أرقام.
- **قرار التفتيت:** فصلتُ منطق الفلترة عن مخطّط الجدول لأنهما وحدتان مستقلتان قابلتان للتطبيق كلٌّ على حدة (يمكن تبنّي المخطّط بمنطق فرز آخر، والعكس). ولم أُنشئ مفهوماً لكل عمود.
- بقية شرائح هذا المنشور في patches منفصلة لنفس الشورت كود (`Master_Outreach_Mechanics`، `Master_AI_And_Automation`، `Master_Systems_And_Workflow`).
