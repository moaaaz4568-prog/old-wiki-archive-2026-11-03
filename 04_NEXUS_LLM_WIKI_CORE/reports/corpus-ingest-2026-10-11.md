# تقرير تسجيل corpus — 2026-10-11

## نوع العملية

- **العملية:** أول خطوة فعلية لتحويل المصادر إلى ويكي: collection عامة لتسجيل الهوية والمقام.
- **الحد الفاصل:** قراءة بايتية وحساب SHA-256 فقط؛ لا قراءة دلالية، لا تصنيف domain، لا routing، لا نسخ مصدر، لا Terms/Claims/Concepts/Masters.
- **النتيجة:** `2,541` سجلًا في `collections/corpus/manifest.jsonl`.
- **وقت التنفيذ الفعلي UTC:** `2026-10-13T17:59:24.299708Z`.
- **`raw_changed`:** `0` أثناء التشغيل؛ قورنت لقطة pre وpost لكل مسار raw بالحجم والبصمة، ولم يتغير أي مسار.

## الملفات المرجعية المقروءة

قبل التنفيذ قُرئت هذه الملفات المرجعية المطلوبة كعقود/مقامات للعمل:

- `reports/CORPUS_INVENTORY_SCOPE_2026-10-11.md`
- `reports/FULL_DOMAIN_CATALOG_PROPOSAL_2026-10-11.md`
- `reports/CORPUS_DOMAIN_ORDER_PLAN_2026-10-11.md`
- `AGENTS.md`
- `SCHEMA.md`
- `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md`

لم تُعدّل أيًا منها. لم تُقرأ ملفات المصدر دلاليًا، ولم تُعدّل `raw/` أو طبقة المعرفة الحالية أو `config/`.

## مقام الجذور الستة

الأرقام السابقة مأخوذة من `CORPUS_INVENTORY_SCOPE_2026-10-11.md`، والأرقام الحالية قيسَت من القرص في نفس التشغيل:

| root alias | root class | الحالي: ملفات | الحالي: بايتات | الجرد المرجعي: ملفات | الجرد المرجعي: بايتات | النتيجة |
|---|---|---:|---:|---:|---:|---|
| `raw_new` | `raw_immutable` | 1,776 | 43,757,343 | 1,776 | 43,757,343 | مطابق |
| `raw_legacy_brain` | `raw_immutable` | 0 | 0 | 0 | 0 | مطابق |
| `raw_legacy_chats` | `raw_immutable` | 39 | 6,148,975 | 39 | 6,148,975 | مطابق |
| `raw_context` | `raw_immutable` | 3 | 252,610 | 3 | 252,610 | مطابق |
| `nexus_brain_brain` | `legacy_reference` | 564 | 19,680,572 | 564 | 19,680,572 | مطابق |
| `nexus_brain_nexus_vault` | `vault_reference` | 159 | 24,885,393 | 159 | 24,885,393 | مطابق |
| **الإجمالي** | — | **2,541** | **94,724,893** | **2,541** | **94,724,893** | مطابق |

حسب الطبقة:

| root_class | الملفات | البايتات |
|---|---:|---:|
| `legacy_reference` | 564 | 19,680,572 |
| `raw_immutable` | 1,818 | 50,158,928 |
| `vault_reference` | 159 | 24,885,393 |

## الهوية والتكرار

- `source_id` uniqueness: صيغة ثابتة مشتقة من `root_alias + relative_path + sha256 prefix`; **2,541/2,541 فريدة**.
- SHA-256 الكاملة: **1,937** بصمة فريدة.
- exact duplicate hash groups داخل هذه collection: **585**.
- سجلات duplicate غير الأساسية المرتبطة بـ`duplicate_of`: **604**.
- duplicate matching هو exact SHA-256 داخل هذه collection فقط؛ لا normalized/dedup دلالي.

أعلى مجموعات التكرار بعدد السجلات (البصمة الكاملة محفوظة في manifest):

| SHA-256 prefix | عدد السجلات |
|---|---:|
| `e3b0c44298fc1c14` | 6 |
| `0c124a1438d77a55` | 4 |
| `307027a7955cd7db` | 4 |
| `4524d7f6fa7e68e3` | 4 |
| `99b09401ae22e1ab` | 4 |
| `d5830007607a947d` | 4 |
| `d81487a2536aa2ec` | 4 |
| `fc703443340fea58` | 4 |
| `44136fa355b3678a` | 3 |
| `004665a1f27fd8df` | 2 |

## الملفات المفقودة/غير المقروءة

- جذور مفقودة: **0**.
- أخطاء walk/stat/read/تغير أثناء القراءة: **0**.
- symlink أو ملفات non-regular مستبعدة من مقام regular files: **0**.
- فرق نقص مقابل مقام الجرد المرجعي: **0**.
- **الخلاصة:** لا ملفات مفقودة أو غير مقروءة في هذه اللقطة؛ كل `2,541` سجلًا له حجم وبصمة.

## فحوص JSON/JSONL والمسارات

| الفحص | النتيجة المقاسة |
|---|---|
| JSONL parsing | **PASS** — `2,541` سطرًا، أخطاء JSON = `0` |
| source_id uniqueness | **PASS** — `2,541` معرّفًا فريدًا |
| source_path alias safety | **PASS** — `2,541` مسارًا alias-prefixed، بلا absolute أو `..` |
| path readability / byte hash | **PASS** — كل manifest path موجود regular وقابل للقراءة، bytes/hash match للـpost-scan |
| count/bytes مقابل الجرد | **PASS** — الجذور الستة مطابقة |
| duplicate_of integrity | **PASS** — الروابط إلى primary من نفس البصمة |
| registration-only fields | **PASS** — status registered، semantic_read false، primary_domain null، disposition unclassified |
| raw pre/post | **PASS** — `raw_changed=0` |

فشل/ملاحظات validator: `jsonl_errors=0`، `record_errors=0`، `changed_paths_all_roots=0`.

## سجل الأوامر والنتائج

1. قراءة الملفات المرجعية أعلاه عبر قارئ الملفات: **PASS**.
2. ماسح Python inline استخدم `os.walk(..., followlinks=False)`، `lstat`، قراءة binary chunks، و`hashlib.sha256`؛ كتب فقط `collections/corpus/README.md`, `manifest.jsonl`, `INDEX.md`، وهذا التقرير، والـcheckpoint تحت جذر الويكي: **PASS**.
3. إعادة scan/hash كاملة بعد إنشاء manifest للمقارنة pre/post: **PASS**؛ `raw_changed=0`.
4. Validator JSONL/uniqueness/path/hash/count/duplicate/registration fields: **PASS** بالأرقام أعلاه.
5. `lsp_diagnostics` لـ`collections/corpus/README.md` و`collections/corpus/INDEX.md` و`reports/corpus-ingest-2026-10-11.md` و`checkpoints/CORPUS_INGEST_2026-10-11.md`: **PASS** — `No diagnostics found. All clean!` لكل ملف.

## معنى الحالة والقيود

- `registered` هنا حالة collection، وليست `Source.status` في `SCHEMA.md` ولا `route_done`.
- `semantic_read=false` مقصودة؛ EOF أو SHA-256 لا يثبت الفهم أو semantic coverage.
- لا يوجد primary domain لأي سجل، ولا يثبت هذا العمل أي domain أو subdomain أو catalog expansion.
- لا توجد نسخة من أي source في collection؛ manifest يحفظ metadata والبصمة فقط.
- المقارنة مع تقرير الجرد تثبت تطابق العدد/الحجم في لقطة التنفيذ. لا توجد بصمات تاريخية لكل ملف في تقرير الجرد السابق؛ لذلك لا ندّعي عدم تغير تاريخي قبل بداية هذه العملية، بل نثبت عدم التغير أثناء pre/post التشغيل.
- collection لا تفتح domain ولا تتجاوز قفل المجال النشط أو بوابات R/T/C/K/M/QA.

## المخرجات

- [`collections/corpus/README.md`](../collections/corpus/README.md)
- [`collections/corpus/manifest.jsonl`](../collections/corpus/manifest.jsonl)
- [`collections/corpus/INDEX.md`](../collections/corpus/INDEX.md)
- [`checkpoints/CORPUS_INGEST_2026-10-11.md`](../checkpoints/CORPUS_INGEST_2026-10-11.md)
