# استخراج مرشح لمصدر واحد — proposal/follow-up/pipeline

## الحكم والنطاق

هذه **مساهمة مصدر واحدة candidate** للمجال النشط `sales` والقسم
`proposal_follow_up_pipeline`. لا تعلن هذه المخرجات `source_done`، ولا
`subdomain_extraction_done`، ولا `domain_terms_complete`، ولا `domain_done`، ولا
تنشئ Concepts أو Masters أو قبولًا نهائيًا لأي Term/Claim.

قُرئت النسخة المستقلة كاملة، وسُجلت Terms وClaims المرشحة فقط بما يسنده النص.
تفاصيل `outreach` التي ظهرت في المصدر بقيت سياقًا مقروءًا ومؤجلًا، ولم تُستخرج
لأن قفل المعرفة النشط هو `sales` فقط.

## هوية المصدر وسلامة الدليل

| الحقل | القيمة المتحققة |
|---|---|
| `source_id` | `SRC_NEW_34aaffac87a9dd7f_0535de17` |
| المسار الخام | `raw/new/smartleadai__How to Close 500+ Sales Opps in 90 Days with David Lehnert__DhzsNovGxgM.txt` |
| النسخة المقروءة | `done/sales/proposal_follow_up_pipeline/SRC_NEW_34aaffac87a9dd7f_0535de17.txt` |
| الحجم | `70,159` bytes |
| Unicode view | `70,159` code points، سطر واحد بلا newline نهائي |
| raw SHA-256 | `sha256:34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d` |
| copy SHA-256 | مطابق تمامًا |
| raw/copy bytes | متساوية؛ فحص مستقل من البايتات |
| route/reference | `ROUTE_SRC_NEW_34aaffac87a9dd7f_0535de17` و`REF_SRC_NEW_34aaffac87a9dd7f_0535de17` |

البصمة المحفوظة في JSON هي بصمة البايتات، لا بصمة نص مطبّع. لم يُعدّل raw، ولم
تُعدّل `term_inventory.json` أو `full_evidence_ledger.jsonl` أو أي `INDEX.md`.

## تغطية القراءة

سجل القراءة الكامل محفوظ داخل `read_coverage` في ملف الدفعة. الحدود صفرية
وبـUnicode code points ونصف مفتوحة:

| segment | start | end | مضمون القراءة |
|---|---:|---:|---|
| `SEG_SALES_EXTRACTION_20261017_0535de17_01` | 0 | 23,386 | الغرض والنتائج والتكلفة وبناء القائمة والتأهيل وprompts |
| `SEG_SALES_EXTRACTION_20261017_0535de17_02` | 23,386 | 46,772 | جهات الاتصال، أسلوب النسخة، hook/pain/proof/remedy/CTA والـproposal |
| `SEG_SALES_EXTRACTION_20261017_0535de17_03` | 46,772 | 70,159 | أمثلة التخصيص، القياس، المتابعة، deliverability والحدود |

الاتحاد المتصل هو `[0,70159)` بلا overlap أو فجوة، و`unread_ranges=[]`. سجلت
خمس `content_units` مصيرها، مع فصل السياق المؤجل عن الوحدات التي خرجت منها
مرشحات sales. `semantic_review_status=reviewed` و`extraction_status=reviewed`
هما مراجعة ذاتية للمرشح، وليسا مراجعة Reviewer مستقلة.

## حصيلة المرشحات

- **29 candidate terms**، وكل Term يحمل `source_label`، و`definition` أوليًا
  فقط حين يشرحه النص، أو `definition_gap` صريحًا، وscope وoccurrence مع quote
  وUnicode offset وhash.
- **28 atomic candidate claims**، وكل Claim يحمل statement عربيًا مقيدًا،
  `evidence_type`، `source_id`، locator/start/end، quote حرفيًا،
  `quote_hash`، scope، confidence، `status=candidate`، وحدود
  `what_it_does_not_prove`.
- توزيع نوع الدليل: `direct_quote=18`، `reported_result=7`،
  `example=3`، `inference=0`، `hypothesis=0`.
- لم تُحوّل أرقام المتحدث أو أمثلة الحملات إلى قواعد عامة. لا توجد Claims من
  نوع `inference`؛ أي قراءة تحليلية غير منقولة بقيت في حدود scope/limits ولم
  تُسجل كدليل.

### عائلات Terms

1. **هوية pipeline والنتيجة:** `521 opportunities`، `pipeline`، `reply rates`،
   `positive reply rate`.
2. **بناء وتأهيل المسار:** `list building`، `lead list`،
   `qualifies the results`، `value proposition`،
   `every table just has one purpose`، `waterfall process`، `find contacts`.
3. **الرسالة والعرض:** `copy`، `personalized`، `hook`، `pain`، `proof`،
   `remedy`، `proposal`، `CTA`، والهيكل المركب
   `hook, pain, proof, remedy, and a CTA`.
4. **المتابعة والقياس:** `social proof`، `deliverability`، `spin tax`،
   `tracking links`، `response rates`، `follow-ups`، `in batches`،
   `unique offer`.

هذه labels مصدرية مرشحة وليست أسماء canonical معتمدة؛ أي تشابه لفظي لاحقًا لا
يبرر الدمج.

### فصل أنواع Claims

#### `reported_result`

المرشحون `001–004` و`020–021` و`024` تحفظ النتائج المنسوبة كما وردت: 521
فرصة و2M في التقديم، تكلفة/مخرجات setup، نسب الرد والإيجابية، مثال CTA بنسبة
3%، مقارنة ألمانيا، وتجربة spinx لحملة عميل. كل واحد bounded بسياقه وحدود
المقام والتحقق.

#### `example`

المرشحون `005` و`007` و`022` أمثلة حملة/تأهيل أو مثال نتيجة محدد. لم تُحوّل
شروط فنادق ألمانيا، 13 غرفة، أو رقم 45 lead إلى ICP أو benchmark عام.

#### `direct_quote`

المرشحون `006–019` و`023` و`025–028` تحفظ ممارسات أو توصيات المتحدث حرفيًا:
جداول ذات غرض واحد، التأهيل، الفحص اليدوي السابق للأتمتة، بنية prompts، عدم
إنشاء البريد كاملًا عبر ChatGPT، waterfall contacts، التحقق، أسلوب الرسالة،
تدرج الفقرات، وظائف hook/problem/pain/remedy/CTA، هيكل الرسالة، social proof،
القياس، إعادة المراسلة، الدفعات، وإظهار العمل مع المنافسة.

#### `inference`

لا توجد inference Claims. تم تجنب تحويل ملاحظات المتحدث مثل «قد يكون» أو
التفسير الشخصي لأداء السوق إلى استنتاج مستقل.

## تناقض مصدر محفوظ

يظهر في النص رقمان مختلفان للـpipeline مع نفس 521 فرصة:

1. في تقديم الجلسة: **$2 million pipeline** عند `chars 1452:1686`.
2. في سؤال لاحق من المضيف: **$9 million pipeline** عند `chars 8240:8293`.

حُفظت القيمتان والـhashان في `source_internal_conflicts` داخل JSON. لم تُسوَّيا
بالتخمين؛ Claim `001` يقتصر على أول صياغة، والثانية بقيت تعارضًا غير محسوم
لأنها وردت داخل سؤال المضيف لا كتصحيح موثق من المتحدث.

## حدود التفسير

- النسب والأرقام reported من transcript، وليست نتائج مستقلة أو benchmark.
- المثال ليس قاعدة: بنية `hook/pain/proof/remedy/CTA` واحدة من هياكل الرسالة،
  ومثال Aston Martin ومثال 45 lead لا يثبتان قاعدة عامة.
- النص لا يثبت تعريفًا قياسيًا لـ`opportunity` أو `pipeline` أو `reply rate`،
  ولا يثبت سببًا وحيدًا لأداء ألمانيا أو هبوط حملة spinx.
- لا توجد Claims عن `pricing_offers` أو `content_strategy` أو معرفة مستقلة
  لـ`outreach`; أي صلة ثانوية بقيت مرئية دون استخراج في هذا المجال.

## فحوص التحقق المنفذة

| الفحص | الأمر/الطريقة | النتيجة |
|---|---|---|
| JSON parsing | `python3` يحمّل ملف الدفعة عبر `json.loads` | PASS |
| quote slices | إعادة قص كل `Term.occurrences` و`Claim.evidence_start:end` من النسخة | PASS؛ لا slice mismatch |
| quote hashes | إعادة حساب SHA-256 لكل quote ومقارنته بـ`quote_hash` | PASS؛ 29 Term و28 Claim و4 conflict observations |
| coverage | فحص أول start وآخر end وتساوي حدود segments المتجاورة | PASS؛ `[0,70159)` متصل |
| source/copy | إعادة حساب raw/copy SHA-256 ومقارنة البايتات | PASS؛ متطابقان |
| raw unchanged | إعادة قراءة raw بعد الكتابة ومقارنة البصمة المسجلة | PASS؛ `raw_unchanged=true` |
| LSP | `lsp_diagnostics` على ملف JSON | PASS؛ `No diagnostics found. All clean!` |
| فحص الويكي البنيوي المساعد | `python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json` | PASS؛ exit 0 و`ok=true`، ولا يُعامل وحده كإثبات قراءة دلالية أو بوابة T/C |

التحقق أعلاه يثبت سلامة الاقتباس والموضع والـIO لهذا artifact، ولا يثبت قبول
المعرفة أو اكتمال المصدر/القسم/المجال.

محاولة `wiki_quality.py` الأولى بمهلة 120 ثانية انتهت بمهلة تشغيل، ثم أُعيد
تشغيل الأمر بمهلة 300 ثانية وانتهى `exit 0` و`ok=true`؛ لذلك لا تبقى نتيجة
الفحص المساعد غير منفذة، مع بقاء حدوده البنيوية كما هي.

## الملفات التي أنشأها Worker

1. `collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_PROPOSAL_FOLLOW_UP.json`
2. `reports/sales-extraction-proposal-follow-up-2026-10-17.md`
3. `checkpoints/SALES_EXTRACTION_PROPOSAL_FOLLOW_UP_2026-10-17.md`

هذه الملفات الثلاثة هي مخرجات هذا النطاق فقط؛ لا يوجد تعديل على سجل Term أو
ledger أو أي فهرس مشترك.
