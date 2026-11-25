# pricing_offers — فهرس المجال، عقد 2026-10-10

| الحقل | القيمة |
|---|---|
| `domain_id` | `pricing_offers` |
| الحالة | `pending` للعمل المعرفي فقط؛ ليست quarantine |
| ترتيب المعرفة | 3 من 4؛ لا يتطلب بيعًا فعليًا أو عرضًا مثبتًا |
| شرط فتح المعرفة | `outreach = domain_done` ببوابات موثقة |
| التوجيه | global_intake_routing مسموح الآن، حتى قبل دور المعرفة |
| الإغلاق | null/not_closed؛ لا raw مقروء دلاليًا أو منسوخ في هذه المراجعة |

## المراجع النشطة (canonical)

- `/sdcard/Nexus_Brain/nexus_vault/BRAIN_INDEX.md`
- `/sdcard/Nexus_Brain/nexus_vault/03_pricing_offers/_index.md`
- `/sdcard/Nexus_Brain/nexus_vault/03_pricing_offers/Master_Pricing_And_Offer_Design.md`

هذه مراجع بنية فقط؛ مضمون الخام ومواضعه تحكم التصنيف، لا قبول المعرفة القديمة.

## subdomains provisional

- [offer_design_and_transformation](offer_design_and_transformation/INDEX.md)
- [value_ladder_and_packaging](value_ladder_and_packaging/INDEX.md)
- [pricing_architecture_and_tiers](pricing_architecture_and_tiers/INDEX.md)
- [value_stack_and_anchoring](value_stack_and_anchoring/INDEX.md)
- [guarantees_risk_reversal_and_price_objections](guarantees_risk_reversal_and_price_objections/INDEX.md)

الطبقات الأخرى مفهرسة فقط، ولا تُنشئ هذه الشجرة Offer أو Price أو Master.

## خريطة الطبقات — مراجع الأعمال المقبولة لاحقًا

- [source_refs/](source_refs/INDEX.md): روابط legacy للمجلدات المباشرة، لا نسخ مصادر.
- [terms/](terms/INDEX.md): مراجع المصطلحات بعد بوابة T.
- [claims/](claims/INDEX.md): مراجع الادعاءات بعد بوابة C.
- [concepts/](concepts/INDEX.md): مراجع المفاهيم بعد بوابة K.
- [masters/](masters/INDEX.md): مراجع الماسترز بعد بوابة M.
- [reports/](reports/INDEX.md): قرارات QA والمصير وسجل الإغلاق.

كل subdomain مباشر يستقبل نسخة مستقلة byte-exact وroute metadata، لا إزالة
الأصل ولا symlink/hardlink. route_done لا يفتح المعرفة. source_done بلا Master؛
كل Master ينتظر domain_terms_complete لكل مصادر ومجلدات snapshot شامل حديث
ومراجعة C/K. وصول جديد ذو صلة يجعل التغطية stale ويحتاج delta review.
[عقد الحالة](../../config/processing_order.json) — [الفهرس العام](../INDEX.md).
