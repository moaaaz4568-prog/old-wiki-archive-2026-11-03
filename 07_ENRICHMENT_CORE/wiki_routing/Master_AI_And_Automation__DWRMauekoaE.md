---
target_master: Master_AI_And_Automation.md
source_shortcode: DWRMauekoaE
index_format: bullet
next_row: 40
concepts: 4
applied: false
---

## صفوف الفهرس المقترحة

40. [[Concept_Marketing_Team_Five_Skills]] — تفكيك فريق التسويق إلى خمس مهارات Claude كل واحدة تلعب دور موظف: بحث، محتوى، تصميم، بيانات، عرض
41. [[Concept_SOP_To_Skill_Conversion]] — لا تخترع الإجراء: انسخ إجراءك القائم من Notion/Docs وحوّله إلى ملف مهارة موصولة بأداة بحث
42. [[Concept_Skill_Context_Gate_And_Tool_Fallback]] — تعليمتان إلزاميتان داخل كل مهارة: تحقّق من ملفات السياق واسأل قبل البدء، وحدّد أداة أساسية مع بديل عند غيابها
43. [[Concept_Skills_Packaged_As_Plugin]] — تغليف مهارات `.claude/skills/` في إضافة واحدة قابلة لإعادة الاستخدام مع أمر مائل مخصّص

## المفاهيم الكاملة

### Concept_Marketing_Team_Five_Skills — فريق تسويق من خمس مهارات: تقسيم الأدوار بدل مطالبة عامة

الفكرة المركزية للكاروسيل (11 شريحة صامتة، لا فيديو ولا صوت): بدل مطالبات متفرّقة في كل مرة، تُحوَّل إجراءات العمل التي تتبعها **أصلاً** إلى خمس مهارات (Claude Skills)، كل واحدة تلعب دور موظف مستقل في فريق تسويق.

**الأسماء كما وردت حرفياً في شريحة الغلاف:**
`marketing-research` — `social-content` — `creative-designer` — `data-analysis` — `campaign-presenter`.

**دور كل واحدة كما شُرح في شريحته:**

1. **Marketing research** — يأخذ إجراء البحث الذي تتّبعه فعلاً ويُشغّله على أي علامة تجارية، موصولاً بأداة بحث ويب.
2. **Social content** — يقرأ أفضل 10 منشورات أداءً لديك + إطار كتابتك (الخطّافات، القصص، نداءات الفعل) فيكتب بطريقتك أنت لا بطريقة عامة.
3. **Creative designer** — أداة توليد صور + ألوان العلامة وخطوطها وأسلوبها **كإعدادات افتراضية**، فيكفي بعدها «اصنع لي جرافيك عن كذا» بلا أخذ ورد ولا موجز تصميم.
4. **Data analysis** — يُسقَط عليه جدول بيانات الحملة فيبني لوحة معلومات بألوان العلامة، برسوم تفاعلية وتفصيل حسب القناة.
5. **Campaign presenter** — يأخذ مخرجات مهارتَي البحث والبيانات ويحوّلها إلى عرض شرائح متوافق مع العلامة جاهزاً للإرسال.

**القاعدة القابلة للاختبار:** المهارة الواحدة = دور وظيفي واحد بمخرَج واحد قابل للتسليم. المعيار العملي لتقسيم مهاراتك: لو كنت ستوظّف بشراً لهذه المهمة، هل ستكون وظيفة مستقلة؟ إن نعم فهي مهارة مستقلة.

**نقطة التكامل التي تُبرّر التقسيم:** بعد بناء الخمس، **تُعطى مهمة واحدة فيختار Claude المهارات المناسبة ويشغّلها معاً ويسلّم كل شيء دفعة واحدة** ("it picks the right skills, runs them together, and delivers everything in one go"). أي أن قيمة التفكيك ليست في استدعاء كل مهارة يدوياً بل في أن التوجيه بينها يصبح تلقائياً.

**مسار التخزين الظاهر من لقطة الشاشة:** `<المشروع>/.claude/skills/<اسم-المهارة>/` — استُخرج من مسارات أدوات `Read` و`Glob` الظاهرة في شريحة المهارة الرابعة:
`/Users/demo/Documents/Projects/Simple Home/.claude/skills/marketing-research-strategy/references…`

المصدر: DWRMauekoaE.

---

### Concept_SOP_To_Skill_Conversion — لا تخترع الإجراء: انسخه من مكانه القائم وحوّله

أوضح مبدأ في المنشور وأكثره قابلية للنقل، وقيل صراحةً في شريحتين متتاليتين:

- **للبحث:** "Go to your google docs or notion. Find the research process you already follow. Copy it." ثم "Paste that process into a claude skill file. connect perplexity so it can search the web. that's it. Your research assistant is ready."
- **للمحتوى:** "Go find your last 10 best performing posts. The ones that actually got engagement. Save them in a folder." ثم "Add your writing framework how you structure hooks, stories, CTAs."

**المبدأ:** مادة المهارة موجودة سلفاً في عملك — إجراء مكتوب (SOP) أو أعمال سابقة ناجحة. دور النموذج **استخلاص النمط لا اختراعه**. المطالبة المعروضة للمحتوى تقولها بوضوح: اقرأ الأمثلة في `/examples/`، **حلّل الأنماط وما يجعل هذه المنشورات تنجح** (الخطّافات، البُنى، أنماط السرد)، **ثم** أنشئ المهارة.

**البنية التنظيمية المرئية (شريحة Notion):** مساحة فيها شجرة جانبية `Skills` وتحتها `Content`, `Design`, `Marketing Research`, `Brand`, `Growth Projects`, `Systems`. صفحة `Marketing Research` خاصيتها `Type: Skill`، وداخلها قائمة مهام: `Customer research` (غير مؤشَّر) و`Competitor research` (مؤشَّر). أي أن الإجراء موثّق كصفحة مصنّفة قبل أن يصير مهارة.

**المسارات الحرفية المستخدمة كمدخلات:** `/sop/` لوثائق الإجراء، `/examples/` لأمثلة المحتوى وأطر السرد، `/quarterly-review/` لمخرجات المراجعة الربعية.

**الأرقام كما ظهرت:** شريحة المحتوى تعرض ثلاث مصغّرات منشورات بأرقام مشاهدات 30.5K و1M (مؤطَّرة بالأصفر) و575K — أي أن معيار «الأفضل أداءً» عندها بصري لا محسوب بمعادلة معلنة.

المصدر: DWRMauekoaE.

---

### Concept_Skill_Context_Gate_And_Tool_Fallback — بوّابة السياق وبديل الأداة: تعليمتان تُكتبان داخل كل مهارة

أعلى نصوص المنشور قيمة هندسية، وهو مربّع `IMPORTANT` الحرفي داخل مطالبة بناء مهارة البحث:

> "IMPORTANT: - Before starting, check if there are relevant brand context files given. If key context is missing, ask the user focused questions before starting the task. - Follow the exact step outlined in the SOP. Use the Perplexity MCP tool as the primary research tool. If it is not available, fall back to any other available search tools."

**ثلاث قواعد مستخرجة قابلة للتطبيق على أي مهارة:**

1. **بوّابة السياق:** تحقّق من وجود ملفات سياق العلامة **قبل البدء**، وإن نقص سياق جوهري **اسأل أسئلة مركّزة** بدل التوليد على فراغ. هذه هي الحاجز بين مخرَج مخصّص ومخرَج عام.
2. **الالتزام الحرفي بالإجراء:** "Follow the exact step outlined in the SOP" — المهارة تنفّذ الإجراء الموثّق لا نسخة النموذج المُعاد صياغتها منه.
3. **أداة أساسية + بديل معلن:** حدّد الأداة الأولى بالاسم (**Perplexity MCP**) وانصّ صراحةً على السقوط إلى أي أداة بحث متاحة عند غيابها. المهارة لا تتعطّل بغياب أداة واحدة.

**تكرار مستقل يؤكّد النمط:** مهارة المحتوى أيضاً تستخدم Perplexity MCP لكن لغرض مختلف — **إيجاد المحادثات الرائجة والمواضيع الساخنة** حول الموضوع المعطى. أي أن الأداة نفسها تُوظَّف بغرضين مختلفين حسب المهارة.

**قاعدة رابعة من مطالبة مهارة العرض:** "Now, outline your plan first before you execute the task" — **اعرض خطتك أولاً قبل التنفيذ**. وهذه تُقرن بنمط **التقسيم إلى مهام متوازية**: مراجعة ربعية قُسمت إلى 3 مهام (استراتيجية تسويق، تحليل أداء الحملة وبناء لوحة تفاعلية، ثم عرض استراتيجي **لا يزيد عن 10 شرائح** يلخّص نتائج البحث ورؤى البيانات) مع الحفظ في `/quarterly-review/`.

**بنية موجز التصميم كما ظهرت حرفياً** (نموذج قابل للنسخ لمهارة التصميم): موضوع + `Style` + `Layout` + `Colors`. مثالها:
`Create a Anatomy / Breakdown social media infographic about "What Makes the Perfect Bedsheet Set" / Style: Blueprint / Technical / Layout: Central Focus / Colors: Monochrome + accent using rich navy and burnished copper`

المصدر: DWRMauekoaE.

---

### Concept_Skills_Packaged_As_Plugin — التغليف: من مهارات متفرّقة إلى إضافة واحدة بأمر مائل

الخطوة الأخيرة بعد بناء الخمس، والمطالبة الحرفية:

> "Package all the custom skills in this project's .claude/skills/ folder into a resusable plugin called \"ai-marketing-skills\". Reference the official Plugin documentation for the correct format: https://code.claude.com/docs/en/plugins"
> "Also define a custom slash command called /landing-page that runs this workflow:" (مقطوع)

**العناصر الثلاثة للتغليف:**
1. **النطاق:** كل ما في `.claude/skills/` بالمشروع.
2. **الاسم:** `ai-marketing-skills` — إضافة واحدة قابلة لإعادة الاستخدام عبر مشاريع.
3. **مرجع الصيغة:** التوثيق الرسمي `https://code.claude.com/docs/en/plugins` — أي أن الصيغة تُقرأ من المصدر لا تُخمَّن.

**العنصر الرابع:** تعريف **أمر مائل مخصّص** (`/landing-page`) يشغّل سير عمل معيّن. أي أن الإضافة ليست مجرد حاوية مهارات بل تحمل أيضاً نقاط دخول مسمّاة لسيَر عمل مركّبة.

**تحفّظ:** تفاصيل سير عمل `/landing-page` **مقطوعة في الصورة** ولم أرها. أعرف أن الأمر عُرِّف، ولا أعرف ما الذي يفعله.

**عنصر بيئة مرئي:** في شريحة الاستخدام تظهر واجهة فيها اختيار النموذج `Opus 4.6`، وقائمة `Ask permissions`، ومشروع باسم `Simple Home`، ومؤشر `Local`.

المصدر: DWRMauekoaE.

## ملاحظات أمانة على هذا الـ patch

- **صيغة الفهرس:** قائمة نقطية مرقّمة. آخر رقم صف في الماستر 39 حسب القائمة المعطاة، فالأرقام هنا 40–43. لكن أُنشئت في نفس الدفعة patches أخرى لهذا الماستر (`DW23T4JkbYu` أخذ 40–42، `DWHAhP2kqud` أخذ 43–44، `DWOerZ6klVD` أخذ 45) — **إن طُبِّقت تلك أولاً فالأرقام هنا تبدأ من 46**. يلزم إعادة الترقيم بحسب ترتيب التطبيق الفعلي.
- **المطالبات مقصوصة:** صناديق المطالبات في الشرائح 2 و4 و9 مقصوصة من الأسفل والنص المتبقي غير مقروء — لم يُخمَّن.
- **تعارض داخل شريحة المهارة الرابعة:** النص يتحدث عن بناء لوحة معلومات من جدول بيانات، لكن لقطة الشاشة فوقه تُظهر **تحليلاً تنافسياً لعلامة `Quince`** ضمن استراتيجية بحث سوق لـ`Simple Home`. أثبتُّ الاثنين ولم أوفّق بينهما. مفهوم «لوحة المعلومات» لم يُفرَد كمفهوم مستقل لأن ما رأيته منه نصّ شريحة واحد بلا مخرَج مرئي.
- **ازدواج التسمية:** الغلاف يقول `marketing-research` و`social-content`، والمطالبات تسمّيهما `marketing-research-strategy` و`social-media-content`. لم أوحّدهما لأن كليهما ظهر فعلاً.
- **لماذا هذا الماستر:** المفاهيم الأربعة كلها **بنية أدوات AI وأتمتة سير عمل**، ومجال التسويق فيها مجرد مثال. لم أوجّهها إلى ماسترز المحتوى أو الاستراتيجية لأن القيمة المنقولة معمارية لا موضوعية.
