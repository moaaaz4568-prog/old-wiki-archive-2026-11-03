# 📇 فهرس الويكي على `/sdcard` — تقرير قراءة فقط

> تاريخ الفحص: 2026-11-03 · طبيعة العملية: **قراءة فقط** (لا rm، لا تعديل، لا نسخ ملفات كبيرة)
> أوامر الفحص: `df -h` · `find` (اسم) · `grep` (محتوى) · `du` (حجم)

---

## 1. المساحة المتاحة

```
Filesystem      Size  Used Avail Use% Mounted on
-                48G   48G  646M  99% /mnt/sdcard
```

| البند | القيمة |
|---|---|
| الحجم الكلي | 48G |
| المستخدم | 48G (99%) |
| **المتاح** | **646M** ⚠️ حرجة — أي نسخة كاملة للويكي تستهلك جزءاً كبيراً من المتاح |

---

## 2. المجلدات الرئيسية (أعداد + أحجام)

| # | المسار | الحجم | إجمالي الملفات | ملفات .md | سبب الارتباط بالويكي |
|---|---|---|---|---|---|
| 1 | `/sdcard/Nexus_Brain` | **385M** | 18,791 | 8,330 | مخزن Nexus Brain الكامل + نسخ ويكي مدمجة + `.nexus_work/backup/.../wiki_full` |
| 2 | `/sdcard/NEXUS_LLM_WIKI` | **101M** | 7,518 | 4,385 | مشروع الويكي متعدد النطاقات (raw/staging/collections/indexes/tools) |
| 3 | `/sdcard/nexus_wiki` | **25M** | 286 | 120 | طبقات V1/V2/V3 + ملفات روابط `.link.txt` |
| 4 | `/sdcard/wiki` | **24M** | 246 | 122 | طبقات V1/V2/V3 (نسخة تشبه `nexus_wiki` بكثير) |
| 5 | `/sdcard/wikillm` | **8.3M** | 443 | 403 | بروتوكول البناء `BUILD_PROTOCOL.md` + إصدارات argon/glm/kimi |
| 6 | `/sdcard/NEXUS_WIKI_SKILLS` | **190K** | 13 | 13 | 12 مهارة ويكي + `INDEX.md` |
| — | **المجموع (مجلدات)** | **~543M** | **27,297** | **13,373** | |

### أرشيف ZIP (تنزيلات)

| المسار | الحجم | ملاحظة |
|---|---|---|
| `/sdcard/Download/Nexus_Brain.zip` | 45.4M (47,616,910 B) | نسخة مضغوطة من Nexus_Brain |
| `/sdcard/Download/Nexus_Brain-2.zip` | 45.4M (47,616,910 B) | **مطابق بالحجم تماماً** — نسخة مكررة محتملة |

---

## 3. الملفات المفرقة (Root / خارج المجلدات)

| المسار | الحجم | النوع | سبب الارتباط |
|---|---|---|---|
| `/sdcard/NEW_WIKI_MASTER_PLAN.md` | 10.9K | md | خطة الماستر للويكي |
| `/sdcard/NEXUS_LLM_WIKI_REPORT.html` | 30.5K | html | تقرير مشروع الويكي |
| `/sdcard/NEXUS_WIKI_EXPLAIN.html` | 76.5K | html | شرح تفاعلي للويكي |
| `/sdcard/IGWIKI_ALL_IN_ONE.txt` | 119.9K | txt | محتوى IGWIKI مجمع |
| `/sdcard/exploration-artifacts/WIKI_SKILLS_INSTALLATION.md` | 2.3K | md | توثيق تثبيت مهارات الويكي |
| `/sdcard/Android/media/.../WhatsApp Documents/IGWIKI_ALL_IN_ONE (2).txt` | 119.9K | txt | نسخة واتساب من نفس الملف (مطابقة بالحجم) |
| `/sdcard/Android/media/.../WhatsApp Documents/mind_operations_taxonomy_full.md` | — | md | طابع محتوى ويكي (grep match) |

---

## 4. تفصيل داخل كل مجلد رئيسي

### 4.1 `/sdcard/Nexus_Brain` (385M / 18,791 ملف)

| المسار الفرعي | الحجم | النوع | سبب الارتباط |
|---|---|---|---|
| `/sdcard/Nexus_Brain/Nexus_Brain/` | 258M | مجلد | النواة (يتضمن `.nexus_work`, `.stversions`) |
| `/sdcard/Nexus_Brain/nexus_vault/` | 25M | مجلد | الواجهة الرسمية (`NEXUS_BRAIN.md`, AGENTS.md) |
| `/sdcard/Nexus_Brain/brain/` | 20M | مجلد | مخزن المعرفة |
| `/sdcard/Nexus_Brain/rag/` | 3.3M | مجلد | نظام الاسترجاع `query.py` |
| `/sdcard/Nexus_Brain/Nexus_Brain/Nexus_Brain/wiki/` | **23M** | مجلد ويكي | نسخة ويكي كاملة داخلية |
| `/sdcard/Nexus_Brain/Nexus_Brain/wiki/` | **23M** | مجلد ويكي | نسخة ويكي (تكرار محتمل للأعلاه) |
| `/sdcard/Nexus_Brain/Nexus_Brain/.nexus_work/backup/pre_unification/wiki_full/` | **23M** (2,332 ملف) | نسخة احتياطية | حالة الويكي قبل التوحيد (`R4_old_wiki_state.md`) |
| `/sdcard/Nexus_Brain/NEXUS_LLM_WIKI.md` | 29.6K | md | مستند الويكي |
| `/sdcard/Nexus_Brain/NEXUS_LLM_WIKI_PHASE2.md` | 20.0K | md | مرحلة 2 |
| `/sdcard/Nexus_Brain/Nexus_Brain_Prompt.md` | 20.0K | md | برومبت النظام |
| `/sdcard/Nexus_Brain/nexus_vault/NEXUS_BRAIN.md` | — | md | مدخل الويكي/الدماغ |
| `/sdcard/Nexus_Brain/Nexus_Brain_Processed/` | 28K | مجلد | نسخة معالَجة |

⚠️ **ثلاث نسخ ويكي بحجم 23M متطابق** داخل Nexus_Brain — تكرار فعلي ~46M قابل للفهرسة كـ«مرشح تجميع» (وليس للحذف).

### 4.2 `/sdcard/NEXUS_LLM_WIKI` (101M / 7,518 ملف)

| المسار الفرعي | الحجم | النوع | سبب الارتباط |
|---|---|---|---|
| `raw/` | 53M | بيانات خام | مصادر أولية (أكبر ملف: `raw/new/transcript_full.txt` ≈1.5M) |
| `staging/` | 15M | بيانات وسطى | مخرجات عمال + `manifests` |
| `collections/` | 13M | مجموعات | أكبر ملف: `sales/full_evidence_ledger.jsonl` ≈5.7M |
| `sources/` | 7.2M | مصادر | |
| `claims/` | 7.2M | ادعاءات/أدلة | |
| `indexes/` | 2.7M | فهارس | `catalog.json` ≈1.5M |
| `reports/` | 1.8M | تقارير | `WIKI_SYSTEMS_AUDIT_2026-10-21.md` |
| `tools/` | 498K | أدوات | `wiki_quality.py`, `wiki_query.py`, `wiki_workflow.py`, `wiki_system_smoke_test.py` (+ `__pycache__`) |
| `systems/` | 440K | أنظمة | `20_WIKI_OPERATING_SYSTEM.md` |
| `MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md` | 22.4K | md | ميثاق التشغيل |
| `NEXUS_WIKI_EXPLAIN_3D.html` | 96K | html | شرح ثلاثي الأبعاد |
| `checkpoints/`, `model_protocols/`, `config/`, `concepts/`, `done/` | <100K لكل | مجلدات | |

### 4.3 `/sdcard/nexus_wiki` (25M / 286 ملف)

| المسار الفرعي | الحجم | النوع | سبب الارتباط |
|---|---|---|---|
| `03_WIKI_V3_NEW/` | **24M** | طبقة V3 | يتضمن `04_SEARCH/index.json.gz` (17.0M) وحزم العمل |
| `00_PROJECT/` | 192K | إدارة | `goals.md` |
| `06_TOOLS/` | 100K | أدوات | |
| `05_INBOX/` | 96K | وارد | |
| `02_WIKI_V2_TERMS/` | 36K | طبقة V2 | 8 ملفات `.link.txt` |
| `01_WIKI_V1_ARABIC/` | 27K | طبقة V1 | روابط `wiki.link.txt` etc. |
| `04_SOURCES_RAW/` | 19K | مصادر | |
| `README.md` | 8K | md | |

### 4.4 `/sdcard/wiki` (24M / 246 ملف)

| المسار الفرعي | الحجم | النوع | سبب الارتباط |
|---|---|---|---|
| `03_WIKI_V3_STRUCTURED/` | **24M** | طبقة V3 | **مطابق تقريباً لـ `nexus_wiki/03_WIKI_V3_NEW`** (نفس أحجام الملفات الكبيرة: `index.json.gz` 17.0M, `DEFECTS.jsonl` 1.39M, `LINK_PLAN.jsonl` 891K...) |
| `NEXUS_LLM_WIKI_NEW/` | 109K | نواة | `AGENTS.md` |
| `wiki/` | 38K | مجلد متداخل | |
| `02_WIKI_V2_TERMS_ATOMS/` | 16K | طبقة V2 | |
| `01_WIKI_V1_ARABIC_MASTERS/` | 12K | طبقة V1 | |
| `raw/` | 11K | خام | |
| `README.md`, `_FS_CAPABILITY_NOTE.md` | 8K | md | |

### 4.5 `/sdcard/wikillm` (8.3M / 443 ملف)

| المسار الفرعي | الحجم | النوع | سبب الارتباط |
|---|---|---|---|
| `07_user_messages_omnirush.md` | 2.8M | md | سجل رسائل (أكبر ملف نصي) |
| `argon_version/` (wiki_ver1 + wiki_ver2 + _briefs + _agy_logs) | 1.8M | إصدار | إصدار Argon — `wiki_ver1/`, `wiki_ver2/` |
| `06_user_messages_claude_wiki.md` | 820K | md | سجل رسائل Claude |
| `glm_version/wiki_ver2/` | 629K | إصدار | إصدار GLM — أنظمة SYS_01..15 + قوالب domains |
| `kimi_version/wiki_ver2/` | 530K | إصدار | إصدار Kimi |
| `_archive/argon_v1_rejected_2026-10-25/wiki_ver1/` | 450K | أرشيف | نسخة مرفوضة مؤرشفة |
| **`BUILD_PROTOCOL.md`** | **32K** (32,768 B) | md | **بروتوكول البناء — مرجع رئيسي** |
| `10_FULL_CONTEXT.md` | 22.1K | md | السياق الكامل |
| `DELIVERABLE_1_general_architecture.md` | 64K | md | |
| `DELIVERABLE_2_critique.md` | 104K | md | |
| `agents/` | 104K | مجلد | |
| ملفات سجلات أخرى (`07b`, `08`, `07c`, `06b`, `00_source...`) | ~700K | md | |

### 4.6 `/sdcard/NEXUS_WIKI_SKILLS` (190K / 13 ملف — كلها md)

```
INDEX.md
sequential-domain-orchestration/     (24K)
new-to-done-source-lifecycle/        (24K)
folder-index-and-handoff/            (24K)
domain-term-inventory/               (20K)
domain-discovery-and-routing/        (20K)
master-synthesis-retrieval-gate/     (16K)
source-ingestion-and-dedup/          (12K)
claim-extraction-and-evidence/       (12K)
wiki-iteration-and-risk-control/     (7.5K)
opinion-context-evaluation/          (7.5K)
evidence-driven-reasoning/           (7.5K)
concept-deepening/                   (7.5K)
```

---

## 5. نتائج فحص المحتوى (grep — مطابقة داخل الملفات)

النمط: `build_protocol|ويكي|wiki_ver|نظام ويكي|WIKI_V[0-9]|nexus_wiki|wikillm`

| النطاق | النتيجة |
|---|---|
| `/sdcard` كاملاً (`head -100`) | أغلب المطابقات من `.nexus_work/critique/` و `INGESTION_SYSTEM/` داخل Nexus_Brain (كلمات «ويكي» في نص عادي — false positives إدارية) + ملفات الويكي الحقيقية في الأعلى |
| نطاقات الويكي الخمسة (`wiki`, `nexus_wiki`, `wikillm`, `NEXUS_LLM_WIKI`, `NEXUS_WIKI_SKILLS`) | **150+ ملف** مؤكد (قائمة جزئية أعلاه؛ الفحص الكامل تجاوز مهلة 180s بسبب حجم `raw/`) |
| ملفات مفتاحية مؤكدة بالمحتوى | `wikillm/BUILD_PROTOCOL.md`, `wikillm/10_FULL_CONTEXT.md`, كل `wiki_ver*/README.md` + `_BUILD_REPORT.md` + `AGENTS.md`, طبقات `wiki/0*_*/README.md`, `nexus_wiki/README.md` + `00_PROJECT/goals.md` |

⚠️ **فشل جزئي موثّق:** أمر grep على `/sdcard` كاملاً بمهلة 180s لم يُكمل (النتيجة `head -100` خرجت، ثم انتهت المهلة على العدّ). البديل المنفّذ: grep مقيّد على مجلدات الويكي + قوالب `*.md|*.txt|*.json`.

---

## 6. أكبر الملفات (>100K) — مرشحات للنظر في النسخ

| الحجم | المسار |
|---|---|
| 17.0M | `/sdcard/wiki/03_WIKI_V3_STRUCTURED/04_SEARCH/index.json.gz` |
| 17.0M | `/sdcard/nexus_wiki/03_WIKI_V3_NEW/04_SEARCH/index.json.gz` (**تكرار**) |
| 5.7M | `/sdcard/NEXUS_LLM_WIKI/collections/sales/full_evidence_ledger.jsonl` |
| 2.8M | `/sdcard/wikillm/07_user_messages_omnirush.md` |
| 1.7M | `/sdcard/NEXUS_LLM_WIKI/collections/sales/source_classification.json` |
| 1.5M | ملفات `.jsonl` مكررة بين `wiki/` و `nexus_wiki/` (AUDIT_CONCEPTS*, DEFECTS, LINK_PLAN) |
| 1.5M | `/sdcard/NEXUS_LLM_WIKI/raw/new/transcript_full.txt` |
| 1.5M | `/sdcard/NEXUS_LLM_WIKI/indexes/catalog.json` |
| 820K | `/sdcard/wikillm/06_user_messages_claude_wiki.md` |

---

## 7. التكرارات المرصودة (للتجميع — لا للحذف)

| التكرار | الأدلة | التوفير التقديري عند التجميع |
|---|---|---|
| `wiki/03_WIKI_V3_STRUCTURED` ≈ `nexus_wiki/03_WIKI_V3_NEW` | أحجام متطابقة لملف بملف (16997907, 1497272, 1420455, 1386760, 891229...) | ~24M |
| 3× نسخ ويكي داخل Nexus_Brain بحجم 23M | `Nexus_Brain/wiki`, `Nexus_Brain/Nexus_Brain/wiki`, `.nexus_work/backup/.../wiki_full` | ~46M (بشرط التحقق بالـhash قبل أي تجميع) |
| `Nexus_Brain.zip` = `Nexus_Brain-2.zip` | الحجم متطابق 47,616,910 B | ~45M |
| `IGWIKI_ALL_IN_ONE.txt` (root) ≈ نسخة واتساب | 119,906 B كلاهما | ~120K |

---

## 8. المساحة المطلوبة التقديرية للنسخ (فهرس فقط — لم يُنسخ أي شيء)

| سيناريو النسخ | الحجم التقديري | % من المتاح (646M) |
|---|---|---|
| **أ) النواة الصغيرة** — `wikillm` + `NEXUS_WIKI_SKILLS` + الملفات المفرقة + ملفات الويكي داخل Nexus_Brain (5 ملفات md فقط) | **~9M** | 1.4% ✅ |
| **ب) الويكي الكامل بدون Nexus_Brain الكامل** — (أ) + `wiki` + `nexus_wiki` + `NEXUS_LLM_WIKI` + مجلدات الويكي الثلاثة 23M داخل Nexus_Brain | **~170M** | 26% ✅ |
| **ج) كل ما يُطابق اسم wiki/ويكي/nexus_brain** (يشمل Nexus_Brain كاملاً + ZIPs) | **~640M** | **99% ⛔ يفوق المتاح عملياً** |
| **د) النسخ المحسّن (بـ dedup للتكرارات أعلاه)** | **~430M** | 66% ⚠️ ممكن لكن يُبقي ≤200M حرية |

---

## 9. خلاصة

1. **المساحة حرجة:** 646M فقط متاحة من 48G (99% ممتلئ) — نسخة كاملة غير ممكنة.
2. **الويكي موزّع على 6 مجلدات رئيسية + ملفات مفرقة + ZIPs** — إجمالي ~543M مجلدات + 91M زِيبات.
3. **أكبر كتلة:** `Nexus_Brain` (385M) يحوي 3 نسخ ويكي متطابقة القياس (23M×3) + نواة تعرف عليها فهرسنا.
4. **المرجع الأساسي للويكي:** `/sdcard/wikillm/BUILD_PROTOCOL.md` + إصدارات `wiki_ver1/2` (argon/glm/kimi) + طبقات `wiki` و `nexus_wiki` (V1/V2/V3) + مشروع `NEXUS_LLM_WIKI` (101M).
5. **التكرارات كبيرة** (~115M) — أي نسخة مستقبلية يجب أن تمرّ بـ dedup أولاً.
6. **لم يُعدَّل أي ملف** خلال هذه المهمة؛ التقرير أُنشئ خارج `/sdcard` في مساحة العمل.
