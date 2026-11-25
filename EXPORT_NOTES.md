# 📝 وثيقة منهجية تصدير المحادثات — EXPORT_NOTES

**الهدف:** توثيق المنهجية التقنية، واستعلامات SQL، وهياكل البيانات المستخدمة في تصدير محادثات الويكي من المصادر الأربعة.

---

## 1. محادثات Claude Code (`05_CONVERSATIONS/claude/`)
- **المصدر الأصلي:** `/root/.claude/projects/-root-r/` و `/root/.claude/history.jsonl` و `/root/r/conversations_backup/` و `/root/.claude/skills/`.
- **المنهجية:**
  - تم فحص وتصفية ملفات المشاريع بكلمات المفتاح `(wiki|ويكي|wikillm|nexus.?brain)`.
  - نُسخت الملفات الـ 14 الأصلية بصيغة JSONL الخام للحفاظ على الولاء الكامل لبنية المحادثة.
  - تم تصفية أسطر الويكي من `history.jsonl` (28 سطراً) إلى `history_wiki_filtered.jsonl`.
  - نُقلت جلسات التأسيس السبعة من يونيو 2026 من `conversations_backup` كاملة.
  - جُمعت مهارات الويكي الـ 8 في مجلد `skills/`.
  - جرى توليد `digest/digest.md` لرسائل المستخدم المباشرة لتمكين القراءة البشرية السريعة.

---

## 2. محادثات OpenCode (`05_CONVERSATIONS/opencode/`)
- **المصادر:**
  - القاعدة النشطة: `/root/.local/share/opencode/opencode.db` (914.8 MiB).
  - القاعدة الاحتياطية: `/root/r/BACKUP_OMINIRUSH_CHAT/opencode.db` (104.7 MiB).
- **المنهجية:**
  - فُتحت القواعد عبر SQLite URI بنمط القراءة فقط: `file:<path>?mode=ro`.
  - حُصر الاستخراج في النطاق A (الجلسات المطابقة بالعنوان صراحة للويكي).
  - استُخرجت كل جلسة كملف JSONL مستقل بسطور مرتبة تسلسلياً (رسائل + أجزاء).
  - تم استخدام الربط الخارجي `LEFT JOIN part` لضمان عدم سقوط أي رسالة ليس لها أجزاء.
  - إجمالي المستخرج: 52 جلسة (45 من النشطة + 7 من الاحتياطية)، بإجمالي 2,750 رسالة و 8,594 جزءاً.

---

## 3. محادثات Antigravity CLI (`05_CONVERSATIONS/agy/`)
- **المصادر:** `~/.gemini/antigravity-cli/conversations/` و `~/.gemini/antigravity-cli/brain/` و `conversation_summaries.db`.
- **المنهجية:**
  - تم فرز 173 ملف قاعدة بيانات SQLite مطابقة للويكي.
  - استُخرجت النواة التأسيسية الصافية للويكي (الـ 20 جلسة المحددة بدقة لبناء الويكي وأنظمة SYS) بنسخ قواعد بياناتها الأصلية وملفات Brain المقابلة لها في `core_wiki_sessions/` و `brain_logs/`.
  - تم تحويل سجلات المحادثات القوية ($\\ge 5$ مطابقات) إلى صيغة JSONL نقية داخل `tier1_strong/`.
  - أُنشئ فهرس شامل `index.csv` يضم الـ 173 جلسة بكافة بياناتها الوصفية وتواريخها وأحجامها.
  - أُعد ملف `digest.md` لأهم 20 جلسة.

---

## 4. محادثات OmniRush Agent (`05_CONVERSATIONS/omnirush/`)
- **المصادر:** `~/.omnirush/agent/sessions/` و `~/.local/share/omnirush/opencode.db` و `/root/r/BACKUP_OMINIRUSH_CHAT/opencode.db`.
- **المنهجية:**
  - جرى حصر 826 ملف JSONL مطابق، وانتُخبت أهم الجلسات الموضوعية ذات الكثافة المعرفية العالية بحجم إجمالي ~45MB داخل `topic_sessions/`.
  - استُخرجت نصوص الويكي الصافية من جداول الأجزاء (`part`) في قواعد بيانات OmniRush كملفات JSONL مستقلة داخل `db_extracted/`.
  - تم توثيق الفهرس الموحد للجلسات في `index.csv`.
