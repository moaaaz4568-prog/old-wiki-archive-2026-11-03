# تقرير قراءة مبيعات — Worker B

**التاريخ:** 2026-10-09

**الحالة:** Claims مرشحة فقط (`status: candidate`). لم تُرفع أي نتيجة إلى
`reviewed` أو `accepted`، ولم تُنشأ منها Concepts أو Masters.

## النطاق والضوابط

- قُرئ `/sdcard/NEXUS_LLM_WIKI/collections/sales/manifest.json` بعد فحص وجوده.
- اختيرت خمسة عناصر `strong` من `manifest.json`، وفُحص وجود كل مسار خام قبل
  قراءة محتواه.
- قُرئت الملفات الخام بترميز UTF-8، وحُسبت بصمة SHA-256 للبايتات وقورنت ببصمة
  الـmanifest. الاقتباسات أدناه من النص الخام حرفيًا، لا من الملخصات أو من
  Claims سابقة.
- محددات الموضع `chars [start,end)` هي إزاحات Unicode صفرية، والنهاية حصرية؛
  في `transcript_full (1).txt` أُضيف رقم السطر والإزاحة داخل السطر، وكذلك
  الإزاحة المطلقة داخل الملف.
- لم يُعدّل أي ملف تحت `raw/` أو `claims/` أو `concepts/` أو `masters/`؛ هذا
  التقرير هو ملف الكتابة الوحيد في نطاق هذه المهمة.

## المصادر الخمسة المقروءة

| # | `source_id` | المسار النسبي | البايتات | SHA-256 مطابق للـmanifest |
|---:|---|---|---:|---|
| 1 | `SRC_NEW_d4502be125612b86_78d08ff3` | `raw/new/sabonagy__How to Make +$100,000Mo with Cold Email, Calls, DMs & SMS (4 Hour SMMA Masterclass)__iHJLlKlKDhk.txt` | 268033 | نعم |
| 2 | `SRC_NEW_5b782973289bdb21_021e6961` | `raw/new/Build a $100k MRR Agency — 14-Hour Masterclass.txt` | 695086 | نعم |
| 3 | `SRC_NEW_129f7a12e3e9285b_b7e305cd` | `raw/new/aaronxshepherd__If you only watch one cold email video, make it this (4 hour masterclass)__LzGJ3MQParY.txt` | 275152 | نعم |
| 4 | `SRC_NEW_4338afb73c56fdd7_737c056d` | `raw/new/transcript_full (1).txt` | 758611 | نعم |
| 5 | `SRC_NEW_e42b416e46db75c3_237d0cba` | `raw/new/matthewlucero__How To Generate Leads With Cold Email in 2026 (FULL COURSE)__BakY-82NYVQ.txt` | 276215 | نعم |

## Claims المرشحة

### CAND_SALES_B_001

- **statement:** المصدر يصف «greatest acquisition system» بأنه يتكون من ست
  مراحل، ويقول إن كل مرحلة تعمل كنظام فرعي لتحسين التحويل في كل خطوة.
- **source_id:** `SRC_NEW_d4502be125612b86_78d08ff3`
- **locator:** `raw/new/sabonagy__How to Make +$100,000Mo with Cold Email, Calls, DMs & SMS (4 Hour SMMA Masterclass)__iHJLlKlKDhk.txt`, line 1, Unicode chars `[18061,18223)` (zero-based, end-exclusive).
- **evidence_quote:** "So, greatest acquisition system breaks down client acquisition into six fundamental stage. Each stage acts as a subsystem that optimizes conversion at every step."
- **evidence_type:** `direct_quote`
- **scope:** وصف إطار اكتساب عملاء داخل دورة SMMA؛ الاقتباس لا يحدد سوقًا أو حجم عينة أو فترة اختبار.
- **what_it_does_not_prove:** لا يثبت أن كل نظام مبيعات يحتاج ست مراحل، ولا يثبت أن هذا التقسيم يحسن التحويل فعليًا أو يسبب نتيجة قابلة للتعميم.
- **evidence_start:** `18061`
- **evidence_end:** `18223`
- **excerpt_sha256:** `e8f43c8f89e466a038fe773bf76324ce8768cf3e3ec1308ae62084a686e64ca6`
- **confidence:** `source_reported`
- **status:** `candidate`

### CAND_SALES_B_002

- **statement:** المصدر يذكر أن أسئلة التأهيل المسبق تتناول نوع النشاط، والإيراد، والهدف، وما يمنع بلوغ الهدف، وأن جمع هذه المعلومات يساعد على توفير الوقت والوصول إلى المشكلة.
- **source_id:** `SRC_NEW_d4502be125612b86_78d08ff3`
- **locator:** `raw/new/sabonagy__How to Make +$100,000Mo with Cold Email, Calls, DMs & SMS (4 Hour SMMA Masterclass)__iHJLlKlKDhk.txt`, line 1, Unicode chars `[5232,5500)` (zero-based, end-exclusive).
- **evidence_quote:** "So we ask for whether or not you know it's coach, agency, consultants, revenue, target revenue, what's stopping you from hitting the goal. And any type of information that could just save us a ton of time and get straight to the point and helping you fix those issues."
- **evidence_type:** `direct_quote`
- **scope:** أسئلة pre-qualification في سياق تسويق inbound أو outbound لوكالات ومدربين واستشاريين؛ الشروط التشغيلية التفصيلية غير مذكورة هنا.
- **what_it_does_not_prove:** لا يثبت أن هذه الأسئلة ترفع معدل الحجز أو الإغلاق، ولا يثبت أنها مناسبة لكل قطاع أو أن توفير الوقت تحقق بقياس مستقل.
- **evidence_start:** `5232`
- **evidence_end:** `5500`
- **excerpt_sha256:** `a07fa93ffd8b4c093cbc38b081d4108f767bd73952dedae7055c5252e648bf45`
- **confidence:** `source_reported`
- **status:** `candidate`

### CAND_SALES_B_003

- **statement:** المصدر يقول إن تعريف IAP وICP يوضح اختيار استراتيجية التسويق والوصول، ومن ينبغي قبوله أو رفضه كعميل، ويجعل المبيعات والتسويق «أكثر فعالية» بحسب المتحدث.
- **source_id:** `SRC_NEW_5b782973289bdb21_021e6961`
- **locator:** `raw/new/Build a $100k MRR Agency — 14-Hour Masterclass.txt`, line 1, Unicode chars `[361262,361655)` (zero-based, end-exclusive).
- **evidence_quote:** "So, once you've defined these two things, it's it's just becomes very clear as to what the optimal marketing strategy will be, how you can best reach them. It becomes very clear who should be accepted as a client in your agency, who should be rejected. So, sales and marketing becomes much more effective when you have these two things and I can't really emphasize just how important they are."
- **evidence_type:** `direct_quote`
- **scope:** تعريف العميل/الحساب المثالي في سياق وكالة خدمات؛ النص لا يحدد تجربة مقارنة أو مقياسًا لمقدار «الفعالية».
- **what_it_does_not_prove:** لا يثبت سببية تعريف IAP/ICP في زيادة المبيعات أو أن النتيجة تتكرر في كل وكالة، ولا يحدد معيارًا موضوعيًا للقبول أو الرفض.
- **evidence_start:** `361262`
- **evidence_end:** `361655`
- **excerpt_sha256:** `ee287f01c591c149dffd44ff556eefe402e3e3b0a2a2be68aaa667e331f28a2c`
- **confidence:** `source_reported`
- **status:** `candidate`

### CAND_SALES_B_004

- **statement:** في سياق التسعير القائم على القيمة، يقول المصدر إن الوقت لا يُذكر للعميل وإن العميل يهتم بالنتائج.
- **source_id:** `SRC_NEW_5b782973289bdb21_021e6961`
- **locator:** `raw/new/Build a $100k MRR Agency — 14-Hour Masterclass.txt`, line 1, Unicode chars `[539325,539455)` (zero-based, end-exclusive).
- **evidence_quote:** "When you charge on value, you don't mention time, and time is never a question in the client's mind. They just care about results."
- **evidence_type:** `direct_quote`
- **scope:** توصية تسعير لخدمات وكالة؛ النطاق محصور في موقف التسعير الذي يصفه المتحدث، دون تحديد سوق أو سعر أو تجربة.
- **what_it_does_not_prove:** لا يثبت أن كل عميل يهتم بالنتائج وحدها، ولا يثبت أن إخفاء الوقت يرفع السعر أو القبول أو الاحتفاظ بالعميل.
- **evidence_start:** `539325`
- **evidence_end:** `539455`
- **excerpt_sha256:** `ff1382fb59942ab04f3c42cc53cc5d6f50f2033c7b7e0d7620e1c6656f3b1996`
- **confidence:** `source_reported`
- **status:** `candidate`

### CAND_SALES_B_005

- **statement:** يبلّغ المتحدث، في وصفه التاريخي للبريد البارد حول 2020، عن إرسال بضعة آلاف من الرسائل شهريًا ومعدل رد 10–15%، ثم يقول إن التشبع تبعه هبوط في المقاييس.
- **source_id:** `SRC_NEW_129f7a12e3e9285b_b7e305cd`
- **locator:** `raw/new/aaronxshepherd__If you only watch one cold email video, make it this (4 hour masterclass)__LzGJ3MQParY.txt`, line 1, Unicode chars `[1057,1315)` (zero-based, end-exclusive).
- **evidence_quote:** "So, back around 2020, cold email was super simple. You could send a couple thousand emails a month, get 10 to 15% reply rates, and it felt like booking meetings on autopilot. But like all things, eventually it got saturated and those metrics started to fall."
- **evidence_type:** `reported_result`
- **scope:** تجربة/وصف منسوب للمتحدث عن البريد البارد تقريبًا في 2020؛ القناة هي cold email والرقم معدل رد مذكور بلا مقام تفصيلي.
- **what_it_does_not_prove:** لا يثبت أن 10–15% كان معدلًا عامًا أو حاليًا، ولا يثبت أن التشبع وحده سبب هبوط المقاييس، ولا يثبت نتيجة خارج تجربة المتحدث.
- **evidence_start:** `1057`
- **evidence_end:** `1315`
- **excerpt_sha256:** `0915bda58d63051cb6835b9153f1eb3ec5bd9c3b308d7ff4a8ce0afd820c7cd0`
- **confidence:** `source_reported`
- **status:** `candidate`

### CAND_SALES_B_006

- **statement:** يفرّق المتحدث بين inbound وoutbound، ويستنتج أن ICP المبني على افتراضات أو سلوك inbound قد لا يمثل الأشخاص الأكثر احتمالًا للرد، وقد يؤدي إلى إهدار الوقت والمال.
- **source_id:** `SRC_NEW_129f7a12e3e9285b_b7e305cd`
- **locator:** `raw/new/aaronxshepherd__If you only watch one cold email video, make it this (4 hour masterclass)__LzGJ3MQParY.txt`, line 1, Unicode chars `[37194,37802)` (zero-based, end-exclusive).
- **evidence_quote:** "But inbound and outbound are two completely different segments. People who come to you already know who you are. They know they have a problem and they already trust you. at least a little. On the other hand, with outbound, you're reaching out to people who may never even heard of you, and they might not even know that they have a problem. So, if your ICP is based on assumptions or inbound behavior, there's a good chance that it actually doesn't represent the people that are most likely to respond to your cold emails. And when that happens, you end up blasting massive lists and wasting time and money."
- **evidence_type:** `inference`
- **scope:** استهداف قوائم cold email مع مقارنة سلوك العملاء الداخلين بالوصول outbound؛ الاستنتاج مشروط ببناء ICP على assumptions أو inbound behavior.
- **what_it_does_not_prove:** لا يثبت أن كل ICP مبني على inbound يفشل، ولا يثبت أن القائمة الكبيرة ستسبب هدرًا في كل حالة، ولا يقدم اختبارًا أو معدل رد للمقارنة.
- **evidence_start:** `37194`
- **evidence_end:** `37802`
- **excerpt_sha256:** `2ecb12ad66269e3f5f71c575698abc1af3395b9e0057ad9ba381175e21dd1f12`
- **confidence:** `inferred`
- **status:** `candidate`

### CAND_SALES_B_007

- **statement:** في القسم `[13] How We Made $770k in 30 Days With Only 2 Sales Reps`، يبلّغ المتحدث عن دفع 770k خلال 30 يومًا باثنين من مندوبي المبيعات، ويصف النموذج بأنه organic back-end بلا paid ads أو front-end marketing.
- **source_id:** `SRC_NEW_4338afb73c56fdd7_737c056d`
- **locator:** `raw/new/transcript_full (1).txt`, section `[13]`, line 92, line-relative Unicode chars `[79,262)`؛ file-absolute Unicode chars `[277470,277653)` (zero-based, end-exclusive).
- **evidence_quote:** "how we were able to drive 770k in the last 30 days with only two sales reps. And this was done all through organic back-end, no paid ads, and no front-end marketing whatsoever, right?"
- **evidence_type:** `reported_result`
- **scope:** نتيجة مبلغ عنها من فيديو واحد/نموذج واحد، بزمن 30 يومًا وباثنين مندوبي مبيعات، وفق توصيف المتحدث لقناته ونموذجه.
- **what_it_does_not_prove:** لا يثبت أن الرقم قابل للتكرار أو أنه صافي ربح، ولا يثبت أن وجود مندوبين أو غياب الإعلانات سبب النتيجة، ولا يثبت benchmark لباقي الأعمال.
- **evidence_start:** `277470`
- **evidence_end:** `277653`
- **excerpt_sha256:** `33d0e8d45ac85296ace3f98b22b3395a666ee63095d94bfe3cf8c1200ea51fc1`
- **confidence:** `source_reported`
- **status:** `candidate`

### CAND_SALES_B_008

- **statement:** يحذّر المتحدث في القسم نفسه من أن مقارنة مقاييس funnels مختلفة قد تكون منحازة، وأن مقاييس paid تختلف عن organic، وأن دمجها قد يعطي بيانات أقل دقة.
- **source_id:** `SRC_NEW_4338afb73c56fdd7_737c056d`
- **locator:** `raw/new/transcript_full (1).txt`, section `[13]`, line 92, line-relative Unicode chars `[897,1250)`؛ file-absolute Unicode chars `[278288,278641)` (zero-based, end-exclusive).
- **evidence_quote:** "those metrics, if you compare them side by side with a different funnel, um also might be skewed, right? So, like whether you're running paid, your metrics for these are going to be different than if you're running it for organic. And if you combine those metrics together, uh it's going to be giving you data that's a little bit more inaccurate, right?"
- **evidence_type:** `inference`
- **scope:** تحذير منهجي عند مقارنة show/close metrics بين paid وorganic أو funnels مختلفة؛ ورد في سياق النتيجة السابقة ذاتها.
- **what_it_does_not_prove:** لا يحدد مقدار الانحياز أو تعريف «أقل دقة»، ولا يثبت أن كل دمج للمقاييس خاطئ، ولا يقدم اختبارًا إحصائيًا أو عينة مقارنة.
- **evidence_start:** `278288`
- **evidence_end:** `278641`
- **excerpt_sha256:** `946bdd64aacc37e3fd05f5821d1bf33f23db0ae49daa00e6ef6cc43a7e74728c`
- **confidence:** `inferred`
- **status:** `candidate`

### CAND_SALES_B_009

- **statement:** يقسم المتحدث نظام cold email إلى infrastructure، وtargeting/data، وscripting، وappointment setting، ويقول إن فقدان أي قسم يفسد النظام كله.
- **source_id:** `SRC_NEW_e42b416e46db75c3_237d0cba`
- **locator:** `raw/new/matthewlucero__How To Generate Leads With Cold Email in 2026 (FULL COURSE)__BakY-82NYVQ.txt`, line 1, Unicode chars `[433,963)` (zero-based, end-exclusive).
- **evidence_quote:** "First, infrastructure. You can't send cold emails at scale if your domains and email accounts are not set up correctly. Second is targeting and data. The wrong list makes everything else irrelevant. Third is scripting. That's what you actually say in the email and why most people get it completely wrong. And fourth, appointment setting, because replies don't mean anything unless you book them into actual sales calls. These four sections cover the entire cold email system. Miss any one of them and the whole thing falls apart."
- **evidence_type:** `direct_quote`
- **scope:** إطار تدريبي للبريد البارد في B2B؛ يتناول الإرسال على نطاق واسع وتحويل replies إلى sales calls، دون تحديد قطاع أو تجربة مقارنة.
- **what_it_does_not_prove:** لا يثبت أن الأقسام الأربعة شروط لازمة في كل حملة، ولا يثبت أن أي قسم بعينه يسبب الفشل، ولا يقدم قياسًا لمساهمة كل قسم.
- **evidence_start:** `433`
- **evidence_end:** `963`
- **excerpt_sha256:** `881bb80b662487aa6ee28a7ff0ee9b76cb35a92bff86271f1ae912d5cda3c3e9`
- **confidence:** `source_reported`
- **status:** `candidate`

### CAND_SALES_B_010

- **statement:** يوصي المتحدث بمتابعات متعددة لنفس prospect؛ ويعطي مثالًا حسابيًا: عند sequence من أربع رسائل، يحتاج هدف 1,000 رسالة يوميًا إلى 250 prospect يوميًا، أو قرابة 5,000 prospect جديد شهريًا.
- **source_id:** `SRC_NEW_e42b416e46db75c3_237d0cba`
- **locator:** `raw/new/matthewlucero__How To Generate Leads With Cold Email in 2026 (FULL COURSE)__BakY-82NYVQ.txt`, line 1, Unicode chars `[10432,11191)` (zero-based, end-exclusive).
- **evidence_quote:** "People think, okay, you send a,000 emails per day, you're going to need a,000 new people. Not quite. The reason why is because some emails are going to be follow-ups to the same prospect. So, the way that I like to structure most of my email campaigns, and what I recommend for you guys, too, is to send multiple follow-ups to the same prospect. Because some people are busy, they might see your first email and they're not interested right away. But if you keep following up with them, you might catch them at a better time where they're ready to buy your product. On average, let's say if you're sending a four email sequence, this means you're going to need to have 250 people per day because you divide that out or about 5,000 net new prospects per month."
- **evidence_type:** `example`
- **scope:** مثال تخطيطي لحملة cold email بهدف 1,000 رسالة يوميًا مع sequence من أربع رسائل؛ الأرقام تقريبية كما يقول المصدر (`On average, let's say`).
- **what_it_does_not_prove:** لا يثبت أن المتابعات ترفع الشراء أو الرد، ولا يثبت أن أربع رسائل أو 250 يوميًا هي البنية المثلى، ولا يثبت دقة 5,000 خارج هذا الحساب الافتراضي.
- **evidence_start:** `10432`
- **evidence_end:** `11191`
- **excerpt_sha256:** `773080a4ef4fee88435365329b8a627b3f178d66ae1b9f301ac35b0e1c75808e`
- **confidence:** `source_reported`
- **status:** `candidate`

## خلاصة العدّ

- **المصادر المقروءة:** 5.
- **Claims المرشحة:** 10، بواقع Claimين لكل مصدر.
- **Claims من نوع `reported_result`:** 2.
- **Claims من نوع `example`:** 1.
- **Claims من نوع `inference`:** 2.
- **Claims من نوع `direct_quote`:** 5.
- **القرار:** لا اعتماد نهائي؛ يلزم مراجع مستقل قبل أي نقل إلى Claims الويكي أو Concepts.

## فحص التقرير

شُغّل فحص بنيوي بسيط بعد الكتابة للتحقق من وجود التقرير، وعدم فراغه، ووجود عشرة
أقسام Claim، وخمسة `source_id`، والحقول الستة المطلوبة في كل Claim
(`source_id`, `locator`, `evidence_quote`, `evidence_type`, `scope`,
`what_it_does_not_prove`)، مع بقاء كل حالة `candidate`.

النتيجة الفعلية: `REPORT_CHECK=PASS sources=5 claims=10 required_fields=6_each`.
وفحص القراءة السابق، الذي تحقق من وجود المسارات قبل القراءة ومطابقة SHA-256
وتطابق الشرائح الحرفية، أعاد: `READ_AND_QUOTE_CHECK=PASS`.
