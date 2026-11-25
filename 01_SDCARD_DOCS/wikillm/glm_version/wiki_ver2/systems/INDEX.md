# INDEX — مجلد systems/ (فهرس أنظمة الويكي)

## retrieval_questions
- ما الأنظمة الخمسة عشر التي تحكم الويكي، وما وظيفة كل نظام؟
- أي نظام يحكم التسمية وقيود أسماء الملفات؟ (SYS_02)
- أي نظام يحدد بنية الماستر وأقسامه الثمانية عشر؟ (SYS_07)
- أي نظام يفرض عقد الفهرس (retrieval_questions + limitations + الحالة)؟ (SYS_10)
- أي نظام يحدد أدوات التدقيق الآلي وأوامرها؟ (SYS_12)
- ما البروتوكول لإضافة نظام جديد أو توسيع قائم؟ (SYS_15)
- كيف تُوثَّق الآراء المتعارضة بلا حذف؟ (SYS_08)
- ما حدود كل نظام — ما الذي لا يجيب عنه؟ (قسم limitations أدناه)

## limitations
- هذا الفهرس لا يجيب عن تفاصيل تنفيذ نظام بعينه؛ لكل نظام ملفه الخاص المذكور في المداخل.
- لا يغطي مجلد `domains/` ولا `tools/`؛ لكل منهما فهرسه أو توثيقه الخاص.
- الفهرس يعرض حالة مشتقة من ملفاته ولا يملك `active_domain` ولا أي سلطة قرار معرفي (R06 في SYS_10).
- المسار العكسي للإسناد (Master ← Concept ← Claim ← source_id) يُتبع داخل ملفات الأنظمة نفسها، لا هنا.

## الحالة
`partial` — الأنظمة الخمسة عشر موثقة كاملة على القرص، والتحقق التشغيلي (بوابات G1-G12) يجري في الموجة 4 بتاريخ 2026-10-28. أي تعديل لاحق على ملفات المجلد يقلب هذه الحالة إلى `stale` حتى يُحدَّث الفهرس (R04 في SYS_10).

## المداخل

| id | kind | path | title | function | domain | subdomain | scope | status | coverage_status | snapshot_id | updated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SYS_01 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_01_الميثاق.md | الميثاق | الدستور الحاكم: القواعد غير القابلة للتفاوض | governance | constitution | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_02 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_02_التسمية.md | التسمية | قواعد تسمية الملفات والكيانات | governance | naming | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_03 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_03_الشجرة.md | الشجرة | شجرة المعرفة: الأنطولوجيا والبنية | governance | ontology | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_04 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_04_محرك_التفكير.md | محرك التفكير | الإدراك الرباعي: كيف يفكر الويكي | cognition | thinking_engine | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_05 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_05_الاستيعاب.md | الاستيعاب | استيعاب المصادر الخام وتحويلها | ingestion | absorption | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_06 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_06_المصطلحات_والتعميق.md | المصطلحات والتعميق | الخطوات السبع للتعميق + بوابات D05/D06 | terms | deepening | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_07 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_07_تشريح_الماستر.md | تشريح الماستر | بنية الماستر بأقسامه الثمانية عشر | masters | anatomy | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_08 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_08_تعددية_الآراء.md | تعددية الآراء | توثيق الآراء المتعارضة بلا حذف | synthesis | pluralism | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_09 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_09_التوليف_التراكمي.md | التوليف التراكمي | دمج المعرفة تراكمياً عبر الموجات | synthesis | accumulation | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_10 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_10_الفهارس.md | الفهارس | عقد INDEX لكل مجلد + الحد الأدنى للمدخل | retrieval | indexing | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_11 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_11_تنفيذ_البيزنس.md | تنفيذ البيزنس | تحويل المعرفة إلى تنفيذ تجاري | execution | business | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_12 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_12_التدقيق.md | التدقيق | التدقيق الآلي: أدوات audit/count وحدودها | verification | auditing | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_13 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_13_التفويض.md | التفويض | تفويض المهام وحدود المسؤولية | governance | delegation | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_14 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_14_الأنماط_المضادة.md | الأنماط المضادة | الأنماط التي تنكسر وحدود كل وصفة | verification | antipatterns | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
| SYS_15 | system | /sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_15_التوسع_الديناميكي.md | التوسع الديناميكي | بروتوكول إضافة أنظمة ومجالات جديدة | governance | expansion | wiki_ver2 | active | documented | W4-2026-10-28 | 2026-10-28 |
