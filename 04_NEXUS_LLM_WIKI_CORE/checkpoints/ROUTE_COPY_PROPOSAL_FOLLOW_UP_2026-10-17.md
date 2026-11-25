# Checkpoint — ROUTE_COPY_PROPOSAL_FOLLOW_UP_2026-10-17

## العملية والحالة

- **المهمة:** route + copy فقط للمصدر `SRC_NEW_34aaffac87a9dd7f_0535de17`.
- **النطاق:** `sales/proposal_follow_up_pipeline`، مصدر واحد.
- **الحالة:** `route_done` للنسخ وmetadata؛ `source_extraction_status=not_started`.
- **workflow_id:** `WF_20261017_route_copy_proposal_follow_up`.
- **المراجعة:** `worker-self-check`؛ لا توجد مراجعة مستقلة في هذه المهمة.
- **snapshot scope:** `SNAP_SALES_BATCH_2026-10-11_001` بمعنى batch فقط؛
  `inventory_complete=false`.

## الملفات المقروءة

- `/sdcard/NEXUS_LLM_WIKI/AGENTS.md`
- `/sdcard/NEXUS_LLM_WIKI/SCHEMA.md`
- `/sdcard/NEXUS_LLM_WIKI/systems/14_SOURCE_ROUTING_AND_DONE_TREE.md`
- `/sdcard/NEXUS_LLM_WIKI/config/domain_catalog.json`
- `collections/sales/reading/SALES_BATCH_2026-10-11_001.json` كاملًا
- المصدر الخام كاملًا من `raw/new/...DhzsNovGxgM.txt`
- سجل Source الحالي، manifest sales، classification، staging reference، وفهارس
  duplicate ذات الصلة للتحقق المساعد والهوية.

المصدر في reading batch لم يُعامل كبديل عن إعادة التحقق: أُعيد حساب البصمة
والحجم وEOF ومواضع الاقتباس من الملف الخام نفسه.

## المخرجات

1. `done/sales/proposal_follow_up_pipeline/SRC_NEW_34aaffac87a9dd7f_0535de17.txt`
2. `done/sales/proposal_follow_up_pipeline/REF_SRC_NEW_34aaffac87a9dd7f_0535de17.json`
3. `done/sales/proposal_follow_up_pipeline/ROUTE_SRC_NEW_34aaffac87a9dd7f_0535de17.md`
4. تحديث `done/sales/proposal_follow_up_pipeline/INDEX.md` المحلي فقط.
5. `reports/route-copy-proposal-follow-up-2026-10-17.md`
6. هذا الـcheckpoint.

لم تُنشأ Terms أو Claims أو Concepts أو Masters، ولم يُنشأ Source record جديد.

## القياسات

| القياس | القيمة |
|---|---|
| المصدر bytes | `70,159` |
| المصدر UTF-8 code points | `70,159` |
| lines | `1`؛ بلا newline نهائي |
| EOF / strict decode | PASS / PASS |
| decode replacements | `0` |
| المصدر SHA-256 | `34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d` |
| النسخة bytes | `70,159` |
| النسخة SHA-256 | مطابق تمامًا |
| regular copy | `true` |
| symlink | `false` |
| hardlink | `false` |
| same inode | `false` |
| read coverage | `[0,23386)+[23386,46772)+[46772,70159)`، بلا فجوات |
| primary route | `sales/proposal_follow_up_pipeline`, confidence `medium` |
| secondary route | `outreach/outreach_mechanics_and_follow_up`, bounded |
| independent evidence count | `1`؛ corpus/legacy references غير مستقلة |

## raw pre/post وحراس عدم التعديل

جرد `raw/new` قبل وبعد باستخدام `os.walk(followlinks=False)` و`lstat` وSHA-256
لكل regular file:

```text
files: 1776
bytes: 43757343
tree_sha256: 571243cdbc520c67961627bcd76e73ead52f2579492dbf7bfd638450602a5140
```

القيمة نفسها قبل وبعد. كذلك بقيت الملفات المحمية التالية بلا تغيير:

| الملف | SHA-256 قبل وبعد |
|---|---|
| `collections/corpus/manifest.jsonl` | `aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3` |
| `config/domain_catalog.json` | `3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add` |
| `done/sales/INDEX.md` parent | `d8939a1afed2e29b1c8ec2b97fc43749fa482fdb8b04513bc50228983233314f` |
| `reports/INDEX.md` parent | `0e2c64cf9057d4754cb5ba76bfec5787bd229d5c35fbff65e1be06d881b8698e` |

لا تُعد الويكي Git repository؛ لم يُستخدم Git كدليل عدم تغيير. الدليل هو قياس
القرص قبل/بعد. لا يوجد أي تعديل في raw أو corpus manifest أو config أو parent
indexes.

## الفحوص الفعلية

- Python strict read/stat/reread/EOF/SHA: **PASS**.
- Python copy verifier: **PASS** للـbyte equality وSHA والحجم وregular/lstat
  وsymlink/hardlink/same-inode.
- Python REF verifier: **PASS**؛ JSON parse، أربع primary quote slices،
  locators الثانوية، segments المتصلة، والحالات النهائية.
- route G0–G8: **PASS** ضمن نطاق route + copy؛ G4 self-check لا independent
  review.
- `python3 tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json`:
  **PASS** برمز خروج 0، `ok=true`، `errors=[]`، counts: sources=1,781،
  claims=1,777، concepts=34، masters=1. هذا فحص بنيوي مساعد ولا يثبت
  استقلال نسخة `done/` أو quote offsets أو G0–G8 أو source_done؛ الأعداد
  السابقة موجودة ولم تُنشأ في هذه المهمة.

## القيود والخطوة التالية

- `route_done` لا يعني `source_done` أو `domain_done` ولا يفتح استخراج domain
  pending؛ الاستخراج بقي `not_started`.
- batch reading سابق ليس snapshot كاملة؛ لا توجد دعوى inventory completeness.
- `confidence=medium` بسبب تداخل cold-email/outreach مع pipeline/proposal/CTA؛
  حُفظ التداخل bounded بدل نسخ متعددة.
- سجل Source القديم الذي يحمل `status=processed` لم يُعدّل ولا يُعد برهانًا
  على source_done.
- الخطوة التالية تقع خارج هذا Worker: مراجعة مستقلة/اعتماد القائد ثم، إن
  أُجيز، تشغيل استخراج sales في نطاقه المقرر. لا يُستخرج شيء من هذا checkpoint
  تلقائيًا.
