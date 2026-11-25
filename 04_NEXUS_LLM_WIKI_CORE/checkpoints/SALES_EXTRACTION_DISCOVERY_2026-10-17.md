# Checkpoint — SALES_EXTRACTION_DISCOVERY_2026-10-17

## الحالة

- **العملية:** استخراج Terms وcandidate Claims لمصدر واحد فقط.
- **المجال النشط:** `sales` فقط.
- **المسار:** `sales/discovery_and_sales_conversations`.
- **source_id:** `SRC_NEW_2a98697c6e73ffa1_82a4e90e`.
- **الحالة:** `candidate_only`؛ ليست `source_done` ولا `domain_terms_complete` ولا `domain_done`.
- **الدفعة:** `batch_inventory_complete=false`، وليست domain snapshot.
- **مصادر خارجية:** planner للاستكشاف فقط؛ لم تُستحضر Claims أو تعريفات من Masters، التزامًا باستخراج المصدر المحدد وحده.

## القراءة والتتبع

- المصدر الخام والنسخة المستقلة قُرئا كاملين: `14,545 / 14,545` bytes، `14,545` Unicode code points، EOF، UTF-8 strict، بلا replacements، بلا trailing newline.
- source/copy SHA-256: `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047` لكليهما، والنسخة byte-exact مستقلة وفق REF/ROUTE.
- `read_coverage_ref`: `READ_SALES_EXTRACTION_20261017_DISCOVERY_SRC_NEW_2a98697c6e73ffa1_82a4e90e`.
- extraction snapshot: `SALES_EXTRACTION_SNAPSHOT_20261017_DISCOVERY`؛ single-source فقط وليست domain snapshot.
- المقاطع: `[0,4848) + [4848,9696) + [9696,14545)`؛ اتحاد متصل كامل، `unread_ranges=[]`.

## النتائج

- Terms مرشحة: **47**.
- Claims مرشحة: **26**.
- الدليل: `direct_quote=20`, `reported_result=2`, `example=4`, `inference=0`, `hypothesis=0`.
- كل Claim يحمل statement عربيًا ذريًا، evidence type، source_id، locator/start/end، quote/hash، scope، confidence، `status=candidate`، و`what_it_does_not_prove`.
- كل Term يحمل source_label، definition أو definition_gap، scope، occurrences وUnicode offsets/hash، و`status=candidate`.

## تحقق منفذ

- `python3 -m json.tool` على artifact: **PASS**.
- verifier مستقل للـquote slices/hashes: **PASS — 87 term occurrence slices/hashes و26 Claim slices/hashes**.
- verifier للتغطية والعدادات والمراجع: **PASS — اتحاد `[0,14545)` بلا gaps/overlaps، والعدادات 47/26 متطابقة**.
- `tools/wiki_quality.py --json`: **PASS** في الإعادة بمهلة 300s (`ok=true`، بلا أخطاء؛ فحص مساعد لا يثبت وحده بوابات T/C/K/M/QA). محاولة متوازية أولى بمهلة 120s انتهت بمهلة الأداة ثم نجحت الإعادة.
- `lsp_diagnostics` على JSON: **clean — No diagnostics found**.
- raw selected-source hash unchanged: **مطابق لسجل REF/ROUTE pre/post**.
- بصمات `collections/sales/manifest.json` و`collections/corpus/manifest.jsonl` و`config/domain_catalog.json`: **مطابقة للسجلات السابقة**.
- ملفات shared (`term_inventory.json`، `full_evidence_ledger.jsonl`، وكل INDEX): **لم تُعدّل**.
- Concepts/Masters/Claims النهائية: **لم تُنشأ**؛ ملفات candidate داخل artifact فقط.

## الملفات الخاصة فقط

1. `collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_DISCOVERY.json`
2. `reports/sales-extraction-discovery-2026-10-17.md`
3. `checkpoints/SALES_EXTRACTION_DISCOVERY_2026-10-17.md`

## قيد الاستلام

هذه مساهمة مصدر واحدة مرشحة. لا ترفع حالة المصدر أو المجال، ولا تعتبر `source_done` أو `domain_terms_complete`.
