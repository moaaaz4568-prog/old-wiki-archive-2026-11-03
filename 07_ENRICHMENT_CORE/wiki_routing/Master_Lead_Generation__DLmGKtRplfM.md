---
target_master: Master_Lead_Generation.md
source_shortcode: DLmGKtRplfM
index_format: table2
next_row: n/a (الفهرس غير مرقّم — max_row = null، يُلحق الصف بلا رقم)
concepts: 4
applied: false
---

## صفوف الفهرس المقترحة

| [[Concept_Google_Dork_Instagram_Email_Harvest]] | استخراج إيميلات ليدز من بايوهات إنستقرام عبر معاملات بحث Google |
| [[Concept_Email_Extractor_Chrome_SERP_Scrape]] | التقاط كل إيميلات صفحة نتائج البحث دفعة واحدة بإضافة Email Extractor |
| [[Concept_Zero_Budget_Lead_List_Stack]] | حزمة بناء قائمة ليدز بلا ميزانية: Google + إضافة + Sheets + GMass |
| [[Concept_Two_Column_Lead_Sheet_Minimum]] | الهيكل الأدنى لقاعدة الليدز: عمودا Emails وName فقط |

## المفاهيم الكاملة

### Concept_Google_Dork_Instagram_Email_Harvest — قالب استعلام Google لاصطياد بايوهات إنستقرام التي تعرض إيميلها

الاستعلام المكتوب حرفياً في شريط بحث Google كما ظهر على الشاشة:

```
site:instagram.com "coach" "united states" "@gmail.com"
```

تشريح المعادلة بوصفها قالباً قابلاً لإعادة الاستعمال:
- `site:instagram.com` — يحصر النتائج في نطاق إنستقرام وحده، فتصير كل نتيجة صفحة حساب حقيقي.
- `"coach"` — كلمة المهنة/النيتش المستهدف بين علامتي تنصيص. تُستبدل بأي نيتش آخر (agency، nutritionist، realtor).
- `"united states"` — الحصر الجغرافي، مأخوذ من نص البايو.
- `"@gmail.com"` — الحيلة الجوهرية: تفرض على Google ألّا يُظهر إلا الصفحات التي يظهر فيها نص إيميل جيميل داخل البايو، فيتحوّل البحث إلى فلتر «حسابات تعرض إيميلها علناً».

الحصيلة الظاهرة على الشاشة: «About 17,100 results (0.42 seconds)» من استعلام واحد.

الدرس العملي المرصود: مقتطف نتيجة Google نفسه يكشف الإيميل فلا حاجة لفتح كل حساب يدوياً. أمثلة ظهرت في المقتطفات مباشرة: Coach Tommy Lim Thor (@coach_tommylim) بإيميل ظاهر في المقتطف، وlaura.girard — online fitness coach بإيميل ظاهر كذلك، وAhmed kamal (@ahmedkamal_k) «The Transformation Coach … United States of America»، وBrandon DaCruz | Nutritionist & Online Physique Coach (41K Followers، 7088 Following، 3256 Posts).

خطأ شائع يتفاداه هذا المفهوم: إهمال علامات التنصيص — بدونها يبحث Google بحثاً فضفاضاً ويسقط شرط وجود الإيميل داخل الصفحة.

المصدر: DLmGKtRplfM (ريل صامت، عرض شاشة — لا تفريغ صوتي).

### Concept_Email_Extractor_Chrome_SERP_Scrape — استخراج إيميلات صفحة نتائج البحث دفعة واحدة

الأداة: إضافة كروم اسمها **Email Extractor**، وهي النتيجة الأولى في بحث Google عن `email extractor` (عدّاد النتائج الظاهر: «About 6,24,00,000 results»). وصفها في نتيجة البحث: «Powerful Extension To E... FEATURES: AutoVisit websites and Au...». البديل الويبي الظاهر ثانياً: Email Extractor من email-checker.net، ووُصف بأنه «completely free to use with some fair usag[e]».

آلية التشغيل: تُثبَّت الإضافة («4. Add the extension» — اللافتة الوحيدة المرقّمة الظاهرة على الشاشة)، ثم تُشغَّل وهي واقفة على صفحة نتائج Google فتلتقط كل إيميل ظاهر في الصفحة دفعة واحدة.

أرقام وعناصر الواجهة كما رُصدت:
- «Total Email ID's Found : 44» — أي 44 إيميلاً من صفحة نتائج واحدة.
- مفتاح **Autosave** (كان مطفأً في اللقطة) وزر **Automation** برتقالي.
- أيقونة الإضافة في شريط كروم تحمل الشارة الرقمية **44** كعدّاد مباشر.
- تلميح تشغيلي أسفل النافذة: «Tip: Try Ctrl+Shift+1 directly from the webpage» — اختصار لوحة مفاتيح يستدعي الاستخراج من أي صفحة.

نوعية الليد الناتجة (من عيّنة الالتقاط): بايوهات مدرّبين ومصوّرين ومقدّمي خدمات، غالبيتها عناوين gmail شخصية مع بعض عناوين الدومين الخاص. لم يظهر اسم المطوّر ولا السعر في أي إطار.

المصدر: DLmGKtRplfM.

### Concept_Zero_Budget_Lead_List_Stack — حزمة بناء قائمة ليدز بلا ميزانية وحدّها المعلن

المسار الكامل بستّ خطوات كما رُصد بصرياً: استعلام Google بمعاملات → تثبيت إضافة Email Extractor → استخراج إيميلات صفحة النتائج → لصقها في Google Sheets → التحقق مجاناً داخل Gmail → الإرسال عبر GMass.

كل مكوّن مجاني: Google، إضافة مجانية، Sheets، وGMass بخطة مجانية. الفئة المستهدفة مصرَّح بها في الكابشن: «This method is for people.. Who do not have 💲 to spend on softwares!».

**الحدّ المعلن صراحةً من صاحب المنشور**: «But if you want to scale your business.. Best is to do it using cold-email softwares!» — أي أن سقف هذا الأسلوب منخفض ولا يُقاس عليه في الحجم، ومن يريد التوسّع الحقيقي يحتاج أدوات إيميل بارد مدفوعة. هذا التحفّظ جزء من المفهوم لا هامش عليه.

أداة الإرسال في نهاية السلسلة: **GMass** (gmass.co). النصوص الحرفية من صفحتها: «Send email campaigns inside Gmail»، زر **Add to Gmail**، الشرط التقني «GMass requires Chrome»، الدليل الاجتماعي «5-star reviews from 300,000+ happy users»، وشريط «Used by employees of:» بشعارات Uber وTwitter وLinkedIn وGoogle. شريطا إعلان مؤرّخان: **03/29/24** «You can now have ChatGPT write your c[ampaigns]»، و**06/15/22** «Your campaigns can now include preview text». داخل Gmail يزرع GMass نفسه في نافذة «New Message» بزر **GMass ▸** بجوار زر **Send** العادي، ويعرض المستلمين بمربّعات اختيار.

آلية التوزيع المرفقة بالمنشور: بوابة تعليق — المستند «how you can scale your business using just cold-email» مقابل متابعة + تعليق كلمة **"email"**.

المصدر: DLmGKtRplfM.

### Concept_Two_Column_Lead_Sheet_Minimum — الهيكل الأدنى لقاعدة الليدز

يُفتح جدول Google Sheets جديد (ظهر باسم «Untitled spreadsheet» على docs.google.com/spreadsheets) بعمودين اثنين فقط:
- العمود A: **Emails**
- العمود B: **Name**

تُلصق مخرجات الإضافة في العمود A. بساطة الهيكل مقصودة: عمودان يكفيان لدمج المتغيّرات (variables) في حملة لاحقاً. هذا يضع سقفاً واقعياً على تخصيص الرسالة في هذا المسار — لا يوجد عمود للشركة ولا للنيتش ولا لسطر مخصّص، فالتخصيص المتاح هو الاسم وحده.

المصدر: DLmGKtRplfM.

## ملاحظات أمانة على هذا الـ patch
- الريل صامت (`transcript_chars: 0`)، فكل ما أعلاه مقروء من الشاشة والكابشن لا من صوت.
- ترقيم الخطوات 1–6 أعلاه مستنتج من تسلسل الشاشات المرئي، لا من لافتات مرقّمة كاملة؛ اللافتة المرقّمة الوحيدة التي ظهرت فعلاً هي «4. Add the extension».
- لم أنقل أياً من عناوين البريد الشخصية الحقيقية التي ظهرت في اللقطة إلى صفوف الفهرس ولا إلى شرح المفاهيم؛ هي بيانات أفراد لا معرفة قابلة لإعادة الاستعمال.
- فهرس هذا الماستر غير مرقّم (max_row = null)، لذلك تُلحق الصفوف بلا أرقام في نهاية الجدول تحت `## §19 — قائمة المفاهيم` (السطر الأخير المرصود 1870).
