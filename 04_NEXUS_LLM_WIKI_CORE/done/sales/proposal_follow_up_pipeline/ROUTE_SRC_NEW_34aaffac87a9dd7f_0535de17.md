---
type: route_record
route_id: ROUTE_SRC_NEW_34aaffac87a9dd7f_0535de17
workflow_id: WF_20261017_route_copy_proposal_follow_up
source_id: SRC_NEW_34aaffac87a9dd7f_0535de17
source_path: raw/new/smartleadai__How to Close 500+ Sales Opps in 90 Days with David Lehnert__DhzsNovGxgM.txt
content_hash: sha256:34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d
copy_path: done/sales/proposal_follow_up_pipeline/SRC_NEW_34aaffac87a9dd7f_0535de17.txt
copy_sha256: sha256:34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d
route_status: route_done
source_extraction_status: not_started
---

# Route + copy — `SRC_NEW_34aaffac87a9dd7f_0535de17`

## الحكم والنطاق

أُنجزت قراءة توجيهية كاملة للمصدر الخام المحدد، ثم أُنشئت نسخة regular مستقلة
byte-exact في المسار المباشر. هذا السجل يثبت **route + copy فقط**؛ لا يثبت
`source_done` أو `domain_done` أو أي بوابة T/C/K/M/QA، ولا ينشئ Terms أو Claims أو
Concepts أو Masters.

المصدر القديم في `collections/sales/reading/SALES_BATCH_2026-10-11_001.json`
استُخدم كدليل مساعد لتحديد مواضع الفحص فقط. أُعيد فتح الملف الخام نفسه وحُسبت
البصمة والمواضع والاقتباسات من البايتات الموجودة على القرص قبل إغلاق هذا السجل.

## هوية المصدر وقراءة EOF

| الحقل | النتيجة المتحققة |
|---|---|
| `source_id` | `SRC_NEW_34aaffac87a9dd7f_0535de17` |
| المصدر الخام | `raw/new/smartleadai__How to Close 500+ Sales Opps in 90 Days with David Lehnert__DhzsNovGxgM.txt` |
| الحجم المتوقع/المقروء | `70,159 / 70,159` bytes |
| UTF-8 code points | `70,159` |
| الأسطر | `1`، بلا newline نهائي |
| EOF | PASS |
| إعادة القراءة | `bytes_equal_on_reread=true`, `stable_after_read=true` |
| decode replacements | `0` |
| SHA-256 المعاد حسابه | `sha256:34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d` |
| SHA-256 المسجل في batch/Source | مطابق؛ استُخدم للمقارنة لا كبديل عن إعادة القراءة |

القراءة الدلالية التوجيهية تغطي كامل view المتصل بوحدة Unicode code points
وبحدود نصف مفتوحة `[start,end)`:

| segment | البداية | النهاية | النطاق |
|---|---:|---:|---|
| `SEG_ROUTE_COPY_20261017_0535de17_01` | 0 | 23,386 | غرض الجلسة، الفرص، pipeline، والأدوات والسياق الأولي |
| `SEG_ROUTE_COPY_20261017_0535de17_02` | 23,386 | 46,772 | القائمة والتأهيل وجهات الاتصال وبنية الرسالة وproposal/CTA |
| `SEG_ROUTE_COPY_20261017_0535de17_03` | 46,772 | 70,159 | التخصيص وdeliverability والردود والحدود والأسئلة |

الاتحاد هو `[0,70159)` بلا فجوة أو overlap، و`unread_ranges=[]`. هذه تغطية
توجيهية فقط؛ `content_units=[]` و`extraction_status=not_started` عمدًا.

## القرار الأساسي

```text
primary domain:       sales
primary subdomain:    proposal_follow_up_pipeline
confidence:           medium
route_status:         route_done
```

الغرض الغالب في المتن هو شرح نظام توليد الفرص وبناء pipeline ثم تحويل الردود
إلى مكالمات ومسار عرض وCTA. توجد تفاصيل كثيرة عن cold email والأدوات والتأهيل
والرسائل، لكنها سياق داعم وإحالة ثانوية إلى outreach؛ لم تُنشأ نسخة ثانية.

### أدلة التصنيف من المتن

المواضع صفرية البداية، نصف مفتوحة، بوحدة Unicode code points، و`line 1` مساعد
لأن المصدر كله سطر واحد:

| العائلة | locator | الاقتباس الحرفي | دلالة القرار |
|---|---|---|---|
| purpose | `chars 1452:1686; line 1` | “And today's session is super interesting because David is going to break down the exact systems, copies, tools, and workflows that helped him generate 521 opportunities and a $2 million pipeline without spending on ads or hiring HDRs.” | يثبت أن غرض الجلسة يدور حول توليد الفرص وبناء pipeline؛ النتيجة منسوبة للمقدّم وليست تحققًا مستقلًا. |
| actions | `chars 37960:38215; line 1` | “And it's sets also the stage again for the next one for the solution and for the proposal. Yeah. Right. And then we we show them the remedy. Yeah. We show them the way out of the situation that might be very painful. And then we we we have the CTA. Yeah. ” | يثبت تسلسل المشكلة ثم الحل والعرض والـCTA داخل مسار الرسالة. |
| structure | `chars 13900:13932; line 1` | “every table just has one purpose” | يثبت modular workflow لخطوات النظام. |
| structure | `chars 46416:46469; line 1` | “it's going to be hook, pain, proof, remedy, and a CTA” | يثبت بنية رسالة مذكورة في المصدر، لا قاعدة عامة مثبتة. |

أُعيد فحص كل slice أعلاه على النص الخام، وحُفظت `quote_sha256` و`quote_offset`
في `REF_SRC_NEW_34aaffac87a9dd7f_0535de17.json`.

## الإحالة الثانوية والتكرار

الإحالة الثانوية الوحيدة هي:

```text
outreach / outreach_mechanics_and_follow_up
```

سببها أن المتن يشرح بناء قوائم cold email والبحث عن جهات الاتصال والرسائل
وdeliverability ومعدلات الرد. المواضع الداعمة هي `chars 9755:10136` و
`chars 49784:49882`؛ الإحالة تحمل نفس `source_id` ومرجع المسار الأساسي ولا
تضاعف الدليل ولا تنشئ copy ثانية.

فحص التكرار وجد مراجع بصمة مطابقة غير مستقلة:

1. `collections/corpus/manifest.jsonl:1406` يسجل نفس المحتوى تحت
   `SRC_CORPUS_raw_new_34aaffac87a9dd7f_6f8e239dbeeb` وبصيغة مسار `raw_new`؛
   هذا تسجيل corpus لنفس الملف وليس دليلًا مستقلًا.
2. `raw/SOURCE_MANIFEST.tsv:4964` يشير إلى مسار legacy قديم بالبصمة نفسها؛
   `raw/legacy/brain` كان خاليًا في جرد ما قبل/بعد التشغيل، لذا عومل المرجع
   كـ`stale_reference` لا كملف ثانٍ.

لذلك `duplicate_of=null` للمصدر المطلوب، و`independent_evidence_count=1`.

## النسخة المستقلة والتحقق

النسخة المباشرة هي:

```text
done/sales/proposal_follow_up_pipeline/SRC_NEW_34aaffac87a9dd7f_0535de17.txt
```

نتيجة التحقق الفعلية:

| الفحص | النتيجة |
|---|---|
| bytes الأصل/النسخة | `70,159 / 70,159` — PASS |
| SHA-256 الأصل | `sha256:34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d` |
| SHA-256 النسخة | مطابق تمامًا — PASS |
| regular file الأصل/النسخة | `true / true` |
| symlink الأصل/النسخة | `false / false` |
| hardlink / same inode | `false / false` |
| link count الأصل/النسخة | `1 / 1` |
| overwrite | لم يكن destination موجودًا؛ أُنشئت النسخة بـ `O_EXCL` |
| الأصل بعد النسخ | الحجم والبصمة وinode ثابتة — PASS |

## بوابات R المحلية G0–G8

| البوابة | النتيجة | الدليل |
|---|---|---|
| G0 الهوية والمسار | PASS | `source_id` ثابت، والمسارات نسبية traversal-free |
| G1 سلامة IO | PASS | قراءة كاملة، EOF، `70159 == 70159`، UTF-8 strict، replacements=0، stable/reread equal |
| G2 البصمة | PASS | SHA-256 الخام والنسخة مطابقان للمقارنة المسجلة |
| G3 التكرار | PASS مع مراجع غير مستقلة موثقة | لا نسخة مستقلة ثانية؛ corpus registration وlegacy stale reference محفوظان في REF |
| G4 القراءة والصلة | PASS للتوجيه | segments متصلة تغطي `[0,70159)`، والاقتباسات تطابق offsets؛ self-check وليس مراجعة مستقلة |
| G5 المسار الأساسي | PASS | زوج واحد صالح في catalog: `sales/proposal_follow_up_pipeline` |
| G6 المراجع الثانوية | PASS | إحالة واحدة bounded بسبب ومواضع، بلا copy ثانية |
| G7 النسخة والmetadata | PASS | regular byte-exact copy + REF + ROUTE، hashes/bytes/symlink/hardlink متحققة |
| G8 الخام والفهرس المحلي | PASS | raw pre/post متطابقان، وINDEX المحلي يذكر النسخة والmetadata؛ parent indexes لم تُمس |

`route_status=route_done` هنا يعني اكتمال التوجيه والنسخة وmetadata فقط.
أما `source_extraction_status=not_started` فمتعمد، ولا توجد أي ملفات أو سجلات
Terms/Claims/Concepts/Masters منشأة في هذه المهمة.

## القيود والحدود

- `SNAP_SALES_BATCH_2026-10-11_001` هو نطاق batch؛ `inventory_complete=false`.
  هذه العملية لا تدّعي snapshot كاملة ولا `domain_done`.
- `confidence=medium` لأن المصدر يجمع outreach كثيفًا مع pipeline/offer/CTA؛
  استُخدم primary المطلوب المدعوم بالمتن مع bounded secondary بدل نسخ متعددة.
- نتيجة 521 فرصة و$2 million pipeline، ومعدلات الرد، أقوال منسوبة داخل المصدر؛
  لم تُحوّل إلى Claims ولم تُعامل كتحقق مستقل.
- سجل Source القديم `status=processed` لم يُعدّل، ولا يُعامل وحده كدليل
  `source_done`. سجل القراءة القديم أداة مساعدة فقط؛ إعادة التحقق الحالي هو
  أساس هذا route artifact.
- لم تُعدّل `raw/` أو `collections/corpus/manifest.jsonl` أو أي config أو
  parent index مشترك. لا توجد Terms/Claims/Concepts/Masters جديدة.
- لا توجد مراجعة مستقلة من Reviewer في هذه المهمة؛ `worker-self-check` موثق
  صراحةً في REF والـcheckpoint.

## المخرجات

| الملف | الوظيفة |
|---|---|
| `SRC_NEW_34aaffac87a9dd7f_0535de17.txt` | النسخة regular byte-exact الإلزامية |
| `REF_SRC_NEW_34aaffac87a9dd7f_0535de17.json` | route/reference metadata والبصمات والتغطية |
| `ROUTE_SRC_NEW_34aaffac87a9dd7f_0535de17.md` | قرار التوجيه وفحوص G0–G8 |
| `INDEX.md` | الفهرس المحلي للمجلد، دون تعديل فهرس parent مشترك |
