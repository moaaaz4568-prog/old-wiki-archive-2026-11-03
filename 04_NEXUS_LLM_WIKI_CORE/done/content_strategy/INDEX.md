# content_strategy — فهرس المجال، عقد 2026-10-10

| الحقل | القيمة |
|---|---|
| `domain_id` | `content_strategy` |
| الحالة | `pending` للعمل المعرفي فقط؛ ليست quarantine |
| ترتيب المعرفة | 4 من 4؛ قرار موجة لا وصفة بزنس |
| شرط فتح المعرفة | `pricing_offers = domain_done` ببوابات موثقة |
| التوجيه | global_intake_routing مسموح الآن؛ لا يتطلب اعتماد عرض فعلي |
| الإغلاق | null/not_closed؛ لا raw مقروء دلاليًا أو منسوخ في هذه المراجعة |

## المراجع النشطة (canonical)

- `/sdcard/Nexus_Brain/nexus_vault/BRAIN_INDEX.md`
- `/sdcard/Nexus_Brain/nexus_vault/04_content_strategy/_index.md`
- `/sdcard/Nexus_Brain/nexus_vault/04_content_strategy/Master_Content_Strategy.md`

دليل بنية فقط؛ الخام هو دليل التصنيف ولا علاقة لقبول معرفتهم بالتوجيه الجديد.

## subdomains provisional

- [audience_positioning_and_content_manifesto](audience_positioning_and_content_manifesto/INDEX.md)
- [content_funnel_tofu_mofu_bofu](content_funnel_tofu_mofu_bofu/INDEX.md)
- [customer_voice_and_validated_ideation](customer_voice_and_validated_ideation/INDEX.md)
- [content_formats_and_repurposing](content_formats_and_repurposing/INDEX.md)
- [distribution_calendar_and_measurement](distribution_calendar_and_measurement/INDEX.md)
- [content_monetization_and_offer_alignment](content_monetization_and_offer_alignment/INDEX.md)

الـproduction والـhooks والـstorytelling والـcopywriting والـplatforms مجالات
مجاورة وليست مضافة ضمن هذا الفهرس.

## خريطة الطبقات — مراجع الأعمال المقبولة لاحقًا

- [source_refs/](source_refs/INDEX.md): روابط legacy إلى المسارات المباشرة؛ لا نسخ مصادر.
- [terms/](terms/INDEX.md): مراجع المصطلحات بعد بوابة T.
- [claims/](claims/INDEX.md): مراجع الادعاءات بعد بوابة C.
- [concepts/](concepts/INDEX.md): مراجع المفاهيم بعد بوابة K.
- [masters/](masters/INDEX.md): مراجع الماسترز بعد بوابة M.
- [reports/](reports/INDEX.md): قرارات QA والمصير وسجل الإغلاق.

المسارات المباشرة لنسخة المصدر المستقلة byte-exact وroute metadata ضمن عمل R، لا
symlink/hardlink ولا إزالة raw. source_done لا يحتاج Master، ووجود المصدر هنا
لا يعني اكتماله. أي Master ينتظر domain_terms_complete لكل مصادر ومجلدات
snapshot شامل حديث وC/K المراجعة. أي وصول ذي صلة يجعل التغطية stale مع delta
معلنة وقفل معرفة واحد. [عقد الحالة](../../config/processing_order.json) —
[الفهرس العام](../INDEX.md).
