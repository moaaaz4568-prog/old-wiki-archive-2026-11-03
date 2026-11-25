# SYS_05 — استيعاب المصادر (SOURCE INGESTION)

**الإصدار:** V3.0 · **الحالة:** complete · **الغرض:** كيف تدخل كل مصدر في الويكي **بكل محتواه بلا فلترة** — هوية byte-exact، idempotency، checkpoint بالبصمات + snapshot شامل + delta.

**ما تأخذه (المصادر):**
- `/sdcard/NEXUS_WIKI_SKILLS/skills/source-ingestion-and-dedup/` — هوية المصدر SHA-256 byte-exact · idempotent · checkpoint بالبصمات · snapshot شامل + delta.
- `/sdcard/NEXUS_LLM_WIKI/systems/15_DOMAIN_COMPLETION_GATES.md` — سلسلة الحالات: `route_done` → `source_done` → `subdomain_extraction_done` → `domain_terms_complete` → `domain_done`.
- `/sdcard/NEXUS_LLM_WIKI/systems/17_FOLDER_INDEX_CONTRACT.md` — snapshot شامل + المسار العكسي.
- `/sdcard/wikillm/11_USER_VISION_AND_RULES.md:17-28` — رفض Claims/الفلترة verbatim.
- `/sdcard/wikillm/21_wikis_analysis.md:86-91` — ما نتجنبه (عينة متنكرة كـsnapshot، ادعاء فحوص).
- `/sdcard/wikillm/10_FULL_CONTEXT.md:26` — درس GPT-6 البيروقراطي (3 ملفات من 2,541).

**ما تتجنبه:** **نظام Claims فلترة** (المالك حظره حرفيا: «مش تراجع وتقول كلامهم صح او غلط») · عينة متنكرة كـsnapshot · ملفات مجهرية (درس CLM_*.md).

**ما لا تكتبه:** رقم بدون أمر قياس.

---

## 1. المبدأ الدستوري: Zero Data Loss

**الحقيقة النفسية:** الخوف من فقدان المعرفة هو الجذر (40 شكوى خوف حذف).

**المبدأ:** كل مصدر يدخل الويكي **بكل محتواه بلا استثناء**، بلا حكم صح/خطأ على كلام الخبراء.

**رفض نظام Claims/الفلترة — نص حرفي** (`20_user_intent_facts.md:S1`):
> «مش تراجع وتقول كلامهم صح او غلط لانه بالحالة دى هتختار حاجات معينة فقط والباقي هتتجاهله تماما فانت كل ملف هتدخله على الويكى لازم يدخل بكل محتواه بلا استثناء ومش تقول واحد صح و واحد خطأ» — AGY رسالة 11.

**الاستثناء الوحيد** (`20_user_intent_facts.md:S1:GPT6 #40`):
> «وممكن نلاقي حاجة تانية انه راى غبي جدا واحد يكون بيهبد او مش له علاقة بالمجال اصلا فاهمنى؟ فده نحذفه تماما»

**التطبيق العملي:**
1. كل رأي يُحفظ **بمصفوفة سياق** (مهارة `opinion-context-evaluation`): `context/target/mechanism/conditions/counterconditions/transferability`.
2. قاعدة التناقض: اختلف الجمهور/المرحلة/السعر/القناة ⇒ **توصيتان مشروطتان** لا تناقض منطقي ولا دمج قسري.
3. الفلترة الوحيدة: استبعاد الهراء الصريح خارج المجال **مع توثيق السبب** (وسم `status: rejected · reason: هبد` لا حذف صامت).

**الدرس التاريخي:** GPT-6 دفع ثمن الفلترة: 3 ملفات معالجة من 2,541 بسبب البيروقراطية + Claims. **NEXUS_LLM_WIKI كان جزءا من البيروقراطية التي قتلت الإنتاج** (`10_FULL_CONTEXT.md:26`).

---

## 2. الهوية: SHA-256 byte-exact

**الحقيقة النفسية:** المصدر المُعاد رفعه (نفس الفيديو، تاريخ مختلف) يُحسب مرتين ⇒ أرقام تتضخم.

**المبدأ:** هوية المصدر على **البايتات الأصلية قبل أي تطبيع** — لا تشابه عنوان ولا نص، بل `sha256` كامل.

**أمر القياس:**
```bash
# بصمة المصدر الأصلي (قبل أي تعديل)
sha256sum "<المصدر>"
# ⇒ e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

**قاعدة الهوية:**
1. `S_` Source = نسخة byte-exact في `done/<domain>/<subdomain>/`.
2. التكرار = **بصمة byte-exact متطابقة** بلا حذف — canonical واحد + سجل `duplicates`.
3. `idempotent` — إعادة التشغيل لا تنشئ سجلا ثانيا لنفس البصمة.
4. الدفعة ثابتة + checkpoint مربوط **بالبصمات** (`source-ingestion-and-dedup`).

**مثال:**
```bash
# دفعة إدخال — idempotent
bash tools/ingest.sh <ملف_المصدر> domains/outreach/
# ⇒ إذا كانت البصمة موجودة مسبقا: "skip (duplicate: <b64>)"
# ⇒ إذا كانت جديدة: نسخة + بصمة + سجل
```

---

## 3. snapshot شامل + delta

**الحقيقة النفسية:** الوصول الجديد = إعادة فتح صامتة ⇒ إسقاط إغلاق قديم على مخزون أحدث (`NEXUS_LLM_WIKI` دروس التشغيل).

**المبدأ:**
1. **snapshot شامل:** كل مرشح له `disposition` وسبب ودليل — **حتى خارج المجال**. `unresolved` سجل ظاهر يمنع الإغلاق. الإغلاق بمساواة **المجموعات** لا مقارنة عددين.
2. **delta:** الوصول الجديد يُعالج كـ delta + تعليم التغطية `stale` — لا إعادة فتح صامتة ولا إسقاط إغلاق قديم على مخزون أحدث.

**جدول حالات المصادر:**

| الحالة | المعنى | الدليل المطلوب |
|---|---|---|
| `pending` | لم يُفحص | — |
| `reading` | جاري القراءة | `bytes_read` متزايد |
| `read_done` | اكتملت IO | `bytes_read == bytes_expected` |
| `terms_extraced` | استخرجت مصطلحات | مصفوفة مصطلحات + locators |
| `domain_terms_complete` | كل المصادر في المجال + فروعه | مقارنة المجموعات |
| `domain_done` | مفاهيم معمّقة + بوابات | تقارير QA |
| `stale` | مصدر جديد وصل | `delta` محسوب |
| `unresolved` | عالق (فساد/تعذر) | `disposition` مسجّل |
| `rejected` | هبد خارج المجال | `reason` مسجّل |

**سلسلة الحالات المستقلة** (`systems/15`): `route_done` → `source_done` → `subdomain_extraction_done` → `domain_terms_complete` → `domain_done` — كل حالة لها دليلها اللازم وما لا تبيحه.

---

## 4. المسار الكامل للمصدر

```
raw/ (محمي) ──[b64]──> intake/ (جرد بالبصمة) ──[cp]──> done/<domain>/<subdomain>/<S_...>.md
                                                      │
                                                      ├──> TERMS (مصطلحات)
                                                      └──> PROVENANCE (ثلاثي الربط)
```

**الخطوة 1 — الجرد (intake):**
```bash
# جرد كل الملفات الخام — بصمة + حجم + طابع
find raw/ -type f | while read f; do
  b=$(sha256sum "$f" | cut -d' ' -f1)
  s=$(stat -c%s "$f")
  t=$(stat -c%Y "$f")
  echo "$b|$s|$t|$f"
done > intake/manifest.jsonl
```

**الخطوة 2 — النقل (done):**
```bash
# نسخة byte-exact + تسجيل
cp raw/<file> done/<domain>/<subdomain>/<S_$(basename $f).md>
```

**الخطوة 3 — استخراج المصطلحات (TERMS):**
```bash
# لكل مصدر: استخراج الجمل الحاملة معنى → T_ بمعرّف مصدر + موضع
python3 tools/extract_terms.py --source_id "<SRC_ID>" --locator "line:120|timestamp:14:30" <done/...>
```

**الخطوة 4 — الترقية (T_ → C_):**
عند `mentions ≥ 2`:
```bash
# الترقية لا حذف الأصل
type: concept
name: <اسم_المفهوم>
aka: [<ترادفات>]
# الأقسام الستة...
```

---

## 5. ما نتجنبه — 3 أخطاء موثّقة

### E1 — نظام Claims فلترة (محظور صراحة)
- **المسار:** `NEXUS_LLM_WIKI/systems/15` (بوابة C: مراجعة Claims).
- **لماذا ممنوع:** المالك يرفض الفلترة حرفيا (S1 أعلاه). نظام GPT-6 (Claims + SCHEMA) قتل الإنتاج.
- **البديل:** مصفوفة السياق الستة + `status: disputed` + `confidence: disputed` — الخلاف يُحفظ مشروطا.

### E2 — عينة متنكرة كـsnapshot
- **المسار:** `NEXUS_LLM_WIKI/systems/15` (بوابة T).
- **الوصف:** دفعة مكتملة لا تجعل قسما أو مجالا كاملا؛ عينة اعتراضات + باقي الأقسام غير مقروءة = `batch_complete` فقط.
- **الحكم:** T وMaster **مرفوضان**.
- **الحماية:** `domain_terms_complete` = استخراج ومراجعة مصطلحات **كل** مصادر snapshot الشامل (لا عينة، لا batch، لا top-N).

### E3 — ملفات مجهرية (درس CLM_*.md)
- **المسار:** `NEXUS_LLM_WIKI` (انفجار claims/CLM_*.md كاد يمتلئ القرص بـ211MB).
- **الحماية:** ملف جامع لكل نطاق (PLAYBOOK + TERMS + SOURCES_CATALOG) — `SYS_04`/`SYS_09`.

### E4 — ادعاء فحوص لم تُنفّذ
- **المسار:** `NEXUS_LLM_WIKI/systems/15` (بوابة QA).
- **الحكم:** أي ادعاء ببوابات T/C/K/M/QA يحتاج تقريرا منفصلا يذكر **أمره ودليله**.

---

## 6. البوابة — أمرا shell حرفية

**بوابة I1 (SHA-256 مذكور + بصمة):**
```bash
grep -c "SHA-256\|بصمة\|sha256" systems/SYS_05_الاستيعاب.md   # ≥ 3   ✅
```

**بوابة I2 (نظام Claims إلزامي = 0):**
```bash
grep -c "نظام Claims إلزامي\|claim_id" systems/SYS_05_الاستيعاب.md   # = 0   ✅
# ملاحظة: ذكر "نظام Claims" في سياق الحظر مسموح، لكن كلمة claim_id يجب أن تكون صفر.
```

**بوابة I3 (snapshot شامل + delta مذكوران):**
```bash
grep -c "snapshot شامل\|delta" systems/SYS_05_الاستيعاب.md   # ≥ 2
```

**بوابة I4 (رفض Claims verbatim موثق):**
```bash
grep -c "مش تراجع وتقول كلامهم صح او غلط\|بكل محتواه بلا استثناء" systems/SYS_05_الاستيعاب.md   # ≥ 1
```

**بوابة I5 (فاحص بصمات قبل/بعد دفعة):**
```bash
# يفحص: صفر ملف في done/ بلا بصمة مسجلة في manifest.jsonl
python3 - <<'EOF'
import json, hashlib, pathlib
seen = {}
for line in open('intake/manifest.jsonl'):
    b, f = line.strip().split('|', 1)[0], line.strip().split('|', -1)[-1]
    seen[b] = f
missing = 0
for p in pathlib.Path('done/').rglob('*'):
    if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() not in seen:
        missing += 1
print('missing_bsm:', missing)   # = 0
EOF
```

**التحقق العملي (شُغِّل الآن):**
```bash
cd /sdcard/wikillm/kimi_version/wiki_ver2 && grep -c "SHA-256\|بصمة" systems/SYS_05_الاستيعاب.md
# ≥ 3  ✅
cd /sdcard/wikillm/kimi_version/wiki_ver2 && grep -c "نظام Claims إلزامي\|claim_id" systems/SYS_05_الاستيعاب.md
# = 0  ✅
```

---

## 7. الخلاصة — 4 قواعد

1. كل مصدر يدخل **بكل محتواه** بلا فلترة — بلا حكم صح/خطأ.
2. هوية byte-exact: `sha256` على البايتات الأصلية قبل التطبيع.
3. snapshot شامل لكل مرشح + delta للوارد الجديد.
4. checkpoint مربوط **بالبصمات** — idempotent.

**مصدري:** مهارة `source-ingestion-and-dedup` (`/sdcard/NEXUS_WIKI_SKILLS/`) · بوابة 15 (`/sdcard/NEXUS_LLM_WIKI/systems/15_DOMAIN_COMPLETION_GATES.md`) · رفض الفلترة verbatim (`/sdcard/wikillm/20_user_intent_facts.md:S1`) · درس GPT-6 (`/sdcard/wikillm/10_FULL_CONTEXT.md:26`).

**معيار القبول (أمر shell حرفي):**
```bash
grep -c "SHA-256\|بصمة" systems/SYS_05_الاستيعاب.md              # ≥ 3   ✅
grep -c "نظام Claims إلزامي\|claim_id" systems/SYS_05_الاستيعاب.md   # = 0   ✅
```
