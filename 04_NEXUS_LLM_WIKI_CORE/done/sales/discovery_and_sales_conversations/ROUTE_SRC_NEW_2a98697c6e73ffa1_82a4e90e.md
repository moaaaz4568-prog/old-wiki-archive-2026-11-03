# Route `SRC_NEW_2a98697c6e73ffa1_82a4e90e`

- `route_status`: `route_done`
- `source_extraction_status`: `not_started`
- `source_id`: `SRC_NEW_2a98697c6e73ffa1_82a4e90e`
- `source_path`: `raw/new/sabonagy__How to Get Your First Client A-Z Guide to Client Acquisition (Proven Steps)__FiDEMUsG6SQ.txt`
- `copy_path`: `done/sales/discovery_and_sales_conversations/SRC_NEW_2a98697c6e73ffa1_82a4e90e.txt`
- `reference_metadata`: `done/sales/discovery_and_sales_conversations/REF_SRC_NEW_2a98697c6e73ffa1_82a4e90e.json`
- `batch`: `collections/sales/reading/SALES_BATCH_2026-10-11_001.json`
- `workflow_id`: `WF_20261017_ROUTE_COPY_DISCOVERY`
- `reviewer`: `worker-self-check` (لا توجد مراجعة مستقلة في نطاق هذه المهمة)

## حدود القرار

هذا الملف يسجل التوجيه ونسخة المصدر والتحقق منهما فقط. لا يمثل Claim أو Term أو
Concept أو Master، ولا يعلن `source_done` أو `domain_done` أو نجاح بوابات
`T/C/K/M/QA`. لم تُنشأ في هذه المهمة أي ملفات معرفية جديدة.

المصدر القديم في reading batch استُخدم كإشارة مساعدة للمسار والمواضع فقط. أُعيدت
قراءة ملف `raw/new` نفسه كاملًا في 2026-10-17، وأُعيد حساب SHA-256، وأُعيد فحص كل
اقتباس أدناه على `source_text[start:end]`؛ لم تُنقل نتائج batch القديم باعتبارها
بديلًا عن إعادة التحقق.

## الهوية والقراءة الكاملة

| الحقل | النتيجة المتحققة |
|---|---|
| نوع الملف | transcript نصي UTF-8 |
| الحجم | `14,545` بايت |
| القراءة | `14,545 / 14,545` بايت، `EOF=true` |
| Unicode | `14,545` code points، سطر واحد، بلا trailing newline |
| الترميز | UTF-8 strict، `decode_replacements=0` |
| SHA-256 المصدر | `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047` |
| تغطية routing | `[0,4848) + [4848,9696) + [9696,14545) = [0,14545)`، بلا gaps/overlaps |
| read coverage | `READ_ROUTE_COPY_DISCOVERY_20261017_SRC_NEW_2a98697c6e73ffa1_82a4e90e` |

المقاطع الثلاثة هي تغطية فهم توجيهي (`mode=routing`) لا استخراجًا معرفيًا؛
`content_units=[]` و`extraction_status=not_started` عمدًا.

## قرار المسار الأساسي

```text
primary domain:    sales
primary subdomain: discovery_and_sales_conversations
confidence:        medium
```

الغرض الغالب كما يظهر من متن المصدر هو نقل العميل المحتمل عبر دورة اكتساب
العميل ثم حجز المكالمة والحضور والمحادثة البيعية والإغلاق ومعالجة الاعتراضات.
لذلك يطابق المسار `sales/discovery_and_sales_conversations`. لا يعتمد القرار على
اسم الملف وحده.

### أدلة التصنيف الحرفية من المتن

كل المواضع صفرية البداية، بوحدة Unicode code point، وبحدود نصف مفتوحة `[start,end)`.
البصمات أدناه هي SHA-256 للاقتباس نفسه بترميز UTF-8.

| العائلة | الموضع | الاقتباس الحرفي | SHA-256 للاقتباس |
|---|---:|---|---|
| purpose | `chars 1397:1520` | “So client acquisition is a structured set of processes designed to attract, nurture, convert leads into highpaying clients.” | `95c20b0ff20fc322ecaa5b1e396becce75f025cbb1cd11e8873534aa86572990` |
| structure/action | `chars 5538:5642` | “So, booking a call, the key to high appointment setting rate is making sure the process is frictionless.” | `e19faf256b2feb45a134d654d02d08a4753d9377fbb532645d94083a97bb208f` |
| sales conversation | `chars 8551:8603` | “the goal is to convert them into high paying clients” | `66f18bc1d708746914ee764a21229080bd1c830f37d7d0e12283d2063a9429f4` |
| objection handling | `chars 9755:9801` | “here's some just objection handling frameworks” | `031100c2f46ec380015735cba83fccb6a62912d90f67eda3a518babe5fb71b77` |
| measurement | `chars 11303:11348` | “The key metrics are appointment booking rate.” | `daf7d1ee4ad38d4b241dc89025b74a440007995a0f5bc6d9b8d07bdb5ca02a4d` |

### مراجع ثانوية bounded

المراجع التالية سياقية، وتحمل نفس `source_id` ولا تنشئ نسخًا أو دليلًا مستقلًا:

1. `outreach/outreach_mechanics_and_follow_up` — `medium`، لأن outbound يظهر
   كقناة ضمن دورة جذب الانتباه، مع موضع `chars 3437:3570`: “then you have
   outbound, which is doing cold email, LinkedIn outreach, direct messages, cold
   calling, strategic network, partnerships,”.
2. `pricing_offers/guarantees_risk_reversal_and_price_objections` — `low`، لأن
   التسعير وضمان تقليل المخاطر والاعتراض السعري تظهر داخل محادثة البيع، لا كغرض
   أساسي لتصميم architecture، مع موضعي `chars 9266:9356` و`chars 10290:10355`.

لا توجد إحالة ثانوية إلى `content_strategy` في هذا route؛ ذكر inbound/content
يخدم دورة الاكتساب ولا يثبت أن المصدر يشرح استراتيجية محتوى.

## التكرار والهوية

- `duplicate_of`: `null`؛ لا توجد نسخة done سابقة لهذا `source_id`.
- `collections/corpus/manifest.jsonl` يحمل مرجعًا آخر بنفس البصمة تحت
  `SRC_CORPUS_raw_new_2a98697c6e73ffa1_a8ee347ee067`؛ عومل ذلك كمطابقة hash
  مرجعية لنفس البايتات، لا كمصدر مستقل ولا كنسخة ثانية.
- `raw/SOURCE_MANIFEST.tsv` يحمل مسارًا legacy بنفس الحجم والبصمة، لكن الملف
  legacy المشار إليه غير موجود عند الفحص؛ سُجل كـ`stale_reference` ولم يُعتبر
  duplicate مستقلًا متحققًا.
- لم يُعدّل أي manifest، ولم تُنشأ نسخة duplicate إضافية.

## تحقق النسخة المستقلة

النسخة أُنشئت كملف regular جديد مباشرة تحت المسار الأساسي، دون تطبيع ترميز أو
استبدال ملف قائم:

| الفحص | النتيجة |
|---|---|
| حجم الأصل قبل/بعد | `14545 / 14545` |
| حجم النسخة | `14545` |
| SHA-256 الأصل | `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047` |
| SHA-256 النسخة | نفس البصمة تمامًا |
| bytes equal | `true` |
| symlink | `false` |
| hardlink / same inode | `false` (`source dev/ino=(169,1997006)`, `copy dev/ino=(169,2032083)`) |
| regular file | `true` |
| الأصل unchanged | `true` |

## بوابات G0–G8

| البوابة | الحكم | الدليل |
|---|---|---|
| G0 الهوية والمسار | PASS | source ID آمن traversal-free، والمسارات نسبية بلا `..`، ووجهة النسخة تحت المسار الأساسي |
| G1 سلامة IO | PASS | strict UTF-8، `bytes_read=bytes_expected=14545`، EOF، إعادة قراءة مستقرة، بلا replacements |
| G2 البصمة | PASS | hash المصدر المعاد حسابه يطابق batch وsource record؛ hash النسخة يطابقه |
| G3 التكرار | PASS | فحص source record وsales reading وcorpus manifest وdone؛ المطابقة الأخرى مرجعية فقط، والlegacy path stale موثق |
| G4 القراءة الدلالية والصلة | PASS | routing segments متصلة تغطي `[0,14545)`، مع مواضع body/structure/purpose واقتباسات قابلة لإعادة القراءة |
| G5 المسار الأساسي | PASS | زوج `sales/discovery_and_sales_conversations` موجود في `config/domain_catalog.json` |
| G6 المراجع الثانوية | PASS | مرجعان bounded لهما نفس source ID ومواضع وسياق؛ لا نسخ ثانية |
| G7 النسخة وmetadata | PASS | regular byte-exact copy، hash/bytes متساويان، symlink/hardlink=false، وREF/ROUTE مكتملان |
| G8 سلامة الخام والفهرسة | PASS | raw pre/post متساويان، وINDEX المحلي محدث؛ لم تُلمس parent indexes |

## الحراس والقيود

جرد `raw/new` استُخرج بـ`os.walk(followlinks=False)`، مع ترتيب المسارات، ثم hash
صفوف `relative_path + size + sha256`؛ النتيجة قبل وبعد:

```text
file_count:       1776
total_bytes:      43,757,343
inventory_sha256: 4ce12a3c7d48371333ba77367817f88d065152b09ad2106ab01cf0d32a3cff4b
```

كما بقيت البصمات التالية دون تغيير:

- `collections/sales/manifest.json`: `sha256:1c729810fbc2ca115e7cf55a17fe4a891eea62f63195c7304182622efee92923`.
- `collections/corpus/manifest.jsonl`: `sha256:aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3`.
- `config/domain_catalog.json`: `sha256:3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add`.
- المصدر الخام المحدد: `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047`.

قيود هذا التسليم:

- الدفعة المختارة ليست inventory أو snapshot كاملة؛ لا يُستنتج منها اكتمال sales.
- `semantic_review_status=reviewed` هو self-check توجيهي من Worker، وليس QA
  مستقلًا أو مراجعة معرفية.
- سجل `sources/SRC_NEW_2a98697c6e73ffa1_82a4e90e.md` القديم بحالة `processed`
  لم يُعدّل، ولا يُستخدم هنا لإثبات `source_done`؛ الحالة التشغيلية المنفصلة في
  هذا route هي `source_extraction_status=not_started`.
- لم تُنشأ Terms/Claims/Concepts/Masters، ولم تُعدّل ملفات raw أو corpus
  manifest أو config أو parent indexes المشتركة.
