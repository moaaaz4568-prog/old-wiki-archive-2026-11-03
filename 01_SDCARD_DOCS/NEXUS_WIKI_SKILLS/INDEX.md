# فهرس Skills — Nexus Wiki

**إصدار العقد: 2026-10-10.** المرجع الحاكم هو `<alignment_path>` والملحق الأحدث
في `<user_messages_path>`؛ تُضبط هذه المسارات مع `<wiki_root>` و`<skills_root>`
قبل التشغيل. قواعد المواءمة الأحدث تتقدم على تعليمات قديمة تؤخر النسخ أو تمنع
تسجيل المرشحين. هذا الفهرس لا يعلن تنفيذ العقد داخل الويكي.

| Skill | الوظيفة | النطاق |
|---|---|---|
| `source-ingestion-and-dedup` | هوية المصدر والبصمة والتكرار | general |
| `claim-extraction-and-evidence` | Claim واقتباس وموضع وحدود | general |
| `opinion-context-evaluation` | حفظ الآراء حسب السياق واختبار الهبد | reusable with sales examples |
| `concept-deepening` | بناء Concept عميق من Claims | general |
| `master-synthesis-retrieval-gate` | Master كبير أو صغير بعد اكتمال مصطلحات المجال كله ومراجعة أدلته | reusable with sales examples |
| `evidence-driven-reasoning` | خطة وفرضيات واختبارات قابلة للتدقيق | general |
| `wiki-iteration-and-risk-control` | Agents وcheckpoints ودورة التحسين | general |
| `domain-discovery-and-routing` | فرز عام لكل المجالات بقراءة كاملة وprimary واحد وsecondary؛ غموض التصنيف غير العزل | general |
| `new-to-done-source-lifecycle` | نسخة مصدر فعلية في done وإغلاق routing مستقل عن استخراج المصدر وإغلاق المجال | general |
| `domain-term-inventory` | تسجيل المصطلحات أثناء القراءة مع Claims المرشحة ثم إكمال terms لكل المجال قبل أي Master | general |
| `sequential-domain-orchestration` | فرز عام، معرفة في current_domain فقط، وانتقال معرفي بعد domain_done | general |
| `folder-index-and-handoff` | فهارس root/domain/subdomain/layer وحزمة handoff بالحالة والاعتماديات | general |

## توجيه

`general` إجراء عام؛ `reusable with sales examples` إجراء قابل لإعادة الاستخدام
تتضمن نسخته أمثلة مبيعات، وليس اختصاصًا حصريًا بالمبيعات. عُدلت المهارات الثلاث
المساندة المصرح بها للمواءمة؛ بقيت المهارات الأربع الأخرى دون تعديل.

اقرأ `<skills_root>/<skill-name>/SKILL.md` مع تعليمات المشروع وschema والمرجع
الأحدث. ثبّت mapping الحالات في workflow دون إضافة قيم جديدة إلى Source.status.
لا تجعل نجاح فحص Markdown أو وجود مجلد تصريحًا بأن المصدر أو المجال مكتمل.

## معاني البوابات R/T/C/K/M/QA

هذه تسميات تشغيل لمعاني المواءمة، لا ادعاء أن برنامجًا قائمًا يطبقها:

| البوابة | شرطها ونطاقها | ليست شرطًا لـ |
|---|---|---|
| R | full semantic read، hash/dedup، تصنيف مثبت، نسخة مستقلة byte-exact متحققة في `done/<domain>/<subdomain>/`؛ ينتج route_done | لا ينتظر extraction أو Concepts أو Master |
| T | `domain_terms_complete`: استخراج ومراجعة مصطلحات كل المجال وكل subdomains ومصادر snapshot المغلق، مع كل المرشحين وقراراتهم | ليس شرطًا لتسجيل candidate Claims أو terms أثناء القراءة |
| C | مراجعة Claims على مستوى المساهمات: اقتباس/موضع/scope/نوع الدليل وتقييم مستقل؛ الخلاف المحفوظ ليس فشلًا | لا يحتاج إجماع الآراء أو Master |
| K | Concepts من Claims مراجعة ومصطلحات ذات provenance وحدود واضحة؛ لا تعريفات مختلقة | ليس شرطًا لـsource_done ولا ينتظر T العام إذا كانت أدلته جاهزة |
| M | بدء أي Master، حتى الصغير، بعد T لكل المجال ثم C/K لأدلته؛ توليف ومعرفة وتوجيه واسترجاع لا حشو | لا يصنع مصدرًا مكتمل الاستخراج بأثر رجعي |
| QA | مراجعة مستقلة معلنة النطاق؛ QA المصدر لا يساوي QA المجال الذي يضم المخرجات والفهارس واختبارات الاسترجاع | نجاح schema أو عد الملفات وحده ليس QA معرفيًا |

## الحالات والتشغيل

- `done` تصنيف ملموس للمصدر، لا `domain_done`. نسخة مستقلة افتراضيًا، ليست
  symlink أو hardlink؛ `source_refs` فهارس ثانوية فقط، لا بديلًا عن وجود الملف.
- `route_done` جائز لأي domain قبل extraction. الفرز العام لا يفتح مجال معرفة:
  extraction/deepening في `current_domain` فقط، والباقي `queued` لا quarantined.
- اجمع terms وcandidate Claims معًا أثناء قراءة المجال النشط، مع المواضع؛ ترتيب
  بوابات الاعتماد لا يعني تأجيل توثيق الاقتباسات حتى قراءة المجال كله.
- `source_done`: استخراج كامل terms/Claims مع تتبع وتقييم وQA، بلا اعتماد على
  Concepts أو Master. `subdomain_extraction_done` يجمع المصادر المحددة، ولا
  يجيز Master صغيرًا قبل T لكل المجال. لا يُستخدم `subdomain_done` القديم كاختصار
  غامض يجمع الاستخراج وإغلاق المعرفة.
- snapshot ليس sample ولا قائمة تخفي مرشحًا بلا قرار؛ المرشح غير المحسوم يمنع
  اكتمال التغطية. لا تعرّف مصطلحًا بالتخمين لإغلاق T. احفظ الخلاف مع scope.
- `quarantine` لفساد/تعذر قراءة/هوية غير موثوقة؛ غموض التصنيف `uncertain`،
  والانتظار `queued`. لا تحذف رأيًا مدعومًا لمجرد اختلافه.
- وصول جديد ينشئ `delta` ويعلّم التغطية المتأثرة `stale`؛ يُعالج في المجال
  النشط أو يصطف للدور. لا انتقال معرفي إلا بعد `domain_done` ومراجعة أثر delta
  قبل الانتقال، ولا فتح مجالين. يبقى الإغلاق القديم صحيحًا للقطته فقط.
- لا تعديل raw أو نقل يزيل الأصل أو حذف أو استخدام Codex. إخفاق التفويض لا
  يسمح للمنسق بتجاوز الملكيات أو بوابات المعرفة؛ Worker لا يولد subagents.
