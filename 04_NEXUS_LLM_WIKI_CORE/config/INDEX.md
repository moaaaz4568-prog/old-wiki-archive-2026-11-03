# فهرس config — عقد 2026-10-10

| الملف | الوظيفة والحالة |
|---|---|
| [domain_catalog.json](domain_catalog.json) | حدود provisional، دليل البنية، سياسة التصنيف والنسخ وهوية المصدر؛ لا تصنيف raw منجز |
| [processing_order.json](processing_order.json) | مصدر حالة العمل المعرفي وقفل المجال الواحد، حالات الاكتمال والبوابات والمراجعات؛ لقطة أولية `null/not_closed` |

الحسم: [مرجع المواءمة](../reports/sales-proof/MULTIDOMAIN_ALIGNMENT_2026-10-10.md)
و[ملحق المستخدم](../reports/sales-proof/USER_MESSAGES_SESSION_EF22.md)،
`current_conversation: expansion_request_after_EF22`. الطلب الحالي يخصص
quarantine لـmissing/corrupt/unreadable؛ الغموض uncertain/cross_domain_review.

## خريطة التشغيل

[new/INDEX](../new/INDEX.md) → قراءة intake عامة وتصنيف ونسخة مستقلة متطابقة →
[done/INDEX](../done/INDEX.md) → `done/<domain>/<subdomain>/`.
route_done لا يعني source_done أو فتح استخراج domain مؤجل.

## الطبقات الأصلية — ليست نسخًا تحت done

- [sources/](../sources/): سجل الهوية الأصلي؛ route metadata تربط الأصل والنسخة ولا تنشئ هوية ثانية.
- [claims/](../claims/): الادعاءات؛ candidate Claims تُجمع مع terms أثناء استخراج المجال النشط.
- [concepts/](../concepts/): مفاهيم مبنية على Claims مراجعة وقابلة للتتبع.
- [masters/](../masters/): كل Master، صغيرًا أو كبيرًا، ينتظر domain_terms_complete على كل مصادر ومجلدات snapshot الحالي وC/K اللازمة.
- [reports/](../reports/): التقارير الأصلية؛ فهارس done/reports تشير إليها ولا تكررها.
- `terms/` في الجذر **غير موجود عند فحص هذه المراجعة**. فهارس done/terms تحفظ الدور ولا تنشئ بديلًا؛ يلزم تعيين مسار الطبقة الأصلية بواسطة القائد قبل إغلاق T. مرجع البوابات أعلاه هو الرابط الفعلي المتاح، وليس رابطًا مختلقًا لملف Terms.

الـVault القديم دليل شكل وتنظيم فقط؛ الخام هو سلطة التصنيف، وقبول المعرفة القديمة
ليس شرطًا للتصنيف الجديد. الترتيب قرار موجة معرفية لا وصفة بزنس.
هذه إعدادات ووثائق، وليست ادعاء أن سكربتات التشغيل القائمة تنفذ العقد بالفعل.
