# sales/high_ticket_closing — فهرس route المحلي

هذا الفهرس يعدد النسخ المباشرة المتحققة ومسارات REF/ROUTE في هذا المجلد فقط.
لا يعلن `source_done` أو `domain_terms_complete` أو جاهزية Master أو `domain_done`.
التصنيف `provisional`؛ الدليل الخام ومواضع المتن هما سلطة التوجيه، لا اسم المجلد.

| source_id | النسخة regular | REF | ROUTE | route_status | source_extraction_status |
|---|---|---|---|---|---|
| `SRC_NEW_b0140a4d41654bab_b1f4775a` | [SRC_NEW_b0140a4d41654bab_b1f4775a.txt](SRC_NEW_b0140a4d41654bab_b1f4775a.txt) | [REF](REF_SRC_NEW_b0140a4d41654bab_b1f4775a.json) | [ROUTE](ROUTE_SRC_NEW_b0140a4d41654bab_b1f4775a.md) | `route_done` | `not_started` |

## النطاق والحالة

- `domain`: `sales`; `subdomain`: `high_ticket_closing`.
- النسخ الأساسية: **1 source identity / 1 primary copy**؛ لا نسخة ثانية للمراجع الثانوية.
- المصدر الخام: unchanged؛ النسخة مستقلة byte-exact، لا symlink ولا hardlink.
- التغطية: route batch لمصدر واحد؛ ليست snapshot مكتملة للمجال.
- المعرفة: لم تُنشأ Terms أو Claims أو Concepts أو Masters في هذه المهمة.

## المراجع

- [تقرير route + copy](../../../reports/route-copy-high-ticket-2026-10-17.md)
- [Checkpoint](../../../checkpoints/ROUTE_COPY_HIGH_TICKET_2026-10-17.md)
- [سجل التشغيل](../../../staging/routing/ROUTE_RUN_20261017_HIGH_TICKET.json)
- [فهرس sales](../INDEX.md)
- [العقد والبوابات](../../../config/domain_catalog.json) و[processing order](../../../config/processing_order.json)
