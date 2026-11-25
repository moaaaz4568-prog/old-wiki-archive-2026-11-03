# Route `SRC_NEW_b0140a4d41654bab_b1f4775a`

- `route_status`: `route_done`
- `source_extraction_status`: `not_started`
- `source_id`: `SRC_NEW_b0140a4d41654bab_b1f4775a`
- `source_path`: `raw/new/matthewlucero__The Best Way To Book High-Ticket Sales Calls in 2026__Kx3ZSv2NqVQ.txt`
- `content_hash`: `sha256:b0140a4d41654babf5ec880c63fa0da5e68ff72a8a2e5611a4b5652b31bb0d54`
- `primary_route`: `sales/high_ticket_closing`
- `confidence`: `medium`
- `workflow_id`: `WF_20261017_route_copy_high_ticket`
- `snapshot_id`: `ROUTE_SNAPSHOT_20261017_HIGH_TICKET` (single-source route batch; ليس snapshot إغلاق للمجال)
- `reviewer`: `worker-self-check`
- `independent_reviewer_report`: غير مُدّعى في هذه المهمة

## حدود هذا الملف

هذا سجل توجيه ونسخ والتحقق من التتبع فقط. لا يمثل Claim أو Term أو Concept أو
Master، ولا يثبت `source_done` أو `domain_terms_complete` أو `domain_done`. بقيت
كل طبقات المعرفة الناتجة عن المصدر خارج هذه المهمة.

## قرار التوجيه من متن المصدر

الغرض الغالب الذي ظهر من القراءة الكاملة هو حجز مكالمات مبيعات عالية القيمة ثم
تحويل العملاء المحتملين عبر عملية مبيعات تتضمن التأهيل والاكتشاف ومعالجة
الاعتراضات. لذلك اختير المسار الأساسي `sales/high_ticket_closing`. يظهر cold
email بوصفه قناة وصول وحجز وسياقًا للحملات؛ لذلك أُدرجت إحالة ثانوية bounded إلى
`outreach/cold_email_and_message_systems` دون نسخة ثانية أو عدٍّ مستقل للدليل.

المواضع صفرية البداية بوحدة Unicode code point وبحدود نصف مفتوحة `[start,end)`؛
المصدر كله في السطر 1.

| عائلة الدليل | locator | الاقتباس الحرفي | وظيفة الدليل |
|---|---|---|---|
| purpose | `chars 0:210` | `Over the last 3 years, I have booked over 4,000 sales calls for myself and for my clients using one of the most consistent engines for producing high quality sales calls, and that is none other than cold email.` | يحدد الغرض العملي في sales calls، مع cold email كقناة. |
| scope | `chars 914:1013` | `So the businesses cold email actually works for are mainly B2B businesses. There's rare exceptions.` | يحدد سياق الجمهور للقناة، لا ملكية المصدر وحدها. |
| structure | `chars 6053:6202` | `And the reality of why, you know, people think the leads aren't qualified is really just because they don't do proper discovery in the sales process.` | يثبت حضور التأهيل والاكتشاف داخل عملية المبيعات. |
| structure | `chars 6250:6286` | `They don't do any objection handling` | يثبت معالجة الاعتراضات كسياق داخل العملية. |
| secondary context | `chars 25143:25217` | `The more specific you are, the better your campaigns are going to perform.` | يبرر الإحالة السياقية إلى outreach دون جعلها primary. |

هذه الاقتباسات أدلة توجيه موضعية، وليست Claims مقبولة. لا يثبت أي منها الرقم
المذكور أو السببية أو قابلية التعميم؛ ولا يثبت اختيار cold email كمعيار عام.

## القراءة الكاملة وIO

- `bytes_expected`: 30,707؛ `bytes_read`: 30,707؛ `eof_reached`: `true`.
- إعادة القراءة: 30,707 بايت مطابقة حرفيًا؛ `stable_after_read`: `true`.
- UTF-8 strict decode: نجح؛ `decode_replacements`: `0`.
- `line_count`: `1`؛ `character_count`: `30,707`.
- `view`: Unicode code points، `[0,30707)`، وبصمة view مطابقة لبصمة البايتات.
- `unread_ranges`: `[]`.
- التغطية المتصلة: `[0,10235)` + `[10235,20471)` + `[20471,30707)`؛ بلا gap أو overlap.
- `semantic_review_status`: `reviewed` من self-check للـrouting فقط؛ لا extraction.

مرجع التغطية: `READ_ROUTE_20261017_SRC_NEW_b0140a4d41654bab_b1f4775a` داخل
`REF_SRC_NEW_b0140a4d41654bab_b1f4775a.json`، والنسخة التنفيذية في
`staging/routing/ROUTE_RUN_20261017_HIGH_TICKET.json`.

## التكرار والهوية

- أُعيدت مطابقة المصدر الحالي في `raw/new/` بالـSHA-256 والحجم؛ لا يوجد ملف raw
  آخر نشط ببصمة مطابقة.
- سجل `sources/SRC_NEW_b0140a4d41654bab_b1f4775a.md` موجود ويطابق الهوية والبصمة.
- يوجد في `raw/SOURCE_MANIFEST.tsv` سجل قديم واحد (السطر 780) للمسار
  `raw/legacy/brain/...` بالبصمة نفسها، لكن المسار غير موجود حاليًا؛ لذلك سُجل
  كـ`stale_legacy_manifest_reference` لا كنسخة مستقلة ثانية ولا كـ`duplicate_of`.
- المصدر القديم في `collections/sales/reading/SALES_BATCH_2026-10-11_001.json`
  استُخدم كدليل اختيار مساعد فقط؛ كل hash/bytes/quotes/coverage أُعيد التحقق
  منها من raw الحالي قبل إغلاق route.

## النسخة المستقلة

- النسخة المباشرة: `done/sales/high_ticket_closing/SRC_NEW_b0140a4d41654bab_b1f4775a.txt`.
- الإنشاء كان regular file بإنشاء حصري؛ لم يحدث overwrite.
- `copy_size_bytes`: 30,707؛ `copy_sha256` يساوي hash الأصل حرفيًا.
- `bytes_equal`: `true`؛ `hashes_equal`: `true`.
- الأصل regular وغير symlink؛ النسخة regular وغير symlink.
- `source_nlink=1` و`copy_nlink=1`؛ `same_inode=false`، لذلك ليست hardlink.
- `original_unchanged=true` بعد الكتابة والتحقق وإعادة القراءة.

## المراجع الثانوية

`outreach/cold_email_and_message_systems` مرجع سياقي واحد بنفس `source_id` وبنفس
المسار الأساسي. مواضعه bounded هي `chars 0:210` و`chars 914:1013` و`chars
25143:25217`. لا توجد نسخة أو evidence count مستقل لهذا المرجع.

## بوابات R المحلية

| البوابة | النتيجة | الدليل |
|---|---|---|
| G0 الهوية والمسار | PASS | source_id آمن وفريد، ومسار نسبي بلا traversal. |
| G1 سلامة IO | PASS | 30,707/30,707، EOF، UTF-8 strict، وثبات وإعادة قراءة. |
| G2 البصمة | PASS | hash المصدر مطابق للدفعة وبصمة القراءة الحالية. |
| G3 التكرار | PASS مع stale reference مرئي | لا raw hash match نشط آخر؛ manifest القديم غير موجود مسجل كقيد. |
| G4 القراءة الدلالية والصلة | PASS | segments متصلة تغطي `[0,30707)` وlocators قابلة لإعادة الفحص. |
| G5 المسار الأساسي | PASS | `sales/high_ticket_closing` موجود في catalog، primary واحد. |
| G6 المراجع الثانوية | PASS | مرجع outreach bounded بمواضع وسبب، بلا نسخة ثانية. |
| G7 النسخة والmetadata | PASS | نسخة regular byte-exact مستقلة + REF/ROUTE. |
| G8 raw والفهرسة المحلية | PASS | raw pre/post متطابقان، وINDEX المحلي محدث. |

## حالة طبقات المعرفة

- `source_extraction_status`: `not_started`.
- `term_refs`: `[]`، `claim_refs`: `[]`، `concept_refs`: `[]`، `master_refs`: `[]`.
- لا توجد ملفات Terms أو Claims أو Concepts أو Masters منشأة لهذه المهمة.
- `route_done` لا يساوي `source_done` ولا يفتح بوابات T/C/K/M/QA.

## التحقق الزمني

- `verified_at`: `2026-10-17T22:47:33Z`.
- تقرير التنفيذ المستقل: `reports/route-copy-high-ticket-2026-10-17.md`.
- Checkpoint: `checkpoints/ROUTE_COPY_HIGH_TICKET_2026-10-17.md`.
