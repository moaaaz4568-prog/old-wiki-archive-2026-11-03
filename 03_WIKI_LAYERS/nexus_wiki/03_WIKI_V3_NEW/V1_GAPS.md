# V1_GAPS — فجوات وأرقام مُقاسة لنسخة v1

> **مهم:** كل رقم في هذا الملف **مُقاس بأداة على القرص**، ولا يوجد رقم مُخمَّن.
> كل أمر مُنفَّذ مذكور حرفياً إلى جانب النتيجة ليسهل إعادة التحقق.
>
> - v1 = `/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/`
> - القياس بتاريخ: 2026-10-01
> - فرع العمل: `v3-fix` (base `4ccd0ca`)
> - **لا شيء حُذف ولا نُقل ولا أُرشف في هذه المهمة** — الأبواب اللاحقة تتكفّل بالنقل/الأرشفة.
> - الملفات الميتة **لا يجوز حذفها**؛ هذا الملف توثيق فقط.

---

## 1) الملفات الفارغة/الميتة — العدد والاسم

### 1.1 النتيجة: **صفر** ملف `.md` فارغ

```bash
find $PKG -type f -name "*.md" | wc -l                              # → 5451
find $PKG -type f -name "*.md" -size 0 | wc -l                       # → 0
find $PKG -type f -name "*.md" -size 0 | sed "s|$PKG/||" | sort      # → (فارغ)
```

تحقّق إضافي بـ Python (يشمل الفراغ المحتمل `whitespace-only`، وهو أضيق من `-size 0`):

```python
# os.walk على الشجرة كلها: 0 ملف .md بحجم 0، و0 ملف .md كل محتواه مسافات/أسطر فارغة
ZERO/BLANK .md = 0
```

**الخلاصة:** لا يوجد ملف `.md` ميت/فارغ في v1. العدد المُبلَّغ عنه في التوجيه
(`find … -size 0 | wc -l`) يساوي **0** وليس عدداً موجباً.

### 1.2 ملفّا صفريبا الحجم (لكنهما ليسا `.md`) — **لا يُحذفان**

| المسار | الحجم | الحكم |
|---|---|---|
| `brain/processed/jaydenleilua/DbbY21Ggazg.txt` | 0 بايت | ملف ناتج تفريغ (فيديو بلا كلام؟) — يحتاج فحص مصدر، **ليس `.md`** |
| `nexus_vault/02_sales_closing/.gitkeep` | 0 بايت | **متعمَّد** — يحفظ المجلد في git. حذفه يمسح المجلد من الفهرس |

```bash
find $PKG -type f -size 0 -printf '%p\n'      # → الملفان أعلاه بالضبط (2)
```

### 1.3 `Master_Sales_Funnel_Strategy.md` — ليس ميتاً، بل **مؤرشف**

```bash
wc -l $PKG/nexus_vault/*/Master_Sales_Funnel_Strategy.md
# → wc: … No such file or directory   (لأنه ليس في أي مجلد نشط)
find $PKG -name "Master_Sales_Funnel_Strategy.md" -printf '%s bytes  %p\n'
# → 96436 bytes  $PKG/nexus_vault/_archive/superseded_masters/Master_Sales_Funnel_Strategy.md
```

الملف **موجود وسليم 96,436 بايت** لكنه في `_archive/superseded_masters/` فقط.
 ملاحظة: حسب `.nexus_work/apply/mirror` فهو **ليس** من الـ16 ناقصاً (انظر §3) —
 لسبب أنه غير نشط أصلاً فلا يدخل في تغطية الـmirror.

### 1.4 ملفات `.md` صغيرة جداً (<512 بايت) — **155 ملفاً**، ليست فارغة

أصغرها واحد حقيقي ومقصود:

```
29 B  .nexus_work/youtube_analysis/YT_y37.md   → "# 🧠 يوتيوب y37 — 18 ملف"
29 B  .nexus_work/youtube_analysis/YT_y60.md   → "# 🧠 يوتيوب y60 — 18 ملف"
```

والباقي (153 ملفاً) هي بطاقات كيان/أداة مثل
`Nexus_Brain/wiki/tools/Tool_CRM.md` (161 بايت) ونسخها في
`.nexus_work/backup/pre_unification/wiki_full/tools/`. **لا تعبث بها.**

---

## 2) المسارات الميتة — الإصلاح الفعلي

### 2.1 المُصلَح (داخل نطاق v1) — **ملفان، 3 ثوابت مسار**

| # | الملف | السطر | المسار الميت | البديل الصحيح | الدليل على صحّة البديل |
|---|---|---|---|---|---|
| 1 | `.nexus_work/apply/merge_tables.py` | 11 | `/root/r/nexus_enrichment/state/apply_wiki/mirror/*.md` | `MIRROR_DIR = Path(__file__).resolve().parent / 'mirror'` | `exists=True` · `23 ملف` · **متتبَّع في git** |
| 2 | `Nexus_Brain/wiki/fix_links.py` | 12 | `/root/v/wiki/concepts` | `_WIKI_ROOT = Path(__file__).resolve().parent` → `concepts` | `exists=True` · `1613 ملف Concept_*.md` |
| 3 | `Nexus_Brain/wiki/fix_links.py` | 13 | `/root/v/wiki/link_repair_report.md` | `_WIKI_ROOT / "link_repair_report.md"` | `exists=True` (التقرير موجود فعلاً في `Nexus_Brain/wiki/`) |

كلٌّthem يحمل تعليق التتبع المطلوب:

```python
# v3-fix 2026-10-01: مسار ميت /root/r/nexus_enrichment/state/apply_wiki/mirror → .nexus_work/apply/mirror
# v3-fix 2026-10-01: مسار ميت /root/v/wiki → Nexus_Brain/wiki (داخل الحزمة)
```

**قرار تصميمي:** استُبدلت المسارات المطلقة بـ `Path(__file__).resolve().parent`
بدل تثبيت `$PKG` المطلق، حتى يبقى السكربت صحيحاً عند نقل الحزمة.

### 2.2 التحقق

```bash
python3 -m py_compile $PKG/.nexus_work/apply/merge_tables.py   # → OK
python3 -m py_compile $PKG/Nexus_Brain/wiki/fix_links.py       # → OK
# فحص المسارات المتحلّلة دون تشغيل حلقة الكتابة (merge_tables.py يُعيد كتابة الـmirror):
MIRROR_DIR = …/.nexus_work/apply/mirror   exists = True   files = 23
WIKI_DIR   = …/Nexus_Brain/wiki/concepts  exists = True   Concept_*.md = 1613
```

⚠️ **لم يُشغَّل `merge_tables.py` فعلياً** لأنه يُعيد كتابة ملفات الـmirror
(حلقة `open(p,'w')`) — تشغيله تدمير للبيانات. فُحص مساره فقط.

### 2.3 موت `/root/v` — مؤكد

```bash
ls -d /root/v/wiki/concepts   # → No such file or directory
ls -d /root/v                # → المجلد موجود لكن فارغ من wiki
```

### 2.4 مسارات ميتة **خارج** النطاق المكلَّف — لم تُعدَّل، موثّقة هنا

| الملف | العدد | الحكم |
|---|---|---|
| `WIKI/01_ACTIVE_WIKI/.nexus_work/backup/pre_unification/wiki_full/fix_links.py:12-13` | 2 | **أُبقي كما هو عمداً** — لقطة أرشيفية (`git log`: `fa4ab0a أرشيف Nexus Brain الكامل`). تعديلها يفسد أمانة اللقطة، ولا يشغّلها شيء. → قرار للمالك |
| `WIKI/02_ENRICHMENT_PROJECT/state/wiki_routing/build_manifest.py:14` | 1 | خارج v1 (مشروع 02)، ومعه تبعيات خارجية `/sdcard/…` غير موجودة على هذا المضيف |
| `AGENT_WORK/05_ANCESTOR_PROJECTS/cognee_nexus/**` | 37 | مشروع **أسلاف** مجمَّد؛ `PROJECT_ROOT = "/root/cognee_nexus"` هو جذره الأصلي. تعديله يكتب فوق السجل التاريخي |

### 2.5 اكتشاف أكبر: **27 سطراً تشير إلى `/sdcard/Nexus_Brain/` وهي ميتة على هذا المضيف**

```bash
ls -d /sdcard/Nexus_Brain/nexus_vault /sdcard/Nexus_Brain/rag
# → No such file or directory  (للوجينين!)
```

| الملف | السطور |
|---|---|
| `nexus_vault/build_remaining_masters.py` | 12, 13 |
| `nexus_vault/workflow_automation.py` | 30, 31, 32, 33 (+ 434, 437, 445 توثيق) |
| `rag/add_links.py` | 12, 13 |
| `rag/build_index.py` | 5, 16, 17 |
| `rag/query.py` | 23, 24, 25 |
| `rag/search.py` | 5, 37, 154 |
| `.nexus_work/audit_sources.py` | 13, 14 |
| `.nexus_work/audit_entities_tools.py` | 40, 41 |
| `.nexus_work/apply/sync_masters.py` | 25 |

**ولم تُعدَّل** لأنها خارج قائمة `grep` المكلَّفة في التوجيه، ولأن `/sdcard`
هو موثَّق في `CLAUDE.md` كـ«مصدر الحقيقة» على جهاز حقيقي. **لكنها ميتة هنا.**

**البدائل داخل الحزمة موجودة ومُقاسة:**

| الميت `/sdcard/Nexus_Brain/…` | موجود فعلاً داخل الحزمة |
|---|---|
| `rag/index.json.gz` | `$PKG/rag/index.json.gz` ✓ |
| `rag/query.py` · `rag/build_index.py` | `$PKG/rag/query.py` · `$PKG/rag/build_index.py` ✓ |
| `nexus_vault/planner.py` | `$PKG/nexus_vault/planner.py` ✓ |
| `Nexus_Brain/wiki/concepts` | `$PKG/Nexus_Brain/wiki/concepts` ✓ (1613) |

→ **مهمة مقترحة لبوابة تالية** (تحتاج إذن، لأنها تلمس `CLAUDE.md` نفسه).

---

## 3) الـ16 ماستر بلا mirror

```bash
PKG=…/WIKI/01_ACTIVE_WIKI; V=$PKG/nexus_vault; W=$PKG/.nexus_work
comm -23 <(find $V -name 'Master_*.md' -not -path '*_archive*' -printf '%f\n'|sed 's/\.md$//'|sort -u) \
         <(ls -1 $W/apply/mirror|sed 's/\.md$//'|sort)
```

**الحساب:** 39 ماستر نشط − 23 mirror = **16** ✓

| # | الماستر الناقص | المجلد النشط |
|---|---|---|
| 1 | `Master_Agency_Operations` | `13_agency` |
| 2 | `Master_Brand_Identity_System` | `09_personal_branding` |
| 3 | `Master_Business_Models` | `14_business_models` |
| 4 | `Master_Digital_Products_Coaching` | `14_business_models` |
| 5 | `Master_Foundation_Business_Strategy` | `24_foundation_business` |
| 6 | `Master_Lead_Qualification` | `01_outreach` |
| 7 | `Master_Niche_And_Positioning` | `17_niche` |
| 8 | `Master_Personal_Brand_System` | `09_personal_branding` |
| 9 | `Master_Productivity_Deep_Work_Systems` | `11_mindset` |
| 10 | `Master_Scripting_Frameworks` | `06_copywriting_scripts` |
| 11 | `Master_Storytelling_Complete` | `07_storytelling` |
| 12 | `Master_VSL_System` | `19_youtube` |
| 13 | `Master_Video_Production` | `05_content_production` |
| 14 | `Master_Visual_Hook_Design` | `08_hooks_attention` |
| 15 | `Master_Visual_Identity_Design` | `23_design_visual` |
| 16 | `Master_YouTube_Strategy` | `19_youtube` |

⚠️ **لم يُنشأ أي mirror في هذه المهمة** — موثَّق للبوابة التالية.
⚠️ تصحيح على صيغة التوجيه: `sort -uniq` **خاطئ** (`-q` ليست خياراً لـ`sort` —
الأمر يفشل ويطبع `sort: invalid option -- 'q'` ويعطي `0` وهمياً).
الصيغة الصحيحة `sort -u`. بـ `-u` فقط يخرج العدد الحقيقي **16**.

---

## 4) التكرار الصامت — جدول TOP 10 بأرقام حقيقية

**تعريف النسبة:** `أسطر مكررة بايت-ببايت ÷ إجمالي الأسطر غير الفارغة × 100`
حيث *سطر مكرر* = سطر غير فارغ نصّه الكامل يتكرر أكثر من مرة **داخل الملف نفسه**.
**`§` مكرر** = تسمية `§` نفسها (نصها بعد العلامة) تتكرر أكثر من مرة.
**العيّنة: 39 ماستراً نشطاً** (مستثنى `_archive`).

| # | الملف | نسبة الأسطر المكررة | أسطر مكررة/إجمالي | `§` مكرر/`§` الإجمالي |
|---|---|---|---|---|
| 1 | `Master_Brand_Identity_System.md` | **90.93%** | 491/540 | 4/41 |
| 2 | `Master_Personal_Brand_System.md` | 30.06% | 398/1324 | **120/263** |
| 3 | `Master_Video_Production.md` | 20.98% | 382/1821 | 2/171 |
| 4 | `Master_Lead_Qualification.md` | 18.15% | 297/1636 | 0/84 |
| 5 | `Master_Foundation_Business_Strategy.md` | 17.76% | **1348/7592** | **132/647** |
| 6 | `Master_Marketing_Strategy.md` | 14.98% | 220/1469 | 14/261 |
| 7 | `Master_VSL_System.md` | 14.16% | 222/1568 | 0/94 |
| 8 | `Master_Entrepreneurship_Mindset.md` | 13.82% | 167/1208 | 0/100 |
| 9 | `Master_Systems_And_Workflow.md` | 13.74% | 333/2424 | 0/90 |
| 10 | `Master_Niche_And_Positioning.md` | 12.02% | 217/1806 | 0/130 |

### أسوأ 5 بالتفصيل

1. **`Master_Brand_Identity_System.md` — 90.93% (491/540).** ملاحظة حرجة:
   الرقم وحده لا دليل على «تكرار» — نسبة 91% تعني غالباً **بنية مكررة متكررة
   آلياً** (قوالب متطابقة) لا نصاً مكرراً. **هذا الأقرب لملف مولَّد/حلقة.**
   يجب فتحه وفحصه يدوياً قبل أي حكم.
2. **`Master_Personal_Brand_System.md` — 30.06% (398/1324)** مع **120 `§` مكرراً
   من 263** (أعلى نسبة تكرار أقسام في v1 = 45.6%). تكرار الأقسام بنيوي لا سطري.
3. **`Master_Video_Production.md` — 20.98% (382/1821)** — تكرار سطري ثقيل
   لكن الأقسام سليمة (`§` مكرر = 2 فقط). غالباً قوائم أمثلة/تنسيق متكرر.
4. **`Master_Lead_Qualification.md` — 18.15% (297/1636)** — `§` مكرر = 0،
   أي التكرار في المتن لا في الهيكل. أسهل ملف لتنظيف آلي.
5. **`Master_Foundation_Business_Strategy.md` — 17.76% (1348/7592)** مع
   **132 `§` مكرراً من 647** — **أكبر حجم تكرار مطلق في v1** (1,348 سطر).
   ليس الأسوأ نسبةً لكنه **الأثقل حجماً**، وهوリスク الأداء/الفهرسة الأكبر.

> الأرقام خارج TOP 10 موثّقة في سكربت القياس (`/tmp/opencode/dup_metrics.py`)،
> وأدنى قيمة في v1 = `Master_Visual_Hook_Design.md` عند 3.89%.

---

## 5) البنود الأربعة غير المُتحقَّق منها في `FIX_LOG_01.md` §3 — **قِياس كامل**

مصدر الأرقام: `/root/r/NB2/`. كل قيمة مُقاسة، لا مخمَّنة.

### 5.1 `26,828 مصطلح فريد` — ❌ **لا يُطابق؛ القيمة المقيسة 26,864**

```python
# اشتقاق التفرّد من canon_index.jsonl (27,009 سجل)
records            = 27009
unique term        = 26864     ← الرقم المقيس الحقيقي
dup term rows      =  145
unique term (norm) = 26851     ← بعد strip()+lower() على التسمية
```

| القراءة | القيمة | الفارق عن 26,828 |
|---|---|---|
| `unique term` (بايت-ببايت) | **26,864** | **+36** |
| `unique term` (مطبَّع) | 26,851 | +23 |
| سجلات `canon_index.jsonl` | 27,009 | +181 |

**الحكم:** المقياس **مُعرَّف الآن** (تفرّد حقل `term` في `canon_index.jsonl`)
وهو ما كان ناقصاً في `FIX_LOG_01` («لا يعيد `count.py` قياس التفرّد»).
لكن **لا يقرأ 26,828 تحت أي تطبيع مقيس** → الرقم في `CHECKPOINT.md:9,36`
**خاطئ ويجب تصحيحه إلى 26,864** (أو 26,851 إن كان التطبيع مطلوباً — قرار للمالك).

### 5.2 `215 بنك / 27,440 مصطلح خام / 198 تقرير وكيل` — 2 من 3 **مؤكَّدان بالضبط**، والثالث **مُعرَّف بفارق +3**

`LOG.md:79` يفسّر بنفسه: «27,440 مصطلح (**بعدّ النوع**)» — أي أن المقياس
هو **أسطر `النوع:`** لا عدد عناوين `##`.

| البند | المُعلن | **المقيس** | الحكم |
|---|---|---|---|
| `215 بنك` | 215 | **215** ملف `.md` في `01_TERMS/*.md` | ✅ **مؤكَّد** |
| `215 بنك` (جانب الفهرس) | — | **215** بنك فريد في حقل `bank` من `canon_index.jsonl` | ✅ **مؤكَّد مرتين** |
| `198 تقرير وكيل` | 198 | **198** ملف `agent_*.md` في `01_TERMS/_WAVES/` | ✅ **مؤكَّد** |
| `27,440 مصطلح خام` | 27,440 | **27,443** سطر `النوع:` عبر الـ215 بنك | ❌ **فارق +3** |

> ملاحظة على العدّ: `grep -c 'النوع'` يعطي **27,594** لأن 151 سطراً تذكر
> «النوع» في متن/سياق بلا `:`. المقياس الصحيح يتطلّب النمط `النوع[:：]`
> ← **27,443**.

**جدول المرشحين المُقاس كلهم** (لا تخمين — قائمة كاملة):

| المقياس | القيمة |
|---|---|
| `##` headings في الـ215 بنك | 27,321 |
| `##` فريد (بايت-ببايت) | 27,148 |
| `##` فريد (مطبَّع) | 27,134 |
| سجلات `canon_index.jsonl` | 27,009 |
| **(فريد) أزواج `(term,type)`** | **26,891** |
| **أسطر `النوع:` ← الأقرب** | **27,443** |
| `###` headings | 538 |

**الحكم:** «لا مقياس مطابق في المستودع» — نص `FIX_LOG_01` §3 **مُتجاوَز**:
المقياس موجود (`النوع:` بعدّ النوع). يبقى تصحيح 27,440 ← **27,443**
(فارق 3؛ على الأرجح 3 مصطلحات أُضيفت للبنوك بعد تسجيل الرقم).
مطلوب من المالك تأكيد دلالة الـ+3 قبل التعديل.

### 5.3 `5,123 مصدر` (Reality 5,126) — ✅ **مُطابَق حسابياً؛ سبب الفارق مُحدَّد**

```python
inventory_full.json['total'] = 5126          # Reality ✓ (كما في FIX_LOG §4)
ext hist = [('txt', 5122), ('md', 3), ('srt', 1)]
non-md (txt + srt) = 5122 + 1 = 5123          # ← يطابق 5,123 بالضبط
```

**الملفات الـ3 المستثناة (كلها `kind = system_md` في `brain_root`):**

```
01-setup-commands.md   system_md   brain_root
02-master-prompt.md    system_md   brain_root
service.md             system_md   brain_root
```

**الحكم:** الفارق **3** مُفسَّر تفسيراً كاملاً، **وليس** بـ `duplicates/`+`processed/`
كما افترض `FIX_LOG_01` §3:

```bash
find /root/r/NB2 -type d \( -name duplicates -o -name processed \)   # → لا شيء
```

الملفات الـ3 مستندات نظام لا مصادر. إذن **`5,123` = عدد المصادر غير-`.md`،
وهو رقم صحيح**، والجرد `5,126` هو الشامل. **الاثنان صحيحان، لا تعارض بينهما**
بعد هذا التفسير. (بقيَ تأكيد دلالي من المالك: هل «5,123/5,123 ملف» تعني
تغطية W1-W10 بالامتداد، أم التغطية بالملفات المُستثناة صراحةً؟)

### 5.4 `272 صفاً` — ✅ **مُفسَّر: عدد أسطر `01_INVENTORY/BRAIN_INVENTORY_FULL.md`**

```bash
wc -l 01_INVENTORY/BRAIN_INVENTORY_FULL.md   # → 272   ✓
grep -c '^|' 01_INVENTORY/BRAIN_INVENTORY_FULL.md   # → 206  (صفوف جدول فقط)
wc -l  01_INVENTORY/FULL_FILE_INDEX.md        # → 5831  (5,406 سطر جدول)
wc -l  01_INVENTORY/BRAIN_INVENTORY.md        # → 41    (27 سطر جدول)
```

**الحكم:** «272 صفاً» = **272 سطر** في `BRAIN_INVENTORY_FULL.md`، وهو الملف
الوحيد في `01_INVENTORY/` الذي يعطي هذا الرقم بالضبط. ملاحظة: `README.md:10`
يسمّيه «صفاً» بينما هو في الأصل **أسطر** (206 منها صفوف جدول) — **سوء تسمية
دلالي، لا خطأ رقمي**. الرقم صحيح، والوصف يحتاج ضبطاً إلى «سطراً».
(ملاحظة: `FULL_FILE_INDEX.md` فيه **5,831** سطراً لا 5,406 — رقم `FIX_LOG_01`
§3 نقل جدول الصفوف لا الأسطر.)

---

## 6) ملخّص حالة البند (§3 من FIX_LOG_01)

| البند | قبل | بعد القياس |
|---|---|---|
| `26,828 مصطلح فريد` | غير مُتحقَّق | ❌ **مُقاس 26,864** — خاطئ، يحتاج تصحيح |
| `215 بنك` | غير مُتحقَّق | ✅ **مؤكَّد** (ملفات + حقول فهرس) |
| `27,440 مصطلح خام` | غير مُتحقَّق | ❌ **مُقاس 27,443** (فارق +3) |
| `198 تقرير وكيل` | غير مُتحقَّق | ✅ **مؤكَّد** |
| `5,123 ملف مصدر` | قرار بشري | ✅ **مُطابَق** (غير-`.md`)، والسبب مُحدَّد |
| `272 صفًا` | بلا معنى | ✅ **مُفسَّر** (أسطر `BRAIN_INVENTORY_FULL.md`) |

---

## 7) ما لم يُنفَّذ عمداً (للبوابة التالية)

- **لا حذف** لأي ملف (بما فيه الملفان صفحريبا الحجم في §1.2).
- **لا نقل ولا أرشفة** — التوجيه نصّ على تأجيلها.
- **لم يُنشأ أي mirror** للـ16 في §3.
- **لم تُعدَّل** المسارات خارج v1 (§2.4) ولا الـ27 سطراً المتجهة إلى
  `/sdcard` (§2.5) — خارج قائمة `grep` المكلَّفة، وتحتاج إذناً منفصلاً.
- **لم يُشغَّل** `merge_tables.py` (يكتب على الـmirror).