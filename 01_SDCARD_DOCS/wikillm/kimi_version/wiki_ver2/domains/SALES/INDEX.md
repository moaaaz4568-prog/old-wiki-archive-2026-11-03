---
type: domains_index
version: 1
---

# domains/SALES/ — خارطة مجال عملية البيع

> **الحالة: جاهزة للهيكل، محتواه pending — لا محتوى معرفي.**
> هذا الملف يوجّه الباحث/الوكيل إلى **أي محتوى يجب بناؤه** في مجال عملية البيع.

**سؤال الماستر:** ما هي مراحل/التكتيكات/أدوات عملية البيع؟

**القاعدة الحاكمة (BUILD_PROTOCOL.md القسم 3):**
- `domains/SALES/` يحتوي **فقط** على `INDEX.md` + `PLAYBOOK_TEMPLATE.md` +
  `TERMS_TEMPLATE.md` +
  `CONTINGENCY_MATRIX_TEMPLATE.md` لكل مجال فرعي.
- **ممنوع** محتوى معرفي (PLAYBOOK/MASTER/TERMS بمعرف معرفي) في مرحلة الأنظمة.
- المحتوى يُبنى لاحقاُ في `domains/SALES/<الفرع>/PLAYBOOK_*.md` بعد اكتمال مصطلحات المجال.

---

## مجال عملية البيع

| المكون | الكيان | الحالة | المحتوى المعرفي |
|---|---|---|---|
| **sales** | `domains/SALES/` | **pending** | ❌ لا — لا مصطلحات مستخلَجة |

---

## أسئلة الاسترجاع (retrieval_questions)

**سؤال واحد يُولّد ماستر واحد لكل مجال** (BUILD_PROTOCOL.md القسم 3؛ ONTOLOGY.md):

| المجال | سؤال الماستر (يُستخدم في `domains/SALES/INDEX.md`) |
|---|---|
| SALES | ما هي مراحل/التكتيكات/أدوات عملية البيع؟ |

**كيفية الاستخلاص (BUILD_PROTOCOL.md القسم 3):**
```bash
find /sdcard/Nexus_Brain/Nexus_Brain/brain -iname "*<كلمة_من_سؤال_الماستر>*" | wc -l
```
إذا كان العدد `0` ⇒ الماستر **لا ينطبق** (العقد وظيفي لا كمي).

---

## المحددات (limitations)

- **لا محتوى معرفي**: هذا المجلد هيكل وقوالب فقط (BUILD_PROTOCOL.md).
- **القوالب الثلاثة** (`PLAYBOOK_TEMPLATE.md`, `TERMS_TEMPLATE.md`, `CONTINGENCY_MATRIX_TEMPLATE.md`) **فارغة** — تعليمات فقط.
- **حقل `الحالة` في كل `INDEX.md` فرعي**: `pending` ما لم يتم استخلاص مصطلحات المجال.
- **لا `domains/SALES/<فرع>/PLAYBOOK_*.md`** حتى `domain_terms_complete`.

---

## التدقيق (audit checklist)

```bash
# 1. المحتوى المعرفي = 0
grep -rE '\[\[C_[^]]*\]\]|\[\[M_[^]]*\]\]' domains/SALES/PLAYBOOK_TEMPLATE.md domains/SALES/TERMS_TEMPLATE.md domains/SALES/CONTINGENCY_MATRIX_TEMPLATE.md | wc -l  # ⇒ 0

# 2. القوالب الثلاثة لكل مجال
for t in PLAYBOOK_TEMPLATE TERMS_TEMPLATE CONTINGENCY_MATRIX_TEMPLATE; do
  test -f domains/SALES/$t.md || echo "ناقص: domains/SALES/$t.md"
done

# 3. CJK = 0
python3 -c "import pathlib;print('CJK:', sum(1 for p in pathlib.Path('domains').rglob('*.md') for c in p.read_text(errors='ignore') if '\u4e00' <= c <= '\u9fff'))"

# 4. الأرشيف محفوظ
ls _archive/domain_content_2026-11-01/ | wc -l  # ⇒ 18
```
