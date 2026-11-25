# Checkpoint — `ROUTE_COPY_DISCOVERY_2026-10-17`

## العملية والحالة

- **العملية:** route + copy لمصدر واحد فقط.
- **source_id:** `SRC_NEW_2a98697c6e73ffa1_82a4e90e`.
- **المدخل:** `collections/sales/reading/SALES_BATCH_2026-10-11_001.json`.
- **المصدر الخام:** `raw/new/sabonagy__How to Get Your First Client A-Z Guide to Client Acquisition (Proven Steps)__FiDEMUsG6SQ.txt`.
- **primary route:** `sales/discovery_and_sales_conversations`، confidence `medium`.
- **route_status:** `route_done`.
- **source_extraction_status:** `not_started`.
- **نطاق الدفعة:** `batch_inventory_complete=false`؛ ليست snapshot كاملة ولا دليل اكتمال domain.

## ما أُنجز

1. قُرئت bytes المصدر الخام كاملة وأُعيد decode UTF-8 strict وإعادة القراءة.
2. أُعيد حساب SHA-256 والمواضع الحرفية من المصدر نفسه؛ reading batch القديم كان
   دليلًا مساعدًا فقط.
3. أُنشئت نسخة regular byte-exact مباشرة تحت المسار الأساسي.
4. أُنشئ `REF_<source_id>.json` و`ROUTE_<source_id>.md`، وحُدّث INDEX المحلي فقط.
5. أُنشئت سجلات التشغيل في `staging/routing/` (run، summary، checks).
6. أُنشئ التقرير المستقل `reports/route-copy-discovery-2026-10-17.md`.
7. لم تُنشأ Terms/Claims/Concepts/Masters، ولم يُعدّل raw أو corpus manifest أو
   config أو parent indexes المشتركة.

## القياسات المثبتة

| القياس | القيمة |
|---|---:|
| bytes expected/read | `14,545 / 14,545` |
| Unicode code points | `14,545` |
| lines / trailing newline | `1 / false` |
| decode replacements | `0` |
| source SHA-256 | `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047` |
| copy SHA-256 | مطابق تمامًا |
| copy bytes equal | `true` |
| symlink | `false` |
| hardlink / same inode | `false` |
| source dev/ino → copy dev/ino | `(169,1997006) → (169,2032083)` |
| read segments | `[0,4848) + [4848,9696) + [9696,14545)` |
| unread ranges | `[]` |
| quote checks | `5/5 PASS` |
| staging run/summary JSON | `json.tool PASS`، entries `1`، route_done `1` |

## raw pre/post والحراس

الجرد استخدم `os.walk(followlinks=False)` وصفوفًا مرتبة من
`relative_path + NUL + size + NUL + sha256 + LF` ثم SHA-256 للحمولة:

| raw/new inventory | pre | post | الحكم |
|---|---:|---:|---|
| files | `1776` | `1776` | UNCHANGED |
| bytes | `43,757,343` | `43,757,343` | UNCHANGED |
| inventory SHA-256 | `4ce12a3c7d48371333ba77367817f88d065152b09ad2106ab01cf0d32a3cff4b` | نفس البصمة | UNCHANGED |

وجرد `raw/` الكامل أيضًا مطابق: `1820` files، `50,898,163` bytes،
inventory SHA-256 `96e9ff6f6ce82ceb244f87df23097100576a8b26cf8731eacbe59b6f980c21a2`
قبل وبعد.

الملفات المحمية بقيت ببصماتها المسجلة:

- `collections/sales/manifest.json`: `1c729810fbc2ca115e7cf55a17fe4a891eea62f63195c7304182622efee92923`.
- `collections/corpus/manifest.jsonl`: `aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3`.
- `config/domain_catalog.json`: `3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add`.
- المصدر المحدد: `2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047`.

## بوابات G0–G8

`G0 PASS` path/id · `G1 PASS` full IO/EOF/stability · `G2 PASS` source/copy
hash · `G3 PASS` dedup references documented · `G4 PASS` contiguous routing read
and quotes · `G5 PASS` catalog route · `G6 PASS` bounded secondary references ·
`G7 PASS` independent copy + REF/ROUTE · `G8 PASS` raw pre/post + local INDEX.

## مخرجات التشغيل

- `done/sales/discovery_and_sales_conversations/SRC_NEW_2a98697c6e73ffa1_82a4e90e.txt`
- `done/sales/discovery_and_sales_conversations/REF_SRC_NEW_2a98697c6e73ffa1_82a4e90e.json`
- `done/sales/discovery_and_sales_conversations/ROUTE_SRC_NEW_2a98697c6e73ffa1_82a4e90e.md`
- `done/sales/discovery_and_sales_conversations/INDEX.md` (محلي فقط)
- `staging/routing/ROUTE_RUN_20261017_DISCOVERY.json`
- `staging/routing/ROUTE_RUN_20261017_DISCOVERY_summary.json`
- `staging/routing/ROUTE_RUN_20261017_DISCOVERY_checks.md`
- `reports/route-copy-discovery-2026-10-17.md`

## القيود والمرحلة التالية

- المطابقة في `collections/corpus/manifest.jsonl` بنفس hash موثقة كمرجع لنفس
  البايتات، لا مصدر مستقل؛ مسار legacy في `raw/SOURCE_MANIFEST.tsv` stale لأن
  الملف المشار إليه غير موجود.
- سجل Source القديم بحالة `processed` لم يُعدّل، ولا يُستخدم كدليل source_done؛
  القراءة/الاستخراج الحاليان منفصلان وموسومان `not_started`.
- لا توجد مراجعة مستقلة أو بوابات T/C/K/M/QA في هذه المهمة.
- الخطوة التالية المخوّلة منفصلة: مراجعة/استخراج معرفي داخل domain النشط فقط،
  مع إبقاء هذا route والنسخة مصدر التتبع وعدم الكتابة إلى parent indexes.
