# 📊 تقرير استكشاف محادثات OmniRush المتعلقة بالويكي

**تاريخ التنفيذ:** 2026-11-03
**النطاق:** قراءة فقط — لا تعديل، لا حذف، لا نسخ قواعد بيانات كاملة.
**الكلمات المفتاحية:** `wiki` · `ويكي` · `wikillm` (case-insensitive)
**منهجية التصنيف:** مبني على تحليل فعلي للنص (JSONL / SQLite)، لا على الافتراضات.

---

## 1️⃣ جدول المصادر

| # | المسار | الحجم | # ملفات / كيانات | # مطابقات |
|---|---|---:|---:|---:|
| 1 | `/root/r/BACKUP_OMINIRUSH_CHAT/agent-sessions/` | 7.0 KB | **0 ملف** (مجلد واحد فارغ `--root-r--`) | **0** — لا ملفات تُفحص |
| 2 | `/root/r/BACKUP_OMINIRUSH_CHAT/omnirush-upload-sessions.json` | 7,510 B (8 KB) | 1 ملف · **34 معرف محادثة** | **0** (`wiki`=0, `ويكي`=0, `wikillm`=0) |
| 3 | `/root/r/BACKUP_OMINIRUSH_CHAT/opencode.db` | **105 MB** (109,793,280 B) | 20 جدول · **40 جلسة** · 1,093 رسالة · 5,851 جزء · 17,352 حدث | **1,767** جزء مطابق (27,548 occurrence) + **4,224** حدث (32,252) |
| 4 | مجلدات OmniRush الأخرى في `/root/r` (`omnirush-login-fix`, `omnirush_migrate`, `omnirush-delegate`, `skills/omnirush-delegate`, `OMNIRUSH_*.md`) | ~100 KB | 8 ملفات (توثيق/سكربتات/SKILL) | **0** — لا تحتوي session/chat |
| 5a | `~/.omnirush/agent/sessions/` | **253 MB** | **1,404** ملف (1,403 `.jsonl` + 1 `.subagents-sorted.json` مطابقته 0) | **700** ملف مطابق (60,763 occurrence) |
| 5b | `~/.omnirush/omnirush-archive/sessions/` | 16 KB | 3 | **0** |
| 5c | `~/.omnirush/updates/sessions/` | 12 KB | 2 | **0** |
| 5d | `~/.omnirush/omnirush-upload-sessions.json` | 7,790 B | 18 جلسة رفع | **0** |
| 5e | `~/.omnirush/strict-sessions.json` | — | 1 (مفتاح واحد `https://omnirush.ai`) | **0** |
| 5f | `~/.omnirush/classic-imports.json` | 247,340 B | 1 | **0** |
| 5g | `~/.omnirush/omnirush-upload-bases/` | 172 MB | 37,811 (محتوى ملفات مرفوعة — ليس محادثات) | 728 (محتوى ملفات، خارج نطاق المحادثات) |
| 5h | `~/.omnirush/omnirush-upload-spool/` | 88 MB | 31 (معظمه `.zst` مضغوط) | 0 في الـ `.json` غير المضغوط · `.zst` غير قابل للفحص المباشر |
| 5i | `~/.local/share/omnirush/opencode.db` (النشط) | **446 MB** (446,279,680 B) | **235 جلسة** · 4,113 رسالة · 26,368 جزء | **6,949** جزء مطابق (92,570 occurrence) |
| 5j | `~/.local/share/omnirush/backup-v1/opencode.db.2026-10-27T18-23-15-890Z` | 446,197,760 B | نفس العدّادات (235/4,113/26,368) | **6,949** جزء — نسخة مطابقة عدديًا للنشط |
| 5k | `~/.local/share/omnirush/v1-sessions.json` | 7,790 B | 3 مفاتيح (`v`, `engine`, `ids`) | **0** |
| 5l | `~/.config/omnirush/` | 63 MB | 3,651 ملف (معظمه `node_modules`) | **0** باستثناء `node_modules` (15 معها) |
| 5m | `~/.local/state/omnirush/` | 46 KB | 7 | **1** (`prompt-history.jsonl` → `wikillm`) |
| 5n | `~/.cache/omnirush/` | 177 MB | 9,436 (حزم/opencode-orchestrator) | **0** |

> **ملاحظة 1:** مجلد `BACKUP_OMINIRUSH_CHAT/agent-sessions/` **فارغ فعليًا** — `find -type f | wc -l` = **0**، ويحوي مجلدًا واحدًا باسم `--root-r--` بلا أي ملف.
> **ملاحظة 2:** `omnirush-upload-sessions.json` **لا يحوي نصوص محادثات**، فقط معرّفات + metadata رفع → البحث عن "wiki" فيه = 0 نتيجة (لمحة أدناه).
> **ملاحظة 3:** `~/.local/share/omnirush/backup-v1/*` و `opencode.db` النشط متطابقان في العدّادات الأساسية (235/4,113/26,368) رغم اختلاف الحجم بمقدار ~82 KB (WAL/فراغ).

---

## 2️⃣ المصدر 2 بالتفصيل: `omnirush-upload-sessions.json`

| البند | القيمة |
|---|---|
| البنية | `{"version": 1, "sessions": {…}}` (dict) |
| عدد الجلسات الأم | **3** |
| `childSessionIds` | **31** |
| **إجمالي المعرّفات الفريدة** | **34** |
| المعرّفات الأم (3) | `ses_ef2243c6fffeq0hPvbQJVh1ZCu` (31 طفل) · `ses_ee9080c70ffegpCzae414xoOQV` (0) · `ses_ef25cbb7cffe711BXCUQ4KUU7D` (0) |
| الموديل | `omnirush / gpt-6-astra` · variant `high` · agent `build` |
| آخر ظهور | `2026-10-08T13:07:42.273Z` |
| `failureCount` (أعلى) | 462 |
| نصوص محادثات؟ | **لا** — metadata فقط |
| مطابقات `wiki` / `ويكي` / `wikillm` | **0 / 0 / 0** |

**الخلاصة:** الملف يحوي **34 معرّف محادثة** لكن **لا يحوي أي محتوى**، لذا لا يمكن ترتيبها كـ"محادثات ويكي" من هذا الملف وحده — الترتيب يأتي من `opencode.db` و `agent/sessions/*.jsonl`.

---

## 3️⃣ المصدر 3 بالتفصيل: `BACKUP_OMINIRUSH_CHAT/opencode.db`

**الجداول:** `account, account_state, control_account, credential, data_migration, event, event_sequence, message, migration, part, permission, project, project_directory, session, session_context_epoch, session_input, session_message, session_share, todo, workspace`

| المقياس | القيمة |
|---|---:|
| إجمالي الجلسات | 40 |
| إجمالي الرسائل | 1,093 |
| إجمالي الأجزاء (`part`) | 5,851 |
| إجمالي الأحداث (`event`) | 17,352 |
| أجزاء مطابقة لـ wiki/ويكي | **1,767** (30.2%) |
| occurrences داخل الأجزاء | **27,548** |
| أحداث مطابقة | **4,224** (24.3%) |
| occurrences داخل الأحداث | **32,252** |
| مطابقات `wikillm` | **0** |
| `message.data` مطابقة | **0** |
| جلسات عنوانها يحوي wiki/ويكي | **7** |
| جلسات تحتوي ≥1 جزء مطابق | **36 / 40** |
| جلسات **موضوعها ويكي** (العنوان أو أول رسالة مستخدم) | **33 / 40** |
| نطاق التاريخ | 2026-10-05 19:56 → 2026-10-08 13:06 |

### 3.1 الجلسات السبع ذات العنوان الواضح

| معرّف الجلسة | العنوان | التاريخ |
|---|---|---|
| `ses_ef1e8f63affeMReI0nqoO5OBxd` | تحليل بنية الويكي القديمة (@explore subagent) | 2026-10-05 22:02 |
| `ses_ef1bd39ddffe387rt8u0LJBGn9` | تحليل بنية الويكي القديمة (@explore subagent) | 2026-10-05 22:50 |
| `ses_ef151aa0dffe4zm4gIWVFXV4S9` | تدقيق مسودة الويكي الجديدة (@Reviewer subagent) | 2026-10-06 00:47 |
| `ses_ee9cf3076ffeCcSyGP0LOyxdyH` | استكمال wiki unclaimed 1 (@Worker subagent) | 2026-10-07 11:47 |
| `ses_ee9cf2df6ffejlr9GKSHq0YLHv` | استكمال wiki unclaimed 2 (@Worker subagent) | 2026-10-07 11:47 |
| `ses_ee9cf2c75ffeO0ELgMEFHNjl5L` | استكمال wiki unclaimed 3 (@Worker subagent) | 2026-10-07 11:47 |
| `ses_ee9cf2b0effeJFCdPVJXVz7pAq` | استكمال wiki unclaimed 4 (@Worker subagent) | 2026-10-07 11:47 |

### 3.2 أعلى 10 جلسات حسب كثافة الـ wiki (جزء مطابق / إجمالي الأجزاء)

| # | مطابق/الكل | معرّف الجلسة | العنوان |
|---:|---:|---|---|
| 1 | 98/182 | `ses_eea09771cffePDNtDf3PcT7fLf` | استخراج chunk أربعة (@Worker) |
| 2 | 94/205 | `ses_ee842461fffe2k1cJMbYXSHjU2` | مراجعة معنى المرشحات (@Reviewer) |
| 3 | 71/171 | `ses_ee7b0cb03ffef3oI1BEO8r3lCD` | كتابة مفاهيم المحتوى (@Worker) |
| 4 | 67/150 | `ses_eeca74f65ffe6vCWPLnnSY2zy5` | تدقيق التغطية (@Reviewer) |
| 5 | 66/185 | `ses_ee8424b3cffegOQR2fAzSvJ0P4` | بناء مفاهيم المبيعات الفعلية (@Worker) |
| 6 | 66/207 | `ses_ee7cdc4deffeftQYLIsQYvxZRE` | كتابة مفاهيم المبيعات (@Worker) |
| 7 | 64/194 | `ses_ee842478bffeY0uBRUfAAlAHmz` | بناء مفاهيم المحتوى والبراند (@Worker) |
| 8 | 55/185 | `ses_eeca75051ffe5VggEo1xcd3C2e` | تحليل المحتوى والبراند (@Worker) |
| 9 | 51/134 | `ses_ef1bd39ddffe387rt8u0LJBGn9` | تحليل بنية الويكي القديمة (@explore) |
| 10 | 51/157 | `ses_ef1a6e900ffeDyR1dko2A1Tg0z` | تحليل صيغ المفاهيم والماسترز (@general) |

---

## 4️⃣ المصدر 5 بالتفصيل: `~/.omnirush/agent/sessions/*.jsonl`

| المقياس | القيمة |
|---|---:|
| إجمالي ملفات JSONL | **1,403** (معرّفات فريدة 1,403) |
| ملفات فيها أي ذكر | **700** (49.9%) |
| ملفات **موضوعها ويكي** (أول رسالة مستخدم تذكر wiki/ويكي) | **373** |
| إجمالي occurrences | **60,763** (في ملفات الموضوع: 39,343) |
| مطابقات `wikillm` | **0** |
| نطاق التاريخ | 2026-04-24 → 2026-10-09 |

### حسب المجلد الفرعي

| المجلد | ملفات | أي مطابقة | موضوع ويكي | occurrences |
|---|---:|---:|---:|---:|
| `--root-r--/` | 535 | 374 | **232** | 40,742 |
| `--root-opencode--/` | 858 | 325 | **141** | 20,000 |
| `--root-ig--/` | 1 | 1 | 0 | 21 |
| `--tmp--/` | 7 | 0 | 0 | 0 |
| `--tmp-octest--/` | 2 | 0 | 0 | 0 |

### أعلى 10 محادثات حسب occurrences

| occurrences | معرّف الجلسة | المجلد | أول رسالة (مقتطف) |
|---:|---|---|---|
| 1,440 | `ses_f26ced106ffeMk7sCCNf8dpMea` | root-r | استكشف المرجعين `/root/r/NEXUS_REFERENCES/llm-wiki-plugin` و `llm-wiki-compiler` |
| 1,078 | `ses_ee842461fffe2k1cJMbYXSHjU2` | root-r | تقرير `/sdcard/NEXUS_LLM_WIKI/reports/SEMANTIC_AUDIT_2026-10-07.md` |
| 856 | `ses_ef151aa0dffe4zm4gIWVFXV4S9` | root-r | اقرأ المسودة على `/sdcard/wiki/` (`README.md`, `wiki/systems/00_WHY.md`) |
| 810 | `ses_f0c292dd0ffe766mk6TLpesYSK` | root-r | محادثة سابقة مع glm 5.3 حول الويكي |
| 781 | `ses_f0540dd22ffedHe7VhJfoxWT4A` | root-r | مهمة تنفيذية (قراءة/كتابة الويكي) |
| 763 | `ses_080316dd2ffedXK11QcPSCpovr` | root-r | افحص بنية `/sdcard/Nexus_Brain` |
| 692 | `ses_ee9cf2df6ffejlr9GKSHq0YLHv` | root-r | `staging/unclaimed_chunks/chunk_2.txt` (350 مسار) |
| 684 | `ses_ef1bd39ddffe387rt8u0LJBGn9` | root-r | اقرأ بنية الويكي القديمة |
| 658 | `ses_ee7b0cb03ffef3oI1BEO8r3lCD` | root-r | اكتب داخل `/sdcard/NEXUS_LLM_WIKI/` |
| 591 | `ses_f039914e9ffeO1ow46bZf1VmcQ` | root-r | مهمتك محصورة في `/sdcard/wiki/` |

---

## 5️⃣ المصدر 5 بالتفصيل: قواعد بيانات OmniRush النشطة

### `~/.local/share/omnirush/opencode.db` (446 MB)

| المقياس | القيمة |
|---|---:|
| الجلسات | **235** |
| الرسائل | 4,113 |
| الأجزاء | 26,368 |
| أجزاء مطابقة | **6,949** |
| occurrences | **92,570** |
| جلسات ≥1 جزء مطابق | **177 / 235** |
| جلسات **موضوعها ويكي** | **148 / 235** |
| عناوين مطابقة | 15 |
| **مطابقات `wikillm`** | **1** ← جلسة واحدة |
| نطاق التاريخ | 2026-07-03 → 2026-10-27 |

**الجلسة الوحيدة التي تذكر `wikillm`:**

| معرّف الجلسة | العنوان | التاريخ | أول رسالة |
|---|---|---|---|
| `ses_e81921099ffebArD7mwDNRJZnB` | New session - 2026-10-27T17:34:56.374Z | 2026-10-27 17:34:56 | «اقرأ الملف `/sdcard/wikillm/BUILD_PROTOCOL.md` كاملاً ونفّذه حرفياً من أوله لآخره…» |

> **تنبيه:** الجلسة الوحيدة `wikillm` موجودة **فقط** في قاعدة البيانات النشطة و`~/.local/state/omnirush/prompt-history.jsonl` — **غير موجودة** في النسخة الاحتياطية ولا في `agent/sessions/*.jsonl`.

### `~/.local/share/omnirush/backup-v1/opencode.db.2026-10-27T18-23-15-890Z`

نفس العدّادات تمامًا (235 جلسة / 4,113 رسالة / 26,368 جزء / 6,949 مطابق / 148 موضوع / 15 عنوان) → نسخة مطابقة عدديًا.

---

## 6️⃣ المصدر 4: مجلدات OmniRush في `/root/r`

```
find /root/r -maxdepth 2 -iname "*omnirush*" -o -maxdepth 2 -iname "*omni*"
```

| المسار | النوع | يحوي session/chat؟ |
|---|---|---|
| `/root/r/BACKUP_OMINIRUSH_CHAT/` | نسخة احتياطية | **نعم** — الوحيد الذي يحوي محادثات في `/root/r` |
| `/root/r/omnirush-login-fix/research.md` | توثيق | لا |
| `/root/r/omnirush_migrate/opencode_to_pi.mjs` | سكربت | لا |
| `/root/r/omnirush-delegate/` + `/root/r/skills/omnirush-delegate/` | SKILL + refs + scripts | لا (1 ذكر `/sdcard/NEXUS_LLM_WIKI` في `references/writing-the-brief.md`) |
| `/root/r/OMNIRUSH_*.md` (8 ملفات) | توثيق إصلاحات | لا |
| `/root/r/omniroute-key-key_new_99.txt`, `omnirush_test.log` | مفتاح/سجل | لا |

**الخلاصة:** لا يوجد أي مجلد محادثات OmniRush آخر في `/root/r` عدا `BACKUP_OMINIRUSH_CHAT/`.

---

## 7️⃣ إجمالي المحادثات المطابقة (التقاطع بين المصادر)

| المعيار | العدد |
|---|---:|
| معرّفات محادثات قبل إزالة التكرار | 1,403 (jsonl) + 235 (db نشط) + 40 (db احتياطي) = 1,678 |
| **معرّفات محادثات فريدة بعد إزالة التكرار** | **1,567** |
| **محادثات موضوعها ويكي** (عنوان أو أول رسالة مستخدم) — اتحاد المصادر | **468** |
| محادثات تحتوي أي ذكر للويكي في محتواها — اتحاد المصادر | **816** |
| من الـ jsonl: موضوع ويكي | 373 |
| من القاعدة النشطة: موضوع ويكي (53 منها متداخلة مع jsonl) | 148 → **95 جديدة** غير موجودة في jsonl |
| من النسخة الاحتياطية: موضوع ويكي (كلها متداخلة مع jsonl) | 33 |
| جلسات `wikillm` صريحة | **1** (`ses_e81921099ffebArD7mwDNRJZnB`) |
| جلسات `wikillm` في `BACKUP/opencode.db` | 0 |
| جلسات `wikillm` في `agent/sessions/*.jsonl` | 0 |

> **تفصيل التداخل:**
> - `jsonl topic ∩ live topic` = **53**
> - `jsonl topic` غير الموجودة في القاعدة النشطة = **320** (معظمه أقدم من 2026-07-03 أو تم تدويرها)
> - `live topic` غير الموجودة في ملفات jsonl = **95** (معظمه بعد 2026-10-09 — ملفات jsonl تنتهي عنده)
> - `backup topic` ⊆ `jsonl topic` (كلها الـ 33 موجودة)
> - من حيث الجلسات بلا تصنيف: 164 جلسة في القاعدة النشطة غير موجودة في jsonl، و40 جلسة النسخة الاحتياطية كلها موجودة في jsonl

---

## 8️⃣ ملاحظات ومنع التضخيم

1. **"أي ذكر" ≠ "موضوع الويكي":** 700 ملف jsonl و177 جلسة في القاعدة تحتوي كلمة wiki، لكن كثير منها ذكر عرضي (مسار `/sdcard/NEXUS_LLM_WIKI/` داخل prompt عام). لذلك أُبلِّغ الرقمان معًا: **468 موضوعيًا** مقابل **816 بأي ذكر**.
2. **`wikillm` نادر جدًا:** كلمة `wikillm` تظهر في محادثة واحدة فقط عبر كل المصادر (مع ملف `prompt-history.jsonl` مرتبط بها) — لا تُحوِّل أي مثال إلى قاعدة مطلقة.
3. **النطاق الزمني مختلف لكل مصدر:** jsonl (أبريل→9 أكتوبر)، القاعدة النشطة (3 يوليو→27 أكتوبر)، النسخة الاحتياطية (5→8 أكتوبر فقط). أي عدد نهائي يعتمد على أي مصدر تُعِدّه المرجع.
4. **`omnirush-upload-bases` (728 مطابقة)** هي محتوى ملفات مرفوعة وليست محادثات — استُثنيت من عدّ المحادثات.
5. **`omnirush-upload-spool`** معظمه `.zst` مضغوط → غير قابل للفحص النصي المباشر دون فك ضغط (لم يُفك، التزامًا بنطاق القراءة الآمن).

---

## 9️⃣ الأوامر الفعلية التي شُغّلت (إثبات)

```bash
# 1) agent-sessions
find /root/r/BACKUP_OMINIRUSH_CHAT/agent-sessions/ -type f | wc -l   # → 0

# 2) upload-sessions.json
python3 -c "import json;d=json.load(open('.../omnirush-upload-sessions.json'));..."   # → 3 sessions / 34 ids / wiki=0

# 3) opencode.db (read-only)
sqlite3 "file:.../opencode.db?mode=ro" ".tables"
sqlite3 "file:.../opencode.db?mode=ro" "select count(*) from part where lower(data) like '%wiki%' or data like '%ويكي%';"  # → 1767

# 4) مجلدات omnirush في /root/r
find /root/r -maxdepth 2 -iname "*omnirush*" -o -maxdepth 2 -iname "*omni*"

# 5) ~/.omnirush* و ~/.local/share/*omni*
ls -d ~/.omnirush* ~/.local/share/*omni*
find /root/.omnirush/agent/sessions -type f -print0 | xargs -0 grep -licE "wiki|ويكي|wikillm" | wc -l   # → 700
```

**الأدلة الرقمية المخزّنة كملفات:**
- `/tmp/opencode/wiki_rows.json` — 1,403 صف (تحليل JSONL)
- `/tmp/opencode/db_backup.json` — 40 صف (تحليل القاعدة الاحتياطية)
- `/tmp/opencode/db_live.json` — 235 صف (تحليل القاعدة النشطة)
