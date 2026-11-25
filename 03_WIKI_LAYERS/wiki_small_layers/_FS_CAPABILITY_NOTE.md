# قيد نظام الملفات — لماذا لا symlinks هنا

> **هذا الملف ناتج عن فحص قدرة، لا وثيقة ويكي.** وُجد بالصدفة أثناء محاولة إنشاء
> الـsymlinks في `/sdcard/wiki/`، فبُقي توثيقاً بدل حذفه (قاعدة «صفر حذف»).

## الفحص

```bash
stat -f /sdcard
#   Type: fuseblk          ← تخزين محاكى (emulated / Android) عبر FUSE

ln -s /tmp /sdcard/wiki/_symtest
#   ln: failed to create symbolic link ...: Permission denied     (exit 1)

touch /sdcard/wiki/_t1 && ln /sdcard/wiki/_t1 /sdcard/wiki/_t2
#   ln: failed to create hard link ...: Operation not permitted   (exit 1)
```

`/sdcard` و `/mnt/sdcard` **نفس نظام الملفات** (`stat` ⇒ `194:4836` لنفس الـinode) —
أي: Directory واحد بوجهين. لا حلّ بديل داخل المسار.

## النتيجة المؤلمة

| المطلوب | ممكن في `/sdcard`؟ |
|---|---|
| `symlink` (§2 من التوجيه) | ❌ لا — الـkernel يرفض |
| `hardlink` | ❌ لا |
| ملف نصّي عادي | ✅ نعم |
| `mkdir` | ✅ نعم |
| `cp -a` (نسخ v3) | ✅ نعم |

## الحل المطبَّق (بلا نسخ لـv1/v2)

الـsymlinks بُنيت في `/root/r/WIKI_HUB/` — نفس أسماء الأقسام تماماً، و `/root/r`
منطقة كتابة مسموحة. المسار المعلن للقراءة:

```bash
/sdcard/wiki/01_WIKI_V1_ARABIC_MASTERS/README.md      ← التوثيق (يعيش في /sdcard)
/root/r/WIKI_HUB/01_WIKI_V1_ARABIC_MASTERS/nexus_vault → /root/r/…/01_ACTIVE_WIKI/nexus_vault
```

**22 symlink** إجمالاً (11 للـv1 + 11 للـv2). `v3` نسخ حقيقي على `/sdcard` لأنه جديد
وصغير (224 ملفاً · 24,016,136 بايت) والنسخة هي كما طلب التوجيه.

## لو أُلغي القيد مستقبلاً

```bash
# بعد الانتقال إلى نظام ملفات يدعم الروابط (ext4/btrfs) — لا حذف، فقط إضافة:
cd /sdcard/wiki/01_WIKI_V1_ARABIC_MASTERS
ln -s /root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/nexus_vault nexus_vault
# … إلخ — نفس الأسماء، نفس الأهداف
```