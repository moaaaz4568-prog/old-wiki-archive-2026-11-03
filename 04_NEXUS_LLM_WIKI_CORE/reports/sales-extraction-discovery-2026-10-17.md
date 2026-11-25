# تقرير استخراج مرشّح — sales / discovery_and_sales_conversations — 2026-10-17

## الحكم والنطاق

هذه دفعة استخراج معرفي **لمصدر واحد فقط** داخل المجال النشط المسموح `sales`، ومسارها الأساسي `sales/discovery_and_sales_conversations`. كل ما في الدفعة مرشح (`candidate`) ولم يُقبل نهائيًا. لا تمثل هذه الدفعة `source_done`، ولا `source_domain_extraction_complete`، ولا `domain_terms_complete`، ولا `domain_done`.

لم تُنشأ Concepts أو Masters، ولم تُكتب أي نتيجة إلى `collections/sales/term_inventory.json` أو `collections/sales/full_evidence_ledger.jsonl` أو أي INDEX مشترك.

شُغّل `planner.py` للاستكشاف فقط وفق تعليمات Nexus Brain، ولم تُستحضر Claims أو تعريفات من Master خارجي؛ لأن هذه الدفعة source-only وتستخرج ما يثبته النص المحدد فقط.

## هوية المصدر والقراءة

| الحقل | النتيجة |
|---|---|
| `source_id` | `SRC_NEW_2a98697c6e73ffa1_82a4e90e` |
| النسخة المقروءة | `done/sales/discovery_and_sales_conversations/SRC_NEW_2a98697c6e73ffa1_82a4e90e.txt` |
| الخام المقارن | `raw/new/sabonagy__How to Get Your First Client A-Z Guide to Client Acquisition (Proven Steps)__FiDEMUsG6SQ.txt` |
| الحجم | `14,545` bytes |
| Unicode | `14,545` code points، سطر واحد، بلا trailing newline |
| source SHA-256 | `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047` |
| copy SHA-256 | مطابق تمامًا |
| `read_coverage_ref` | `READ_SALES_EXTRACTION_20261017_DISCOVERY_SRC_NEW_2a98697c6e73ffa1_82a4e90e` |
| extraction snapshot | `SALES_EXTRACTION_SNAPSHOT_20261017_DISCOVERY` (single-source only; not a domain snapshot) |
| التغطية | `[0,4848) + [4848,9696) + [9696,14545) = [0,14545)` |
| unread ranges | `[]` |

تمت قراءة النص كاملًا بترميز UTF-8 strict بلا decode replacements. المقاطع الثلاثة متجاورة، بحدود Unicode code point نصف مفتوحة، وتغطي النص كله. `semantic_review_status=reviewed` هو self-check للعامل، بينما `extraction_status=in_progress` لأن هذه Terms/Claims مرشحة ولم تمر بمراجعة قبول مستقلة.

## المخرجات المرشحة

- Terms مرشحة: **47**.
- Claims مرشحة: **26**.
- `direct_quote`: **20**.
- `reported_result`: **2**.
- `example`: **4**.
- `inference`: **0**؛ لم يُنشأ استنتاج إضافي كي لا يتجاوز النص.
- `hypothesis`: **0**.

لكل Term `source_label` كما ورد في النص، ومواضع occurrences، وquote slice/hash. حيث قدّم المصدر وصفًا تشغيليًا أوليًا حُفظ في `definition` مع attribution واضح؛ وحيث لم يقدّم تعريفًا مستقلًا حُفظ `definition_gap` بدل التخمين.

لكل Claim: صياغة عربية ذرية، `evidence_type` من الـschema، المصدر والموضع و`evidence_start/evidence_end`، اقتباس حرفي، `quote_hash`، scope، confidence، `status=candidate`، وحدود صريحة في `what_it_does_not_prove`.

## فصل نوع الدليل والحدود

- `direct_quote`: تصريحات المصدر وتعريفاته وتوصياته حُفظت منسوبة للمصدر، لا كحقائق خارجية.
- `reported_result`: أرقام الحضور `90%` و`60%` حُفظت كنتائج/توصيفات منسوبة، مع عدم تعميمها.
- `example`: مثال ألف بريد وتوقيت رسائل التذكير ومخرجات النظام بقيت أمثلة محدودة؛ لا تحول إلى benchmark أو وصفة عامة.
- `inference`: صفر؛ لم أستنتج قواعد من ترتيب الخطوات أو من الأمثلة.
- الوعد الشخصي بالتوقيع خلال أسبوع حُفظ كاقتباس ترويجي مرشح، لا كنتيجة مثبتة.
- عتبات مثل `$200/day` و`6–12 months` و`20–30%` و`40–50k/month` لم تُحوّل إلى قواعد عامة؛ تظهر فقط حيث كان يلزم حفظ term أو سياق bounded.

## سلامة المصدر والملفات المشتركة

- hash الخام الحالي يطابق hash `REF` و`ROUTE` المسجلين (`sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047`)، والنسخة المطابقة byte-exact؛ `bytes_equal=true`، و`symlink=false`، و`hardlink=false` حسب المرجع.
- لم يتغير المصدر الخام أثناء هذه المهمة بحسب تطابق hash المصدر المحدد مع سجل pre/post الموجود في `REF_SRC_NEW_2a98697c6e73ffa1_82a4e90e.json`.
- بصمات الحراس المشتركة الحالية تطابق السجلات السابقة: `collections/sales/manifest.json`، و`collections/corpus/manifest.jsonl`، و`config/domain_catalog.json`؛ لم تُكتب هذه الملفات.
- الملفات المنشأة الوحيدة هي:
  1. `collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_DISCOVERY.json`
  2. `reports/sales-extraction-discovery-2026-10-17.md`
  3. `checkpoints/SALES_EXTRACTION_DISCOVERY_2026-10-17.md`

## أوامر التحقق ونتائجها

- `python3 -m json.tool collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_DISCOVERY.json`: **PASS**.
- verifier مستقل inline أعاد فحص `raw[start:end] == quote` وSHA-256 لكل occurrence وClaim: **PASS — 87 term occurrence slices/hashes و26 Claim slices/hashes**.
- verifier التغطية أعاد فحص اتحاد المقاطع، الفراغات، العدادات، ومراجع Claims: **PASS — [0,14545) بلا gaps/overlaps**.
- `python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json`: **PASS** في الإعادة بمهلة 300s (`ok=true`, بلا أخطاء؛ فحص مساعد للويكي الحالية، ولا يثبت وحده schema هذا الـJSON أو بوابات T/C/K/M/QA). محاولة متوازية أولى بمهلة 120s انتهت بمهلة الأداة، ثم نجحت الإعادة.
- `lsp_diagnostics` على ملف JSON: **clean — No diagnostics found**.
- فحص hash المصدر والنسخة والحراس: **PASS**؛ raw المحدد يطابق `REF/ROUTE`، و`collections/sales/manifest.json` و`collections/corpus/manifest.jsonl` و`config/domain_catalog.json` تطابق البصمات المسجلة.

## عدم الإغلاق

هذه ليست `source_done`: قد توجد وحدات/قرارات مراجعة لاحقة خارج هذا التسليم، ولا توجد مراجعة مستقلة. كما أن الدفعة ليست snapshot شاملة للمجال؛ لذلك لا تسمح بإعلان اكتمال مصطلحات sales أو إنشاء Master. أي دمج لاحق في السجلات المشتركة يتطلب مراجعة مستقلة وفحوص البصمة والاقتباسات والبوابات المناسبة.
