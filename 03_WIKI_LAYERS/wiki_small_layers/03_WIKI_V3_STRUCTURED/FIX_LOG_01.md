# FIX_LOG_01 — تصحيح الأرقام الكاذبة في NB2

**التاريخ:** 2026-10-01
**الفرع:** `v3` (HEAD قبل التصحيح `30560e36`)
**السياسة:** صفر حذف — كل تصحيح سطر `> ⚠️ صحّح 2026-10-01: …` **تحت** الرقم القديم، والسطر القديم باقٍ.
**النطاق:** 3 ملفات فقط — `00_SYSTEMS/CHECKPOINT.md` · `02_CONCEPTS/_INDEX.md` · `README.md`
**لم يُلمس:** YAML الماسترات الخمسة (`03_MASTERS/*/Master_*.md`) — تحقّق بصري فقط.

---

## 1) جدول التصحيحات

| الملف | السطر (قبل) | قبل | بعد | أمر الدليل |
|---|---|---|---|---|
| `00_SYSTEMS/CHECKPOINT.md` | 4 | `166/27,620 صفحة معمّقة` | **166/29,583 ملف .md** (و29,585 ملفًا بكل الامتدادات = 29,583 .md + 2 .log في `_REPORTS/`) | `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f \| wc -l` → 29583 · `find /root/r/NB2/02_CONCEPTS -type f \| wc -l` → 29585 · `rg -l deepened /root/r/NB2/02_CONCEPTS/ \| wc -l` → 168 (166 + تقريران) |
| `00_SYSTEMS/CHECKPOINT.md` | 8 | `5,123/5,123 ملف (W1-W10)` | الجرد المعتمد **5,126 ملفًا** (فرق 3 — يُحتمل أنه استثناء مقصود لـ`duplicates/`+`processed/`؛ قرار مطلوب) | `python3 -c "import json;print(json.load(open('/root/r/NB2/01_INVENTORY/inventory_full.json'))['total'])"` → 5126 · `grep -n 'إجمالي الملفات في الشجرة كلها' /root/r/NB2/01_INVENTORY/BRAIN_INVENTORY_FULL.md` → 5,126 |
| `00_SYSTEMS/CHECKPOINT.md` | 8 | `215 بنك · 27,440 مصطلح خام · 198 تقرير وكيل` | **بلا تصحيح — غير مُتحقَّق** (لا مقياس مطابق في المستودع) | `find /root/r/NB2/01_TERMS -type f \| wc -l` → 552 · `wc -l /root/r/NB2/00_SYSTEMS/canon_index.jsonl` → 27009 |
| `00_SYSTEMS/CHECKPOINT.md` | 9 | `27,745 صفحة كانونية (26,828 مصطلح فريد)` | **27,742 ذرّة YAML** في `terms_26k/` + **1,841 ملف .md** خماسي خارجها (1,836 قطاعات + 4 `_REPORTS/` + `_INDEX.md`) = **29,583 ملف .md** | `find /root/r/NB2/02_CONCEPTS/terms_26k -name '*.md' -type f \| wc -l` → 27742 · `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f -not -path '*/terms_26k/*' \| wc -l` → 1841 · `jq -r '.nb2.terms_26k.files, .nb2.quintuple_concepts_excl_terms26k._files_scanned' /root/r/V3_SYS/COUNTS.json` → 27742 · 1841 |
| `00_SYSTEMS/CHECKPOINT.md` | 9 | `26,828 مصطلح فريد` | **بلا تصحيح — غير مُتحقَّق** (`count.py` لا يقيس التفرّد؛ `canon_index.jsonl` = 27,009 سطرًا) | `wc -l /root/r/NB2/00_SYSTEMS/canon_index.jsonl` → 27009 |
| `00_SYSTEMS/CHECKPOINT.md` | 13 | `166/27,620 صفحة` | **166/29,583 ملف .md** | `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f \| wc -l` → 29583 |
| `00_SYSTEMS/CHECKPOINT.md` | 15 | `نظام 03 الماسترز — لم يبدأ` | **النظام مبنيّ وكامل: 5 ماسترات** (01_outreach · 02_sales_calls · 03_offers_pricing · 07_branding · 08_mindset) · **100,103 كلمة** في `Master_*.md` (10 ملفات = 100,956 مع `_index.md`) | `find /root/r/NB2/03_MASTERS -name 'Master_*.md' -type f \| wc -l` → 5 · `find /root/r/NB2/03_MASTERS -name 'Master_*.md' -type f -exec cat {} + \| wc -w` → 100103 · `find /root/r/NB2/03_MASTERS -name '*.md' -type f -exec cat {} + \| wc -w` → 100956 · `jq -r '.nb2.masters_total' /root/r/V3_SYS/COUNTS.json` → 10 |
| `00_SYSTEMS/CHECKPOINT.md` | 17 | `نظام 04 البحث … (لم يُعاد بعد نظام 05)` | **الدعوى غير مدعومة بالتواريخ**: `04_SEARCH/index.json.gz` أحدث من كل ملفات `terms_26k/` (0 ملف أحدث منه) | `find /root/r/NB2/04_SEARCH -type f \| wc -l` → 6 · `find /root/r/NB2/02_CONCEPTS/terms_26k -name '*.md' -newer /root/r/NB2/04_SEARCH/index.json.gz \| wc -l` → 0 |
| `00_SYSTEMS/CHECKPOINT.md` | 31 | `canon_build.py → 02_CONCEPTS/ (27,745 صفحة)` | **29,583 ملف .md** | `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f \| wc -l` → 29583 · `jq -r '.nb2.concepts_md' /root/r/V3_SYS/COUNTS.json` → 29583 |
| `00_SYSTEMS/CHECKPOINT.md` | 36 | `26,828 مصطلح فريد · 27,745 صفحة كانونية` | **27,742 ذرّة + 1,841 خماسي = 29,583 ملف .md** · `27,009 مدخل` مؤكَّد · `5,123 ملف مصدر` يتباين مع 5,126 (بلا تصحيح) | كما في السطرين 8 و9 أعلاه |
| `00_SYSTEMS/CHECKPOINT.md` | 39 | `آخر commit 7e36936` | **HEAD = 30560e36**؛ `7e36936` موجود في التاريخ فقط وليس رأس الفرع | `git -C /root/r/NB2 rev-parse --short HEAD` → 30560e36 · `git -C /root/r/NB2 cat-file -t 7e36936` → commit · `git -C /root/r/NB2 log --oneline -1` |
| `00_SYSTEMS/CHECKPOINT.md` | 39 | `كل شغل الجلسة مدفوع على GitHub` | **مُتحقَّق عبر `main` (= `origin/main` = 30560e36)**؛ `v3` بلا upstream — تصحيح 2026-10-01 محلي بلا push | `git -C /root/r/NB2 branch -vv` → `main 30560e36 [origin/main]` · `v3 30560e36` |
| `02_CONCEPTS/_INDEX.md` | 3 | `29,583 ملفًا` | **صحيح — بلا تغيير** (مُثبت) | `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f \| wc -l` → 29583 |
| `02_CONCEPTS/_INDEX.md` | 7 | `1,836 مفهومًا` (الخماسي) | **صحيح — بلا تغيير**؛ طُلب 1,837 **ورُفض** (1,837 = 1,836 + `_INDEX.md`؛ الفهرس ليس مفهومًا). التفصيل: 1,836 قطاعًا + 4 `_REPORTS/` + `_INDEX.md` = 1,841 .md؛ 1,833 فقط مكتملة الأقسام الخمسة (3 ملفات قطاعات ناقصة `## الآلية`) | `find /root/r/NB2/02_CONCEPTS -mindepth 2 -name '*.md' -type f -not -path '*/_REPORTS/*' -not -path '*/terms_26k/*' \| wc -l` → 1836 · `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f -not -path '*/terms_26k/*' \| wc -l` → 1841 · `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f -not -path '*/terms_26k/*' -not -path '*/_REPORTS/*' \| wc -l` → 1837 · `grep -rL '## الآلية' /root/r/NB2/02_CONCEPTS --include='*.md' \| grep -v terms_26k \| wc -l` → 7 **بعد** تعديل `_INDEX.md` (ذاتي المرجع: هذا السطر يحوي نص القسم) — استُبدل بعدّ البايثون أدناه · `python3 -c "import pathlib;p=pathlib.Path('/root/r/NB2/02_CONCEPTS');fs=[f for f in p.rglob('*.md') if 'terms_26k' not in f.parts and '_REPORTS' not in f.parts and f.name!='_INDEX.md'];print(len(fs),sum(1 for f in fs if '## الآلية' not in f.read_text(encoding='utf-8',errors='replace')))"` → `1836 3` · `jq -r '.nb2.quintuple_concepts_excl_terms26k._files_scanned, .nb2.quintuple_concepts_excl_terms26k.mechanism' /root/r/V3_SYS/COUNTS.json` → 1841 · 1833 |
| `02_CONCEPTS/_INDEX.md` | 7 | (جدول القطاعات) | **صحيح — بلا تغيير**: 22 قطاعًا تجمع 1,836 بالضبط، وكل صف يطابق `count.py` | `jq -r '.nb2.concepts_sectors' /root/r/V3_SYS/COUNTS.json` |
| `02_CONCEPTS/_INDEX.md` | 27 | `27,742 مفهومًا` | **محصور في `terms_26k/` وحده**؛ الكلي: 27,742 ذرّة YAML + 1,836 خماسي = 29,583 ملف .md. طُلب «+1,843 خماسي» **ورُفض** (1,843 = كل الملفات خارج `terms_26k/` = 1,841 .md + 2 .log) | `find /root/r/NB2/02_CONCEPTS/terms_26k -name '*.md' -type f \| wc -l` → 27742 · `find /root/r/NB2/02_CONCEPTS -type f -not -path '*/terms_26k/*' \| wc -l` → 1843 · `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f \| wc -l` → 29583 |
| `02_CONCEPTS/_INDEX.md` | 30 | (جدول قطاعات `terms_26k`) | **صحيح — بلا تغيير**: مجموع 28 قطاعًا = 27,742 | `for d in /root/r/NB2/02_CONCEPTS/terms_26k/*/; do find "$d" -name '*.md' -type f \| wc -l; done \| paste -sd+ \| bc` → 27742 |
| `README.md` | 13 | `04_COUNCIL/    أحكام المجلس + الأرقام المحظورة` | **المجلد غير موجود إطلاقًا**؛ الصحيح `04_SEARCH/` (6 ملفات: `index.json.gz` 14.2MB + `tools/{add_links,build_index,planner,query,search}.py`) | `ls -d /root/r/NB2/04_COUNCIL` → `No such file or directory` · `find /root/r/NB2/04_SEARCH -type f \| wc -l` → 6 |
| `README.md` | 13 | `04_COUNCIL/` | **مرجع مشلّ**: 5 إشارات `04_COUNCIL` معلّقة في 3 من 5 ماسترات — `03_MASTERS/01_outreach/Master_Outreach_Mechanics.md:390,616` · `03_MASTERS/02_sales_calls/Master_Sales_Call_Architecture.md:350` · `03_MASTERS/03_offers_pricing/Master_Offer_Construction_Pricing.md:431,673`. طُلب «27 إشارة» **ورُفض الرقم** | `grep -rn '04_COUNCIL' /root/r/NB2/03_MASTERS/` → 5 مواضع · `grep -rl '04_COUNCIL' /root/r/NB2/03_MASTERS/` → 3 ملفات · `grep -rno '04_COUNCIL' /root/r/NB2/00_CHARTER/ \| wc -l` → 3 · `grep -rno '04_COUNCIL' /root/r/NB2/00_SYSTEMS/MASTER_MAKING_SYSTEM.md \| wc -l` → 1 |
| `README.md` | 5 · 10 | `5,126 ملفًا` · `137 قناة` (10 يوتيوب + 127 إنستجرام) | **صحيح — بلا تغيير** (مُثبت) | `python3 -c "import json;print(json.load(open('/root/r/NB2/01_INVENTORY/inventory_full.json'))['total'])"` → 5126 · `python3 -c "import json;d=json.load(open('/root/r/NB2/01_INVENTORY/channels_full.json'));print({k:len(v) for k,v in d.items()}, sum(len(v) for v in d.values()))"` → `{'youtube': 10, 'instagram': 127} 137` |

---

## 2) الأرقام الموصى بها من التكليف التي رُفضت (أوامر التكليف ليست أرقامًا مختبَرة)

| رقم التكليف | الموقع | الحكم | السبب بدليل |
|---|---|---|---|
| `29,585 ملف .md` في 02_CONCEPTS | تكليف 3 | **رُفض** | 29,585 = **كل الملفات** (29,583 .md + 2 .log في `_REPORTS/`). عدد `.md` = **29,583** — وهو الرقم المكتوب أصلًا في `_INDEX.md:3` (صحيح). الدليل: `find /root/r/NB2/02_CONCEPTS -name '*.md' -type f \| wc -l` → 29583 · `find /root/r/NB2/02_CONCEPTS -type f -not -name '*.md'` → 2 |
| `1,841 مفهوم` كبديل لـ`27,745` | تكليف 3 | **قُبِل كعدد ملفات لا كعدد مفاهيم** | 1,841 = كل `.md` خارج `terms_26k/` (شاملة `_REPORTS/` و`_INDEX.md`)، لا عدد المفاهيم (1,836). الدليل: `find /root/r/NB2/02_CONCEPTS -mindepth 2 -name '*.md' -type f -not -path '*/_REPORTS/*' -not -path '*/terms_26k/*' \| wc -l` → 1836 |
| `1,843 خماسي` | تكليف 4 | **رُفض** | 1,843 = 1,841 `.md` + 2 `.log` = كل الملفات خارج `terms_26k/`، ولا واحد منها «خماسي» بهذا العدّ. الدليل: `find /root/r/NB2/02_CONCEPTS -type f -not -path '*/terms_26k/*' \| wc -l` → 1843 |
| `1,837` (بدل `1,836`) | تكليف 5 | **رُفض** | 1,837 = 1,836 + `_INDEX.md`؛ الـ`_INDEX.md` فهرس لا مفهوم. الدليل: `find /root/r/NB2/02_CONCEPTS -mindepth 2 -name '*.md' -type f -not -path '*/_REPORTS/*' -not -path '*/terms_26k/*' \| wc -l` → 1836 |
| `27 إشارة في الماسترات` | تكليف 6 | **رُفض** | الواقع **5** في `03_MASTERS/`. الدليل: `grep -ro '04_COUNCIL' /root/r/NB2/03_MASTERS/ \| wc -l` → 5 |
| `100,103 كلمة` للماسترات | تكليف 6 | **قُبِل** ✓ | `find /root/r/NB2/03_MASTERS -name 'Master_*.md' -type f -exec cat {} + \| wc -w` → 100103 (و100,956 مع `_index.md`) |
| `5 ماسترات` | تكليف 6 | **قُبِل** ✓ | `find /root/r/NB2/03_MASTERS -name 'Master_*.md' -type f \| wc -l` → 5 |
| `27,742 ذرّة` | تكليف 4 | **قُبِل** ✓ | `find /root/r/NB2/02_CONCEPTS/terms_26k -name '*.md' -type f \| wc -l` → 27742 |

---

## 3) أرقام لم تُصحَّح (مفتوحة — تحتاج قرارًا لا تخمينًا)

| الرقم | الملف:السطر | لماذا تُرك |
|---|---|---|
| `26,828 مصطلح فريد` | `CHECKPOINT.md:9,36` | لا مقياس تفرّد في `count.py`؛ `canon_index.jsonl` = 27,009 مدخلًا ≠ 26,828. يحتاج إعادة اشتقاق التفرّد من الفهرس. |
| `215 بنك` · `27,440 مصطلح خام` · `198 تقرير وكيل` | `CHECKPOINT.md:8` | لا مقياس مطابق في المستودع (`01_TERMS/` = 552 ملفًا فقط). |
| `5,123 ملف مصدر` | `CHECKPOINT.md:8,36` | الجرد المعتمد 5,126؛ فرق 3 قد يكون استثناءً مقصودًا لـ`duplicates/`+`processed/`. قرار بشري مطلوب. |
| `27,463 اقتباس` · `140 مجموعة` · `146 شريحة` | `CHECKPOINT.md:36,30` | غير مُقاسة في هذه المهمة (خارج النطاق المكلَّف). |
| `272 صفًا` | `README.md:10` | لا معنى مُحدد (الفهرس الحرفي `FULL_FILE_INDEX.md` فيه 5,406 سطر جدول؛ 137 قناة لا 272). بلا تصحيح — يحتاج تعريفًا من المالك. الدليل: `grep -c '^|' /root/r/NB2/01_INVENTORY/FULL_FILE_INDEX.md` → 5406 |
| `697 مفهومًا` (التغطية الماسترية) | `02_CONCEPTS/_INDEX.md:27` | **مُتحقَّق ✓ بلا تغيير** — 697 إشارة `Concept_*` فريدة عبر الماسترات الخمسة. الدليل: `rg -o 'Concept_[A-Za-z0-9_]+' /root/r/NB2/03_MASTERS/ \| sed 's/.*://' \| sort -u \| wc -l` → 697 |

---

## 4) الأرقام التي ثبتت صحّتها (بلا سطر تصحيح — توثيق فقط)

- `02_CONCEPTS/_INDEX.md:3` — `29,583 ملفًا` ✓
- `02_CONCEPTS/_INDEX.md:7` — `1,836 مفهومًا` وجدول القطاعات ✓
- `02_CONCEPTS/_INDEX.md:27` — `27,742` في `terms_26k/` ✓ (تحتّ التصحيح: محصور في هذا المجلد)
- `02_CONCEPTS/_INDEX.md:30` — جدول 28 قطاعًا لـ`terms_26k` = 27,742 ✓
- `README.md:5,10` — `5,126 ملفًا` و`137 قناة (10+127)` ✓
- `02_CONCEPTS/_INDEX.md:27` — `697 مفهومًا` التغطية الماسترية ✓ (`rg -o 'Concept_[A-Za-z0-9_]+' 03_MASTERS/ | sort -u | wc -l` → 697)
- `CHECKPOINT.md:4,13` — `166` ملفًا معمّقًا ✓ (168 مطابقة لـ`deepened` − تقريرَي `_REPORTS`)

---

## 5) الأوامر المُنفَّذة للتحقق (كلها محلية، قراءة فقط)

```bash
python3 /root/r/V3_SYS/count.py --root /root/r/NB2          # 155s → /root/r/V3_SYS/COUNTS.json
jq -r '.nb2.terms_26k.files, .nb2.concepts_md, .nb2.concepts_total, .nb2.quintuple_concepts_excl_terms26k._files_scanned, .nb2.quintuple_concepts_excl_terms26k.mechanism, .nb2.masters_total' /root/r/V3_SYS/COUNTS.json
# → 27742 · 29583 · 29585 · 1841 · 1833 · 10
find /root/r/NB2/02_CONCEPTS -name '*.md' -type f | wc -l                      # 29583
find /root/r/NB2/02_CONCEPTS -type f | wc -l                                  # 29585
find /root/r/NB2/02_CONCEPTS/terms_26k -name '*.md' -type f | wc -l           # 27742
find /root/r/NB2/02_CONCEPTS -name '*.md' -type f -not -path '*/terms_26k/*' | wc -l                                  # 1841
find /root/r/NB2/02_CONCEPTS -mindepth 2 -name '*.md' -type f -not -path '*/_REPORTS/*' -not -path '*/terms_26k/*' | wc -l  # 1836
find /root/r/NB2/03_MASTERS -name 'Master_*.md' -type f | wc -l                # 5
find /root/r/NB2/03_MASTERS -name 'Master_*.md' -type f -exec cat {} + | wc -w  # 100103
ls -d /root/r/NB2/04_COUNCIL                                                   # No such file or directory
find /root/r/NB2/04_SEARCH -type f | wc -l                                     # 6
grep -ro '04_COUNCIL' /root/r/NB2/03_MASTERS/ | wc -l                          # 5
```

---

## 6) القواعد المحترمة

- ✅ **صفر حذف** — كل سطر قديم باقٍ؛ التصحيح سطر مضاف تحته.
- ✅ **لم يُلمس** YAML الماسترات الخمسة — `git status` لا يظهر `03_MASTERS/` في قائمة التغييرات.
- ✅ **بلا push / بلا force** — commit محلي على `v3` فقط.
- ✅ **بلا كتابة في `/sdcard`**.
- ✅ **بلا `rm` / `rmdir` / `shred` / `dd`**.
