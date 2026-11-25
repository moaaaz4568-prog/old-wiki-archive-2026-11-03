# تقرير فحص الجودة الآلي — V3_SYS/audit.py

- **الجذر:** `/root/r/NB2`
- **التاريخ:** 2026-10-01T02:36:49+0000
- **الزمن:** 367.38s (مسح 45.26s، قراءة 175.67s، 36195 ملف / 108.8 MB، 1 threads)
- **المفاهيم:** 34865 · **الماسترات:** 5 · **ملفات .md:** 36195 · **إجمالي الملفات:** 37098
- **مجموع الأوزان:** 100

## جدول النتائج

| ID | الفحص | العدد | الخطورة | الوزن | العتبة | الحالة |
|---|---|---:|---:|---:|---|---|
| C01 | روابط [[ ]] معلّقة | 59 | 8 | 7 | 0 | 🔴 مخالفة |
| C02 | كعبات <300 بايت | 164 | 6 | 5 | 0 | 🔴 مخالفة |
| C03 | تكرار حرفي بين concept | 1964 | 7 | 5 | 0 | 🔴 مخالفة |
| C04 | concept بلا اقتباس/مصدر | 129 | 8 | 6 | 0 | 🔴 مخالفة |
| C05 | concept بلا «حدود الفناء» | 27785 | 8 | 6 | 0 | 🔴 مخالفة |
| C06 | concept بلا «الآلية» | 27576 | 7 | 6 | 0 | 🔴 مخالفة |
| C07 | ماستر بأقسام <18 | 0 | 8 | 4 | 0 | ✅ نظيف |
| C08 | concept مكرر الاسم | 0 | 5 | 3 | 0 | ✅ نظيف |
| C09 | قطاع بلا ماستر | 17 | 6 | 3 | 0 | 🔴 مخالفة |
| C10 | شرط §18 (صفوف الجدول = concepts القطاع) | 5 | 8 | 4 | 0 | 🔴 مخالفة |
| C11 | رقم بلا ⚠️ ولا مصدر | 26979 | 6 | 4 | 0 | 🔴 مخالفة |
| C12 | فهرس البحث stale | 1 | 4 | 2 | 0 | 🔴 مخالفة |
| C13 | concept بلا wikilink | 34487 | 5 | 3 | 0 | 🔴 مخالفة |
| C14 | concept بلا الأقسام الستة كاملة | 34861 | 9 | 7 | 0 | 🔴 مخالفة |
| C15 | أسماء مولّدة آلياً | 981 | 4 | 2 | 0 | 🔴 مخالفة |
| C16 | حشو / Ukrainian | 69 | 5 | 2 | 0 | 🔴 مخالفة |
| C17 | ماستر بلا حدود فناء | 0 | 7 | 3 | 0 | ✅ نظيف |
| C18 | بوابات Master SPEC | 1 | 9 | 4 | 4 sub-gates | 🔴 مخالفة |
| C19 | YAML ناقص (---/type/version/sections) | 0 | 6 | 3 | 0 | ✅ نظيف |
| C20 | نسخة مطابقة بين مجلدين (تراجع) | 2173 | 7 | 3 | 0 | 🔴 مخالفة |
| C21 | مجلد >1000 ملف | 1 | 3 | 2 | 0 | 🔴 مخالفة |
| C22 | حجم 99_misc ≤3% من 02_CONCEPTS | 1 | 5 | 2 | ≤3% | 🔴 مخالفة |
| C23 | concept بلا أقسام توتر (تقرير فقط) | 27713 | 0 | 0 | — | ℹ️ تقرير فقط (27713) |
| C24 | concept <250 كلمة | 27264 | 6 | 4 | 0 | 🔴 مخالفة |
| C25 | concept >600 كلمة (≤3%) | 11 | 4 | 2 | ≤3% | 🔴 مخالفة |
| C26 | concept بلا «## المصدرية» | 27641 | 7 | 4 | 0 | 🔴 مخالفة |
| C27 | placeholders (TODO/TBD/XXX) | 8 | 5 | 2 | 0 | 🔴 مخالفة |
| C28 | concepts بلا sources غير فارغ | 7212 | 7 | 2 | 0 | 🔴 مخالفة |
| — | **TOTAL** | **247102** | | **100** | | |

## التفاصيل (حتى 3 مثال لكل فاحص)

### C01 · روابط [[ ]] معلّقة — 59 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `[["Send me more information" Reply]]` | 0 | معلّق في 1 ملف، مثال: 02_CONCEPTS/terms_26k/01_outreach/part_02/Concept_Sentiment_Analysis_For_Replies.md |
| 2 | `[[<المصطلح>]]` | 0 | معلّق في 1 ملف، مثال: 00_SYSTEMS/SYSTEM_02_DEEPENING.md |
| 3 | `[[A]]` | 0 | معلّق في 1 ملف، مثال: 00_SYSTEMS/SYSTEM_02_DEEPENING.md |

> … و56 مخالفة أخرى (راجع JSON؛ محفوظ 59)

### C02 · كعبات <300 بايت — 164 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `00_SYSTEMS/MERGE_SLICES/01_outreach_12of19.auto.md` | 275 | حجم 275B < 300B |
| 2 | `00_SYSTEMS/MERGE_SLICES/02_sales_closing_03of8.auto.md` | 250 | حجم 250B < 300B |
| 3 | `00_SYSTEMS/MERGE_SLICES/02_sales_closing_05of8.auto.md` | 297 | حجم 297B < 300B |

> … و161 مخالفة أخرى (راجع JSON؛ محفوظ 164)

### C03 · تكرار حرفي بين concept — 1964 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/A1/concepts/Concept_AI_Production_Pipeline.md` | 5430 | sha256[:12]=b1b1b94b9803 متطابق في 4 ملف: .nexus_work/stage/A1/concepts/Concept_AI_Production_Pipeline.md | 02_CONCEPTS… |
| 2 | `.nexus_work/stage/A1/concepts/Concept_Access_Ownership_Aggregation.md` | 4485 | sha256[:12]=a779a6af23ba متطابق في 4 ملف: .nexus_work/stage/A1/concepts/Concept_Access_Ownership_Aggregation.md | 02_CO… |
| 3 | `.nexus_work/stage/A1/concepts/Concept_Attention_Economy.md` | 4110 | sha256[:12]=2bcbc9402021 متطابق في 4 ملف: .nexus_work/stage/A1/concepts/Concept_Attention_Economy.md | 02_CONCEPTS/11_m… |

> … و1961 مخالفة أخرى (راجع JSON؛ محفوظ 1964)

### C04 · concept بلا اقتباس/مصدر — 129 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/C6/concepts/Concept_VictimMentalityGrowthBlock.md` | 1627 | لا '## الدليل' ولا backtick ولا 'channel:' |
| 2 | `02_CONCEPTS/08_mindset/Concept_VictimMentalityGrowthBlock.md` | 1627 | لا '## الدليل' ولا backtick ولا 'channel:' |
| 3 | `02_CONCEPTS/terms_26k/99_misc/part_01/Concept_AI_Email_Warmup_(2-Week_Minimum).md` | 224 | لا '## الدليل' ولا backtick ولا 'channel:' |

> … و126 مخالفة أخرى (راجع JSON؛ محفوظ 129)

### C05 · concept بلا «حدود الفناء» — 27785 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/C6/concepts/Concept_VictimMentalityGrowthBlock.md` | 1627 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |
| 2 | `.nexus_work/stage/CT14/concepts/Concept_PrecisionLanguaging.md` | 2971 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |
| 3 | `02_CONCEPTS/02_sales_calls/Concept_PrecisionLanguaging.md` | 2971 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |

> … و27782 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

### C06 · concept بلا «الآلية» — 27576 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | لا يوجد: الآلية / آلية العمل |
| 2 | `02_CONCEPTS/06_hooks_retention/Concept_Curiosity_Gap.md` | 734 | لا يوجد: الآلية / آلية العمل |
| 3 | `02_CONCEPTS/terms_26k/01_outreach/part_01/Concept_0.001_Reply_Rate.md` | 1105 | لا يوجد: الآلية / آلية العمل |

> … و27573 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

### C07 · ماستر بأقسام <18 — 0 مخالفة

### C08 · concept مكرر الاسم — 0 مخالفة
> ℹ️ لا أسماء مكررة


### C09 · قطاع بلا ماستر — 17 مخالفة
> ℹ️ قطاعات: 22 · مغطّاة: 5 · بلا ماستر: 17

| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `04_content_strategy` | 0 | قطاع '04_content_strategy' (60 ملف) بلا ماستر — الماسترات المتاحة: ['01_outreach', '02_sales_calls', '03_offers_pricing… |
| 2 | `05_content_production` | 0 | قطاع '05_content_production' (93 ملف) بلا ماستر — الماسترات المتاحة: ['01_outreach', '02_sales_calls', '03_offers_prici… |
| 3 | `06_hooks_retention` | 0 | قطاع '06_hooks_retention' (70 ملف) بلا ماستر — الماسترات المتاحة: ['01_outreach', '02_sales_calls', '03_offers_pricing'… |

> … و14 مخالفة أخرى (راجع JSON؛ محفوظ 17)

### C10 · شرط §18 (صفوف الجدول = concepts القطاع) — 5 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `03_MASTERS/01_outreach/Master_Outreach_Mechanics.md` | 183495 | §18 = 124 صف · concepts(01_outreach) = 133 · فرق -9 |
| 2 | `03_MASTERS/02_sales_calls/Master_Sales_Call_Architecture.md` | 216480 | §18 = 181 صف · concepts(02_sales_calls) = 500 · فرق -319 |
| 3 | `03_MASTERS/03_offers_pricing/Master_Offer_Construction_Pricing.md` | 220315 | §18 = 109 صف · concepts(03_offers_pricing) = 166 · فرق -57 |

> … و2 مخالفة أخرى (راجع JSON؛ محفوظ 5)

### C11 · رقم بلا ⚠️ ولا مصدر — 26979 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/C6/concepts/Concept_VictimMentalityGrowthBlock.md` | 1627 | رقم بلا تنبيه/مصدر، مثال: '** شوهد في ملف واحد (لدي 34,000 متابع) — «السم الخام' |
| 2 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | رقم بلا تنبيه/مصدر، مثال: 'ttern Interrupt\ncreated: 2026-09-26\ntags: [08]\nmention' |
| 3 | `02_CONCEPTS/06_hooks_retention/Concept_Borrowed_Familiarity.md` | 776 | رقم بلا تنبيه/مصدر، مثال: 'wed Familiarity\ncreated: 2026-09-26\ntags: [99]\nmention' |

> … و26976 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

### C12 · فهرس البحث stale — 1 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `04_SEARCH/index.json.gz` | 14175094 | mtime الفهرس أقدم من أحدث concept بـ 17 ثانية |

### C13 · concept بلا wikilink — 34487 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/A1/concepts/Concept_AI_Production_Pipeline.md` | 5430 | صفر روابط [[ ]] |
| 2 | `.nexus_work/stage/A1/concepts/Concept_Access_Ownership_Aggregation.md` | 4485 | صفر روابط [[ ]] |
| 3 | `.nexus_work/stage/A1/concepts/Concept_Attention_Economy.md` | 4110 | صفر روابط [[ ]] |

> … و34484 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

### C14 · concept بلا الأقسام الستة كاملة — 34861 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/A1/concepts/Concept_AI_Production_Pipeline.md` | 5430 | أقسام ناقصة: التعريف |
| 2 | `.nexus_work/stage/A1/concepts/Concept_Access_Ownership_Aggregation.md` | 4485 | أقسام ناقصة: التعريف |
| 3 | `.nexus_work/stage/A1/concepts/Concept_Attention_Economy.md` | 4110 | أقسام ناقصة: التعريف |

> … و34858 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

### C15 · أسماء مولّدة آلياً — 981 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/terms_26k/01_outreach/part_01/Concept_0.001_Reply_Rate.md` | 1105 | نمط _0.5_ في الاسم |
| 2 | `02_CONCEPTS/terms_26k/01_outreach/part_01/Concept_0.5_Reply-Rate_Cutoff.md` | 1469 | نمط _0.5_ في الاسم |
| 3 | `02_CONCEPTS/terms_26k/01_outreach/part_01/Concept_10_positive_replies_per_1000_prospects_(test_standard).md` | 1284 | أربعة أرقام متتالية في الاسم |

> … و978 مخالفة أخرى (راجع JSON؛ محفوظ 981)

### C16 · حشو / Ukrainian — 69 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/C10/concepts/Concept_PersonalizationAtScale.md` | 5214 | نص سيريليكي (Ukrainian): р — 3 رسالات متتابعة بم расстояل 2–3 أيام تعالج فئة "المقتنع ال… |
| 2 | `.nexus_work/stage/C11/PROVENANCE.md` | 10642 | نص سيريليكي (Ukrainian): п — تشغيل أداة، والكام прибыли «بالصدفة» (ضجيج تحيز موثق في ال… |
| 3 | `.nexus_work/stage/C4/concepts/Concept_SingleOfferCompounding.md` | 5088 | نص سيريليكي (Ukrainian): п — ؤسس؛ خدمة قابلة للت повтор عبر عملاء متشابهين؛ سوق يكفي لتغ… |

> … و66 مخالفة أخرى (راجع JSON؛ محفوظ 69)

### C17 · ماستر بلا حدود فناء — 0 مخالفة

### C18 · بوابات Master SPEC — 1 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `03_MASTERS/01_outreach/Master_Outreach_Mechanics.md` | 183495 | §4=7138 كلمة = 39.98% <40% |

### C19 · YAML ناقص (---/type/version/sections) — 0 مخالفة

### C20 · نسخة مطابقة بين مجلدين (تراجع) — 2173 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `README.md` | 1589 | sha256[:12]=b2564ced8245 في 2 مجلد: README.md | TRASH/2026-09-26_RESET/README.md |
| 2 | `.nexus_work/EXTRACTION_BRIEF.md` | 9959 | sha256[:12]=53588965e4aa في 2 مجلد: .nexus_work/EXTRACTION_BRIEF.md | TRASH/2026-09-26_RESET/.nexus_work/EXTRACTION_BRI… |
| 3 | `.nexus_work/MERGE_CANDIDATES.md` | 311512 | sha256[:12]=c2f7c2294a58 في 2 مجلد: .nexus_work/MERGE_CANDIDATES.md | TRASH/2026-09-26_RESET/.nexus_work/MERGE_CANDIDAT… |

> … و2170 مخالفة أخرى (راجع JSON؛ محفوظ 2173)

### C21 · مجلد >1000 ملف — 1 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `TRASH/2026-09-26_RESET/02_CONCEPTS` | 0 | ملفات مباشرة = 1401 > 1000 |

### C22 · حجم 99_misc ≤3% من 02_CONCEPTS — 1 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/99_uncategorized:02_CONCEPTS/terms_26k/99_misc` | 13114403 | 99_misc = 18.05% من حجم المفاهيم (حد 3%) · 28.94% من العدد (10089/34865 مفهوم، 13114403/72667489 بايت) |

### C23 · concept بلا أقسام توتر (تقرير فقط) — 27713 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/C6/concepts/Concept_VictimMentalityGrowthBlock.md` | 1627 | لا قسم توترات/تعارضات |
| 2 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | لا قسم توترات/تعارضات |
| 3 | `02_CONCEPTS/06_hooks_retention/Concept_Borrowed_Familiarity.md` | 776 | لا قسم توترات/تعارضات |

> … و27710 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

### C24 · concept <250 كلمة — 27264 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/C11/concepts/Concept_ClientVoicedDifferentiator.md` | 2312 | 238 كلمة < 250 |
| 2 | `.nexus_work/stage/C6/concepts/Concept_VictimMentalityGrowthBlock.md` | 1627 | 154 كلمة < 250 |
| 3 | `02_CONCEPTS/02_sales_calls/Concept_ClientVoicedDifferentiator.md` | 2312 | 238 كلمة < 250 |

> … و27261 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

### C25 · concept >600 كلمة (≤3%) — 11 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/terms_26k/01_outreach/part_03/Concept_Spintax.md` | 38819 | 5161 كلمة > 600 |
| 2 | `02_CONCEPTS/terms_26k/01_outreach/part_01/Concept_Clay.md` | 28495 | 3742 كلمة > 600 |
| 3 | `02_CONCEPTS/terms_26k/29_instagram_growth/part_01/Concept_القسم_1_kallawaymarketing_(18_ملفا_-_17_ريل_1_كاروسيل).md` | 27690 | 4103 كلمة > 600 |

> … و8 مخالفة أخرى (راجع JSON؛ محفوظ 11)

### C26 · concept بلا «## المصدرية» — 27641 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/C6/concepts/Concept_VictimMentalityGrowthBlock.md` | 1627 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |
| 2 | `02_CONCEPTS/_INDEX.md` | 3419 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |
| 3 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |

> … و27638 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

### C27 · placeholders (TODO/TBD/XXX) — 8 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `01_TERMS/ig_en_b44.md` | 60346 | «XXX» — قرر أين تتوسع) — مع هدف محدد [XXX] لما يجب أن يبدو عليه النجاح  |
| 2 | `01_TERMS/ig_root_misc_23.md` | 212943 | «XXX» — ng like I'm the president CEO XXX of this nobody cares about yo |
| 3 | `01_TERMS/yt_root_misc_37.md` | 353018 | «TBD» — a list of 10,000 prospects or TBD. AI analyze based on triggers |

> … و5 مخالفة أخرى (راجع JSON؛ محفوظ 8)

### C28 · concepts بلا sources غير فارغ — 7212 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/stage/A1/concepts/Concept_AI_Production_Pipeline.md` | 5430 | لا frontmatter ⇒ لا sources |
| 2 | `.nexus_work/stage/A1/concepts/Concept_Access_Ownership_Aggregation.md` | 4485 | لا frontmatter ⇒ لا sources |
| 3 | `.nexus_work/stage/A1/concepts/Concept_Attention_Economy.md` | 4110 | لا frontmatter ⇒ لا sources |

> … و7209 مخالفة أخرى (راجع JSON؛ محفوظ 4000)

## أعلى المجلدات حجمًا

| المجلد | ملفات | bytes |
|---|---:|---:|
| `00_SYSTEMS` | 271 | 68519697 |
| `02_CONCEPTS` | 29585 | 47273329 |
| `01_TERMS` | 552 | 31779191 |
| `TRASH` | 4056 | 29664541 |
| `.nexus_work` | 2412 | 18219616 |
| `04_SEARCH` | 6 | 14242255 |
| `01_INVENTORY` | 6 | 2503209 |
| `03_MASTERS` | 10 | 1047623 |
| `06_GLOSSARY` | 65 | 568057 |
| `05_TENSIONS` | 65 | 563303 |
| `07_PROVENANCE` | 65 | 506967 |
| `00_CHARTER` | 4 | 38513 |
| `(root)` | 1 | 1589 |
