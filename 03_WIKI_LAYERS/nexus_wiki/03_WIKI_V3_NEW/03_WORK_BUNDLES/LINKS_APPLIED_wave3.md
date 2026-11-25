# LINKS_APPLIED_wave3 — تطبيق خطة الروابط على 3 قطاعات جديدة

> `V3/03_WORK_BUNDLES/apply_links.py` · **إضافة فقط (append)** · بلا تعديل أو حذف لسطر موجود · بلا push.
> النطاق: `08_mindset` · `07_branding` · `03_offers_pricing` = **541 ملفًا** فقط.

## 1) الاختيار (ترتيب حصة الخطة تنازليًا بعد المُطبَّقَين)

`01_outreach` 133/1,074 و`02_sales_calls` 500/4,029 مُطبَّقان مسبقًا ← التالي: **`08_mindset` 200/1,579** ·
**`07_branding` 175/1,373** · **`03_offers_pricing` 166/1,335**.

## 2) `sector | files | links | dangling`

| sector | files | links | أهداف فريدة | مع `--verify` | **dangling** | EXIT |
|---|---:|---:|---:|---|---:|---:|
| `01_outreach` | 133 | 1,074 | 138 | 133/133 بقسم الروابط | **0** | 0 |
| `02_sales_calls` | 500 *(499 مُعدَّل)* | 4,029 | 497 | 499/500 | **0** | 0 |
| `08_mindset` | 200 | 1,579 | 194 | 200/200 | **0** | 0 |
| `07_branding` | 175 | 1,373 | 174 | 175/175 | **0** | 0 |
| `03_offers_pricing` | 166 | 1,335 | 169 | 166/166 | **0** | 0 |
| **الإجمالي** | **1,174** | **9,390** | — | — | **0** | **0** |

`EXIT=0` لكل نطاق ⇒ **صفر معلّق** ⇒ شرط التوقّف لم يُطلَق. روابط مرفوضة (لم تُحلّ ملفًا): **0**. جذور مُفهرسة: **29,643**.
`02_sales_calls/Concept_Pattern_Interrupt.md` يبقى بلا روابط (الخطة لم تقترح له أيًّا — C24).

## 3) `git -C /root/r/NB2 diff --numstat`

| المقياس | قبل | بعد | **فرق الموجة** |
|---|---:|---:|---:|
| ملفات معدَّلة | 632 | 1,173 | **+541** |
| `added` | 6,381 | 11,767 | **+5,386** |
| `deleted` | 14 | 31 | **+17** |

حسب القطاع: `01_outreach` 133/+1344/−4 · `02_sales_calls` 499/+5037/−10 · `08_mindset` 200/**+1988/−9** ·
`07_branding` 175/**+1727/−4** · `03_offers_pricing` 166/**+1671/−4**.

**مطابقة `added=5,386` بلا فرق** (روابط + 2×ملف-له-فاصل + 3×ملف-بلا-فاصل):
`1,579+2×191+3×9 = 1,988` · `1,373+2×171+3×4 = 1,727` · `1,335+2×162+3×4 = 1,671` ⇒ **5,386**.

## 4) `deleted=17` ليس حذفًا — `\ No newline at end of file`

`git` يعيد إحصاء السطر الأخير عند إضافة فاصله فيسجّل `-1/+1` لملف واحد لا أكثر:

```diff
 ## المصدرية
-- … · كيف 3 بوش أبس غيروا حياتي (وخلوني أبدأ البزنس تبعي).txt
\ No newline at end of file
+- … · كيف 3 بوش أبس غيروا حياتي (وخلوني أبدأ البزنس تبعي).txt
+
+## الروابط
+- [[Concept_CrisisPlanProtocol]]
```

**دليلان مستقلان على صفر الحذف:**
1. السطر المُعاد إدراجه **بايت-بالبات** = المحذوف: `repr(minus[0]) == repr(plus[0]) → True`،
   و`git show HEAD:<file>` لا ينتهي بفاصل سطر (`endswith(b'\n') → False`)؛ والعلامة `\ No newline` تظهر في الطرف `-` فقط.
2. **البايت-بالبات الكامل**: محتوى القرص **يبدأ بـ** محتوى `HEAD` في **541/541** ملف —
   `08_mindset 200/200 · 07_branding 175/175 · 03_offers_pricing 166/166 · rewritten: 0`:
```bash
python3 - <<'PY'
import subprocess, glob
for s in ['08_mindset','07_branding','03_offers_pricing']:
    ok=bad=0
    for f in sorted(glob.glob('02_CONCEPTS/%s/*.md'%s)):
        old=subprocess.run(['git','show','HEAD:'+f],capture_output=True).stdout
        if open(f,'rb').read().startswith(old): ok+=1
        else: bad+=1
    print(s,"byte-prefix:",ok,"| rewritten:",bad)
PY
```

## 5) احترام النطاق (بالقياس)

| الحارس | النتيجة |
|---|---|
| `01_outreach` | **UNCHANGED** — `sha256 9f511bf4…fb0bcd` (133 ملفًا) قبلًا وبعدها |
| `02_sales_calls` | **UNCHANGED** — `sha256 105cb6ef…eb1de` (500 ملف) قبلًا وبعدها |
| `terms_26k` | **UNCHANGED** — بصمة `ed1579ad…d417` · 27,742 ملفًا · 38,306,837 بايت · `git status` = 0 |
| `git status --porcelain \| cut -c1-2 \| sort \| uniq -c` | `1173 M` فقط ⇒ **صفر** جديد/محذوف/غير متتبَّع |
| خارج القطاعات الثلاثة | **0** كتابة · لا `push` · لا commit · لا `/sdcard` |

## 6) المتبقي من 14,564 بالأرقام

```
الخطة الكلية : 14,564 رابطًا / 1,836 مفهومًا / 23 قطاعًا
المُطبَّق (5) :  9,390 رابطًا / 1,174 مفهومًا  (100% من حصصها)
المتبقي      :  5,174 رابطًا /   662 مفهومًا /    18 قطاعًا
```

أكبر المتبقي: `05_content_production` 748 · `09_agencies_clients` 633 · `06_hooks_retention` 540 ·
`11_marketing_ads` 489 · `04_content_strategy` 483 · `12_growth` 468 · `17_ai_automation` 377 · `10_funnels` 329 ·
`20_productivity_learning` 272 · `19_operations_teams` 258 · `99_uncategorized` 203 · `15_platforms_algo` 142 ·
`16_business_models` 97 · `13_storytelling` 78 · `14_copywriting` 37 · `22_finance_legal` 12 ·
`21_persuasion_psych` 6 · `18_trust_authority` 2 — خارج نطاق هذه المهمة عمدًا.
