# مقترح كتالوج المجالات الكامل — قراءة بنيوية مقارنة

**المعرّف:** `FULL_DOMAIN_CATALOG_PROPOSAL_2026-10-11`  
**نوع المخرج:** proposal للقراءة والمراجعة فقط، وليس تعديلًا للكتالوج أو سجل معرفة  
**حالة المخرج:** غير معتمد، لا يفتح أي مجال معرفي، ولا يثبت اكتمال مصدر أو مجال  
**نطاق القراءة:** وثيقة جرد corpus، تعليمات المشروع، schema، الميثاق التشغيلي، ملفا config الحاليان، `BRAIN_INDEX.md`، `MASTER_GRAPH.json`، وفهارس `_index.md` للمجلدات canonical النشطة فقط  
**الاستبعاد:** لم تُقرأ `_archive/` كمصدر نشط، ولم تُعدّل `raw/` أو `claims/` أو `concepts/` أو `masters/` أو `config/`.

## 1. خلاصة القرار المقترح

يظهر في فهرس الـVault القديم **26 عنقودًا canonical** تضم **39 Master**. لذلك يقترح هذا التقرير الاحتفاظ بهذه العناقيد كطبقة catalog مرشحة، مع إعطاء كل عنقود `domain_id` آمنًا وفريدًا لا يعتمد على الرقم وحده. هذه نتيجة فهرسية/بنيوية؛ لا تعني أن العناقيد هي تقسيم corpus الجديد، ولا أن أعداد المفاهيم دليل على اكتمال القراءة.

المقارنة مع المصادر الستة المقاسة تعطي ثلاث درجات مختلفة من المعرفة:

1. **مثبت كعنقود في الفهرس (`I`)**: العنقود ظاهر صراحةً في `BRAIN_INDEX.md`، وله `_index.md` canonical، وتدعمه عقدة في `MASTER_GRAPH.json`.
2. **مستنتج من أسماء/بنية المصادر (`S`)**: توجد إشارات اسمية أو بنيوية في جرد `raw/new/` أو في بنية المصدر، لكنها ليست قراءة دلالية ولا قرار توجيه.
3. **يحتاج قراءة دلالية (`D`)**: لا يمكن نسبة مصدر إلى المجال، أو اعتماد subdomain، أو إنشاء مجال جديد، قبل قراءة الجسم والسياق والغرض مع مواضع قابلة للتتبع. هذا ينطبق على إسناد المصادر الستة إلى المجالات، حتى عندما تكون أسماء الملفات واضحة.

الكتالوج الحالي في `config/domain_catalog.json` يعرّف أربعة مجالات للموجة الأولى فقط: `sales` و`outreach` و`pricing_offers` و`content_strategy`. هذه المجالات الأربعة تقابل أربعة عناقيد قديمة، بينما يظل **22 عنقودًا إضافيًا خارج config الحالي** إلى أن يراجعها Commander ويقرر إن كانت مجالات مستقلة أو subdomains أو حدودًا تحتاج دمجًا.

## 2. قواعد الدليل والحساب

- أعداد `Masters` و`Concepts` أدناه هي أعداد مكتوبة في الفهارس أو في عقد graph. عدد المفاهيم لكل عنقود هو **مجموع أرقام Masters المفهرسة داخل العنقود**، وليس عدًّا فريدًا عالميًا؛ لا يجوز جمعها واعتبار الناتج عدد Concepts مستقلة.
- يعلن `BRAIN_INDEX.md` عن 39 Master و26 cluster و32 graph edges، ويعلن `nexus_vault/AGENTS.md` عن 1,608 مفهومًا مفهرسًا. يظل الفرق بين هذه الأرقام وأي مجموع فرعي غير محسوم هنا؛ التقرير لا يعيد بناء سجل Concepts.
- `MASTER_GRAPH.json` يصف علاقات على مستوى الـMaster. تحويل العلاقة إلى dependency على مستوى domain هنا **اقتراح ملاحي** لا يغيّر `processing_order.json` ولا يفرض ترتيبًا تشغيليًا.
- `raw/new/` جُردت أسماؤه وبنيته في تقرير الجرد، لكن لم تُجرَ قراءة دلالية لمحتوى الملفات في هذا العمل. لذلك عبارات `S` تعني «إشارة مرشحة من الاسم/البنية» فقط.
- وجود ملف أو مجلد أو اسم Master لا يثبت `source_done` أو `domain_done` أو اجتياز بوابات `R/T/C/K/M/QA`.

### رموز حالة المقارنة

| الرمز | المعنى في هذا التقرير |
|---|---|
| `I` | مثبت كعنقود/ماستر نشط في فهرس الـVault؛ دليل بنيوي فقط |
| `S+` | إشارة اسمية/بنيوية قوية في `raw/new/`، غير دلالية |
| `S~` | إشارة اسمية/بنيوية عامة أو مختلطة في `raw/new/` |
| `U` | موجود ضمن القياس، لكن لم يُسند إلى مجال في هذا العمل |
| `D` | يحتاج قراءة دلالية كاملة ومراجعة قبل أي تصنيف أو اعتماد |

## 3. لقطة المصادر الستة المقاسة

الأرقام التالية من `reports/CORPUS_INVENTORY_SCOPE_2026-10-11.md`، وهي قياس ملفات وحجم فقط. لا تمثل أعداد مصادر معرفية ولا تغطية مجالات.

| المصدر المقاس | النوع/الدور المقاس | الملفات العادية | الحجم بالبايت | MiB تقريبًا | وضع الإسناد في هذا التقرير |
|---|---|---:|---:|---:|---|
| `/sdcard/NEXUS_LLM_WIKI/raw/new/` | صندوق مصادر خام جديدة | 1,776 | 43,757,343 | 41.730 | `S` من إشارات أسماء/بنية فقط؛ `D` للإسناد |
| `/sdcard/NEXUS_LLM_WIKI/raw/legacy/brain/` | نسخة خام legacy للمراجعة | 0 | 0 | 0.000 | لا توجد ملفات عادية في القياس؛ لا إشارة مصدرية |
| `/sdcard/NEXUS_LLM_WIKI/raw/legacy/chats/` | نسخ محادثات خام legacy | 39 | 6,148,975 | 5.864 | `U/D`؛ لا إسناد دلالي في هذا التقرير |
| `/sdcard/NEXUS_LLM_WIKI/raw/context/` | خام سياقي | 3 | 252,610 | 0.241 | `U/D`؛ لا إسناد دلالي في هذا التقرير |
| `/sdcard/Nexus_Brain/brain/` | مصدر قديم/مرجعي أصلي | 564 | 19,680,572 | 18.769 | `U/D`؛ قياس legacy لا يساوي تصنيفًا جديدًا |
| `/sdcard/Nexus_Brain/nexus_vault/` | ويكي نشطة وفهارس وأدوات | 159 | 24,885,393 | 23.733 | `I` للعناقيد المفهرسة؛ ليس corpus خامًا جديدًا |

### 3.1 قراءة المقارنة

- **`raw/new/`:** أسماء الملفات تُظهر إشارات كثيرة إلى outreach وsales وoffers وcontent وvideo وstorytelling وbranding وplatforms وAI وغيرها. هذه الإشارات مفيدة لبناء قائمة القراءة، لكنها لا تثبت primary domain أو subdomain، ولا تسمح باحتساب coverage.
- **`raw/legacy/brain/`:** وجود المسار لا يضيف ملفات؛ القياس سجل صفر ملفات عادية. لا تُستنتج منه فجوة معرفية أو اكتمال.
- **`raw/legacy/chats/` و`raw/context/`:** أعداد صغيرة نسبيًا، لكن طبيعة المحادثة/السياق لا تكفي لإسنادها إلى مجال. يلزم قراءة كاملة وتحديد ما إذا كانت تعليمات أو مادة معرفة أو سجل قرار.
- **`/sdcard/Nexus_Brain/brain/`:** مصدر قديم/مرجعي منفصل عن catalog الجديد. لا تُعامل مجلدات `processed/` أو `duplicates/` كدليل قبول أو كنسخ مستقلة دون مراجعة الهوية والتكرار.
- **`nexus_vault/`:** مصدر إثبات العناقيد في هذا proposal فقط عبر الفهارس والـgraph. لا تُعامل Masters القديمة بوصفها دليلًا على تغطية `raw/new/` أو على اكتمال المجالات الجديدة.

## 4. مواءمة المقترح مع config الحالي

| `config/domain_catalog.json` الحالي | العنقود canonical المطابق | وضع config الحالي | وضع هذا التقرير |
|---|---|---|---|
| `sales` | `02_sales_closing` | `in_progress`، `completion_claim: false` | `I`؛ proposal domain_id ثابت هو `sales` |
| `outreach` | `01_outreach` | `pending`، `completion_claim: false` | `I`؛ proposal domain_id ثابت هو `outreach` |
| `pricing_offers` | `03_pricing_offers` | `pending`، `completion_claim: false` | `I`؛ proposal domain_id ثابت هو `pricing_offers` |
| `content_strategy` | `04_content_strategy` | `pending`، `completion_claim: false` | `I`؛ proposal domain_id ثابت هو `content_strategy` |
| 22 عناقيد أخرى | لا توجد لها سجلات domains في config الحالي | خارج الموجة الأولى الحالية | `I` كعناقيد Vault فقط؛ لا تُضاف إلى config بهذا التقرير |

ترتيب `sales → outreach → pricing_offers → content_strategy` في `processing_order.json` هو قفل **لعمل المعرفة**، وليس dependency تجارية، ولا يبرر اعتبار أي مجال من العناقيد القديمة مكتملًا.

## 5. الكتالوج المقترح للعناقيد الـ26

### 5.1 `outreach`

- **`canonical_cluster`:** `01_outreach`
- **`proposed_domain_id`:** `outreach` — يحافظ على معرّف config الحالي.
- **حالة الدليل:** `I` كعنقود مفهرس؛ `S+` في `raw/new/` بسبب إشارات `cold email` و`outreach` و`lead generation` وLinkedIn؛ `D` لإسناد أي ملف بعينه.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/01_outreach/_index.md`; والـMasters: `Master_Cold_Email_System.md`, `Master_Email_Deliverability.md`, `Master_Lead_Generation.md`, `Master_Outreach_Mechanics.md` تحت المسار نفسه.
- **العدد الموثق فهرسيًا:** 4 Masters؛ 150 مفهومًا مفهرسًا (27 + 23 + 59 + 41). هذا ليس عددًا فريدًا ولا دليل اكتمال.
- **subdomains أولية:** `lead_generation`، `prospect_research_and_list_building`، `cold_email_and_message_systems`، `email_deliverability`، `outreach_mechanics_and_follow_up`، `outreach_measurement`.
- **dependencies مقترحة:** `outreach → sales` (مرفوع من علاقة `Master_Cold_Email_System → Master_Sales_Conversation`؛ `feeds`). سياقيًا قد يحتاج إلى `market_research_validation` و`niche_positioning`، لكن ذلك يحتاج قراءة دلالية ولا يغيّر ترتيب config.
- **سبب الاحتياج:** يملك آلية الوصول الأولي وتوليد الفرص والبنية التقنية للإرسال، وهي مختلفة عن محادثة البيع بعد الرد وعن تصميم العرض.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`. كل نسبة مصدر خارج الفهرس تحتاج `D`.

### 5.2 `sales`

- **`canonical_cluster`:** `02_sales_closing`
- **`proposed_domain_id`:** `sales` — يحافظ على معرّف config الحالي.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب أسماء sales/call/closing/objection/qualification؛ `D` لإثبات ملكية المصدر.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/02_sales_closing/_index.md`; والـMasters: `Master_Sales_Conversation.md`, `Master_High_Ticket_Closing.md`, `Master_Lead_Qualification.md`, `Master_Objection_Handling.md`.
- **العدد الموثق فهرسيًا:** 4 Masters؛ 186 مفهومًا مفهرسًا (64 + 25 + 49 + 48).
- **subdomains أولية:** `sales_conversations_and_discovery`، `lead_qualification`، `objection_handling`، `high_ticket_closing`، `proposal_follow_up_and_pipeline`، `negotiation`.
- **dependencies مقترحة:** `outreach → sales`؛ `psychology_influence → sales` و`trust_authority → sales` كسياقين يغذيان الإغلاق، استنادًا إلى علاقات graph على مستوى Masters. `sales` يغذي داخليًا `objection_handling` ثم `high_ticket_closing`.
- **سبب الاحتياج:** المجال يملك المحادثة والتشخيص والتأهيل والاعتراضات والإغلاق؛ دمجه مع outreach أو pricing سيخفي حدود الملكية بين القناة والمحادثة وتصميم العرض.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`. لا توجد دعوى بأن `sales` الحالي `domain_done`.

### 5.3 `pricing_offers`

- **`canonical_cluster`:** `03_pricing_offers`
- **`proposed_domain_id`:** `pricing_offers` — يحافظ على معرّف config الحالي.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب price/pricing/offer/discount/value/guarantee؛ `D` لتحديد هل المادة تصميم عرض أم اعتراض سعر في محادثة.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/03_pricing_offers/_index.md` و`Master_Pricing_And_Offer_Design.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 131 مفهومًا مفهرسًا؛ 51 قسمًا في `BRAIN_INDEX.md`.
- **subdomains أولية:** `offer_design_and_transformation`، `value_ladder_and_packaging`، `pricing_architecture_and_tiers`، `value_stack_and_anchoring`، `guarantees_and_risk_reversal`، `price_objections_boundary`.
- **dependencies مقترحة:** `business_models → pricing_offers` (`prerequisite` على مستوى Master)، و`pricing_offers → funnels_conversion` (`feeds`). ملكية اعتراض السعر مقابل تصميم السعر تحتاج `cross_domain_review` دلالية.
- **سبب الاحتياج:** تصميم القيمة والباقات والسعر وشروط الضمان ليس هو نفس التعامل مع اعتراض حي أثناء call، ولا هو مجرد رسالة outreach.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`. لا يُفهم من رقم 131 أن العرض الجديد validated.

### 5.4 `content_strategy`

- **`canonical_cluster`:** `04_content_strategy`
- **`proposed_domain_id`:** `content_strategy` — يحافظ على معرّف config الحالي.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب content strategy/content planning/social/content-to-customer؛ `D` للفصل بين الاستراتيجية والإنتاج والـhooks والمنصات.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/04_content_strategy/_index.md` و`Master_Content_Strategy.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 161 مفهومًا مفهرسًا؛ 30 قسمًا.
- **subdomains أولية:** `audience_positioning`، `content_funnel_tofu_mofu_bofu`، `customer_voice_and_validated_ideation`، `content_formats_and_repurposing`، `distribution_calendar_and_measurement`، `content_monetization_and_offer_alignment`.
- **dependencies مقترحة:** `personal_branding → content_strategy` (`feeds` على مستوى Master)، و`content_strategy → hooks_attention` و`content_strategy → funnels_conversion`. الإنتاج والـhooks والمنصات لا تُدمج تلقائيًا؛ يلزم فحص حدود دلالي.
- **سبب الاحتياج:** التخطيط للجمهور والمحاور والقمع والتوزيع والقياس طبقة استراتيجية، بينما إنتاج الفيديو أو كتابة script أو فهم algorithm طبقات تنفيذية/متخصصة.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`. لا يثبت وجود إشارة اسمية تغطية المجال الجديد.

### 5.5 `content_production`

- **`canonical_cluster`:** `05_content_production`
- **`proposed_domain_id`:** `content_production`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب video/reels/editing/production؛ `D` لمعرفة حدود الإنتاج مقابل الاستراتيجية والسكريبت.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/05_content_production/_index.md` و`Master_Video_Production.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 90 مفهومًا مفهرسًا؛ 25 قسمًا.
- **subdomains أولية:** `video_preproduction`، `recording_and_production`، `editing_and_postproduction`، `short_form_production`، `creative_team_workflows`، `production_quality_and_delivery`.
- **dependencies مقترحة:** `copywriting_scripts → content_production` (`feeds`) و`visual_identity_design → content_production` (`complements`)؛ `content_production → platform_strategy` (`feeds`).
- **سبب الاحتياج:** يحول الفكرة أو script إلى أصل مرئي/فيديو، وله دورة إنتاج وتسليم مختلفة عن قرار ماذا ننشر ولماذا.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`. لا توجد قراءة إنتاجية للمصادر هنا.

### 5.6 `copywriting_scripts`

- **`canonical_cluster`:** `06_copywriting_scripts`
- **`proposed_domain_id`:** `copywriting_scripts`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب script/copywriting/VSL/sales script؛ `D` لتقرير هل النص استراتيجية محتوى أو script إنتاج أو sales copy.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/06_copywriting_scripts/_index.md`؛ والـMasters: `Master_Scripting_Frameworks.md` و`Master_VSL_System.md`.
- **العدد الموثق فهرسيًا:** 2 Masters؛ 84 مفهومًا مفهرسًا (59 + 25).
- **subdomains أولية:** `copywriting_frameworks`، `script_structure`، `vsl_systems`، `sales_scripts`، `hook_body_cta`، `templates_and_examples`.
- **dependencies مقترحة:** `storytelling → copywriting_scripts` (`complements`) و`copywriting_scripts → content_production` (`feeds`).
- **سبب الاحتياج:** النص/السكريبت وحدة وسيطة يمكن أن تغذي فيديو أو VSL أو رسالة، ولا ينبغي خلطها مع تصوير/مونتاج أو content planning.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.7 `storytelling`

- **`canonical_cluster`:** `07_storytelling`
- **`proposed_domain_id`:** `storytelling`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب storytelling/narrative/characters/retention؛ `D` لتحديد ما هو سرد عام وما هو hook أو script.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/07_storytelling/_index.md` و`Master_Storytelling_Complete.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 111 مفهومًا مفهرسًا؛ 20 قسمًا.
- **subdomains أولية:** `story_architecture`، `narrative_arcs`، `character_conflict_and_transformation`، `emotion_and_retention`، `storytelling_for_content`، `examples_and_case_patterns`.
- **dependencies مقترحة:** `storytelling → copywriting_scripts` (`complements`)؛ ويمكن أن يغذي `content_strategy` سياقيًا، لكن ذلك ليس edge صريحًا على مستوى domain.
- **سبب الاحتياج:** السرد آلية تركيب ومعنى عابرة للصيغ؛ إبقاؤه منفصلًا يمنع اختزاله في كتابة script أو في تقنية جذب انتباه واحدة.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.8 `hooks_attention`

- **`canonical_cluster`:** `08_hooks_attention`
- **`proposed_domain_id`:** `hooks_attention`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب hooks/attention/thumbnails/first seconds؛ `D` للفصل بين hook لفظي ومرئي ومنصة معينة.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/08_hooks_attention/_index.md`؛ والـMasters: `Master_Hooks_And_Attention.md` و`Master_Visual_Hook_Design.md`.
- **العدد الموثق فهرسيًا:** 2 Masters؛ 78 مفهومًا مفهرسًا (43 + 35).
- **subdomains أولية:** `attention_psychology`، `verbal_hooks`، `visual_hooks`، `curiosity_and_open_loops`، `platform_specific_hooks`، `hook_testing`.
- **dependencies مقترحة:** `content_strategy → hooks_attention` (`feeds`) و`hooks_attention → visual_hook_design` كعلاقة داخل العنقود (`complements` بين Masters)، مع صلة سياقية بـ`content_production`.
- **سبب الاحتياج:** لحظة جذب الانتباه لها وظيفة وحدود مختلفة عن بناء القصة أو إنتاج الفيديو الكامل؛ فصلها يحسن الاسترجاع ولا يثبت أنها مجال مستقل في config.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.9 `personal_branding`

- **`canonical_cluster`:** `09_personal_branding`
- **`proposed_domain_id`:** `personal_branding`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب personal brand/branding/identity/authority/positioning؛ `D` لتحديد ما يخص brand شخصيًا أو هوية بصرية أو trust.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/09_personal_branding/_index.md`؛ والـMasters: `Master_Personal_Brand_System.md`, `Master_Brand_Authority_Positioning.md`, `Master_Brand_Identity_System.md`.
- **العدد الموثق فهرسيًا:** 3 Masters؛ 146 مفهومًا مفهرسًا (31 + 75 + 40).
- **subdomains أولية:** `personal_brand_strategy`، `brand_identity`، `authority_and_positioning`، `voice_and_consistency`، `audience_trust`، `brand_growth`.
- **dependencies مقترحة:** `brand_identity → personal_branding` (`prerequisite` داخل graph)، `brand_authority_positioning → trust_authority` (`feeds`)، و`personal_branding → content_strategy` (`feeds`).
- **سبب الاحتياج:** البراند الشخصي والسلطة والهوية طبقة ثقة وتموضع، وقد تتقاطع مع content وvisual design دون أن تصبح أيًا منهما.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.10 `psychology_influence`

- **`canonical_cluster`:** `10_psychology_influence`
- **`proposed_domain_id`:** `psychology_influence`.
- **حالة الدليل:** `I`؛ `S~` في `raw/new/` بسبب psychology/neuroscience/influence/behavior؛ `D` لتحديد نطاق الدليل والأخلاقيات وعدم تحويل النصائح إلى claims عامة.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/10_psychology_influence/_index.md` و`Master_Psychology_Influence.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 105 مفاهيم مفهرسة؛ 15 قسمًا مفهرسًا في graph (مع فجوة ترقيم ظاهرة لا يعالجها هذا التقرير).
- **subdomains أولية:** `decision_psychology`، `influence_principles`، `attention_and_behavior`، `persuasion_ethics`، `social_proof_and_framing`، `applications_to_sales_and_content`.
- **dependencies مقترحة:** `psychology_influence → sales` كسياق `prerequisite` لـ`high_ticket_closing` على مستوى Master؛ وصلات سياقية إلى `hooks_attention` و`storytelling` تحتاج تحققًا.
- **سبب الاحتياج:** مبادئ السلوك والتأثير تُستخدم عبر عدة مجالات، ووجودها كعنقود مستقل يمنع تكرارها بلا حدود أو نسبتها تلقائيًا إلى sales/content.
- **مقارنة المصادر:** `raw/new=S~`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.11 `entrepreneurship_mindset`

- **`canonical_cluster`:** `11_mindset`
- **`proposed_domain_id`:** `entrepreneurship_mindset` — أكثر أمانًا من `mindset` العام.
- **حالة الدليل:** `I`؛ `S~` في `raw/new/` بسبب mindset/discipline/goals/failure/momentum؛ `D` للفصل بين تجربة شخصية ونصيحة عامة.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/11_mindset/_index.md` و`Master_Entrepreneurship_Mindset.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 67 مفهومًا مفهرسًا؛ 40 قسمًا.
- **subdomains أولية:** `entrepreneurial_identity`، `discipline_and_consistency`، `resilience_and_failure`، `goal_setting_and_momentum`، `focus_and_energy`، `decision_making`.
- **dependencies مقترحة:** `entrepreneurship_mindset → foundation_business_strategy` (`complements`). لا يُستنتج منه dependency على نتائج مالية أو business claims دون قراءة الأدلة.
- **سبب الاحتياج:** سلوك المؤسس والانضباط والهوية التشغيلية ليست استراتيجية سوق أو نظام مبيعات، لكنها تؤثر في فهم تلك الأنظمة وتحتاج حدودًا مستقلة.
- **مقارنة المصادر:** `raw/new=S~`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.12 `trust_authority`

- **`canonical_cluster`:** `12_trust_authority`
- **`proposed_domain_id`:** `trust_authority`.
- **حالة الدليل:** `I`؛ `S~` في `raw/new/` بإشارات trust/authority/proof/testimonials بصورة متفرقة؛ `D` مرتفع لتحديد الأدلة الفعلية للثقة.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/12_trust_authority/_index.md` و`Master_Trust_And_Authority.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 23 مفهومًا مفهرسًا؛ 18 قسمًا.
- **subdomains أولية:** `credibility_signals`، `authority_building`، `proof_and_testimonials`، `reliability_and_transparency`، `trust_in_sales_and_content`، `risk_reduction`.
- **dependencies مقترحة:** `brand_authority_positioning → trust_authority` (`feeds`) و`trust_authority → sales` كسياق `feeds` إلى `high_ticket_closing`.
- **سبب الاحتياج:** الثقة والسلطة نتيجة أدلة وسياق وعلاقة مخاطرة؛ لا ينبغي اختزالها في branding أو persuasion أو ضمان سعر.
- **مقارنة المصادر:** `raw/new=S~`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.13 `agency_scaling`

- **`canonical_cluster`:** `13_agency`
- **`proposed_domain_id`:** `agency_scaling` — يزيل الالتباس مع `13_agency_ops`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب agency/scale/MRR/team/growth؛ `D` للفصل بين النموذج التشغيلي والتوسع.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/13_agency/_index.md` و`Master_Agency_Scaling_Systems.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 54 مفهومًا مفهرسًا؛ 70 قسمًا.
- **subdomains أولية:** `agency_model`، `service_delivery_scaling`، `team_and_capacity`، `client_portfolio`، `profitability_and_growth`، `leadership_and_delegation`.
- **dependencies مقترحة:** `agency_operations → agency_scaling` (`prerequisite`). صلات contextual إلى `outreach` و`sales` و`pricing_offers` تحتاج قراءة ملكية المصدر.
- **سبب الاحتياج:** التوسع التجاري للأيجنسي يجيب عن كيف تنمو القدرة والإيرادات، وليس كيف تُدار كل عملية تسليم يومية.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.14 `agency_operations`

- **`canonical_cluster`:** `13_agency_ops`
- **`proposed_domain_id`:** `agency_operations`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب operations/SOP/workflow/client onboarding/team delivery؛ `D` للفصل بين التشغيل والتوسع.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/13_agency_ops/_index.md` و`Master_Agency_Operations.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 48 مفهومًا مفهرسًا؛ 18 قسمًا.
- **subdomains أولية:** `operations_design`، `sops_and_workflows`، `client_onboarding`، `quality_control`، `team_management`، `delivery_and_reporting`.
- **dependencies مقترحة:** `systems_workflow → agency_operations` (`feeds`) و`agency_operations → agency_scaling` (`prerequisite`).
- **سبب الاحتياج:** العمليات اليومية، التسليم، الجودة، onboarding، والـSOPs قابلة للاسترجاع كطبقة مستقلة عن قرارات النمو والتوسع.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.15 `business_models`

- **`canonical_cluster`:** `14_business_models`
- **`proposed_domain_id`:** `business_models`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب online business/coaching/digital products/creator economy/monetization؛ `D` للفصل بين نموذج الأعمال والعرض المحدد.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/14_business_models/_index.md`؛ والـMasters: `Master_Business_Models.md` و`Master_Digital_Products_Coaching.md`.
- **العدد الموثق فهرسيًا:** 2 Masters؛ 81 مفهومًا مفهرسًا (38 + 43).
- **subdomains أولية:** `business_model_types`، `creator_economy`، `service_models`، `digital_products`، `coaching_and_education`، `monetization_and_recurring_revenue`.
- **dependencies مقترحة:** `niche_positioning → business_models` (`prerequisite`) و`business_models → pricing_offers` (`prerequisite`)، و`business_models` يغذي `funnels_conversion` عبر Master المنتجات الرقمية/التدريب.
- **سبب الاحتياج:** يحدد كيف تُخلق الإيرادات وتُسلّم القيمة على مستوى النموذج، وهو أوسع من تسعير باقة واحدة أو بناء funnel واحد.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.16 `funnels_conversion`

- **`canonical_cluster`:** `15_funnels_conversion`
- **`proposed_domain_id`:** `funnels_conversion`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب funnel/sales funnel/conversion/landing page/backend/ascension؛ `D` لتحديد حدود funnel مقابل sales process أو content.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/15_funnels_conversion/_index.md` و`Master_Funnel_Systems.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 114 مفهومًا مفهرسًا؛ 18 قسمًا.
- **subdomains أولية:** `funnel_architecture`، `traffic_and_entry_points`، `lead_magnets_and_nurture`، `conversion_pages_and_sales_process`، `backend_and_ascension`، `funnel_metrics_and_optimization`.
- **dependencies مقترحة:** `pricing_offers → funnels_conversion`، `content_strategy → funnels_conversion`، `marketing_strategy → funnels_conversion`، و`business_models → funnels_conversion` (`feeds` على مستوى Masters).
- **سبب الاحتياج:** يربط نقاط الدخول بالتغذية والتحويل والـbackend، وهو مسار نظامي لا يساوي مجرد رسالة أو عرض أو post.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.17 `growth_frameworks`

- **`canonical_cluster`:** `16_growth_frameworks`
- **`proposed_domain_id`:** `growth_frameworks`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب marketing/growth/strategy/framework/scale؛ `D` للفصل بين إطار استراتيجي عام وتنفيذ channel أو funnel.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/16_growth_frameworks/_index.md`؛ والـMasters: `Master_Marketing_Strategy.md` و`Master_Strategic_Frameworks.md`.
- **العدد الموثق فهرسيًا:** 2 Masters؛ 164 مفهومًا مفهرسًا (42 + 122).
- **subdomains أولية:** `marketing_strategy`، `strategic_frameworks`، `growth_loops`، `competitive_advantage`، `experimentation_and_prioritization`، `resource_allocation`.
- **dependencies مقترحة:** `metrics_analytics → growth_frameworks` (`feeds` إلى `Master_Strategic_Frameworks`)؛ `marketing_strategy → funnels_conversion` (`feeds`).
- **سبب الاحتياج:** يوفر مستوى تركيب ومفاضلة أعلى من تكتيك منصة أو funnel مفرد، مع ضرورة إبقاء الأطر قابلة للتتبع لا شعارات عامة.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.18 `market_research_validation`

- **`canonical_cluster`:** `17_niche`
- **`proposed_domain_id`:** `market_research_validation` — أوضح من `niche` العام.
- **حالة الدليل:** `I`؛ `S~` في `raw/new/` بسبب market/niche/research/validation/customer/problem؛ `D` لتحديد ما هو بحث فعلي وما هو تجربة شخصية أو رأي.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/17_niche/_index.md` و`Master_Market_Research_Validation.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 48 مفهومًا مفهرسًا؛ 18 قسمًا.
- **subdomains أولية:** `market_research`، `customer_problem_validation`، `demand_signals`، `competitor_analysis`، `research_methods_and_interviews`، `validation_decisions`.
- **dependencies مقترحة:** `foundation_business_strategy → market_research_validation` (`prerequisite`) و`market_research_validation → niche_positioning` (`feeds`).
- **سبب الاحتياج:** يثبت أو يختبر فهم السوق والمشكلة قبل اختيار niche أو نموذج عمل؛ لذلك لا ينبغي اختزاله في positioning أو lead generation.
- **مقارنة المصادر:** `raw/new=S~`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.19 `niche_positioning`

- **`canonical_cluster`:** `17_niche_positioning`
- **`proposed_domain_id`:** `niche_positioning`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب niche/ICP/positioning/ideal client/market focus؛ `D` للفصل بين البحث والقرار الاتصالي.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/17_niche_positioning/_index.md` و`Master_Niche_And_Positioning.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 91 مفهومًا مفهرسًا؛ 24 قسمًا.
- **subdomains أولية:** `niche_selection`، `icp_and_segment_definition`، `positioning_statement`، `differentiation`، `category_and_market_context`، `messaging_alignment`.
- **dependencies مقترحة:** `market_research_validation → niche_positioning` (`feeds`) و`niche_positioning → business_models` (`prerequisite`).
- **سبب الاحتياج:** يحول معرفة السوق إلى اختيار شريحة ورسالة وتموضع، وهو حد مستقل عن البحث الخام وعن كتابة message لقناة outreach.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.20 `platform_strategy`

- **`canonical_cluster`:** `18_platforms_algorithm`
- **`proposed_domain_id`:** `platform_strategy`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب social media/algorithm/Instagram/TikTok/LinkedIn/distribution؛ `D` للفصل بين strategy العامة ومادة platform-specific.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/18_platforms_algorithm/_index.md` و`Master_Platform_Strategy.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 373 مفهومًا مفهرسًا؛ 19 قسمًا.
- **subdomains أولية:** `platform_selection`، `algorithm_signals`، `distribution_mechanics`، `cross_platform_systems`، `platform_metrics`، `risk_and_policy_constraints`.
- **dependencies مقترحة:** `content_production → platform_strategy` (`feeds`)؛ `platform_strategy → youtube_strategy` (`complements`). يلزم فحص مستقل لأي ادعاء خوارزمي زمني.
- **سبب الاحتياج:** سلوك المنصات وقواعد التوزيع والقياس يتغير عن content strategy، ويحتاج سياق منصة وتاريخًا وحدودًا واضحة.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.21 `youtube_strategy`

- **`canonical_cluster`:** `19_youtube`
- **`proposed_domain_id`:** `youtube_strategy`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب YouTube/channel/subscribers/thumbnails/video funnel؛ `D` لتحديد ما هو استراتيجية YouTube وما هو video production عام.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/19_youtube/_index.md` و`Master_YouTube_Strategy.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 82 مفهومًا مفهرسًا؛ 18 قسمًا.
- **subdomains أولية:** `youtube_positioning`، `channel_strategy`، `video_packaging_titles_thumbnails`، `discovery_and_search`، `retention_and_publishing`، `youtube_monetization_and_funnels`.
- **dependencies مقترحة:** `platform_strategy → youtube_strategy` (`complements`)؛ `content_production → platform_strategy` upstream غير مباشر.
- **سبب الاحتياج:** YouTube حالة منصة متخصصة ذات بحث وتغليف واحتفاظ وتحويل، ولا يكفي وضعها داخل platform العام إذا أثبتت القراءة اختلاف الاحتياجات.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.22 `ai_automation`

- **`canonical_cluster`:** `20_ai_automation`
- **`proposed_domain_id`:** `ai_automation`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب AI/Claude/agents/automation/n8n؛ `D` لتحديد الأدوات والمخرجات والضوابط وعدم مساواة tutorial بclaim أداء.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/20_ai_automation/_index.md` و`Master_AI_And_Automation.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 41 مفهومًا مفهرسًا؛ 18 قسمًا.
- **subdomains أولية:** `ai_use_cases`، `workflow_automation`، `agentic_systems`، `prompt_and_tooling`، `human_in_the_loop`، `risks_and_governance`.
- **dependencies مقترحة:** `ai_automation → systems_workflow` (`complements`). الروابط إلى outreach أو content أو agency تحتاج فصلًا بين أداة مساعدة وdomain معرفي.
- **سبب الاحتياج:** الأتمتة طبقة تمكين عابرة للمجالات مع مخاطر وقرارات human-in-the-loop؛ فصلها يمنع خلط الأداة بالنتيجة التجارية.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.23 `metrics_analytics`

- **`canonical_cluster`:** `21_metrics`
- **`proposed_domain_id`:** `metrics_analytics`.
- **حالة الدليل:** `I`؛ `S~` في `raw/new/` بسبب analytics/reporting/metrics/attribution/results؛ `D` لتعريف denominator والسياق والتمييز بين تقرير وملاحظة.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/21_metrics/_index.md` و`Master_Metrics_And_Analytics.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 36 مفهومًا مفهرسًا؛ 19 قسمًا مفهرسًا في graph.
- **subdomains أولية:** `metric_definitions`، `funnel_and_conversion_metrics`، `leading_and_lagging_indicators`، `experimentation_and_attribution`، `dashboards_and_reporting`، `decision_loops`.
- **dependencies مقترحة:** `metrics_analytics → growth_frameworks` (`feeds` إلى `Master_Strategic_Frameworks`). قد تغذي القياسات كل مجال، لكن لا تُنسب أرقام raw قبل قراءة موضعها ونوعها.
- **سبب الاحتياج:** القياس والتعريفات والـdenominators طبقة تحقق مشتركة، وليست مجرد قسم داخل marketing أو outreach.
- **مقارنة المصادر:** `raw/new=S~`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.24 `systems_workflow`

- **`canonical_cluster`:** `22_systems_workflow`
- **`proposed_domain_id`:** `systems_workflow`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب systems/workflow/SOP/process/productivity/deep work؛ `D` لفصل process design عن نصيحة productivity العامة.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/22_systems_workflow/_index.md`؛ والـMasters: `Master_Systems_And_Workflow.md` و`Master_Productivity_Deep_Work_Systems.md`.
- **العدد الموثق فهرسيًا:** 2 Masters؛ 108 مفاهيم مفهرسة (70 + 38).
- **subdomains أولية:** `process_design`، `workflow_documentation`، `sops_and_automation`، `productivity_and_deep_work`، `handoffs_and_controls`، `continuous_improvement`.
- **dependencies مقترحة:** `productivity_deep_work → systems_workflow` (`complements` داخل العنقود) و`ai_automation → systems_workflow` (`complements`)، ثم `systems_workflow → agency_operations` (`feeds`).
- **سبب الاحتياج:** توثيق العمليات وتسليماتها وضوابطها بنية تشغيلية تعبر agency وغيرها، ولا ينبغي أن تضيع داخل Master واحد خاص بالأيجنسي.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.25 `visual_identity_design`

- **`canonical_cluster`:** `23_design_visual`
- **`proposed_domain_id`:** `visual_identity_design`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب logo/visual identity/design/Canva/brand assets؛ `D` لتحديد هل الملف tutorial تصميم أم دليل هوية قابل للتعميم.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/23_design_visual/_index.md` و`Master_Visual_Identity_Design.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 110 مفاهيم مفهرسة؛ 24 قسمًا.
- **subdomains أولية:** `brand_visual_identity`، `logo_and_symbol`، `color_and_typography`، `design_systems`، `applications_and_assets`، `briefs_and_reviews`.
- **dependencies مقترحة:** `visual_identity_design → content_production` (`complements`)؛ وعلاقة `brand_identity → personal_branding` تبقى ضمن cluster branding وتحتاج عدم خلط المعرفات.
- **سبب الاحتياج:** الهوية المرئية ونظم التصميم والـassets لها أدلة وقرارات مختلفة عن personal brand النصي أو إنتاج الفيديو.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

### 5.26 `foundation_business_strategy`

- **`canonical_cluster`:** `24_foundation_business`
- **`proposed_domain_id`:** `foundation_business_strategy`.
- **حالة الدليل:** `I`؛ `S+` في `raw/new/` بسبب broad business/strategy/fundamentals/online business؛ `D` مرتفع لأن الاتساع قد يجعل الملف جامعًا أكثر من اللازم.
- **المسار المرجعي:** `/sdcard/Nexus_Brain/nexus_vault/24_foundation_business/_index.md` و`Master_Foundation_Business_Strategy.md`.
- **العدد الموثق فهرسيًا:** 1 Master؛ 253 مفهومًا مفهرسًا؛ 32 قسمًا.
- **subdomains أولية:** `business_fundamentals`، `strategy_and_positioning`، `market_and_customer`، `offer_and_revenue`، `operations_and_growth`، `execution_and_decision_making`.
- **dependencies مقترحة:** `entrepreneurship_mindset → foundation_business_strategy` (`complements`) و`foundation_business_strategy → market_research_validation` (`prerequisite`). لا يُستخدم كحاوية تلقائية لكل ملف business واسع قبل قراءة دلالية.
- **سبب الاحتياج:** يوفر سياقًا تأسيسيًا للمفاهيم والقرارات، لكن اتساعه يستلزم حدودًا وsubdomains صارمة حتى لا يصبح بديلًا عن كل domains الأخرى.
- **مقارنة المصادر:** `raw/new=S+`؛ `raw/legacy/brain=U(0 files)`؛ `raw/legacy/chats=U`؛ `raw/context=U`؛ `brain=U`؛ `nexus_vault=I`.

## 6. مجالات/عناقيد مستنتجة من أسماء وبنية المصادر فقط

هذه ليست إضافات إلى catalog الحالي، وليست عناقيد canonical جديدة. هي مجموعات موضوعية تظهر كإشارات متكررة في أسماء `raw/new/` أو في حدود Masters، وقد تصبح subdomains داخل أحد الـ26 أو domains منفصلة فقط بعد قراءة دلالية ومراجعة التداخل:

| مرشح بنيوي مؤقت | لماذا ظهر في أسماء/بنية المصادر | المالك الأولي المحتمل | القرار الحالي |
|---|---|---|---|
| `linkedin_outreach` | إشارات LinkedIn وSales Navigator وconnection messages وautomation | `outreach` | subdomain مرشح؛ ليس domain canonical مستقلًا |
| `cold_calling_and_sms` | إشارات cold calls وSMS وsetters تظهر بجانب email | `outreach` أو `sales` | حدود الملكية تحتاج `cross_domain_review` |
| `email_deliverability_infrastructure` | SPF/DKIM/DMARC وwarm-up وinbox وdomains | `outreach` | subdomain واضح بنيويًا، لا قبول دلالي بعد |
| `lead_scraping_and_enrichment` | Apollo/Clay/Sales Navigator/scraping/enrichment | `outreach` | يحتاج فصل sourcing عن automation وعن privacy |
| `short_form_video` | reels/TikTok/short-form/editing | `content_production` | مرشح subdomain، لا يساوي platform strategy |
| `copywriting_and_vsl` | script/copy/VSL/CTA/templates | `copywriting_scripts` | مرشح subdomain؛ يجب فصل sales copy عن content copy |
| `platform_specific_growth` | Instagram/TikTok/LinkedIn/YouTube/algorithm | `platform_strategy` | قد تبقى subdomains منصية |
| `coaching_and_digital_products` | coaching/info products/course sellers | `business_models` | موجود كإشارة داخل Master قديم، وليس domain جديدًا |
| `ai_agents_and_business_automation` | Claude/AI agents/n8n/automation | `ai_automation` | مرشح subdomain؛ لا تُثبت النتائج التجارية من العنوان |
| `brand_visual_assets` | logos/Canva/visual identity/brand design | `visual_identity_design` | subdomain مرشح مع صلة بـ`personal_branding` |
| `analytics_attribution_reporting` | metrics/analytics/reporting/attribution | `metrics_analytics` | يحتاج تعريف المقاييس والدينومينيتور |
| `agency_delivery_operations` | agency operations/client onboarding/SOPs | `agency_operations` | مرشح subdomain واضح، لا يُدمج تلقائيًا مع scaling |

القاعدة هنا: **الاسم يرشح القراءة ولا يحكم التصنيف**. لا تُنشأ domains جديدة لهذه القائمة ولا تُسجّل Claims/Concepts بناءً عليها.

## 7. ما يحتاج قراءة دلالية قبل أي اعتماد

ينبغي أن يبقى كل ما يلي في حالة `D`/غير محسوم حتى تنفذ قراءة قابلة للتتبع:

1. إسناد أي ملف من `raw/new/` إلى `primary_domain` و`primary_subdomain`؛ الاسم قد يكون عنوانًا تسويقيًا أو مثالًا أو نسخة مكررة.
2. تحديد ما إذا كانت ملفات `raw/legacy/chats/` و`raw/context/` مصادر معرفة، تعليمات تشغيل، أو سياقًا لا يدخل denominator.
3. مطابقة `/sdcard/Nexus_Brain/brain/` مع `raw/new/` بالهوية والبصمة قبل احتساب أي مصدر أو استنتاج تكرار.
4. فصل `sales` عن `outreach` عند الحديث عن lead أو follow-up، وفصل `sales` عن `pricing_offers` عند الحديث عن اعتراض السعر.
5. فصل `content_strategy` عن `content_production` و`copywriting_scripts` و`hooks_attention` و`platform_strategy`.
6. اختبار ما إذا كان `foundation_business_strategy` سياقًا جامعًا أم عنقودًا يحتاج تقليصًا؛ لا يُستخدم لامتصاص المجالات الأخرى.
7. تحديد ما إذا كان `agency_scaling` و`agency_operations` domainين مستقلين أم طبقتين تحت مجال agency واحد.
8. التحقق من كل dependency المقترحة على مستوى Claims/Concepts لا على أسماء Masters فقط.
9. إنشاء snapshot شامل لكل domain قبل أي `domain_terms_complete` أو Master جديد، وفق schema والميثاق؛ هذا التقرير لا ينفذ تلك البوابات.

## 8. حدود التقرير وما لا يدعيه

- لا يدعي التقرير أن كل مصدر في المسارات الستة صُنّف أو قُرئ دلاليًا.
- لا يدعي أن أي domain من الـ26 مكتمل، أو أن أي Master قديم صالح تلقائيًا كمعرفة جديدة، أو أن أرقام Concepts تغطي corpus الحالي.
- لا يدعي أن المجالات المقترحة تمثل taxonomy نهائية؛ قد يدمج الفحص اللاحق بعضها أو يحول بعضها إلى subdomains.
- لا يدعي وجود مصدر داخل `raw/legacy/brain/`؛ القياس الموثق هو صفر ملفات عادية، لا حكم على الأدلة الفرعية.
- لا يرفع `route_done` أو أي إشارة اسمية إلى `source_done` أو `domain_done`.
- لا يغيّر `config/domain_catalog.json` أو `config/processing_order.json`، ولا يضيف سجلًا في `claims/` أو `concepts/` أو `masters/`.

## 9. مراجع القراءة

| المرجع | موضع الاستعمال |
|---|---|
| `/sdcard/NEXUS_LLM_WIKI/reports/CORPUS_INVENTORY_SCOPE_2026-10-11.md` | قياس المصادر الستة، الأعداد، الأحجام، وحدود الجرد |
| `/sdcard/NEXUS_LLM_WIKI/AGENTS.md` | immutable raw، حدود الكتابة، الفرق بين routing وknowledge، وعدم إعلان الاكتمال |
| `/sdcard/NEXUS_LLM_WIKI/SCHEMA.md` | أشكال Source/Claim/Concept/Master، snapshots، gates، وقيود التتبع |
| `/sdcard/NEXUS_LLM_WIKI/MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md` | الموجة الأولى، القفل التسلسلي، الطبقات، ومعاني R/T/C/K/M/QA |
| `/sdcard/NEXUS_LLM_WIKI/config/domain_catalog.json` | domains الأربعة الحالية، subdomains الأولية، سياسة المصدر، وحدود Vault المرجعي |
| `/sdcard/NEXUS_LLM_WIKI/config/processing_order.json` | ترتيب المعرفة الحالي وحالاته وشروط فتح المجال التالي |
| `/sdcard/Nexus_Brain/nexus_vault/BRAIN_INDEX.md` | 26 عناقيد، 39 Masters، وأرقام Concepts/Sections المفهرسة |
| `/sdcard/Nexus_Brain/nexus_vault/MASTER_GRAPH.json` | 39 عقدة، 32 علاقة، وأسماء/مسارات Masters والعلاقات المقترحة |
| `*/_index.md` داخل `/sdcard/Nexus_Brain/nexus_vault/` | قوائم Masters canonical لكل عنقود؛ `_archive/` مستبعد |

**الخلاصة التشغيلية:** هذا الملف يسلّم قائمة مرشحة قابلة للمراجعة، لا catalog معتمدًا. الخطوة التالية المسموح بها هي مراجعة Commander لنطاق domains والحدود، ثم قراءة دلالية بمصادر ومواضع قبل أي تعديل config أو تصنيع معرفة.
