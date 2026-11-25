# تقرير استخراج مرشّح — `SRC_NEW_b0140a4d41654bab_b1f4775a`

**التاريخ التشغيلي:** 2026-10-17  
**المجال النشط:** `sales` فقط  
**القسم:** `high_ticket_closing`  
**النطاق:** استخراج مرشّح لمصدر واحد، لا إغلاق مصدر أو قسم أو مجال  
**الحالة:** `candidate_only`؛ لا `source_done` ولا `domain_terms_complete` ولا `domain_done`

## 1. نطاق العمل والمرجع

قُرئت قبل الاستخراج الملفات التالية:

1. `/sdcard/NEXUS_LLM_WIKI/AGENTS.md`
2. `/sdcard/NEXUS_LLM_WIKI/SCHEMA.md`
3. `/sdcard/NEXUS_LLM_WIKI/systems/15_DOMAIN_COMPLETION_GATES.md`
4. `done/sales/high_ticket_closing/REF_SRC_NEW_b0140a4d41654bab_b1f4775a.json`
5. `done/sales/high_ticket_closing/ROUTE_SRC_NEW_b0140a4d41654bab_b1f4775a.md`
6. `done/sales/high_ticket_closing/SRC_NEW_b0140a4d41654bab_b1f4775a.txt`

أُعيدت قراءة النص المستقل كاملًا بدل اعتبار دفعة القراءة القديمة مصدرًا بديلًا.
استُخدمت البصمة والنسخة الخام للتحقق من الهوية فقط. لم تُنشأ Concepts أو Masters،
ولم تُقبل أي Term أو Claim نهائيًا.

## 2. هوية المصدر وسلامة النسخة

| الحقل | القيمة |
|---|---|
| `source_id` | `SRC_NEW_b0140a4d41654bab_b1f4775a` |
| المسار الخام | `raw/new/matthewlucero__The Best Way To Book High-Ticket Sales Calls in 2026__Kx3ZSv2NqVQ.txt` |
| النسخة المقروءة | `done/sales/high_ticket_closing/SRC_NEW_b0140a4d41654bab_b1f4775a.txt` |
| bytes | `30,707` |
| Unicode code points | `30,707` |
| الأسطر | `1` |
| UTF-8 | strict decode؛ replacements=`0` |
| SHA-256 الخام والنسخة | `sha256:b0140a4d41654babf5ec880c63fa0da5e68ff72a8a2e5611a4b5652b31bb0d54` |
| bytes/hash | متساويان؛ `same_inode=false` |

المسار الخام الحالي والنسخة المستقلة متساويان byte-exact، والبصمة مطابقة لـREF/ROUTE.
لم يُعدّل raw. سجّل REF السابق أيضًا ثبات الأصل قبل/بعد إنشاء النسخة؛ وأُعيد فحص
البصمة الحالية بعد إنشاء مخرجات هذه المهمة.

## 3. تغطية القراءة

مرجع التغطية في JSON هو:
`READ_SALES_EXTRACTION_20261017_HIGH_TICKET`.

| segment | البداية | النهاية | ملاحظة |
|---|---:|---:|---|
| `SEG_SALES_EXTRACTION_20261017_HIGH_TICKET_01` | 0 | 10,235 | الغرض، الملاءمة، حجم الصفقة، دورة المبيعات، وفجوات العملية والاكتشاف |
| `SEG_SALES_EXTRACTION_20261017_HIGH_TICKET_02` | 10,235 | 20,471 | التأهيل، النموذج الافتراضي، قيمة العقد والإغلاق، وحالة العميل |
| `SEG_SALES_EXTRACTION_20261017_HIGH_TICKET_03` | 20,471 | 30,707 | الاستهداف والعروض والأمثلة والخاتمة، مع فصل سياق outreach |

الاتحاد المتصل هو `[0,10235) + [10235,20471) + [20471,30707)`، بلا gap أو overlap،
و`unread_ranges=[]`. هذه تغطية استخراج ذاتية كاملة للمصدر، وليست شهادة R شاملة
للمجال.

## 4. الأرقام الناتجة

- candidate terms: **16**.
- term occurrences: **31**.
- atomic candidate claims: **8**.
- semantic segments: **3**.
- unread ranges: **0**.
- `reported_result`: **1**.
- `direct_quote`: **4**.
- `example`: **3**.
- `inference`: **0**.

## 5. Candidate Terms

كل Term في هذه القائمة يحمل `status=candidate`، و`canonical_label=null`، وفجوة
تعريف، ومواضع Unicode صفرية بنهاية نصف مفتوحة، وعبارة المصدر ذاتها داخل JSON.
لا يوجد Term مقبول أو مدموج.

| # | `source_label` | عدد الظهور | المراجع المرشحة |
|---:|---|---:|---|
| 001 | `sales calls` | 5 | C001, C002 |
| 002 | `qualified sales calls` | 1 | — |
| 003 | `sales process` | 8 | C003, C004, C005 |
| 004 | `proper discovery` | 1 | C003 |
| 005 | `follow up` | 1 | C004 |
| 006 | `objection handling` | 1 | C004 |
| 007 | `second meeting` | 1 | C004 |
| 008 | `trust and relationship` | 1 | C004 |
| 009 | `sales cycle` | 2 | C002 |
| 010 | `qualified leads` | 2 | C005 |
| 011 | `minimum deal size` | 1 | — |
| 012 | `ticket size` | 1 | C006 |
| 013 | `average contract value` | 1 | C007 |
| 014 | `ACV` | 2 | C007 |
| 015 | `close rate` | 1 | — |
| 016 | `closed deals` | 2 | C007 |

المصطلحات المرتبطة بحجم الصفقة و`ACV` بقيت مرشحة ومقيدة بسياق النموذج الحسابي؛
لم تُعامل كتعريفات تسعير عامة.

## 6. Atomic Candidate Claims

كل Claim أدناه `status=candidate`، وبـ`source_id` نفسه، و`start/end` و`locator`
و`evidence_quote` و`quote_hash` قابلين لإعادة الفحص. الصياغة العربية لا تتجاوز
قوة النص، و`what_it_does_not_prove` محفوظ كاملًا في JSON.

| Claim | النوع | locator | confidence | مضمون محدود |
|---|---|---|---|---|
| C001 | `reported_result` | `0:210` | `source_reported` | المتحدث يبلّغ عن أكثر من 4,000 sales calls لنفسه ولعملائه خلال ثلاث سنوات وينسب ذكر cold email إلى المحرك المستخدم. |
| C002 | `direct_quote` | `3726:4096` | `source_reported` | عروض 10k/50k/100k لا تتم على الأرجح في مكالمة واحدة، وقد يستغرق الإغلاق أسابيع أو أشهر في هذا السياق. |
| C003 | `direct_quote` | `6053:6202` | `source_reported` | تفسير المتحدث لاعتقاد أن leads غير مؤهلة: غياب proper discovery داخل sales process. |
| C004 | `direct_quote` | `6203:6475` | `source_reported` | قائمة فجوات يذكرها المتحدث: المتابعة بعد المكالمة، objection handling، اجتماع ثانٍ، وبناء الثقة والعلاقة. |
| C005 | `direct_quote` | `11144:11435` | `source_reported` | توصيف المتحدث لـqualified بأنه lead قابل للبيع تحت شروط مناسبة، لا مجرد من لم يشترِ فورًا. |
| C006 | `example` | `2679:2939` | `hypothetical` | مثال حسابي: 100 صفقة بقيمة 100 دولار مقابل صفقة واحدة بقيمة 10,000 للوصول إلى 10,000 دولار إيراد. |
| C007 | `example` | `12115:12552` | `hypothetical` | سيناريو يضع ACV عند 20,000 دولار وثلاث صفقات مغلقة عنده، مع 100,000 رسالة، لحساب 60,000 دولار إيراد أمامي. |
| C008 | `example` | `13928:14884` | `source_reported` | حالة عميل واحدة: نحو 6,000 رسالة، 1.3% reply rate، 38% قالوا إنهم مهتمون، أول اجتماع بعد نحو 3 ساعات، وثلاثة اجتماعات في اليوم التالي. |

### فصل أنواع الدليل

- **reported_result:** C001 نتيجة منسوبة مباشرة إلى المتحدث عن خبرته.
- **direct_quote:** C002–C005 عبارات تفسيرية/وصفية نقلها النص مباشرة.
- **example:** C006 وC007 حسابات افتراضية؛ C008 حالة عميل وصفها المتحدث صراحة بأنها
  example/case study. لم تُحوّل أرقامها إلى benchmarks أو قواعد.
- **inference:** لا توجد inference claims؛ لم أضف استنتاجًا تركيبيًا لأن ذلك يتجاوز
  ما يثبته المصدر الواحد.

## 7. ما بقي خارج نطاق sales

يحتوي النص على مادة واسعة عن cold-email infrastructure، deliverability، الأدوات،
الاستهداف، TAM/ICP/segments، specificity، no-brainer offer، والمنافسة. تلك المادة
مرتبطة في ROUTE بإحالة سياقية إلى `outreach`، لذلك لم تُنشأ منها Claims مستقلة في
هذه المساهمة. أُبقي فقط ما كان لازمًا لتقييد سياق sales calls أو دورة الإغلاق أو
حسابات high-ticket، مع وسمه `example` أو `source_reported` عند اللزوم.

## 8. حدود الحالة والملفات المشتركة

- هذه **مساهمة مصدر واحدة مرشحة**، وليست `source_done` ولا
  `source_domain_extraction_complete` ولا `domain_terms_complete`.
- لم تُنشأ Concepts أو Masters، ولم تُكتب Terms في `term_inventory.json`.
- لم يُكتب أي سجل في `full_evidence_ledger.jsonl`، ولم يُحدّث أي INDEX مشترك.
- الملفات المنشأة فقط في هذه المهمة:
  1. `collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_HIGH_TICKET.json`
  2. `reports/sales-extraction-high-ticket-2026-10-17.md`
  3. `checkpoints/SALES_EXTRACTION_HIGH_TICKET_2026-10-17.md`

## 9. فحوص التنفيذ

| الفحص | النتيجة |
|---|---|
| `python3 -m json.tool` على JSON | PASS |
| إعادة حساب source/copy SHA-256 والـbytes | PASS؛ `30707/30707` والبصمة المتوقعة |
| raw مقابل النسخة المستقلة | PASS؛ bytes/hash متساويان و`same_inode=false` |
| كل term quote slice/hash | PASS؛ `31/31` |
| كل Claim quote slice/hash | PASS؛ `8/8` |
| روابط term→claim وحالات candidate-only | PASS؛ كل الروابط تحل، وConcepts/Masters=`0/0` |
| اتحاد semantic segments | PASS؛ `[0,30707)` بلا فجوة أو overlap |
| `unread_ranges` | PASS؛ `[]` |
| raw unchanged بعد المخرجات | PASS؛ البصمة الحالية ما زالت مطابقة لـREF |
| LSP diagnostics على JSON وملفي Markdown الناتجين | PASS؛ `No diagnostics found. All clean!` لكل ملف |
| `python3 tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json` | PASS؛ `ok=true`, `errors=[]`؛ فحص مساعد عام لا يثبت بوابات المجال |

التحقق البنيوي/الحسابي أعلاه لا يحوّل candidate إلى reviewed أو accepted، ولا يفتح
أي بوابة مجال.
