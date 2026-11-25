---
type: index
version: W4.0
domain: pricing_offers
subdomain: 02_pricing_psychology
status: pending
updated: 2026-10-28
---

# INDEX — pricing_offers / 02_pricing_psychology (سيكولوجية التسعير)

قرار السعر كقرار إدراكي: المراسي، الحزم، الأرقام
## retrieval_questions

- ما القوالب الجاهزة لاستقبال تشريح مصادر نطاق «pricing_offers — 02_pricing_psychology»؟ (هذا الفهرس)
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
| pricing_offers_02_pricing_psychology_playbook_template | playbook_template | `domains/pricing_offers/02_pricing_psychology/PLAYBOOK_TEMPLATE.md` | قالب تشريح الماستر (18 قسماً) | استقبال محتوى التشريح وفق SYS_07 | pricing_offers | 02_pricing_psychology | global | pending | uncovered | — | 2026-10-28 |
| pricing_offers_02_pricing_psychology_terms_template | terms_template | `domains/pricing_offers/02_pricing_psychology/TERMS_TEMPLATE.md` | قالب تعميق المصطلحات (الخطوات السبع) | استقبال تعميق المصطلح وفق SYS_06 | pricing_offers | 02_pricing_psychology | global | pending | uncovered | — | 2026-10-28 |
| pricing_offers_02_pricing_psychology_contingency_matrix_template | contingency_matrix_template | `domains/pricing_offers/02_pricing_psychology/CONTINGENCY_MATRIX_TEMPLATE.md` | قالب سجل الرأي ومصفوفة القرار | استقبال تعددية الآراء وفق SYS_08 | pricing_offers | 02_pricing_psychology | global | pending | uncovered | — | 2026-10-28 |
