---
type: index
version: W4.0
domain: business_architecture
subdomain: 01_business_models
status: pending
updated: 2026-10-28
---

# INDEX — business_architecture / 01_business_models (نماذج البيزنس)

أنواع النماذج التجارية ومنطق الإيراد في كل منها
## retrieval_questions

- ما القوالب الجاهزة لاستقبال تشريح مصادر نطاق «business_architecture — 01_business_models»؟ (هذا الفهرس)
- ما حالة كل قالب؟ (القسم الثالث أدناه: كلها `pending`)
- أين تُوثَّق الآراء المتعارضة لهذا النطاق؟ (CONTINGENCY_MATRIX_TEMPLATE)

## limitations

- هذا الفهرس لا يحوي معرفة — فقط قوالب فارغة (`pending`)؛
  لا تُبنى عليه توصية تنفيذية.
- لا يجيب عن أسئلة المضمون (ما التكتيك الفعّال؟ ما الشروط؟) —
  تُبحث في القوالب بعد ملئها وفق SYS_07.
- لا يملك `active_domain` ولا أي سلطة قرار (R06 في SYS_10)؛
  القرار للأنظمة (SYS_01–SYS_09).

## الحالة الصريحة

- `pending` — القوالب أُنشئت ولم يُشرَّح فيها مصدر بعد.
- المسار العكسي (R03): Master ← Concept ← Claim ← `source_id` —
  يسلك بعد الملء؛ القوالب الفارغة بلا مصدر بعد.

---

## المداخل (12 حقلاً وفق R02: id, kind, path, title, function, domain, subdomain, scope, status, coverage_status, snapshot_id, updated)

| id | kind | path | title | function | domain | subdomain | scope | status | coverage_status | snapshot_id | updated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| business_architecture_01_business_models_playbook_template | playbook_template | `domains/business_architecture/01_business_models/PLAYBOOK_TEMPLATE.md` | قالب تشريح الماستر (18 قسماً) | استقبال محتوى التشريح وفق SYS_07 | business_architecture | 01_business_models | global | pending | uncovered | — | 2026-10-28 |
| business_architecture_01_business_models_terms_template | terms_template | `domains/business_architecture/01_business_models/TERMS_TEMPLATE.md` | قالب تعميق المصطلحات (الخطوات السبع) | استقبال تعميق المصطلح وفق SYS_06 | business_architecture | 01_business_models | global | pending | uncovered | — | 2026-10-28 |
| business_architecture_01_business_models_contingency_matrix_template | contingency_matrix_template | `domains/business_architecture/01_business_models/CONTINGENCY_MATRIX_TEMPLATE.md` | قالب سجل الرأي ومصفوفة القرار | استقبال تعددية الآراء وفق SYS_08 | business_architecture | 01_business_models | global | pending | uncovered | — | 2026-10-28 |
