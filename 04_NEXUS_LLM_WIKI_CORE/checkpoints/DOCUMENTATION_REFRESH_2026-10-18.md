# checkpoint — مزامنة التوثيق من القرص، 2026-10-18

## الهدف والنطاق

تحديث الحالة وفهارس sales والتقرير الآلي من الملفات الفعلية، دون تعديل المعرفة أو
raw أو config أو الأنظمة أو البروتوكولات. الكتابة محصورة في الملفات التسعة التي
حددها التكليف؛ لا تفويض فرعي، لا Codex، لا حذف ولا commit.

## حالة العمل الحالية

- جارٍ القياس؛ هذا checkpoint ليس شهادة اعتماد لأي ملف يجري تحريره.
- قُرئت تعليمات المشروع وREADME والحالة والفهارس الحالية. لا يوجد `.opencode/`
  داخل الويكي؛ سياق `/root/r/.opencode/` المقروء تاريخي ولم يُعدّل.
- محاولة `git_status` داخل الويكي أعادت `not a git repository`؛ لن يُستخدم git
  لإثبات الحالة أو لإنشاء commit.
- تبين أن عدّ ملفات Markdown في concepts يشمل `INDEX.md`؛ سيُعاد العد من
  frontmatter `type: concept`، وكذلك Masters من `type: master` فقط.

## baseline الحماية (قبل أي كتابة)

بدأ القياس عند `2026-10-18T22:59:54.199124+00:00` بأمر Python للقراءة والحساب
فقط: `os.walk` مرتب، SHA-256 لكل ملف؛ لا قراءة لمحتوى raw بغرض المعرفة.

| النطاق | النتيجة |
|---|---|
| raw | 1,820 ملفًا، 50,898,163 بايت، 14 مجلدًا، لا symlinks |
| raw content snapshot SHA-256 | `9609cc9bcc1f676abbac7d15545904653d4403eead42205bf69cd5dcc8339b8f` |
| raw metadata snapshot SHA-256 | `50f264e69d26ab8c4dd50d61ccbb1730de71434de79327a7bc0a865b26874757` |
| collections/corpus/manifest.jsonl | `aa8756ebcf18547a02658c0d46f6457ddd9c274edb3b8b4b08f50bea2eed7cb3` |
| collections/sales/manifest.json | `1c729810fbc2ca115e7cf55a17fe4a891eea62f63195c7304182622efee92923` |
| config/INDEX.md | `b2c3e047570213582a21777692173a29f9081205f597b8e03d7faae1740c0395` |
| config/domain_catalog.json | `3df551218814f08d345c6ce436f2df589b3f756d8ac891daa789c1354c4a1add` |
| config/processing_order.json | `4c77a8ecc537149f571f2e43ecdb858abbafefffae89d96261b3a94834529b8c` |

صيغة snapshot: SHA-256 لـJSON مضغوط UTF-8، `ensure_ascii=False`، مفاتيح مرتبة.
المحتوى: صفوف `[path,size,sha256]` بترتيب `os.walk` مع ترتيب أسماء المجلدات
والملفات. metadata: كائن `files/directories/symlinks`؛ صف الملف يضيف
`mode,mtime_ns,inode,device,nlink` وصف المجلد `[path,mode,mtime_ns,inode,device]`.
لا يدخل atime لأنه قد يتأثر بالقراءة.

## الخطوة التالية والعوائق

الخطوة التالية: فحص schemas الفعلية وarrays في دفعات الاستخراج، ثم قياس manifests
والتوجيه والنسخ وfrontmatter، وتحديث الملفات المسموح بها وفحص الروابط وLSP
وإعادة بصمات الحماية. لا توجد نتيجة تحقق نهائية بعد. اكتمال مراجعة المرشحات أو
بوابات المجال خارج مهمة مزامنة التوثيق.
