# موجة 4 — domains/ + القوالب + المولّد

اقرأ أولاً: /sdcard/wikillm/BUILD_PROTOCOL.md (القسم 3 domains/ والبوابات G4-G6) ثم /root/r/V3/00_CHARTER/FORMAT_MASTER.md (الأقسام §1-§18) وNAMING.md.

اكتب في /sdcard/wikillm/argon_version/wiki_ver2/domains/ (المجلد موجود وفيه 5 مجلدات فارغة: sales, outreach, pricing_offers, content_strategy, business_architecture):

1. **اكتب يدوياً القالب النمطي الواحد** في domains/sales/01_discovery_qualification/PLAYBOOK_TEMPLATE.md — الأقسام الثمانية عشر §1-§18 (مطابق FORMAT_MASTER — العقد الحاكم 18 قسماً وليس 10):
§1 TL;DR · §2 الفلسفة · §3 التعريفات (جدول ثلاثي) · §4 الأنظمة والعمليات · §5 الأرقام ⚠️ · §6 الأخطاء الشائعة · §7 المتغيرات · §8 الجواهر (اقتباسات) · §9 التوترات · §10 نماذج جاهزة · §11 Checklist · §12 سيناريوهات · §13 الأدوات · §14 KPIs · §15 التحليل المستقل · §16 أسئلة وأجوبة · §17 روابط · §18 جدول المفاهيم.
**داخل كل قسم سطر «ماذا يُكتب:» بتعليمات دقيقة** (ماذا يُكتب، بأي شروط، بأي مصادر، متى يجوز «لا ينطبق» بالسبب). القالب فارغ من المحتوى المعرفي — تعليمات فقط. مثال توضيحي واحد موثق بـpath:line من مصدر حقيقي موجود فعلاً: /sdcard/Nexus_Brain/Nexus_Brain/brain/aaronxshepherd__21 Cold Email Hacks To Book More Sales Calls INSTANTLY__i7vdM5SZsmk.txt (تحقق بـtest -e أولاً).
**معيار القبول: `grep -c "ماذا يُكتب" PLAYBOOK_TEMPLATE.md` ≥ 18 و`grep -cE '^#{2,3} §' PLAYBOOK_TEMPLATE.md` ≥ 18.**

2. **domains/sales/01_discovery_qualification/TERMS_TEMPLATE.md** — قالب مصطلح: التعريف · المصدر (path:line) · التعميق · حدّ الفناء · aka.

3. **domains/sales/01_discovery_qualification/CONTINGENCY_MATRIX_TEMPLATE.md** — مصفوفة الآراء: الرأي / السياق / الشروط / الشروط المضادة / القابلية للنقل / الحالة (مشروط/تجريبي/فرضية/متعارض/مستبعد/هبد).

4. **domains/sales/01_discovery_qualification/INDEX.md** — بحقول retrieval_questions وlimitations وحالة صريحة (pending).

5. **domains/INDEX.md** — خريطة المجالات الخمسة ووظيفة كل منها.

6. **اكتب /sdcard/wikillm/argon_version/wiki_ver2/tools/generate_templates.py** — سكريبت Python ينسخ القالب الثلاثي (PLAYBOOK+TERMS+CONTINGENCY+INDEX) لبقية المجالات مع استبدال اسم المجال، وينشئ 3 أقسام فرعية لكل مجال:
- sales: 01_discovery_qualification (موجود — لا يُعاد توليده)، 02_closing، 03_objection_handling
- outreach: 01_cold_email، 02_linkedin_dm، 03_followup_sequences
- pricing_offers: 01_pricing_tiers، 02_offer_design، 03_guarantees
- content_strategy: 01_content_pillars، 02_distribution، 03_repurposing
- business_architecture: 01_systems_ops، 02_hiring، 03_metrics
وينشئ INDEX.md لكل مجلد (المجال + الأقسام الفرعية). **شغّله بنفسك بعد كتابته.**

## قواعد صارمة:
- عربية فصحى 100% — صفر حرف صيني. القوالب فارغة من المحتوى المعرفي (ممنوع ملؤها).
- كل مسار مصدر تذكره متحقق بـtest -e. لا TODO/TBD. ممنوع الحذف نهائياً.

## تحققك النهائي (شغّل وأعطني المخرجات الحرفية):
find /sdcard/wikillm/argon_version/wiki_ver2/domains -name INDEX.md | wc -l
find /sdcard/wikillm/argon_version/wiki_ver2/domains -name PLAYBOOK_TEMPLATE.md | wc -l
grep -c "ماذا يُكتب" /sdcard/wikillm/argon_version/wiki_ver2/domains/sales/01_discovery_qualification/PLAYBOOK_TEMPLATE.md
