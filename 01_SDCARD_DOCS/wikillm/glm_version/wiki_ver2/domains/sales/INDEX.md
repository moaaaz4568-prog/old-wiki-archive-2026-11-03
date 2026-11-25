---
type: index
version: W4.0
domain: sales
status: pending
updated: 2026-10-28
---

# INDEX — المبيعات (حركة الإيراد من العميل المحتمل إلى التوقيع)

## retrieval_questions

-
 
م
ا
 
ا
ل
أ
ق
س
ا
م
 
ا
ل
ف
ر
ع
ي
ة
 
ل
ن
ط
ا
ق
 
«
ا
ل
م
ب
ي
ع
ا
ت
»
؟
 
(
ا
ل
ج
د
و
ل
 
أ
د
ن
ا
ه
)

## limitations

- هذا الفهرس لا يحوي معرفة — الأقسام الفرعية كلها قوالب فارغة.
- لا يجيب عن أسئلة المضمون — تُبحث داخل أقسامه بعد ملئها.
- لا يملك `active_domain` (R06 في SYS_10).

## الحالة الصريحة

- `pending` — كل الأقسام الفرعية قوالب فارغة.

---

## المداخل (12 حقلاً وفق R02: id, kind, path, title, function, domain, subdomain, scope, status, coverage_status, snapshot_id, updated)

| id | kind | path | title | function | domain | subdomain | scope | status | coverage_status | snapshot_id | updated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sales_01_discovery_qualification | subdomain_index | `domains/sales/01_discovery_qualification/INDEX.md` | فهرس الاكتشاف والتأهيل | إيجاد العملاء الذين يحتاجون الخدمة فعلاً وتأهيلهم قبل العرض | sales | 01_discovery_qualification | global | pending | uncovered | — | 2026-10-28 |
| sales_02_closing | subdomain_index | `domains/sales/02_closing/INDEX.md` | فهرس الإغلاق | حركات إنهاء الصفقة: الالتزام، التوقيع، الشروط | sales | 02_closing | global | pending | uncovered | — | 2026-10-28 |
| sales_03_objections | subdomain_index | `domains/sales/03_objections/INDEX.md` | فهرس الاعتراضات | معالجة الاعتراضات بوصفها بيانات لا معارك | sales | 03_objections | global | pending | uncovered | — | 2026-10-28 |
