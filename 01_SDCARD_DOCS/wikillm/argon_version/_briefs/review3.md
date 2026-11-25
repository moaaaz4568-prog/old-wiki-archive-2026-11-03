# مراجعة 3 — domains والقوالب والأدوات
افحص في /sdcard/wikillm/argon_version/wiki_ver2/:
1. domains/sales/01_discovery_qualification/PLAYBOOK_TEMPLATE.md: الأقسام §1-§18 كاملة؟ كل قسم فيه «ماذا يُكتب:»؟ القالب فارغ من المحتوى المعرفي (تعليمات فقط)؟ المثال التوضيحي مصدر موجود فعلاً (test -e)؟
2. عينة 3 قوالب مولدة: outreach/01_cold_email/PLAYBOOK_TEMPLATE.md وpricing_offers/01_pricing_tiers/TERMS_TEMPLATE.md وcontent_strategy/02_distribution/CONTINGENCY_MATRIX_TEMPLATE.md — مطابقة للنمط مع اسم المجال صحيح؟ صفر حرف صيني؟
3. كل INDEX.md في domains/: يحمل retrieval_questions وlimitations وحالة صريحة؟
4. tools/nexus_rag.py وtools/count.py وtools/audit.py: اقرأ الكود — مكتبات قياسية فقط بلا خارجية؟ صفر حرف صيني؟ شغّل: cd /sdcard/wikillm/argon_version/wiki_ver2 && python3 tools/nexus_rag.py "cold email" && python3 tools/count.py --check && python3 tools/audit.py /sdcard/wikillm/argon_version/wiki_ver2/
5. tools/generate_templates.py: idempotent (إعادة التشغيل آمنة)؟
لا تعدّل أي ملف. اكتب تقريرك في /sdcard/wikillm/argon_version/_agy_logs/review3.md: PASS لكل بند أو المشكلة بالسطر.
