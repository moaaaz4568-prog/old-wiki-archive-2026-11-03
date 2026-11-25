# تقرير Worker — Concepts المبيعات

## النطاق

تمت قراءة Claims البذرة `CLM_SALES_SEED_001` إلى `CLM_SALES_SEED_006`، وسجلات المصادر المرتبطة بها، والملفات الخام الستة في `raw/new`. كُتبت أربعة Concepts فقط في مجلد `concepts/`، ولم تُعدّل ملفات `raw/` أو `sources/` أو `claims/` أو `systems/` أو `masters/`.

## الملفات المكتوبة

| الملف | Claim refs | Source refs |
|---|---|---|
| [`CPT_SALES_OUTBOUND_CHANNELS.md`](../../../../sdcard/NEXUS_LLM_WIKI/concepts/CPT_SALES_OUTBOUND_CHANNELS.md) | `CLM_SALES_SEED_001`, `CLM_SALES_SEED_006` | `SRC_NEW_d4502be125612b86_78d08ff3`, `SRC_NEW_5b782973289bdb21_021e6961` |
| [`CPT_SALES_OUTREACH_ARCHITECTURE.md`](../../../../sdcard/NEXUS_LLM_WIKI/concepts/CPT_SALES_OUTREACH_ARCHITECTURE.md) | `CLM_SALES_SEED_003`, `CLM_SALES_SEED_001` | `SRC_NEW_8688040e70bb4e91_dda6bcf6`, `SRC_NEW_d4502be125612b86_78d08ff3` |
| [`CPT_SALES_OFFER_AND_DELIVERABILITY.md`](../../../../sdcard/NEXUS_LLM_WIKI/concepts/CPT_SALES_OFFER_AND_DELIVERABILITY.md) | `CLM_SALES_SEED_003`, `CLM_SALES_SEED_004`, `CLM_SALES_SEED_002` | `SRC_NEW_8688040e70bb4e91_dda6bcf6`, `SRC_NEW_a6063fcc40808ccf_fd6e5360`, `SRC_NEW_129f7a12e3e9285b_b7e305cd` |
| [`CPT_SALES_EMAIL_TO_DISCOVERY.md`](../../../../sdcard/NEXUS_LLM_WIKI/concepts/CPT_SALES_EMAIL_TO_DISCOVERY.md) | `CLM_SALES_SEED_005`, `CLM_SALES_SEED_006` | `SRC_NEW_8ee4c08d48272680_8da6b92d`, `SRC_NEW_5b782973289bdb21_021e6961` |

روابط الويكي داخل الملفات تستخدم مسارات `../claims/` و`../sources/` إلى السجلات الحقيقية، وليست Claims أو مصادر مخترعة.

## ضوابط المحتوى

- كل Concept يحتوي الأقسام: الجوهر، الآلية، الشروط، الحدود، أمثلة موسومة، التوترات، التطبيقات المشروطة، وتصنيف الادعاءات، وسجل الأدلة.
- صُنّفت النتيجة الرقمية في `CLM_SALES_SEED_002` كـ`reported_result` مع حدود الإسناد والسببية، ولم تُستخدم كضمان أو benchmark.
- صُنّف ترتيب `deliverability`/`offer` في `CLM_SALES_SEED_004`، وتفضيل العلاقة الأصيلة في `CLM_SALES_SEED_006` كـ`opinion`/تفضيل منسوب.
- وُسمت القواعد التشغيلية داخل Concepts كقواعد تطبيقية مشتقة ومشروطة، لا كـClaims مصدرية جديدة.

## الاختبارات والنتائج

1. تحقق قراءة/مقارنة الأدلة الخام: سكربت قراءة فقط فحص `evidence_start:evidence_end` و`evidence_quote` و`excerpt_sha256` للـ6 Claims؛ النتيجة `ALL_EXCERPTS_EXACT=True`، وكل الستة `exact=True`.
2. تحقق المسارات: الملفات الأربعة موجودة في `/sdcard/NEXUS_LLM_WIKI/concepts/`، وسجلات المصادر الستة وClaims الستة موجودة قبل الكتابة.
3. تحقق بنية الويكي: شُغّل `python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json` بعد الكتابة؛ النتيجة `FAIL` مع 6 أخطاء محددة في Claims البذرة نفسها: `excerpt_sha256 does not match evidence_quote`. فحص القراءة المستقل أثبت أن الشرائح والاقتباسات والهاش المقصود متطابقة؛ سبب الفرق أن Claims تحمل قيمة الهاش مسبوقة بـ`sha256:` بينما validator يقارنها دون إزالة السابقة. لم تُعدّل Claims ضمن النطاق. توجد أيضاً مشكلة السجلات القديمة الموثقة في `/root/r/.opencode/sync-issues.md`، لكن مخرجات هذا التشغيل حصرت الأخطاء الستة في Claims البذرة.

## حدود التحقق

لم أعدّل أو أصلح مشكلة `wiki_quality.py` العامة، ولم أشغّل `--index` أو أي أداة كتابة إضافية؛ بقي النطاق محصوراً في الملفات الأربعة المطلوبة وهذا التقرير.
