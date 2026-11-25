# تشخيص `no_progress` — ترقيم صفحات إنستقرام يستسلم عند 60 منشوراً

تشخيص ساكن من الكود وحده. صفر لمس للشبكة، صفر تشغيل حصاد.

## السبب الجذري (سطر واحد)

الحلقة تقيس التقدّم **بعد إزالة التكرار** (`drain.gained`) وبمؤشّر `end_cursor`
الذي يُعطَّل صامتاً كلما كان `null`، بينما الشاهد الثالث الموثّق `bodies_seen`
(وصول ردّ شبكة أصلاً) **محسوب ولا يُقرأ أبداً** — فدفعة وصلت بمنشورات كلّها
مكرّرة تُحسَب "جولة فاضية" فتحرق ميزانية الصبر ويُصدر `no_progress` والحساب فيه
المزيد.

## الملف:السطر

- `src/browse.py:590-591` — مُصدِر `no_progress`: `if idle_rounds >= _idle_limit(has_next): return "no_progress"`.
- `src/browse.py:722` — قياس التقدّم: `moved = drain.gained > 0 or (drain.cursor != "" and drain.cursor != cursor)`. **`bodies_seen` غائب عن الشرط.**
- `src/browse.py:535` — `bodies_seen=parsed_bodies` يُحسب هنا.
- `src/browse.py:470` + `src/browse.py:663-667` — الـ docstring **يوثّق** الشاهد الثالث نصاً: الجولة لا تُحسب فاضية إلا إذا لم تكسب منشوراً **و** لم يتغيّر المؤشّر **و** «لم يصل ردّ شبكة أصلاً». التنفيذ أضيق من الوثيقة.
- `src/browse.py:529-533` — الـ dedup بـ `code in seen` هو ما يجعل `gained` رقماً **بعد** الفلترة لا عدد عقد DOM الواصلة.
- `src/browse.py:459` — `cursor = page_info.get("end_cursor") or ""`؛ ومع الشرط `drain.cursor != ""` في السطر 722 فإن `end_cursor: null` = «لا تقدّم» حتى لو وصلت دفعة كاملة.
- `src/browse.py:566-568, 70-71` — عدد الجولات قبل الاستسلام: `SCROLL_IDLE_LIMIT_HAS_NEXT = 15` لو `has_next is True`، وإلا `SCROLL_IDLE_LIMIT = 7`. و`has_next` لاصق (`browse.py:718` لا يحدّثه إلا إذا لم يكن None)، فغياب `page_info` يُبقيه None → السقف 7 → دورة واحدة ونصف فقط على سلّم الإيماءات الخمس.

## شاهد القرص

`state/runs/full_20260804_040944/harvest_summary.json`: `accounts.suprava.ss = 60`،
`raw_seen = 60`، `stop_reasons = "no_progress"`، `hard_stop = null`.

60 = 5 دفعات × 12. `max_items` كان 500 (`config/settings.yaml:19`) و`max_minutes`
45 — فلا السقف ولا الزمن هو القاطع، وإلا لقال السبب `max_items` أو `max_minutes`.

**عيب ثانٍ يفسّر عجزنا عن الحسم**: `scripts/full_harvest.py:91` يُنشئ
`exhaustion_evidence: {}` و`_LAST` (سطر 47-62) و`_PROFILE_COUNT_JS` (سطر 65)
— **ولا شيء منها يُكتب في الملخّص أبداً**. لذلك `has_next` الأخير غير مُسجَّل.
والملخّص على القرص **يخلو** من مفتاح `exhaustion_evidence` أصلاً (mtime الملخّص
04:15 مقابل السكربت 04:19)، أي أن الرن سبق هذه النسخة.

### المقطوع صراحةً (لم أره فلا أكتبه)

- لا أجسام GraphQL محفوظة في المستودع (بحثت: صفر نتائج)، فلا سبيل ساكن لمعرفة هل حملت الدفعة الخامسة `has_next_page=true` أم `false` أم لا `page_info` إطلاقاً.
- لا لوج تمرير في مجلد الرن: محتواه `dedup_local.sqlite`, `harvest_summary.json`, `media/`, `media_shard1/`, `posts/`, `reading/` فقط. و`logs/` فارغ.
- عدد منشورات الحساب الحقيقي **غير معلوم** (يتطلب شبكة). مدى المنشورات الستين 2025-09-18 → 2026-07-27 (312 يوماً).
- لذلك لا أستطيع نفي احتمال أن الحساب استُنفد فعلاً بدفعة أخيرة `end_cursor: null`. الإصلاح أدناه يُزيل استسلاماً مبكراً موثّقاً، ولا يخلق دفعة سادسة لو صمتت الشبكة حقاً.

## الإصلاح المقترح (diff نصي)

```diff
--- a/src/browse.py
+++ b/src/browse.py
@@ SCROLL_IDLE_LIMIT_HAS_NEXT = 15
+# ميزانية الجولات التي يكفي فيها **وصول ردّ** ليُعدّ تقدّماً: الشاهد الثالث
+# الموثّق في paginate_timeline وكان مهجوراً. محدودة لا مفتوحة، وإلا صار الردّ
+# المكرّر الدائم حلقة لا تنتهي إلا بالجدار الزمني.
+SCROLL_STALE_BODY_BUDGET = 6
@@ paginate_timeline
     idle_rounds = 0
+    stale_body_rounds = 0
@@
-        moved = drain.gained > 0 or (drain.cursor != "" and drain.cursor != cursor)
+        real_move = drain.gained > 0 or (drain.cursor != "" and drain.cursor != cursor)
+        if real_move:
+            stale_body_rounds = 0
+            moved = True
+        elif drain.bodies_seen > 0 and stale_body_rounds < SCROLL_STALE_BODY_BUDGET:
+            stale_body_rounds += 1
+            moved = True
+        else:
+            moved = False
```

## كيف يُتحقق منه لاحقاً

المعيار المطلوب: `stop_reasons` = `has_next_page=false` **و** عدد المنشورات > 60.

1. ساكناً الآن: `python3 -m pytest tests/ -q` — اختبار الانحدار
   `test_body_arrival_alone_is_not_idle` يُثبت أن جولة بردّ مكرّر لا تُحسب فاضية.
2. حيّاً لاحقاً (خارج نطاق هذه المهمة، تحتاج شبكة): شغّل
   `xvfb-run -a python3 scripts/full_harvest.py <run_id> suprava.ss 500` ثم اقرأ
   `state/runs/<run_id>/harvest_summary.json`.
3. **قبل أي رن حيّ، أصلح العيب الثاني**: املأ `exhaustion_evidence` من `_LAST`
   في `scripts/full_harvest.py` (has_next الأخير + cursor + عدد الـ drains).
   بدونه سيعود `no_progress` غامضاً كما هو الآن ولن يُحسم شيء.

## ما نُفِّذ فعلاً (مُحقَّق)

الإصلاح **مُطبَّق** في `src/browse.py` (لا في `scripts/`)، وبميزانية محدودة بدل
الشرط المفتوح الذي في الـ diff أعلاه:

- `src/browse.py` — أُضيف `SCROLL_STALE_BODY_BUDGET = 6` بعد `SCROLL_IDLE_LIMIT_HAS_NEXT`.
- `src/browse.py` — `paginate_timeline`: أُضيف عدّاد `stale_body_rounds`، وحُوّل `moved` إلى ثلاثة فروع: تقدّم حقيقي (يُصفّر الميزانية) / ردّ واصل بلا تقدّم (يُغتفر حتى نفاد الميزانية) / لا شيء (ركود).
- الـ docstring حُدِّث ليصف الحدّ، فلا تعود الوثيقة أوسع من التنفيذ.

**نتيجة الاختبارات الحقيقية**: `python3 -m pytest tests/ -q` → **347 passed**
(41.38s). صفر فشل، وكل الاختبارات الـ 345 السابقة سليمة.

اختباران جديدان في `tests/test_harvest.py`:

- `test_body_arrival_alone_is_not_idle` — 18 جولة ردّ مكرّر ثم دفعة جديدة → النتيجة `["C0","C1","C2","C3"]` و`has_next_page=false`.
- `test_repeated_duplicate_bodies_eventually_idle` — ردّ مكرّر بلا دفعة جديدة → لا يزال يستسلم بـ `no_progress` (حراسة ضد الحلقة اللانهائية).

**الاختبار غير أجوف — مُتحقَّق تجريبياً**: بتثبيت `SCROLL_STALE_BODY_BUDGET = 0`
(محاكاة المنطق القديم) يفشل `test_body_arrival_alone_is_not_idle` ويعطي
`(2 منشورين, no_progress)`، وبالإصلاح يعطي `(4 منشورات, has_next_page=false)`.
العدد 18 مقصود: جرّبت 15/16/17 فنجحت في **الحالتين** (لا تفصل شيئاً)، وأول عدد
يفصل السلوكين هو 18.

### ما يبقى غير محسوم بعد الإصلاح

هذا الإصلاح يُزيل استسلاماً مبكراً **مُثبَتاً بالاختبار**، لكنه لا يُثبت أن هذا
هو ما قصّ رنّ 2026-08-04 عند 60. لو كانت الجولات الفاضية في ذلك الرن **بلا أي
ردّ** (`bodies_seen == 0`) فالإصلاح لا يغيّر شيئاً هناك، والسبب يكون في
الإيماءات/الحسّاس أو حجب ناعم — وذلك لا يُحسم إلا برنّ حيّ مع
`exhaustion_evidence` مملوءاً (البند 3 أعلاه).
