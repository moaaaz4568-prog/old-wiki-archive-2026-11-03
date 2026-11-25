# تقرير فحص الجودة الآلي — V3_SYS/audit.py

- **الجذر:** `/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI`
- **التاريخ:** 2026-10-01T02:38:41+0000
- **الزمن:** 86.22s (مسح 11.59s، قراءة 16.06s، 5451 ملف / 67.6 MB، 1 threads)
- **المفاهيم:** 3230 · **الماسترات:** 136 · **ملفات .md:** 5451 · **إجمالي الملفات:** 10624
- **مجموع الأوزان:** 100

## جدول النتائج

| ID | الفحص | العدد | الخطورة | الوزن | العتبة | الحالة |
|---|---|---:|---:|---:|---|---|
| C01 | روابط [[ ]] معلّقة | 1244 | 8 | 7 | 0 | 🔴 مخالفة |
| C02 | كعبات <300 بايت | 65 | 6 | 5 | 0 | 🔴 مخالفة |
| C03 | تكرار حرفي بين concept | 1613 | 7 | 5 | 0 | 🔴 مخالفة |
| C04 | concept بلا اقتباس/مصدر | 2644 | 8 | 6 | 0 | 🔴 مخالفة |
| C05 | concept بلا «حدود الفناء» | 3222 | 8 | 6 | 0 | 🔴 مخالفة |
| C06 | concept بلا «الآلية» | 2300 | 7 | 6 | 0 | 🔴 مخالفة |
| C07 | ماستر بأقسام <18 | 24 | 8 | 4 | 0 | 🔴 مخالفة |
| C08 | concept مكرر الاسم | 0 | 5 | 3 | 0 | ✅ نظيف |
| C09 | قطاع بلا ماستر | 0 | 6 | 3 | 0 | ✅ نظيف |
| C10 | شرط §18 (صفوف الجدول = concepts القطاع) | 136 | 8 | 4 | 0 | 🔴 مخالفة |
| C11 | رقم بلا ⚠️ ولا مصدر | 1894 | 6 | 4 | 0 | 🔴 مخالفة |
| C12 | فهرس البحث stale | 0 | 4 | 2 | 0 | ✅ نظيف |
| C13 | concept بلا wikilink | 24 | 5 | 3 | 0 | 🔴 مخالفة |
| C14 | concept بلا الأقسام الستة كاملة | 3230 | 9 | 7 | 0 | 🔴 مخالفة |
| C15 | أسماء مولّدة آلياً | 44 | 4 | 2 | 0 | 🔴 مخالفة |
| C16 | حشو / Ukrainian | 171 | 5 | 2 | 0 | 🔴 مخالفة |
| C17 | ماستر بلا حدود فناء | 133 | 7 | 3 | 0 | 🔴 مخالفة |
| C18 | بوابات Master SPEC | 128 | 9 | 4 | 4 sub-gates | 🔴 مخالفة |
| C19 | YAML ناقص (---/type/version/sections) | 134 | 6 | 3 | 0 | 🔴 مخالفة |
| C20 | نسخة مطابقة بين مجلدين (تراجع) | 2365 | 7 | 3 | 0 | 🔴 مخالفة |
| C21 | مجلد >1000 ملف | 3 | 3 | 2 | 0 | 🔴 مخالفة |
| C22 | حجم 99_misc ≤3% من 02_CONCEPTS | 0 | 5 | 2 | ≤3% | ✅ نظيف |
| C23 | concept بلا أقسام توتر (تقرير فقط) | 2974 | 0 | 0 | — | ℹ️ تقرير فقط (2974) |
| C24 | concept <250 كلمة | 252 | 6 | 4 | 0 | 🔴 مخالفة |
| C25 | concept >600 كلمة (≤3%) | 11 | 4 | 2 | ≤3% | 🔴 مخالفة |
| C26 | concept بلا «## المصدرية» | 2738 | 7 | 4 | 0 | 🔴 مخالفة |
| C27 | placeholders (TODO/TBD/XXX) | 137 | 5 | 2 | 0 | 🔴 مخالفة |
| C28 | concepts بلا sources غير فارغ | 1006 | 7 | 2 | 0 | 🔴 مخالفة |
| — | **TOTAL** | **26492** | | **100** | | |

## التفاصيل (حتى 3 مثال لكل فاحص)

### C01 · روابط [[ ]] معلّقة — 1244 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `[[..]]` | 0 | معلّق في 3 ملف، مثال: .nexus_work/critique/concepts_81.md |
| 2 | `[[...]]` | 0 | معلّق في 23 ملف، مثال: .nexus_work/apply/mirror/Master_Email_Deliverability.md |
| 3 | `[[...`) بقوسين مربعين مزدوجين غير متوازنين، والعنوان الداخلي مكتوب كwikilink `]]` | 0 | معلّق في 1 ملف، مثال: .nexus_work/critique/concepts_86.md |

> … و1241 مخالفة أخرى (راجع JSON؛ محفوظ 1244)

### C02 · كعبات <300 بايت — 65 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/entities/Entity_Mohamed_Osama.md` | 174 | حجم 174B < 300B |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/entities/Entity_Aaron_Brimhall.md` | 175 | حجم 175B < 300B |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/entities/Entity_Taylor_Agency_Birth.md` | 180 | حجم 180B < 300B |

> … و62 مخالفة أخرى (راجع JSON؛ محفوظ 65)

### C03 · تكرار حرفي بين concept — 1613 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | sha256[:12]=d640cd8f1f6d متطابق في 2 ملف: .nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketi… |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | sha256[:12]=f70176139b2b متطابق في 2 ملف: .nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_P… |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Word_of_Mouth_Branding.md` | 5630 | sha256[:12]=c7db11a42314 متطابق في 2 ملف: .nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Word_of_Mouth_B… |

> … و1610 مخالفة أخرى (راجع JSON؛ محفوظ 1613)

### C04 · concept بلا اقتباس/مصدر — 2644 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | لا '## الدليل' ولا backtick ولا 'channel:' |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | لا '## الدليل' ولا backtick ولا 'channel:' |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Word_of_Mouth_Branding.md` | 5630 | لا '## الدليل' ولا backtick ولا 'channel:' |

> … و2641 مخالفة أخرى (راجع JSON؛ محفوظ 2644)

### C05 · concept بلا «حدود الفناء» — 3222 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Word_of_Mouth_Branding.md` | 5630 | لا يوجد: حدود الفناء / متى لا يعمل / الفناء |

> … و3219 مخالفة أخرى (راجع JSON؛ محفوظ 3222)

### C06 · concept بلا «الآلية» — 2300 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | لا يوجد: الآلية / آلية العمل |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Word_of_Mouth_Branding.md` | 5630 | لا يوجد: الآلية / آلية العمل |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Urgency_Scarcity.md` | 9720 | لا يوجد: الآلية / آلية العمل |

> … و2297 مخالفة أخرى (راجع JSON؛ محفوظ 2300)

### C07 · ماستر بأقسام <18 — 24 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/routing/Master_Marketing_Strategy__BRA.md` | 27883 | عدد أقسام '## §' = 0 < 18 |
| 2 | `.nexus_work/routing/Master_Metrics_And_Analytics__BRA.md` | 6279 | عدد أقسام '## §' = 0 < 18 |
| 3 | `.nexus_work/routing/Master_Lead_Generation__BRA.md` | 12032 | عدد أقسام '## §' = 0 < 18 |

> … و21 مخالفة أخرى (راجع JSON؛ محفوظ 24)

### C08 · concept مكرر الاسم — 0 مخالفة
> ℹ️ لا أسماء مكررة


### C09 · قطاع بلا ماستر — 0 مخالفة
> ℹ️ لا قطاعات (NN_*) مباشرة تحت 02_CONCEPTS — تخطّي


### C10 · شرط §18 (صفوف الجدول = concepts القطاع) — 136 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/apply/mirror/Master_Content_Strategy.md` | 567266 | لا جدول مفاهيم في §18 |
| 2 | `.nexus_work/apply/mirror/Master_Platform_Strategy.md` | 271409 | تعذّر ربط الماستر بقطاع (master=Master_Platform_Strategy, rows=36, القطاعات=لا شيء) |
| 3 | `.nexus_work/apply/mirror/Master_Email_Deliverability.md` | 123422 | لا جدول مفاهيم في §18 |

> … و133 مخالفة أخرى (راجع JSON؛ محفوظ 136)

### C11 · رقم بلا ⚠️ ولا مصدر — 1894 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | رقم بلا تنبيه/مصدر، مثال: 'Marketing_Types\ncreated: 2026-05-19\nupdated: 2026-05-2' |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | رقم بلا تنبيه/مصدر، مثال: 'ontent Pipeline\ncreated: 2026-06-19\nupdated: 2026-06-1' |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Urgency_Scarcity.md` | 9720 | رقم بلا تنبيه/مصدر، مثال: 'gency Scarcity\n\nupdated: 2026-06-10\nsynthesized_from: ' |

> … و1891 مخالفة أخرى (راجع JSON؛ محفوظ 1894)

### C12 · فهرس البحث stale — 0 مخالفة

### C13 · concept بلا wikilink — 24 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Me_&_You_vs_The_Problem.md` | 16543 | صفر روابط [[ ]] |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Card_Link_Strategy.md` | 1966 | صفر روابط [[ ]] |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_End_Screen_Optimization.md` | 2026 | صفر روابط [[ ]] |

> … و21 مخالفة أخرى (راجع JSON؛ محفوظ 24)

### C14 · concept بلا الأقسام الستة كاملة — 3230 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | أقسام ناقصة: التعريف، الآلية، حدود الفناء، الشروط، الدليل، المصدرية |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | أقسام ناقصة: التعريف، حدود الفناء، الشروط، الدليل، المصدرية |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Word_of_Mouth_Branding.md` | 5630 | أقسام ناقصة: التعريف، الآلية، حدود الفناء، الشروط، الدليل |

> … و3227 مخالفة أخرى (راجع JSON؛ محفوظ 3230)

### C15 · أسماء مولّدة آلياً — 44 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Multi_Touch_Conversion_2026.md` | 13573 | أربعة أرقام متتالية في الاسم |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Info_Industry_2026_Survival.md` | 16111 | أربعة أرقام متتالية في الاسم |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Service_Hierarchy_2026.md` | 10050 | أربعة أرقام متتالية في الاسم |

> … و41 مخالفة أخرى (راجع JSON؛ محفوظ 44)

### C16 · حشو / Ukrainian — 171 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/INGESTION_SYSTEM/02_CONCEPT_EXTRACTION.md` | 9226 | نص سيريليكي (Ukrainian): а — ت القادمة فقط. > المастرات والـpatches الحالية لا تعتمد علي… |
| 2 | `.nexus_work/analysis/BR_b05.md` | 56498 | نص سيريليكي (Ukrainian): у — اس فعلاً، وسكريبت ي удержل المشاهد بعد الثانية 30. - دليل:  |
| 3 | `.nexus_work/apply/mirror/Master_Agency_Scaling_Systems.md` | 168394 | نص سيريليكي (Ukrainian): Р — [نتيجة محددة] لـ [ICР] عبر [نظامنا الملكي]". الوضوح يجذب ال… |

> … و168 مخالفة أخرى (راجع JSON؛ محفوظ 171)

### C17 · ماستر بلا حدود فناء — 133 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/apply/mirror/Master_Content_Strategy.md` | 567266 | لا حدود فناء |
| 2 | `.nexus_work/apply/mirror/Master_Platform_Strategy.md` | 271409 | لا حدود فناء |
| 3 | `.nexus_work/apply/mirror/Master_Email_Deliverability.md` | 123422 | لا حدود فناء |

> … و130 مخالفة أخرى (راجع JSON؛ محفوظ 133)

### C18 · بوابات Master SPEC — 128 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/apply/mirror/Master_Content_Strategy.md` | 567266 | §4=5033 كلمة = 8.42% <40% | §15=1581 كلمة <1800 |
| 2 | `.nexus_work/apply/mirror/Master_Platform_Strategy.md` | 271409 | §4=314 كلمة = 1.21% <40% | §15=74 كلمة <1800 |
| 3 | `.nexus_work/apply/mirror/Master_Email_Deliverability.md` | 123422 | §4=2926 كلمة = 21.28% <40% |

> … و125 مخالفة أخرى (راجع JSON؛ محفوظ 128)

### C19 · YAML ناقص (---/type/version/sections) — 134 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/apply/mirror/Master_Content_Strategy.md` | 567266 | لا frontmatter --- |
| 2 | `.nexus_work/apply/mirror/Master_Platform_Strategy.md` | 271409 | لا frontmatter --- |
| 3 | `.nexus_work/apply/mirror/Master_Email_Deliverability.md` | 123422 | مفاتيح ناقصة: sections: |

> … و131 مخالفة أخرى (راجع JSON؛ محفوظ 134)

### C20 · نسخة مطابقة بين مجلدين (تراجع) — 2365 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/apply/mirror/Master_Content_Strategy.md` | 567266 | sha256[:12]=6f714f591885 في 2 مجلد: .nexus_work/apply/mirror/Master_Content_Strategy.md | nexus_vault/04_content_strate… |
| 2 | `.nexus_work/apply/mirror/Master_Platform_Strategy.md` | 271409 | sha256[:12]=c593e84b94bb في 2 مجلد: .nexus_work/apply/mirror/Master_Platform_Strategy.md | nexus_vault/18_platforms_alg… |
| 3 | `.nexus_work/apply/mirror/Master_Email_Deliverability.md` | 123422 | sha256[:12]=b13f01442aaf في 2 مجلد: .nexus_work/apply/mirror/Master_Email_Deliverability.md | nexus_vault/01_outreach/M… |

> … و2362 مخالفة أخرى (راجع JSON؛ محفوظ 2365)

### C21 · مجلد >1000 ملف — 3 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts` | 0 | ملفات مباشرة = 1613 > 1000 |
| 2 | `Nexus_Brain/wiki/concepts` | 0 | ملفات مباشرة = 1613 > 1000 |
| 3 | `brain` | 0 | ملفات مباشرة = 1216 > 1000 |

### C22 · حجم 99_misc ≤3% من 02_CONCEPTS — 0 مخالفة
> ℹ️ لا مجلد 99_misc/99_uncategorized — تخطّي


### C23 · concept بلا أقسام توتر (تقرير فقط) — 2974 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | لا قسم توترات/تعارضات |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | لا قسم توترات/تعارضات |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Word_of_Mouth_Branding.md` | 5630 | لا قسم توترات/تعارضات |

> … و2971 مخالفة أخرى (راجع JSON؛ محفوظ 2974)

### C24 · concept <250 كلمة — 252 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | 190 كلمة < 250 |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Content_Pre_Verification.md` | 2314 | 190 كلمة < 250 |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Confirmation_Bias.md` | 2150 | 174 كلمة < 250 |

> … و249 مخالفة أخرى (راجع JSON؛ محفوظ 252)

### C25 · concept >600 كلمة (≤3%) — 11 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Identity_Selling.md` | 90455 | 8363 كلمة > 600 |
| 2 | `Nexus_Brain/wiki/concepts/Concept_Identity_Selling.md` | 90455 | 8363 كلمة > 600 |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Visible_Authority.md` | 52130 | 5141 كلمة > 600 |

> … و8 مخالفة أخرى (راجع JSON؛ محفوظ 11)

### C26 · concept بلا «## المصدرية» — 2738 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Urgency_Scarcity.md` | 9720 | لا '## المصدرية' ولا '## المصادر' ولا '## المراجع' |

> … و2735 مخالفة أخرى (راجع JSON؛ محفوظ 2738)

### C27 · placeholders (TODO/TBD/XXX) — 137 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/apply/mirror/Master_High_Ticket_Closing.md` | 155818 | «XXX» — محدد]. > توقع اتصالاً من رقم [XXX-XXX-XXXX] — يُرجى الرد حتى نت |
| 2 | `.nexus_work/apply/mirror/Master_High_Ticket_Closing.md` | 155818 | «XXX» — ]. > توقع اتصالاً من رقم [XXX-XXX-XXXX] — يُرجى الرد حتى نتمكن  |
| 3 | `.nexus_work/apply/mirror/Master_Cold_Email_System.md` | 211695 | «XXX» — losed: 2 (0.8%) | Revenue: $X,XXX ``` **متى تغير الاستراتيجية؟ |

> … و134 مخالفة أخرى (راجع JSON؛ محفوظ 137)

### C28 · concepts بلا sources غير فارغ — 1006 مخالفة
| # | المسار | bytes | الدليل |
|---:|---|---:|---|
| 1 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Digital_Marketing_Types.md` | 15116 | لا frontmatter ⇒ لا sources |
| 2 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Video_Content_Pipeline.md` | 2308 | مصادر فارغة: sources=[] |
| 3 | `.nexus_work/backup/pre_unification/wiki_full/concepts/Concept_Negative_Framing_Behavior_vs_Identity.md` | 7729 | لا مفتاح مصادر في frontmatter |

> … و1003 مخالفة أخرى (راجع JSON؛ محفوظ 1006)

## أعلى المجلدات حجمًا

| المجلد | ملفات | bytes |
|---|---:|---:|
| `brain` | 5126 | 46438609 |
| `.nexus_work` | 2730 | 36916832 |
| `Nexus_Brain` | 2338 | 18321031 |
| `nexus_vault` | 117 | 11803929 |
| `chats` | 39 | 6148975 |
| `rag` | 5 | 3296835 |
| `Phase2_DeepDive` | 254 | 1131487 |
| `(root)` | 8 | 140708 |
| `concepts` | 4 | 8302 |
| `keywords` | 3 | 818 |
