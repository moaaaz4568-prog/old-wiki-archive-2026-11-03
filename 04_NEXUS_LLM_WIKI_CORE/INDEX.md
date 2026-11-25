# فهرس مدخل Nexus LLM Wiki

هذا فهرس ملاحي فقط: يحدد أين يوجد العقد والسجل والطبقات، ولا يضيف معرفة ولا يملك
حالة `active_domain` أو `domain_done` مستقلة.

## مراجع الحسم

1. [مرجع المواءمة 2026-10-10](reports/sales-proof/MULTIDOMAIN_ALIGNMENT_2026-10-10.md)
2. [الميثاق التشغيلي متعدد المجالات](MULTI_DOMAIN_WIKI_OPERATING_CHARTER_2026-10-09.md)
3. [ملحق رسائل المستخدم الأحدث](reports/sales-proof/USER_MESSAGES_SESSION_EF22.md)
4. [ميثاق الهدف والتنفيذ 2026-10-08](PROJECT_INTENT_AND_EXECUTION_CHARTER_2026-10-08.md)

عند التعارض، يُقرأ المرجع الأحدث ثم تُراجع الأنظمة العامة المشار إليها بدل نسخ حكم
قديم في هذا الفهرس.

## نطاق الموجة الأولى

| المجال | الدور في الموجة | حالة المعرفة |
|---|---|---|
| `sales` | المجال الأول في ترتيب المعرفة | تُقرأ من `config/processing_order.json` |
| `outreach` | المجال التالي بعد إغلاق السابق | تُقرأ من config |
| `pricing_offers` | المجال التالي بعد إغلاق السابق | تُقرأ من config |
| `content_strategy` | المجال الأخير في الموجة | تُقرأ من config |

التصنيف والنسخ جزء من **global intake** ويمكن أن يشملا المجالات الأربعة، بينما
صناعة Terms/Claims/Concepts/Masters محصورة في مجال معرفي نشط واحد. لا ينسخ الفهرس
حالة config ولا يعلن أن مجالًا مكتملًا.

## خريطة الطبقات

| الطبقة | المسار | الوظيفة | المرجع التالي |
|---|---|---|---|
| Inbox | `new/` | استقبال أصل جديد قبل التوجيه | [نظام 14](systems/14_SOURCE_ROUTING_AND_DONE_TREE.md) |
| Raw | `raw/` | دليل immutable للقراءة والبصمة | [AGENTS](AGENTS.md) |
| Source | `sources/` | هوية المصدر والبصمة وحالاته المحدودة | [SCHEMA](SCHEMA.md) |
| Routed copy | `done/<domain>/<subdomain>/` | نسخة مستقلة مباشرة وroute metadata | [نظام 14](systems/14_SOURCE_ROUTING_AND_DONE_TREE.md) |
| Collection | `collections/<domain>/` | snapshot وmanifest وقراءة التغطية | [نظام 15](systems/15_DOMAIN_COMPLETION_GATES.md) |
| Terms/Claims/Concepts | `claims/`, `concepts/` وسجلات المصطلحات | استخراج ومراجعة وتوليف قابل للتتبع | [نظام 13](systems/13_MULTI_DOMAIN_ARCHITECTURE.md) |
| Masters | `masters/` | كتب قرار بعد T الشاملة، لا عدادات | [نظام 04](systems/04_MASTER_AUTHORING.md) و[فهرس Masters](masters/INDEX.md) |
| Config | `config/` | catalog والحالة الوحيدة للترتيب | [نظام 18](systems/18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md) و[نظام 16](systems/16_SEQUENTIAL_AGENT_ORCHESTRATION.md) |

## العقود العامة

- [13 — المعمارية متعددة المجالات](systems/13_MULTI_DOMAIN_ARCHITECTURE.md)
- [14 — توجيه المصدر وشجرة done](systems/14_SOURCE_ROUTING_AND_DONE_TREE.md)
- [15 — بوابات اكتمال المجال](systems/15_DOMAIN_COMPLETION_GATES.md)
- [16 — التشغيل التسلسلي والقفل](systems/16_SEQUENTIAL_AGENT_ORCHESTRATION.md)
- [17 — عقد فهارس المجلدات](systems/17_FOLDER_INDEX_CONTRACT.md)
- [18 — كتالوج المجالات وترتيبها](systems/18_DOMAIN_CATALOG_AND_PROCESSING_ORDER.md)
- [19 — الوصول الجديد وإعادة المعالجة](systems/19_NEW_SOURCE_REPROCESSING.md)

هذه العقود هي latest contract للمسارات العامة؛ الأنظمة 00/01/04/10/11/12 تشرح
الأساس أو التخصيص، وتحيل إلى العقود بدل تكرارها.

## الحالة الموثقة

السجل الأولي في `config/processing_order.json` يميز بين `not_closed` و
`not_evaluated`، ولا يثبت إغلاقًا. ويعرض `masters/INDEX.md` المسودة/المسودات
الموروثة بحالة `draft`/`partial`؛ لا يرفعها ذلك إلى `reviewed` أو `canonical`.
لا تُكتب الأرقام هنا يدويًا؛ تُقاس من القرص عند تشغيل الفحص وتُربط بلقطة وتقرير.

## الفحص

```bash
python3 tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json
```

نتيجة هذا الفحص لا تغطي وحدها semantic reading أو raw quote offsets أو T/C/K/M/QA؛
مسار التحقق والحدود موثق في
[مراجعة تكامل المداخل](reports/sales-proof/MULTIDOMAIN_INTEGRATION_REVIEW_2026-10-10.md).

موقع كل مخرجات المشروع موثق في
[سياسة موقع المخرجات](PROJECT_OUTPUT_LOCATION_2026-10-10.md)؛ لا يُستخدم
`/root/r/` لمسار تشغيل أو تقرير جديد.

## خريطة الملاحة الموسعة

### نقاط البداية والحالة المرجعية

- [ابدأ من هنا](START_HERE.md): ترتيب القراءة الأولي وحدود التشغيل.
- [الحالة من الصفر](STATUS_FROM_ZERO.md): شرح ما بُني وما لم يُبنَ بعد.
- [بروتوكولات تشغيل النموذج](model_protocols/README.md): السلوك الخارجي والأدلة
  القابلة لإعادة الفحص.
- [فهرس corpus](collections/corpus/INDEX.md): مقام التسجيل وحدوده.
- [manifest corpus](collections/corpus/manifest.jsonl): سجل الهوية والبصمة للمصادر.

### أنظمة التشغيل والتوثيق والتحديث

تُقرأ هذه المجموعة بالترتيب 20 ثم 21 ثم 22 ثم 23 ثم 24 ثم 25؛ وجود الروابط لا يثبت
تشغيل أي نظام أو اكتمال أي مجال:

1. [20 — نظام تشغيل الويكي](systems/20_WIKI_OPERATING_SYSTEM.md)
2. [21 — خط أنابيب المصدر إلى المعرفة](systems/21_SOURCE_TO_KNOWLEDGE_PIPELINE.md)
3. [22 — نظام الكتابة والدليل](systems/22_WRITING_AND_EVIDENCE_SYSTEM.md)
4. [23 — الاسترجاع وضمان الجودة والحالة الصادقة](systems/23_RETRIEVAL_QA_AND_HONEST_STATUS.md)
5. [24 — تسليم الوكيل والاسترداد](systems/24_AGENT_HANDOFF_AND_RECOVERY.md)
6. [25 — ضبط التغيير والتحديث](systems/25_CHANGE_CONTROL_AND_UPDATE_PROTOCOL.md)

### دفعات استخراج sales المرشحة

- [HIGH_TICKET](collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_HIGH_TICKET.json)
- [PROPOSAL_FOLLOW_UP](collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_PROPOSAL_FOLLOW_UP.json)
- [DISCOVERY](collections/sales/extraction_batches/SALES_EXTRACTION_2026-10-17_DISCOVERY.json)

هذه الدفعات هي مخرجات `candidate` لا أكثر؛ وجود batch أو Term/Claim مرشح فيها لا يعني
`accepted knowledge`، ولا يثبت `source_done` أو `domain_done` أو اكتمال الويكي.

### مسارات sales المباشرة: route وcopy

| المصدر/المسار | الفهرس المحلي | route | النسخة المباشرة |
|---|---|---|---|
| `sales/high_ticket_closing` | [INDEX](done/sales/high_ticket_closing/INDEX.md) | [ROUTE](done/sales/high_ticket_closing/ROUTE_SRC_NEW_b0140a4d41654bab_b1f4775a.md) | [copy](done/sales/high_ticket_closing/SRC_NEW_b0140a4d41654bab_b1f4775a.txt) |
| `sales/proposal_follow_up_pipeline` | [INDEX](done/sales/proposal_follow_up_pipeline/INDEX.md) | [ROUTE](done/sales/proposal_follow_up_pipeline/ROUTE_SRC_NEW_34aaffac87a9dd7f_0535de17.md) | [copy](done/sales/proposal_follow_up_pipeline/SRC_NEW_34aaffac87a9dd7f_0535de17.txt) |
| `sales/discovery_and_sales_conversations` | [INDEX](done/sales/discovery_and_sales_conversations/INDEX.md) | [ROUTE](done/sales/discovery_and_sales_conversations/ROUTE_SRC_NEW_2a98697c6e73ffa1_82a4e90e.md) | [copy](done/sales/discovery_and_sales_conversations/SRC_NEW_2a98697c6e73ffa1_82a4e90e.txt) |

الروابط أعلاه تصل إلى نسخ `done/sales/` المباشرة وسجلات route المقابلة؛ `route_done`
ليس `source_done`، ولا يحول النسخة أو السجل إلى معرفة مقبولة.

### تنبيه على وظيفة هذا الفهرس

هذا `INDEX.md` ملاحي فقط: لا يملك حالة تشغيلية أو `active_domain` أو `domain_done`،
ولا يثبت coverage أو قبول المعرفة أو اكتمال الويكي. المرجع الحاكم للحالة هو الملف
المملوك لذلك الغرض، والنتيجة المرشحة تبقى مرشحة حتى تجتاز المراجعة والبوابات المناسبة.
