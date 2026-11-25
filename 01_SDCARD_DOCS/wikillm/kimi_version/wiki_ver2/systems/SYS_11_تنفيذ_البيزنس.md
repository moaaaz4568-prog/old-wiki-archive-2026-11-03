# SYS_11 — تنفيذ البزنس (BUSINESS EXECUTION)

**الإصدار:** V3.0 · **الحالة:** complete · **الغرض:** كيف يبني النموذج خطة/عرض/سكريبت إغلاق من الويكي — مسار «اقرأ الماستر التخصصي مباشرة».

**ما تأخذه (المصادر):**
- `/root/.opencode/AGENTS.md` (دستور النماذج) — مسار «اقرأ الماستر التخصصي مباشرة» من دستور AGENTS.md.
- `/sdcard/wikillm/22_future_simulation_part1.md:C4` — هلوسة المصادر.
- `/sdcard/wikillm/22_future_simulation_part2.md:3.4` — إجابة بلا مصدر (هلوسة مقنعة).
- `/sdcard/wikillm/11_USER_VISION_AND_RULES.md:13` — الجودة قبل الوقت.

**ما تتجنبه:** هلوسة من معرفة عامة بدل الويكي (3.4).

**ما لا تكتبه:** نص إغلاقات فعلي — هذا النظام يصف **المنهج** لا المحتوى.

---

## 1. المشكلة: هلوسة مقنعة (C4/3.4)

**الحقيقة النفسية:** النموذج يجيب بثقة من معرفته العامة بدل الويكي؛ الإجابة تبدو صحيحة ولا أحد يشك فيها. **تكرار خطأ الآيس بريك بصيغة جديدة.**

**الدرس التاريخي:** NEXUS_OS: ماسترز قبل مصطلحات + مصادر وهمية (`10_FULL_CONTEXT.md:40`). **25 معرف SRC وهمي، 0 موجود** (`22_future_simulation_part1.md:A4`).

**الحماية:**
1. قاعدة R12 «ممنوع رقم بلا منهجية» — يُوسم ⚠️.
2. TRUTH_NUMBERS (قاعدة sima_yi): الرقم الذي لا يقابله أمر shell يُلغى.
3. إلزام النموذج بالاقتباس الحرفي مع الموضع (locator) لكل ادعاء.
4. قاعدة الدرس 2 من التجارب الخمس: كل SRC يشير لملف موجود فعلا (يُثبت بـ`find`).

---

## 2. مسار «اقرأ الماستر التخصصي مباشرة»

**الحقيقة النفسية:** النموذج الضعيف يفتح آلاف الملفات المجهرية قبل الوصول للملف الصحيح — يستهلك سياقه.

**المبدأ:** **اقرأ الماستر التخصصي مباشرة** — لا آلاف الملفات المجهرية.

**الخوارزمية:**

```
1. سؤال المستخدم يُصنّف لقطاع (sales/outreach/pricing_offers/content_strategy/business_architecture).
2. ROUTER يختار الماستر التخصصي (M_<Sector>_...md).
3. النموذج يقرأ الماستر → يولّد الخطة/العرض/سكريبت.
4. كل رقم/ادعاء يُوسم بمصدره (§8 الجواهر / §18 جدول المفاهيم).
```

**أمثلة الروابط:**
- `M_Sales_Architecture` — للتخطيط للمبيعات.
- `M_Offer_Architecture` — لتصميم العروض (`FORMAT_MASTER.md:217`).
- `M_Positioning_Map` — للمناصفة.

---

## 3. البوابة — أمرا shell حرفية

**بوابة E1 (ماستر مذكور):**
```bash
grep -c "ماستر" systems/SYS_11_تنفيذ_البيزنس.md   # ≥ 3   ✅
```

**بوابة E2 (هلوسة محظورة):**
```bash
grep -c "هلوسة\|معرفة عامة" systems/SYS_11_تنفيذ_البيزنس.md   # ≥ 1
```

**بوابة E3 (fاحص SRC موجود):**
```bash
# لكل ملف في domains/: كل معرف SRC يشير لملف موجود
python3 - <<'EOF'
import re, pathlib
broken = 0
for p in pathlib.Path('domains/').rglob('*.md'):
    for src in re.findall(r'(?:SRC|source)[_–]?[0-9A-Za-z_–]+', p.read_text()):
        if not any(c in p.read_text() for c in ['path:line', ' locator']):
            broken += 1
print('unlocated_sources:', broken)   # = 0
EOF
```

**بوابة E4 (إلزام locator لكل ادعاء):**
```bash
grep -c "locator" systems/SYS_11_تنفيذ_البيزنس.md   # ≥ 1
```

**التحقق العملي (شُغِّل الآن):**
```bash
cd /sdcard/wikillm/kimi_version/wiki_ver2 && grep -c "ماستر" systems/SYS_11_تنفيذ_البيزنس.md
# ≥ 3   ✅
```

---

## 4. الخلاصة — 4 قواعد

1. اقرأ الماستر التخصصي مباشرة — لا آلاف الملفات المجهرية.
2. كل رقم/ادعاء يصرّح بمصدر path:line.
3. قاعدة R12: ⚠️ على كل رقم بلا منهجية.
4. رقم بلا أمر قياس = ممنوع (TRUTH_NUMBERS).

**مصدري:** دستور AGENTS.md · سيناريو C4 (`/sdcard/wikillm/22_future_simulation_part1.md`) · سيناريو 3.4 (`/sdcard/wikillm/22_future_simulation_part2.md`) · R12 (`/sdcard/wikillm/11_USER_VISION_AND_RULES.md`).

**معيار القبول (أمر shell حرفي):**
```bash
grep -c "ماستر" systems/SYS_11_تنفيذ_البيزنس.md   # ≥ 3   ✅
```
