# تقرير route + copy — `SRC_NEW_34aaffac87a9dd7f_0535de17`

**التاريخ:** 2026-10-17  
**النطاق:** مصدر واحد، توجيه ونسخة مستقلة فقط  
**الحكم:** `route_done` للتوجيه والنسخ وmetadata؛ `source_extraction_status=not_started`

## 1. نطاق التنفيذ والقيود

نُفذت المهمة للمصدر المحدد في:

```text
collections/sales/reading/SALES_BATCH_2026-10-11_001.json
```

وقُرئ المصدر الخام نفسه كاملًا من:

```text
raw/new/smartleadai__How to Close 500+ Sales Opps in 90 Days with David Lehnert__DhzsNovGxgM.txt
```

المسار الأساسي المحسوم من متن المصدر هو:

```text
done/sales/proposal_follow_up_pipeline/
```

طُبقت القيود التالية:

- لا تعديل أو نقل أو إعادة تسمية أو حذف داخل `raw/`.
- لا تعديل لـ`collections/corpus/manifest.jsonl` أو `config/domain_catalog.json`.
- لا تعديل لفهرس parent مشترك مثل `done/sales/INDEX.md` أو `reports/INDEX.md`.
- لا إنشاء Terms أو Claims أو Concepts أو Masters أو Source record جديد.
- لا Codex ولا subagents.
- المصدر القديم في reading batch دليل مساعد فقط؛ hash وbytes وEOF والاقتباسات
  أُعيد التحقق منها من الملف الخام الموجود على القرص.

## 2. المخرجات المنشأة

| الملف | الوظيفة | الحجم | SHA-256 |
|---|---|---:|---|
| `done/sales/proposal_follow_up_pipeline/SRC_NEW_34aaffac87a9dd7f_0535de17.txt` | نسخة regular byte-exact | 70,159 | `34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d` |
| `done/sales/proposal_follow_up_pipeline/REF_SRC_NEW_34aaffac87a9dd7f_0535de17.json` | route/reference metadata | 15,101 | `4e7f06a1135332d6e265241c59ad899a2b42373da0b8cb19502a6923c7901797` |
| `done/sales/proposal_follow_up_pipeline/ROUTE_SRC_NEW_34aaffac87a9dd7f_0535de17.md` | قرار التوجيه وفحوص G0–G8 | 10,941 | `aec2e61509b7c8e4f66b555a870677cde0e5f84799d8f6971bb8a4ac563bb991` |
| `done/sales/proposal_follow_up_pipeline/INDEX.md` | تحديث الفهرس المحلي للمجلد فقط | 1,495 | `0ddcd3d4adb36914b33d5090d078518c4df7be0cbfb3645840a9ded6a1fd3a96` |

لم توجد destination قبل النسخ؛ أُنشئت النسخة regular بـ`O_EXCL` دون overwrite.

## 3. إعادة التحقق من المصدر الخام

| الفحص | النتيجة |
|---|---|
| bytes expected/read | `70,159 / 70,159` — PASS |
| UTF-8 strict decode | PASS؛ `decode_replacements=0` |
| Unicode code points | `70,159` |
| line count | `1`؛ لا newline نهائي |
| EOF | PASS |
| إعادة القراءة | `bytes_equal_on_reread=true`، `stable_after_read=true` |
| SHA-256 | `sha256:34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d` |
| reading batch hash | مطابق، لكنه لم يُستخدم بدل القراءة الحالية |

الـread coverage في REF تستخدم mode=`routing` وثلاثة segments متصلة:

```text
[0,23386) + [23386,46772) + [46772,70159) = [0,70159)
```

و`unread_ranges=[]` و`content_units=[]`. المراجعة المسجلة هي
`worker-self-check` وليست مراجعة مستقلة.

## 4. قرار التوجيه وأدلة المتن

```text
primary_domain:    sales
primary_subdomain: proposal_follow_up_pipeline
confidence:        medium
```

الغرض الغالب هو شرح أنظمة توليد الفرص وبناء pipeline، ثم تحويل الردود إلى
مكالمات ومسار عرض وCTA. cold email والأدوات والبحث عن جهات الاتصال والتسليم
والرسائل حضورها قوي، لذلك سُجلت إحالة bounded إلى
`outreach/outreach_mechanics_and_follow_up`، دون نسخة ثانية أو عدّ دليل مستقل.

الاقتباسات التالية أُعيد حسابها من النص الخام بمواضع صفرية البداية ونصف مفتوحة
بوحدة Unicode code point:

| العائلة | locator | الدليل الحرفي المختصر |
|---|---|---|
| purpose | `chars 1452:1686; line 1` | `exact systems, copies, tools, and workflows` التي ساعدت في توليد `521 opportunities` و`$2 million pipeline` |
| actions | `chars 37960:38215; line 1` | `solution` ثم `proposal` ثم `remedy` ثم `CTA` |
| structure | `chars 13900:13932; line 1` | `every table just has one purpose` |
| structure | `chars 46416:46469; line 1` | `hook, pain, proof, remedy, and a CTA` |

النصوص الكاملة، offsets، و`quote_sha256` محفوظة في REF. لا تمثل هذه الأدلة
Claims مقبولة؛ هي أدلة تصنيف فقط.

## 5. فحص التكرار والهوية

حُفظت نتيجة الفحص التفصيلية في REF. الخلاصة:

- `collections/corpus/manifest.jsonl:1406` يسجل نفس bytes تحت
  `SRC_CORPUS_raw_new_34aaffac87a9dd7f_6f8e239dbeeb` ومسار `raw_new`؛ هذا
  تسجيل لنفس المحتوى لا مصدر مستقل.
- `raw/SOURCE_MANIFEST.tsv:4964` يحمل hash نفسه لمسار
  `raw/legacy/brain/...`، لكن جرد `raw/legacy/brain` قبل/بعد كان خاليًا؛ لذلك
  هو `stale_reference` لا نسخة موجودة.
- `duplicate_of=null` للمصدر المطلوب، و`independent_evidence_count=1`.

## 6. تحقق النسخة والاستقلال

| الخاصية | الأصل | النسخة | الحكم |
|---|---:|---:|---|
| الحجم | 70,159 | 70,159 | PASS |
| SHA-256 | `34aaffac…d97b83d` | `34aaffac…d97b83d` | PASS |
| regular | `true` | `true` | PASS |
| symlink | `false` | `false` | PASS |
| hardlink | `false` | `false` | PASS |
| same inode | — | `false` بالنسبة للأصل | PASS |
| link count | `1` | `1` | PASS |
| الأصل بعد النسخ | ثابت | — | PASS |

المقارنة كانت byte-for-byte، إضافة إلى SHA-256 والحجم و`lstat`؛ لا تعتمد على
اسم الملف أو metadata وحدها.

## 7. raw pre/post وحراس الملفات المحمية

جُردت شجرة `raw/new` بـ`os.walk(followlinks=False)` و`lstat` وSHA-256 لكل
regular file قبل الكتابة وبعدها. استُخدمت بصمة شجرة deterministic لمصفوفة
`(relative_path, bytes, sha256)` المرتبة:

| الجذر/الملف المحمي | قبل | بعد | الحكم |
|---|---|---|---|
| `raw/new` | 1,776 ملفًا؛ 43,757,343 bytes؛ `571243cdbc520c67961627bcd76e73ead52f2579492dbf7bfd638450602a5140` | نفس العدد والحجم والبصمة | UNCHANGED |
| المصدر الخام المحدد | 70,159؛ `34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d` | نفسهما | UNCHANGED |
| `collections/corpus/manifest.jsonl` | 1,614,698؛ `aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3` | نفسهما | UNCHANGED |
| `config/domain_catalog.json` | 31,397؛ `3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add` | نفسهما | UNCHANGED |
| `done/sales/INDEX.md` (parent) | 3,452؛ `d8939a1afed2e29b1c8ec2b97fc43749fa482fdb8b04513bc50228983233314f` | نفسهما | UNCHANGED |
| `reports/INDEX.md` (parent) | 1,773؛ `0e2c64cf9057d4754cb5ba76bfec5787bd229d5c35fbff65e1be06d881b8698e` | نفسهما | UNCHANGED |

`raw_new_tree` لا يتضمن الملفات الجديدة لأن النسخة تحت `done/`. لم تُستخدم
نتيجة Git للمساحة لأنها ليست Git repository؛ دليل عدم التعديل هنا هو جرد
القرص والبصمات قبل/بعد.

## 8. بوابات النتيجة

| البوابة | الحكم |
|---|---|
| G0 الهوية والمسار | PASS |
| G1 سلامة IO | PASS |
| G2 SHA-256 | PASS |
| G3 duplicate check | PASS؛ المراجع المطابقة غير مستقلة ومعلّمة |
| G4 routing read coverage | PASS؛ كامل النص، self-check فقط |
| G5 primary catalog route | PASS؛ `sales/proposal_follow_up_pipeline` موجود في catalog |
| G6 secondary references | PASS؛ bounded reference مع locators |
| G7 independent copy + metadata | PASS |
| G8 raw integrity + local index | PASS |

الفحص المساعد `python3 tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI
--json` مرّ برمز خروج 0، `ok=true`، و`errors=[]`، مع counts مقيسة على القرص:
sources=1,781، claims=1,777، concepts=34، masters=1. لا يفحص هذا الأمر
استقلال نسخة `done/` أو quote offsets أو G0–G8، ولا يثبت `source_done`؛ الأعداد
المذكورة موجودة مسبقًا وليست مخرجات هذه المهمة.

بناءً على ذلك فقط تم تسجيل `route_status=route_done`. بقي
`source_extraction_status=not_started`، ولم يُرفع `source_done` أو `domain_done`.

## 9. الملفات المقروءة وعدم التنفيذ

قُرئت العقود المطلوبة: `AGENTS.md` و`SCHEMA.md` و
`systems/14_SOURCE_ROUTING_AND_DONE_TREE.md` و`config/domain_catalog.json`.
وقُرئ JSON batch كاملًا، ثم الملف الخام كاملًا على دفعات متجاورة حتى EOF.

لم يُنفذ عمدًا:

- تعديل raw أو corpus manifest أو config أو parent indexes.
- تعديل Source record القديم ذي `status=processed`.
- استخراج أو كتابة Terms/Claims/Concepts/Masters.
- إنشاء secondary copy أو legacy `source_refs` artifact.
- إعلان snapshot/domain/source completion.

## 10. الخلاصة

المصدر المطلوب الآن له نسخة مباشرة مستقلة byte-exact وREF وROUTE وفهرس محلي.
كل شروط النسخة والبصمة والاستقلال وسلامة raw اجتازت الفحص، لذلك حالة التوجيه
النهائية هي `route_done` ضمن نطاق هذه العملية. هذا لا يغيّر حالة المعرفة ولا
يثبت اكتمال الاستخراج أو المجال.
