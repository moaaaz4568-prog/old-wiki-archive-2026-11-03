# Checkpoint — SALES extraction / proposal_follow_up_pipeline — 2026-10-17

## الحالة

- **النطاق:** مصدر واحد فقط، المجال النشط `sales`، القسم
  `proposal_follow_up_pipeline`.
- **الحكم:** `candidate_only=true`؛ هذه ليست `source_done` وليست
  `source_domain_extraction_complete` أو `subdomain_extraction_done` أو
  `domain_terms_complete` أو `domain_done`.
- **الممنوع الذي لم يحدث:** لا Concepts، لا Masters، لا قبول نهائي، لا تعديل
  `term_inventory.json` أو `full_evidence_ledger.jsonl` أو أي `INDEX.md` مشترك،
  ولا استخراج لمجال `outreach` pending.

## هوية المصدر

| الحقل | القيمة |
|---|---|
| `source_id` | `SRC_NEW_34aaffac87a9dd7f_0535de17` |
| raw | `raw/new/smartleadai__How to Close 500+ Sales Opps in 90 Days with David Lehnert__DhzsNovGxgM.txt` |
| copy | `done/sales/proposal_follow_up_pipeline/SRC_NEW_34aaffac87a9dd7f_0535de17.txt` |
| SHA-256 | `sha256:34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d` |
| الحجم/الـview | `70,159` bytes و`70,159` Unicode code points |
| المصدر | سطر واحد، UTF-8، EOF وصل، بلا decode replacements |

## القراءة والتغطية

قُرئت النسخة المستقلة كاملة. سجل `read_coverage` الكامل موجود في ملف JSON
الخاص بالدفعة، مع `unread_ranges=[]` وsegments متصلة:

```text
[0,23386)       SEG_SALES_EXTRACTION_20261017_0535de17_01
[23386,46772)   SEG_SALES_EXTRACTION_20261017_0535de17_02
[46772,70159)   SEG_SALES_EXTRACTION_20261017_0535de17_03
```

الاتحاد يساوي `[0,70159)` بلا gap أو overlap. حالات القراءة هي
`semantic_review_status=reviewed` و`extraction_status=reviewed` بمعنى self-check
للمرشح؛ لا توجد مراجعة مستقلة لاحقة في هذا checkpoint.

## مخرجات الاستخراج

- `29` candidate Terms مع source labels وdefinition/definition_gap وscope،
  occurrences، quotes، Unicode offsets وquote hashes.
- `28` atomic candidate Claims مع statement عربي، source/locator/start/end،
  evidence quote/hash، scope، confidence، `status=candidate`، و
  `what_it_does_not_prove`.
- أنواع الدليل: `direct_quote=18`، `reported_result=7`، `example=3`،
  `inference=0`، `hypothesis=0`.
- أرقام المتحدث والأمثلة بقيت source-reported ومحدودة بالسياق؛ لا تعميم.
- تعارض `$2m` مقابل `$9m` للـpipeline محفوظ في `source_internal_conflicts`
  دون تسوية أو اختيار صامت.

## ملفات Worker الخاصة

1. `collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_PROPOSAL_FOLLOW_UP.json`
2. `reports/sales-extraction-proposal-follow-up-2026-10-17.md`
3. `checkpoints/SALES_EXTRACTION_PROPOSAL_FOLLOW_UP_2026-10-17.md`

## فحوص منفذة ونتائجها

شُغّل verifier مستقل بـ`python3` بعد الكتابة على ملف الدفعة، وكانت النتائج:

- `json.loads`: **PASS**.
- إعادة قص كل quotes من النسخة عبر `[start:end]`: **PASS**.
- إعادة حساب كل quote hashes: **PASS** لكل 29 Term و28 Claim و4 observations
  للتعارض.
- فحص حدود segments المتجاورة: **PASS**؛ coverage كامل.
- raw SHA-256: مطابق للبصمة المسجلة.
- copy SHA-256: مطابق للـraw.
- raw/copy bytes: متساوية.
- raw بعد الكتابة: **unchanged** (`raw_unchanged=true`).
- `lsp_diagnostics` على JSON: **clean — No diagnostics found. All clean!**
- `python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json`:
  **PASS**، exit 0 و`ok=true`؛ فحص مساعد بنيوي فقط وليس إثباتًا للقراءة
  الدلالية أو لبوابة T/C.

الدليل يثبت سلامة هذا artifact والـIO والتتبع فقط؛ لا يثبت قبولًا معرفيًا أو
اكتمالًا للمصدر أو القسم أو المجال. يحتاج الإغلاق مراجعة Commander/Reviewer
مستقلة وفق بوابات C/T وبقية البوابات، ولا يجوز تسميته `source_done` أو
`domain_terms_complete` من هذا checkpoint وحده.
