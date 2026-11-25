# تقرير route + copy — `SRC_NEW_2a98697c6e73ffa1_82a4e90e`

## الحكم التنفيذي

اكتملت مهمة route + copy للمصدر المحدد فقط:

- المسار الأساسي: `done/sales/discovery_and_sales_conversations/`.
- القرار: `sales/discovery_and_sales_conversations`، بثقة `medium`، اعتمادًا على
  متن المصدر لا على اسم الملف وحده.
- النسخة: regular file مستقلة، byte-exact، بلا symlink أو hardlink.
- `route_status`: `route_done`.
- `source_extraction_status`: `not_started`.
- لم تُنشأ Terms أو Claims أو Concepts أو Masters.
- لم تُعدّل raw أو أي corpus manifest أو config أو parent index مشترك.

مخرجات الويكي الناتجة/المعدلة في هذه المهمة:

1. `done/sales/discovery_and_sales_conversations/SRC_NEW_2a98697c6e73ffa1_82a4e90e.txt`
2. `done/sales/discovery_and_sales_conversations/REF_SRC_NEW_2a98697c6e73ffa1_82a4e90e.json`
3. `done/sales/discovery_and_sales_conversations/ROUTE_SRC_NEW_2a98697c6e73ffa1_82a4e90e.md`
4. `done/sales/discovery_and_sales_conversations/INDEX.md` — تحديث الفهرس المحلي فقط
5. `staging/routing/ROUTE_RUN_20261017_DISCOVERY.json`
6. `staging/routing/ROUTE_RUN_20261017_DISCOVERY_summary.json`
7. `staging/routing/ROUTE_RUN_20261017_DISCOVERY_checks.md`
8. `reports/route-copy-discovery-2026-10-17.md`
9. `checkpoints/ROUTE_COPY_DISCOVERY_2026-10-17.md`

## نطاق القراءة وإعادة التحقق

المدخل التشغيلي هو:

```text
collections/sales/reading/SALES_BATCH_2026-10-11_001.json
```

السجل المطلوب فيه:

```text
source_id: SRC_NEW_2a98697c6e73ffa1_82a4e90e
raw_path:  raw/new/sabonagy__How to Get Your First Client A-Z Guide to Client Acquisition (Proven Steps)__FiDEMUsG6SQ.txt
```

قُرئ المصدر الخام نفسه كاملًا في 2026-10-17 بقراءة bytes كاملة ثم decode UTF-8
strict، وإعادة قراءة للمقارنة. استُخدم سجل reading batch القديم للتنقل الأولي
فقط؛ لم يُعتبر دليلًا بديلًا عن هذه القراءة.

| القياس | النتيجة |
|---|---:|
| bytes expected/read | `14,545 / 14,545` |
| Unicode code points | `14,545` |
| lines | `1` |
| trailing newline | `false` |
| encoding | `utf-8` strict |
| decode replacements | `0` |
| EOF | `true` |
| source SHA-256 | `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047` |
| read coverage | `READ_ROUTE_COPY_DISCOVERY_20261017_SRC_NEW_2a98697c6e73ffa1_82a4e90e` |

تغطية routing المتصلة هي:

```text
[0,4848) + [4848,9696) + [9696,14545) = [0,14545)
```

لا توجد `unread_ranges` أو gaps أو overlaps. هذه تغطية توجيه وفهم الغرض، وليست
استخراجًا دلاليًا؛ لذلك بقيت `content_units=[]` و`source_extraction_status` على
`not_started`.

## أدلة قرار التصنيف

الغرض الغالب في المتن هو دورة اكتساب العميل التي تنقل lead إلى حجز مكالمة، ثم
الحضور والمحادثة البيعية والإغلاق ومعالجة الاعتراضات. لذلك اختير
`sales/discovery_and_sales_conversations` بدل `outreach` أو `pricing_offers` كمسار
أساسي.

كل المواضع أدناه صفرية البداية، بوحدة Unicode code point، وبحدود نصف مفتوحة؛
أُعيد فحص كل اقتباس على النص الخام مباشرة:

| العائلة | locator | الاقتباس | quote SHA-256 |
|---|---|---|---|
| purpose | `chars 1397:1520` | `So client acquisition is a structured set of processes designed to attract, nurture, convert leads into highpaying clients.` | `95c20b0ff20fc322ecaa5b1e396becce75f025cbb1cd11e8873534aa86572990` |
| structure/action | `chars 5538:5642` | `So, booking a call, the key to high appointment setting rate is making sure the process is frictionless.` | `e19faf256b2feb45a134d654d02d08a4753d9377fbb532645d94083a97bb208f` |
| sales conversation | `chars 8551:8603` | `the goal is to convert them into high paying clients` | `66f18bc1d708746914ee764a21229080bd1c830f37d7d0e12283d2063a9429f4` |
| objection handling | `chars 9755:9801` | `here's some just objection handling frameworks` | `031100c2f46ec380015735cba83fccb6a62912d90f67eda3a518babe5fb71b77` |
| measurement | `chars 11303:11348` | `The key metrics are appointment booking rate.` | `daf7d1ee4ad38d4b241dc89025b74a440007995a0f5bc6d9b8d07bdb5ca02a4d` |

المراجع الثانوية bounded، بنفس `source_id` ومن دون نسخ ثانية:

- `outreach/outreach_mechanics_and_follow_up`، ثقة `medium`، لأن outbound يظهر
  كقناة داخل دورة الاكتساب (`chars 3437:3570`).
- `pricing_offers/guarantees_risk_reversal_and_price_objections`، ثقة `low`، لأن
  السعر والضمان والاعتراض السعري تظهر داخل محادثة البيع (`chars 9266:9356` و
  `chars 10290:10355`) وليست الغرض المركزي.

لا توجد إحالة secondary إلى `content_strategy`؛ إشارات inbound/content سياق في
دورة الاكتساب ولا تكفي لتوجيه المصدر إلى استراتيجية محتوى.

## نسخة المصدر والتحقق

النسخة أُنشئت مباشرة في:

```text
done/sales/discovery_and_sales_conversations/SRC_NEW_2a98697c6e73ffa1_82a4e90e.txt
```

نتائج الفحص:

| الفحص | النتيجة |
|---|---|
| copy size | `14,545` bytes |
| original SHA-256 | `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047` |
| copy SHA-256 | مطابق تمامًا |
| bytes equal | `true` |
| source `dev,ino` | `(169,1997006)` |
| copy `dev,ino` | `(169,2032083)` |
| symlink | `false` |
| hardlink / same inode | `false` |
| regular file | `true` |
| original unchanged after copy | `true` |

لا يوجد overwrite؛ قبل النسخ لم يكن ملف source-id أو REF أو ROUTE هذا موجودًا في
المجلد المباشر.

## التكرار ومراجع الهوية

وجد الفحص المرجعي تطابق hash في `collections/corpus/manifest.jsonl` تحت:

```text
SRC_CORPUS_raw_new_2a98697c6e73ffa1_a8ee347ee067
raw_new/sabonagy__How to Get Your First Client A-Z Guide to Client Acquisition (Proven Steps)__FiDEMUsG6SQ.txt
```

هذه إحالة لنفس البايتات، لا مصدر مستقل؛ لم تُنشأ لها نسخة ثانية ولم يتضاعف وزن
الدليل. بقي `duplicate_of=null` للمصدر الحالي لأن المصدر الحالي هو سجل
`raw/new` القائم الذي أُعيد التحقق منه، ولا توجد نسخة done سابقة.

كما يشير `raw/SOURCE_MANIFEST.tsv` إلى مسار legacy بنفس الحجم والبصمة، لكن المسار
الفعلي `raw/legacy/brain/...` غير موجود عند الفحص. لذلك سُجل كـstale reference
فقط، ولم يُعامل كتكرار مستقل متحقق.

## raw pre/post والملفات المحمية

جرد `raw/` و`raw/new` أُجري قبل وبعد باستخدام `os.walk(followlinks=False)`، مع ترتيب
المسارات، وبناء صفوف:

```text
relative_path + NUL + size + NUL + sha256(file) + LF
```

ثم SHA-256 للحمولة المرتبة. النتيجة قبل وبعد مطابقة:

| الجرد | pre | post | الحكم |
|---|---:|---:|---|
| `raw/` file count | `1820` | `1820` | UNCHANGED |
| `raw/` total bytes | `50,898,163` | `50,898,163` | UNCHANGED |
| `raw/` inventory SHA-256 | `96e9ff6f6ce82ceb244f87df23097100576a8b26cf8731eacbe59b6f980c21a2` | نفس البصمة | UNCHANGED |
| `raw/new` file count | `1776` | `1776` | UNCHANGED |
| `raw/new` total bytes | `43,757,343` | `43,757,343` | UNCHANGED |
| `raw/new` inventory SHA-256 | `4ce12a3c7d48371333ba77367817f88d065152b09ad2106ab01cf0d32a3cff4b` | نفس البصمة | UNCHANGED |

وبالتالي لا يقتصر الحارس على `raw/new` وحده؛ نتيجة الجرد الكامل لـ`raw/` أيضًا
مطابقة قبل/بعد.

| الجرد الإضافي | pre | post | الحكم |
|---|---:|---:|---|
| selected raw source | `14,545` bytes / target SHA | `14,545` bytes / target SHA | UNCHANGED |

وبقيت البصمات المحمية التالية كما كانت:

- `collections/sales/manifest.json`: `sha256:1c729810fbc2ca115e7cf55a17fe4a891eea62f63195c7304182622efee92923`.
- `collections/corpus/manifest.jsonl`: `sha256:aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3`.
- `config/domain_catalog.json`: `sha256:3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add`.
- المصدر الخام المحدد: `sha256:2a98697c6e73ffa19e4825eaf35e80a5d14890cafba47213d919bfd0b8558047`.

لم تُرسل أي عملية كتابة إلى parent indexes المشتركة؛ التعديل الوحيد في طبقة
الفهرسة كان `done/sales/discovery_and_sales_conversations/INDEX.md` المحلي.

## بوابات التحقق

| البوابة | الحكم | الدليل |
|---|---|---|
| G0 الهوية والمسار | PASS | source ID آمن، path نسبي، بلا traversal |
| G1 سلامة IO | PASS | full strict read، EOF، bytes كاملة، stable، no replacements |
| G2 SHA-256 | PASS | hash الخام والنسخة متطابقان معًا ومع السجل المساعد |
| G3 dedup | PASS | corpus match موثق كمرجع، legacy path موثق stale، لا نسخة ثانية |
| G4 routing coverage | PASS | segments متصلة كاملة، quotes قابلة لإعادة القراءة |
| G5 primary route | PASS | الزوج موجود في catalog الحالي |
| G6 secondary refs | PASS | مرجعان bounded بنفس الهوية والمواضع |
| G7 copy + metadata | PASS | regular byte-exact، no symlink/hardlink، REF وROUTE مكتملان |
| G8 raw + local index | PASS | raw pre/post متطابقان، INDEX المحلي محدث |

## أوامر التحقق الفعلية

1. قراءة المصدر الكامل والبصمة وإعادة القراءة:

   ```text
   python3 -c '... Path(raw).read_bytes(); decode("utf-8"); stat before/after; reread; sha256 ...'
   ```

   النتيجة: `bytes=14545`, `chars=14545`, `lines=1`, `trailing_newline=False`,
   hash مطابق، وEOF/re-read ثابتان.

2. تحقق النسخة وmetadata والاقتباسات والsegments وraw inventory والملفات المحمية:

   ```text
   python3 -c '... json.loads(REF); source/copy bytes+hash+inode; evidence slices; segment union; os.walk(raw/new); protected hashes ...'
   ```

   النتيجة الفعلية:

   ```json
   {
     "bytes_equal": true,
     "symlink": false,
     "hardlink": false,
     "segments": "PASS",
     "quotes": 5,
     "raw_new_inventory": [1776, 43757343, "4ce12a3c7d48371333ba77367817f88d065152b09ad2106ab01cf0d32a3cff4b"],
     "protected_hashes": "PASS",
     "json": "PASS",
     "route_status": "route_done",
     "source_extraction_status": "not_started"
   }
   ```

3. فحص JSON مستقلًا عبر `json.loads` في الأمر السابق: `PASS`.
4. فحص سجلي التشغيل عبر `python3 -m json.tool` للـrun والـsummary، ثم إعادة
   مطابقة quote slices في `ROUTE_RUN_20261017_DISCOVERY.json`: `PASS` (`entries=1`،
   `quotes=5`، `route_done=1`).

لم يُستخدم Codex أو subagents، ولم تُنفذ عملية حذف أو نقل أو overwrite.

## القيود والمرحلة التالية

- batch `SALES_BATCH_2026-10-11_001` يعلن `inventory_complete=false`؛ هذا التسليم
  لا يمثل snapshot كاملة ولا يرفع حالة domain.
- `route_done` لا يعني `source_done`؛ لم يبدأ استخراج Terms/Claims، ولذلك لا
  توجد بوابات T/C/K/M/QA أو اعتماد Concept/Master هنا.
- سجل Source القديم في `sources/` بحالة `processed` بقي دون تعديل؛ أُشير إليه فقط
  كحالة تاريخية، ولا يُستخدم كإثبات route أو source completion.
- أي تعميق معرفي لاحق يجب أن يبدأ من النسخة والـREF والـROUTE مع إعادة التتبع، لا
  من اسم الملف أو من reading batch وحده.
