# تقرير فهرسة الويكي في `/root` (قراءة فقط)

**تاريخ الفحص:** 2026-11-03  
**النطاق:** `/root` باستثناء `/root/.cache` و`/root/.local/share/opencode`  
**القيود:** لم يُعدَّل أو يُحذف أي ملف — فهرسة فقط.

---

## 1. جدول المسارات

| المسار | الحجم | النوع | سبب الارتباط |
|---|---|---|---|
| `/root/r/nexus_enrichment` | 209M | مجلد (1457 ملف) | مشروع إثراء الويكي: state/runs + knowledge + `wiki_routing/` + `control/WIKI_STRUCTURE.md` |
| `/root/r/NEXUS_GITHUB_PACKAGE/WIKI` | 169M | مجلد (11438 ملف) | الويكي الفعلية: `01_ACTIVE_WIKI` (146M، يحوي NEXUS_LLM_WIKI.md + nexus_vault + brain) و`02_ENRICHMENT_PROJECT` (23M، نسخة mirror من nexus_enrichment) |
| `/root/r/NEXUS_REFERENCES/llm-wiki-compiler` | 16M | مجلد (71 ملف) | أكواد إضافة wiki-compile (أوامر wiki-init/ingest/lint/query…) |
| `/root/r/NEXUS_REFERENCES/llm-wiki-plugin` | 9.1M | مجلد (259 ملف) | مستودع إضافة LLM Wiki: سكربتات wiki_evolve/graph/lint/search + واجهة WikiPage/Sidebar + اختبارات |
| `/root/r/V3` | 24M | مجلد (239 ملف) | بيئة/بوابة الإصدار V3 المرتبطة بمعمارية الويكي الجديدة |
| `/root/r/V3_SYS` | 483K | مجلد (16 ملف) | نظام V3 المصاحب |
| `/root/r/orchestrator` | 1.5M | مجلد | `nexus_brain_ops/exploration/02_wiki_concepts.md` + `output/MY_wiki_messages.md` |
| `/root/r/nexus-brain-v2` | 98K | مجلد | نسخة Nexus Brain v2 المرتبطة بمشاريع الويكي |
| `/root/r/WIKI_HUB` | 11K | مجلد (هيكل + README) | hub تنظيمي: `01_WIKI_V1_ARABIC_MASTERS` و`02_WIKI_V2_TERMS_ATOMS` (11 مساراً فرعياً لكل منهما) |
| `/root/r/nexus_wiki_links` | 18K | مجلد (هيكل روابط/mirrors) | `01_WIKI_V1_ARABIC` + `02_WIKI_V2_TERMS` + `04_SOURCES_RAW` — جسور/روابط لطبقات الويكي |
| `/root/r/NEXUS_WIKI_SCALABLE_ARCHITECTURE.md` | 12K | ملف md | وثيقة المعمارية القياسية لنظام Nexus LLM Wiki الموسع (100K+ ملفات، Raw→Route→Candidate→Claims→Concepts→Masters) |
| `/root/r/الويكي.md` | 628K (9768 سطر) | ملف md | سجل جلسة "استيراد الإضافة وتشغيل الوكلاء" — ويكي |
| `/root/r/wiki1.md` | 464K (6102 سطر) | ملف md | سجل جلسة "متابعة مشروع متعدد المراحل عبر جيت هب والويكي" |
| `/root/r/wiki.md` | 440K (4503 سطر) | ملف md | نسخة/مكمل لسجل الجلسة نفسها (بنية مطابقة لـ wiki) |
| `/root/r/wiki` | 440K (4503 سطر) | ملف نصي (بدون امتداد) | مطابق تماماً لـ `wiki.md` — نسخة مكررة |
| `/root/process_wiki_loop.sh` | 8K | سكربت bash | "Nexus Brain Wiki — AUTO PROCESSOR v3" (حلقة تلقائية لمعالجة الويكي على `/sdcard/Nexus_Brain`) |
| `/root/r/data/masters/*_V3.json` (3 ملفات) | ضمن 11M | json | ماسترز بإصدار V3: Content_Creation_Framework / Storytelling_Copywriting / Foundation_Business_Strategy |
| `/root/r/reports/sales-proof/*-v3.md` (3 ملفات) | ضمن 280K | md | تقارير أنظمة مبيعات V3 |
| `/root/r/conversations_backup/conversation_nexus_wiki_3_*.jsonl` | ضمن 16M | jsonl | نسخة احتياطية لجلسة "nexus_wiki" |
| `/root/r/NEXUS_GITHUB_PACKAGE/.../wikirepo.md` + `conversation_nexus_wiki_*.jsonl` | ضمن 341M | md/jsonl | نسخ داخل حزمة GitHub: تصدير رسائل ويكي + جلسة ويكي |
| `/root/r/NEXUS_GITHUB_PACKAGE/.../cognee_nexus/data/misc/wiki_*.json` (5 ملفات) + `prep_missing_wiki.py` | ضمن 341M | json/py | فهارس وسجلات ويكي: wiki_index.json, wiki_CHECKPOINT, wiki_log, wiki_link_repair_report, wiki_business_plan_index |
| `/root/r/NEXUS_GITHUB_PACKAGE/.../cognee_nexus/reports/*wiki*.md` (2 ملف) | ضمن 341M | md | تدقيق اكتمال الويكي + استخراج المفقود (2026-07-29) |
| `/root/r/NEXUS_GITHUB_PACKAGE/.git` (فرع `v3-fix`) | ضمن 341M | git | فرع إصلاح V3 |
| `/root/r/NB2` (فرع git `v3`) + مفاهيم *_V3* | — | git/md | نسخة NB2 بفرع v3 + مفاهيم مرتبطة بـ DeepSeek V3 وMidro v3 |
| `/root/AGENTS.md` | — | md | يحتوي إشارة إلى wiki (يُطابق `grep -liE "wiki|ويكي"` لملفات `/root/*.md`) |

### مسارات طُلبت فحصها ولم توجد
- `/root/r/NEXUS_PROJECT` — **غير موجود**
- `/root/r/NEXUS_WIKI_EXPLAIN*` — **غير موجود** (لا تطابق أي ملف)
- (`/root/r/NEXUS_OS*` وُجد لكنه ليس ويكي: `NEXUS_OS_COMPREHENSIVE_SYSTEMS_BLUEPRINT.md`, `NEXUS_OS_PERFECT_ARCHITECTURE_SPEC.md`)

---

## 2. نتائج أوامر البحث المباشرة

1. `find /root/r ... (*wiki*|*ويكي*|*wikillm*|*V3*)` → **66 ملف ويكي + 50 ملف V3** (بلا node_modules)؛ من أبرزها مسارا `NEXUS_GITHUB_PACKAGE/WIKI/*` و`NEXUS_REFERENCES/llm-wiki-*` و`nexus_enrichment/*` وملفات md الجذور.
2. `find /root -maxdepth 2 ... (*wiki*|*ويكي*)` → 7 ملفات:
   - `/root/process_wiki_loop.sh`
   - `/root/r/wiki.md`, `/root/r/الويكي.md`, `/root/r/wiki`, `/root/r/wiki1.md`, `/root/r/NEXUS_WIKI_SCALABLE_ARCHITECTURE.md`
   - (وأيضاً `/root/AGENTS.md` يظهر عبر grep لا عبر find)
3. `ls /root/*.md | xargs grep -liE "wiki|ويكي"` → `/root/AGENTS.md` فقط.

---

## 3. الإجماليات

| البند | القيمة |
|---|---|
| عدد ملفات الويكي المسمّاة صراحةً (find في /root/r) | 66 |
| عدد ملفات V3 المسمّاة صراحةً (find في /root/r) | 50 |
| ملفات داخل `NEXUS_GITHUB_PACKAGE/WIKI` | 11,438 |
| ملفات داخل `nexus_enrichment` | 1,457 |
| ملفات داخل `V3` / `V3_SYS` | 239 / 16 |
| ملفات `llm-wiki-plugin` / `llm-wiki-compiler` | 259 / 71 |
| **إجمالي تقريبي لملفات النطاق الويكي** | **≈ 13,500 ملف** |

### المساحة التقديرية للنسخ (backup/copy)

| المكوّن | الحجم |
|---|---|
| nexus_enrichment | 209M |
| NEXUS_GITHUB_PACKAGE/WIKI | 169M |
| V3 | 24M |
| llm-wiki-compiler | 16M |
| llm-wiki-plugin | 9.1M |
| orchestrator + nexus-brain-v2 + WIKI_HUB + nexus_wiki_links | ≈ 1.7M |
| ملفات md/نص الجذور (wiki, الويكي, wiki1, NEXUS_WIKI_SCALABLE…) | ≈ 1.5M |
| **إجمالي النطاق الويكي (بدون باقي NEXUS_GITHUB_PACKAGE/NEXUS_REFERENCES)** | **≈ 431M** |

> ملاحظة: النسخة الكاملة لـ `NEXUS_GITHUB_PACKAGE` = 341M و`NEXUS_REFERENCES` = 52M، لكنها تشمل ملفات غير ويكي؛ النطاق الويكي المصعد أعلاه ≈ **431M**، ونسخة شاملة مع الحزمتين ≈ **~700M**.

---

## 4. ملاحظات مهمة

- **تكرار:** `NEXUS_GITHUB_PACKAGE/WIKI/02_ENRICHMENT_PROJECT` (23M) نسخة تبدو mirror لـ `/root/r/nexus_enrichment` (209M الفرق ناتج عمّا إضافي في الأصل)؛ و`/root/r/wiki` مطابق لـ `wiki.md`. أي نسخ احتياطي يجب أن يتحقق من هذه التكرارات أولاً لتفادي مضاعفة المساحة.
- **روابط/هيكل فارغ نسبياً:** `WIKI_HUB` و`nexus_wiki_links` يحويان غالباً مجلدات وروابط (11K/18K فقط) — هياكل تنظيمية لا محتوى.
- **سكربت نشط خارج r:** `/root/process_wiki_loop.sh` يشير إلى مسار `/sdcard/Nexus_Brain` (خارج نطاق هذا الفحص).
