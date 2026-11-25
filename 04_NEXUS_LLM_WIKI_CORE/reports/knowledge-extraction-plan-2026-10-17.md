# سجل بدء استخراج المعرفة — 2026-10-17

## النطاق

بدأت مرحلة استخراج المعرفة من المصادر داخل `/sdcard/NEXUS_LLM_WIKI/` وفق قفل المجال النشط في `config/processing_order.json`: المجال النشط هو `sales`. ستظل نتائج الدفعات مرشحة إلى أن تمر بالمراجعة والبوابات، ولن يُعلن اكتمال المجال من عينة.

## أدلة Nexus Brain المستحضرة

- قُرئ `/sdcard/Nexus_Brain/CLAUDE.md`.
- قُرئ `/sdcard/Nexus_Brain/nexus_vault/AGENTS.md`.
- شُغّل `planner.py` بصيغة compact لطلب استخراج المعرفة وبناء الويكي.
- أعاد planner مرشحين إرشاديين، منهم: `Master_Business_Models`, `Master_Funnel_Systems`, `Master_Content_Strategy`, و`Master_Foundation_Business_Strategy`. هذه نتائج استكشاف وليست خطة ملزمة ولا مصدرًا بديلًا عن corpus الخام.

## سياسة التنفيذ

- استخراج Terms وcandidate Claims من مصادر `sales` الموجهة فقط في هذه المرحلة.
- كل Claim يحتفظ بالمصدر والموضع والاقتباس وحدود ما لا يثبته.
- لا تحويل المثال أو النتيجة المبلّغ عنها إلى قاعدة عامة.
- لا إنشاء Master جديد قبل إغلاق snapshot المجال واجتياز بوابة `domain_terms_complete` ومراجعة Claims/Concepts.
- لا تعديل `raw/` ولا حذف أو نقل أي مصدر.

## الحالة عند البدء

- Corpus المسجل: 2,541 سجل هوية.
- routing batches موثقة: 6 مصادر مقروءة توجيهيًا.
- دفعة مبيعات سابقة: 3 مصادر مقروءة مع Terms/Claims مرشحة، لكنها ليست إغلاقًا للمجال.
- المخرج الحالي المطلوب من Agents: نسخ route مستقلة ثم دفعات استخراج مرشحة قابلة للمراجعة.
