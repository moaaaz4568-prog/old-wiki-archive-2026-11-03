# NEXUS WIKI — الفهرس الرئيسي

> **مركز معرفة واحد.** كل ويكي، المصادر الخام، الـinbox، والأدوات — في مكان واحد.
> كل قسم يقول **وين الملف الأصلي** — القارئ يبدأ من هنا دائماً.

---

## ⚠️ اقرأ أولاً: symlinks على `/sdcard` مستحيلة

نظام الملفات هنا `fuseblk` (emulated) والـkernel **يرفض** إنشاء الروابط:

```
$ ln -s /tmp /sdcard/nexus_wiki/_probe
ln: failed to create symbolic link: Permission denied   (exit 1)
$ mount --bind /tmp /sdcard/nexus_wiki/x
mount(): Function not implemented                        (exit 32)
```

فالحل المطبَّق **بلا نسخ لـv1/v2** (لا ضياع 70MB، ولا «نقل»):

| المجلد | ما بداخله |
|---|---|
| `/root/r/nexus_wiki_links/` | ✅ **15 symlink حقيقي** بنفس الأسماء المطلوبة + مسارات مطلقة |
| `01_WIKI_V1_ARABIC/*.link.txt` | 📄 مؤشر نصّي: `name:` + `target:` + مسار الـsymlink الحيّ |
| `02_WIKI_V2_TERMS/*.link.txt` | 📄 نفس آلية المؤشر |
| `04_SOURCES_RAW/*.link.txt` | 📄 نفس آلية المؤشر |

فحص الصحة: **15 link · 0 broken · 15/15 تُحلّ.** لم يُحذف أي symlink موجود
(`/root/r/WIKI_HUB/` بـ22 symlink سليمة **باقٍ كما هو**).

---

## ويكي الـ3 — بالأرقام

| # | المجلد | النوع | العدد | الحجم | الجذر الأصلي | الكتابة |
|---|---|---|---|---|---|---|
| 1 | `01_WIKI_V1_ARABIC/` | 5 symlink | 24 مِستر · 42 dir | 70MB | `/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/` | ❌ قراءة فقط |
| 2 | `02_WIKI_V2_TERMS/` | 8 symlink | 552 term · 29,585 concept · 10 مِستر | 90MB | `/root/r/NB2/` | ❌ قراءة فقط |
| 3 | `03_WIKI_V3_NEW/` | **نسخة حقيقية** | 238 ملف | 24MB | `/root/r/V3/` | ✅ **الكتابة هنا** |

### 🚨 ويكي 1 و 2 للقراءة فقط — كل الكتابة في ويكي 3

- **v1 و v2 مؤرشفان.** أي تعديل عليهما يكسر الـprovenance ويخلط الأرقام (29,585 مفهوم في v2 مقابل 96 في v3 — مقاييس مختلفة، لا تخلطهم).
- **v3 هو حيّ**: `01_ATOMS` (30) · `02_CONCEPTS` (96) · `03_MASTERS` · `12_LOGS`.
- للكتابة: افتح `03_WIKI_V3_NEW/` واعمل نسخة جديدة هناك. **لا تكتب فوق v1/v2.**

---

## خريطة «أين أبحث عن ماذا»

| أبحث عن… | أروح لـ |
|---|---|
| مِستر عربي كامل (24 مِستر) | `01_WIKI_V1_ARABIC/nexus_vault/` |
| brain الخام · 5,126 ملف | `04_SOURCES_RAW/brain/` (أو `01_WIKI_V1_ARABIC/Nexus_Brain/brain/`) |
| تعريف مصطلح (552) | `02_WIKI_V2_TERMS/01_TERMS/` |
| مفهوم بالقطاع (29,585) | `02_WIKI_V2_TERMS/02_CONCEPTS/` |
| تصريف · tensions · provenance | `02_WIKI_V2_TERMS/05_TENSIONS/` · `06_GLOSSARY/` · `07_PROVENANCE/` |
| الأنظمة والقواعد | `02_WIKI_V2_TERMS/00_SYSTEMS/` |
| **المفهوم الجديد (حيّ)** | `03_WIKI_V3_NEW/02_CONCEPTS/` |
| **الذرة — أصغر وحدة** | `03_WIKI_V3_NEW/01_ATOMS/` |
| شغل غير مطبّق · 19 حزمة | `05_INBOX/WB_*.txt` |
| الميثاق · الخطة · السجل | `00_PROJECT/` (goals · plan · plan_v2 · worklog · memory) |
| contradictory numbers | `00_PROJECT/INGEST_02_numbers_contradiction.md` |
| العدّ والتدقيق | `06_TOOLS/count.py` · `audit.py` · `COUNTS.json` |
| كورس خام · 323 ملف | `04_SOURCES_RAW/course_tx/` |
| مهملات — TRASH | `02_WIKI_V2_TERMS/TRASH/` |

---

## المصادر الخام

| المصدر | العدد | الحجم | المسار |
|---|---|---|---|
| `brain/` | **5,126 ملف** | 60MB | `/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/brain` |
| `course_tx/` | **323 ملف** | 9.5MB | `/root/r/COURSE_TX/` |

النسخة على `/sdcard/Nexus_Brain/Nexus_Brain/` هي **mirror** لفيكي 1
(مرتبط كـ`01_WIKI_V1_ARABIC/mirror`).

---

## قاعدة صفر حذف

1. **لا `rm` ولا `rmdir` ولا `shred` ولا `dd` ولا `trash`** — إطلاقاً، بلا استثناء.
2. التصحيح = **إضافة** (`>` ملف جديد، `mv` لـ`suffix`) لا حذف.
3. symlink مكسور ⇒ **أصلحه بـ`ln -sfn` بالهدف الصحيح**، لا تحذفه.
4. أي نقلة تُنسخ، لا تُحرَّك. الأصل يبقى في مكانه.

---

## أوامر التحقق

```bash
# 1) البنية
ls -la /sdcard/nexus_wiki/

# 2) الـsymlinks الحيّة (15 · 0 broken)
find /root/r/nexus_wiki_links -type l | wc -l
find /root/r/nexus_wiki_links -xtype l | wc -l          # يجب 0
find /root/r/nexus_wiki_links -type l -exec test -e {} \; -print | wc -l

# 3) لا symlinks مكسورة داخل /sdcard (0 — الـkernel لا يسمح بها)
find /sdcard/nexus_wiki -xtype l | wc -l                 # يجب 0

# 4) سلامة النسخ الحقيقية
ls -1 /sdcard/nexus_wiki/05_INBOX/WB_*.txt | wc -l      # يجب 19
ls -1 /sdcard/nexus_wiki/06_TOOLS/ | wc -l               # يجب 3
find /sdcard/nexus_wiki/03_WIKI_V3_NEW -type f | wc -l   # يجب 238

# 5) المساحة
du -sh /sdcard/nexus_wiki
df -h /mnt/sdcard | tail -1
```