# COVERAGE_MATRIX — من المغطّى، ومن عليه البناء

<!-- counts-ref: V3_SYS/COUNTS.json -->
<!-- atoms=27742 concepts=1841 masters=5 -->

> **سؤال هذا الملف الواحد:** لكل قطاع — كم مفهوماً خماسياً، كم ذرّة، كم منها مغطّى بماستر قائم، و**ما هي أسماء غير المغطّى بالحرفي**؟
> **الأرقام:** `MASTER_QUEUE.md §1` (الأوامر) · **الترتيب:** `MASTER_QUEUE.md §2` · **حدود القطاعات:** `SECTOR_MAP.md`.
> **قاعدة `{formula}` بلا حدّ فناء تسقط** (`FORMAT_MASTER.md` §1.2). لذلك قوائم §18 في كل ماستر يجب أن تُبنى من هذه القوائم — ومن **لا** يُبنى من اسم ملف حقيقي يتحوّل إلى جدول أسماء ميت.

---

## 0) قاعدة التغطية المستعملة — مُعلَنة قبل الجداول

**«مغطّى» تعني:** اسم المفهوم ورد **حرفياً** في جدول §18 من ماستر القطاع. لا تعني اجتياز بند 5 (`DO_MASTER.md §5`).

**السبب مُقاس:** `grep -o '\[\[C_[^]]*\]\]'` على الماسترات الخمسة = **0** ⇒ لا رابط واحد ⇒ بند 5 يسقط على الخمسة معاً.

**الأثر:** «مغطّاة 697» رقم **اسمي** لا رقم بوابة. لو عُدّ المتروك صفراً لأصبح خمس الوحدات من الجهد مهدوراً.

```bash
# الأمر الذي يولّد قوائم «غير المغطّى» — قابل للتكرار لكل قطاع
S=02_sales_calls
cd /root/r/NB2/02_CONCEPTS
find "$S" -maxdepth 1 -name 'Concept_*.md' | sed 's|.*/||; s|\.md$||' | sort -u > /tmp/f.txt
awk '/^## §18/{f=1;next} /^## §/{f=0} f' /root/r/NB2/03_MASTERS/$S/Master_*.md \
  | grep -o '`Concept_[A-Za-z0-9_]*`' | tr -d '`' | sort -u > /tmp/c.txt
comm -23 /tmp/f.txt /tmp/c.txt      # ⇒ غير المغطّى
comm -13 /tmp/f.txt /tmp/c.txt      # ⇒ أسماء في الماستر بلا ملف على القرص (وهة)
```

**اختبار الوَهْة نظيف:** `comm -13` = **صفر** في القطاعات الخمسة ⇒ لا اسم في أي §18 بلا ملف مقابل. النتيجة الوحيدة المتبقّية: 477 مفهوماً على القرص خارج كل §18.

| القياس | القيمة | الأمر |
|---|---:|---|
| مفاهيم خماسية على القرص | **1,836** | `find 02_CONCEPTS -name 'Concept_*.md' -not -path '*terms_26k*' \| wc -l` |
| غيرها في نفس النطاق (ليست مفاهيم) | **5** | `_INDEX.md` + 4 `agent_*.md` في `_REPORTS/` |
| **مجموع المفاهيم غير المغطّاة** | **1,139** | 1,836 − 697 |
| أسماء في §18 بلا ملف على القرص (وَهْة) | **0** | `comm -13` على القطاعات الخمسة |
| ذرّات | **27,742** | `find 02_CONCEPTS/terms_26k -name '*.md' \| wc -l` |

---

## 1) جدول التغطية — 23 قطاعاً

| # | قطاع | مفاهيم | ذرّات | مغطّاة | غير مغطّاة | النسبة | حالة الوحدة |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `02_sales_calls` | 500 | 1,554 | 181 | 319 | 36.2% | 8 عناقيد |
| 2 | `09_agencies_clients` | 80 | 645 | 0 | 80 | 0% | ماستر واحد |
| 3 | `11_marketing_ads` | 63 | 463 | 0 | 63 | 0% | ماستر واحد |
| 4 | `03_offers_pricing` | 166 | 1,018 | 109 | 57 | 65.7% | إغلاق + 1 ماستر |
| 5 | `04_content_strategy` | 60 | 565 | 0 | 60 | 0% | ماستر واحد |
| 6 | `17_ai_automation` | 47 | 984 | 0 | 47 | 0% | ماستر واحد (جذر الشجرة) |
| 7 | `10_funnels` | 41 | 503 | 0 | 41 | 0% | ماستر واحد |
| 8 | `12_growth` | 59 | 463 | 0 | 59 | 0% | ماستر واحد |
| 9 | `01_outreach` | 133 | 4,521 | 124 | 9 | 93.2% | إعادة كتابة الماستر |
| 10 | `06_hooks_retention` | 70 | 340 | 0 | 70 | 0% | ماستر واحد |
| 11 | `05_content_production` | 93 | 109 | 0 | 93 | 0% | ماستر واحد (B=1) |
| 12 | `99_uncategorized` | 25 | 10,064 | 0 | 25 | 0% | **بوابة triage — لا ماستر** |
| 13 | `07_branding` | 175 | 350 | 141 | 34 | 80.6% | إغلاق + 1 ماستر |
| 14 | `15_platforms_algo` | 18 | 289 | 0 | 18 | 0% | يُدمج مع `16_business_models` |
| 15 | `20_productivity_learning` | 34 | 371 | 0 | 34 | 0% | يُدمج مع `19_operations_teams` |
| 16 | `19_operations_teams` | 33 | 371 | 0 | 33 | 0% | يُدمج مع `20_productivity_learning` |
| 17 | `14_copywriting` | 7 | 1,245 | 0 | 7 | 0% | يُدمج مع `13_storytelling` |
| 18 | `13_storytelling` | 11 | 344 | 0 | 11 | 0% | يُدمج مع `14_copywriting` |
| 19 | `08_mindset` | 200 | 218 | 142 | 58 | 71.0% | إغلاق + 1 ماستر |
| 20 | `16_business_models` | 12 | 126 | 0 | 12 | 0% | يُدمج مع `15_platforms_algo` |
| 21 | `22_finance_legal` | 4 | 468 | 0 | 4 | 0% | يُدمج مع `21` + `23` |
| 22 | `21_persuasion_psych` | 3 | 174 | 0 | 3 | 0% | يُدمج مع `21` + `23` |
| 23 | `18_trust_authority` | 2 | 324 | 0 | 2 | 0% | يُدمج مع `21` + `22` |
| | **المجموع** | **1,836** | **25,509** | **697** | **1,139** | **38.0%** | **18 وحدة ماستر** |

> عمود «ذرّات» = الذرّات **المربوطة** (25,509) لا ذرّات القرص (27,742). الفارق 2,233 مُفصَّل في `MASTER_QUEUE.md §2.1`: 3,067 ذرّة في 7 قطاعات بلا مقابل خماسي، و‎−834 ازدواج.

---

## 2) القطاعات ذات الماستر القائم — القوائم الحرفية

### 2.1 `02_sales_calls` — 500 مفهوم · مغطّاة 181 · **غير مغطّاة 319**

**الأول 20 من 319** (الترتيب أبجدي، ثابت):

```
Concept_AnswerFirstQuestionDesign        Concept_CurrentProcessBlame
Concept_AssertiveAskStack                Concept_Current_Strategy_Attribution
Concept_AttractiveServiceSelection       Concept_CustomerAwarenessJourney
Concept_AuthenticScarcity                Concept_Deal_Timing_Discipline
Concept_Authentic_Frame_Selection        Concept_DeservingnessPricing
Concept_AvatarMatchedTestimonial         Concept_DesignCredibilitySignal
Concept_AvatarTestimonialLibrary         Concept_DirectPromoBillboard
Concept_BackendConversionStack           Concept_DirectionOverVolume
Concept_BeliefBeforeOffer                Concept_Discovery_Depth_As_Frame
Concept_BetweenCallPriming               Concept_Discovery_Pressure_Probes
Concept_BonusArchitecture                Concept_Discovery_Stage_Formula
Concept_BonusValueOverstack              Concept_DisguisedQualification
Concept_Burnout_Perception_Reframe       Concept_DisqualificationPositioning
Concept_BusinessSkillStack               Concept_DollarPerLeadNorthStar
Concept_BusinessSkillsMultiplier         Concept_Dream_Goal_Quantification
Concept_BusynessHerdSignal               Concept_DualCertaintyArchitecture
Concept_BuyingEnergyPressureTest         Concept_DualDirectionMotivation
```

**بقية الـ299** في `MASTER_BUILD_ORDER.md §2` (مجمّعة في 8 عناقيد) — وتُقتطع حرفياً بالأمر في §0 عند كل عنقود.
**عيّب على وحدة التغطية:** الـ319 غير مغطّاة **لا توجد في أي مكان آخر كمصفوفة**؛ §18 الماستر القائم يذكر 181 فقط. ⇒ هذه القائمة هي المرجع الوحيد لباقي القطاع.

### 2.2 `03_offers_pricing` — 166 مفهوم · مغطّاة 109 · **غير مغطّاة 57** (القائمة كاملة)

```
Concept_AgenticAppGeneration             Concept_MVP_Sprint_Map
Concept_AscensionLadderEcosystem         Concept_MicroNicheSubscriptionMath
Concept_AudienceOfferMismatch            Concept_MinimumLovableProductLaunch
Concept_BetaTestimonialSeeding           Concept_OnePageOfferPlan
Concept_BlueOceanPositioning             Concept_OneToManyLeverage
Concept_BrandDealTouchpointBundling      Concept_OnlynessIntersection
Concept_BuyingIntentLadder               Concept_OrderBumpUpsellDownsell
Concept_BuyingIntentValidation           Concept_OverwhelmReplayUpsell
Concept_CompetitiveEdgeIntersection      Concept_OverwhelmTrap
Concept_ComponentWiseValidation          Concept_PainFirstValidationSurvey
Concept_ConversionRateRealism            Concept_PayoffDestination
Concept_DollarADayAdTesting              Concept_PreBuildValidationGate
Concept_EarnedTrustValueFirst            Concept_PresellDeliveryPromise
Concept_EnjoymentOverSkill               Concept_PriceLadderPsychology
Concept_FeedbackDiscernmentThreshold     Concept_PricingAsSignal
Concept_FourP_ScopeLimiter               Concept_ProductLadderFlywheel
Concept_FreemiumToValueLadder            Concept_PromoInventoryOpportunityCost
Concept_GrindVsEmpireMindset             Concept_QuickWinOffer
Concept_ImplementationGapAccountability  Concept_SawdustOfferSpinoffs
Concept_LeadMagnetAmuseBouche            Concept_SelfLiquidatingOffer
Concept_LowFrictionSubscriptionPricing   Concept_SelfLiquidatingOfferTesting
Concept_SevenEndingPriceLadder           Concept_TimeboxedQuickWinFormat
Concept_ShipToLearnFeedback              Concept_ValueAbovePaywall
Concept_SmallNicheSubscriptionMath       Concept_ValueFirstWaitlist
Concept_SpecialistGPTChain               Concept_ValueLadderEcosystem
Concept_SpecialistGptSwarm               Concept_VibeCodedValidationApp
Concept_TeachNotSellDelivery             Concept_ViewerContextIllusion
Concept_TechMinimalValidation            Concept_Value_Based_Pricing  ← ملاحظة أدناه
Concept_TechStackMinimization
Concept_ThreeCircleSweetSpot
```

> **تحقّق صفر وَهْة:** `comm -13` على هذا القطاع = **صفر** ⇒ لا اسم في §18 بلا ملف على القرص. القائمة أعلاه مطابقة للأمر حرفاً (57/57).

### 2.3 `08_mindset` — 200 مفهوم · مغطّاة 142 · **غير مغطّاة 58** (القائمة كاملة)

```
Concept_AccountabilityMultiplier         Concept_Milestone_Celebration_Rituals
Concept_Action_Before_Confidence         Concept_MomentumStreakGate
Concept_Activity_Over_Training           Concept_Negative_Story_Fuel
Concept_AmbitionContentmentAnd           Concept_NoveltyTimeExpansion
Concept_BoundaryAlignedBusiness         Concept_Obsession_Follows_Action
Concept_CelebrationRituals               Concept_OnePercentConversionNorm
Concept_ChampionCircle                   Concept_OsmosisContentDiet
Concept_CognitiveResourceConservation    Concept_ParticipationPyramid
Concept_ConditionedAutomation            Concept_Past_Future_Self_Command
Concept_CreatorScalingCeiling            Concept_PerfectDayCompass
Concept_Creator_Seasons                  Concept_Perfect_Day_Path_Audit
Concept_EmployerTransparencyFraming      Concept_PersonalBrandLeverageAsset
Concept_EnergyAsState                    Concept_PlatformDependencyRisk
Concept_EnergyAwareLaunchPlan            Concept_Platform_Dependency_Collapse
Concept_FeedbackDiscernmentFilter        Concept_ProcessVarianceDiscipline
Concept_FocusOverMultiplexing            Concept_Process_Not_Identity
Concept_Fun_First_Sequencing             Concept_Proximity_Is_Power
Concept_Habit_Loop_Design                Concept_ScalingCeiling
Concept_HourlyWorkFormAudit              Concept_Shame_Free_Failure_Loop
Concept_HumanInTheLoopGate               Concept_ShipBeforeReady_ForcingFunctions
Concept_ICE_Engagement_Quota             Concept_SmallLoyalAudience
Concept_IdeationStation                  Concept_SoftLaunchBufferRoadmap
Concept_InternalFirstGrowth              Concept_SomaticAnchorConditioning
Concept_LearnedHelplessnessLocus          Concept_StoryVsFacts
Concept_LizardBrainVsPrefrontal          Concept_StrategicLoneliness
Concept_Mastery_By_Adaptation            Concept_StructureLeadsToSpontaneity
Concept_TimeToExpertiseCurve
Concept_Towards_Why_Framing
Concept_TwoDoListCommitment
Concept_TwoOne_Operating_Rhythm
Concept_UnscalableFirstValidation
Concept_ViralVsPersonalWriting
```

### 2.4 `07_branding` — 175 مفهوم · مغطّاة 141 · **غير مغطّاة 34** (القائمة كاملة)

```
Concept_AssociationLevelUp                Concept_Mind_Share_Movement
Concept_AttentionHighlightQuestion       Concept_NicheSpecificityReferral
Concept_Audience_Concretization          Concept_OnlyStatementPositioning
Concept_BeforeAfterBridge                Concept_PersonalDetailEngagement
Concept_BrandPyramidEmotion              Concept_PersonalProfileOverBusinessPage
Concept_Care_Supremacy                   Concept_PersonalVoiceSnippet
Concept_ContentIsChicken                 Concept_PersonalityOverPerfection
Concept_ContextualPreviewTest            Concept_SemanticColorAssociation
Concept_CoreFourPillars                  Concept_SingleServiceValueFilter
Concept_CoreValuesFilter                 Concept_StateCompressionLegibility
Concept_CredibilityContentMultiplier     Concept_TitleThumbnailSynergy
Concept_CuriosityGapIntensity            Concept_ToneSnippetReuse
Concept_EmotionalDifferentiation         Concept_TwoSecondClarityAssets
Concept_Exclusivity_Claim_Positioning     Concept_VRINPositioning
Concept_ExpertBlindness                  Concept_ViewerUnderstandingSupremacy
Concept_FlavorSpiceDifferentiation       Concept_ViralReplication
Concept_LandingPageProofStack            Concept_WriteLikeYouTalk
```

### 2.5 `01_outreach` — 133 مفهوم · مغطّاة 124 · **غير مغطّاة 9** (القائمة كاملة)

```
Concept_AuthorityCommentPipeline         Concept_EngagementAsWarmLeadSignal
Concept_AuthorityCommenting              Concept_NicheSpecificityReferralTrigger
Concept_BorrowedAudienceValueComments    Concept_OnPlatformFunnel
Concept_BrowserSnapshotMining            Concept_ReferralAskBootstrap
                                          Concept_ReferralAskDeframing
```

**الملاحظة:** 7 من هذه التسعة في عنقود واحد (`AuthorityComment*` · `BorrowedAudienceValueComments` · `EngagementAsWarmLeadSignal` · `NicheSpecificityReferralTrigger`) و2 في عنقود الإسناد (`ReferralAsk*`). ⇒ **وحدة واحدة، وكيل واحد، 9 مفاهيم** — لا تحتاج ماستراً جديداً، بل إعادة كتابة `Master_Outreach_Mechanics.md` ليأخذها.

---

## 3) القطاعات بلا ماستر — العدد كامل، الأسماء عند الطلب

الجداول أعلاه (§1) تحمل العدد الدقيق لكل قطاع. القواس الحرفية كاملة لـ18 قطاعاً (1,132 اسماً) **لم تُطبع هنا** لسببين مذكورَين:

1. **`MASTER_QUEUE.csv`** يحمل الأرقام كاملة، والقوائم تُقتطع بالأمر في §0.
2. **الأولوية العملية:** الطابور يبني `#1 02_sales_calls` و`#2 09_agencies_clients` و`#3 11_marketing_ads` أولاً — وقائمتاهما **حرفية وكاملة في `FIRST_3_MASTERS.md`** لأنهما الوحدات الثلاث الأولى. وطُبعت قوائم القطاعات الخمسة ذات الماستر القائم هنا كاملة لأن كل اسم فيها يجب أن يدخل §18.

**ما هو مطبوع لا غير:** `02_sales_calls` (أول 20 من 319) · `03_offers_pricing` (57 كاملة) · `08_mindset` (58 كاملة) · `07_branding` (34 كاملة) · `01_outreach` (9 كاملة) = **178 اسماً**، وهي كامل ما في الماسترات الخمسة القائمة. و`05_content_production` (93 مفهوماً) هو أكبر قطاع بلا ماستر بعد `#1`، وقائمته تُقتطع بالأمر عند بناء موجته.

---

## 4) جدول التغطية الثاني — على مستوى الذرّات

**لماذا هذا الجدول موجود:** كل صف في §1 يحمل ذرّات قطاع. لكن **3,067 ذرّة (11.1%) في 7 قطاعات ليس لها أي قطاع خماسي** ⇒ لا صف في §1 يقابلها. هذا جدول الفجوة.

| قطاع الذرّات | ذرّات | النسبة من 27,742 | مفهوم خماسي مقابل | وحدة V3 |
|---|---:|---:|---|---|
| `17_niche` | 523 | 1.9% | **لا يوجد** | غير مغطّاة — تدمج في `12_growth` |
| `19_youtube` | 150 | 0.5% | **لا يوجد** | غير مغطّاة — تدمج في `05_content_production` |
| `23_design_visual` | 401 | 1.4% | **لا يوجد** | غير مغطّاة — تدمج في `05_content_production` |
| `24_foundation_business` | 368 | 1.3% | **لا يوجد** | غير مغطّاة — تدمج في `16_business_models` |
| `26_editing_montage` | 364 | 1.3% | **لا يوجد** | غير مغطّاة — تدمج في `05_content_production` |
| `29_instagram_growth` | 939 | 3.4% | **لا يوجد** | غير مغطّاة — تدمج في `11_marketing_ads` |
| `30_leads_generation` | 322 | 1.2% | **لا يوجد** | غير مغطّاة — تدمج في `10_funnels` |
| **المجموع** | **3,067** | **11.1%** | **0** | — |

**قرار التوزيع (مُعلَن، لا متروك):** كل قطاع ذرّات بلا مقابل خماسي يُدمج في القطاع الخماسي الأقرب موضوعاً، **ويُفتح له باب في §18** للمفاهيم الجديدة التي ينتجها. هذا يحوّل 11.1% من الذرّات من «خارج التغطية» إلى «مغطّاة تحت ماستر»، ويزيد عدد مفاهيم `10_funnels` مثلاً من 41 إلى **363** فعلياً — وهو رقم يجب أن يُعاد حساب A عندئذ.

⚠️ **العدد 363 مُشتق لا مقيس:** `41 + 322 = 363` حساباً على الورق. **لم يُبنَ أي مفهوم خماسي من الذرّات بعد** — فالتغطية الحقيقية اليوم **صفر** لهذه الـ3,067، لا 363. الرقم 363 هو **الالتزام المستهدف** لا الواقع.

---

## 5) خلاصة التغطية — ثلاثة أرقام تكفي

| الرقم | القيمة | الدلالة |
|---|---:|---|
| نسبة التغطية الحالية | **38.0%** (697/1,836) | أقل من ثلثي المعرفة الخماسية بلا ماستر |
| نسبة الذرّات بلا قطاع خماسي | **11.1%** (3,067/27,742) | أكبر فجوة هيكلية في V3 |
| نسبة الذرّات بلا تصنيف | **36.3%** (10,064/27,742) | `99_misc` — بوابة triage تحجب كل شيء |

**الخلاصة الواحدة:** الطابور (§2 في `MASTER_QUEUE.md`) يبدأ من **1,139 مفهوماً**، لكن **11.1% من الذرّات** تحتاج بنية قطاع جديدة قبل أن يستطيع أي ماستر أن يذكرها. بناء `#1` و`#2` و`#3` وحدها لا يمسّ أياً منهما.