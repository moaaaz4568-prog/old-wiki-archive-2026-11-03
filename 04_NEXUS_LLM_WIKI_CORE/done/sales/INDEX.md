# sales — فهرس المجال، عقد 2026-10-10

| الحقل | القيمة |
|---|---|
| `domain_id` | `sales` |
| الحالة | `in_progress` |
| اعتماد الإغلاق | غير موجود؛ لا يُعلن `sales` مكتملًا |
| مرجع الحالة | `/sdcard/NEXUS_LLM_WIKI/config/processing_order.json` |
| مرجع التصنيف | `/sdcard/NEXUS_LLM_WIKI/config/domain_catalog.json` |
| ترتيب المعرفة | 1 من 4؛ ليس ترتيب ممارسة البزنس |
| التوجيه | global_intake_routing مسموح لكل المجالات |

## وظيفة المجلد

مواضع النسخ المصنفة المباشرة وفهارس الطبقات الأصلية. لم تُقرأ مصادر raw دلاليًا
أو تُنسخ في هذه المراجعة. كل gate snapshot مبدئي null/not_closed.

## المراجع النشطة (canonical)

- `/sdcard/Nexus_Brain/nexus_vault/BRAIN_INDEX.md`
- `/sdcard/Nexus_Brain/nexus_vault/02_sales_closing/_index.md`
- الـVault دليل بنية فقط؛ قبول معرفته لا يؤثر في التصنيف الجديد، والخام هو
  سلطة القرار. [عقد التصنيف](../../config/domain_catalog.json).

## subdomains أولية

كل المجلدات أدناه مباشرة تحت sales و`provisional`. تستقبل لاحقًا نسخة المصدر
byte-exact مستقلة وroute metadata وفق R، لا symlink/hardlink ولا إزالة الأصل:

- [discovery_and_sales_conversations](discovery_and_sales_conversations/INDEX.md)
- [lead_qualification](lead_qualification/INDEX.md)
- [objection_handling](objection_handling/INDEX.md)
- [high_ticket_closing](high_ticket_closing/INDEX.md)
- [proposal_follow_up_pipeline](proposal_follow_up_pipeline/INDEX.md)
- [negotiation](negotiation/INDEX.md): جديد؛ ذكر المستخدم التفاوض صراحةً، لا استخراج معرفي جديد.

## خريطة الطبقات

| المسار | الوظيفة | الحالة الحالية |
|---|---|---|
| [source_refs/](source_refs/INDEX.md) | فهرسة legacy وروابط للمسارات المباشرة | ليست مكان نسخ المصادر |
| [terms/](terms/INDEX.md) | مراجع مخرجات بوابة T | لا قرار قبول جديد |
| [claims/](claims/INDEX.md) | مراجع مخرجات بوابة C | لا قرار قبول جديد |
| [concepts/](concepts/INDEX.md) | مراجع مخرجات بوابة K | لا قرار قبول جديد |
| [masters/](masters/INDEX.md) | مراجع مخرجات بوابة M | لا قرار قبول جديد |
| [reports/](reports/INDEX.md) | قرارات QA والمصير المقبولة لاحقًا | لا سجل إغلاق |

## قاعدة الإغلاق

route_done غير source_done الذي لا يحتاج Master. تجمع Terms وcandidate Claims
معًا في المجال النشط؛ لا يبدأ أي Master حتى domain_terms_complete لكل المصادر
والمجلدات ضمن snapshot شامل حديث ومراجعة C/K اللازمة. domain_done وQA والفهارس
والاسترجاع وسجل الإغلاق تسبق فتح معرفة outreach، لا تسبق intake الخاص به.
مصدر جديد ذو صلة يجعل التغطية stale ويحتاج delta review، لا إغلاقًا صامتًا.
[الحالات والبوابات](../../config/processing_order.json) — [الفهرس العام](../INDEX.md).
