# تقرير Worker — الأنظمة العامة متعددة المجالات v2

## الحالة وcheckpoint

- **التاريخ:** 2026-10-10.
- **الحالة الحالية:** `in_progress`؛ لم يُعلن إغلاق أي domain أو إنجاز معرفة.
- **الهدف:** كتابة الأنظمة 13 و15–19 وتحديث `systems/INDEX.md` فقط، مع فصل اكتمال المصدر والقسم والمجال، دون تغيير نظام التوجيه 14.
- **الخطوة التالية:** توثيق العقود الستة، ثم فحص الروابط والبنية والتوافق مع الأدوات الحالية، وإعادة قياس البصمات.
- **نطاق الكتابة:** الملفات السبعة المطلوبة داخل `/sdcard/NEXUS_LLM_WIKI/systems/` وهذا التقرير فقط. لا ملفات حالة تشغيلية جديدة، ولا Claims/Concepts/Masters/Terms/Source records، ولا تغيير raw أو المصادر القديمة، ولا نقل أو حذف.
- **ملكية القرار:** Worker يسلّم الأدلة؛ Commander يراجع التسليم ويغلق المهمة وTODO. لا تفويض فرعي، ولا استخدام Codex.

## ما تمت قراءته قبل التعديل

قراءة كاملة حتى EOF بأداة `read`:

| المرجع | الأسطر |
|---|---:|
| `/root/r/reports/sales-proof/USER_MESSAGES_SESSION_EF22.md` | 305 |
| `/root/r/reports/sales-proof/agent-multidomain-plan.md` | 95 |
| `/root/r/reports/sales-proof/agent-domain-selection.md` | 172 |
| `/sdcard/NEXUS_LLM_WIKI/MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md` | 233 |
| `/sdcard/NEXUS_LLM_WIKI/AGENTS.md` | 39 |
| `/sdcard/NEXUS_LLM_WIKI/SCHEMA.md` | 92 |
| `/sdcard/NEXUS_LLM_WIKI/README.md` | 56 |
| `systems/00_ARCHITECTURE.md` | 26 |
| `systems/01_SOURCE_INGEST.md` | 24 |
| `systems/02_CLAIM_EXTRACTION.md` | 28 |
| `systems/03_CONCEPT_AUTHORING.md` | 24 |
| `systems/04_MASTER_AUTHORING.md` | 90 |
| `systems/05_RETRIEVAL_AND_EVALUATION.md` | 33 |
| `systems/11_AGENT_EXECUTION_CONTRACT.md` | 84 |
| `systems/12_ITERATION_AND_RISK_LOOP.md` | 74 |
| `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md` | 766 |
| `systems/INDEX.md` قبل التغيير | 22 |

قراءة إضافية للتوافق: الأنظمة 06–10 و99 كاملة، وتعليمات Nexus Brain في `CLAUDE.md` و`nexus_vault/AGENTS.md`. قُرئت ملفات المهمة السابقة `.opencode/todo.md` و`context.md` و`sync-issues.md` دون تغييرها أو إعلان إغلاق عملها؛ `status.md` غير موجود. لا توجد تعليمات إضافية داخل `systems/` وفق جرد `**/AGENTS.md`، و`/sdcard/AGENTS.md` غير موجود.

شُغّل الاستكشاف المحلي:

```bash
python3 /sdcard/Nexus_Brain/nexus_vault/planner.py "تصميم أنظمة عامة لويكي معرفة متعددة المجالات: فصل source_done وsubdomain_done وdomain_done، ترتيب المجالات، orchestration التسلسلي، الفهارس، إعادة معالجة المصادر الجديدة، وبوابات QA مع raw immutable" --format compact
python3 /sdcard/Nexus_Brain/rag/query.py --master Master_Systems_And_Workflow --section 4
python3 /sdcard/Nexus_Brain/rag/query.py --master Master_Systems_And_Workflow --section 15
```

الأوامر الثلاثة عادت بـexit code 0. استُخدمت أفكار توثيق handoff، حدود العمل الجاري، وQA فقط كمرجع تصميم عام، لا نسب/أمثلة الأعمال ولا ترتيب planner كمتطلبات. المرجع الملزم هو التكليف الحالي وملفات تشغيل الويكي.

محاولة تحميل مهارة `project-artifact` فشلت لأنها غير متاحة؛ استُخدمت `wiki-update` المتاحة بدلًا منها. تعليمات عدم السؤال وعدم توسيع النطاق لها الأولوية على خطوات الموافقة وتوليد فهارس خارج النطاق داخل المهارة؛ لا تشغيل مولد يكتب خارج الملفات المأذونة، ولا commit.

## التناقض المطلوب إصلاحه — نتيجة القراءة

- الخطة السابقة (`agent-multidomain-plan.md:21,49–53`) والميثاق (`§4,§8,§9`) يمكن أن يُفهما كأن كل سجل مصدر يجب أن ينتظر Master المجال كله قبل إغلاقه.
- النظام 14 يفصل أصلًا `route_status: done` عن المعرفة: `Source.status: processed` وإيداع route/reference في `done/` يثبتان **التوجيه فقط**، لا اكتمال T/C/K ولا Master (`§3,§9,§12`). لن يُعدَّل هذا النظام.
- التصميم المطلوب: `route_done` موروث من 14؛ `source_done` بعد route + terms + claims + concepts + QA؛ `subdomain_done` بعد تكامل مصادر القسم؛ `domain_done` وحده يتطلب بوابة Master واعتماد المجال. يجب ألا يصبح وجود ملف داخل `done/` اختبارًا لاكتمال المجال.
- تظهر الفجوات والخلافات حتى بعد القبول؛ لا يشترط الوصول لإجماع مزيف. المانع هو نقص الدليل/العمل المطلوب أو إخفاء الخلاف، لا وجود رأي مخالف موثق.

## baseline قبل الكتابة

أُجري فحص قراءة فقط: لكل مجلد رتبت الملفات، وسُجل لكل ملف `relative_path<TAB>size<TAB>sha256`، ثم SHA-256 للأسطر مجمعة بـnewline بدون newline نهائي. يشمل العد ملفات الفهرس، لذا ليس عدًّا للسجلات المعرفية.

| النطاق | عدد الملفات | manifest SHA-256 |
|---|---:|---|
| `raw/` | 1820 | `2cbd868afee7a1023ef9c00bd0a7cc600b96ec9cd8c4ca9fd75c8d34bb0b0b0f` |
| `claims/` | 1778 | `abb8a2584a999d844e35421d979aed8f8b427ab0de3e81b356995d42a3991d96` |
| `concepts/` | 35 | `f4ead1df3686e4215db96eeb2e4ca3ee9c889fe2fb299532cb60cffa4081dba6` |
| `masters/` | 3 | `d13798f38ca5e1891a5b064e5c63778fa3c28b83447f2c34552b09390fd61d94` |
| `sources/` | 1782 | `a20bc28454755f0178271381195169be3055170701b4f51a79cf91a17d371023` |

- `systems/14_SOURCE_ROUTING_AND_DONE_TREE.md`: 39019 bytes، SHA-256 `bacbb4bd068cd20f28f26fb45b5cfc73be880484d7514a6d6ea7ea7b24179356`.
- `systems/INDEX.md` قبل التغيير: 1212 bytes، SHA-256 `c5b8d1fb8e4a141a422386798719184a78555c8511a603e842a89e5122c2eb8f`.
- الستة المستهدفة غير موجودة قبل العمل وفق جرد الأنظمة.
- `git_status` أظهر working tree واسعًا غير متتبع من جذر البيئة، وليس baseline موثوقًا لملفات هذه الويكي؛ ستستخدم مقارنة بصمات القرص لا افتراض نظافة git.

## الفحوص والنتيجة النهائية

### اكتشاف التوافق وbaseline الاختبارات

- قُرئت `tools/wiki_quality.py` (218 سطرًا) و`tools/bulk_ingest.py` (130 سطرًا) كاملتين، وفهارس sources/claims/concepts/masters وcheckpoints ذات الصلة. لا يوجد `tools/wiki_build_index.py`؛ وظيفة `build_index` داخل `wiki_quality.py` هي الموجودة، وتكتب فهرسًا عامًا لا الفهارس المحلية. لم تُشغَّل.
- أداة الجودة تقرأ أربع طبقات فقط، ولا تفحص الأنظمة أو المصطلحات أو الأقفال أو سجلات الإغلاق. `bulk_ingest.py` لا يصلح لإثبات التوجيه الكامل أو صفر آثار (`--no-write` ينشئ مجلدات). لن يُشغّل.
- ظهرت بنية `done/<domain>/source_refs/<subdomain>/` وفهارسها وملفا `config/domain_catalog.json` و`config/processing_order.json` أثناء القراءة؛ قُرئت الإعدادات كاملة (476 و141 سطرًا) وعينة فهارس sales. هذه ملفات خارج ملكية Worker ولا تعدّل. الإعدادات تقول sales=in_progress والباقي pending، وsubdomains=provisional، وليست إغلاقًا معرفيًا.
- توجد فروق تحتاج تصريحًا في العقود الجديدة: 14 يحدد route تحت `done/<domain>/<subdomain>/` بينما الهيكل الآخر يضع `source_refs/`؛ الإعدادات تستخدم quarantine المنطقي لمعنى أوسع من فشل السلامة في 14؛ وأسماء `offers_pricing` و`content` في ingest ليست IDs المجالات الحالية. ستوثق الحدود دون تعديل الملفات الخارجية أو نقل أي محتوى.
- الأمر الفعلي `python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json` قبل الإنشاء: **exit 0**، `ok=true`, `errors=[]`؛ sources=1781 (processed=1772/quarantined=9)، claims=1777 (reviewed=93/candidate=1684)، concepts=34 (reviewed=27/draft=7)، masters=1 (draft). هذه نتيجة بنيوية لا اعتماد مجال.
- فحص RED قبل الإنشاء (Python قراءة فقط): الستة المستهدفة غير موجودة، ومداخلها الستة غير موجودة في INDEX؛ **exit 1 متوقع**. تحقق أيضًا أن بصمة 14 تطابق baseline. سيُحتفظ بأمر هذا الفحص في التقرير مع نتيجة GREEN بعد الإنشاء.

ما زالت فحوص ما بعد الكتابة غير منفذة. لا PASS عام مستنتج من النتائج أعلاه.
