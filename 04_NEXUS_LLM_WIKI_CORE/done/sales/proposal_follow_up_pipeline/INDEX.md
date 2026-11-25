# sales/proposal_follow_up_pipeline — 2026-10-17

التصنيف `provisional`: العرض المكتوب والمتابعة ومراحل الـpipeline؛ الخام يحسم
التداخل مع `outreach`. هذا المجلد هو الموضع المباشر للنسخة المستقلة وroute
metadata وفق [عقد النسخ](../../../config/domain_catalog.json)، بلا symlink أو
hardlink وبلا تعديل أو إزالة للأصل.

## المصدر الموجّه

| source_id | النسخة | REF | ROUTE | الحالة |
|---|---|---|---|---|
| `SRC_NEW_34aaffac87a9dd7f_0535de17` | [`SRC_NEW_34aaffac87a9dd7f_0535de17.txt`](SRC_NEW_34aaffac87a9dd7f_0535de17.txt) | [`REF_SRC_NEW_34aaffac87a9dd7f_0535de17.json`](REF_SRC_NEW_34aaffac87a9dd7f_0535de17.json) | [`ROUTE_SRC_NEW_34aaffac87a9dd7f_0535de17.md`](ROUTE_SRC_NEW_34aaffac87a9dd7f_0535de17.md) | `route_done`; extraction `not_started` |

النسخة `70,159` bytes وتطابق SHA-256 الخام
`34aaffac87a9dd7fffeb9807ebd32242357364578a64d7a3565f13202d97b83d`؛ فحوص
regular/symlink/hardlink محفوظة في REF. المصدر الأصلي يبقى في `raw/new/`.

`route_done` لا يعني `source_done` ولا `domain_done`. لم تُنشأ Terms أو Claims أو
Concepts أو Masters. أي Master ينتظر T على كل المجال وC/K اللازمة، وdelta جديدة
تجعل التغطية stale.

[فهرس sales](../INDEX.md) — [الحالات](../../../config/processing_order.json).
