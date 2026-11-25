# اختيار مجالات الموجة الأولى

## القرار

ترتيب التنفيذ على مستوى المجالات في الموجة الأولى هو:

1. `sales`
2. `outreach`
3. `pricing_offers`
4. `content_strategy`

هذا **قرار ترتيب للموجة الحالية** وليس ادعاءً بأن ترتيب أرقام مجلدات Nexus Brain يفرض مسار التنفيذ. فالفهرس يضع `01_outreach` قبل `02_sales_closing`، لكن رقم المجلد يصف موضع المجال في الـVault لا أولوية إنجازه. كما أن `planner.py` و`MASTER_GRAPH.json` أدوات اكتشاف/علاقات، وليسا خطة تنفيذ ملزمة.

الترتيب المقترح هنا هو ترتيب بناء معرفة تجارية قابلة للتطبيق: نبدأ بمعيار النجاح التجاري، ثم نبني مصدر الفرص، ثم نضبط العرض وسعره، ثم نحول اللغة والنتائج المتحققة إلى محرك محتوى. وهو لا يمنع أن يعمل الـoutreach عملياً قبل أو بالتوازي مع مكالمات البيع بعد اعتماد عقد المبيعات؛ المقصود أن **تصميم المعرفة** يبدأ من نتيجة البيع قبل توسيع قناة الوصول.

## قاعدة الدليل وحدود النسبة

- الرسائل تؤكد أن المطلوب «شغل حقيقي للمبيعات» لا نتيجة تجريبية (`USER_MESSAGES_SESSION_EF22.md:L42`)، وأن المطلوب خطة فعلية وفهم ما يُبنى لا مجرد Scripts (`:58`).
- الرسائل تصف الـMaster النهائي كمعرفة مجمعة ومنظمة، وتطلب تقسيم المبيعات الكبيرة إلى Masters متعددة وفهرساً يشرح وظيفة كل ملف (`USER_MESSAGES_SESSION_EF22.md:L65-L67`).
- الرسائل الخام لا تسمي هذه المجالات الأربعة بهذا الترتيب حرفياً؛ لذلك فاختيار الترتيب نفسه **استنتاج تشغيلي للموجة** مبني على الهدف والـVault، وليس متطلباً تاريخياً منسوباً إلى رسالة بعينها.
- أسماء الـsubdomains أدناه **اقتراحات أولية فقط**. لم تعتمد الرسائل الخام أسماء تفصيلية أو بوابة رسمية لكل subdomain (`USER_MESSAGES_SESSION_EF22.md:L222-L233` و`:L270-L281`).
- لا يوجد استخدام لـCodex في هذه الوثيقة، ولا يوجد نقل أو حذف أو تعديل لأي مصدر من الـVault.

## صورة الأدلة في الـVault

`BRAIN_INDEX.md` يعلن 39 Master canonical نشطاً، موزعة على 26 cluster، مع 32 graph edges (`BRAIN_INDEX.md:L1-L7`). المجالات الأربعة المطلوبة موجودة كـclusters نشطة منفصلة، وبها التغطية التالية:

| ترتيب الموجة | الاسم التشغيلي | الـcluster canonical | Masters النشطة | إجمالي Concepts المفهرسة |
|---:|---|---|---:|---:|
| 1 | `sales` | `02_sales_closing` | 4 | 186 |
| 2 | `outreach` | `01_outreach` | 4 | 150 |
| 3 | `pricing_offers` | `03_pricing_offers` | 1 | 131 |
| 4 | `content_strategy` | `04_content_strategy` | 1 | 161 |

إجماليات Concepts في الجدول هي جمع الأرقام التي يوردها فهرس كل cluster، وليست عدّاً جديداً للمحتوى.

## لماذا يبدأ الترتيب بـ`sales`؟

### 1. `sales` — معيار النتيجة والقبول

**سبب الأولوية:** الهدف المؤكد في رسائل المستخدم هو بناء نظام مبيعات حقيقي. لذلك نحتاج أولاً إلى تعريف ما الذي يعنيه العميل المؤهل، وما شكل المحادثة الجيدة، وكيف تُعالج الاعتراضات، وما الذي يُعد إغلاقاً ومتابعة ناجحة. بدون هذا المعيار قد ينتج الـoutreach حجماً من الردود أو الاجتماعات لا نعرف إن كان مناسباً أو قابلاً للإغلاق.

**الأدلة:**

- رسالة المستخدم تطلب مصادر ومعلومات لازمة للمبيعات، وتفرق صراحة بين العمل الحقيقي والشيء التجريبي (`USER_MESSAGES_SESSION_EF22.md:L42`).
- الرسالة التي تشرح شكل الـMaster تقول إن المبيعات موضوع ضخم ويجب تقسيمه إلى Masters للأقسام الكبيرة، مع فهرس يشرح وظيفة الملفات (`USER_MESSAGES_SESSION_EF22.md:L65-L67`).
- الـcluster النشط يضم محادثة البيع، الإغلاق عالي السعر، تأهيل العميل، ومعالجة الاعتراضات (`BRAIN_INDEX.md:L31-L51`).
- الاستحضار الموضعي من `Master_Sales_Conversation` يضع دورة تشغيلية من التأهيل/ما قبل المكالمة إلى Discovery ثم تقديم الحل والإغلاق والمتابعة في `§17` و`§20.11`. وهذا يجعل sales عقداً عملياً للمعرفة التي ستغذّي المجالات التالية.

**لماذا قبل outreach تحديداً؟** لأننا نريد أن نعرف أولاً من هو العميل المناسب وما النتيجة التي نريد الوصول إليها في المكالمة. بعد ذلك يمكن تصميم الرسالة والقناة والحجم لخدمة هذا الهدف، بدلاً من تحسين الإرسال بمعزل عن جودة الصفقة.

**المسارات النشطة:**

- فهرس المجال: `/sdcard/Nexus_Brain/nexus_vault/02_sales_closing/_index.md`
- `/sdcard/Nexus_Brain/nexus_vault/02_sales_closing/Master_Sales_Conversation.md` — 64 Concept؛ المحادثة من Discovery إلى Closing.
- `/sdcard/Nexus_Brain/nexus_vault/02_sales_closing/Master_High_Ticket_Closing.md` — 25 Concept؛ الإغلاق عالي السعر والتموضع المتميز.
- `/sdcard/Nexus_Brain/nexus_vault/02_sales_closing/Master_Lead_Qualification.md` — 49 Concept؛ تأهيل العميل والـICP.
- `/sdcard/Nexus_Brain/nexus_vault/02_sales_closing/Master_Objection_Handling.md` — 48 Concept؛ الاعتراضات والإغلاق.

**اقتراح — subdomains أولية:**

1. `discovery_and_sales_conversations` — اكتشاف المشكلة، Frame، الأسئلة، تقديم الحل.
2. `lead_qualification` — ICP، شروط الملاءمة، التأهيل قبل المكالمة.
3. `objection_handling` — اعتراض السعر، المخاطرة، التوقيت، ومعالجة الجذر.
4. `high_ticket_closing` — إغلاق العروض عالية السعر، الثقة، والقرار.
5. `proposal_follow_up_pipeline` — الـProposal، المتابعة، ومراحل الـPipeline.

هذه أسماء تنظيمية مقترحة؛ لا تعني إنشاء Masters أو مجلدات جديدة الآن، ولا تعني أن كل subdomain سيحصل على Master منفصل قبل فحص المصادر.

### 2. `outreach` — محرك توليد الفرص بعد تثبيت معيار البيع

**سبب الأولوية الثانية:** بعد تحديد العميل المؤهل ونتيجة المحادثة، يصبح ممكناً بناء قناة تجلب فرصاً تخدم هذا المعيار. الـoutreach هو طبقة الاستحواذ: تحديد الحسابات، جمع الـLeads، كتابة الرسالة، المتابعة، القياس، وحماية قابلية وصول البريد.

**الأدلة:**

- الـcluster النشط يحتوي أربعة Masters تغطي Cold Email، Deliverability، Lead Generation، وOutreach Mechanics (`BRAIN_INDEX.md:L9-L29`).
- `Master_Cold_Email_System.md §4` يقدّم Workflow يبدأ بـICP ثم Lead Generation ثم Sales Script ثم المتغيرات وفحص Spam وصحة الـDomain والإرسال. هذا يبين أن outreach قناة تشغيلية يجب أن تُبنى على تعريف العميل والرسالة والنتيجة، لا على الحجم وحده.
- `Master_Outreach_Mechanics.md §1` يلخص النظام في: ICP محدد + رسالة مخصصة + متابعة منظمة + تتبع دقيق.
- `Master_Cold_Email_System.md §14` يربط Inbox/Reply/Meeting بالمعدل النهائي للإغلاق، فلا يكون قياس outreach منفصلاً عن sales.
- `Master_Outreach_Mechanics.md §15.8` يحذر من أن Outreach القوي لا يعوض Offer ضعيف؛ لذلك نحتاج أولاً إلى معيار sales، ثم نستخدم outreach لاختبار الوصول إليه.

**علاقة الترتيب بالـGraph:** توجد في `MASTER_GRAPH.json` علاقة `Master_Cold_Email_System → Master_Sales_Conversation` بوصفها `feeds`، وعلاقة `Master_Lead_Qualification → Master_Sales_Conversation` بوصفها `prerequisite`. هذه علاقات اعتماد معرفية وليست ترتيب تشغيل إلزامياً. القراءة الصحيحة للموجة هي: نثبت عقد sales أولاً، ثم نبني outreach بحيث يغذي هذا العقد ويقيسه.

**المسارات النشطة:**

- فهرس المجال: `/sdcard/Nexus_Brain/nexus_vault/01_outreach/_index.md`
- `/sdcard/Nexus_Brain/nexus_vault/01_outreach/Master_Cold_Email_System.md` — 27 Concept؛ الرسالة الباردة والـSequences.
- `/sdcard/Nexus_Brain/nexus_vault/01_outreach/Master_Email_Deliverability.md` — 23 Concept؛ البنية التحتية، السمعة، وقابلية الوصول.
- `/sdcard/Nexus_Brain/nexus_vault/01_outreach/Master_Lead_Generation.md` — 59 Concept؛ البحث عن العملاء المحتملين وبناء القوائم.
- `/sdcard/Nexus_Brain/nexus_vault/01_outreach/Master_Outreach_Mechanics.md` — 41 Concept؛ التخصيص، المتابعة، القياس، والتوسع.

**اقتراح — subdomains أولية:**

1. `lead_generation_and_prospect_research` — تحديد الحسابات، جمع البيانات، وبحث الـICP.
2. `cold_email_and_message_systems` — Ice Breaker، PSL، VSL، CTA، وSequences.
3. `outreach_mechanics_and_follow_up` — التخصيص، القيمة أولاً، القنوات، والمتابعة.
4. `email_deliverability_infrastructure` — SPF/DKIM/DMARC، Warm-up، السمعة، والقائمة النظيفة.
5. `outreach_measurement_and_scaling` — Reply/Meeting/Close KPIs، التجارب، والتوسع.

الحد المقترح بين `sales` و`outreach`: Lead sourcing والرسالة والقناة في outreach؛ Discovery والملاءمة والاعتراض والإغلاق في sales. الحالات المشتركة، مثل Follow-up بعد مكالمة البيع، تُسجل في sales مع روابط إلى تسلسلات outreach عند الحاجة.

### 3. `pricing_offers` — تحويل التعلم الميداني إلى عرض قابل للشراء

**سبب الأولوية الثالثة:** sales يكشف المشكلة والنتيجة والاعتراضات، وoutreach يكشف من يستجيب وأي لغة وقيمة تجذب العميل المناسب. بعد هذه الإشارات نضبط تصميم العرض، مستويات الخدمة، السعر، الضمان، والـrisk reversal. بذلك لا يكون التسعير تمريناً نظرياً منفصلاً عن قدرة العرض على الإغلاق.

**الأدلة:**

- `BRAIN_INDEX.md:L53-L58` يورد Master واحداً نشطاً في هذا المجال، لكنه واسع: 131 Concept و51 قسماً.
- `Master_Pricing_And_Offer_Design.md §1` يربط السعر بإدراك القيمة، Value Ladder، Value Stack، والـAnchor، ويضع السعر داخل سياق التحول لا كرقم منفصل.
- `Master_Pricing_And_Offer_Design.md §4` يغطي Value Ladder وValue Stack وTiered Pricing وAnchoring وIrresistible Offer؛ وهي مكونات تأتي بعد فهم العميل ونتيجته واعتراضاته.
- `Master_Outreach_Mechanics.md §15.8` يصرح بأن حجز مكالمات جيداً مع إغلاق منخفض قد يعني مشكلة في الـOffer. هذا سبب مباشر لجعل pricing/offers مرحلة لاحقة للتعلم من sales وoutreach.
- `Master_Content_Strategy.md §4.3` يقرر أن Offer-First يحتاج Offer مُثبتاً مسبقاً؛ وهذا يدعم وضع pricing_offers قبل content_strategy.

**المسار النشط:**

- فهرس المجال: `/sdcard/Nexus_Brain/nexus_vault/03_pricing_offers/_index.md`
- `/sdcard/Nexus_Brain/nexus_vault/03_pricing_offers/Master_Pricing_And_Offer_Design.md` — 131 Concept؛ تصميم العرض، سلم القيمة، الباقات، والتسعير.

**اقتراح — subdomains أولية:**

1. `offer_design_and_transformation` — العميل، الوعد، النتيجة، والـUnique Mechanism.
2. `value_ladder_and_packaging` — Free/Low/Mid/High Ticket، والانتقال بين المستويات.
3. `pricing_architecture_and_tiers` — النماذج، الباقات، Retainer، Performance، والـCustom Pricing.
4. `value_stack_and_anchoring` — تجميع القيمة، المقارنة، والـDecoy/Anchor.
5. `guarantees_risk_reversal_and_price_objections` — الضمانات، تقليل المخاطرة، واعتراض السعر.

هذه subdomains مقترحة للتصنيف الأولي فقط؛ لا تفترض سعراً أو ضماناً قبل ربط القرار بأدلة العملاء والنتائج والقيود.

### 4. `content_strategy` — نشر الرسالة بعد تثبيت العميل والعرض

**سبب الأولوية الرابعة:** استراتيجية المحتوى هي طبقة التوزيع والتراكم. لكي لا تنتج محتوى يجذب مشاهدين غير مؤهلين، يجب أن تستفيد من لغة العملاء التي ظهرت في sales، ومن إشارات الـICP والرسائل في outreach، ومن العرض والسعر بعد تثبيتهما في pricing_offers. عندها يوجه المحتوى الجمهور إلى المسار المالي الصحيح بدلاً من أن يكون إنتاجاً منفصلاً عن المبيعات.

**الأدلة:**

- `BRAIN_INDEX.md:L60-L65` يورد Master محتوى واحداً نشطاً يضم 161 Concept و30 قسماً.
- `Master_Content_Strategy.md §1` يفرق بين Cold Outreach الذي يموت عند الإرسال ومحرك المحتوى الذي يتراكم؛ لذلك المحتوى أصل طويل الأمد، وليس بديلاً عن تثبيت الرسالة والعرض في بداية الموجة.
- `Master_Content_Strategy.md §4.3` يضع Offer-First: تحديد ما سيباع ثم بناء المحتوى حول المشكلة والحل والعرض، مع شرط أن يكون الـOffer مثبتاً.
- `Master_Content_Strategy.md §4.8` يجعل أسئلة العملاء واعتراضاتهم ونتائجهم ومشاكلهم مصدراً لأفكار المحتوى؛ وهذه بيانات تنتجها المرحلتان الأولى والثانية.
- `Master_Content_Strategy.md §4.13` يربط المحتوى بمسار مالي: Content → Lead Magnet → Email Sequence → Offer. لذلك يأتي بعد pricing_offers في موجة بناء المعرفة.

**المسارات النشطة:**

- فهرس المجال: `/sdcard/Nexus_Brain/nexus_vault/04_content_strategy/_index.md`
- `/sdcard/Nexus_Brain/nexus_vault/04_content_strategy/Master_Content_Strategy.md` — 161 Concept؛ المحاور، القمع، التوزيع، القياس، والربط بالعرض.

**اقتراح — subdomains أولية:**

1. `audience_positioning_and_content_manifesto` — الجمهور، التموضع، الصوت، وما يقوله المحتوى وما لا يقوله.
2. `content_funnel_tofu_mofu_bofu` — الوعي، التنشئة، والتحويل.
3. `customer_voice_and_validated_ideation` — الأسئلة، الاعتراضات، النتائج، واختبار الأفكار.
4. `content_formats_and_repurposing` — صيغ المحتوى، الـLego، الـBatching، وإعادة الاستخدام.
5. `distribution_calendar_and_measurement` — المنصات، الإيقاع، TVP، وقياس الإشارة التجارية.
6. `content_monetization_and_offer_alignment` — ربط كل قطعة بمسار Lead Magnet/Email/Offer.

المقصود هنا `content_strategy` فقط. أما الإنتاج المرئي أو كتابة الـScripts فلهما Masters أخرى خارج هذه الموجة، مثل `05_content_production` و`06_copywriting_scripts`، ولا ينبغي خلطهما بالـcluster الاستراتيجي الرابع.

## الخلاصة التشغيلية

| المرحلة | سؤال القبول الذي تجيب عنه | ما الذي تغذيه للمرحلة التالية |
|---:|---|---|
| `sales` | من العميل المناسب؟ ما المشكلة؟ كيف تُدار المحادثة ويُغلق القرار؟ | تعريف العميل، الألم، اللغة، الاعتراضات، ومعيار الإغلاق |
| `outreach` | كيف نصل إلى هؤلاء العملاء برسالة وقناة قابلة للقياس؟ | قوائم، رسائل، ردود، اجتماعات، وبيانات ICP |
| `pricing_offers` | ما العرض والقيمة والسعر والبنية التي تستحق الشراء؟ | عرض مثبت ورسائل قيمة ومواد تحويل |
| `content_strategy` | كيف نراكم الثقة والطلب ونقود الجمهور إلى العرض؟ | محرك محتوى مرتبط بالقمع والإيراد |

إذن: `sales` أولاً لأنه يحدد النتيجة، `outreach` ثانياً لأنه يخلق الفرص وفق ذلك المعيار، `pricing_offers` ثالثاً لأنه يحول التعلم إلى عرض قابل للإغلاق، و`content_strategy` رابعاً لأنه يوسع الرسالة والعرض بعد تثبيتهما. كل أسماء الـsubdomains في هذا الملف موسومة **اقتراحاً** ولا تُعد مواصفات نهائية.

## التحقق من النطاق

- تم التحقق من وجود المسارات الأربعة وفهارسها والـMasters المذكورة داخل `/sdcard/Nexus_Brain/nexus_vault/`.
- الملف الناتج المقصود الوحيد هو: `/root/r/reports/sales-proof/agent-domain-selection.md`.
- لم تُعدّل ملفات المصدر أو الـVault، ولم تُحذف ملفات، ولم يُستخدم Codex.
