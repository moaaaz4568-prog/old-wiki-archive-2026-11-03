# 07 — مراجعة Claims في المبيعات

## الغرض

تحويل مرشحي Claims إلى سجلات أمينة لما يقوله المصدر، لا إلى وصفات مبيعات
مفترضة. يطبق هذا النظام بوابة `evidence quote + locator`، ويفصل النقل عن
التفسير والنتيجة المبلغ عنها والمثال.

## المدخلات

- مصدر مسجل في `sources/` ومساره وبصمته سليمان.
- نص المصدر نفسه من `raw/` أو مرجع قراءة معتمد.
- Claim مرشح يحمل `claim_id`, `source_id`, موضعًا أوليًا، واقتباسًا إن توفر.
- سياسة نوع الدليل: `direct_quote`, `reported_result`, `example`, `inference`,
  `hypothesis`.

## نموذج المراجعة

1. اقرأ سياقًا كافيًا قبل وبعد الموضع، وسجل المتحدث أو الجهة إن ظهر.
2. افصل الجملة القابلة للتحقق عن التفسير الذي يقدمه المراجع.
3. تحقق من أن `evidence_quote` يساوي الشريحة الفعلية بين `evidence_start` و
   `evidence_end`، وأن `excerpt_sha256` يطابق الاقتباس.
4. اكتب `statement` بصياغة لا تتجاوز النص: «المصدر يذكر/يبلغ/يقترح...» عند الحاجة.
5. حدد الجمهور والقناة والمرحلة والزمن والشروط، ثم اكتب `what_it_does_not_prove`.
6. إذا كان الرقم من قصة أو تجربة شخصية، استخدم `reported_result` و`source_reported`؛
   لا تحوله إلى benchmark أو سببية.
7. سجل العلاقة مع Claims أخرى (`supports`, `contradicts`, `example_of`,
   `derived_from`, `related_to`) بدل دمجها في Claim واحد.

## عقد Claim المتوافق مع SCHEMA

```yaml
type: claim
claim_id: CLM_YYYYMMDD_slug_001
statement: صياغة أمينة قابلة للمراجعة
evidence_type: direct_quote|reported_result|example|inference|hypothesis
source_id: SRC_...
locator: chars 120:240|line 120-128|timestamp 00:12:31|section 3
scope: الجمهور والقناة والشرط والزمن
confidence: source_reported|supported|inferred|hypothetical|disputed
status: candidate|reviewed|accepted|rejected
```

ويُطلب عمليًا، وإن لم يكن في الحد الأدنى، `evidence_start`, `evidence_end`,
`evidence_quote`, `excerpt_sha256`, و`what_it_does_not_prove`.

## المخرجات

ينتج النظام ملف Claim مراجعًا أو قرارًا موثقًا بإبقائه `candidate` أو رفضه، مع
سجل `review_id` ونتيجة كل بوابة. لا يُعدّل المصدر الخام، ولا تُنشأ صفحة Concept
من Claim لم يثبت موضعه.

## بوابات القبول

- **C0 المطابقة:** المصدر موجود، و`source_id` معروف، والاقتباس يطابق الشريحة والبصمة.
- **C1 الصدق الدلالي:** statement لا يرفع درجة اليقين ولا يوسع النطاق عن النص.
- **C2 النوع:** المثال والنتيجة المبلغ عنها يظلان `source_reported`؛ inference =
  `inferred`؛ hypothesis = `hypothetical`.
- **C3 الحدود:** لكل Claim مقبول بيان لما لا يثبته، خصوصًا الأرقام والسببية والتعميم.
- **C4 الحالة:** `candidate` للمرشح الآلي، `reviewed` بعد مراجعة الموضع والمعنى،
  و`accepted` فقط بعد سياسة المراجعة المعتمدة؛ الادعاء المتعارض لا يُخفى بل يوضع
  `disputed` أو تسجل علاقته.
- **C5 الإحالة:** يمكن لمراجع مستقل الوصول إلى الدليل دون تخمين موضعه.

## حالات الفشل

| الفشل | القرار |
|---|---|
| الاقتباس لا يطابق المصدر | `rejected` أو إعادة استخراج؛ ممنوع تصحيح الاقتباس بالتخمين |
| موضع عام مثل «في الفيديو» | يبقى `candidate` حتى يضاف timestamp/section قابل للتحقق |
| المصدر يقول «قد» والـstatement يقول «يؤدي إلى» | خفض الصياغة، وتسجيل سبب التعديل |
| رقم بلا مقام أو زمن | `reported_result` مع حدوده، لا benchmark |
| Claim مشتق من مثال واحد | `example` فقط؛ أي تعميم يحتاج Claim مستقلًا ودليلًا مستقلًا |
| مصدران متعارضان | يحتفظ كلاهما، وتضاف `contradicts` مع الشروط والسياق |
| لا يمكن تحديد الصلة بالنطاق | `rejected` مع سبب «خارج النطاق» لا حذف السجل |

## معايير القياس

- **Evidence validity:** Claims ذات شرائح صحيحة / Claims المفحوصة، الهدف 100% للقبول.
- **Locator coverage:** Claims بمحدد قابل للتحقق / كل Claims، منفصل بحسب الحالة.
- **Semantic fidelity:** عينة مراجعة مزدوجة؛ نسبة الاتفاق على النوع والنطاق والصياغة.
- **Generalization leakage:** حالات تحويل مثال/رقم إلى قاعدة ÷ العينة؛ الهدف صفر.
- **Contradiction visibility:** التعارضات المسجلة / التعارضات المكتشفة.
- **زمن المراجعة:** الوسيط من المرشح إلى `reviewed`، دون استخدام السرعة لتجاوز C0–C3.

## مخرجات وسجل القرار

ينتج ملف Claim أو تحديثًا موثقًا له، وسجل مراجعة يتضمن `review_id`, `claim_id`,
المراجع، التاريخ، القرار، الحقول المعدلة، سبب التعديل، والاختبارات المنفذة. لا
يتغير `raw/`. روابط Concepts اللاحقة تشير إلى `claim_refs` لا إلى نص خام منسوخ.
