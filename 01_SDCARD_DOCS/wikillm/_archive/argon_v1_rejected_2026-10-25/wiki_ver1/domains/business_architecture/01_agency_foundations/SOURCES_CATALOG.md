# SOURCES_CATALOG — قالب كتالوج مصادر القسم (Sources Catalog Template)

> **الغرض:** السجل الكامل لكل مصدر استُخدم في هذا القسم، بمعرفات SRC_ تشير لملفات موجودة فعلاً على القرص (درس NEXUS_OS: 25 معرفاً وهمياً وصفر موجود = فشل موثق).
> **صيغة السجل:** | SRC_<رقم> | المسار الكامل | الأسطر | نوعه (تفريغ/مقال/سكريبت) | ماذا استُخرج منه |
> **سياسة:** المصدر الأصلي لا يُنقل ولا يُعدل — يبقى في /sdcard/Nexus_Brain/Nexus_Brain/brain/ (مستودع محمي، انظر raw/SOURCE_MANIFEST.tsv). هنا توثيق إحالة فقط.

| SRC_ | المسار الكامل | الأسطر | النوع | ماذا استُخرج منه |
|---|---|---|---|---|
| (مثال شكل فقط) SRC_01 | /sdcard/Nexus_Brain/Nexus_Brain/brain/aaronxshepherd__Beginner's Guide to Cold Email in 2026 (FULL SETUP)__L-E2HEtXTjc.txt | 1 | تفريغ فيديو | خطوات إعداد حملة cold email من الصفر |

## بوابة القبول
```bash
# كل معرف SRC_ يشير لملف موجود:
# for p in $(awk -F'|' 'NR>5 {print $3}' SOURCES_CATALOG.md | grep -o '/sdcard/[^ ]*' | sort -u); do test -f "$p" || echo "MISSING: $p"; done
```
