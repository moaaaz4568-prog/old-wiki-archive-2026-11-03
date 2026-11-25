# LINKS_APPLIED_wave4 — تطبيق خطة الروابط على 4 قطاعات جديدة (الموجة الرابعة)

> `V3/03_WORK_BUNDLES/apply_links.py --scope …` · **إضافة فقط (append)** · بلا تعديل أو حذف لسطر موجود ·
> بلا `commit` · بلا `push` · بلا كتابة في `/sdcard` · بلا أي عملية حذف.
> النطاق: `05_content_production` · `09_agencies_clients` · `06_hooks_retention` · `11_marketing_ads`
> = **306 ملفًا** فقط.

## 1) الاختيار (ترتيب حصة الخطة تنازليًا بعد الخمسة السابقة)

الخمسة المُطبَّقَون سابقًا: `01_outreach` 1,074 · `02_sales_calls` 4,029 · `08_mindset` 1,579 ·
`07_branding` 1,373 · `03_offers_pricing` 1,335 ← التالي من `LINK_PLAN.jsonl` (استُبعد الخمسة):
**`05_content_production` 748** · **`09_agencies_clients` 633** · **`06_hooks_retention` 540** ·
**`11_marketing_ads` 489**. `--dry-run` نظيف على الأربعة قبل أي كتابة (0 مرفوض · 0 متخطّى).

## 2) `sector | files | links | dangling`

| sector | files | links | أهداف فريدة | مع `--verify` | **dangling** | EXIT |
|---|---:|---:|---:|---|---:|---:|
| `01_outreach` | 133 | 1,074 | 138 | 133/133 بقسم الروابط | **0** | 0 |
| `02_sales_calls` | 500 *(499 مُعدَّل)* | 4,029 | 497 | 499/500 | **0** | 0 |
| `08_mindset` | 200 | 1,579 | 194 | 200/200 | **0** | 0 |
| `07_branding` | 175 | 1,373 | 174 | 175/175 | **0** | 0 |
| `03_offers_pricing` | 166 | 1,335 | 169 | 166/166 | **0** | 0 |
| **`05_content_production`** | **93** | **748** | 90 | 93/93 | **0** | 0 |
| **`09_agencies_clients`** | **80** | **633** | 83 | 80/80 | **0** | 0 |
| **`06_hooks_retention`** | **70** | **540** | 72 | 70/70 | **0** | 0 |
| **`11_marketing_ads`** | **63** | **489** | 64 | 63/63 | **0** | 0 |
| **الإجمالي (9 قطاعات)** | **1,480** | **11,800** | — | — | **0** | **0** |

`EXIT=0` لكل نطاق ⇒ **صفر معلّق** ⇒ شرط التوقّف لم يُطلَق. روابط مرفوضة (لم تُحلّ ملفًا): **0** في الأربعة.
جذور مُفهرسة: **29,643** (ثابتة عبر الموجات ⇒ لا ملف جديد/مفقود).Concept بلا روابط يبقى كما هو
(`02_sales_calls/Concept_Pattern_Interrupt.md` — الخطة لم تقترح له أيًّا، C24).

## 3) `git -C /root/r/NB2 diff --numstat`

| المقياس | قبل الموجة | بعد الموجة | **فرق الموجة 4** |
|---|---:|---:|---:|
| ملفات معدَّلة | 1,173 | 1,479 | **+306** |
| `added` | 11,767 | 14,792 | **+3,025** |
| `deleted` | 31 | 34 | **+3** |

حسب القطاع: `05_content_production` 93/**+934/−0** · `09_agencies_clients` 80/**+796/−3** ·
`06_hooks_retention` 70/**+680/−0** · `11_marketing_ads` 63/**+615/−0**.

**مطابقة `added=3,025` بلا فرق** (روابط + 2×ملف-له-فاصل + 3×ملف-بلا-فاصل):
`748+2×93 = 934` · `633+2×77+3×3 = 796` · `540+2×70 = 680` · `489+2×63 = 615` ⇒ **3,025**.

## 4) `deleted=3` ليس حذفًا — `\ No newline at end of file`

`git` يعيد إحصاء السطر الأخير عند إضافة فاصله فيسجّل `-1/+1` لملف واحد لا أكثر. الملفات الثلاثة:
`09_agencies_clients/Concept_{AccountWarmingCamouflage,OutcomeOwnershipLoop,PermissionChainAccountability}.md`.

**دليلان مستقلان على صفر الحذف (قيسا على الملفات الثلاثة نفسها):**
1. `minus_lines=1` و`plus_lines=11`، و**`minus[0] == plus[0]` ⇒ `True`** بايت-بالبات؛
   `git show HEAD:<file>` **لا ينتهي بفاصل سطر** (`endswith(b'\n') → False`)؛ وعلامة
   `\ No newline at end of file` حاضرة، ويظهر ذلك السطر في الطرف `-` ثم يُعاد إدراجه في `+` وفيه 10 أسطر جديدة.
2. **البايت-بالبات الكامل**: محتوى القرص **يبدأ بـ** محتوى `HEAD` في **306/306** ملف —
   `05_content_production 93/93 · 09_agencies_clients 80/80 · 06_hooks_retention 70/70 ·
   11_marketing_ads 63/63` أي `rewritten: 0`:
   ```bash
   cd /root/r/NB2 && python3 - <<'PY'
   import subprocess, glob
   for s in ['05_content_production','09_agencies_clients','06_hooks_retention','11_marketing_ads']:
       ok=bad=0
       for f in sorted(glob.glob('02_CONCEPTS/%s/*.md'%s)):
           old=subprocess.run(['git','show','HEAD:'+f],capture_output=True).stdout
           if old and open(f,'rb').read().startswith(old): ok+=1
           else: bad+=1
       print(s,"byte-prefix:",ok,"| rewritten:",bad)
   PY
   ```

## 5) احترام النطاق (بالقياس)

| الحارس | النتيجة |
|---|---|
| `01_outreach` | **UNCHANGED** — `sha256 6691fa49951a370a5bea39ae` قبلًا وبعدها · `--verify` = **0 معلّق** |
| `02_sales_calls` | **UNCHANGED** — `sha256 06a8cf32a5d6cf55760b33b1` · **0 معلّق** |
| `08_mindset` | **UNCHANGED** — `sha256 310afa401f684b8414abdf61` · **0 معلّق** |
| `07_branding` | **UNCHANGED** — `sha256 532ba83f15525dcf8963bd77` · **0 معلّق** |
| `03_offers_pricing` | **UNCHANGED** — `sha256 2b2785babd6706f197c1aedf` · **0 معلّق** |
| `terms_26k` | **UNCHANGED** — بصمة `aac73c49b473` · 27,742 ملفًا · 38,306,837 بايت (قبلًا=بعدًا) |
| `C_Ext01..15` | **لم تُمَسّ** — `01_outreach` خارج النطاق؛ الـ15 `??` هي نفسها قبل وبعد (`C_Ext01…15`) |
| `git status --porcelain \| cut -c1-2 \| sort \| uniq -c` | `1479 M` + `15 ??` ⇒ **صفر** جديد/محذوف |
| ملفات معدَّلة خارج `02_CONCEPTS/` | **0** |
| خارج الأربعة | **0** كتابة · لا `push` · لا commit · لا `/sdcard` · لا `rm/rmdir/shred/dd` |

## 6) المتبقي من 14,564 بالأرقام

```
الخطة الكلية  : 14,564 رابطًا / 1,836 مفهومًا / 23 قطاعًا
المُطبَّق (9)  : 11,800 رابطًا / 1,480 مفهومًا  (100% من حصصها، صفر معلّق)
المتبقي       :  2,764 رابطًا /   356 مفهومًا /    14 قطاعًا
```

المتبقي (تنازليًا): `04_content_strategy` 483/60 · `12_growth` 468/59 · `17_ai_automation` 377/47 ·
`10_funnels` 329/41 · `20_productivity_learning` 272/34 · `19_operations_teams` 258/33 ·
`99_uncategorized` 203/25 · `15_platforms_algo` 142/18 · `16_business_models` 97/12 ·
`13_storytelling` 78/11 · `14_copywriting` 37/7 · `22_finance_legal` 12/4 ·
`21_persuasion_psych` 6/3 · `18_trust_authority` 2/2 — خارج نطاق هذه المهمة عمدًا.