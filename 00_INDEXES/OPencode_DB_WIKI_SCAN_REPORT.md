# تقرير فحص قاعدة بيانات OpenCode — بحث عن محادثات الويكي

**التاريخ:** 2026-11-03
**الوضع:** قراءة فقط (`mode=ro`) — لم يُنسخ أي ملف `.db`، ولم يُحذف شيء.

---

## 1. المصادر والفحص الأولي

| المصدر | الحجم | الحالة |
|---|---|---|
| `/root/.local/share/opencode/opencode.db` | 959,197,184 بايت (914.8 MiB) | فُتح read-only بنجاح |
| `/root/r/BACKUP_OMINIRUSH_CHAT/opencode.db` | 109,793,280 بايت (104.7 MiB) | فُتح read-only بنجاح |
| `~/.local/share/opencode/storage/` | 6 ملفات فقط | — |
| `session_diff/*.json` | 5 ملفات، كلها 2 بايت | **0 مطابقة** لـ `wiki\|ويكي` |

`sqlite3` المتاح: **3.46.1** (2024-08-13).

> **تحذير أمني/سلامة:** القاعدة **نشطة أثناء الفحص** — تغيّر عدد صفوف `part` بين الاستعلامات
> (115,586 ← 115,801 خلال دقائق). أي رقم أدناه لقطة زمنية وليس حصراً نهائياً.

---

## 2. أسماء الجداول (من `.tables`)

```
account               message              session_context_epoch
account_state         migration            session_input
control_account       part                 session_message
credential            permission           session_share
data_migration        project              todo
event                 project_directory    workspace
event_sequence        session
```

**20 جدولاً.** الجداول النصية القابلة للبحث: `session`, `message`, `part`, `session_message`, `session_input`, `todo`, `event`, `project`, `workspace`.

---

## 3. عدد المطابقات لكل جدول

### 3.1 القاعدة الرئيسية (`opencode.db` — 959 MB)

| الجدول | العمود المفحوص | إجمالي الصفوف | المطابقات (`wiki` / `ويكي` / `wikillm`) |
|---|---|---|---|
| `session` | `title, slug, directory, path, metadata` | 1,537 | **44** |
| `part` | `data` | 115,801 | **10,993** |
| `message` | `data` | 30,020 | **2** |
| `session_message` | `data` | 669 | **0** |
| `session_input` | `prompt` | 0 | **0** |
| `todo` | `content` | 212 | **7** |
| `event` | `data` | 217,903 | **17,456** |
| `project` | `name, worktree` | 1 | **0** |
| `workspace` | — | 0 | **0** |
| `session_context_epoch` | — | 0 | **0** |

**تفصيل توزيع المطابقة في `session`:** 25 عنواناً بالإنجليزية (`wiki`) + 19 عربياً (`ويكي`).

### 3.2 النسخة الاحتياطية (`BACKUP_OMINIRUSH_CHAT/opencode.db` — 110 MB)

| الجدول | إجمالي الصفوف | المطابقات |
|---|---|---|
| `session` | 40 | **7** |
| `part` | 5,851 | **1,767** |
| `message` | 1,093 | **0** |
| `todo` | 28 | **0** |
| `event` | 17,352 | **4,224** |
| `session_message` / `session_input` | 0 | **0** |

### 3.3 `storage/session_diff/`

```
grep -licE "wiki|ويكي" .../session_diff/*.json | grep -v ':0' | wc -l  →  0
```
الملفات الخمسة كلها `2 bytes` (محتوى `{}` تقريباً) — **لا قيمة**.

---

## 4. جدول المحادثات المطابقة (44 محادثة — القاعدة الرئيسية)

المرتبة تنازلياً حجم `part` (تقدير = بايت النص الخام، غير مضغوط).

| # | session id | العنوان | msgs | parts | حجم parts (KB) | wiki_parts | الإنشاء |
|---|---|---|---|---|---|---|---|
| 1 | `ses_e6b7fdbd3ffe0ShhsiJlQ7ZVQj` | wiki (fork #2) | 430 | 1126 | 1466 | 260 | 2026-11-01 |
| 2 | `ses_f0c292dd0ffe766mk6TLpesYSK` | متابعة مشروع متعدد المراحل عبر جيت هب والويكي | 195 | 633 | 1326 | 138 | 2026-09-30 |
| 3 | `ses_e94afaf0cffeGjWc0HZdN6KpKl` | wiki | 346 | 972 | 1264 | 211 | 2026-10-24 |
| 4 | `ses_e8f8875eaffeum0nKPHczAIPmw` | wiki (fork #1) | 334 | 903 | 1057 | 194 | 2026-10-25 |
| 5 | `ses_f01d297d0ffedTfe82N4s1pEs2` | Ingest wiki.md into NEXUS_PROJECT (@Worker) | 42 | 168 | 1050 | 42 | 2026-10-02 |
| 6 | `ses_e8188680bffetLfajw6QE7g5PD` | بناء موجة 1 ويكي (@general) | 88 | 312 | 855 | 113 | 2026-10-27 |
| 7 | `ses_e8f88d729ffepfUUbb7uK8CYYm` | wiki (fork #1) | 244 | 675 | 784 | 128 | 2026-10-25 |
| 8 | `ses_e8f888e53ffep0X0oR05BsSO1B` | wiki (fork #1) | 244 | 675 | 784 | 128 | 2026-10-25 |
| 9 | `ses_e8dff9635ffexnn3oaUCgHVgfy` | argonwiki | 173 | 450 | 732 | 78 | 2026-10-25 |
| 10 | `ses_f04d1144cffeaRMPtegsTrvfCM` | Fix wiki links in 1836 concepts (@Worker) | 95 | 357 | 692 | 22 | 2026-10-02 |
| 11 | `ses_e91313ae6ffevb9sJhyg7Fv1kK` | تنفيذ بروتوكول BUILD_PROTOCOL لبناء wiki_ver1 | 77 | 230 | 582 | 33 | 2026-10-24 |
| 12 | `ses_f26ced106ffeMk7sCCNf8dpMea` | تحليل مراجع بناء الويكي (@general) | 12 | 60 | 505 | 27 | 2026-09-25 |
| 13 | `ses_e69d62e2affeYqepfp2Wyv3SYi` | استكشاف مشروع الويكي كاملاً (@general) | 27 | 95 | 459 | 39 | 2026-11-01 |
| 14 | `ses_06c5e911fffetsFv0AlJk1YzjN` | فهم هيكل الويكي على sdcard | 66 | 174 | 448 | 27 | 2026-07-24 |
| 15 | `ses_e8f6bf32bffeXyV717nhy6BL5L` | تحليل الويكيات الخمس واستخلاص الأفضل (@general) | 16 | 52 | 324 | 18 | 2026-10-25 |
| 16 | `ses_f039914e9ffeO1ow46bZf1VmcQ` | Build sdcard wiki structure (@Worker) | 36 | 145 | 297 | 47 | 2026-10-02 |
| 17 | `ses_11a2a8c07ffeAKI5a48vUdpNI6` | استكشاف wiki structure (@discover-explore) | 4 | 20 | 288 | 16 | 2026-06-20 |
| 18 | `ses_f0586070fffeqCutkF6YMasm6X` | Audit IGWIKI v2.1 source (@general) | 9 | 30 | 213 | 10 | 2026-10-02 |
| 19 | `ses_11a013543ffe76eSJT3uUvKDvc` | هيكلية wiki (@discover-explore) | 7 | 44 | 203 | 27 | 2026-06-20 |
| 20 | `ses_e6b7508c8ffeaxzs4K5eq3B6TX` | استكشاف مشروع الويكي كاملاً (@general) | 11 | 45 | 187 | 24 | 2026-11-01 |
| 21 | `ses_f0b4f75deffeezJfVXuPBaZEhX` | Design v3 wiki architecture (@Planner) | 9 | 39 | 154 | 9 | 2026-09-30 |
| 22 | `ses_e611d35cbffeDr7X8U3ZtEP5i1` | E1.3 فلترة محادثات Claude Code للويكي (@general) | 7 | 37 | 107 | 17 | 2026-11-03 |
| 23 | `ses_e8fd11df0ffel71MJ1GmImKrPI` | تدقيق ملفات wikillm (@explore) | 3 | 10 | 106 | 6 | 2026-10-24 |
| 24 | `ses_e8ea9a8afffeIpdcZByiVfO714` | محاكاة مستقبلية للويكي — سيناريوهات الفشل (@general) | 5 | 13 | 88 | 6 | 2026-10-25 |
| 25 | `ses_e8f5c748cffe0KFYGcfwF5yu0H` | محاكاة مستقبلية للويكي — سيناريوهات الفشل (@general) | 3 | 7 | 86 | 4 | 2026-10-25 |
| 26 | `ses_08eca9417ffebeEYPAD8obhwTQ` | Explore wiki concepts source (@explore) | 10 | 39 | 72 | 14 | 2026-07-17 |
| 27 | `ses_e611dfc7dffe57acQAM02Av41M` | E1.1 مسح sdcard لملفات الويكي (@general) | 5 | 22 | 52 | 12 | 2026-11-03 |
| 28 | `ses_e611ddf09ffes6PRGiY3IyVEZf` | E1.2 مسح /root و/root/r لملفات الويكي (@general) | 7 | 30 | 52 | 17 | 2026-11-03 |
| 29 | `ses_e611d252effeMV6fKerORx42yR` | E1.6 استكشاف OmniRush للويكي (@general) | 7 | 31 | 44 | 9 | 2026-11-03 |
| 30 | `ses_efc5789ebffeO8gvAv3G7I55Cd` | Extracting data from wiki.md to JSON | 3 | 5 | 37 | 3 | 2026-10-03 |
| 31 | `ses_f0361ca36ffeTmZ0wM5rZJm11O` | Build sdcard wiki structure (@Worker) | 4 | 17 | 36 | 6 | 2026-10-02 |
| 32 | `ses_e611db55cffePQvPBiU9VILhO4` | E1.5 استكشاف Antigravity للويكي (@general) | 9 | 32 | 33 | 8 | 2026-11-03 |
| 33 | `ses_e6b44a8efffepdpiXzFKMrpgKJ` | استكشاف مشروع الويكي كاملاً (@general) | 4 | 11 | 28 | 5 | 2026-11-01 |
| 34 | `ses_efc39057bffeyUTKPl0Ej2E1Ab` | تحليل wiki.md واستخراج تقرير JSON | 3 | 7 | 2 | 3 | 2026-10-03 |
| 35 | `ses_e85c62c97ffePiLN3rdcGWZntq` | بناء قوالب wiki_ver2 (@zen-worker) | 2 | 1 | 2 | 1 | 2026-10-26 |
| 36 | `ses_e6b302bb2ffeWDsbZ2ZbqlDIkz` | استكشاف مشروع الويكي كاملاً (@general) | 2 | 5 | 2 | 3 | 2026-11-01 |
| 37 | `ses_efc373fd5ffeERHwpbUSGJleMe` | Parsing wiki.md into big_pickle_analysis.json | 2 | 1 | 1 | 1 | 2026-10-03 |
| 38 | `ses_e91d076cdffeUQF56ZznYtAc28` | بناء نظام الويكي المثالي — تحليل معماري | 2 | 1 | 1 | 1 | 2026-10-24 |
| 39 | `ses_e91cff736ffe1q2os52FLEnnWR` | بناء نظام الويكي المثالي — تحليل معماري | 2 | 1 | 1 | 1 | 2026-10-24 |
| 40 | `ses_e91ceb1deffej8WFqmr10s6mUB` | تصميم معماري لنظام الويكي المعرفي | 2 | 1 | 1 | 1 | 2026-10-24 |
| 41 | `ses_e9142c179ffeu5sJttW0c81xT1` | تنفيذ بروتوكول بناء wiki_ver1 لنسخة kimi | 4 | 2 | 1 | 2 | 2026-10-24 |
| 42 | `ses_e8fd21b7cffezUqLcDgeU7soTU` | تدقيق ملفات wikillm (@zen-researcher) | 2 | 1 | 1 | 1 | 2026-10-24 |
| 43 | `ses_e85c64fafffehW5eqLtAGbXQ1I` | بناء هيكل wiki_ver2 (@zen-worker) | 2 | 1 | 1 | 1 | 2026-10-26 |
| 44 | `ses_efc72e81fffeNQ8Fjkt5ANGA8w` | Reading and analyzing wiki.md for metadata | 2 | 1 | 0 | 1 | 2026-10-03 |

**ملاحظات:**
- المحادثات الأربع الأكبر (`fork #1/#2`, `wiki`, `متابعة مشروع...`) تمثل **~6.9 MB من أصل 14.4 MB** (48%).
- `ses_e8f88d729ffe...` و `ses_e8f888e53ffe...` **متطابقتان تماماً** (244/675/784 KB) — fork مكرر، يكفي تصدير أحدهما.
- 13 محادثة حجمها ≤ 2 KB (غنية بالمحتوى لكن أجزاءها صغيرة/معاد توجيهها).

### 4.1 محادثات النسخة الاحتياطية (7 محادثات)

| session id | العنوان | msgs | parts | KB | wiki_parts | الإنشاء |
|---|---|---|---|---|---|---|
| `ses_ef1bd39ddffe387rt8u0LJBGn9` | تحليل بنية الويكي القديمة (@explore) | 16 | 134 | 1444 | 51 | 2026-10-05 |
| `ses_ef1e8f63affeMReI0nqoO5OBxd` | تحليل بنية الويكي القديمة (@explore) | 15 | 104 | 1381 | 42 | 2026-10-05 |
| `ses_ee9cf3076ffeCcSyGP0LOyxdyH` | استكمال wiki unclaimed 1 (@Worker) | 37 | 187 | 1156 | 38 | 2026-10-07 |
| `ses_ef151aa0dffe4zm4gIWVFXV4S9` | تدقيق مسودة الويكي الجديدة (@Reviewer) | 19 | 111 | 1060 | 42 | 2026-10-06 |
| `ses_ee9cf2c75ffeO0ELgMEFHNjl5L` | استكمال wiki unclaimed 3 (@Worker) | 17 | 124 | 755 | 48 | 2026-10-07 |
| `ses_ee9cf2df6ffejlr9GKSHq0YLHv` | استكمال wiki unclaimed 2 (@Worker) | 20 | 108 | 693 | 32 | 2026-10-07 |
| `ses_ee9cf2b0effeJFCdPVJXVz7pAq` | استكمال wiki unclaimed 4 (@Worker) | 19 | 113 | 563 | 40 | 2026-10-07 |

**الخلاصة:** الـ BACKUP يغطي فترة **05–07 أكتوبر 2026** فقط (7 محادثات، لا تتعارض مع قائمة القاعدة الرئيسية) — أي أنه يضيف محتوى **جديداً** لا يوجد في القاعدة الحالية.

---

## 5. إجمالي الحجم القابل للتصدير

### 5.1 القاعدة الرئيسية

| نطاق التصدير | عدد المحادثات | عدد الرسائل | عدد الأجزاء | الحجم الخام |
|---|---|---|---|---|
| **A — مطابقة العنوان (44)** | 44 | 2,578 | 7,589 | **15,978,875 B = 15.24 MB**<br>(parts 15,063,953 + msg 914,922) |
| **B — أي جزء يحوي wiki (787)** | 787 | — | 10,993 جزء مطابق | **114,539,625 B = 109.22 MB** (جزء المطابقات فقط) |
| **C — أحداث (`event`) مطابقة** | — | — | 17,456 صف | (جزء من `event.data`) |
| **D — `todo` مطابقة** | 4 محادثات | — | 7 صفوف | تافه (< 10 KB) |
| **E — `message.data` مطابقة** | `ses_06c607aeaffebzc8yvvE7A8ems` | 2 | — | 920 B |

### 5.2 النسخة الاحتياطية

| نطاق التصدير | محادثات | الحجم الخام |
|---|---|---|
| **A — مطابقة العنوان (7)** | 7 | **7,279,868 B = 6.94 MB**<br>(parts 7,224,000 + msg 55,868) |
| **B — أي جزء يحوي wiki (36)** | 36 | **22,037,857 B = 21.02 MB** (جزء المطابقات) |

### 5.3 الإجمالي الكلي للتصدير

| السيناريو | الحجم |
|---|---|
| **الحد الأدنى (العناوين فقط: 44 + 7)** | **23.2 MB** (22,258,743 B) |
| **الحد الأقصى (كل الأجزاء المطابقة: 787 + 36)** | **130.2 MB** (136,577,482 B) |
| **الملف الخام كاملاً (بدون فلترة)** | 914.8 MB + 104.7 MB = **1,019.5 MB** |

**التوصية العملية:** النطاق **A = 23.2 MB** يكفي لاستعادة كل محادثات الويكي ذات العنوان المطابق.
النطاق **B = 130 MB** يضيف 743 محادثة ذُكر فيها `wiki` عرضاً (أخطاء، مسارات، مراجع جانبية) — معظمها **ضوضاء** وليست محادثات وويكي حقيقية.

---

## 6. ملاحظات وحدود

1. **القاعدة نشطة** — الأرقام تتغير أثناء القراءة (فرق 215 صفاً في `part` خلال دقائق الفحص).
2. **`event` جدول ضخم** (217,903 صفاً، 17,456 مطابقاً) — يحتوي سجل تدفقي؛ تصديره غير ضروري لاستعادة المحادثات (المحتوى موجود في `part`).
3. **`storage/session_diff/`** — لا قيمة إطلاقاً (5 ملفات × 2 بايت، 0 مطابقة).
4. **743 محادثة رئيسية + 29 احتياطية** لها أجزاء تحوي `wiki` لكن عنوانها غير مطابق — مثال: `ses_0604fca2effe...` "Parallel: Unit Review: ..." حيث وردت كلمة wiki داخل مسار ملف (`wiki/concepts`).
5. **`session_input` فارغ تماماً** في القاعدتين (0 صف).
6. **تم الفحص بـ `mode=ro` حصراً** — لم يُستخدم `.backup`، لم يُنسخ أي `.db`، لم يُحذف أي ملف.
