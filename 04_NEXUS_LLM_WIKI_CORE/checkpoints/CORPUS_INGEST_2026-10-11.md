# Checkpoint — CORPUS_INGEST_2026-10-11

## العملية

- **المعرّف:** `CORPUS_INGEST_2026-10-11`
- **نوعها:** public corpus collection registration / identity-only
- **الحالة:** `registration_complete`; ليست semantic coverage وليست domain completion.
- **وقت التنفيذ UTC:** `2026-10-13T17:59:24.299708Z`
- **الجذور:** ستة aliases في `collections/corpus/README.md`.

## المخرجات المنشأة

- `collections/corpus/README.md`
- `collections/corpus/manifest.jsonl`
- `collections/corpus/INDEX.md`
- `reports/corpus-ingest-2026-10-11.md`
- `checkpoints/CORPUS_INGEST_2026-10-11.md`

## القياسات المثبتة

- records: **2,541**.
- bytes: **94,724,893**.
- unique SHA-256: **1,937**.
- exact duplicate hash groups: **585**.
- duplicate records linked by `duplicate_of`: **604**.
- missing/unreadable: **0**.
- `source_id` unique: **True**.
- JSONL valid: **True**.
- counts/bytes match `CORPUS_INVENTORY_SCOPE_2026-10-11.md`: **True**.
- raw pre/post unchanged: **True** (`raw_changed=0`).
- every record remains `status=registered`, `semantic_read=false`, `primary_domain=null`, `disposition=unclassified`.

## ما لم يُنفذ

- لا قراءة دلالية أو تصنيف من متن المصدر.
- لا route أو copy إلى `done/`.
- لا Terms/Claims/Concepts/Masters، ولا بوابة T/C/K/M/QA.
- لا تعديل في `raw/` أو المعرفة الحالية أو `config/`، ولا حذف.

## الخطوة التالية المصرح بها فقط

إن قرر المالك المتابعة، يبدأ intake/route دلالي مستقل من هذا المقام مع قراءة المصدر كاملًا، أدلة موضعية، dedup قابل للتتبع، وقرار primary واحد. يجب إبقاء هذا manifest identity-only وعدم تحويل أي حقل دلالي فيه تلقائيًا.
