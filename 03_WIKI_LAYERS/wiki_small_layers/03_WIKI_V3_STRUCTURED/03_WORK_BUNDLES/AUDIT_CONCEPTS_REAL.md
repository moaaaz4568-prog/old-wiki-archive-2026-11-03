# تقرير فحص الجودة الآلي — audit_scoped.py

- **النطاق:** `concepts` — 02_CONCEPTS/<قطاعات NN_*> فقط — بلا terms_26k و _REPORTS
- **ملفات النطاق:** 1836 مُدقَّقة · 35262 مستبعدة · Findings بلا سقف
- **الجذر:** `/root/r/NB2`
- **التاريخ:** 2026-10-02T03:14:39+0000
- **الزمن:** 68.48s (مسح 43.84s، قراءة 16.58s، 1841 ملف / 9.5 MB، 8 threads)
- **المفاهيم:** 1836 · **الماسترات:** 0 · **ملفات .md:** 1836 · **إجمالي الملفات:** 1836
- **مجموع الأوزان:** 100

## جدول النتائج

| ID | الفحص | العدد | الخطورة | الوزن | العتبة | الحالة |
|---|---|---:|---:|---:|---|---|
| C01 | روابط [[ ]] معلّقة | 0 | 8 | 7 | 0 | ✅ نظيف |
| C02 | كعبات <300 بايت | 0 | 6 | 5 | 0 | ✅ نظيف |
| C03 | تكرار حرفي بين concept | 0 | 7 | 5 | 0 | ✅ نظيف |
| C04 | concept بلا اقتباس/مصدر | 1 | 8 | 6 | 0 | 🔴 مخالفة |
| C05 | concept بلا «حدود الفناء» | 5 | 8 | 6 | 0 | 🔴 مخالفة |
| C06 | concept بلا «الآلية» | 2 | 7 | 6 | 0 | 🔴 مخالفة |
| C07 | ماستر بأقسام <18 | 0 | 8 | 4 | 0 | ✅ نظيف |
| C08 | concept مكرر الاسم | 0 | 5 | 3 | 0 | ✅ نظيف |
| C09 | قطاع بلا ماستر | 17 | 6 | 3 | 0 | 🔴 مخالفة |
| C10 | شرط §18 (صفوف الجدول = concepts القطاع) | 0 | 8 | 4 | 0 | ✅ نظيف |
| C11 | رقم بلا ⚠️ ولا مصدر | 4 | 6 | 4 | 0 | 🔴 مخالفة |
| C12 | فهرس البحث stale | 0 | 4 | 2 | 0 | ✅ نظيف |
| C13 | concept بلا wikilink | 1836 | 5 | 3 | 0 | 🔴 مخالفة |
| C14 | concept بلا الأقسام الستة كاملة | 1835 | 9 | 7 | 0 | 🔴 مخالفة |
| C15 | أسماء مولّدة آلياً | 0 | 4 | 2 | 0 | ✅ نظيف |
| C16 | حشو / Ukrainian | 4 | 5 | 2 | 0 | 🔴 مخالفة |
| C17 | ماستر بلا حدود فناء | 0 | 7 | 3 | 0 | ✅ نظيف |
| C18 | بوابات Master SPEC | 0 | 9 | 4 | 4 sub-gates | ✅ نظيف |
| C19 | YAML ناقص (---/type/version/sections) | 0 | 6 | 3 | 0 | ✅ نظيف |
| C20 | نسخة مطابقة بين مجلدين (تراجع) | 0 | 7 | 3 | 0 | ✅ نظيف |
| C21 | مجلد >1000 ملف | 0 | 3 | 2 | 0 | ✅ نظيف |
| C22 | حجم 99_misc ≤3% من 02_CONCEPTS | 0 | 5 | 2 | ≤3% | ✅ نظيف |
| C23 | concept بلا أقسام توتر (تقرير فقط) | 4 | 0 | 0 | — | ℹ️ تقرير فقط (4) |
| C24 | concept <250 كلمة | 5 | 6 | 4 | 0 | 🔴 مخالفة |
| C25 | concept >600 كلمة (≤3%) | 449 | 4 | 2 | ≤3% | 🔴 مخالفة |
| C26 | concept بلا «## المصدرية» | 4 | 7 | 4 | 0 | 🔴 مخالفة |
| C27 | placeholders (TODO/TBD/XXX) | 0 | 5 | 2 | 0 | ✅ نظيف |
| C28 | concepts بلا sources غير فارغ | 1833 | 7 | 2 | 0 | 🔴 مخالفة |
| — | **TOTAL** | **5999** | | **100** | | |

## التفاصيل (حتى 4 مثال لكل فاحص)

### C01 · روابط [[ ]] معلّقة — 0 مخالفة
> ℹ️ لا روابط معلّقة


### C02 · كعبات <300 بايت — 0 مخالفة
> ℹ️ لا كعبات


### C03 · تكرار حرفي بين concept — 0 مخالفة
> ℹ️ لا تكرار حرفي


### C04 · concept بلا اقتباس/مصدر — 1 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/08_mindset/Concept_VictimMentalityGrowthBlock.md` | 1627 | لا '## الدليل' ولا backtick ولا 'channel:' |

### C05 · concept بلا «حدود الفناء» — 5 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/02_sales_calls/Concept_PrecisionLanguaging.md` | 2971 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |
| 2 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |
| 3 | `02_CONCEPTS/06_hooks_retention/Concept_Borrowed_Familiarity.md` | 776 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |
| 4 | `02_CONCEPTS/06_hooks_retention/Concept_Curiosity_Gap.md` | 734 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |

> … و1 مخالفة أخرى (راجع JSON؛ محفوظ 5)

### C06 · concept بلا «الآلية» — 2 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | لا يوجد: الآلية / آلية العمل |
| 2 | `02_CONCEPTS/06_hooks_retention/Concept_Curiosity_Gap.md` | 734 | لا يوجد: الآلية / آلية العمل |

### C07 · ماستر بأقسام <18 — 0 مخالفة
> ℹ️ لا ماسترات في هذا الجذر


### C08 · concept مكرر الاسم — 0 مخالفة
> ℹ️ لا أسماء مكررة


### C09 · قطاع بلا ماستر — 17 مخالفة
> ℹ️ قطاعات: 22 · مغطّاة: 5 · بلا ماستر: 17

| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `04_content_strategy` | 0 | قطاع '04_content_strategy' (60 ملف) بلا ماستر — الماسترات المتاحة: ['01_outreach', '02_sales_calls', '03_offers_pricing… |
| 2 | `05_content_production` | 0 | قطاع '05_content_production' (93 ملف) بلا ماستر — الماسترات المتاحة: ['01_outreach', '02_sales_calls', '03_offers_prici… |
| 3 | `06_hooks_retention` | 0 | قطاع '06_hooks_retention' (70 ملف) بلا ماستر — الماسترات المتاحة: ['01_outreach', '02_sales_calls', '03_offers_pricing'… |
| 4 | `09_agencies_clients` | 0 | قطاع '09_agencies_clients' (80 ملف) بلا ماستر — الماسترات المتاحة: ['01_outreach', '02_sales_calls', '03_offers_pricing… |

> … و13 مخالفة أخرى (راجع JSON؛ محفوظ 17)

### C10 · شرط §18 (صفوف الجدول = concepts القطاع) — 0 مخالفة
> ℹ️ لا ماسترات في هذا الجذر (تخطّي)


### C11 · رقم بلا ⚠️ ولا مصدر — 4 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | رقم بلا تنبيه/مصدر، مثال: 'ttern Interrupt\ncreated: 2026-09-26\ntags: [08]\nmention' |
| 2 | `02_CONCEPTS/06_hooks_retention/Concept_Borrowed_Familiarity.md` | 776 | رقم بلا تنبيه/مصدر، مثال: 'wed Familiarity\ncreated: 2026-09-26\ntags: [99]\nmention' |
| 3 | `02_CONCEPTS/06_hooks_retention/Concept_Curiosity_Gap.md` | 734 | رقم بلا تنبيه/مصدر، مثال: ': Curiosity Gap\ncreated: 2026-09-26\ntags: [10]\nmention' |
| 4 | `02_CONCEPTS/08_mindset/Concept_VictimMentalityGrowthBlock.md` | 1627 | رقم بلا تنبيه/مصدر، مثال: '** شوهد في ملف واحد (لدي 34,000 متابع) — «السم الخام' |

### C12 · فهرس البحث stale — 0 مخالفة
> ℹ️ لا ملف فهرس (04_SEARCH/index.json.gz) — تخطّي


### C13 · concept بلا wikilink — 1836 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/01_outreach/Concept_AIOnboardingTriad.md` | 3939 | صفر روابط [[ ]] |
| 2 | `02_CONCEPTS/01_outreach/Concept_AttributionReframeOutreach.md` | 4677 | صفر روابط [[ ]] |
| 3 | `02_CONCEPTS/01_outreach/Concept_AuthorityCommentPipeline.md` | 6094 | صفر روابط [[ ]] |
| 4 | `02_CONCEPTS/01_outreach/Concept_AuthorityCommenting.md` | 5668 | صفر روابط [[ ]] |

> … و1832 مخالفة أخرى (راجع JSON؛ محفوظ 1836)

### C14 · concept بلا الأقسام الستة كاملة — 1835 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/01_outreach/Concept_AIOnboardingTriad.md` | 3939 | أقسام ناقصة: التعريف |
| 2 | `02_CONCEPTS/01_outreach/Concept_AttributionReframeOutreach.md` | 4677 | أقسام ناقصة: التعريف |
| 3 | `02_CONCEPTS/01_outreach/Concept_AuthorityCommentPipeline.md` | 6094 | أقسام ناقصة: التعريف |
| 4 | `02_CONCEPTS/01_outreach/Concept_AuthorityCommenting.md` | 5668 | أقسام ناقصة: التعريف |

> … و1831 مخالفة أخرى (راجع JSON؛ محفوظ 1835)

### C15 · أسماء مولّدة آلياً — 0 مخالفة
> ℹ️ لا أسماء مولّدة آلياً


### C16 · حشو / Ukrainian — 4 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/01_outreach/Concept_PersonalizationAtScale.md` | 5214 | نص سيريليكي (Ukrainian): р — 3 رسالات متتابعة بم расстояل 2–3 أيام تعالج فئة "المقتنع ال… |
| 2 | `02_CONCEPTS/02_sales_calls/Concept_Identity_Elevation.md` | 6603 | نص سيريليكي (Ukrainian): с — و هوية لا يقبلها في себя («كن القائد» لعائدٍ كارثي مع قائد … |
| 3 | `02_CONCEPTS/03_offers_pricing/Concept_SpecialistGptSwarm.md` | 5458 | نص سيريليكي (Ukrainian): е — ار نمط «طقم GPTs» كمез تسويقي، يتشبع الجمهور ويتحول من عامل… |
| 4 | `02_CONCEPTS/03_offers_pricing/Concept_SingleOfferCompounding.md` | 5088 | نص سيريليكي (Ukrainian): п — ؤسس؛ خدمة قابلة للت повтор عبر عملاء متشابهين؛ سوق يكفي لتغ… |

### C17 · ماستر بلا حدود فناء — 0 مخالفة
> ℹ️ لا ماسترات في هذا الجذر (تخطّي)


### C18 · بوابات Master SPEC — 0 مخالفة
> ℹ️ لا ماسترات في هذا الجذر (تخطّي)


### C19 · YAML ناقص (---/type/version/sections) — 0 مخالفة
> ℹ️ لا ماسترات في هذا الجذر (تخطّي)


### C20 · نسخة مطابقة بين مجلدين (تراجع) — 0 مخالفة
> ℹ️ لا نسخ متطابقة بين مجلدين


### C21 · مجلد >1000 ملف — 0 مخالفة
> ℹ️ لا مجلد يتجاوز 1000 ملف


### C22 · حجم 99_misc ≤3% من 02_CONCEPTS — 0 مخالفة
> ℹ️ 99_misc = 1.34% (ضمن 3%)


### C23 · concept بلا أقسام توتر (تقرير فقط) — 4 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | لا قسم توترات/تعارضات |
| 2 | `02_CONCEPTS/06_hooks_retention/Concept_Borrowed_Familiarity.md` | 776 | لا قسم توترات/تعارضات |
| 3 | `02_CONCEPTS/06_hooks_retention/Concept_Curiosity_Gap.md` | 734 | لا قسم توترات/تعارضات |
| 4 | `02_CONCEPTS/08_mindset/Concept_VictimMentalityGrowthBlock.md` | 1627 | لا قسم توترات/تعارضات |

### C24 · concept <250 كلمة — 5 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/02_sales_calls/Concept_ClientVoicedDifferentiator.md` | 2312 | 238 كلمة < 250 |
| 2 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | 114 كلمة < 250 |
| 3 | `02_CONCEPTS/06_hooks_retention/Concept_Borrowed_Familiarity.md` | 776 | 61 كلمة < 250 |
| 4 | `02_CONCEPTS/06_hooks_retention/Concept_Curiosity_Gap.md` | 734 | 72 كلمة < 250 |

> … و1 مخالفة أخرى (راجع JSON؛ محفوظ 5)

### C25 · concept >600 كلمة (≤3%) — 449 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/05_content_production/Concept_PatternInterrupt.md` | 12227 | 1442 كلمة > 600 |
| 2 | `02_CONCEPTS/01_outreach/Concept_CommentKeywordDMFunnel.md` | 10678 | 1198 كلمة > 600 |
| 3 | `02_CONCEPTS/08_mindset/Concept_BinaryPositionalityRelease.md` | 10013 | 990 كلمة > 600 |
| 4 | `02_CONCEPTS/01_outreach/Concept_CommentGatedLeadDelivery.md` | 9564 | 1109 كلمة > 600 |

> … و445 مخالفة أخرى (راجع JSON؛ محفوظ 449)

### C26 · concept بلا «## المصدرية» — 4 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/02_sales_calls/Concept_Pattern_Interrupt.md` | 1136 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |
| 2 | `02_CONCEPTS/06_hooks_retention/Concept_Borrowed_Familiarity.md` | 776 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |
| 3 | `02_CONCEPTS/06_hooks_retention/Concept_Curiosity_Gap.md` | 734 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |
| 4 | `02_CONCEPTS/08_mindset/Concept_VictimMentalityGrowthBlock.md` | 1627 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |

### C27 · placeholders (TODO/TBD/XXX) — 0 مخالفة
> ℹ️ لا placeholders


### C28 · concepts بلا sources غير فارغ — 1833 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `02_CONCEPTS/01_outreach/Concept_AIOnboardingTriad.md` | 3939 | لا frontmatter ⇒ لا sources |
| 2 | `02_CONCEPTS/01_outreach/Concept_AttributionReframeOutreach.md` | 4677 | لا frontmatter ⇒ لا sources |
| 3 | `02_CONCEPTS/01_outreach/Concept_AuthorityCommentPipeline.md` | 6094 | لا frontmatter ⇒ لا sources |
| 4 | `02_CONCEPTS/01_outreach/Concept_AuthorityCommenting.md` | 5668 | لا frontmatter ⇒ لا sources |

> … و1829 مخالفة أخرى (راجع JSON؛ محفوظ 1833)

## أعلى المجلدات حجمًا

| المجلد | ملفات | bytes |
|---|---:|---:|
| `02_CONCEPTS` | 1836 | 8921097 |
