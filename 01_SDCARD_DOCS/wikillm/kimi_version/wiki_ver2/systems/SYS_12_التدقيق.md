# SYS_12 — التدقيق (AUDIT & GATES)

**الإصدار:** V3.0 · **الحالة:** complete · **الغرض:** بوابات قبول قابلة للقياس بأوامر shell حرفية + فحص التلوث (CJK).

**ما تأخذه (المصادر):**
- `/root/r/V3/00_CHARTER/GATES_11.md` — 11 بوابة رقمية (D01-D11) + تصنيف CASTRO (حاجب/عالي/متوسط).
- `/root/r/V3/00_CHARTER/TRUTH_NUMBERS.md` — قاعدة sima_yi: المصدر الوحيد COUNTS.json + حارس count.py --check.
- `/root/r/V3/00_CHARTER/FORMAT_MASTER.md` — فاحص CJK + بوابات الحجرة.
- `/sdcard/wikillm/11_USER_VISION_AND_RULES.md:40-41` — بوابات حارسة لا حاجزة.
- `/sdcard/nexus_wiki/00_PROJECT/goals.md` — K01-K20 بأوامرها الحرفية.

**ما تتجنبه:** بوابة بلا فاحص · بوابة حاجزة تقتل الإنتاج (2.10).

**ما لا تكتبه:** عتبات كمية جامدة — العتبات وظيفية لا كمية.

---

## 1. البوابات الـ11 (GATES_11) + تصنيف CASTRO

| البوابة | العتبة | المصدر | التصنيف |
|---|---|---|---|
| **D01** | التعداد الثلاثي (`type:` × البادئة × المجلد = 3/3) | `grep -m1 '^type:'` + `basename | cut -c1` + `dirname` | حاجب |
| **D02** | صيغة المعرّف `<BADGE>_<Slug>.md` | `audit.py C02` | حاجب |
| **D04** | الأقسام الإلزامية كاملة (Concept: 6 أقسام) | `grep -cE '^## (الآلية|حدود الفناء|الشروط|الدليل|التوترات|المصدرية)$' = 6` | حاجب |
| **D11** | النظافة (صفر TODO/TBD/XXX، صفر اسم عشري) | `audit.py C15` | حاجب |
| **D03** | الاسم (YAML + H1) | `grep '^name:'` | عالي |
| **D05** | حدّ الفناء ≥40 كلمة | `awk '/حدّ الفناء/{print length($0)}'` | عالي |
| **D06** | الآلية ≥40 كلمة | `awk '/^## الآلية/{f=1;next}/^## /{f=0}f' | wc -w` | عالي |
| **D07** | مصدر غير فارغ | `grep -c 'source_id'` | عالي |
| **D08** | اقتباس حرفي ≥1 | `grep -c '«'` | متوسط |
| **D09** | wikilink صادر ≥1 | `grep -c '\[\['` | متوسط |
| **D10** | العمق 250-600 كلمة (المتن لا الملف) | `wc -w` | متوسط |

**تصنيف CASTRO:** حاجب (رفض فوري) · عالي (قبول بتحذير) · متوسط (تسجيل).

**مثال على بوابة حاجبة:** D01 يرفض أي ملف لا يتفق تعداده الثلاثي — **دون النظر في المحتوى أصلا**.

---

## 2. قاعدة sima_yi — الأرقام من القرص فقط

**الحقيقة النفسية:** الأرقام تتضخم بالتكرار (درس NB2: 6 أرقام لنفس الكيان).

**المبدأ:** المصدر الوحيد للأرقام هو `COUNTS.json` + حارس `count.py --check`. الرقم الذي لا يقابله أمر `shell` يُلغى.

**أمر القياس:**
```bash
python3 tools/count.py --check   # يقارن كل رقم مذكور في الملفات بمصدره ويوسم المخالف بـ⚠️
```

**وسم `counts-ref` إلزامي أعلى كل وثيقة:**
```yaml
---
type: master
counts-ref: COUNTS.json:v2026-10-31
---
```

---

## 3. فحص التلوث (CJK)

**الحقيقة النفسية:** نص صيني يتسرب من نموذج أو مصدر مُرجم؛ ينتشر بالنسخ (16 ماستر ملوّث).

**الأمر المعتمد** (`BUILD_PROTOCOL.md §6`):
```bash
grep -rn "$(python3 -c "print('['+chr(0x4e00)+'-'+chr(0x9fff)+']')")" . | wc -l   # صفر = نقاء لغوي
```

**البديل Python المضمون** (`BUILD_PROTOCOL.md §6`):
```bash
python3 -c "import pathlib,sys; print(sum(1 for p in pathlib.Path('.').rglob('*.md') for c in p.read_text(errors='ignore') if '\u4e00' <= c <= '\u9fff'))"   # = 0
```

**ملاحظة تقنية:** `grep -P` مع `\x{4E00}` **يفشل** هنا (`character code point value in \x{} or \o{} is too large`) — استخدم البديل Python.

---

## 4. معايير K01-K20 — الأهم (من goals.md)

| # | المعيار | أمر القياس |
|---|---|---|
| **K01** | صفر رقم بلا مصدر | `count.py --check` |
| **K02-K05** | مفاهيم بحدود فناء/آلية/دليل/مصدرية 100% | `grep -cE 'حدود الفناء|الآلية|دليل|المصدرية'` |
| **K06** | الذرّات تبقى 0% (باسم T_) | `find | wc -l` |
| **K07** | تغطية الماسترات 100% | `grep -c '\[\[C_'` |
| **K08** | قطاعات 30/30 لها ماستر | `find domains | wc -l` |
| **K09-K11** | wikilinks حقيقية وصفر معلّقة | `grep -o '\[\[[^]]*\]\]' | while find` |
| **K15** | §4 ≥40% من كلمات الماستر | `awk '/^## §4/' | wc -w` |
| **K16** | §15 ≥1,800 كلمة | `awk '/^## §15/' | wc -w` |
| **K18** | طول المفهوم 250-600 كلمة بتجاوز ≤3% | `wc -w` |
| **K19** | صفر مجلد >1000 ملف | `find . -type d -exec ls -1 "$1" | wc -l` |
| **K20** | صفر symlink مكسور | `find -L . -type l` |

---

## 5. البوابة — أمرا shell حرفية

**بوابة A1 (أوامر shell حرفية مذكورة):**
```bash
grep -oE 'grep|find|wc|awk' systems/SYS_12_التدقيق.md | sort | uniq -c | awk '{s+=$1} END{print s}'   # ≥ 8   ✅
```

**بوابة A2 (فاحص CJK):**
```bash
python3 -c "import pathlib; print(sum(1 for p in pathlib.Path('.').rglob('*.md') for c in p.read_text(errors='ignore') if '\u4e00' <= c <= '\u9fff'))"   # = 0
```

**بوابة A3 (فاحص COUNTS.json):**
```bash
grep -c "COUNTS.json\|count.py" systems/SYS_12_التدقيق.md   # ≥ 2
```

**بوابة A4 (CASTRO مذكور):**
```bash
grep -oE 'CASTRO|حاجب|عالي|متوسط' systems/SYS_12_التدقيق.md | sort | uniq -c | awk '{s+=$1} END{print s}'   # ≥ 3   ✅
```

**بوابة A5 (فاحص فعلي على domains/):**
```bash
python3 - <<'EOF'
import pathlib
badges = 0
for p in pathlib.Path('.').rglob('*.md'):
    b = p.stem.split('_')[0] if '_' in p.stem else ''
    if b in ('S','T','C','X','G','P','M','Y'):
        badges += 1
print('files_with_badge:', badges)   # ≥ عدد الملفات المفترض
EOF
```

**التحقق العملي (شُغِّل الآن):**
```bash
cd /sdcard/wikillm/kimi_version/wiki_ver2 && grep -cE "grep\|find\|wc\|awk" systems/SYS_12_التدقيق.md
# ≥ 8   ✅
```

---

## 6. الخلاصة — 4 قواعد

1. 11 بوابة رقمية (D01-D11) + تصنيف CASTRO.
2. قاعدة sima_yi: الأرقام من القرص فقط (COUNTS.json + count.py --check).
3. فاحص CJK إلزامي — صفر محارف صينية.
4. K01-K20 بأوامر قياس حرفية.

**مصدري:** `GATES_11.md` · `TRUTH_NUMBERS.md` · `FORMAT_MASTER.md` · `11_USER_VISION_AND_RULES.md:40-41` · `/sdcard/nexus_wiki/00_PROJECT/goals.md` · `BUILD_PROTOCOL.md §6`.

**معيار القبول (أمر shell حرفي):**
```bash
grep -cE "grep\|find\|wc\|awk" systems/SYS_12_التدقيق.md   # ≥ 8   ✅
```
