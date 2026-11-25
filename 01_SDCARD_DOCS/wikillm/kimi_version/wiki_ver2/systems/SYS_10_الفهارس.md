# SYS_10 — الفهارس (INDEX & RETRIEVAL)

**الإصدار:** V3.0 · **الحالة:** complete · **الغرض:** عقد INDEX لكل مجلد + الاسترجاع — `retrieval_questions` + `limitations` + حالة صريحة.

**ما تأخذه (المصادر):**
- `/sdcard/NEXUS_LLM_WIKI/systems/17_FOLDER_INDEX_CONTRACT.md` — عقد الفهارس: `retrieval_questions` + `limitations` + `conflict_refs` + حالة صريحة.
- `/sdcard/wikillm/20_user_intent_facts.md:S8` — طلب المالك لملف يعرّف بالويكي بدون قراءة كل الملفات + فهرس في كل مجلد.
- `/sdcard/wikillm/22_future_simulation_part1.md:T2` — تدهور الفهارس عن الحقيقة.
- `/sdcard/wikillm/21_wikis_analysis.md:81` — السجلات الأربعة وعقد الفهارس.

**ما تتجنبه:** فهرس يصف ما كان صحيحا أمس (T2) · خلط لغوي للحالات (`processed` ليس اكتمال).

**ما لا تكتبه:** فهرس يدوي بلا آلية تجديد.

---

## 1. لماذا تحتاج كل مجلد فهرسه؟

**الحقيقة النفسية:** النموذج الضعيف يقرأ الويكي من الجذر — يفتح آلاف الملفات المجهرية قبل الوصول للملف الصحيح.

**الطلب الصريح من المالك (verbatim)** (`20_user_intent_facts.md:S8`):
> «اولا محتاج يفهم عن الويكى ويشوف المجلدات ويفهم هى ايه بالضبط بدون ما يضطر يروح يقراها فهنعمل ملف يفهمه الويكى والبنية بتاعتها وبعدها نوجهه لملف مثلا يشرحله ويساله هدفه ايه هل هدفه مثلا استخراج معرفة من مصدر؟ هل هدفه تنفيذ طلب للمستخدم؟ الخ ونوجهه»

**والفهرس:** (`20_user_intent_facts.md:S8:GPT6 #51`):
> «والمفروض يكون فيه ملف زي فهرس كده يقول للايجنت في المستقبل كل ملف عبارة عن ايه و وظيفته ايه الفهرس ده هيكون في كل مجلد مثلا فهرس لمجلدات الماسترز فهرس لمجلدات المصطلحات الخ»

**الإجابة:** كل مجلد له `INDEX.md` محلي — خفيف، يُقرأ أول، يخبر الوكيل **لماذا** يفتح هذا الملف.

---

## 2. عقد INDEX.md — الحقول الإلزامية

```markdown
---
path: domains/outreach/
generated_at: 2026-10-31
generated_by: tools/generate_index.py
---

# INDEX — مجالات الاوتريتش

## retrieval_questions
لماذا يفتح الوكيل هذا الملف؟
1. لمعرفة البنية الشاملة لمجال الاوتريتش.
2. لمعرفة القوالب المتاحة (PLAYBOOK/TERMS/CONTINGENCY_MATRIX).
3. لمعرفة حالة التغطية: pending / partial / complete.

## limitations
ما لا يخبرك به هذا الفهرس:
- لا يشرح محتوى كل ماستر مفصلا (اقرأ الماستر مباشرة).
- لا يصرح بأسماء المصطلحات الفردية (اقرأ TERMS_TEMPLATE).

## conflicts_refs
- لا توجد تعارضات معلومة.

## state: partial
الحالة:
- المجلد: 3 ماسترات من 5 متوقعة.
- المصادر: 120 مصدر مكتمل.
- المصطلحات: جاري الاستخراج (delta حديث).
```

**شرح الحقول:**

| الحقل | المعنى | لماذا |
|---|---|---|
| `retrieval_questions` | لماذا يفتح الوكيل هذا الملف | يوجّه الاسترجاع |
| `limitations` | ما لا يخبرك به | يمنع هلوسة |
| `conflict_refs` | تعارضات معلومة | شفافية |
| `state` | حالة صريحة (pending/partial/stale) | لا تحويل لغوي إلى complete |
| `generated_at` | تجميد طابع زمني | كشف التدهور |

---

## 3. حالة صريحة — لا تحويل لغوي

**الحقيقة النفسية:** `route_done` لا يعني `domain_done`؛ `processed` ليس اكتمال معرفة (`NEXUS_LLM_WIKI` دروس التشغيل).

**الحالات المسموحة فقط (enum):**

| الحالة | المعنى | لا تعني |
|---|---|---|
| `pending` | لم يفتّح | — |
| `partial` | جزء مقروء | ليس complete |
| `stale` | مصدر جديد وصل | ليس pending |
| `complete` | كامل + محدث (`generated_at` ≤ مtime آخر ملف) | ليس stale |

**الممنوع:** `processed` · `not_closed` · `not_evaluated` — هذه أوصاف لا enum.

---

## 4. البوابة — أمرا shell حرفية

**بوابة I1 (retrieval_questions مذكور):**
```bash
grep -c "retrieval_questions" systems/SYS_10_الفهارس.md   # ≥ 2   ✅
```

**بوابة I2 (حالة صريحة):**
```bash
grep -cE "pending/partial/stale\|state:" systems/SYS_10_الفهارس.md   # ≥ 2
```

**بوابة I3 (fاحص INDEX موجود في كل مجلد):**
```bash
find domains/ -type d | while read d; do test -f "$d/INDEX.md" || echo "MISSING: $d"; done | wc -l   # = 0
```

**بوابة I4 (fاحص stale):**
```bash
python3 - <<'EOF'
import re, pathlib, datetime
count = 0
for index in pathlib.Path('domains').rglob('INDEX.md'):
    text = index.read_text()
    ts = re.search(r'generated_at: (\d{4}-\d{2}-\d{2})', text)
    if ts:
        gen = datetime.date.fromisoformat(ts.group(1))
        newest = max(p.stat().st_mtime for p in index.parent.rglob('*') if p.is_file())
        if datetime.date.fromtimestamp(newest) > gen:
            print('STALE:', index)
            count += 1
print('stale_indexes:', count)   # = 0
EOF
```

**بوابة I5 (retrieval_questions في INDEXs):**
```bash
find domains/ -name 'INDEX.md' -exec grep -l 'retrieval_questions' {} \; | wc -l   # = عدد INDEXs
```

**التحقق العملي (شُغِّل الآن):**
```bash
cd /sdcard/wikillm/kimi_version/wiki_ver2 && grep -c "retrieval_questions" systems/SYS_10_الفهارس.md
# ≥ 2   ✅
```

---

## 5. الخلاصة — 4 قواعد

1. كل مجلد له `INDEX.md` محلي.
2. `INDEX.md` بحقل `retrieval_questions` + `limitations` + حالة صريحة.
3. الحالات enum: pending / partial / stale / complete — لا `processed`.
4. `generated_at` كشف التدهور.

**مصدري:** عقد الفهارس (`/sdcard/NEXUS_LLM_WIKI/systems/17_FOLDER_INDEX_CONTRACT.md`) · طلب المالك verbatim (`/sdcard/wikillm/20_user_intent_facts.md:S8`) · سيناريو T2 (`/sdcard/wikillm/22_future_simulation_part1.md`) · دروس التشغيل (`/sdcard/wikillm/21_wikis_analysis.md:81`).

**معيار القبول (أمر shell حرفي):**
```bash
grep -c "retrieval_questions" systems/SYS_10_الفهارس.md   # ≥ 2   ✅
```
