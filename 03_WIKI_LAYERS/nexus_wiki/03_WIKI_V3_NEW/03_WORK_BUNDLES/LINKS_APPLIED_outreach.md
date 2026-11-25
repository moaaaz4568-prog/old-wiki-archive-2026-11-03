# LINKS_APPLIED_outreach — تطبيق خطة الروابط على قطاع outreach

> منفّذ آليًا عبر `V3/03_WORK_BUNDLES/apply_links.py` · إضافة فقط (append) · **بلا تعديل أو حذف لسطر موجود**.
> النطاق: `/root/r/NB2/02_CONCEPTS/01_outreach/*.md` حصرا. الزمن: دقائق قليلة.

---

## 1) الخلاصة بالأرقام

| المقياس | القيمة |
|---|---:|
| ملفات outreach في الخطة | **133** |
| ملفات عُدِّلت | **133 / 133** (100%) |
| ملفات مُستبَعة | **0** |
| روابط كُتبت | **1,074** |
| — منها مفاهيم `Concept_…` | 1,064 |
| — منها توترات `TENSION_…` | 10 |
| أهداف فريدة (جذر لا يتكرر) | 138 |
| روابط لم تُلحَ ملفًا حقيقيًا (رُفضت) | **0** |
| **روابط معلّقة بعد التطبيق** | **0** |
| `git diff --numstat` | `added=1344, deleted=4` |
| ملفات بلا فاصل سطر نهائي (يُكتمَل بفصل) | 4 |

**مطابقة الرقم البنيوي للـ `added=1344`:**
1,074 سطر رابط + 133 عنوان `## الروابط` + 133 سطر فاصل + 4 أسطر إكمال فاصل نهائي
= **1,344** — مطابق لـ`numstat` مطابقةً تامّة، دون فرق.

**التغطية مقابل الخطة:** outreach يملك 1,074 رابطًا من أصل 14,564 في `LINK_PLAN.jsonl`
(100% من حصة القطاع نُفِّذت). البقية — 13,490 رابطًا في 1,703 مفهوم — خارج نطاق هذه المهمة.

---

## 2) صفر حذف — بأمر git

```bash
git -C /root/r/NB2 diff --numstat -- 02_CONCEPTS/01_outreach \
  | awk '{d+=$2;a+=$1}END{print "added="a",deleted="d}'
# added=1344,deleted=4
```

### الحذف = 4، وليست 0 — وهذا سببه البنيوي

`deleted=4` كلها في **4 ملفات لم تكن تنتهي بفاصل سطر**:

```
11  1  02_CONCEPTS/01_outreach/Concept_AttributionReframeOutreach.md
11  1  02_CONCEPTS/01_outreach/Concept_ContentDistributionMultiplication.md
11  1  02_CONCEPTS/01_outreach/Concept_DecisionMakerBypass.md
11  1  02_CONCEPTS/01_outreach/Concept_SenderProfileSignalAlignment.md
```

كلّها نفس النمط، حرفًا بحرف:

```diff
-- Document_Merged_(1)_(١)_PDF_to_Text_765_554.txt · ازاي عملت فلوس من الاونلاين بيزنس وانا 19 سنه ( مش كدب ).txt
\ No newline at end of file
+- Document_Merged_(1)_(١)_PDF_to_Text_765_554.txt · ازاي عملت فلوس من الاونلاين بيزنس وانا 19 سنه ( مش كدب ).txt
+
+## الروابط
+- [[Concept_SixElementEmailStack]]
…
```

**القراءة:** السطر «محذوف» وإعادة إضافته **متطابقان بايتًا-بالبات** — الوحيد المتغيّر هو
غياب الفاصل `\n` ثم وجوده. لا يوجد أي احتمال هندسي لكتابة محتوى بعد سطر بلا فاصل نهائي
دون إتمام هذا الفاصل، فالسبب بنيوي لا اختياري.

### الدليل المستقل عن git

`git diff` يقارن *سجلات سطور*، فيتغيّر سجلّ السطر الأخير عند اكتمال الفاصل. التحقق البايتي
الذي لا يعرف عن git شيء:

| الفحص | النتيجة |
|---|---|
| هل يبقى الأصل بادئة بايتية للناتج؟ (`after.startswith(before)`) | **133 / 133** |
| هل غيّر أي سطر من أسطر الأصل؟ | **0 ملف** |
| أزواج `(-x / +x)` حيث `x` متطابق بايتيًا | **4 / 4** (أقصى حدّ نظري) |
| سطور محذوفة بلا إضافة مطابقة | **0** |
| سطور محذوفة غير مرفقة بعلامة `\ No newline at end of file` | **0** |

**الحكم:** لا محو محتوى. الحذف الأربعة في `numstat` أثر إحصائي لغياب فاصل سطر مسبق
الوجود في 4 ملفات، لا تصحيحًا ولا تعديلًا.

> **بديل كان ممكنًا:** استبعاد هذه الملفات الأربعة يحقّق `deleted=0` حرفيًا — لكنه يترك 4
> مفاهيم بلا أي رابط، أي 4 مفاهيم تبقى ميتة. اخترت تغطية القطاع كاملًا وإفصاح السبب،
> لا تجميل الرقم على حساب الهدف.

### ضمان إضافي على مستوى الكود

`append_block()` يرفض الكتابة إن لم يبدأ مؤشرها من EOF، ويثبّت بعد كل كتابة أن
`الناتج == الأصل + الكتلة` بايتًا بايتًا:

```python
with path.open("a", encoding="utf-8", newline="\n") as fh:
    if fh.tell() != size_before:
        raise RuntimeError("مؤشر الكتابة != الحجم الأصلي — رفض الكتابة")
    fh.write(block); fh.flush(); os.fsync(fh.fileno())
after = path.read_bytes()
assert after.startswith(data) and after == data + block_bytes
```

لا يوجد في السكريبت مسار `write()` ولا `write_text()` ولا إعادة قراءة-وتعديل-وكتابة.

---

## 3) صفر رابط معلّق

```bash
grep -o '\[\[[^]]*\]\]' /root/r/NB2/02_CONCEPTS/01_outreach/*.md \
  | sed 's/^[^:]*://' | sed 's/\[\[//;s/\]\]//' | sort -u > /tmp/links.txt
# 138 أهداف فريدة، 1,074 ورودًا
```

ثم التحقق الآلي أن كل جذر يقابل ملفًا موجودًا على القرص:

| الفحص | القيمة |
|---|---:|
| أهداف فريدة | 138 |
| تُحلّ ملفًا حقيقيًا | **138** |
| **روابط معلّقة** | **0** |

ووضع الفحص المستقل داخل السكريبت نفسه:

```bash
python3 V3/03_WORK_BUNDLES/apply_links.py --verify
# النطاق: 02_CONCEPTS/01_outreach
# ملفات .md: 133  |  منها بقسم '## الروابط': 133
# إجمالي ورود الروابط: 1074  |  أهداف فريدة: 138
# جذور مُفهرسة على القرص: 29643
# روابط معلّقة (لا تُحلّ ملفًا حقيقيًا): 0      → exit=0
```

**الآلية:** أي رابط لا يقابل `Concept_<slug>.md` أو `TENSION_<code>.md` على القرص
**يُرفَض ولا يُكتب** — لا يُكتَب إلا ما يُفتَح. هذا شرط البناء، لا فحص نهائي فقط.

---

## 4) تعارض التسمية — موقّف وموثّق (القاعدة: لا تخمّن)

`LINK_PLAN.jsonl` مُصدَّرة بـ `--link-form alias`، وقاعدتها الموثّقة في
`build_link_plan.py` (§36–48):

```
C_<slug>  ⇒  02_CONCEPTS/<sector>/Concept_<slug>.md
X_<code>  ⇒  05_TENSIONS/TENSION_<code>.md
```

**هذه قاعدة تحويل، وليست أسماء ملفات.** على القرص:

| الأمر | النتيجة |
|---|---:|
| `find NB2 -name 'C_*.md'` (بعداً عن TRASH) | **0** |
| `find NB2 -name 'Concept_*.md'` | **31,504** |
| روابط حية بصيغة `[[C_…]]` في كل الـvault | **0** |
| روابط حية بصيغة `[[Concept_…]]` | آلاف (مثل `[[Concept_SmartLead]]` ×11) |

Obsidian يحلّ `[[target]]` **بجذع اسم الملف فقط**، فلا يوجد أي ملف `C_X.md` ⇒ كل
`[[C_X]]` يكون رابطًا معلّقًا حتمًا. أي تطبيق حرفي لصيغة `alias` على 1,074 رابطًا
كان سيُنتج 1,074 رابطًا معلّقًا ويُبقي الـWiki ميتًا — وهو عكس الهدف مباشرةً.

### القرار المُنفَّذ والمستند

أُصدِر **صيغة الجذع** (`--link-form stem` في مولّد الخطة نفسه)، وهي الترجمة التي
يستعملها `build_link_plan.py` عند التحقق من الصلاحية في سطريه 556–558:

```python
if link.startswith("C_"):   ok = ("Concept_" + link[2:]) in stems
elif link.startswith("X_"): ok = ("TENSION_" + link[2:]) in stems
```

| العنصر | قبل | بعد |
|---|---|---|
| المفهوم | `C_OneToOneSignalPersonalization` | `[[Concept_OneToOneSignalPersonalization]]` |
| التوتر | `X_B8` | `[[TENSION_B8]]` |
| صيغة alias مكتوبة فعليًا | — | **0** (`grep -ohE '\[\[(C\|X)_[^]]*\]\]'` = 0) |

**ما تغيّر:** صيغة الإصدار فقط. **ما لم يتغيّر:** قائمة الأهداف، وعددها، وترتيبها
التنازلي حسب أعلى درجة تشابه من الخطة الأصلية. هذا ليس تخمينًا: صيغة `alias` لا
تحلّ شيئًا على القرص، وصيغة الجذع هي المعهودُ الوحيد الموثّق فعليًا في الـvault.

> لو أراد المُفَوِّض صيغة `alias` رغم ذلك، فالطريق صحيح وغير مقلوب: شغّل
> `build_link_plan.py --emit --link-form stem` بدل `alias`، أو أعد التسمية على مستوى
> الـvault من `Concept_` إلى `C_` — وهذا إجراء تسمية مستقلّ أكبر بكثير من نطاق هذه
> المهمة، ولا يصحّ مزجه بها.

---

## 5) خمسة أمثلة قبل/بعد

### 5.1 `Concept_AIOnboardingTriad.md` — `+10 / -0`

```diff
  - gregoryjhickman: Dbra13IDRtW · thomassmedia: DGA-IC1Mvut · timdanilovhi: DFD7vsmSB2P
+
+## الروابط
+- [[Concept_OneToOneSignalPersonalization]]
+- [[Concept_MechanismSwapping]]
+- [[Concept_OnPlatformFunnel]]
+- [[Concept_VolumeSequenceAutomation]]
+- [[Concept_MultiChannelSameProspectStacking]]
+- [[Concept_PreCallPermissionPing]]
+- [[Concept_MessageProfileCongruence]]
+- [[Concept_PersonalizedLeadMagnet]]
```

### 5.2 `Concept_CommentGateLeadCapture.md` — `+11 / -0` (يحتوي رابط توتر)

```diff
  - DZsTQDZDGbY.txt (optimizedjake)
+
+## الروابط
+- [[Concept_Keyword_Gated_DM_Funnel]]
+- [[Concept_CommentIntentGate]]
+- [[Concept_CommentKeywordGate]]
+- [[Concept_CommentGatedLeadDelivery]]
+- [[Concept_OnPlatformFunnel]]
+- [[Concept_AuthorityCommenting]]
+- [[Concept_AttributionReframeOutreach]]
+- [[Concept_PreCallPermissionPing]]
+- [[TENSION_B8]]
```

### 5.3 `Concept_AttributionReframeOutreach.md` — `+11 / -1` (الحالة الوحيدة)

الملف لم يكن ينتهي بفاصل سطر، فاكتمل الفصل ثم أُضيف القسم:

```diff
-- Document_Merged_(1)_(١)_PDF_to_Text_765_554.txt · … ( مش كدب ).txt
\ No newline at end of file
+- Document_Merged_(1)_(١)_PDF_to_Text_765_554.txt · … ( مش كدب ).txt
+
+## الروابط
+- [[Concept_SixElementEmailStack]]
+- [[Concept_ContentDistributionMultiplication]]
+- [[Concept_SenderProfileSignalAlignment]]
+- [[Concept_StakeWeightedProspecting]]
+- [[Concept_ContentWorkProofAcquisition]]
+- [[Concept_BenchmarkedIteration]]
+- [[Concept_SolutionOutcomeFraming]]
+- [[Concept_ContentBeatsColdOutreach]]
```

### 5.4 `Concept_AuthorityCommentPipeline.md` — `+10 / -0`

```diff
  - OfferCraft Training- Replay Resources.txt (شريحة أسطر 9401-14138) — اليوم 2 د 0:02-0:30 …
+
+## الروابط
+- [[Concept_BorrowedAudienceValueComments]]
+- [[Concept_AuthorityCommenting]]
+- [[Concept_ReferralAskDeframing]]
+- [[Concept_Voice_Of_Customer_Mining]]
+- [[Concept_OneToOneSignalPersonalization]]
+- [[Concept_EnrichedHyperPersonalization]]
+- [[Concept_VolumeSequenceAutomation]]
+- [[Concept_EngagementAsWarmLeadSignal]]
```

### 5.5 `Concept_KeywordGatedLeadCapture.md` — `+10 / -0`

```diff
  - (تحقق استرداد 7-w2-B4rec) mattyr_ecom — عاين الاسترداد 3 ملفات من سلسلة ENVELOPE …
+
+## الروابط
+- [[Concept_CommentIntentGate]]
+- [[Concept_CommentKeywordGate]]
+- [[Concept_CommentGatedLeadDelivery]]
+- [[Concept_Keyword_Gated_DM_Funnel]]
+- [[Concept_CommentKeywordDMFunnel]]
+- [[Concept_FreePersonalizedDemoLeadgen]]
+- [[Concept_CommentGateLeadCapture]]
+- [[Concept_OnPlatformFunnel]]
```

**ملاحظة بصرية:** في كل الأمثلة السطر الأخير من الأصل باقٍ كما هو، والسطر الفاصل
الأبيض (`+` وحده) هو الحدّ بين النص الأصلي والقسم الجديد. لا يظهر أي سطر `-` عدا
الحالة 5.3 الموثّقة أعلاه.

---

## 6) أوامر التحقق الكاملة (مُعاد تشغيلها حرفيًا)

```bash
# 1) كم أُضيف وحُذف
git -C /root/r/NB2 diff --numstat -- 02_CONCEPTS/01_outreach \
  | awk '{d+=$2;a+=$1}END{print "added="a",deleted="d}'
# → added=1344,deleted=4

# 2) الأهداف الفريدة
grep -o '\[\[[^]]*\]\]' /root/r/NB2/02_CONCEPTS/01_outreach/*.md \
  | sed 's/^[^:]*://' | sed 's/\[\[//;s/\]\]//' | sort -u > /tmp/links.txt
# → 138

# 3) كل هدف = ملف حقيقي
python3 V3/03_WORK_BUNDLES/apply_links.py --verify   # → روابط معلّقة: 0 (exit=0)

# 4) لا صيغة alias تائهة
grep -ohE '\[\[(C|X)_[^]]*\]\]' /root/r/NB2/02_CONCEPTS/01_outreach/*.md | wc -l
# → 0

# 5) لا عنوان «الروابط» مكرّر (1 لكل ملف)
grep -c '^## الروابط$' /root/r/NB2/02_CONCEPTS/01_outreach/*.md | awk -F: '$2!=1'
# → (فارغ)
```

### الإعادة الآمنة (idempotence)

```bash
python3 V3/03_WORK_BUNDLES/apply_links.py --dry-run
# → الملفات يُكتب عليها: 0 | الروابط يُكتب: 0
#   مستبعد (تكرار/ذاتي/القسم قائم): 133
#   وضع --dry-run: لم تكتب أي بايت.
```

تكرار التطبيق **لا يضيف شيئًا** — تم التثبيت على نسخة اختبارات مستقلة في
`/tmp/opencode/scratch` قبل اللمس الفعلي، وأعيد التشغيل مرتين: `numstat` ثابت عند
`added=1344,deleted=4` في كلتيهما، وبادئة البات الأصل محفوظة في 133/133 ملفًا.

### تسلسل ما أُنفِّذ فعليًا

1. قراءة `LINK_PLAN.jsonl` (1,836 صفًا)، `LINK_PLAN_REPORT.md`، `V3/00_CHARTER/NAMING.md`.
2. مسح واقع القرص: جذور `Concept_`/`TENSION_`، صيغة الروابط الحية، `C_*.md` = 0.
3. اختبار `git diff` على `/tmp/opencode/difftest` لكشف أثر غياب الفاصل النهائي **قبل** اللمس.
4. بناء `apply_links.py`، تشغيل `--dry-run` (3 ملفات قبل/بعد).
5. **الـdry-run كشف عيبًا حقيقيًا:** فهرسة الجذور كانت تستبعد قطاع outreach نفسه،
   فكل روابطه الداخلية رُفضت «غير قابلة للحلّ» (ملف واحد خرج برابط واحد من 9).
   أُصلح، وأعيد الفحص: 1,074 رابطًا صفر مرفوض.
6. تطبيق على `/tmp/opencode/scratch/NB2` (نسخة 133 ملفًا) → نفس الأرقام، + idempotence
   + إثبات البادئة الباتية.
7. تطبيق على الشجرة الحقيقية بعد تأكيد `git status --porcelain` فارغًا (قاعدة نظيفة).
8. أوامر التحقق الخمس أعلاه.

---

## 7) ما تبقى (خارج نطاق هذه المهمة)

| القطاع | الحالة |
|---|---|
| `01_outreach` | **مُنفَّذ** — 133 ملفًا، 1,074 رابطًا، 0 معلّق |
| القطاعات الـ23 المتبقية | **لم يُمَسّ** — 1,703 مفهوم، 13,490 رابطًا |

السكريبت يقبل النطاق كوسيط، فالإدامة لأي قطاع آخر مباشرة:

```bash
python3 V3/03_WORK_BUNDLES/apply_links.py \
  --scope 02_CONCEPTS/02_sales_calls --dry-run
```

وملاحظة استباقية قبل الإدامة: عيب الفهرسة المُصحَّح أعلاه يجعل كل قطاع **يتضمّن
نفسه** — فأي قطاع يُضاف لاحقًا سيحصل على روابطه الداخلية أيضًا، وهي كانت ستُفقد لولا
هذا الإصلاح.

---

## 8) ما لم يُنفَّذ عمدًا

- **`sections_missing: ["التعريف"]`** في صفوف الخطة **لم يُمَسّ**. هذه المهمة رُكِّزت
  على الروابط حصراً، وإضافة قسم تعريف تعني توليد محتوى مفاهيمي — قرار تحريري منفصل
  يحتاج مصدراً، لا آلية إضافية آلية. 1,832 مفهومًا بلا قسم تعريف على مستوى الـvault
  (من `LINK_PLAN_REPORT.md` §4)؛ outreach حصريًا هو جزء منها.
- **`no_frontmatter`** (1,833 مفهومًا) — نفس المنطق: لا تُنشأ بيانات بلا مصدر.
- **لا حذف، لا push، لا كتابة خارج النطاق.** لم يُنفَّذ أي `rm`/`rmdir`/`shred`/`dd`،
  ولم تُكتب أي بايت إلى `/sdcard` أو خارج `/root/r`.
- **لم يُلتَمَس أي ملف في خارج `02_CONCEPTS/01_outreach/`.**
