# LINKS_APPLIED_sector2 — تطبيق خطة الروابط على القطاع الثاني `02_sales_calls`

> منفّذ آليًا عبر `V3/03_WORK_BUNDLES/apply_links.py` · إضافة فقط (append) · **بلا تعديل أو حذف لسطر موجود**.
> النطاق: `/root/r/NB2/02_CONCEPTS/02_sales_calls/*.md` حصرًا. قطاع واحد فقط.

---

## 1) لماذا هذا القطاع

اختيار **أكبر قطاع بعد `01_outreach`** من `LINK_PLAN.jsonl`:

| رتب�� | القطاع | ملفات في الخطة |
|---:|---|---:|
| 1 | `01_outreach` *(مستثنى — سبق تطبيقه)* | 133 |
| **2** | **`02_sales_calls` ← الهدف** | **500** |
| 3 | `08_mindset` | 200 |
| 4 | `07_branding` | 175 |
| 5 | `03_offers_pricing` | 166 |

ملاحظة تشغيلية: السكربت لا يقبل معاملًا موضعيًا، بل `--scope`. استُخدم:
`python3 .../apply_links.py --scope 02_CONCEPTS/02_sales_calls [—dry-run|--verify]`.

---

## 2) الخلاصة بالأرقام

| المقياس | القيمة |
|---|---:|
| ملفات القطاع على القرص | **500** |
| ملفات في الخطة | **500** (500 مسار فريد، صفر ملف ناقص) |
| ملفات عُدِّلت | **499 / 500** |
| ملفات مُستبَعة | **1** (`Concept_Pattern_Interrupt.md` — الخطة لم تقترح له أي رابط) |
| روابط كُتبت | **4,029** |
| — منها مفاهيم `Concept_…` | 3,992 |
| — منها توترات `TENSION_…` | 37 |
| أهداف فريدة (جذر لا يتكرر) | **497** |
| روابط لم تُحلّ ملفًا حقيقيًا (رُفضت) | **0** |
| ملفات بقسم `## الروابط` | **499 / 500** |
| ملفات بلا فاصل سطر نهائي (يُكتمَل بفصل) | 10 |
| **`--verify` ⇒ روابط معلّقة** | **0** ✅ |
| `git -C /root/r/NB2 diff --numstat` (القطاع) | **`added=5037, deleted=10`** |

**مطابقة الرقم البنيوي لـ`added=5037` (بلا فرق):**
4,029 سطر رابط + 2×489 ملفًا (فاصل + عنوان `## الروابط`) + 3×10 ملفًا (إعادة إدراج السطر الأخير بلا فاصل + فاصل + عنوان)
= **5,037** — مطابق لـ`numstat` مطابقةً تامّة.

---

## 3) بوابة التحقق

```bash
python3 /root/r/V3/03_WORK_BUNDLES/apply_links.py \
  --scope 02_CONCEPTS/02_sales_calls --verify
# النطاق: 02_CONCEPTS/02_sales_calls
# ملفات .md: 500  |  منها بقسم '## الروابط': 499
# إجمالي ورود الروابط: 4029  |  أهداف فريدة: 497
# جذور مُفهرسة على القرص: 29643
# روابط معلّقة (لا تُحلّ ملفًا حقيقيًا): 0
# EXIT=0
```

`EXIT=0` = **صفر رابط معلّق**، وتوقّف الشرط 5 لم يُطلق: لم تظهر أي وصلة معلقة.

---

## 4) `deleted=10` تفسيرُه — ليس حذفًا للمحتوى

الرقمان `+11/-1` في `numstat` يظهران لملفات بلا فاصل سطر نهائي، لأن `git` يُعيد إحصاء السطر الأخير عند إضافة فاصله:

```diff
 ## المصدرية
-- يومين في حياة رائد اعمال ١٨ سنة... (نص السطر كما هو)
\ No newline at end of file
+- يومين في حياة رائد اعمال ١٨ سنة... (نفس النص حرفيًا)
+
+## الروابط
+- [[Concept_RepeatPurchaseCompounding]]
...
```

الملفات العشرة: `Concept_AttractiveServiceSelection` · `Concept_FirstImpressionEngineering` ·
`Concept_MoneyFocusProcessCorruption` · `Concept_PriceCommitmentFilter` ·
`Concept_ProofFirstReferralChain` · `Concept_ReflectFirstMeetingControl` ·
`Concept_RemoteSellingThroughput` · `Concept_RepeatPurchaseCompounding` ·
`Concept_SelfConclusionSelling` · `Concept_StarvingCrowdMarketSelection`.

**دليل مستقل على صفر الحذف** — محتوى `HEAD` بايت-بالبات سابقة تمامًا لمحتوى القرص في **500/500** ملف:

```bash
python3 - <<'PY'
import subprocess, glob
files = sorted(glob.glob('02_CONCEPTS/02_sales_calls/*.md'))
ok = bad = 0
for f in files:
    old = subprocess.run(['git','show','HEAD:'+f], capture_output=True).stdout
    if open(f,'rb').read().startswith(old): ok += 1
    else: bad += 1
print("byte-prefix:", ok, "| rewritten:", bad)
PY
# byte-prefix: 500 | rewritten: 0
```

---

## 5) احترام النطاق

```bash
git -C /root/r/NB2 diff --numstat | awk -F'\t' '{split($3,a,"/"); print a[1]"/"a[2]}' | sort | uniq -c
#   133 02_CONCEPTS/01_outreach        ← تعديلات سابقة (قبل هذه المهمة، لم تُمَسّ)
#   499 02_CONCEPTS/02_sales_calls     ← تعديلات هذه المهمة
git -C /root/r/NB2 status --porcelain | grep -vc '^ M'   # 0 ⇒ لا ملف جديد ولا محذوف
```

- `01_outreach`: **لم يُمَسّ** (الـ133 تعديلًا موجودة من تشغيل `LINKS_APPLIED_outreach.md` السابق).
- `terms_26k`: **لم يُمَسّ** (0 ملف معدَّل).
- لا كتابة خارج `02_CONCEPTS/02_sales_calls/`، ولا ملف جديد، ولا `push`.
- السكربت يفتح بوضع `'a'`، ويفشل إن كان مؤشر الكتابة ≠ الحجم الأصلي، ويعيد التحقق أن الناتج = الأصل + الكتلة.

---

## 6) التغطية المتبقية خارج هذا النطاق

`02_sales_calls` استهلك 4,029 رابطًا من `LINK_PLAN.jsonl` بالكامل (100% من حصة القطاع).
إجمالي الخطة 14,564 رابطًا في 1,836 مفهومًا؛ بعد التطبيقين (outreach 1,074 + sector2 4,029)
يتبقّى **9,461 رابطًا في 1,203 مفهوم عبر 21 قطاعًا** لم تُطبَّق بعد — خارج نطاق هذه المهمة عمدًا.