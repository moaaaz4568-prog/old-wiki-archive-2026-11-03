# مواصفة تحويل Nexus LLM Wiki إلى منتج مفتوح المصدر على GitHub
**تاريخ الوثيقة:** 2026-10-21  
**المعرف:** `SPEC_GITHUB_PRODUCTIZATION_20261021`  
**الحالة:** معتمدة للتنفيذ الهندسي (Engineering Blueprint)  

---

## 1. الرؤية والهدف (The Vision)

تحويل نظام تشغيل المعرفة للذكاء الاصطناعي (**Nexus Cognitive Operating System**) من مجرد مجلدات محلية على الهاتف إلى **مشروع مفتوح المصدر عالمي على GitHub** باسم:
```text
Nexus-OS: The Open-Source LLM Knowledge & Cognitive Operating System
```
يمكّن هذا النظام أي مطور، أو شركة، أو نموذج لغوي من:
1. تحويل آلاف الملفات والوثائق غير المنظمة إلى بنية معرفية هرمية خالية من الهلوسة.
2. استخدام بروتوكولات استرجاع فائقة الدقة (Verbatim Evidence Anchors).
3. بناء خطط أعمال، واستراتيجيات مبيعات، وأنظمة تسويق متكاملة عبر نماذج الذكاء الاصطناعي.

---

## 2. معمارية مستودع GitHub المقترح (Repository Architecture)

يُقسم المستودع إلى مكونين رئيسيين: **المحرك والأدوات (Core Engine & Tools)** و **قوالب المعرفة (Knowledge Starter Packs)**:

```text
nexus-os/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                     # فحص الكود والاختبارات الآلية
│   │   └── smoke-test.yml             # تشغيل wiki_system_smoke_test تلقائياً
│   └── ISSUE_TEMPLATE/
├── core/                              # محرك التشغيل البرمجي (Python Standard Library)
│   ├── manifest_builder.py            # فهرسة وتتبع بصمات الملفات الخام
│   ├── batch_extractor.py             # استخراج المصطلحات والادعاءات بدفعات
│   ├── semantic_registry.py           # منع التكرار وإثراء المفاهيم القائمة
│   └── retriever.py                   # محرك البحث والاسترجاع الدقيق للنماذج
├── systems/                           # عقود وتشريعات التشغيل القياسية
│   ├── 20_WIKI_OPERATING_SYSTEM.md
│   ├── 21_SOURCE_TO_KNOWLEDGE_PIPELINE.md
│   ├── 22_WRITING_AND_EVIDENCE_SYSTEM.md
│   ├── 23_RETRIEVAL_QA_AND_HONEST_STATUS.md
│   ├── 24_AGENT_HANDOFF_AND_RECOVERY.md
│   └── 25_CHANGE_CONTROL_AND_UPDATE_PROTOCOL.md
├── model_protocols/                   # بروتوكولات سلوك النماذج الذكية
│   ├── BEHAVIOR_CONTRACT.md
│   ├── REASONING_PROTOCOL.md
│   └── VERIFICATION_GATES.md
├── templates/                         # قوالب Schema الجاهزة
│   ├── claim.template.md
│   ├── concept.template.md
│   └── master.template.md
├── starter_packs/                     # حقائب معرفية جاهزة (Business, Sales, Dev)
│   └── business_growth/
├── tests/                             # جناح الاختبارات الآلية
│   ├── test_smoke.py
│   ├── test_schemas.py
│   └── test_retrieval.py
├── docs/                              # التوثيق الشامل ثنائي اللغة (AR / EN)
│   ├── ARCHITECTURE.md
│   ├── QUICKSTART.md
│   └── AGENTS_GUIDE.md
├── README.md                          # واجهة المستودع مع شارات الاختبار
├── LICENSE                            # MIT License
└── pyproject.toml                     # إعدادات الحزمة البرمجية
```

---

## 3. العزل الأمني وحماية الخصوصية (Data Hygiene & Isolation)

قبل رفع أي ملف إلى GitHub:
1. **عزل المحتوى الخاص والتفريغات:** الملفات الخام الخاصة بالمستخدم في `raw/` **لن تُرفع إلى المستودع العام**؛ يُرفع فقط كود المحرك والقوالب وحقائب معرفية عامة (Public Domain / Curated).
2. **استبعاد المسارات المحلية المطلقة:** استبدال المسارات الخاصة ببيئة الجهاز (`/sdcard/...`) بمسارات نسبية تعتمد على جذر المشروع (`./`).
3. **تجريد مفاتيح الوصول والتوكنز:** التحقق الآلي من عدم وجود أي Bearer Tokens أو بيانات اعتماد من سجلات الجلسات.

---

## 4. الميزات التنافسية لـ Nexus-OS مقارنة بأنظمة الويكي التقليدية

| الميزة | أنظمة الويكي التقليدية (Obsidian/Dendron) | Nexus-OS |
|---|---|---|
| **الموجه الأساسي** | القراءة البشرية فقط | **النماذج اللغوية (LLM-Native)** مع قابلية القراءة للبشر |
| **دقة الأدلة** | روابط تشعبية عامة | **اقتباس حرفي برقم السطر والـ Hash** لكل قاعدة |
| **فض التناقضات** | تضارب أو إلغاء | **مصفوفة سياق السوق (Contextual Bifurcation)** |
| **استيعاب البيانات** | يدوي ومحدود | **محرك استخراج دفعي آلي (High-Throughput Batch)** |
| **التفاعل التنفيذي** | بحث نصي بسيط | **أدوات تخطيط واسترجاع تكتيكي للأقسام (`planner` & `retriever`)** |

---

## 5. خطة الإطلاق ومراحل التنفيذ (Rollout Phases)

1. **المرحلة 1: التدقيق والاختبار الداخلي (الحالية):**
   - تثبيت اختبارات السلامة الآلية وتوثيق الأنظمة ومراجعتها محلياً.
2. **المرحلة 2: بناء النواة البرمجية (The Engine):**
   - نقل أدوات الاستخراج والفهرسة إلى وحدة بايثون قياسية موحدة في `core/`.
3. **المرحلة 3: تجربة الاستنساخ المستقل (Clean Clone Test):**
   - اختبار تشغيل المستودع في بيئة نظيفة معزولة للتأكد من أن أي مستخدم جديد يستطيع تشغيل النظام بأمر واحد:
     ```bash
     git clone https://github.com/moazmaster4/nexus-os.git
     cd nexus-os
     python3 core/smoke_test.py
     ```
4. **المرحلة 4: النشر والإطلاق الرسمي على GitHub:**
   - تجهيز صفحة المستودع، التوثيق باللغتين العربية والإنجليزية، وتفعيل GitHub Actions.
