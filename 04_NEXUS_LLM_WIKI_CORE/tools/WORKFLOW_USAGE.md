# `wiki_workflow.py` — دليل التشغيل الآمن

هذه الأداة تفصل بين **intake/routing** وبين صناعة المعرفة. كل أمر قراءة أولًا،
والأمر `publish` لا يكتب إلا مع العلم الصريح `--apply`. لا تشغّل الأمثلة على
`raw/` الحقيقي أثناء تطوير الاختبارات؛ الاختبارات تستخدم جذرًا مؤقتًا داخل
`tools/tests/`.

## الأوامر

من جذر الويكي:

```bash
python3 tools/wiki_workflow.py inventory
python3 tools/wiki_workflow.py status
python3 tools/wiki_workflow.py validate-batch --manifest staging/manifests/example.json
python3 tools/wiki_workflow.py publish --manifest staging/manifests/example.json
python3 tools/wiki_workflow.py publish --manifest staging/manifests/example.json \
  --reviewer-report reports/sales-proof/independent-review.json --apply
```

كل مخرجات CLI JSON. يمكن تمرير `--vault` لجذر اختبار آخر داخل مساحة الويكي.
`inventory` و`status` و`validate-batch` لا تكتب شيئًا. `publish` بدون `--apply`
dry-run ويعيد خطة المسارات فقط. لا يُشغّل هذا الدليل أو الاختبارات على corpus
الحقيقي؛ لا يثبت أيًا من اكتمال domain.

### `inventory` (قراءة فقط)

يجرد الملفات تحت `new/` و`raw/new/`، ويعيد الحجم والبصمة SHA-256 وثبات الملف،
ويرفض symlink كعنصر مصدر. لا ينشئ manifest أو checkpoint أو فهرسًا، ويعيد
`writes_performed: 0`.

### `status` (قراءة config)

يقرأ فقط `config/domain_catalog.json` و`config/processing_order.json`. يعرض
الترتيب، `current_domain`، حالة القفل، وحالة كل domain. `processing_order.json`
هو مصدر حالة العمل؛ لا تنشئ الأداة state منافسًا.

## عقد manifest

الحد الأدنى لدفعة routing:

```json
{
  "schema_version": 1,
  "batch_id": "BATCH_20261010_01",
  "snapshot_id": "SNAP_ROUTE_01",
  "operation": "route",
  "scope_kind": "batch",
  "inventory_complete": false,
  "coverage_status": "partial",
  "entries": [
    {
      "candidate_id": "ITEM_01",
      "source_id": "SRC_20261010_example",
      "path": "new/example.txt",
      "content_hash": "sha256:<64 lowercase hex>",
      "primary_route": {
        "domain": "sales",
        "subdomain": "objection_handling",
        "rationale": "سبب مستند إلى المتن",
        "evidence_locators": ["chars 0:12"]
      },
      "coverage": {
        "view": {"unit": "unicode_codepoint", "bounds": "half_open", "start": 0, "length": 120},
        "ranges": [[0, 60], [60, 120]],
        "semantic_segments": [
          {"start": 0, "end": 120, "reader": "reader-id", "read_at": "2026-10-10T00:00:00Z", "reviewer": "reviewer-id", "reviewed_at": "2026-10-10T01:00:00Z", "note": "ملاحظة مراجعة المقطع"}
        ],
        "unread_ranges": [],
        "semantic_review_status": "reviewed"
      },
      "evidence": [
        {
          "quote_offset": {
            "unit": "unicode_codepoint",
            "start": 0,
            "end": 12,
            "bounds": "half_open"
          },
          "quote": "النص الحرفي",
          "quote_hash": "sha256:<64 lowercase hex>"
        }
      ]
    }
  ]
}
```

### فحوص `validate-batch`

لكل entry:

1. المسار نسبي، داخل جذر الويكي، بلا `..` أو backslash، والمصدر regular
   non-symlink. تقرأ الأداة كل البايتات وتقارن `content_hash` (والحجم إن وُجد).
2. `coverage` يستخدم Unicode code points وحدودًا نصف مفتوحة `[start,end)`؛ يجب
   أن يبدأ أول range عند صفر، تتصل النطاقات بلا gap أو overlap، وتنتهي عند
   `view.length == len(text)`. `unread_ranges` غير مسموحة.
3. كل مصدر له primary route واحد فقط. `route` أو `primary_route` أو `routes` لا
   يجوز أن تعرّف أكثر من route. الزوج domain/subdomain يجب أن يوجد في
   `domain_catalog.json`.
4. كل مصدر موجه يحتاج quote مع offsets Unicode code-point وبحدود نصف مفتوحة.
   تقبل الأداة أيضًا أسماء ledger الحالية `evidence_start` و`evidence_end`
   و`evidence_quote` و`excerpt_sha256`. تعيد الأداة حساب `source_text[start:end]`
   و`quote_hash` إن قدمه manifest؛ اختلاف quote أو hash، أو quote فارغ، يوقف الدفعة.
5. `source_id` لا يجوز أن يشير إلى مسارين أو بصمتين مختلفتين. تطابق البايتات
   بين هويتين يحتاج تصريح duplicate؛ لا يرفع عدد الأدلة المستقلة.
6. تغطية القراءة تحتاج `semantic_segments` متصلة، ولكل segment `reader` و`read_at`
   و`reviewer` و`reviewed_at` و`note` غير فارغة، مع أوقات timezone-aware مرتبة؛
   غياب `semantic_review_status: reviewed|complete` يوقف الدفعة.

### قفل المجال والبوابات

- routing في domain `pending` مسموح: هو نسخة وتوجيه فقط، وليس extraction.
- إذا كان `operation` هو `extraction`/`knowledge`، أو طلب manifest مخرجات
  معرفية، فلا يمر إلا للمجال الموجود في `processing_order.json` كـ
  `current_domain` وحالته `active` أو `in_progress`. extraction لمجال pending
  يفشل صراحةً بدل أن يتحول إلى quarantine.
- طلب `T` (`requested_gates: ["T"]` أو `domain_terms_complete`) لا يمر من
  `scope_kind: batch` أو `subset`. يلزم snapshot شامل صريح: `scope_kind` من
  نوع `domain_snapshot`، `inventory_complete: true`، تغطية `complete/closed`،
  كل subdomains في catalog، كل candidate IDs، و`unresolved_candidates: []`.
- طلب `master` له نفس شرط snapshot، ويحتاج كذلك `t_gate_status: "pass"` أو
  `t_gate_passed: true`. لا ينشئ `publish` Masterًا ولا يرفع domain state؛ هذه
  guards فقط.

## `publish --apply` والمراجع المستقل

قبل أول كتابة يعاد تشغيل validation وتلزم وثيقة JSON مستقلة عبر
`--reviewer-report`:

```json
{
  "report_type": "independent_reviewer",
  "independent": true,
  "decision": "pass",
  "reviewer": "reviewer-id",
  "validation_ok": true,
  "manifest_sha256": "sha256:<hash of manifest bytes>",
  "reviewed_at": "2026-10-11T00:00:00Z"
}
```

يجب أن تكون الوثيقة regular non-symlink داخل جذر الويكي، وأن تطابق بصمة ملف
manifest حرفيًا، وأن يعلن manifest هوية `author` مختلفة عن `reviewer` حتى يكون
الاستقلال قابلاً للفحص. بعد ذلك فقط تفحص الأداة الوجهات، ولا تسمح بأي symlink أو
hardlink أو artifact زائد أو مختلف يمكن أن يؤدي إلى overwrite. الوجهة المباشرة
لكل route هي:

```text
done/<domain>/<subdomain>/
  <source_id>.<original-extension>
  REF_<source_id>.json
  ROUTE_<source_id>.md
  INDEX.md
```

النسخة تُكتب بإنشاء حصري، ثم تُفحص بالـSHA-256 والحجم و`(st_dev, st_ino)`
وبـ`st_nlink`. الأصل لا يُعدل ولا يُنقل. `REF` و`ROUTE` يثبتان
`route_done` و`source_extraction_status: not_started` فقط؛ الفهرس يصرح بأن
`source_done` وT/M و`domain_done` غير مثبتة.

إذا فشلت الكتابة بعد إنشاء artifact، لا تنفذ الأداة حذفًا أو rollback صامتًا؛
تعيد `partial_write: true` والمسارات التي كُتبت لتتم مراجعتها يدويًا. وفي
التشغيل الطبيعي يمنع preflight التعارض قبل أول كتابة. إذا كانت وجهة
`done/domain/subdomain` موجودة، فلا تُستبدل: تُقبل الإعادة فقط إذا أثبتت الأداة أن
كل النسخ وREF/ROUTE/INDEX مطابقة للدفعة الحالية، وتعيد `already_published: true`
و`writes_performed: 0`.

## الاختبارات

```bash
python3 -B -m unittest discover -s tools/tests -p 'test_*.py' -v
```

الاختبارات تغطي dry-run وعدم الكتابة، النسخة الفعلية مع reviewer مستقل، تصادم
الهوية/البصمة، Unicode coverage وreview metadata وgap/overlap، exact evidence
بأسماء الحقول الحالية، pending extraction، ورفض T/M من subset، preflight الدفعة،
و`partial write` وإعادة النشر idempotent. اختبارات symlink/hardlink
**capability-aware**: تحاول الاختبارات إنشاء الرابط الفعلي، وتُسجّل `SKIP` صريحًا
مع نوع خطأ النظام إذا كان الـfilesystem يمنع إنشاءه؛ وعندها يبقى اختبار مستقل
دائم التشغيل يحقن metadata مكافئة عبر `lstat` ويثبت رفض path/link metadata بلا
إنشاء رابط. الـ`SKIP` قيد بيئي وليس PASS للمنصة، ولا يُخفى بفشل أو نجاح اصطناعي.
لا تعني خضرة الاختبارات فحص corpus أو اكتمال أي domain.
