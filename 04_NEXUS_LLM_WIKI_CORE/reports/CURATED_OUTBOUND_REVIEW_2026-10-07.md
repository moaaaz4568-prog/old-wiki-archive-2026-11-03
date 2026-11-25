# مراجعة المعرفة المنسقة: outbound / deliverability

## النطاق
راجعت هذه الدفعة مواد Instantly وSmartlead وExpandi ومقاطع Aaron Shepherd وMatthew Lucero في نطاق deliverability، targeting، follow-up، reply handling، والعمليات. لم أعدّل `raw/`، ولم أنشئ Master، ولم أضف API أو raw edits.

## النتائج والأعداد
- أُنشئت **8 Concepts** مستقلة بالبادئة `CPT_CURATED_OUTBOUND_`.
- أُنشئت **23 Claims** بالبادئة `CLM_CURATED_OUTBOUND_`؛ 7 مفاهيم لها 3 Claims، ومفهوم القنوات المتعددة له Claimان.
- كل Claims الجديدة حالتها `reviewed` و`confidence: source_reported`، وكل واحد يذكر `source_id` موجودًا في manifest، وموضع Unicode صفري البداية، و`excerpt_sha256`.
- المفاهيم تحتوي الشروط، حالات الفشل، التوترات، التطبيقات المشروطة، وجداول أدلة بروابط نسبية إلى claim/source.
- فُصلت صراحةً open rate وreply rate وpositive reply وmeeting booked/show وclose؛ لم تُعامل الردود كإيراد.
- سُجل اختلاف التوصيات بدل توحيدها: تدفئة Matthew «أسبوعان على الأقل»، إعداد Smartlead «صفر إلى 30 رسالة تدفئة يوميًا»، وتحليل Instantly «نحو خطوتين أو ثلاث» للتسلسل، مع شرط Matthew المختلف حسب حجم السوق.

## تحقق الأدلة
تحققت آليًا من أن كل quote يطابق slice من الملف الخام عند `evidence_start:evidence_end` وأن hash يطابق `excerpt_sha256`، وأن hash الملف الكامل يطابق `content_hash` الوارد في manifest للمصادر المستخدمة. شملت الاختبارات 23/23 Claim.

## القيود
- هذه المصادر transcripts/مواد تعليمية وتجارب متحدثين؛ `source_reported` لا يعني تحققًا تجريبيًا مستقلًا.
- بعض النصوص الإنجليزية بها أخطاء تفريغ (مثل DKM/demark/AMX)، لذلك لم أصحح quote ولم أحولها إلى أسماء سجلات مؤكدة.
- أرقام 10 نطاقات، 30 رسالة، 15 دقيقة، 20 حملة، وأمثلة الردود لم تُرفع إلى benchmarks؛ بقيت في نطاق المصدر.
- لا توجد في هذه الدفعة بيانات كافية لإثبات conversion rates أو causal lift أو أفضلية منصة على أخرى.

## ملفات الدفعة
Concepts: `concepts/CPT_CURATED_OUTBOUND_*.md`  
Claims: `claims/CLM_CURATED_OUTBOUND_*.md`
