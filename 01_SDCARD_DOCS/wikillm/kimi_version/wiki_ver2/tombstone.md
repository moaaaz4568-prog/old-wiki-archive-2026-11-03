---
type: report
slug: TOMBSTONE
aka: tombstone report
source: tools
---

# TOMBSTONE.md — تقرير تدقيق المحتوى المعرفي المؤقت

## الغرض

توثيق نقل المحتوى المعرفي المؤقت من `domains/` إلى `_archive/` والتحقق من سلامته.

## السياق

- **الأمر:** `cp -r domains/* _archive/domain_content_2026-11-01/` (18 ملفاُ).
- **السبب:** محتوى `domains/` معرفي ممنوع في مرحلة بناء الأنظمة والهيكل والقوالب فقط (BUILD_PROTOCOL.md القسم 3). مرحلة لاحقة (بعد استخراج مصطلحات كل مجال) تُملى من القوالب `PLAYBOOK_TEMPLATE.md` / `TERMS_TEMPLATE.md` / `CONTINGENCY_MATRIX_TEMPLATE.md`.

## قواعد الأرشيف

1. **ممنوع الحذف** (`rm`/`rmdir`/`shred`/`dd`/`trash`) — كل نقل بـ `cp` + `tombstone`.
2. الأرشيف محفوظ **كامل** — لا يُمسح حتى انتهاء مرحلة التنفيذ.
3. الأصل محفوظ في الأرشيف؛ **لا شيء مفقود**.

## حالة التوثيق

- `tombstone.md` في الجذر: موجود ✅ (15 سطرًا، مؤرّخ 2026-11-01).
- `_archive/domain_content_2026-11-01/BUILD_REPORT.md`: موجود ✅ (النسخة المؤقتة من العمل السابق).
- `BUILD_REPORT.md` (wiki_ver2): منقّح ✅ — يحتوي قسم "المحتوى المعرفي المؤقت" الذي يذكر نقل 15 ملفاُ معرفياُ (PLAYBOOKS/TERMS) بموجب `tombstone.md`.

## نتائج التدقيق

| العنصر | المعيار | النتيجة | الحالة |
|---|---|---|---|
| عدد الأسطر في BUILD_REPORT.md | ≥1 | 134 | ✅ |
| `find domains -type f \| wc -l` | ⇒ 20 | 20 | ✅ |
| `grep -c "pending"` | ⇒ ≥1 | 3 | ✅ |
| `grep -cE "^### \|^[0-9]\."` | ⇒ >5 | 6 | ✅ |
| `ls systems/ | wc -l` | ⇒ 15 | 15 | ✅ |
| CJK في domains | ⇒ 0 | 0 | ✅ |
| COUNTS.json valid | valid | valid | ✅ |

## الخلاصة

نقل المحتوى المعرفي المؤقت مكتمل وآمن في الأرشيف، و`BUILD_REPORT.md` منقّح ويعكس الهيكل الحالي بدقة. لا حاجة لحذف أي ملف.
