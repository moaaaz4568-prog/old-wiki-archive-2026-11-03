# تقرير توجيه corpus — `ROUTE_BATCH_2026-10-14_001`

## الحكم المختصر

أُنجزت قراءة توجيهية كاملة لخمسة سجلات حقيقية متنوعة، مع إعادة حساب البايتات وSHA-256 والوصول إلى EOF لكل سجل. هذه **دفعة routing من 5 فقط** وليست snapshot كاملة، ولا تغلق مصدرًا أو subdomain أو domain، ولا تنشئ نسخًا في `done/` أو route artifacts نهائية.

الملف التنفيذي الوحيد لسجل الدفعة هو:

```text
collections/corpus/route_batches/ROUTE_BATCH_2026-10-14_001.json
```

والنقطة الحالية:

```text
checkpoints/CORPUS_ROUTE_2026-10-14_001.md
```

**مهم:** `semantic_read=true` موجود في سجل الدفعة فقط. لم يُعدَّل `collections/corpus/manifest.jsonl`، وتبقى سجلاته الـ2,541 غير مصنفة دلاليًا؛ هذه الدفعة لا تغيّر ذلك المقام.

## القيود الحاكمة التي طُبقت

- قُرئت `AGENTS.md` و`SCHEMA.md` و`systems/14_SOURCE_ROUTING_AND_DONE_TREE.md` و`systems/15_DOMAIN_COMPLETION_GATES.md` و`config/domain_catalog.json` و`collections/corpus/manifest.jsonl` وتقارير الجرد وingest والـREADME.
- قُرئ أيضًا `/sdcard/Nexus_Brain/CLAUDE.md` و`/sdcard/Nexus_Brain/nexus_vault/AGENTS.md` لأن أحد السجلات من Nexus Brain، دون تحميل كل الويكي أو استخدام `_archive/` كمصدر نشط.
- corpus الخام immutable: لا تعديل أو نقل أو إعادة تسمية أو حذف.
- القرار مبني على الغرض والبنية والأفعال والحدود في **متن المصدر**؛ الاسم والمسار ليسا دليلًا منفردًا.
- البصمة على البايتات الأصلية، والمواضع في JSON هي Unicode code-point offsets صفرية وبحدود نصف مفتوحة `[start,end)`، مع locator سطري مساعد.
- لا توجد أي طبقة معرفة مشتقة في هذه المهمة. لا extraction ولا كتابة لملفات المعرفة الحالية.

## تعارض catalog الحالي مع مقترح الـ26

الملف الفعلي `config/domain_catalog.json` (`schema_version=3.0`) يعرّف 4 domains فقط:

```text
sales · outreach · pricing_offers · content_strategy
```

أما `reports/FULL_DOMAIN_CATALOG_PROPOSAL_2026-10-11.md` فيصف 26 عنقودًا canonical كـ**proposal غير معتمد**، وهو لا يغيّر config. لذلك:

- المسارات الموجودة في config سُجلت `catalog_status=current_config`.
- `systems_workflow/workflow_documentation` و`platform_strategy/algorithm_signals` مستعملان كمرشحين من proposal الـ26 فقط، مع `catalog_status=proposal_only_not_in_current_config`.
- لم تُضف هذه المسارات إلى config، ولم تُفتح مجالات معرفة جديدة.

حراس الهوية قبل الكتابة:

| الملف | البصمة/الحالة |
|---|---|
| `collections/corpus/manifest.jsonl` | `sha256:aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3` |
| `config/domain_catalog.json` | `sha256:3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add`، 31,397 بايت |
| مقترح الـ26 | `sha256:80e388e6e8e4ee299841981b83e1c114081db2e1887d5767ab2d130a3be31c10` |

## السجلات الخمسة

| # | manifest | الدور | primary | الحالة | bytes | SHA-256 المختصر | duplicate |
|---:|---:|---|---|---|---:|---|---|
| 1 | L31 | `raw/new` | `sales / objection_handling` | current, high | 7,118 | `4524d7f6fa7e68e3…` | مجموعة 4؛ المختار primary |
| 2 | L26 | `raw/new` | `outreach / cold_email_and_message_systems` | current, high | 17,849 | `e670a5dc5e90873b…` | مجموعة 2؛ المختار primary |
| 3 | L1816 | `raw/context` | `systems_workflow / workflow_documentation` | proposal-only, medium | 12,121 | `161c4def42c74393…` | hash فريد |
| 4 | L1948 | `/sdcard/Nexus_Brain/brain` | `platform_strategy / algorithm_signals` | proposal-only, high | 20,386 | `41033da306598a79…` | duplicate غير primary؛ primary في raw/new |
| 5 | L2416 | `nexus_vault` نصي غير INDEX | `outreach / cold_email_and_message_systems` | current, high | 105,726 | `a2cd145eb439d26b…` | hash فريد |

كل سجل في JSON يضم `read_audit` و`read_coverage` وsegments متصلة تغطي كامل view، إضافة إلى البصمة الفعلية وقرار primary والمراجع الثانوية. لا يضم أي سجل نسخًا أو `copy_path` نهائيًا.

## دليل التوجيه من متن المصادر

### 1) اعتراض sales — `SRC_CORPUS_raw_new_4524…`

- `chars 0:77; line 1`: «هذه واحدة من أهم الاعتراضات والحاجات التي تخسرك السيلز، للأسف تخصرك المبيعات.»
- `chars 1135:1159; line 1`: «حسناً. دعني أفكر في ذلك.»
- `chars 3576:3605; line 1`: «تتفهم معه على يوم. ما يهربش.»

هذه المواضع تثبت أن الغرض معالجة اعتراض تأجيل القرار ومتابعته داخل sales، لا بناء تسعير. أضيفت إحالة ثانوية bounded إلى `pricing_offers/guarantees_risk_reversal_and_price_objections` لأن المتن يذكر القيمة/الدفع كسبب تردد، دون أن تصبح الإحالة دليلًا مستقلًا أو primary ثانيًا.

### 2) رسالة cold outreach — `SRC_CORPUS_raw_new_e670…`

- `chars 65:132; line 1`: «الناز دي عندها مشكلة كبيرة جداً في الحاجات اللي علاقة بالأوتريتشنج.»
- `chars 3480:3540; line 1`: «الكلداوتريش دا بالضبط كأن انا جبت شخص one on one انا معرفوش».
- `chars 7326:7361; line 1`: «حط له لينك معين مثلا ممكن يحجز منه.»
- `chars 7435:7457; line 1`: «اعمل بوت في ميني شات.»

البنية والغرض كلاهما يثبتان outreach: مشكلة الرسائل، التواصل مع شخص غير معروف، CTA، وآلية استجابة/حجز. توجد إحالة ثانوية إلى `pricing_offers/guarantees_risk_reversal_and_price_objections` فقط لأن الهدية والضمان والبونص تظهر كعناصر مساعدة لقبول العرض داخل الرسالة.

### 3) سياق التشغيل — `SRC_CORPUS_raw_context_161c…`

- `chars 964:998; lines 18:18`: «## القسم (ب): الماسترز — كيف تُبنى».
- `chars 1980:2077; lines 27:27`: «سكربت توجيه كل مفهوم إلى قطاعه الأساسي…».
- `chars 2180:2259; lines 28:28`: «الوكلاء يتفرّغوا للدمج الدلالي بس، والبناء الميكانيكي يسير عبر سكربت حتمي».
- `chars 2278:2317; lines 30:30`: «## القسم (ج): تقسيم المجلدات لحد GitHub».

الغرض الظاهر هو workflow/documentation وحوكمة بناء الويكي. لأن هذا الزوج موجود في proposal الـ26 فقط، لا في config الحالي، بقي decision provisional ولم يُحوّل إلى مجال تشغيلي معتمد. لم تُستخرج منه قواعد معرفة.

### 4) شرح social-media algorithm — `SRC_CORPUS_nexus_brain_brain_4103…`

- `chars 0:164; line 1`: «Today we're talking about the social media algorithm…».
- `chars 3320:3407; line 1`: «The algorithm uses its fit score to pick roughly 200 people…».
- `chars 11176:11212; line 1`: «The first one is average watch time.»
- `chars 19364:19497; line 1`: «The only thing that matters is making great videos for a specific avatar group…».

هذه أدلة متن مباشرة على `platform_strategy/algorithm_signals`. السجل duplicate لـraw/new بالبصمة نفسها (`duplicate_of=SRC_CORPUS_raw_new_41033…`)، لذلك لا يزيد عدد المصادر أو وزن الدليل. الإحالة الثانوية إلى `content_strategy/distribution_calendar_and_measurement` محدودة بمواضع audience/topic/measurement.

### 5) مادة cold-email نصية من vault — `SRC_CORPUS_nexus_brain_nexus_vault_a2cd…`

هذا الملف `01_outreach/Master_Cold_Email_System.md` مادة Markdown نصية، وليس INDEX، وليس داخل `_archive/`؛ قُرئ من السطر 1 إلى 1616. أدلة الغرض:

- `chars 1431:1490; lines 37:37`: «Cold Email يعمل لأنه يستغل انقطاع الاهتمام (Attention Gap).»
- `chars 13535:13593; lines 347:347`: «نظام 10: Cold Outreach Workflow (7 خطوات — محمد أسامة)».
- `chars 16517:16567; lines 414:414`: «كل إيميل زاوية مختلفة + Variable جديد في كل متابعة».
- `chars 33929:34025; lines 925:925`: إعداد دومين و`SPF/DKIM/DMARC` ضمن Deliverability Stack.

هذا يثبت outreach/message systems من المتن. إحالة sales الثانوية bounded بموضعي `PSL → VSL → CTA` و«الـ Outreach يجلب الاهتمام. المهارة البيعية تحوّله.»؛ لا تجعل الـvault مرجعًا canonical تلقائيًا للـraw الجديد.

## سلامة IO والبصمات

تمت إعادة قراءة كل ملف مرتين في فحص Python مستقل، مع مقارنة `stat` قبل/بعد، و`read(1)==b''` لإثبات EOF، وUTF-8 strict decode. النتيجة:

| source_id | bytes expected/read | EOF | stable | bytes equal reread | replacements | chars/lines |
|---|---:|---|---|---|---:|---:|
| `…4524d7f6…` | 7,118 / 7,118 | PASS | PASS | PASS | 0 | 4,039 / 1 |
| `…e670a5dc…` | 17,849 / 17,849 | PASS | PASS | PASS | 0 | 10,107 / 1 |
| `…161c4def…` | 12,121 / 12,121 | PASS | PASS | PASS | 0 | 7,393 / 98 |
| `…41033da3…` | 20,386 / 20,386 | PASS | PASS | PASS | 0 | 20,386 / 1 |
| `…a2cd145e…` | 105,726 / 105,726 | PASS | PASS | PASS | 0 | 69,935 / 1,616 |

SHA-256 الكامل لكل سجل، و`view.sha256`، محفوظان في JSON ويطابقان manifest. لا توجد replacement characters. segments متصلة: `[0,4039)`, `[0,10107)`, `[0,2318)+[2318,4970)+[4970,7393)`, `[0,20386)`, و`[0,10666)+[10666,23293)+[23293,37567)+[37567,61154)+[61154,69935)`.

## فحوص عدم التعديل

جردت الجذور الخام الأربعة قبل كتابة JSON/التقرير وهذه النقطة باستخدام `os.walk(followlinks=False)` و`lstat` وSHA-256 لكل regular file. بصمة الشجرة هي SHA-256 لمصفوفة مرتبة من `(relative_path, bytes, sha256)`:

| الجذر | قبل: ملفات/بايتات | tree SHA-256 قبل |
|---|---:|---|
| `raw/new` | 1,776 / 43,757,343 | `5ad5c8798e5d248fb20ef47d374b5204b6bbf74722a037cfedaa095e1a56deb2` |
| `raw/legacy/brain` | 0 / 0 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| `raw/legacy/chats` | 39 / 6,148,975 | `e739b3d0dbc8be5902a1fc4cad759b2560f8e84b92724824f6c8b2be785a8c76` |
| `raw/context` | 3 / 252,610 | `592c21bb2d65f897ad0e97bad6046f337a77f914976a71e5d902069320441e39` |

النسخة اللاحقة من الفحص أعلاه، بعد إنشاء المخرجات الثلاثة، مطلوبة في قسم سجل الأوامر أدناه قبل اعتماد التقرير. لا يمكن أن تكون هذه المخرجات نفسها داخل `raw/`.

## سجل الأوامر والنتائج والقيود

1. `python3 /sdcard/Nexus_Brain/nexus_vault/planner.py "توجيه دفعة corpus ..." --format compact` — **PASS/استكشاف فقط**؛ أعاد مرشحين من الماسترز، ولم يُستخدم كقرار توجيه أو بديل للمتن.
2. ماسح Python لـ`manifest.jsonl` — **PASS**: 2,541 سطرًا JSON، السجلات الخمسة في L26/L31/L1816/L1948/L2416، والبصمة الكاملة للmanifest قبل الكتابة أعلاه.
3. ماسح Python للملفات الخمسة — **PASS 5/5**: bytes/hash/EOF/UTF-8/ثبات/إعادة قراءة؛ التفاصيل في `read_audit` داخل JSON.
4. `python3 -m json.tool collections/corpus/route_batches/ROUTE_BATCH_2026-10-14_001.json` — **PASS** بعد كتابة الدفعة.
5. فحص Python لبنية الدفعة — **PASS**: `records=5`، `semantic_read` موجود أعلى الدفعة فقط، `record semantic_read keys=0`، و`unread_ranges=[]` لكل السجلات.
6. فحص عدم تعديل raw بعد الكتابة — **PASS**: `raw/new=1,776/43,757,343/5ad5c8798e5d248fb20ef47d374b5204b6bbf74722a037cfedaa095e1a56deb2`، `raw/legacy/brain=0/0/4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`، `raw/legacy/chats=39/6,148,975/e739b3d0dbc8be5902a1fc4cad759b2560f8e84b92724824f6c8b2be785a8c76`، `raw/context=3/252,610/592c21bb2d65f897ad0e97bad6046f337a77f914976a71e5d902069320441e39`؛ كل count/bytes/tree hash طابق baseline.
7. `git -C /sdcard/NEXUS_LLM_WIKI status --short --untracked-files=all` — **UNAVAILABLE/قيْد بيئي**: المساحة ليست Git repository (`fatal: not a git repository`). لا يُفسَّر ذلك كفحص عدم تغيير.
8. مسح كامل لكل شجرة الويكي خارج المخرجات — **TIMEOUT** عند `120000 ms` قبل إكماله؛ لم تُستخدم نتيجة timeout كدليل نجاح. جرى الاكتفاء بجرد raw المحدد وبفحوص الملفات/manifest/config المستهدفة.
9. `lsp_diagnostics` على JSON والتقرير والcheckpoint — **PASS**: `No diagnostics found. All clean!` لكل ملف؛ هذه نتيجة بنيوية فقط ولا تثبت القراءة الدلالية أو بوابات R/T/C/K/M/QA.
10. verifier Python مستقل لسجل JSON — **PASS**: 5/5 manifest hashes، 5/5 byte counts، EOF، segments contiguous بلا فجوات، و**25/25** اقتباسًا حرفيًا (primary + secondary) يطابق offsets المحفوظة. بصمة JSON النهائية: `sha256:52be3c388e41d3d42527fe4fb0d30959d5e955400a05b8bade72516fd26d849f`. بصمات التقرير وهذه النقطة تُعاد طباعتها في تقرير التسليم النهائي بدل تضمين بصمة ذاتية داخل الملف نفسه.

## ما لم يُنفَّذ عمدًا

- لا `collections/corpus/manifest.jsonl` update، ولا config update، ولا Source records جديدة.
- لا نسخ مستقلة في `done/`، لا `REF_`، لا `ROUTE_<source_id>` نهائية، ولا `INDEX.md` جديد.
- لا استخراج أو كتابة لأي طبقة معرفة؛ route evidence فقط.
- لا إعلان `route_done` النهائي: التصنيف هنا batch provisional، والنسخة المستقلة وفحوص G7/G8 ليست ضمن التكليف.
- لا إعلان `source_done` أو `domain_done` أو `domain_terms_complete`.

## خلاصة التسليم

المخرج يثبت قراءة خمسة متون كاملة، hash/bytes/EOF، duplicate handling، primary واحدًا لكل سجل، ومراجع ثانوية bounded ذات أدلة موضعية. لا يثبت اكتمال corpus: **2,541 ما زالت غير مصنفة دلاليًا**، و`ROUTE_BATCH_2026-10-14_001` **batch=5 فقط وليس snapshot كاملة**.
