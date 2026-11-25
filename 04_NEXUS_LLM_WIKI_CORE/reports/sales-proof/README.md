# تقارير الموجة متعددة المجالات

هذا هو المسار canonical لتقارير التشغيل والمراجعة والـAgents:

```text
/sdcard/NEXUS_LLM_WIKI/reports/sales-proof/
```

## سياسة الموقع

- كل تقرير جديد يُكتب هنا مباشرة، وليس في `/root/r/`.
- كل تقرير يذكر الملفات المقروءة، المخرجات، الفحوص، وما لم يُنجز.
- التقارير لا تصبح Claims أو Concepts أو Masters تلقائيًا.
- `MIGRATION_MANIFEST_2026-10-10.tsv` يثبت نقل التقارير المرحلية القديمة إلى هذا المسار.
- أي ظهور لـ`/root/r/reports/sales-proof/` داخل تقرير قديم هو provenance تاريخي؛ لا يُستخدم كمسار تشغيل جديد.

## التقارير الأساسية

| الملف | الوظيفة |
|---|---|
| `USER_MESSAGES_SESSION_EF22.md` | رسائل المستخدم المستخرجة وتحليل الهدف |
| `SOURCE_SESSION_EF22.md` | نسخة sdcard من ملف الجلسة المصدر للتحقق من الاستخراج |
| `MULTIDOMAIN_ALIGNMENT_2026-10-10.md` | تصحيح النطاق والبوابات والمسارات |
| `agent-general-systems-v3.md` | تقرير بناء الأنظمة العامة |
| `agent-domain-catalog-v3.md` | تقرير الكتالوج وشجرة المجالات |
| `agent-multidomain-skills-v3.md` | تقرير مواءمة الـSkills العامة |
| `MULTIDOMAIN_INTEGRATION_REVIEW_2026-10-10.md` | مراجعة التكامل المستقلة |
| `MIGRATION_MANIFEST_2026-10-10.tsv` | بصمات نقل التقارير إلى sdcard |
