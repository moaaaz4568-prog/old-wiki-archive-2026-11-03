# 09_LEGACY — أين v1 وأين v2 · وقاعدة «لا تنسخ»

<!-- counts-ref: v1 مقيس مباشرة 2026-10-02 · v2 من V3_SYS/COUNTS.json -->

> **القاعدة الحاكمة:** لا يُنسخ أي ملف من v1 أو v2 إلى V3. القراءة عبر المسار الأصلي فقط.
> السبب: 47,722 ملفاً (‎215MB + 124MB‎) من نسخٍ ثانٍ = تضخيم · انفصال المصدر · تعارض تعديلات.
> كل رقم في V3 يشير إلى **مسار المصدر** لا إلى نسخة محلية.

## 1) خريطة الطبقتين

| الطبقة | الجذر | الدور |
|---|---|---|
| **v1** | `/root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/` | ويكي TheBrain: `brain/` (مصادر خام ‎5,126 ملف) · `Nexus_Brain/` · `nexus_vault/` · `rag/` · `chats/` |
| **v2** | `/root/r/NB2/` | الطبقة المنتهية: `02_CONCEPTS/` (‎29,585‎) · `terms_26k/` (‎27,742 ذرّة‎) · `03_MASTERS/` (‎10‎) · `.nexus_work/` (‎2,412‎) · `TRASH/` (‎4,056‎) |

## 2) الحجم — مقيس لا مقتبس

| الطبقة | المسار | الملفات | البايت | المجلدات | مصدر الرقم |
|---|---|---:|---:|---:|---|
| **v1** | `NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/` | **10,624** | **124,207,526** | 226 | `find` مباشر 2026-10-02 |
| **v2** | `NB2/` | **37,098** | **214,927,890** | 422 | `V3_SYS/COUNTS.json → nb2.total` |
| **المجموع** | — | **47,722** | **339,135,416** | 648 | — |

> ⚠️ `COUNTS.json` يسجّل `v1.exists = false` — عدّاد المشروع لم يكن يعرف مسار v1.
> رقم v1 أعلاه **مقيس يدوياً**، وهو غير مُدخَل في `COUNTS.json`. من يُحدّث `count.py`
> يضيف جذر `…/WIKI/01_ACTIVE_WIKI` في مفتاح `roots` ليصبح الرقم قابلاً لإعادة القياس.

## 3) كيف تقرأ من v1

```bash
# قائمة القنوات (127 قناة) في brain/processed/
ls /root/r/NEXUS_GITHUB_PACKAGE/WIKI/01_ACTIVE_WIKI/brain/processed/
# جذر المفاتيح lore:
python3 /root/r/V3/11_INDEX/tools/route.py --sector 01_outreach
# فهرسbrain بالأرقام (بدون نسخ):
python3 /root/r/V3/11_INDEX/tools/build_source_index.py
```

## 4) كيف تقرأ من v2

```bash
# طبقة الذرّات (‎27,742‎) وطبقة المفاهيم (‎1,836‎) — من دون فتح أي ملف:
jq '.["01_outreach"]' /root/r/V3/01_ATOMS/SEGMENT_MAP.json
# عدد الذرّات والملفات الخماسية لهذا القطاع:
jq -r '.nb2.terms_26k.sectors["01_outreach"]' /root/r/V3_SYS/COUNTS.json
# ترشيح عيوب قطاع على القرص (بلا نسخ نتائج):
rg -n '01_outreach' /root/r/V3/DEFECTS.jsonl | head
```

## 5) ما الذي يُكتب في V3 بدل النسخ

| ما تُنتجه | مكانه | الحجم |
|---|---|---:|
| خريطة القطاعات | `01_ATOMS/SEGMENT_MAP.json` · `02_CONCEPTS/SEGMENT_MAP.json` | < 12KB |
| فهرس brain بالقنوات | `07_SOURCES/SOURCE_INDEX.json` | < 400KB |
| قوائمMeasured | `MASTER_QUEUE.csv` · `SECTOR_MAP.md` · `COVERAGE_MATRIX.md` | < 100KB |
| سجلات | `12_LOGS/LOOP_LOG.md` · `WORK_LOG.md` | < 20KB |
| **الإجمالي الجديد في V3** | — | **< 1MB مقابل 339MB** |

## 6) متى يُسمح بالنسخ (الاستثناء الوحيد)

| الحالة | المسموح |
|---|---|
| إصدار frozen لماستر واحد مؤرَّخ | نسخة واحدة في `10_ARCHIVE/` مع سطر `ARCHIVE_MANIFEST.jsonl` |
| مادّة خام لا يمكن مراجعتها بالمسار الأصلي | **لا** — يُكتب ملخّص+mصدر المسار فقط |
| أي شيء آخر | **لا** |

** tombstones:** الملف المحذوف من v1/v2 يبقى مقروءاً عبر `10_ARCHIVE/ARCHIVE_MANIFEST.jsonl` — انظر ذلك الملف.