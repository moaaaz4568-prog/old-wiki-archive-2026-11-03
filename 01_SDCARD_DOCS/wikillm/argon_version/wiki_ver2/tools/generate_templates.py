#!/usr/bin/env python3
"""
generate_templates.py — أداة توليد ونشر القوالب والفهارس المعمارية لمجالات الويكي.
موجة 4 — wiki_ver2 (argon_version)
يقوم هذا السكريبت بنسخ القالب الثلاثي (PLAYBOOK + TERMS + CONTINGENCY) وتوليد INDEX.md
لكل مجال ولكل قسم فرعي من الأقسام الـ15، مع استثناء القسم الأساسي sales/01_discovery_qualification.
"""

import os
import sys
from pathlib import Path

# المسارات الأساسية
TOOLS_DIR = Path(__file__).resolve().parent
WIKI_DIR = TOOLS_DIR.parent
DOMAINS_DIR = WIKI_DIR / "domains"
BASE_SUBDOMAIN = DOMAINS_DIR / "sales" / "01_discovery_qualification"

# مصفوفة البيانات المعمارية للمجالات والأقسام الفرعية
DOMAINS_DATA = {
    "sales": {
        "title_ar": "المبيعات",
        "description": "هندسة المحادثات البيعية المباشرة، قيادة قرارات الشراء، الفرز والترشيح الصارم للعملاء، وتفكيك الاعتراضات وإبرام الصفقات.",
        "retrieval_questions": [
            "كيف تُدار المحادثات البيعية المباشرة مع العملاء لتحقيق أعلى نسب إغلاق؟",
            "ما هي معايير التأهيل والفرز المسبق لحماية وقت فريق المبيعات؟",
            "كيف يتم التفكيك المنهجي لاعتراضات السعر والثقة دون الدخول في جدل؟"
        ],
        "limitations": [
            "يقتصر هذا المجال على مسار المحادثات والصفقات المباشرة وإغلاقها.",
            "لا يغطي حملات التواصل البارد الأولي لجلب المواعيد (مكانها: domains/outreach/).",
            "لا يغطي هندسة تسعير المنتجات أو تصميم العروض الاستراتيجية (مكانها: domains/pricing_offers/)."
        ],
        "subdomains": {
            "01_discovery_qualification": {
                "title_ar": "الاستكشاف والتأهيل",
                "retrieval_questions": [
                    "كيف يتم استكشاف وتأهيل العملاء المحتملين قبل وأثناء مكالمة المبيعات الأولى؟",
                    "ما هي معايير الترشيح والتأهيل (BANT / MEDDPICC / Pre-call Friction) المناسبة لمختلف أحجام الصفقات؟",
                    "متى نرفع احتكاك التأهيل المسبق لحماية وقت فريق المبيعات ومتى نخفضه للحد الأدنى لجمع البيانات؟",
                    "ما هي الأسئلة التشخيصية الاستكشافية التي تكشف الألم الجذري للعميل والقدرة الشرائية الفعلية؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على مرحلة الاستكشاف والفرز والتأهيل الأولي للصفقات فقط (Discovery & Qualification).",
                    "لا يغطي تقنيات واستراتيجيات التفاوض النهائي أو إغلاق الصفقات (مكانها الإلزامي: domains/sales/02_closing).",
                    "لا يغطي التعامل المنهجي المفصل مع اعتراضات الأسعار والشكوك المعقدة (مكانها الإلزامي: domains/sales/03_objection_handling)."
                ]
            },
            "02_closing": {
                "title_ar": "الإغلاق وإبرام الصفقات",
                "retrieval_questions": [
                    "كيف تُهيكل مرحلة الإغلاق البيعي دون الوقوع في الضغط المنفر أو التردد؟",
                    "ما هي أساليب تأطير الأسعار وتقديم خيارات الدفع لحسم القرار الاستثماري؟",
                    "كيف يتم تأكيد الالتزام المالي والتعاقدي وتثبيت الصفقة ومنع التراجع؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على مرحلة التفاوض النهائي وحسم قرارات الشراء فقط.",
                    "لا يغطي مرحلة الفرز والتأهيل الأولي (مكانها: domains/sales/01_discovery_qualification).",
                    "لا يغطي تفكيك الاعتراضات التفصيلية السابقة لمرحلة الحسم (مكانها: domains/sales/03_objection_handling)."
                ]
            },
            "03_objection_handling": {
                "title_ar": "معالجة وتفكيك الاعتراضات",
                "retrieval_questions": [
                    "كيف يتم تفكيك اعتراضات السعر، والميزانية، والتردد، والتشكيك في النتائج؟",
                    "ما الفرق الحاسم بين الاعتراض الحقيقي والعذر التهربي وكيف يُكشف كل منهما؟",
                    "ما هي سكريبتات العزل وإعادة التأطير السيكولوجي للاعتراضات البيعية؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على التفكيك المنهجي للاعتراضات وإعادة تأطيرها.",
                    "لا يغطي مرحلة الاستكشاف والتشخيص الأولية للمشكلة (مكانها: domains/sales/01_discovery_qualification).",
                    "لا يغطي الصياغة التعاقدية لخطوات الإغلاق النهائية (مكانها: domains/sales/02_closing)."
                ]
            }
        }
    },
    "outreach": {
        "title_ar": "الاستقطاب والتواصل المباشر",
        "description": "اختراق انتباه العملاء المستهدفين عبر القنوات المباشرة، وبناء الثقة الأولية، وتوليد المحادثات والفرص البيعية المجدولة.",
        "retrieval_questions": [
            "كيف تُبنى حملات المراسلة الباردة عبر البريد الإلكتروني ولينكدإن لتحقيق أعلى معدلات رد؟",
            "ما هي هندسة رسائل كسر التوقع في السطر الأول التي تضمن فتح الرسالة وقراءتها؟",
            "كيف تُدار سلاسل المتابعة التراكمية دون الوقوع في الإلحاح المزعج؟"
        ],
        "limitations": [
            "يقتصر هذا المجال على قنوات التواصل البارد المباشر وتوليد المواعيد والفرص.",
            "لا يغطي إدارة المكالمات البيعية أو إغلاق الصفقات (مكانها: domains/sales/).",
            "لا يغطي النشر العام للمحتوى غير الموجه لفرد محدد (مكانها: domains/content_strategy/)."
        ],
        "subdomains": {
            "01_cold_email": {
                "title_ar": "البريد الإلكتروني البارد",
                "retrieval_questions": [
                    "كيف تُكتب رسائل البريد البارد ذات معدلات الفتح والرد العالية والتحويل المباشر؟",
                    "ما هي بروتوكولات حماية النطاقات والسمعة وتفادي فلاتر السبام؟",
                    "كيف يُصاغ سطر الموضوع والسطر الافتتاحي القصير بنمط كسر التوقع؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على قناة البريد الإلكتروني البارد وبنيتها التقنية والنصية.",
                    "لا يغطي المراسلة عبر منصة لينكدإن (مكانها: domains/outreach/02_linkedin_dm).",
                    "لا يغطي حملات المتابعة طويلة المدى متعددة الوسائط (مكانها: domains/outreach/03_followup_sequences)."
                ]
            },
            "02_linkedin_dm": {
                "title_ar": "المراسلة المباشرة عبر لينكدإن",
                "retrieval_questions": [
                    "كيف يتم فتح محادثات مهنية طبيعية عبر لينكدإن دون الظهور بمظهر البائع المزعج؟",
                    "ما هي استراتيجيات التفاعل المسبق مع محتوى العميل قبل إرسال الرسالة الخاصة؟",
                    "كيف يتم تحويل الحوار المهني على لينكدإن بانسيابية إلى مكالمة استكشافية؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على الرسائل الخاصة المباشرة عبر لينكدإن وحسابات صناع القرار.",
                    "لا يغطي البريد البارد (مكانها: domains/outreach/01_cold_email).",
                    "لا يغطي استراتيجيات نشر المحتوى العام على الصفحة الشخصية (مكانها: domains/content_strategy/)."
                ]
            },
            "03_followup_sequences": {
                "title_ar": "سلاسل المتابعة متعددة القنوات",
                "retrieval_questions": [
                    "كيف تُهيكل سلاسل المتابعة التراكمية متدرجة القيمة لكسر صمت العملاء؟",
                    "كم عدد رسائل المتابعة المناسبة وما هي التباعدات الزمنية المثلى بينها؟",
                    "ما هي صيغة رسالة التوقف (Break-up Message) ومتى تُرسل لاستفزاز الرد الحاسم؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على المتابعات اللاحقة بعد إرسال الرسائل الافتتاحية الأولى.",
                    "لا يغطي صياغة الرسائل الأولى على أي قناة (مكانها: 01_cold_email أو 02_linkedin_dm).",
                    "لا يغطي متابعات ما بعد المكالمات البيعية المكتملة (مكانها: domains/sales/)."
                ]
            }
        }
    },
    "pricing_offers": {
        "title_ar": "التسعير وهندسة العروض",
        "description": "صياغة القيمة الاقتصادية والنفسية، وتصميم العروض الحصرية التي يصعب رفضها، وحماية الهوامش الربحية وإزالة المخاطر.",
        "retrieval_questions": [
            "كيف تُبنى باقات التسعير لتعظيم العائد من كل عميل وحماية الهوامش الربحية؟",
            "ما هي المكونات الهيكلية للعرض المغري الذي لا يمكن رفضه (Grand Slam Offer)؟",
            "كيف تُصمم الضمانات المشروطة وغير المشروطة لعكس المخاطر دون الإضرار بالبيزنس؟"
        ],
        "limitations": [
            "يقتصر هذا المجال على الجوانب الاقتصادية وهندسة القيمة والضمانات والتسعير.",
            "لا يغطي نصوص المكالمات وإجراءات التفاوض الميدانية (مكانها: domains/sales/).",
            "لا يغطي الجوانب المحاسبية وإدارة التدفق النقدي الشامل (مكانها: domains/business_architecture/)."
        ],
        "subdomains": {
            "01_pricing_tiers": {
                "title_ar": "مستويات وهياكل التسعير",
                "retrieval_questions": [
                    "كيف يتم تحديد مستويات وباقات التسعير المناسبة لطبيعة الخدمة والجمهور؟",
                    "ما هي استراتيجيات التثبيت السعري (Price Anchoring) لرفع القيمة المتصورة؟",
                    "متى يُعتمد التسعير القائم على القيمة (Value-based) مقابل التسعير الثابت؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على نماذج وهياكل وباقات التسعير الرياضية والنفسية.",
                    "لا يغطي صياغة تفاصيل العرض والمكافآت التابعة (مكانها: domains/pricing_offers/02_offer_design).",
                    "لا يغطي هندسة بنود الضمان وإزالة المخاطر (مكانها: domains/pricing_offers/03_guarantees)."
                ]
            },
            "02_offer_design": {
                "title_ar": "تصميم وهندسة العروض",
                "retrieval_questions": [
                    "كيف يُصمم عرض استثنائي متكامل يصعب رفضه ويفصلك عن أي منافسة مقارنة؟",
                    "ما هي مضاعفات القيمة ومكافآت التسريع التي تُدمج في العرض لرفع الرغبة؟",
                    "كيف يُصاغ الوعد النهائي للعرض ومؤشر النتيجة المضمونة بوضوح لا لبس فيه؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على هندسة مكونات وحزم ومكافآت العرض الإجرائي.",
                    "لا يغطي تحديد مستويات الأسعار نفسها (مكانها: domains/pricing_offers/01_pricing_tiers).",
                    "لا يغطي الشروط التفصيلية لسياسات استرداد الأموال (مكانها: domains/pricing_offers/03_guarantees)."
                ]
            },
            "03_guarantees": {
                "title_ar": "الضمانات وإزالة المخاطر",
                "retrieval_questions": [
                    "ما هي أنواع الضمانات (المشروطة، غير المشروطة، الضمان العكسي) ومخاطر كل منها؟",
                    "كيف يُصاغ ضمان قوي يزيل خوف المشتري دون تعريض المنشأة للابتزاز؟",
                    "ما هي الشروط الحاكمة التي تمنع استغلال الضمان من العملاء غير الجادين؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على صياغة وهندسة الضمانات وسياسات عكس المخاطر المالية.",
                    "لا يغطي التسعير العام للباقات (مكانها: domains/pricing_offers/01_pricing_tiers).",
                    "لا يغطي مكونات العرض والمكافآت التشغيلية (مكانها: domains/pricing_offers/02_offer_design)."
                ]
            }
        }
    },
    "content_strategy": {
        "title_ar": "استراتيجية وصناعة المحتوى",
        "description": "بناء النفوذ والمصداقية السوقية عبر صناعة الأصول المعرفية، وتوزيعها بفاعلية عبر المنصات، وهندسة الانتباه المستدام.",
        "retrieval_questions": [
            "كيف تُبنى ركائز المحتوى الاستراتيجية التي تغير قناعات الجمهور وتخلق طلباً كبيراً؟",
            "ما هي تكتيكات توزيع المحتوى لتحقيق أقصى وصول دون الاعتماد الحصري على الإعلانات؟",
            "كيف تُدار منظومة إعادة تدوير الأصول المعرفية لتوليد عشرات المنشورات من أصل واحد؟"
        ],
        "limitations": [
            "يقتصر هذا المجال على استراتيجيات إنتاج وتوزيع وإعادة تدوير المحتوى المعرفي والتسويقي.",
            "لا يغطي رسائل التواصل البارد المباشرة للأفراد (مكانها: domains/outreach/).",
            "لا يغطي مكالمات البيع والتفاوض الميدانية (مكانها: domains/sales/)."
        ],
        "subdomains": {
            "01_content_pillars": {
                "title_ar": "ركائز المحتوى والأصول الفكرية",
                "retrieval_questions": [
                    "كيف تُحدد الركائز الاستراتيجية للمحتوى التي تبني السلطة الفكرية للعلامة؟",
                    "ما هي القناعات المعارضة التي يجب تفكيكها في عقل العميل المستهدف عبر المحتوى؟",
                    "كيف يُربط كل عمود من أعمدة المحتوى بألم حقيقي أو هدف تجاري للمنشأة؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على التخطيط الاستراتيجي للأصول الفكرية وركائز المحتوى.",
                    "لا يغطي تفاصيل التوزيع الرقمي عبر المنصات (مكانها: domains/content_strategy/02_distribution).",
                    "لا يغطي أساليب التقطيع وإعادة الصياغة للتنسيقات القصيرة (مكانها: domains/content_strategy/03_repurposing)."
                ]
            },
            "02_distribution": {
                "title_ar": "تكتيكات التوزيع والوصول",
                "retrieval_questions": [
                    "كيف يتم توزيع المحتوى بكفاءة عبر المنصات المختلفة واستثمار خوارزميات الوصول؟",
                    "ما هي استراتيجيات هندسة الانتباه وتوقيتات النشر لتحقيق أعلى تفاعل ممكن؟",
                    "كيف يُبنى مسار تحويل مشاهدي المحتوى إلى مشترين أو مسجلين في القائمة البريدية؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على خطط وقنوات وآليات توزيع المحتوى المنشور.",
                    "لا يغطي صياغة الركائز الفكرية الأصلية للمحتوى (مكانها: domains/content_strategy/01_content_pillars).",
                    "لا يغطي تقنيات التقطيع وإعادة الإنتاج الفني (مكانها: domains/content_strategy/03_repurposing)."
                ]
            },
            "03_repurposing": {
                "title_ar": "إعادة تدوير وتحويل المحتوى",
                "retrieval_questions": [
                    "كيف يُحول الأصل المعرفي الطويل الواحد إلى عشرات التنسيقات المتنوعة بكفاءة عالية؟",
                    "ما هي منظومة العمل الإجرائية التي تمنع استنزاف الوقت في إعادة كتابة نفس الفكرة؟",
                    "كيف نضمن الحفاظ على الجوهر السببي للرسالة عند نقلها من الفيديو إلى التدوين أو المنشورات؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على سلاسل ومسارات إعادة التدوير وتغيير التنسيقات والقوالب.",
                    "لا يغطي إنشاء الأفكار الاستراتيجية الأولى (مكانها: domains/content_strategy/01_content_pillars).",
                    "لا يغطي إدارة جداول النشر وتكتيكات المنصات (مكانها: domains/content_strategy/02_distribution)."
                ]
            }
        }
    },
    "business_architecture": {
        "title_ar": "معمارية البيزنس والعمليات",
        "description": "بناء الهياكل والأنظمة التشغيلية القابلة للتوسع، وتوظيف الكفاءات وإدارتها، وضبط مؤشرات ومقاييس الأداء والمحاسبة.",
        "retrieval_questions": [
            "كيف تُبنى أدلة العمل القياسية (SOPs) لتحرير المؤسس من الاعتمادية التشغيلية؟",
            "ما هي بروتوكولات استقطاب وتوظيف وتأهيل أفضل الكفاءات الميدانية بأعلى سرعة؟",
            "كيف تُدار المنشأة من خلال لوحات تحكم سببية تربط بين الإجراءات والنتائج المالية؟"
        ],
        "limitations": [
            "يقتصر هذا المجال على الهيكل التنظيمي الداخلي، والتوظيف، والأنظمة، ومقاييس الأداء.",
            "لا يغطي هندسة صفقات البيع المباشرة (مكانها: domains/sales/).",
            "لا يغطي إطلاق حملات التسويق والمحتوى الخارجية (مكانها: domains/content_strategy/)."
        ],
        "subdomains": {
            "01_systems_ops": {
                "title_ar": "بناء وتوثيق العمليات والأنظمة",
                "retrieval_questions": [
                    "كيف تُوثق العمليات التشغيلية (SOPs) بطريقة تجعل تفويضها سهلاً ومضموناً بلا أخطاء؟",
                    "ما هي معايير فرز الأنشطة بين الأتمتة، والتفويض للفرق، والإلغاء التام؟",
                    "كيف نضمن التزام الفريق بتطبيق الأنظمة التشغيلية دون الحاجة للرقابة اللصيقة؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على توثيق وهندسة العمليات والأنظمة التشغيلية للمنشأة.",
                    "لا يغطي استقطاب وإجراء مقابلات الموظفين (مكانها: domains/business_architecture/02_hiring).",
                    "لا يغطي تصميم لوحات التحكم الكبرى للمؤشرات (مكانها: domains/business_architecture/03_metrics)."
                ]
            },
            "02_hiring": {
                "title_ar": "التوظيف وبناء وإدارة الفرق",
                "retrieval_questions": [
                    "كيف يُبنى نظام توظيف مستمر يجذب أفضل 1% من الكفاءات الميدانية المتخصصة؟",
                    "ما هي هياكل المقابلات واختبارات المهام الواقعية لكشف الكفاءة العملية بدقة؟",
                    "كيف تُهيكل خطة التأهيل والتدريب السريع (Onboarding) في أول 30 يوماً للموظف الجديد؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على التوظيف، واختيار الكفاءات، والتأهيل، وإدارة الموارد البشرية.",
                    "لا يغطي توثيق العمليات الفنية نفسها (مكانها: domains/business_architecture/01_systems_ops).",
                    "لا يغطي لوحات تقييم المؤشرات العامة للمنشأة (مكانها: domains/business_architecture/03_metrics)."
                ]
            },
            "03_metrics": {
                "title_ar": "مؤشرات الأداء ولوحات التحكم",
                "retrieval_questions": [
                    "ما هي المؤشرات الحاكمة (Leading vs Lagging) التي تعكس الصحة التشغيلية للبيزنس؟",
                    "كيف تُصمم لوحة تحكم أسبوعية تكتشف نقاط الاختناق في الأداء قبل تفاقمها؟",
                    "ما هي آليات المحاسبة والمساءلة الدورية المبنية على الحقائق الرقمية الصريحة؟"
                ],
                "limitations": [
                    "يقتصر هذا القسم على مقاييس الأداء، ولوحات القيادة، ونظم المساءلة والمحاسبة.",
                    "لا يغطي تفاصيل توثيق العمليات الفردية (مكانها: domains/business_architecture/01_systems_ops).",
                    "لا يغطي مقابلات توظيف الأفراد (مكانها: domains/business_architecture/02_hiring)."
                ]
            }
        }
    }
}


def build_domain_index_content(domain_key: str, data: dict) -> str:
    """توليد محتوى INDEX.md الخاص بكل مجال رئيسي."""
    title_ar = data["title_ar"]
    desc = data["description"]
    rq_yaml = "\n".join(f'  - "{q}"' for q in data["retrieval_questions"])
    lim_yaml = "\n".join(f'  - "{l}"' for l in data["limitations"])
    rq_md = "\n".join(f"- {q}" for q in data["retrieval_questions"])
    lim_md = "\n".join(f"- {l}" for l in data["limitations"])
    
    subdomains_rows = []
    for sub_k, sub_v in data["subdomains"].items():
        sub_abs_path = f"/sdcard/wikillm/argon_version/wiki_ver2/domains/{domain_key}/{sub_k}/INDEX.md"
        subdomains_rows.append(f"| [`{sub_k}/`]({sub_abs_path}) | **{sub_v['title_ar']}** |")
    subdomains_table = "\n".join(subdomains_rows)

    content = f"""---
type: domain_index
domain: {domain_key}
status: pending
retrieval_questions:
{rq_yaml}
limitations:
{lim_yaml}
last_updated: 2026-10-25
---

# فهرس المجال المعرفي: {title_ar} ({domain_key})
## نظام الويكي التشغيلي — الإصدار الثاني (wiki_ver2)

### 1. الوظيفة المعرفية والنطاق الحاكم
{desc}

---

### 2. الأقسام الفرعية التابعة للمجال (Subdomains)

| القسم الفرعي (المسار) | المسمى الوظيفي بالعربية |
|---|---|
{subdomains_table}

---

### 3. أسئلة الاسترجاع الحاكمة (Retrieval Questions)
{rq_md}

---

### 4. الحدود والموانع الصريحة (Limitations)
{lim_md}

---

### 5. الحالة الراهنة ومسار الاستيعاب (Status)
- **الحالة:** `pending` (قيد التجهيز — شجرة المجلدات والقوالب مكتملة، وبانتظار استيعاب المصادر وحصد المصطلحات التخصصية).
- **التوجيه:** لا يُصاغ ماستر كلي للمجال قبل اكتمال مصطلحات وبلايبوكات الأقسام الفرعية الثلاثة التابعة له.
"""
    return content


def build_subdomain_index_content(domain_key: str, subdomain_key: str, domain_data: dict, sub_data: dict) -> str:
    """توليد محتوى INDEX.md الخاص بالقسم الفرعي."""
    domain_ar = domain_data["title_ar"]
    sub_ar = sub_data["title_ar"]
    rq_yaml = "\n".join(f'  - "{q}"' for q in sub_data["retrieval_questions"])
    lim_yaml = "\n".join(f'  - "{l}"' for l in sub_data["limitations"])
    rq_md = "\n".join(f"- {q}" for q in sub_data["retrieval_questions"])
    lim_md = "\n".join(f"- {l}" for l in sub_data["limitations"])

    content = f"""---
type: subdomain_index
domain: {domain_key}
subdomain: {subdomain_key}
status: pending
retrieval_questions:
{rq_yaml}
limitations:
{lim_yaml}
last_updated: 2026-10-25
---

# فهرس القسم الفرعي: {sub_ar} ({subdomain_key})
## المجال: {domain_ar} ({domain_key})

### 1. الوظيفة المعرفية والنطاق
يختص هذا القسم الفرعي بتأصيل المعرفة التشغيلية والإجرائية الخاصة بـ«{sub_ar}» ضمن نطاق «{domain_ar}». يوفر هذا المجلد كافة القوالب القياسية والبنى التحتية اللازمة لاستيعاب المصادر وتوليد المصطلحات المؤصلة قبل بناء البلايبوك الحاكم.

---

### 2. أسئلة الاسترجاع الحاكمة (Retrieval Questions)
{rq_md}

---

### 3. الحدود والموانع الصريحة (Limitations)
{lim_md}

---

### 4. الحالة الراهنة ومسار الاستيعاب (Status & Ingestion Route)
- **الحالة الراهنة:** `pending` (قيد التجهيز — الهيكل والقوالب مكتملة وبانتظار استيعاب المصادر وحصد المصطلحات).
- **مسار التغذية المعكوس:** `Master Playbook ← Concepts (C_*) ← Terms (T_*) ← Raw Sources (S_*)`.
- **الملفات التأسيسية المتاحة في هذا المجلد:**
  - `PLAYBOOK_TEMPLATE.md`: العقد الحاكم للبلايبوك النمطي (18 قسماً إجبارياً).
  - `TERMS_TEMPLATE.md`: قالب بطاقة المفهوم والمصطلح الذري الموثق بـ`path:line`.
  - `CONTINGENCY_MATRIX_TEMPLATE.md`: مصفوفة سياق الآراء وتعددية الرؤى الميدانية.
"""
    return content


def adapt_template_content(content: str, domain_key: str, subdomain_key: str, domain_ar: str, sub_ar: str) -> str:
    """استبدال أسماء المجال والقسم الفرعي في متن القالب."""
    # استبدال رأس YAML
    content = content.replace("domain: sales", f"domain: {domain_key}")
    content = content.replace("subdomain: 01_discovery_qualification", f"subdomain: {subdomain_key}")
    
    # استبدال العناوين الفرعية
    content = content.replace(
        "المجال: المبيعات (Sales) — القسم الفرعي: الاستكشاف والتأهيل (01_Discovery & Qualification)",
        f"المجال: {domain_ar} ({domain_key}) — القسم الفرعي: {sub_ar} ({subdomain_key})"
    )
    return content


def run():
    print("=== بدء تشغيل أداة نشر القوالب والمعمارية generate_templates.py ===")
    
    # التأكد من وجود القوالب الأساسية في المرجع
    base_playbook = BASE_SUBDOMAIN / "PLAYBOOK_TEMPLATE.md"
    base_terms = BASE_SUBDOMAIN / "TERMS_TEMPLATE.md"
    base_contingency = BASE_SUBDOMAIN / "CONTINGENCY_MATRIX_TEMPLATE.md"
    
    if not (base_playbook.exists() and base_terms.exists() and base_contingency.exists()):
        print(f"خطأ حرج: لم يتم العثور على القوالب الأساسية في {BASE_SUBDOMAIN}")
        sys.exit(1)
        
    playbook_raw = base_playbook.read_text(encoding="utf-8")
    terms_raw = base_terms.read_text(encoding="utf-8")
    contingency_raw = base_contingency.read_text(encoding="utf-8")

    total_subdomains_processed = 0
    total_files_written = 0

    for domain_k, domain_info in DOMAINS_DATA.items():
        domain_dir = DOMAINS_DIR / domain_k
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        # إنشاء INDEX.md الخاص بالمجال
        domain_index_path = domain_dir / "INDEX.md"
        domain_index_content = build_domain_index_content(domain_k, domain_info)
        domain_index_path.write_text(domain_index_content, encoding="utf-8")
        total_files_written += 1
        print(f"تم إنشاء فهرس المجال: {domain_index_path.relative_to(WIKI_DIR)}")

        # معالجة الأقسام الفرعية
        for sub_k, sub_info in domain_info["subdomains"].items():
            sub_dir = domain_dir / sub_k
            sub_dir.mkdir(parents=True, exist_ok=True)
            total_subdomains_processed += 1
            
            # إذا كان هو القسم الأساسي المكتوب يدوياً: لا يُعاد توليد قوالبه
            if domain_k == "sales" and sub_k == "01_discovery_qualification":
                print(f"القسم الأساسي {domain_k}/{sub_k} موجود ومكتوب يدوياً — تم تخطي إعادة كتابة قوالبه.")
                continue

            domain_ar = domain_info["title_ar"]
            sub_ar = sub_info["title_ar"]

            # 1. PLAYBOOK_TEMPLATE.md
            pb_content = adapt_template_content(playbook_raw, domain_k, sub_k, domain_ar, sub_ar)
            pb_path = sub_dir / "PLAYBOOK_TEMPLATE.md"
            pb_path.write_text(pb_content, encoding="utf-8")
            total_files_written += 1

            # 2. TERMS_TEMPLATE.md
            terms_content = adapt_template_content(terms_raw, domain_k, sub_k, domain_ar, sub_ar)
            terms_path = sub_dir / "TERMS_TEMPLATE.md"
            terms_path.write_text(terms_content, encoding="utf-8")
            total_files_written += 1

            # 3. CONTINGENCY_MATRIX_TEMPLATE.md
            cont_content = adapt_template_content(contingency_raw, domain_k, sub_k, domain_ar, sub_ar)
            cont_path = sub_dir / "CONTINGENCY_MATRIX_TEMPLATE.md"
            cont_path.write_text(cont_content, encoding="utf-8")
            total_files_written += 1

            # 4. INDEX.md الخاص بالقسم الفرعي
            sub_index_content = build_subdomain_index_content(domain_k, sub_k, domain_info, sub_info)
            sub_index_path = sub_dir / "INDEX.md"
            sub_index_path.write_text(sub_index_content, encoding="utf-8")
            total_files_written += 1

            print(f"تم نشر القوالب والفهرس في القسم الفرعي: {domain_k}/{sub_k}")

    print("\n=== اكتمال النشر بنجاح ===")
    print(f"إجمالي الأقسام الفرعية المغطاة: {total_subdomains_processed}")
    print(f"إجمالي الملفات المنشأة والمحدثة: {total_files_written}")


if __name__ == "__main__":
    run()
