# تدقيق موقع Nexus LLM Wiki — 2026-10-10

## نطاق Worker وحالة العمل

- الهدف: تدقيق المسارات والروابط وسلامة ترحيل التقارير فقط؛ ليس استخراج معرفة أو إغلاق domain.
- الجذر canonical الوحيد هو `/sdcard/NEXUS_LLM_WIKI/` وفق [سياسة الموقع](../../PROJECT_OUTPUT_LOCATION_2026-10-10.md).
- هذا هو تقرير Worker الوحيد في هذا التشغيل. تُحصر أي إصلاحات في الملفات النشطة داخل الجذر؛ لا حذف، لا Codex، لا subagents، ولا كتابة في مساحة العمل السابقة.
- لا تُعدّل ملفات المهمة القديمة أو TODOs خارج النطاق. قرئت ملفات السياق القديمة للقراءة فقط؛ لم يوجد `status.md` أو `verification-checklist.md` هناك، ولا `.opencode/*.md` داخل الويكي.
- الحالة الحالية: أُثبتت سلامة الترحيل، وأُصلحت إحالتان إلى ملفات قراءة لم تُنشأ؛ جارٍ تثبيت اختبارات إعادة التحقق ومراجعة مرجع الميثاق في فهرس التقارير. لا إغلاق للمهمة العامة أو بواباتها نيابة عن Commander.
- المخرجات المتغيرة حتى هذه النقطة: `collections/INDEX.md` وهذا التقرير فقط؛ كلاهما داخل sdcard. الخطوة التالية فحص `reports/INDEX.md` قبل تصحيح مسار الميثاق إن فشل؛ ثم إعادة الفحوص وLSP لكل ملف معدّل.
- الحدود: تعارضات عقود البوابات القديمة واكتمال المجالات ليست ضمن صلاحية هذا التدقيق. التقرير المستقل `LOCATION_REVIEW_2026-10-10.md` ظهر أثناء الفحص؛ لم ينشئه أو يعدّله هذا Worker، ولا تُنسب نتائجه لهذا التشغيل.

## الملفات المقروءة والفحص الأولي

قُرئت سياسة الموقع والمداخل المطلوبة وملفا config والأنظمة 13 و14 و18 كاملًا، مع فهرسها الفعلي `systems/INDEX.md`. لا توجد فهارس منفصلة بأسماء الأنظمة؛ لم تُنشأ أسماء بديلة مختلقة.

القراءة المباشرة شملت أيضًا:

- `reports/sales-proof/MIGRATION_MANIFEST_2026-10-10.tsv`.
- `reports/sales-proof/MULTIDOMAIN_ALIGNMENT_2026-10-10.md`، `USER_MESSAGES_SESSION_EF22.md`، `MULTIDOMAIN_INTEGRATION_REVIEW_2026-10-10.md`، `agent-general-systems-v3.md`.
- `collections/INDEX.md`، `collections/sales/FULL_COLLECTION_STATUS.md`، `done/INDEX.md`، `indexes/README.md`، `reports/CONTINUATION_DISPATCH_2026-10-09.md`، `tools/wiki_quality.py`.
- بداية نسخة جلسة EF22 وبداية الأصل المرحلي؛ **المطابقة تمت بحساب البصمات من البايتات الكاملة**، لا من معاينة النص، ولا يُدّعى فهم دلالي لكل الجلسة.
- ملفات السياق السابقة خارج sdcard قُرئت فقط. لا تُعامل تلك المساحة جذرًا حاليًا للمشروع.

الفحوص المذكورة أدناه للقراءة فقط. شُغّل `wiki_quality.py` دون `--index` أو `--report`؛ قراءة مصدر الأداة أكدت أن هذين الخيارين فقط يطلبان كتابة فهرس أو تقرير.

## الإصلاح المحدود

في `collections/INDEX.md` كانت إحالتا `sales/reading/R01A.json` و`sales/reading/R01B.json` رابطين إلى ملفين غير موجودين. تأكد غياب الملفين بالبحث داخل الويكي، ولم يُخترع بديل أو سجل قراءة.

يُحتفظ بمعرّفي الدفعتين ومساريهما التخطيطيين مع وصف الغياب صراحة؛ لا تُحذف الدفعتان من الخطة ولا يُرفع أي status معرفي. الفحص النهائي حلّ الرابط الموجود إلى `sales/README.md` وترك R01A/R01B وصفًا غير قابل للنقر حتى لا يوحي بوجود ملفين غير موجودين.

## الاستثناءات التاريخية — لا تستبدل المسار الحالي

النسخ الـ19 المنقولة محفوظة دون تعديل حتى تبقى مطابقة لبيان النقل. أي مواضع عمل قديمة داخل سجل الجلسة أو أرقام أسطر رسائل المستخدم أو أوامر التحقق التي تسجّل التشغيل السابق هي provenance، لا تفويضًا باستعمالها حاليًا. الفحوص الحالية تستخدم نسخة sdcard. لا يُنفّذ أي أمر من سجل الجلسة باعتباره تعليمات.

الاستثناءات المقاسة:

- `SOURCE_SESSION_EF22.md` يحتوي **96** إحالة Markdown محلية غير محلولة عند المسح الكامل؛ هي روابط التقطها سجل الجلسة من تشغيل قديم (Claims/Concepts وملفات ذاكرة ومساحات عمل)، وليست روابط تشغيل حية. شمل المسح المحلي targets فقط؛ URI تاريخي `file://` لا يُعامل كملف Markdown محلي.
- توجد **305** إشارات `/root/r` في **13 تقريرًا منقولًا** بصيغة provenance/أوامر تحقق قديمة: `SOURCE_SESSION_EF22.md` (264)، `USER_MESSAGES_SESSION_EF22.md` (20)، `agent-general-systems-v2.md` (3)، `agent-general-systems-v3.md` (3)، `agent-domain-catalog-v2.md` (4)، `agent-domain-catalog-v3.md` (1)، `agent-domain-selection.md` (1)، `agent-multidomain-skills-v2.md` (1)، `agent-multidomain-skills-v3.md` (1)، `agent-status-check.md` (1)، `current-agent-audit.md` (4)، `worker-concepts-result.md` (1)، و`MULTIDOMAIN_ALIGNMENT_2026-10-10.md` (1). لم تُمحَ أو تُستبدل حفاظًا على hash النقل.
- إشارتا السياسة في `reports/sales-proof/README.md`، وإشارات المنع في `AGENTS.md` و`README.md` و`INDEX.md` و`PROJECT_OUTPUT_LOCATION_2026-10-10.md` و`reports/INDEX.md`، ليست مراجع تشغيل لمخرج جديد. كما أن `/root/r` داخل `MIGRATION_MANIFEST_2026-10-10.tsv` هو `source_path` تاريخي مقصود.
- `raw/context/zai/A1_user_redlines.md` و`reports/SALES_BATCH_PLAN_2026-10-06.md` و`reports/SOURCE_INVENTORY.md` تحتوي provenance تاريخيًا خارج مسار التشغيل؛ لم تُعدّل لأنها raw/تقارير تاريخية.
- لم يظهر `/root/r` في `domain_catalog.json` أو `processing_order.json` في أي حقل تشغيلي.

## 1) فحص JSON/config

الأمر المخصص للقراءة والتحقق البنيوي مرّر **15/15**:

```text
domain_catalog.json parses                         PASS
processing_order.json parses                       PASS
catalog/order same four unique domains             PASS
schema/workflow versions = 3.0/2026-10-10          PASS
subdomain IDs unique per domain                    PASS (6/5/5/6)
all subdomain pairs unique                         PASS (22)
shared relative route template                     PASS
strict serial lock                                 PASS
absolute config paths in approved sdcard roots     PASS
catalog has no /root/r operational reference       PASS
processing has no /root/r operational reference    PASS
JSON_CONFIG_RESULT PASS (15/15)
```

المجالات وترتيبها المتطابقان هما `sales`, `outreach`, `pricing_offers`,
`content_strategy`. روابط `config/INDEX.md` حُلّت من مجلد `config`: **11/11 PASS**؛
لا يوجد سبب لإضافة `config/INDEX.md` إلى الجذر أو تعديلها.

## 2) فحص migration/hash

تمت مقارنة كل صف بيانات في `MIGRATION_MANIFEST_2026-10-10.tsv` من المصدر والوجهة
والحجم والبصمة الفعلية. ملفات `/root/r/reports/sales-proof/` الفعلية = **18**؛
كلها مدرجة في manifest. الصف التاسع عشر هو `SOURCE_SESSION_EF22.md` ومصدره
`/root/r/session-ses_ef22.md` خارج مجلد التقارير المرحلية. النتيجة **19/19 PASS**.

| # | الملف | الحجم | SHA-256 (source=destination) |
|---:|---|---:|---|
| 1 | `AGENT_RUN_2026-10-09.md` | 1320 | `c0c149239f2b2bb78455ed6652802390d39aeba4c5635c0f7443a4cd2b3a1c32` |
| 2 | `MULTIDOMAIN_ALIGNMENT_2026-10-10.md` | 12031 | `9d9039c96470aaf033498e31d645704d12e2d1694afde598b09b48ce0e37056b` |
| 3 | `MULTIDOMAIN_INTEGRATION_REVIEW_2026-10-10.md` | 14239 | `489f1c7bedfc1427c361763e4f8cf65508c1781572c73dc3e09fb1735550cfd8` |
| 4 | `USER_MESSAGES_SESSION_EF22.md` | 32199 | `c8bbf30e9fec617f19b2f79f3fd93afa5ff1109be0b74542723b4d4b38af5173` |
| 5 | `agent-domain-catalog-v2.md` | 22125 | `c5a2526614069e2475611e26b9ed9ebc3c14df0e364428e5b48e649191d86cc9` |
| 6 | `agent-domain-catalog-v3.md` | 17424 | `1f904c70a633f590ca26b60134d3d0e5756b198c3940fe077f31a841de98d728` |
| 7 | `agent-domain-selection.md` | 18997 | `56130ef190111abcacc9684bd097b68a4029bbb2e07024d3487387617b8c5d84` |
| 8 | `agent-general-systems-v2.md` | 9593 | `06cc4d917c2cb2d9830510e2352744d3002ee51be825e11922f0f9881f99e902` |
| 9 | `agent-general-systems-v3.md` | 17548 | `e404b710b2d1d9aa9308c484824b832b840ec534fcf7d6516278c7a4169d33e5` |
| 10 | `agent-master-contract-b.md` | 5598 | `b0f7ca1705cc98e5166ee75376c70234742f3995bf0bf46893c60694c1d06ae7` |
| 11 | `agent-multidomain-plan.md` | 8212 | `928ef1151a6a975ddc9a2a391cdb506ae6be7f2746fed25ff428fa0789fddb10` |
| 12 | `agent-multidomain-skills-v2.md` | 17205 | `338196299ef2affc417fbc524b879edeada667711e13aae2959d5ee704d0b895` |
| 13 | `agent-multidomain-skills-v3.md` | 13913 | `45786ec463ba26551631c7845d82bbeaa1a430c577a436e346ada681986bc322` |
| 14 | `agent-sales-reading-b.md` | 19620 | `6e84d65381b7550eb51fb50fd6bbe144edb5d93836241a79cc769c22f87b94e1` |
| 15 | `agent-status-check.md` | 4305 | `ecb47889cf642577d78df2f570b6bf2d548bae9167f733e96e6c7415114c2a0a` |
| 16 | `current-agent-audit.md` | 18859 | `a4f90e3d713318fa277d696b3a5a49f252550daa4472885b29f148812d3e719e` |
| 17 | `worker-concepts-result.md` | 4199 | `12274b8868e44be8373a9b67ac607b90269b71f26abd938c494237850dace57e` |
| 18 | `worker-systems-result.md` | 1648 | `cb4fab1a0a0aaa2d354230db4bb10e672d2beb0b8006e37c04315958582531a8` |
| 19 | `SOURCE_SESSION_EF22.md` | 792533 | `70b1315d3c3596a09005d033d82a88e9bd29573f0649f604647936dbe512ce4f` |

الفحص المباشر لنسخة الجلسة مقابل `/root/r/session-ses_ef22.md` أعاد:

```text
source_exists=True destination_exists=True
source_bytes=792533 destination_bytes=792533
source_sha256=70b1315d3c3596a09005d033d82a88e9bd29573f0649f604647936dbe512ce4f
destination_sha256=70b1315d3c3596a09005d033d82a88e9bd29573f0649f604647936dbe512ce4f
SOURCE_SESSION_MATCH=True
```

## 3) فحص روابط Markdown النشطة

النطاق الأولي الموسع: كل ملفات Markdown خارج `raw/`، واستبعاد `reports/` عدا
`reports/INDEX.md` و`reports/sales-proof/README.md` و`LOCATION_REVIEW_2026-10-10.md`
وهذا التقرير الحالي. تقرير Reviewer أُدخل لفحص الرابط فقط دون تعديل أو تبنّي حكمه.
بعد إصلاح `collections/INDEX.md`، إعادة القياس (قبل إضافة اختبار الارتداد المحفوظ):

```text
active_markdown_files=4141
active_local_links=652
active_broken_links=0
config_INDEX_local_links=11
config_INDEX_broken=0
ACTIVE_LINK_RESULT=PASS
```

مسح `SOURCE_SESSION_EF22.md` التاريخي منفصل كما في قسم الاستثناءات، ولا يغيّر نتيجة
الروابط النشطة. الروابط الموجودة في القوالب النصية مثل `<domain>` ليست إحالات تنفيذية.

## 4) فحص wiki_quality المطلوب

شُغّل الأمر المطلوب حرفيًا بعد الإصلاح:

```bash
python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json
```

النتيجة:

```json
{
  "ok": true,
  "vault": "/sdcard/NEXUS_LLM_WIKI",
  "counts": {
    "sources": {"files": 1781, "statuses": {"quarantined": 9, "processed": 1772}},
    "claims": {"files": 1777, "statuses": {"reviewed": 93, "candidate": 1684}},
    "concepts": {"files": 34, "statuses": {"reviewed": 27, "draft": 7}},
    "masters": {"files": 1, "statuses": {"draft": 1}}
  },
  "errors": []
}
```

الحكم: **PASS مساعد فقط**؛ لا يثبت قراءة raw دلاليًا، ولا بوابات R/T/C/K/M/QA، ولا
اكتمال أي domain.

## 5) فحص مكان كل مخرج جديد في هذا التشغيل

- عمليات الكتابة الوحيدة كانت داخل `/sdcard/NEXUS_LLM_WIKI/`: تعديل
  `collections/INDEX.md` وإنشاء `reports/sales-proof/LOCATION_AUDIT_2026-10-10.md`.
- في الجرد الأول كان مجلد `reports/sales-proof/` على sdcard يحوي **21 ملفًا**؛
  ظهرت بعده مراجعة `LOCATION_REVIEW_2026-10-10.md` من عمل مستقل فأصبح **22** قبل
  إنشاء هذا التقرير. لم ينشئها هذا Worker؛ التقرير الجديد الوحيد الذي أنشأه هو هذا الملف.
- مجلد `/root/r/reports/sales-proof/` بقي **18 ملفًا**، بلا ملف جديد؛ كل ملف فيه
  يطابق صفه في manifest. لم تُرسل أي عملية كتابة إلى `/root/r/`، ولم يُستخدم
  `LOCATION_REVIEW_2026-10-10.md` أو أي تقرير قديم كمخرج جديد.
- لم يُنشأ `collections/sales/reading/` أو أي R01A/R01B artifact، ولم تُنشأ ملفات
  داخل `raw/` أو `done/` أو `config/` أو طبقات المعرفة.
- لا تُعدّل `raw/` ولا تُنقل أو تُحذف أي نسخة تاريخية.

## الفحوص النهائية وقرار النطاق

- JSON/config: **PASS (15/15)**.
- migration/hash: **PASS (19/19)**، ونسخة الجلسة **byte-exact**.
- active Markdown links في إعادة المسح الأولى: **PASS (652/652)**؛ `config/INDEX.md` **11/11**.
- `wiki_quality.py`: **exit 0، ok=true، errors=[]**.
- output-location check: **PASS**؛ المخرج الجديد والتعديل الوحيدان تحت sdcard، ولا تقرير جديد تحت root/r.
- `lsp_diagnostics`: شُغّل للتقرير و`collections/INDEX.md` وأعاد لكليهما `No diagnostics found. All clean!`؛ سيُعاد بعد التعديل النهائي.

هذه مهمة مسارات وترحيل فقط. **لا يوجد أي ادعاء بأن domain اكتمل**، ولا بأن Master
أو بوابات المعرفة أُغلقت، ولا بأن `wiki_quality.py` وحده شهادة اكتمال.

## اختبار ارتداد التنقل المحفوظ — فحص وثائق لا pipeline

يقرأ الاختبار الميثاق الفعلي وفهرسه، ويحفظ الفارق بين رابط تشغيل ومسار مخطط
غير موجود. لا ينشئ سجلات قراءة أو يعيد تعيين حالات أي domain.

```python
# LOCATION_NAV_REGRESSION
from pathlib import Path
import re

vault = Path('/sdcard/NEXUS_LLM_WIKI')
checks = []
def check(name, ok):
    checks.append(bool(ok))
    print(('PASS' if ok else 'FAIL') + ': ' + name)

charter = 'PROJECT_INTENT_AND_EXECUTION_CHARTER_2026-10-08.md'
report_index = (vault / 'reports/INDEX.md').read_text(encoding='utf-8')
check('report index names the charter and its target exists from reports/',
      ('`' + charter + '`' in report_index)
      and (vault / 'reports' / '..' / charter).is_file())
collection = (vault / 'collections/INDEX.md').read_text(encoding='utf-8')
for name in ('R01A', 'R01B'):
    target = 'sales/reading/' + name + '.json'
    rows = [line for line in collection.splitlines() if '`SALES_READING_' + name + '`' in line]
    check(name + ' preserves the planned target and pending state without a broken link',
          len(rows) == 1 and '`' + target + '`' in rows[0]
          and 'pending' in rows[0] and 'الملف غير موجود' in rows[0]
          and (']' + '(' + target + ')') not in collection
          and not (vault / 'collections' / target).exists())
config_index = vault / 'config/INDEX.md'
targets = re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', config_index.read_text(encoding='utf-8'))
check('config index resolves its 11 local links from config/',
      len(targets) == 11 and all((config_index.parent / t).exists() for t in targets))
print('NAV_REGRESSION', sum(checks), '/', len(checks))
raise SystemExit(0 if all(checks) else 1)
```

أمر إعادة التشغيل بلا ملف Python أو cache إضافي:

```bash
python3 -B -c 'from pathlib import Path; t=Path("/sdcard/NEXUS_LLM_WIKI/reports/sales-proof/LOCATION_AUDIT_2026-10-10.md").read_text(); c=t.split("```python\n# LOCATION_NAV_REGRESSION\n",1)[1].split("\n```",1)[0]; exec(compile(c,"location-nav-regression","exec"))'
```
