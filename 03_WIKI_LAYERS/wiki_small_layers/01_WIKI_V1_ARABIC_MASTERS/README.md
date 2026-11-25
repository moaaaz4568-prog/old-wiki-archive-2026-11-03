# 01 — WIKI V1 · الماسترات العربية (39 ماستر + 1,613 مفهوم)

> **الحالة: قراءة فقط (read-only).** الكتابة الممنوعة هنا — كل عمل جديد في
> [`03_WIKI_V3_STRUCTURED`](../03_WIKI_V3_STRUCTURED/README.md).
> **مصدر الأرقام:** [`/root/r/V3_SYS/COUNTS.json`](file:///root/r/V3_SYS/COUNTS.json)
> · **خريطة العيوب:** [`/root/r/V3/DEFECTS_SUMMARY.md`](file:///root/r/V3/DEFECTS_SUMMARY.md)
> · **تقرير الفجوات الكامل:** [`/root/r/V3/V1_GAPS.md`](file:///root/r/V3/V1_GAPS.md)

## 1) ما هي · تاريخها · من بناها

| | |
|---|---|
| **الاسم** | الويكي الأولى — «الماسترات العربية» |
| **المصدر (الأصل، غير منسوخ)** | `/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/` |
| **تاريخ البناء** | 2025-08 أقدم ملف · آخر نشاط 2026-09-23 (\ar archive) |
| **الباني** | جيل Nexus Brain المبكر (جلسات المحادثة المحلية `chats/`)، ثم جيلُ الوكلاء اللاحق في `.nexus_work/` |
| **وحدة القياس** | الملف `Master_*.md` = فصل عربي منظَّم في 24 قطاعاً |
| **المستودع** | Git داخل `NEXUS_GITHUB_PACKAGE` (فرع العمل `v3-fix`) |

## 2) الأرقام الحقيقية

| المقياس | القيمة | ملاحظة |
|---|---:|---|
| ملفات (كل الأنواع) | **10,626** | قياس حيّ 2026-10-02 |
| ملفات `.md` | **5,451** | مطابق تماماً لـ`COUNTS.md` |
| بايت | **124,217,084** | `COUNTS.md` لقطة: 124,207,526 (+9,558) |
| مجلدات | **228** | |
| **ماستر حيّ** | **39** | `nexus_vault/*/Master_*.md` بلا `_archive` |
| **ماستر مؤرشف** | **31** | `_archive/superseded_masters/` ⇒ **70 تاريخياً** |
| **مفهوم** | **1,613** | `Nexus_Brain/wiki/concepts/Concept_*.md` |
| ذرّة | **0** | لا مفهوم ذرّي في v1 |

## 3) الأقسام · أين تجد ماذا

المسارات الفعلية تحت **`/root/r/WIKI_HUB/01_WIKI_V1_ARABIC_MASTERS/`** (NODE فقط
⇐ [`_FS_CAPABILITY_NOTE.md`](../_FS_CAPABILITY_NOTE.md)):

| القسم | ما فيه | ملفات |
|---|---|---:|
| `nexus_vault` | **39 ماستراً + 31 مؤرشفاً + `planner.py`** | 117 |
| `wiki` | **1,613 `Concept_*.md` + `fix_links.py`** | 2,333 |
| `brain` | مخرجات التفريغ (نص/فيديو/صوت) | 5,126 |
| `Nexus_Brain` | `0_System` · `sources` · `entities` · `tools` · `checkpoints` | 2,339 |
| `WORK_nexus_work` | 2,412 تقرير وكيل · 215 بنك · `apply/mirror` (23) | 2,731 |
| `rag` | `index.json.gz` (3.2MB) · `query.py` · `build_index.py` | 5 |
| `chats` | سجلّات المحادثات الأصلية | 39 |
| `Phase2_DeepDive` | تنويعات Phase 2 | 254 |
| `concepts` · `keywords` | بطاقات على جذر `01_ACTIVE_WIKI` | 4 · 3 |
| `_SOURCE_ROOT_README.md` | فهرس v1 الأصلي (60,973 بايت) — محفوظ بلا تعديل | 1 |

> ⚠️ `wiki` متداخل داخل `Nexus_Brain` — رابطان إلى نفس الب-tree. لا تحسبهما مرتين.

## 4) ما الذي done · وما الذي not

**done ✅** — 39 ماستر عربي منظَّم في 24 قطاعاً · 1,613 مفهوم بمعرّف `C_*` ·
`MASTER_GRAPH.json` يربط الماسترات · `merge_tables.py` يبني جداول §18 · صفر ملف `.md`
فارغ/ميت (مُقاس: `find -name '*.md' -size 0` ⇒ **0**) · 3 مسارات ميتة أُصلحت في 2026-10-01
(`merge_tables.py:11`، `fix_links.py:12-13`، commit `6f1836b` محلياً بلا push).

**not ❌** — **16 ماستراً بلا mirror** (39 − 23، والقوائم في `V1_GAPS.md §3`) ·
**27 سطراً** في `rag/*.py` و`nexus_vault/*.py` تشير إلى `/sdcard/Nexus_Brain/` وهي
**ميتة على هذا المضيف** (البدائل كلها داخل الحزمة) · لا `sources`/`entities`/`tools`
على مستوى جذر الويكي · لا مخطط (§7) عام لكل ملف.

## 5) أفضل 3 أخطاء موثّقة (بأرقام)

1. **تكرار صامت حتى 90.93%** — `Master_Brand_Identity_System.md`: **491/540** سطراً
   مكرراً بايت-ببايت. يليه `Master_Personal_Brand_System.md` **30.06%** (398/1324)
   و`Master_Video_Production.md` **20.98%** (382/1821). الرقم 90.93% غالباً **بنية
   مولَّدة آلياً** لا نص مكرر — يجب فتحه يدوياً قبل أي حكم.
2. **16 ماستراً بلا mirror** — 39 − 23 = **16**؛ أكبرها ثقلاً
   `Master_Foundation_Business_Strategy.md` بـ**1,348** سطر مكرر من 7,592 (17.76%)
   و**132 `§` مكرراً من 647** = أكبر تكرار مطلق في v1.
3. **27 مساراً ميتاً إلى `/sdcard/Nexus_Brain/`** — موزّعة على 9 ملفات
   (`rag/query.py:23-25` · `rag/search.py:5,37,154` · `nexus_vault/workflow_automation.py:30-33` …).
   `ls -d /sdcard/Nexus_Brain/nexus_vault` ⇒ **No such file or directory**.

## 6) ماذا نأخذ منها للـv3 (3 نقاط)

1. **تقسيم 24 قطاعاً مستقراً** (`01_outreach` … `24_foundation_business`) — أُعيد
   اعتمادها حرفياً في v2 وv3 ⇒ لا إعادة تسمية ولا إعادة تخطيط مطلوبة.
2. **`MASTER_GRAPH.json` + جدول §18 كمخطط تغطية** — فكرة «كل ماستر يسرد مفاهيمه»
   نجحت؛ v3 رفعتها إلى بوابة (`GATES_11.md`) فصارت **قابلة للفحص آلياً**
   بدل الاعتماد على الذاكرة.
3. **نموذج «الأداة في مكانها»** — `planner.py` بجوار الماسترات و`fix_links.py` بجوار
   المفاهيم، ومسارات نسبية `Path(__file__).parent` بدل مطلقة ⇒ نفس النمط في
   `V3/11_INDEX/tools/`.

## 7) ماذا نتجنّب منها (3 نقاط)

1. **التكرار غير المقيس** — 10 ماسترات تتجاوز 12% تكرار؛ فحوص v1 الآلية كانت
   تقيس «الفراغ» لا «العلم»، فمرّ التكرار. ⇒ **كل قالب في v3 له حدّ فناء صريح**
   (`ANTI_DEAD_FORMULA.md`).
2. **مسارات مطلقة ميتة** — 27 سطراً متّسقاً في الموت؛ عدّاد `COUNTS.json` لا يمسك
   الخطأ ⇒ في v3 كل مسار **نسبي** ومُتحقَّق منه بـ`test -e`.
3. **اعتماد `.nexus_work` كمصدر حقيقة** — 2,731 ملفاً عمل داخل جذر المحتوى؛
   v3 يحتفظ بـ`03_WORK_BUNDLES/` **خارج** `01_ATOMS`/`02_CONCEPTS`.

## 8) كيف تقرأها

```bash
H=/root/r/WIKI_HUB/01_WIKI_V1_ARABIC_MASTERS

# 39 ماستراً بالترتيب
ls -1 $H/nexus_vault/*/Master_*.md | sed 's|.*/||'

# بحث نصي في كل المحتوى (1,613 مفهوم + 39 ماستر)
grep -rlE "مغناطيس|جذب" $H/wiki/concepts $H/nexus_vault | head

# أداة الاستعلام الجاهزة (تحتاج fixing لمسارها — انظر خطأ 5.3)
python3 $H/rag/query.py "مغناطيس الجذب"

# قياس التكرار (نفس تعريف V1_GAPS §4: سطر غير فارغ يتكرر داخل الملف)
awk 'NF{gsub(/^ +| +$/,"");c[$0]++} END{n=0;for(k in c)if(c[k]>1)n+=c[k]-1;print n}' \
  $H/nexus_vault/09_personal_branding/Master_Brand_Identity_System.md
```

## 9) حالة التطابق مع `/root/r/V3/DEFECTS_SUMMARY.md`

`DEFECTS_SUMMARY.md` يقيس **NB2 (v2) لا v1** (جدول «القياس الحقيقي» = 1,836 مفهوم
من `NB2/02_CONCEPTS`). عيوب v1 ليست فيه ⇒ تقريرها الوحيد هو
[`V1_GAPS.md`](file:///root/r/V3/V1_GAPS.md) + `V3_SYS/AUDIT_V1.md`.