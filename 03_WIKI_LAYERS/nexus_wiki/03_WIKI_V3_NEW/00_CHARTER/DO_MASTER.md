# DO_MASTER — كيف يُكتب ماستر `M_` ويُعتمد في V3

> ⚠️ صحّح 2026-10-02: المسارات V3/03_CONCEPTS→02_CONCEPTS · V3/02_TERMS→01_ATOMS · V3/07_MASTERS→03_MASTERS · V3/01_SOURCES→07_SOURCES. الدليل: test -e + ls -d /root/r/V3/*/

<!-- counts-ref: V3_SYS/COUNTS.json -->
<!-- atoms=27742 concepts=1841 masters=5 -->

> ⚠️ صحّح 2026-10-02 (T1+T2): كان الوسم `concepts=1841` مخلوطاً بين ملف ومفهوم — والصحيح فصل الحقلين: `concepts=1836 files=1841`، ومعه `masters=5 indexes=5 masters_total=10`. الوسم المصحَّح: `<!-- atoms=27742 concepts=1836 files=1841 masters=5 indexes=5 masters_total=10 -->`.
> الدليل: `find /root/r/NB2/02_CONCEPTS -name 'Concept_*.md' -not -path '*terms_26k*' | wc -l` ⇒ **1836** · `find /root/r/NB2/02_CONCEPTS -name '*.md' -not -path '*terms_26k*' | wc -l` ⇒ **1841** · `find /root/r/NB2/03_MASTERS -name 'Master_*.md' | wc -l` ⇒ **5** · `find /root/r/NB2/03_MASTERS -name '_index.md' | wc -l` ⇒ **5**.

> **هذا الملف إجرائي.** البنية والمحتوى في `FORMAT_MASTER.md`، والعقد المعرفي ضد الوصفة الميتة في `ANTI_DEAD_FORMULA.md`.
> كل بند يحمل **الأمر الحرفي** الذي يُثبته. بند بلا أمر = بند غير موجود (`GATES_11.md` §4).

> ⚠️ صحّح 2026-10-02 (مرجع مخترَع): العبارة «بند بلا أمر = بند غير موجود (`GATES_11.md` §4)» ⇒ **§4 في `GATES_11.md` عنوانه «الجذر العددي — من أين جاءت العتبات» وليس قاعدة «بند بلا أمر»؛ العبارة نفسها غير موجودة في الوثيقة** ⇒ المرجع الصحيح `GATES_11.md` **§5 «أمر التشغيل الكامل»**. الدليل: `grep -n 'بند بلا' /root/r/V3/00_CHARTER/GATES_11.md` ⇒ **0** (لا وجود) · `grep -n '^## 4)\|^## 5)' /root/r/V3/00_CHARTER/GATES_11.md` ⇒ `94:## 4) الجذر العددي…` · `141:## 5) أمر التشغيل الكامل`.
> **سطر التهيئة** الذي تفترضه كل الأوامر أدناه — بلا هذا السطر تكون الأوامر غير قابلة للتشغيل (`GATES_11.md` §2.1):

```bash
ROOT=/root/r
f="$ROOT/V3/07_MASTERS/05_branding/M_Brand_Architecture_System.md"
```

> ⚠️ **صحّح 2026-10-02 (T7 + قوائم القطاع):** سطر التهيئة أعلاه **مكسور على ثلاث جهات**: (1) `07_MASTERS` ⇒ الصحيح **`03_MASTERS`**؛ (2) قطاع `05_branding` غير موجود ⇒ الصحيح **`07_branding`**؛ (3) `M_Brand_Architecture_System.md` غير موجود على القرص ⇒ **مثال افتراضي** (انظر `V3/CHARTER_AUDIT.md` §2.4: 5 من 5 أمثلة غير موجودة).
> السطر المُصلَح: `f="$ROOT/V3/03_MASTERS/07_branding/M_Brand_Architecture_System.md"` (مثال افتراضي — الملف غير موجود).
> **الدليل:** `test -d /root/r/V3/07_MASTERS && echo EXISTS || echo FAIL` ⇒ **FAIL** · `test -d /root/r/V3/03_MASTERS && echo EXISTS || echo FAIL` ⇒ **EXISTS** · `find /root/r/V3/02_CONCEPTS /root/r/V3/01_ATOMS -maxdepth 1 -name '05_branding' | wc -l` ⇒ **0** · `test -d /root/r/V3/02_CONCEPTS/07_branding && echo EXISTS || echo FAIL` ⇒ **EXISTS** · `find /root/r -name 'M_Brand_Architecture_System.md' | wc -l` ⇒ **0**.


## 1) البند 1 — `grep -c '^## §'` = **18** بالضبط (لا 17 ولا 19 ولا 36)

```bash
grep -c '^## §' "$f"                                              # ⇒ 18
grep '^## §' "$f" | sed 's/^## §[0-9]*[: ]*//' | sort | uniq -d   # ⇒ فارغ: لا عنوان مكرَّر
```

**لماذا لا يكفي `≥18`:** عيب موثّق في `data/masters/Master_Brand_Identity_System.json` — 36 قسماً، §19–§36 نسخة من §1–§18، و16 من 18 متن متطابق بايتاً (قِسْتُه 2026-10-01: 53.6% كلمات · 50.8% أسطر). رقم 36 يمرّ على فاحص `C07` (شرطه ≥18) ⇒ **البوابة عدّاد قروسط لا حارس جودة**. القسمة إلى 18 بالضبط هي الحارس.

> ⚠️ **صحّح 2026-10-02 (T15 · «متطابق بايتاً» مبالغ فيه):** كان «16 من 18 متن متطابق بايتاً» ⇒ القياس على القرص: **0 من 18 متطابق بايتاً**، و**16 من 18 متطابق بنسبة ≥ 99%** فقط؛ الأدنى `§15↔§33 = 51.7%` و`§18↔§36 = 85.5%`. ونسب النسخ بأمر جديد **53.5% كلمات · 50.9% أسطر** (لا 53.6/50.8). **الاستنتاج سليم**: التكرار موجود والدعوى بالنسخة صحيحة؛ المتبالغ فيه هو الصفة البايتية وحدها.
> **الدليل:** `python3 -c "import json,re,difflib;d=json.load(open('/root/r/data/masters/Master_Brand_Identity_System.json'));b={};[b.setdefault(int(m.group(1)),x) for x in re.split(r'(?m)^##\s*§',d['content'])[1:] if (m:=re.match(r'^\s*(\d+)',x))];print('identical',sum(1 for i in range(1,19) if b[i]==b[i+18]),'ge99',sum(1 for i in range(1,19) if difflib.SequenceMatcher(None,b[i],b[i+18]).ratio()>=0.99))"` ⇒ `identical 0 ge99 16`.


## 2) البند 2 — `wc -w` ≥10,000 كلمة (مصدره `MASTER_MAKING_SPEC.md` الخطوة هـ)

```bash
[ "$(wc -w < "$f")" -ge 10000 ] && echo "B2 OK"
```

**لماذا لا يكفي:** حدّ للكلّي بلا حدّ لكلّ قسم يجعل التوسّع أسهل عدد — فينفجر §4 وحده. لذلك البند 3 يثبّت الـ40%.


## 3) البند 3 — §4 ≥40% من الكلّي ⇒ ≥4,000 كلمة (`MASTER_MAKING_SPEC.md:63`)

```bash
total=$(wc -w < "$f"); s4=$(awk '/^## §4/{f=1;next}/^## §/{f=0}f' "$f" | wc -w)
echo "§4 = $s4 / $total"
awk -v a="$s4" -v t="$total" 'BEGIN{exit !(a*100/t >= 40)}' && echo "B3 OK"
```

**الفخ:** `MASTER_MAKING_SPEC.md` يحذّر في السطر التالي: «إن سقطت بوابة: عمّق §4 — **لا تحشُ**». الحشّ يُبقي البند 3 أخضر ويُبطل الماستر ⇒ مراجعة يدوية إلزامية: هل كل نظام في §4 له **متى تُشغّله · مدخل · مخرج · حدّ فناء**؟


## 4) البند 4 — §15 ≥1,800 كلمة تحليل مستقل (أنماطك أنت) — `MASTER_MAKING_SPEC.md:70`

```bash
awk '/^## §15/{f=1;next}/^## §/{f=0}f' "$f" | wc -w              # ⇒ ≥1,800
```

**التعارض المُلغى:** `NB2/00_SYSTEMS/SYSTEM_03_MASTERS.md:49` يقول «§15 = مصطلحات متقدمة» ⇒ قسماً بلا حدّ كمّي قابل للقياس. الحكم **NULL** (`FORMAT_MASTER.md` §0 · تعارض #2).


## 5) البند 5 — §18 = **100%** مفاهيم قطاعك بصيغة `[[C_Slug]]`، وصفر رابط وهة

```bash
grep -o '\[\[C_[^]]*\]\]' "$f" | wc -l                            # ⇒ عدد مفاهيمك
grep -o '\[\[[^]]*\]\]' "$f" | tr -d '[]' | sort -u | while read -r s; do
  find "$ROOT/V3/03_CONCEPTS" -name "$s.md" >/dev/null || echo "وهة: $s"
done                                                               # ⇒ يجب أن يطبع صفراً
```

> ⚠️ **صحّح 2026-10-02 (T7 · بند التغطية 5 لا يمرّ أصلاً):** كان `find "$ROOT/V3/03_CONCEPTS"`، والقرص فيه `02_CONCEPTS/` ⇒ الأمر يخرج **1** لكل رابط ⇒ يطبع «وهة» لكل رابط، أي 100% روابط وهمية. الصحيح: `find "$ROOT/V3/02_CONCEPTS" -name "$s.md" >/dev/null || echo "وهة: $s"`.
> **الدليل:** `test -d /root/r/V3/03_CONCEPTS && echo EXISTS || echo FAIL` ⇒ **FAIL** · `test -d /root/r/V3/02_CONCEPTS && echo EXISTS || echo FAIL` ⇒ **EXISTS**.

**عيب v2 المقيس:** `grep -c '\[\['` = **0** على 27,742 بطاقة ⇒ §18 كان جدولَ أسماء بلا روابط: لا يُقرأ كخريطة ولا يُتحقَّق منه.
**عن معنى «100%»:** `V3/03_CONCEPTS/` يضم 1,841 ملفاً (1,840 `.md` + `_INDEX.md`)؛ «تغطية 100%» تعني **كل مفاهيم قطاعك أنت**، لا الـ1,841 — الباقي على زملائك في قطاعاتهم.

> ⚠️ **صحّح 2026-10-02 (T7 + T1 · المعنى لا العِدّ فقط):** كان `V3/03_CONCEPTS/` (غير موجود) و«1,841 ملفاً (1,840 `.md` + `_INDEX.md`)» — والصحيح: المجلد **`V3/02_CONCEPTS/`**، وعلى القرص فيه **71 ملف `C_` فقط** (لا 1,841 ولا 1,840 ولا `_INDEX.md`) ⇒ **لا تُشتق أي نسبة تغطية من 1,841 في V3**؛ المقام المعتمد للتغطية في `V3/COVERAGE_MATRIX.md` هو **1,836 مفهوماً في NB2** (697 مغطّاة = 38.0%).
> **الدليل:** `test -d /root/r/V3/03_CONCEPTS && echo EXISTS || echo FAIL` ⇒ **FAIL** · `find /root/r/V3/02_CONCEPTS -name 'C_*.md' | wc -l` ⇒ **71** · `find /root/r/V3/02_CONCEPTS -name '_INDEX.md' | wc -l` ⇒ **0** · `find /root/r/NB2/02_CONCEPTS -name 'Concept_*.md' -not -path '*terms_26k*' | wc -l` ⇒ **1836** · `grep -n '697' /root/r/V3/COVERAGE_MATRIX.md | head -1` ⇒ `37: 1,836 − 697`.


## 6) البند 6 — YAML كامل: `type` · `version` · `lineage` · `gates_passed` + التعداد الثلاثي (D01)

```bash
grep -m1 '^type:' "$f"; grep -m1 '^version:' "$f"               # ⇒ type: master  ·  version: V3.0
grep -m1 '^lineage:' "$f"; grep -m1 '^gates_passed:' "$f"       # ⇒ lineage: سلسلة · gates_passed: N/11
basename "$f" | cut -c1 ; dirname "$f"                          # ⇒ M · .../07_MASTERS
```

> ⚠️ صحّح 2026-10-02 (T7): التوقع `.../07_MASTERS` ⇒ الصحيح **`.../03_MASTERS`**. الدليل: `test -d /root/r/V3/07_MASTERS && echo EXISTS || echo FAIL` ⇒ **FAIL** · `test -d /root/r/V3/03_MASTERS && echo EXISTS || echo FAIL` ⇒ **EXISTS**.

**`gates_passed: N/11` رقم لا نصّ:** لأن نصّاً مثل «مرّ بالبوابات» غير قابل للتصحيح ولا للنقض. وقيمته تُحدَّث من `GATES_11.md` وحده.
**`lineage` سلسلة لا عبارة:** تُدرج فيها المراجع الملغاة (مثل `SYSTEM_03_MASTERS.md = NULL`) — المرجع الملغى يُسمّى ليُقرأ على أنه ملغى.


## 7) البند 7 — `audit.py --fail-on 8` ⇒ exit 0 (صفر مخالفة خطورة ≥8؛ يُنفَّذ **أخيراً** لأنه يجمع ما قبله)

```bash
python3 "$ROOT/V3_SYS/audit.py" --root "$ROOT/NB2" --checkers C07,C17 --fail-on 8 --quiet
echo "exit=$?"                                                   # ⇒ 0
```

**الفارق عن `GATES_11.md`:** البوابات `D01..D11` **واجهة مختصرة** فوق 28 فاحصاً `C01..C28`، وهذه **لا تغطي D01** — لأن `audit.py` يفحص المحتوى لا هوية الملف (الفجوة موثّقة في `GATES_11.md` §7).
**النتيجة:** البند 7 **لا يكفي وحده**؛ البندان 1 و6 هما اللذان يسدّان فجوة `D01`. لا يُغلق أي بند إلا بسبعة معاً.


## 8) البند 8 — `status: complete` (بعد 1-7 لا قبله) + صفّ مؤرّخ في LOG.md

```bash
grep -m1 '^status:' "$f"                                        # ⇒ status: complete
grep -c 'M_Brand_Architecture_System' "$ROOT/NB2/00_SYSTEMS/LOG.md"  # ⇒ ≥1
```

**صيغة الصف:**
```
## 2026-10-01 — ماستر Brand Architecture (V3.0)
- البوابات: 11/11 · البنود الثمانية: 8/8 · الكلمات: 12,4xx · §4: 41.2% · §15: 1,9xx
- §18: 214/214 رابط [[C_]] · YAML: lineage كامل · gates_passed: 11/11
- audit.py --fail-on 8: exit=0
- مرجع البنية: FORMAT_MASTER.md (SYSTEM_03_MASTERS.md = NULL)
```
**نقطة الاعتماد:** `status: complete` **يُكتب بعد** 1-7 لا قبله؛ فإن سقط بندٌ بعده، يُعاد `status: draft` ويُكتب سبب النقص في السجل.


## 9) جدول الحالة — لكل بند

| # | البند | العتبة | الأمر المميِّز | مُنجَز | ناقص | موزون |
|---|---|---|---|---|---|---|
| 1 | 18 قسماً | `= 18` | `grep -c '^## §'` | 16 · `sort \| uniq -d` فارغ | — | — |
| 2 | إجمالي الكلمات | ≥10,000 | `wc -w < "$f"` | — | — | — |
| 3 | §4 حصة | ≥40% | نسبة `awk -v a=… t=…` | — | — | — |
| 4 | §15 | ≥1,800 | `awk '/^## §15/` | — | — | — |
| 5 | §18 تغطية | 100% | `grep -o '\[\[C_'` | — | — | — |
| 6 | YAML كامل | 4 حقول | `grep -m1 '^type:'` | — | — | — |
| 7 | تدقيق آلي | exit 0 | `audit.py --fail-on 8` | — | — | — |
| 8 | الاعتماد | صفّ في LOG | `grep -m1 '^status:'` | — | — | — |

> الجدول **قالب حالة فارغ، لا تقرير ادّعاء**: كل خانة تُملأ بناتج أمرٍ نُفِّذ فعلاً. الصف المملوء بلا أمرٍ مُنفَّذ = خانة فارغة (`TRUTH_NUMBERS.md` §1).


## 10) ترتيب التنفيذ

1. سؤال الماستر **واحداً** — بلا سؤال لا ماستر (`ONTOLOGY.md` §1 · `M_`).
2. اجمع كل مفاهيم القطاع ⇒ منها تغطية §18 بالضبط (البند 5).
3. اكتب §4 أولاً (أكثف الأقسام) ثم §15 ثم الباقي؛ **§1 أخيراً** لأنه وعد لا مقدّمة.
4. مرّر البنود 1-7 — البند 7 أخيراً لأنه يجمع ما قبله.
5. `status: complete` ثم صفّ السجل (البند 8).
6. تعارض بنية مستقبلي مع `FORMAT_MASTER.md`: هذا الملف الحاكم؛ يُسجَّل التعارض في §0 منه، **ولا يُفتح مرجع ثانٍ**.

> المرافق: `ANTI_DEAD_FORMULA.md` — كل `{formula}` يكتبها بند 3 يمرّ على فحوصه قبل أن يدخل §4.