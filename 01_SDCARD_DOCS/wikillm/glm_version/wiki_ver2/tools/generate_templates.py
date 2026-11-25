#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_templates.py — مولّد قوالب الموجة 4 لمجلد domains/

الوظيفة (وفق BUILD_PROTOCOL.md الموجة 4):
  1. ينسخ PLAYBOOK_TEMPLATE.md النموذجي من sales/01_discovery_qualification/
     إلى بقية الأقسام الفرعية العشرة، مع استبدال اسم المجال والقسم الفرعي
     في YAML والعنوان ومسار المجلد المذكور في المتن.
  2. يولّد TERMS_TEMPLATE.md (الخطوات السبع وفق SYS_06)
     وCONTINGENCY_MATRIX_TEMPLATE.md (سجل الرأي ومصفوفة القرار وفق SYS_08)
     لكل قسم فرعي من الأقسام الأحد عشر.
  3. يولّد INDEX.md لكل مجلد تحت domains/ (الجذر + 5 مجالات + 11 قسماً فرعياً)
     وفق عقد SYS_10: retrieval_questions + limitations + الحالة + جدول مداخل
     باثني عشر حقلاً.

قيود التنفيذ:
  - Python 3 بمكتبة قياسية فقط (os · sys) — لا تبعيات خارجية.
  - لا يحذف شيئاً أبداً؛ يكتب فوق ملفاته فقط أو ينشئ جديدة.
  - كل ملف يولّده يحمل حالة صريحة (pending) — لا ادّعاء اكتمال قبل التشريح.
  - الاستخدام: python3 tools/generate_templates.py
"""

import os
import sys

# ---------------------------------------------------------------------------
# الثوابت الحاكمة
# ---------------------------------------------------------------------------
WIKI_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAINS_ROOT = os.path.join(WIKI_ROOT, "domains")
MODEL_PLAYBOOK = os.path.join(DOMAINS_ROOT, "sales",
                              "01_discovery_qualification", "PLAYBOOK_TEMPLATE.md")

DATE = "2026-10-28"
SNAPSHOT = "W4-2026-10-28"
VERSION = "W4.0"

# بنية المجالات: (اسم المجلد، العنوان العربي، وصف الوظيفة، الأقسام الفرعية)
# كل قسم فرعي: (اسم المجلد، العنوان العربي، وصف الوظيفة)
DOMAINS = [
    ("sales", "المبيعات", "حركة الإيراد من العميل المحتمل إلى التوقيع", [
        ("01_discovery_qualification", "الاكتشاف والتأهيل",
         "إيجاد العملاء الذين يحتاجون الخدمة فعلاً وتأهيلهم قبل العرض"),
        ("02_closing", "الإغلاق",
         "حركات إنهاء الصفقة: الالتزام، التوقيع، الشروط"),
        ("03_objections", "الاعتراضات",
         "معالجة الاعتراضات بوصفها بيانات لا معارك"),
    ]),
    ("outreach", "الأوتريتش", "الوصول البارد إلى الغرباء وتحويلهم إلى محادثات", [
        ("01_cold_email", "البريد البارد",
         "قنوات المراسلة الباردة: الصياغة، التتابع، التسليم"),
        ("02_linkedin_dm", "رسائل لينكدإن",
         "المراسلة المباشرة على لينكدإن: الزاوية، السلسلة، حدود المضايقة"),
    ]),
    ("pricing_offers", "التسعير والعروض", "هندسة العرض وقرار السعر", [
        ("01_offer_architecture", "هندسة العرض",
         "بنية العرض: القيمة، الضمانات، المكافآت، التموضع"),
        ("02_pricing_psychology", "سيكولوجية التسعير",
         "قرار السعر كقرار إدراكي: المراسي، الحزم، الأرقام"),
    ]),
    ("content_strategy", "استراتيجية المحتوى", "ما يُنشر ولماذا وإلى من", [
        ("01_content_pillars", "ركائز المحتوى",
         "أعمدة المواضيع وربطها بالجمهور والهدف التجاري"),
        ("02_distribution", "التوزيع",
         "قنوات النشر وإعادة الاستخدام وقياس الوصول"),
    ]),
    ("business_architecture", "هندسة البيزنس", "بنية النموذج التجاري وقابليته للتوسع", [
        ("01_business_models", "نماذج البيزنس",
         "أنواع النماذج التجارية ومنطق الإيراد في كل منها"),
        ("02_scalable_systems", "الأنظمة القابلة للتوسع",
         "العمليات والتفويض والأتمتة التي تنمو بلا انهيار"),
    ]),
]

# ---------------------------------------------------------------------------
# قوالب المحتوى
# ---------------------------------------------------------------------------

def playbook_for(domain, sub):
    """ينسخ القالب النموذجي ويستبدل المجال والقسم الفرعي في مواضعه الثلاثة:
    YAML (domain/subdomain) · العنوان · مسار المجلد في المتن."""
    with open(MODEL_PLAYBOOK, "r", encoding="utf-8") as fh:
        text = fh.read()
    text = text.replace("domain: sales", "domain: %s" % domain)
    text = text.replace("subdomain: discovery_qualification", "subdomain: %s" % sub)
    text = text.replace(
        "# PLAYBOOK_TEMPLATE — sales / discovery_qualification",
        "# PLAYBOOK_TEMPLATE — %s / %s" % (domain, sub))
    text = text.replace(
        "domains/sales/01_discovery_qualification/",
        "domains/%s/%s/" % (domain, sub))
    return text


def terms_template(domain, sub):
    """قالب المصطلحات وفق SYS_06: الخطوات السبع + بوابتا D05/D06 + حقل aka."""
    return "---\ntype: terms_template\nversion: %s\ndomain: %s\nsubdomain: %s\nsections: 7\nstatus: pending\ndate: %s\n---\n\n" \
        "# TERMS_TEMPLATE — %s / %s\n\n" \
        "> قالب فارغ لتعميق مصطلحات `domains/%s/%s/` وفق SYS_06\n" \
        "> (`/sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_06_المصطلحات_والتعميق.md`).\n" \
        "> المصطلح لا يُعدّ «مستوعَباً» إلا بعد إتمام الخطوات السبع،\n" \
        "> وبوابة D05 (حدود الفناء ≥40 كلمة) حاجبة، وبوابة D06 (الآلية ≥40 كلمة) عالية الأولوية.\n" \
        "> المصدر الحاكم للخطوات: `/root/r/MASTER_SYNTHESIS_AND_DEEPENING_BLUEPRINT_2026.md`.\n\n" \
        "---\n\n" \
        "## المصطلح\n\n" \
        "- الاسم (بالإنجليزية بين قوسين): فارغ — يُملأ عند التشريح.\n" \
        "- `aka:` (المرادفات، مفصولة بـ «·»): فارغ — المرادف حقل لا ملف وفق SYS_02.\n" \
        "- الحالة: `deepening` — لا يُحسب في اكتمال النطاق قبل إتمام الخطوات (R06 في SYS_06).\n\n" \
        "## الخطوات السبع (وفق R01 في SYS_06)\n\n" \
        "### 1. التعريف والميكانيكية\nما هو وكيف يعمل في جملتين: فارغ.\n\n" \
        "### 2. المحاكاة الميدانية\nثلاثة سيناريوهات تطبيقية واقعية مختلفة السياقات (R04 — لا نسخ بمسميات مختلفة):\n- السيناريو (1): فارغ.\n- السيناريو (2): فارغ.\n- السيناريو (3): فارغ.\n\n" \
        "### 3. البدائل والتنوعات\nما يحقق نفس الهدف بطرق أخرى ومتى يتفوق البديل: فارغ.\n\n" \
        "### 4. تناقص العوائد\nمتى يتوقف المزيد من هذا المفهوم عن إضافة قيمة: فارغ.\n\n" \
        "### 5. الربط والتناقض\nما يتصل به من مفاهيم وما يتعارض معه صراحة: فارغ.\n\n" \
        "### 6. التفكير النقدي والتحيزات\nالتحيز الذهني الذي قد يجعل المفهوم يبدو أفضل مما هو: فارغ.\n\n" \
        "### 7. التطبيق خطوة بخطوة\nثلاثة أمثلة تطبيق مرقمة (R05 — يستطيع قارئ بلا خلفية اتباعها):\n1. فارغ.\n2. فارغ.\n3. فارغ.\n\n" \
        "## بوابة D05 — حدّ الفناء (حاجبة)\nفقرة ≥40 كلمة تذكر شرط السياق الذي يفشل عنده المفهوم: فارغ.\n\n" \
        "## بوابة D06 — الآلية (عالية الأولوية)\nفقرة ≥40 كلمة تشرح كيف يعمل المفهوم ميكانيكياً: فارغ.\n\n" \
        "---\n\n" \
        "## قاعدة الحالة\nهذا القالب فارغ — يُملأ عند تشريح المصادر وفق SYS_07\n" \
        "(`/sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_07_تشريح_الماستر.md`).\n" \
        "حتى الاكتمال: حالة الملف `pending` ولا يُبنى عليه توصية تنفيذية.\n" \
        % (VERSION, domain, sub, DATE, domain, sub, domain, sub)


def contingency_template(domain, sub):
    """قالب مصفوفة الرأي وفق SYS_08: سجل الرأي + التقييم الخماسي + مصفوفة القرار."""
    return "---\ntype: contingency_matrix_template\nversion: %s\ndomain: %s\nsubdomain: %s\nstatus: pending\ndate: %s\n---\n\n" \
        "# CONTINGENCY_MATRIX_TEMPLATE — %s / %s\n\n" \
        "> قالب فارغ لتوثيق الآراء المتعارضة في `domains/%s/%s/` وفق SYS_08\n" \
        "> (`/sdcard/wikillm/glm_version/wiki_ver2/systems/SYS_08_تعددية_الآراء.md`).\n" \
        "> لا رأي بلا سجل كامل (R01)، والشروط إلزامية (R04): رأيان متعارضان بسياقين\n" \
        "> مختلفين = توصيتان مشروطتان، لا حذف ولا تسوية.\n" \
        "> المصدر الحاكم: `/sdcard/NEXUS_WIKI_SKILLS/opinion-context-evaluation/SKILL.md`.\n\n" \
        "---\n\n" \
        "## سجل الرأي (الحقول وفق SYS_08)\n\n" \
        "| الحقل | القيمة |\n|---|---|\n" \
        "| opinion_id | فارغ — معرف فريد |\n" \
        "| claim_refs | فارغ — مراجع الادعاء |\n" \
        "| speaker | فارغ — قائل الرأي |\n" \
        "| context | فارغ — سياقه |\n" \
        "| target | فارغ — موضوعه |\n" \
        "| mechanism | فارغ — آليته المزعومة |\n" \
        "| conditions | فارغ — شروط صلاحيته (إلزامية وفق R04) |\n" \
        "| counterconditions | فارغ — شروط فشله (إلزامية وفق R04) |\n" \
        "| evidence_type | فارغ — نوع الدليل |\n" \
        "| reported_result | فارغ — النتيجة المبلَّغة |\n" \
        "| confidence | فارغ — ثقة القائل |\n" \
        "| relevance_score | فارغ — درجة الصلة |\n" \
        "| evidence_quality | فارغ — جودة الدليل |\n" \
        "| transferability | فارغ — قابلية النقل |\n" \
        "| decision_status | فارغ — حالة القرار |\n\n" \
        "## التقييم الخماسي (R03 — درجات 0-2 لكل بُعد، الكلي من 10)\n\n" \
        "| البُعد | الدرجة (0-2) | سبب الدرجة |\n|---|---|---|\n" \
        "| الصلة | فارغ | فارغ |\n" \
        "| جودة الدليل | فارغ | فارغ |\n" \
        "| قابلية النقل | فارغ | فارغ |\n" \
        "| اتساق الآلية | فارغ | فارغ |\n" \
        "| وضوح الشروط | فارغ | فارغ |\n\n" \
        "## مصفوفة القرار (R02 — ست حالات)\n\n" \
        "الحالة المختارة للرأي أعلاه (واحدة فقط، مع سبب في سطر):\n" \
        "- [ ] 1 — مرتبط ومدعوم: يُبنى عليه ويُربط بالادعاءات.\n" \
        "- [ ] 2 — مرتبط وتجريبي: يُقيَّد بعبارة «تجريبي، دليل محدود».\n" \
        "- [ ] 3 — مرتبط بلا دليل: يُعلَّق `suspended` بانتظار دليل.\n" \
        "- [ ] 4 — متعارض مع رأي مدعوم: توصيتان مشروطتان بشرطي كل منهما.\n" \
        "- [ ] 5 — غير مرتبط بالنطاق: يُنقل إلى نطاقه.\n" \
        "- [ ] 6 — هبد (هراء أو تسويق): يُدفن `buried` مع سبب الدفن في سطر.\n\n" \
        "## قاعدة التناقض\nالرأي المعارض لهذا الرأي (إن وُجد): فارغ — يُوثَّق بمدخل سجل مستقل كامل،\n" \
        "والحل الوحيد المسموح للتعارض الحقيقي هو توصيتان مشروطتان بشروط صريحة.\n\n" \
        "---\n\n" \
        "## قاعدة الحالة\nهذا القالب فارغ — يُملأ عند تشريح المصادر وفق SYS_07. حتى الاكتمال:\n" \
        "حالة الملف `pending` ولا يُبنى عليه توصية تنفيذية.\n" \
        % (VERSION, domain, sub, DATE, domain, sub, domain, sub)

# ---------------------------------------------------------------------------
# الفهارس (وفق SYS_10: retrieval_questions + limitations + حالة صريحة
# + مداخل بـ12 حقلاً)
# ---------------------------------------------------------------------------

FIELDS = ("id, kind, path, title, function, domain, subdomain, "
          "scope, status, coverage_status, snapshot_id, updated")

def entry_row(domain, sub, kind, fname, title, function):
    """صف مدخل فهرس بالحقول الاثني عشر وفق R02 في SYS_10."""
    return ("| %s_%s_%s | %s | `domains/%s/%s/%s` | %s | %s | %s | %s | "
            "global | pending | uncovered | — | %s |\n"
            % (domain, sub, kind, kind, domain, sub, fname,
               title, function, domain, sub, DATE))

def index_for_subdomain(domain, dtitle, sub, stitle, sdesc):
    """فهرس القسم الفرعي: مدخل واحد لكل قالب من القوالب الثلاثة."""
    rows = (
        entry_row(domain, sub, "playbook_template", "PLAYBOOK_TEMPLATE.md",
                  "قالب تشريح الماستر (18 قسماً)",
                  "استقبال محتوى التشريح وفق SYS_07") +
        entry_row(domain, sub, "terms_template", "TERMS_TEMPLATE.md",
                  "قالب تعميق المصطلحات (الخطوات السبع)",
                  "استقبال تعميق المصطلح وفق SYS_06") +
        entry_row(domain, sub, "contingency_matrix_template",
                  "CONTINGENCY_MATRIX_TEMPLATE.md",
                  "قالب سجل الرأي ومصفوفة القرار",
                  "استقبال تعددية الآراء وفق SYS_08"))
    return "---\ntype: index\nversion: %s\ndomain: %s\nsubdomain: %s\nstatus: pending\nupdated: %s\n---\n\n" \
        "# INDEX — %s / %s (%s)\n\n" \
        "%s\n" \
        "## retrieval_questions\n\n" \
        "- ما القوالب الجاهزة لاستقبال تشريح مصادر نطاق «%s — %s»؟ (هذا الفهرس)\n" \
        "- ما حالة كل قالب؟ (القسم الثالث أدناه: كلها `pending`)\n" \
        "- أين تُوثَّق الآراء المتعارضة لهذا النطاق؟ (CONTINGENCY_MATRIX_TEMPLATE)\n\n" \
        "## limitations\n\n" \
        "- هذا الفهرس لا يحوي معرفة — فقط قوالب فارغة (`pending`)؛\n" \
        "  لا تُبنى عليه توصية تنفيذية.\n" \
        "- لا يجيب عن أسئلة المضمون (ما التكتيك الفعّال؟ ما الشروط؟) —\n" \
        "  تُبحث في القوالب بعد ملئها وفق SYS_07.\n" \
        "- لا يملك `active_domain` ولا أي سلطة قرار (R06 في SYS_10)؛\n" \
        "  القرار للأنظمة (SYS_01–SYS_09).\n\n" \
        "## الحالة الصريحة\n\n" \
        "- `pending` — القوالب أُنشئت ولم يُشرَّح فيها مصدر بعد.\n" \
        "- المسار العكسي (R03): Master ← Concept ← Claim ← `source_id` —\n" \
        "  يسلك بعد الملء؛ القوالب الفارغة بلا مصدر بعد.\n\n" \
        "---\n\n" \
        "## المداخل (12 حقلاً وفق R02: %s)\n\n" \
        "| id | kind | path | title | function | domain | subdomain | scope | status | coverage_status | snapshot_id | updated |\n" \
        "|---|---|---|---|---|---|---|---|---|---|---|---|\n" \
        "%s" \
        % (VERSION, domain, sub, DATE, domain, sub, stitle,
           sdesc, domain, sub, FIELDS, rows)

def index_for_domain(domain, dtitle, ddesc, subs):
    """فهرس المجال: مدخل واحد لكل قسم فرعي."""
    rows = ""
    for sub, stitle, sdesc in subs:
        rows += ("| %s_%s | subdomain_index | `domains/%s/%s/INDEX.md` | "
                 "فهرس %s | %s | %s | %s | global | pending | uncovered | — | %s |\n"
                 % (domain, sub, domain, sub, stitle, sdesc,
                    domain, sub, DATE))
    questions = "\n".join(
        "- ما الأقسام الفرعية لنطاق «%s»؟ (الجدول أدناه)" % dtitle)
    limits = "\n".join([
        "- هذا الفهرس لا يحوي معرفة — الأقسام الفرعية كلها قوالب فارغة.",
        "- لا يجيب عن أسئلة المضمون — تُبحث داخل أقسامه بعد ملئها.",
        "- لا يملك `active_domain` (R06 في SYS_10)."])
    return "---\ntype: index\nversion: %s\ndomain: %s\nstatus: pending\nupdated: %s\n---\n\n" \
        "# INDEX — %s (%s)\n\n" \
        "## retrieval_questions\n\n%s\n\n" \
        "## limitations\n\n%s\n\n" \
        "## الحالة الصريحة\n\n- `pending` — كل الأقسام الفرعية قوالب فارغة.\n\n" \
        "---\n\n" \
        "## المداخل (12 حقلاً وفق R02: %s)\n\n" \
        "| id | kind | path | title | function | domain | subdomain | scope | status | coverage_status | snapshot_id | updated |\n" \
        "|---|---|---|---|---|---|---|---|---|---|---|---|\n" \
        "%s" \
        % (VERSION, domain, DATE, dtitle, ddesc, questions, limits,
           FIELDS, rows)

def index_for_root(domains):
    """فهرس جذر domains/: مدخل واحد لكل مجال."""
    rows = ""
    for domain, dtitle, ddesc, _subs in domains:
        rows += ("| domains_%s | domain_index | `domains/%s/INDEX.md` | "
                 "فهرس %s | %s | %s | — | global | pending | uncovered | — | %s |\n"
                 % (domain, domain, dtitle, ddesc, domain, DATE))
    return "---\ntype: index\nversion: %s\nstatus: pending\nupdated: %s\n---\n\n" \
        "# INDEX — domains/ (خريطة المجالات)\n\n" \
        "المجالات الخمسة التي تُصب فيها تشريحات المصادر وفق SYS_07.\n\n" \
        "## retrieval_questions\n\n" \
        "- ما المجالات المتاحة للصب؟ (الجدول أدناه)\n" \
        "- ما حالة كل مجال؟ (القسم الثالث: كلها `pending`)\n\n" \
        "## limitations\n\n" \
        "- لا معرفة هنا بعد — قوالب فارغة في كل المجالات.\n" \
        "- لا يملك `active_domain` (R06 في SYS_10)؛ القرار للأنظمة.\n\n" \
        "## الحالة الصريحة\n\n- `pending`\n\n" \
        "---\n\n" \
        "## المداخل (12 حقلاً وفق R02: %s)\n\n" \
        "| id | kind | path | title | function | domain | subdomain | scope | status | coverage_status | snapshot_id | updated |\n" \
        "|---|---|---|---|---|---|---|---|---|---|---|---|\n" \
        "%s" \
        % (VERSION, DATE, FIELDS, rows)

# ---------------------------------------------------------------------------
# التنفيذ
# ---------------------------------------------------------------------------

def write_file(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path

def main():
    created = []
    for domain, dtitle, ddesc, subs in DOMAINS:
        for sub, _stitle, _sdesc in subs:
            subdir = os.path.join(DOMAINS_ROOT, domain, sub)
            os.makedirs(subdir, exist_ok=True)
            created.append(write_file(
                os.path.join(subdir, "PLAYBOOK_TEMPLATE.md"),
                playbook_for(domain, sub)))
            created.append(write_file(
                os.path.join(subdir, "TERMS_TEMPLATE.md"),
                terms_template(domain, sub)))
            created.append(write_file(
                os.path.join(subdir, "CONTINGENCY_MATRIX_TEMPLATE.md"),
                contingency_template(domain, sub)))
            created.append(write_file(
                os.path.join(subdir, "INDEX.md"),
                index_for_subdomain(domain, dtitle, sub, _stitle, _sdesc)))
        created.append(write_file(
            os.path.join(DOMAINS_ROOT, domain, "INDEX.md"),
            index_for_domain(domain, dtitle, ddesc, subs)))
    created.append(write_file(
        os.path.join(DOMAINS_ROOT, "INDEX.md"),
        index_for_root(DOMAINS)))
    print("أُنشئت %d ملفاً:" % len(created))
    for path in created:
        print("  " + path)

if __name__ == "__main__":
    main()
