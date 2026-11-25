# تقرير route + copy — `SRC_NEW_b0140a4d41654bab_b1f4775a`

**التاريخ:** 2026-10-17  
**النطاق:** route + verified copy فقط لمصدر واحد  
**المسار الأساسي:** `done/sales/high_ticket_closing/`  
**الحالة:** `route_done`  
**حالة الاستخراج:** `source_extraction_status: not_started`

## الحكم التنفيذي

أُعيدت قراءة المصدر الخام الحالي كاملًا من المسار المحدد في سجل القراءة، ثم
أُعيد حساب الحجم والبصمة ومواضع الأدلة. أُنشئت نسخة regular مستقلة byte-exact
باسم آمن مبني على `source_id`، وأُنشئت `REF_`, `ROUTE_`, و`INDEX.md` المحلي.
مرّت فحوص البصمة، EOF، التغطية المتصلة، الاقتباسات، الاستقلال عن الأصل، وعدم
تغيير raw. لذلك `route_status=route_done` هنا يعني اكتمال R/route + copy فقط؛
ولا يعني `source_done` أو إغلاق sales أو بدء أي طبقة معرفة.

لم تُنشأ Claims أو Terms أو Concepts أو Masters، ولم يُعدّل raw أو أي manifest
قائم (raw/corpus/sales) أو config أو parent index؛ أُنشئت فقط سجلات route التشغيلية
المذكورة أدناه داخل `staging/routing/`. لم يُستخدم Codex أو subagents، ولم تُنفذ
عملية حذف أو نقل أو overwrite.

## العقود التي قُرئت وطُبقت

قُرئت قبل التنفيذ كاملًا:

1. `/sdcard/NEXUS_LLM_WIKI/AGENTS.md`
2. `/sdcard/NEXUS_LLM_WIKI/SCHEMA.md`
3. `/sdcard/NEXUS_LLM_WIKI/systems/14_SOURCE_ROUTING_AND_DONE_TREE.md`
4. `/sdcard/NEXUS_LLM_WIKI/config/domain_catalog.json`
5. المصدر المحدد في `collections/sales/reading/SALES_BATCH_2026-10-11_001.json`

طُبقت القواعد التالية: مصدر واحد primary، المسار نسبي وآمن، التصنيف من المتن
لا من الاسم وحده، النسخة المباشرة regular لا symlink/hardlink، raw immutable،
و`route_done` منفصل عن extraction/domain gates.

## هوية المصدر والقراءة الكاملة

| الحقل | القيمة المتحققة |
|---|---|
| `source_id` | `SRC_NEW_b0140a4d41654bab_b1f4775a` |
| `source_path` | `raw/new/matthewlucero__The Best Way To Book High-Ticket Sales Calls in 2026__Kx3ZSv2NqVQ.txt` |
| الحجم المتوقع/المقروء | `30,707 / 30,707` bytes |
| UTF-8 code points | `30,707` |
| الأسطر | `1` |
| EOF | PASS؛ probe بعد القراءة أعاد `b''` |
| strict UTF-8 | PASS؛ `decode_replacements=0` |
| إعادة القراءة | PASS؛ bytes/hash مطابقان |
| SHA-256 | `sha256:b0140a4d41654babf5ec880c63fa0da5e68ff72a8a2e5611a4b5652b31bb0d54` |
| `view` | Unicode code points، `[0,30707)`، بصمة مطابقة |

المصدر القديم في `collections/sales/reading/SALES_BATCH_2026-10-11_001.json`
كان دليل اختيار مساعدًا فقط. أعيد فحص المصدر الخام الحالي من الصفر؛ تطابقت
البصمة والحجم، وأعيد فحص locators القديمة، ثم حُفظت أدلة route أوسع وأكثر وضوحًا
في السجلات الجديدة. لا استُخدم batch القديم كبديل عن القراءة الحالية.

## قرار التصنيف

الزوج primary هو:

```text
sales / high_ticket_closing
confidence: medium
```

السبب: الغرض الغالب في المتن هو حجز مكالمات مبيعات عالية القيمة وتحويل العملاء
المحتملين عبر التأهيل والاكتشاف ومعالجة الاعتراضات. cold email حاضر كقناة وصول
وحجز وسياق حملات؛ لذلك سُجل كمرجع ثانوي bounded إلى
`outreach/cold_email_and_message_systems`، بلا نسخة ثانية وبلا احتساب دليل مستقل.

### أدلة موضعية أُعيد التحقق منها

المواضع صفرية البداية، بوحدة Unicode code point، وبحدود نصف مفتوحة `[start,end)`؛
المصدر كله في `line 1`.

| العائلة | locator | الاقتباس الحرفي | ما يثبته للتوجيه |
|---|---|---|---|
| purpose | `chars 0:210` | `Over the last 3 years, I have booked over 4,000 sales calls for myself and for my clients using one of the most consistent engines for producing high quality sales calls, and that is none other than cold email.` | الغرض العملي هو sales calls، مع cold email كقناة. |
| scope | `chars 914:1013` | `So the businesses cold email actually works for are mainly B2B businesses. There's rare exceptions.` | سياق جمهور القناة، لا ملكية primary وحده. |
| structure | `chars 6053:6202` | `And the reality of why, you know, people think the leads aren't qualified is really just because they don't do proper discovery in the sales process.` | حضور التأهيل والاكتشاف داخل sales process. |
| structure | `chars 6250:6286` | `They don't do any objection handling` | حضور معالجة الاعتراضات داخل العملية. |
| secondary context | `chars 25143:25217` | `The more specific you are, the better your campaigns are going to perform.` | صلة bounded بـoutreach والحملات. |

أعيد حساب hash لكل اقتباس من slice المتن: **5/5 PASS**. الاقتباسات أدلة route
وليست Claims مقبولة؛ لا يثبت أي منها الرقم أو السببية أو معيارًا عامًا.

## تغطية routing الدلالية

التغطية المحفوظة في `REF_...json` وmanifest التشغيل:

| segment | start | end | ملاحظة |
|---|---:|---:|---|
| `SEG_ROUTE_20261017_HIGH_TICKET_01` | 0 | 10,235 | الافتتاح، cold email، B2B، شروط السوق، ومقدمات حجز المكالمات |
| `SEG_ROUTE_20261017_HIGH_TICKET_02` | 10,235 | 20,471 | آلية الحملة، التأهيل، تحويل الردود، والأمثلة والسياق المجاور |
| `SEG_ROUTE_20261017_HIGH_TICKET_03` | 20,471 | 30,707 | التخصيص، المتابعة والاعتراضات، الحدود والخاتمة |

الاتحاد يساوي `[0,30707)` بلا gaps أو overlaps، و`unread_ranges=[]`. هذه تغطية
routing كاملة، لا extraction؛ `content_units=[]` عمدًا.

## التكرار والقيود التاريخية

- أُعيد فحص كل ملفات raw بحثًا عن hash مطابق نشط آخر: **0**.
- سجل `sources/SRC_NEW_b0140a4d41654bab_b1f4775a.md` موجود ويطابق المصدر الحالي.
- `raw/SOURCE_MANIFEST.tsv` يحوي تطابقًا واحدًا في السطر 780 لمسار legacy:
  `raw/legacy/brain/matthewlucero__The Best Way To Book High-Ticket Sales Calls in 2026__Kx3ZSv2NqVQ.txt`.
- هذا المسار legacy **غير موجود** حاليًا؛ لذلك سُجل صراحةً كـ
  `stale_legacy_manifest_reference`، لا كـduplicate نشط ولا كنسخة evidence ثانية.
- `duplicate_of: null` للمصدر الحالي؛ عدد الأدلة المستقلة المحتسب: **1**.

هذه الفجوة التاريخية لم تُخفَ ولم تُصلح في هذه المهمة؛ raw وmanifests القائمة
immutable خارج صلاحية route + copy.

## النسخة والmetadata

| artifact | الحجم | SHA-256 / الحالة |
|---|---:|---|
| `done/sales/high_ticket_closing/SRC_NEW_b0140a4d41654bab_b1f4775a.txt` | 30,707 | `sha256:b0140a4d41654babf5ec880c63fa0da5e68ff72a8a2e5611a4b5652b31bb0d54`؛ مطابق للأصل |
| `done/sales/high_ticket_closing/REF_SRC_NEW_b0140a4d41654bab_b1f4775a.json` | 12,705 | `sha256:67d698ad43d1b3833b8ff0f184462d9dc801c73740c284d432ce1d78fa2296dd` |
| `done/sales/high_ticket_closing/ROUTE_SRC_NEW_b0140a4d41654bab_b1f4775a.md` | 8,040 | `sha256:c2dd8097ff3171597c247327e86a2aacb5084036eb7b2308b4f031a82fdef90e` |
| `done/sales/high_ticket_closing/INDEX.md` | 1,769 | `sha256:38d6453e945641b023c8875efa55aa800e9e7cb49becca2d5a05d9e5f2f15616` |

نتائج `lstat` للنسخة والأصل: كلاهما regular، `symlink=false`، `st_nlink=1`،
`same_inode=false`. الحجم والبايتات والبصمة متطابقة، والأصل ثابت قبل/بعد النسخ.
الإنشاء كان exclusive ولم يحدث overwrite.

## raw pre/post وحراس عدم التعديل

جرد raw تم عبر `os.walk(followlinks=False)` و`lstat` وSHA-256 لكل regular file؛
بصمة الشجرة هي SHA-256 لأسطر JSON مرتبة من `(relative_path,type,size/hash)`،
وتشمل entries الدلائل كـ`other`. النتيجة قبل الكتابة وبعدها:

| الجذر | pre: entries / regular / symlink / other / bytes | pre tree SHA-256 | post | الحكم |
|---|---:|---|---|---|
| `raw/` | `1833 / 1820 / 0 / 13 / 50,898,163` | `5a18a1e3be5c8ac735be3d36197e71a2247afbca3763ab66fa0f839b111fb881` | نفس القيم والبصمة | **UNCHANGED** |
| `raw/new/` | `1776 / 1776 / 0 / 0 / 43,757,343` | `47739e2830fd37cf47e97862bb2d3d10d6556c6c65fabfa2dbf72c5e91cd4c29` | نفس القيم والبصمة | **UNCHANGED** |

حراس ملفات النطاق بعد التنفيذ (لم تُستهدف بالكتابة):

| الملف | post SHA-256 |
|---|---|
| `config/domain_catalog.json` | `sha256:3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add` |
| `config/processing_order.json` | `sha256:4c77a8ecc537149f571f2e43ecdb858abbafefffae89d96261b3a94834529b8c` |
| `collections/sales/manifest.json` | `sha256:1c729810fbc2ca115e7cf55a17fe4a891eea62f63195c7304182622efee92923` |
| `collections/corpus/manifest.jsonl` | `sha256:aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3` |
| `raw/SOURCE_MANIFEST.tsv` | `sha256:e4f32124d4615a69849d5a88ed3c8eb2d0899a884b0fc74ec300b2c74469098a` |

## فحوص الأدوات والبوابات

1. `python3 tools/wiki_workflow.py validate-batch --manifest staging/routing/ROUTE_RUN_20261017_HIGH_TICKET.json --json` — **PASS**؛ `ok=true`, `valid_entries=1`, `knowledge_requested=false`, `writes_performed=0`, `errors=[]`.
2. قراءة Python مستقلة للمصدر — **PASS**؛ full bytes، strict UTF-8، EOF،
   reread، stat stability، source hash.
3. verifier النسخة والـREF — **PASS**؛ JSON صالح، 5/5 quotes exact،
   refs الأربعة المعرفية كلها `[]`، route/extraction منفصلان.
4. post-scan raw — **PASS**؛ raw وraw/new unchanged كما في الجدول.
5. `python3 -m json.tool` على manifest التشغيل وREF — **PASS**.
6. فحص محلي للـINDEX والروابط النسبية — **PASS**؛ التعديل الوحيد في فهارس
   النطاق كان `done/sales/high_ticket_closing/INDEX.md`، ولم تُعدّل parent indexes.
7. `python3 tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json` — **PASS**
   في نطاقه المساعد (`ok=true`, `errors=[]`؛ sources=1781, claims=1777,
   concepts=34, masters=1). هذا الفحص العام لا يثبت route tree أو copy
   independence أو القراءة الدلالية؛ الأدلة الحاسمة أعلاه مستقلة.

الملفات التشغيلية الإضافية داخل الويكي:

- `staging/routing/ROUTE_RUN_20261017_HIGH_TICKET.json` — manifest route، hash
  `sha256:7272a417d35fe88387aa7b5770db09f1decc7a1cb389388ad966c56fd35a1b09`.
- `staging/routing/ROUTE_RUN_20261017_HIGH_TICKET.jsonl` — سجل عنصر التشغيل.
- `staging/routing/ROUTE_RUN_20261017_HIGH_TICKET_summary.json` — summary.
- `staging/routing/ROUTE_RUN_20261017_HIGH_TICKET_checks.md` — checks.

## حالات source والقيود المتبقية

- `REF.source_status` هو `new` كحالة workflow للتوجيه وفق نظام 14؛ لم يُعدّل
  سجل Source التاريخي الذي يقرأ `processed`. تلك القيمة التاريخية لا تُعامل
  دليلًا على `source_done`، وقد سُجلت في REF كـ`source_record_status_observed`.
- `source_extraction_status=not_started`؛ لا candidate Terms/Claims أو مراجعة
  استخراج في هذه المهمة.
- route batch لمصدر واحد، وليس inventory أو domain snapshot شاملًا؛ لا يغيّر
  حالة `sales` في config ولا يفتح domain آخر.
- المراجعة المنفذة self-check من Worker؛ لا يُدّعى independent reviewer منفصل.
- checkpoint المستقل: `checkpoints/ROUTE_COPY_HIGH_TICKET_2026-10-17.md`.
