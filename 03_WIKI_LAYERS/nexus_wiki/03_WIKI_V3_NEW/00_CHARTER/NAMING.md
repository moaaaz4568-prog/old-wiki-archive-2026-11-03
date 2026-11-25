# NAMING — عقد التسمية في V3

<!-- counts-ref: V3_SYS/COUNTS.json -->
<!-- atoms=27742 concepts=1841 masters=5 -->

> ⚠️ صحّح 2026-10-02 (T1+T2): كان الوسم `concepts=1841` مخلوطاً بين ملف ومفهوم — والصحيح فصل الحقلين: `concepts=1836 files=1841`، ومعه `masters=5 indexes=5 masters_total=10`. الوسم المصحَّح: `<!-- atoms=27742 concepts=1836 files=1841 masters=5 indexes=5 masters_total=10 -->`.
> الدليل: `find /root/r/NB2/02_CONCEPTS -name 'Concept_*.md' -not -path '*terms_26k*' | wc -l` ⇒ **1836** · `find /root/r/NB2/02_CONCEPTS -name '*.md' -not -path '*terms_26k*' | wc -l` ⇒ **1841** · `find /root/r/NB2/03_MASTERS -name 'Master_*.md' | wc -l` ⇒ **5** · `find /root/r/NB2/03_MASTERS -name '_index.md' | wc -l` ⇒ **5**.

> الاسم هو **مفتاح البحث الأول**. من لا يستطيع استرجاع كيان باسمه لا يملكه.

## 1) الصيغة الإلزامية

```
<BADGE>_<Canonical_Slug>.md
```

`<BADGE>` بادئة النوع (جدول §3) وتسبق الشرطة السفلية دائماً · `<Canonical_Slug>` الاسم المتعارف عليه لا الداخلي ولا المؤقت · لا مسافات ولا `copy/final/new` · `.md` إلزامي.

| ✅ صحيح | لماذا | | ❌ خاطئ | الخطأ |
|---|---|---|---|---|
| `C_Pattern_Interrupt.md` | الآلية لا الأداة | | `C_IceBreaker_V2_FINAL.md` | أداة + نسخة + حجز اسم |
| `C_كسر_التوقع.md` | العربي كما ورد | | `C_0.5_Reply_Rate.md` | كسر عشري مولَّد |
| `M_Sales_Call_Architecture.md` | سؤال الماستر | | `concept_Map.md` | بادئة غير مُعرَّفة |
| `X_Proof_Over_Polish.md` | طرفان متعارضان | | `X1.md` | رقم مكان البادئة |

## 2) العربية والإنجليزية والمرادف

| القاعدة | التفصيل |
|---|---|
| **العربية كما وردت** | لا تُصحَّح ولا تُترجم ولا تُنقّط — التشكيل والإملاء المطبَّع يبقى. |
| **الإنجليزية لا تُترجم** | المصطلح التقني يبقى: `funnel` · `retention` · `cadence` · `warmup`. |
| **العربية أولاً في العنوان** | `# كسر التوقع · Pattern Interrupt` |
| **المرادف = حقل لا ملف** | يدخل `aka:` في YAML — ملف واحد مهما بلغ عدد أسمائه. |
| **الاسم يصف الآلية** | `PatternInterrupt` لا `IceBreaker` (بوصفة `CHARTER.md §3`). |

```yaml
type: concept
name: كسر التوقع · Pattern Interrupt
aka: [ مفاجأة الأسلوب, نمط المقاطعة, Pattern Break ]
```

## 3) جدول البادئات الإلزامي

| النوع | البادئة | المجلد | | النوع | البادئة | المجلد |
|---|---|---|---|---|---|---|
| Source | `S_` | `01_SOURCES/` | | Glossary | `G_` | `05_GLOSSARY/` |
| Term | `T_` | `02_TERMS/` | | Provenance | `P_` | `06_PROVENANCE/` |
| Concept | `C_` | `03_CONCEPTS/` | | Master | `M_` | `07_MASTERS/` |
| Tension | `X_` | `04_TENSIONS/` | | Synthesis | `Y_` | `08_SYNTHESIS/` |

> ⚠️ **صحّح 2026-10-02 (T7 · جدول المجلدات مكسور بالكامل):** كان الجدول أعلاه على مخطط `01_SOURCES / 02_TERMS / 03_CONCEPTS / 07_MASTERS`، **ولا واحد منها موجود على القرص**. الجدول الصحيح على مخطط القرص:
>
> | النوع | البادئة | المجلد **الصحيح** | ما هو عليه الآن |
> |---|---|---|---|
> | Source | `S_` | **`07_SOURCES/`** | `01_SOURCES/` غير موجود |
> | Term (ذرّة) | `T_` | **`01_ATOMS/`** | `02_TERMS/` غير موجود |
> | Concept | `C_` | **`02_CONCEPTS/`** | `03_CONCEPTS/` غير موجود |
> | Master | `M_` | **`03_MASTERS/`** | `07_MASTERS/` غير موجود |
> | Tension | `X_` | `04_TENSIONS/` | صحيح (موجود، 0 ملفات) |
> | Glossary | `G_` | `05_GLOSSARY/` | صحيح (موجود) |
> | Provenance | `P_` | `06_PROVENANCE/` | صحيح (موجود، فارغ) |
> | Synthesis | `Y_` | `08_SYNTHESIS/` | صحيح (موجود) |
>
> **الدليل:** `for d in 01_SOURCES 02_TERMS 03_CONCEPTS 07_MASTERS 07_SOURCES 01_ATOMS 02_CONCEPTS 03_MASTERS; do test -d /root/r/V3/$d && echo "$d EXISTS" || echo "$d MISSING"; done` ⇒ `01_SOURCES MISSING` · `02_TERMS MISSING` · `03_CONCEPTS MISSING` · `07_MASTERS MISSING` · `07_SOURCES EXISTS` · `01_ATOMS EXISTS` · `02_CONCEPTS EXISTS` · `03_MASTERS EXISTS`.
> **أثره:** كل أمر في الميثاق يبني على `find … 03_CONCEPTS` يفشل دائماً ⇒ بند التغطية لا يمرّ أصلاً (انظر `FORMAT_MASTER.md` و`DO_MASTER.md` سطر تصحيح T7).

البادئة ليست اختيارية ولا تُترجم: `مفهوم_` و`concept_` مرفوضان. الرقم المنطقي (`A1`) عنصر **بعد** البادئة: `X_A1.md` مقبول، `X1.md` مرفوض. ولا اسم يبدأ برقم: `C_3_Step_Cadence.md` ❌ · `C_Three_Step_Cadence.md` ✅.

## 4) المحظورات الثلاثة

### 4.1 كسر عشري مولَّد آلياً

```
C_0.5_Reply-Rate_Cutoff.md   ❌      C_Reply_Rate_Cutoff.md   ✅
C_0.001_Reply_Rate.md        ❌      C_0.8x_ROAS_ضمن_الهدف.md ❌
C_0.10-0.20_bulk_Accounts.md ❌
```

**لماذا:** الآلة تولّد الاسم من رقم مخزَّن، فتفقد الملف هويته عند أول تعديل للرقم. **على القرص:** 5 حالات مطابقة `^Concept_0\.[0-9]` (و`audit.py C15` يسجّل 981 اسماً مولَّداً إجمالاً).

```bash
find /root/r/NB2/02_CONCEPTS -name 'Concept_0.*' -print | wc -l   # 5
```

### 4.2 الأرقام داخل الاسم

الأرقام **الكمية** (9,585 · 3% · 2024) داخل النص مقبولة؛ الأرقام **الاسمية** (`3_Step`) مرفوضة.

### 4.3 الإصدارات في الاسم

`v1` / `v2` / `v3` / `FINAL` / `NEW` / `OLD` ممنوعة: `C_Foo_v2.md` يجعل `C_Foo.md` بتيم بلا هوية فيظهر الاثنان ويختار القارئ عشوائياً. الإصدار في البيانات لا في المسار:

```bash
grep -m1 '^version:' "$f"     # الإصدار metadata، لا اسم
```

## 5) redirect stub

### 5.1 صيغة v2 (سابقة موجودة — 125 ملفاً)

```markdown
---
type: concept_redirect
name: AI Email Warmup (2-Week Minimum)
merged_into: Concept_AI_Email_Warmup_2_Week_Minimum
---

> دُمج هذا المصطلح في [[Concept_AI_Email_Warmup_2_Week_Minimum]]
```

### 5.2 صيغة v3 (المعتمدة)

```markdown
---
type: redirect
redirect_to: C_Pattern_Interrupt
aka: [ مفاجأة الأسلوب ]
---

# أُعيدت التوجيه → C_Pattern_Interrupt
هذا الاسم كان معتمداً في v2. الكيان الحالي: [[C_Pattern_Interrupt]].
لماذا: الاسم الجديد يصف الآلية لا الأداة.
```

**أربعة فروق عن v2 عمداً:** `type: redirect` (الكيان ليس بالضرورة مفهوماً) · `redirect_to` بدل `merged_into` (إعادة توجيه لا دمج — الأصل باقٍ) · سطر `لماذا:` الإلزامي · `aka:` لمرادفات فقدها الاسم القديم.

### 5.3 متى يُنشأ

الاسم القديم **موجود فعلاً** على القرص · الهدف `redirect_to` كيان مُعتمد (لا stub إلى stub) · سبب التحويل في سطر واحد. تحويل صامت = فقدان هوية.

### 5.4 حالة العرف في v2

من `terms_26k/` (27,742 ملفاً)؛ المرجع `COUNTS.json → nb2.terms_26k.files`.

| القياس | القيمة | الأمر |
|---|---:|---|
| بطاقات بوسم `type: concept_redirect` | **125** | عدّ `^type: concept_redirect` |
| بطاقات فيها إشارة دمج **بدون** وسم | **0** | عدّ `merged_into` مع غياب الوسم |
| بطاقات فيها كلمة `redirect` في متنها | 190 | `grep -rl 'redirect' . \| wc -l` |
| بطاقات `mentions: 1` | 27,338 (98.54%) | `grep -rl 'mentions: 1$' . \| wc -l` |

**الحكم:** وسم الـredirect **سليم تماماً** — 125 وسم، صفر دمج بلا وسم. الكسر في مكانين آخرَين: الـ125 كلها في `99_misc/part_01` (الحاوية المهملة)، و`mentions: 1` يعني 27,338 بطاقة بلا ارتباط بمفهوم.
والـ190 وروداً لكلمة `redirect` **ليست** وسوماً: مثالها `Concept_CNAME_Verification_…` حيث «redirecting» جزء من شرح DNS.

> الرقم «1,039 بدون وسم» الوارد في تكليف المهمة **لم أتمكّن من إعادة إنتاجه** بأي تعريف قابل للعدّ. أقرب إشارة مكررة: **206 ملفاً في 103 مجموعة** أسماء متطابقة بعد التطبيع، ولا يخرج أيٌّ منها عن الـ125.

## 6) خلاصة قابلة للتنفيذ

- [ ] البادئة صحيحة ومطابقة للمجلد و`type` (تعداد ثلاثي — `GATES_11.md` §D01).
- [ ] لا رقم اسمي، لا كسر عشري، لا `v1/v2/v3`, لا كلمة حجز اسم.
- [ ] العربية كما وردت، والإنجليزية لم تُترجَم، والمرادفات في `aka:`.
- [ ] كل تحويل اسم له stub وإلا فليس تحويلاً — بل فقدان.
