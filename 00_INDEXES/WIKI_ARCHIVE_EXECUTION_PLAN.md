# 🗂️ خطة تنفيذ أرشيف الويكي — `/sdcard/WIKI_ARCHIVE_2026-11-03/`

> **الحالة:** خطة (تخطيط فقط — لم يُنفَّذ أي نسخ بعد)
> **المصدر:** التقارير الستة قراءةً فقط (SDCARD_WIKI_INDEX · WIKI_INDEX · WIKI_CONVERSATION_SCAN · OPencode_DB_WIKI_SCAN · AGY_WIKI_CONVERSATIONS_SCAN · OMNIRUSH_WIKI_CONVERSATIONS_SCAN)
> **التاريخ:** 2026-11-03
> **القيود الحاكمة:** مساحة 646M متاحة · ميزانية **250M** إجمالي النسخ الجديد · add-only (لا rm) · ممنوع نسخ db كاملة >50MB · كل محادثة مطابقة تُصدَّر JSONL/MD/CSV + فهرس.

---

## 0. الأرقام الحاكمة من التقارير (مرجع التخطيط)

| بند | القيمة | المصدر |
|---|---|---|
| مساحة sdcard المتاحة | 646M (99% ممتلئ) | SDCARD_REPORT §1 |
| مجلدات ويكي على sdcard | ~543M / 27,297 ملف | SDCARD_REPORT §2 |
| نطاق /root الويكي | ~431M / ~13,500 ملف | WIKI_INDEX §3 |
| محادثات Claude المطابقة | 14 ملف · 8.56M + history 0.43M ≈ **9M** | CONV_SCAN §1,§5 |
| OpenCode تصدير النطاق A (العناوين المطابقة) | 44 + 7 = 51 محادثة · **23.2M** | DB_SCAN §5 |
| OpenCode النطاق B (أي جزء مطابق) | 787 + 36 · 130.2M (ضوضاء) | DB_SCAN §5 |
| AGY | 168/182 ملف مطابق · 18 صريحة · 83 قوية · مجلد 230M | AGY_REPORT §1,§2 |
| OmniRush | **468** موضوع ويكي فريد · 816 بأي ذكر | OMNI_REPORT §7 |
| تكرارات معروفة | ~115M على sdcard + zips 91M | SDCARD_REPORT §7 |
| أكبر ملفات ثقيلة | index.json.gz 17M ×2 · evidence_ledger 5.7M · raw/ 53M | SDCARD_REPORT §6 |

**قواعد استخراج صارمة مستمدة من التقارير:**
1. لا تُنسخ: `opencode.db` (914M/446M/105M) — استخراج SQL نصي فقط عبر `mode=ro`.
2. لا تُنسخ: `.nexus_work`، `node_modules`، `__pycache__`، `.git`، `omnirush-upload-*` (172M+88M)، `~/.cache`، ZIP المكرر.
3. لا إعادة فحص شامل (grep على 48G فشل سابقاً بمهلة 180s) — نعتمد قوائم المطابقة الجاهزة في التقارير + فحص موجّه فقط.

---

## 1. الهيكل النهائي للمجلد الرئيسي + ميزانية MB

```
/sdcard/WIKI_ARCHIVE_2026-11-03/                     إجمالي الميزانية ≤ 250M
├── README.md                                        (الخريطة + حالة التنفيذ)
├── MANIFEST.json                                    (ربط كل ملف بمساره الأصلي + hash)
├── EXPORT_NOTES.md                                  (منهجية التصدير لكل مصدر)
├── FALLBACK.md                                      (سلّم الأولوية عند نفاد المساحة)
├── RISKS.md                                         (جدول المخاطر)
│
├── 00_INDEXES/                                      ميزانية: 4M   · متوقع ~2M
│   ├── README.md
│   ├── source_inventory.csv                         (كل مصدر: مسار، حجم، حالة)
│   ├── excluded_files.csv                           (المستثنى + السبب + hash المصدر)
│   ├── conversations_index.csv                      (فهرس موحّد لكل المحادثات الأربعة)
│   └── hashes.sha256                                (hash كل ملف مؤرشف)
│
├── 01_SDCARD_DOCS/                                  ميزانية: 10M  · متوقع ~9.5M
│   ├── README.md
│   ├── wikillm/                                     (8.3M كامل — المرجع الأول)
│   ├── NEXUS_WIKI_SKILLS/                           (0.2M)
│   ├── root_files/                                  (ملفات /sdcard المفرقة ~0.4M)
│   └── nexus_brain_wiki_docs/                       (5 ملفات md فقط من Nexus_Brain)
│
├── 02_ROOT_DOCS/                                    ميزانية: 6M   · متوقع ~4M
│   ├── README.md
│   ├── session_logs/                                (wiki.md · الويكي.md · wiki1.md · wiki)
│   ├── architecture/                                (SCALABLE_ARCHITECTURE · V3_SYS · NEW_WIKI_MASTER_PLAN)
│   ├── hubs/                                        (WIKI_HUB · nexus_wiki_links)
│   └── scripts/                                     (process_wiki_loop.sh)
│
├── 03_WIKI_LAYERS/                                  ميزانية: 12M  · متوقع ~11M
│   ├── README.md
│   ├── nexus_wiki/                                  (كل الطبقات بدون 04_SEARCH/index.json.gz)
│   ├── wiki_small_layers/                           (V1/V2 + ملفات /sdcard/wiki الصغيرة فقط)
│   └── BIG_FILE_POINTERS.csv                        (index.json.gz 17M×2 + DEFECTS/LINK_PLAN…)
│
├── 04_NEXUS_LLM_WIKI_CORE/                          ميزانية: 32M  · متوقع ~30M
│   ├── README.md
│   ├── reports/ systems/ indexes/ config/ concepts/ done/ tools/  (≈6M)
│   ├── charter + root md files                      (≈0.1M)
│   ├── collections_filtered/                        (بدون ledger 5.7M + classification 1.7M)
│   ├── staging_manifests/                           (manifests فقط من staging 15M)
│   ├── sources_filtered/ + claims_filtered/          (ملفات ≤500K فقط، الباقي pointer)
│   └── BIG_FILE_POINTERS.csv                        (raw/ 53M كاملاً + الكبيرة)
│
├── 05_CONVERSATIONS/
│   ├── claude/                    ميزانية: 10M · متوقع ~9M
│   │   ├── README.md
│   │   ├── raw/                                    (14 jsonl أصلية كما هي + history_wiki_filtered.jsonl)
│   │   ├── digest/                                 (digest.md لكل ملف: رسائل user المطابقة)
│   │   └── index.csv
│   ├── opencode/                 ميزانية: 28M · متوقع ~25M
│   │   ├── README.md
│   │   ├── main_db/                                (JSONL لكل من 44 جلسة)
│   │   ├── backup_db/                              (JSONL لكل من 7 جلسات)
│   │   └── index.csv
│   ├── agy/                      ميزانية: 34M · متوقع ~30M
│   │   ├── README.md
│   │   ├── tier1_strong/                           (JSONL لل83 قوية ∪ 18 صريحة)
│   │   ├── tier2_index.csv                         (metadata للمتبقي 85 فقط — بلا نص)
│   │   └── index.csv
│   └── omnirush/                 ميزانية: 64M · متوقع ~62M
│       ├── README.md
│       ├── jsonl_topic/                            (أهم ملفات jsonl الموضوع حسب occurrences)
│       ├── db_extracted/                           (95 جلسة جديدة من القاعدة النشطة → JSONL)
│       └── index.csv
│
├── 06_CODE_TOOLS/                                    ميزانية: 26M  · متوقع ~24M
│   ├── README.md
│   ├── llm-wiki-compiler/                           (16M بدون __pycache__)
│   └── llm-wiki-plugin/                             (9.1M بدون .git/node_modules/__pycache__)
│
├── 07_ENRICHMENT_CORE/                               ميزانية: 8M   · متوقع ~6M
│   ├── README.md
│   ├── control/                                     (WIKI_STRUCTURE.md + control/*.md)
│   ├── wiki_routing/                                (فقط *.md/*.json ≤500K)
│   └── reports_subset/                              (تقارير الويكي md فقط)
│
└── _RESERVE/                                        ميزانية: 24M  (تنفّس + طوارئ)
    └── README.md
```

### جدول الميزانية (المجموع = 250M)

| # | المجلد | الميزانية MB | متوقع فعلي MB | الأولوية |
|---|---|---:|---:|---|
| 00 | `_INDEXES` + ملفات الجذر (README/MANIFEST/NOTES) | 4 | 2 | P0 |
| 01 | `01_SDCARD_DOCS` | 10 | 9.5 | P0 |
| 02 | `02_ROOT_DOCS` | 6 | 4 | P0 |
| 03 | `03_WIKI_LAYERS` | 12 | 11 | P1 |
| 04 | `04_NEXUS_LLM_WIKI_CORE` | 32 | 30 | P1 |
| 05a | `05_CONVERSATIONS/claude` | 10 | 9 | P0 |
| 05b | `05_CONVERSATIONS/opencode` | 28 | 25 | P1 |
| 05c | `05_CONVERSATIONS/agy` | 34 | 30 | P2 |
| 05d | `05_CONVERSATIONS/omnirush` | 64 | 62 | P2 |
| 06 | `06_CODE_TOOLS` | 26 | 24 | P1 |
| 07 | `07_ENRICHMENT_CORE` | 8 | 6 | P1 |
| — | `_RESERVE` (تنفّس داخل الأرشيف) | 24 | — | — |
| | **الإجمالي** | **250** | **~232** | |

> سقف أمان تشغيلي: **يُوقف التنفيذ إذا `df` أظهر Available < 30M** → تفعيل سلّم الفشل (§7).

---

## 2. تفصيل كل مجلد فرعي: المصدر · الأمر · الاستثناءات

### 00_INDEXES (4M)
- **المصدر:** إخراج التقارير الستة + نتائج فحص hash.
- **الأوامر:**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03
mkdir -p "$A"/{00_INDEXES,01_SDCARD_DOCS,02_ROOT_DOCS,03_WIKI_LAYERS,04_NEXUS_LLM_WIKI_CORE,05_CONVERSATIONS/{claude,opencode,agy,omnirush},06_CODE_TOOLS,07_ENRICHMENT_CORE,_RESERVE}
df -h /mnt/sdcard | tee "$A/00_INDEXES/preflight_df.txt"
cp /root/r/SDCARD_WIKI_INDEX_REPORT.md /root/r/WIKI_INDEX_REPORT.md \
   /root/r/WIKI_CONVERSATION_SCAN_REPORT.md /root/r/OPencode_DB_WIKI_SCAN_REPORT.md \
   /root/r/AGY_WIKI_CONVERSATIONS_SCAN_REPORT.md /root/r/OMNIRUSH_WIKI_CONVERSATIONS_SCAN_REPORT.md \
   "$A/00_INDEXES/"   # التقارير المصدرية = ~0.5M فقط
```
- **يستثنى:** لا شيء (التقارير الستة نفسها هي الفهرس المرجعي).

### 01_SDCARD_DOCS (10M)
- **المصادر:**
  - `/sdcard/wikillm/` (8.3M) — نسخة كاملة.
  - `/sdcard/NEXUS_WIKI_SKILLS/` (0.2M).
  - `/sdcard/NEW_WIKI_MASTER_PLAN.md` + `NEXUS_LLM_WIKI_REPORT.html` + `NEXUS_WIKI_EXPLAIN.html` + `IGWIKI_ALL_IN_ONE.txt` + `exploration-artifacts/WIKI_SKILLS_INSTALLATION.md` (~0.4M).
  - من `/sdcard/Nexus_Brain` **5 ملفات md فقط**: `NEXUS_LLM_WIKI.md`, `NEXUS_LLM_WIKI_PHASE2.md`, `Nexus_Brain_Prompt.md`, `nexus_vault/NEXUS_BRAIN.md`, `Nexus_Brain_Processed/` (28K).
- **الأوامر:**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03
cp -r /sdcard/wikillm            "$A/01_SDCARD_DOCS/"
cp -r /sdcard/NEXUS_WIKI_SKILLS  "$A/01_SDCARD_DOCS/"
mkdir -p "$A/01_SDCARD_DOCS/root_files" "$A/01_SDCARD_DOCS/nexus_brain_wiki_docs"
cp /sdcard/NEW_WIKI_MASTER_PLAN.md /sdcard/NEXUS_LLM_WIKI_REPORT.html \
   /sdcard/NEXUS_WIKI_EXPLAIN.html /sdcard/IGWIKI_ALL_IN_ONE.txt \
   /sdcard/exploration-artifacts/WIKI_SKILLS_INSTALLATION.md \
   "$A/01_SDCARD_DOCS/root_files/"
cp /sdcard/Nexus_Brain/NEXUS_LLM_WIKI.md \
   /sdcard/Nexus_Brain/NEXUS_LLM_WIKI_PHASE2.md \
   /sdcard/Nexus_Brain/Nexus_Brain_Prompt.md \
   /sdcard/Nexus_Brain/nexus_vault/NEXUS_BRAIN.md \
   "$A/01_SDCARD_DOCS/nexus_brain_wiki_docs/"
cp -r /sdcard/Nexus_Brain/Nexus_Brain_Processed "$A/01_SDCARD_DOCS/nexus_brain_wiki_docs/"
```
- **يستثنى ولماذا:** `Nexus_Brain.zip` و `Nexus_Brain-2.zip` (45.4M×2 متطابقان — تكرار، يُسجَّل hash فقط) · مجلد `Nexus_Brain` الكامل (385M) · نسخ الويكي الثلاثة 23M داخله (يُؤرَّش في `excluded_files.csv` بـhash) · نسخة واتساب من IGWIKI (مطابقة بالحجم).

### 02_ROOT_DOCS (6M)
- **المصادر:** `/root/r/wiki.md` (440K) · `/root/r/الويكي.md` (628K) · `/root/r/wiki1.md` (464K) · `/root/r/wiki` (440K — مطابق لـ wiki.md، يُنسخ رغم ذلك لأن add-only ولا نحذف؛ يُسجَّل covered_by في MANIFEST) · `/root/r/NEXUS_WIKI_SCALABLE_ARCHITECTURE.md` · `/root/r/WIKI_HUB/` · `/root/r/nexus_wiki_links/` · `/root/process_wiki_loop.sh` · `/root/r/V3_SYS/` (483K) · `/root/r/NEXUS_REFERENCES/llm-wiki-compiler` يُنقل لـ06 (هنا فقط وثائقه md) · `/root/r/reports/sales-proof/*-v3.md` (3 ملفات).
- **الأوامر:**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03
mkdir -p "$A/02_ROOT_DOCS"/{session_logs,architecture,hubs,scripts}
cp /root/r/wiki.md /root/r/الويكي.md /root/r/wiki1.md /root/r/wiki \
   "$A/02_ROOT_DOCS/session_logs/"
cp /root/r/NEXUS_WIKI_SCALABLE_ARCHITECTURE.md /root/r/V3_SYS/*.md \
   /root/r/reports/sales-proof/*-v3.md "$A/02_ROOT_DOCS/architecture/" 2>/dev/null
cp -r /root/r/WIKI_HUB /root/r/nexus_wiki_links "$A/02_ROOT_DOCS/hubs/"
cp /root/process_wiki_loop.sh "$A/02_ROOT_DOCS/scripts/"
```
- **يستثنى:** `/root/r/nexus_enrichment` كاملاً (209M — يُستخرج نواة فقط في 07) · `NEXUS_GITHUB_PACKAGE` كاملاً (341M) · `V3/` (24M — يُؤشَّر فقط) · `orchestrator` غير الويكي · `data/masters/*_V3.json` (يُؤشَّر؛ يُنسخ فقط إذا بقيت مساحة >100M في `_RESERVE`).

### 03_WIKI_LAYERS (12M)
- **المصادر:** `/sdcard/nexus_wiki/` (25M) + `/sdcard/wiki/` (24M).
- **الأوامر (بعد قياس دقيق):**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03
# 1) قياس ما سيُستثنى أولاً
du -sh /sdcard/nexus_wiki/03_WIKI_V3_NEW/04_SEARCH/index.json.gz \
       /sdcard/wiki/03_WIKI_V3_STRUCTURED/04_SEARCH/index.json.gz
sha256sum /sdcard/{nexus_wiki/03_WIKI_V3_NEW,wiki/03_WIKI_V3_STRUCTURED}/04_SEARCH/index.json.gz
# 2) نسخ مع تجاهل الملفات الثقيلة (تجاهل الأخطاء حتى لا يفشل النسخ كله)
mkdir -p "$A/03_WIKI_LAYERS"/{nexus_wiki,wiki_small_layers}
cp -r /sdcard/nexus_wiki/. "$A/03_WIKI_LAYERS/nexus_wiki/" 2>/dev/null || true
rm_placeholder_note="لا rm — بدل ذلك يُنسخ المجلد ثم يُستبدل الملف الكبير بمذكرة POINTER"
# بدائل add-only بديلة (مفضّلة — لا تكتب أصلاً):
(cd /sdcard/nexus_wiki && find . -type f ! -name 'index.json.gz' ! -name '*.gz' \
   -print0 | tar --null -cf - -T -) | tar -xf - -C "$A/03_WIKI_LAYERS/nexus_wiki/"
(cd /sdcard/wiki && find . -type f \( -name '*.md' -o -name '*.txt' -o -name '*.link.txt' \
   -o -name '*.jsonl' \) ! -size +2M -print0 | tar --null -cf - -T -) | tar -xf - -C "$A/03_WIKI_LAYERS/wiki_small_layers/"
# 3) سجل المؤشرات
{ echo "source,sha256,size,reason";
  sha256sum /sdcard/nexus_wiki/03_WIKI_V3_NEW/04_SEARCH/index.json.gz | awk '{print "/sdcard/nexus_wiki/03_WIKI_V3_NEW/04_SEARCH/index.json.gz,"$1",17825792,duplicate-gz-excluded"}';
} > "$A/03_WIKI_LAYERS/BIG_FILE_POINTERS.csv"
```
- **يستثنى ولماذا:** `index.json.gz` 17M مرتين (أكبر ملفين، متطابقان تقريباً — لا نضاعف 34M) · ملفات V3 >2M من `wiki/` (مطابقة لنظيرتها في nexus_wiki — تُسجَّل بـhash في `BIG_FILE_POINTERS.csv`). **السبب الجذري:** الميزانية تفرض ألا ندفع 34M لملف فهرس واحد قابل لإعادة توليده.

### 04_NEXUS_LLM_WIKI_CORE (32M)
- **المصدر:** `/sdcard/NEXUS_LLM_WIKI/` (101M).
- **الأوامر:**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03; S=/sdcard/NEXUS_LLM_WIKI; D="$A/04_NEXUS_LLM_WIKI_CORE"
mkdir -p "$D"
# نسخ الأقسام الصغيرة كاملة
for d in reports systems indexes config concepts done tools checkpoints model_protocols; do
  [ -d "$S/$d" ] && cp -r "$S/$d" "$D/"
done
cp "$S"/*.md "$S"/*.html "$D/" 2>/dev/null || true
# collections بدون أكبر ملفين
mkdir -p "$D/collections_filtered"
(cd "$S/collections" && find . -type f ! -name 'full_evidence_ledger.jsonl' \
   ! -name 'source_classification.json' -print0 | tar --null -cf - -T -) | tar -xf - -C "$D/collections_filtered/"
# staging: manifests فقط
mkdir -p "$D/staging_manifests"
find "$S/staging" -maxdepth 3 -type f \( -iname '*manifest*' -o -name '*.md' \) -size -500K \
   -exec cp --parents {} "$D/staging_manifests/" \; 2>/dev/null || true
# sources/claims: ملفات ≤500K فقط
for d in sources claims; do
  mkdir -p "$D/${d}_filtered"
  (cd "$S/$d" && find . -type f -size -500K -print0 | tar --null -cf - -T -) | tar -xf - -C "$D/${d}_filtered/"
done
# سجل المستثنى
{ echo "source,sha256,size,reason";
  find "$S/raw" "$S/collections/sales/full_evidence_ledger.jsonl" \
       "$S/collections/sales/source_classification.json" -type f 2>/dev/null | while read -r f; do
    printf '%s,%s,%s,%s\n' "$f" "$(sha256sum "$f"|cut -d' ' -f1)" "$(stat -c%s "$f")" "heavy-excluded"
  done; } > "$D/BIG_FILE_POINTERS.csv"
du -sh "$D"   # يجب أن ≤ 32M قبل المتابعة
```
- **يستثنى ولماذا:** `raw/` 53M (بيانات أولية خام — أكبر بند منفرد) · `full_evidence_ledger.jsonl` 5.7M · `source_classification.json` 1.7M · `transcript_full.txt` 1.5M · `catalog.json` 1.5M (يُنسخ فقط إذا بقيت المساحة) · `__pycache__`. **السبب:** الميزانية + أن هذه ملفات إعادة-توليد/خام.

### 05a — تصدير محادثات Claude (10M) — «claude 14 ملف»
- **الصيغة المختارة:** **JSONL خام** (لأن الملفات نفسها JSONL أصلية — أعلى ولاء) + **digest MD** (رسائل user المطابقة فقط) + **index.csv**. لا CSV للنص الكامل (يفقد البنية).
- **الترشيح:** القائمة الجاهزة من `WIKI_CONVERSATION_SCAN_REPORT` (14 مساراً) + أسطر `history.jsonl` المطابقة (26 سطر).
- **الأوامر:**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03; D="$A/05_CONVERSATIONS/claude"
mkdir -p "$D"/{raw,digest}
IDS="f9f0f6e4-7562-4cf0-8c2c-19da0f31a9b6 3a75fdd6-e175-405c-b690-2ed385da8e41 0e7a4206-157c-4213-8ed2-3184e5c6c6be 828efe70-ad69-4a74-a88e-5bb69ea58fd5 27df899b-1659-445c-b121-9dedf65d3fed 72f68e8b-b5c9-4f5c-9507-ce6b34161b66 2f219a0b-e15a-4390-87ce-4c63a482f923"
# الملفات الرئيسية (7) + subagents المطابقة (7)
while read -r f; do cp "$f" "$D/raw/$(echo "$f" | sed 's|/|__|g')"; done < <(
  find /root/.claude/projects -name '*.jsonl' -type f | while read -r f; do
    for id in $IDS agent-a6d04f2404633c28e agent-a9510b1d4d257f0dd agent-a8d4f521cda09003c \
              agent-ad3d71c3886e6692c agent-ace079adadd9aac28 agent-a1197c3f65d53d8e agent-acef353e75e560adf; do
      case "$f" in *"$id"*) echo "$f";; esac
    done; done | sort -u)
grep -E 'wiki|ويكي|wikillm|nexus.?brain' /root/.claude/history.jsonl > "$D/raw/history_wiki_filtered.jsonl"
# digest: رسائل user المطابقة فقط (JSONL → MD)
python3 - <<'PY'
import json,glob,os,re,hashlib
D=os.environ.get('D','/sdcard/WIKI_ARCHIVE_2026-11-03/05_CONVERSATIONS/claude')
pat=re.compile(r'wiki|ويكي|wikillm|nexus.?brain',re.I)
rows=[]
for p in glob.glob(D+'/raw/*.jsonl'):
    for i,line in enumerate(open(p,encoding='utf-8',errors='replace')):
        try: o=json.loads(line)
        except Exception: continue
        if o.get('role')=='user' or o.get('type')=='user':
            c=json.dumps(o,ensure_ascii=False)
            if pat.search(c): rows.append({'file':os.path.basename(p),'line':i+1,'ts':o.get('timestamp'),'text':c[:4000]})
rows.sort(key=lambda r:(r['file'],r['line']))
open(D+'/digest/digest.md','w',encoding='utf-8').write(
  '\n\n'.join(f"### {r['file']} :{r['line']}\n- ts: {r['ts']}\n\n{r['text']}" for r in rows))
with open(D+'/index.csv','w',encoding='utf-8') as f:
    f.write('file,matched_user_msgs,bytes\n')
    for p in sorted(glob.glob(D+'/raw/*')):
        f.write(f"{os.path.basename(p)},{sum(1 for r in rows if r['file']==os.path.basename(p))},{os.path.getsize(p)}\n")
print('exported',len(rows),'user msgs')
PY
```
- **الحجم المتوقع:** raw 9M + digest ~1.5M → قد يتجاوز 10M ⇒ **الاستثناء:** إذا تجاوز 10M يُنسخ raw للملفين الرئيسيين فقط (`3a75fdd6` 6.2M + `f9f0f6e4` 1.4M) والباقي digest فقط (الاثنان يشكّلان 97% من المطابقات).

### 05b — تصدير OpenCode (28M) — «opencode 44 جلسة»
- **الصيغة:** **JSONL لكل جلسة** (session_id + title + messages/parts مرتبة زمنياً) + **index.csv**. لا MD للكل (ضياع بنية) — MD اختياري لأكبر 5 جلسات فقط إذا بقيت المساحة.
- **الترشيح:** النطاق **A فقط** (44 عنواناً مطابقاً + 7 من النسخة الاحتياطية = 23.2M خام) — النطاق B (130M) ضوضاء كما أثبت التقرير.
- **الاستثناءات:** `event` (17,456 صف — موجود المحتوى في part) · `session_diff` (5×2 بايت) · `session_input` (فارغ) · الملف `.db` نفسه ممنوع نسخه (>50M).
- **الأوامر (مرحلتان — فحص ثم استخراج):**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03; D="$A/05_CONVERSATIONS/opencode"; mkdir -p "$D"/{main_db,backup_db}
# (1) فحص الـschema أولاً — إلزامي لأن التقرير لم يوثّق العلاقات
sqlite3 "file:/root/.local/share/opencode/opencode.db?mode=ro" ".schema session" ".schema message" ".schema part" | tee "$D/schema_snapshot.txt"
# (2) استخراج (القالب — يُعدَّل بعد فحص الـschema؛ الافتراض message.session_id و part.message_id)
python3 - <<'PY'
import sqlite3,json,os,csv
OUT='/sdcard/WIKI_ARCHIVE_2026-11-03/05_CONVERSATIONS/opencode'
def export(db,sub,ids):
    con=sqlite3.connect(f'file:{db}?mode=ro',uri=True); con.row_factory=sqlite3.Row
    rows=con.execute("""SELECT s.id sid, s.title, s.created_at, m.id mid, m.data mdata, p.id pid, p.type ptype, p.data pdata
        FROM session s JOIN message m ON m.session_id=s.id JOIN part p ON p.message_id=m.id
        WHERE s.id IN (%s) ORDER BY s.id, m.id, p.id""" % ','.join('?'*len(ids)), ids).fetchall()
    by={}
    for r in rows: by.setdefault(r['sid'],[]).append(dict(r))
    with open(f'{OUT}/index.csv','a',newline='',encoding='utf-8') as fi:
        w=csv.writer(fi)
        if fi.tell()==0: w.writerow(['db','session_id','title','msgs','parts','bytes'])
        for sid,items in by.items():
            path=f'{OUT}/{sub}/{sid}.jsonl'
            with open(path,'w',encoding='utf-8') as f:
                for it in items: f.write(json.dumps(it,ensure_ascii=False)+'\n')
            w.writerow([sub,sid,items[0].get('title'),len({i['mid'] for i in items}),len(items),os.path.getsize(path)])
    con.close()
# 44 معرّفات من الجدول 4 في التقرير (تُلصق قائمة session ids هناك) + 7 من backup
# main_ids=[...]; export('/root/.local/share/opencode/opencode.db','main_db',main_ids)
# backup_ids=[...]; export('/root/r/BACKUP_OMINIRUSH_CHAT/opencode.db','backup_db',backup_ids)
PY
```
- **الحجم المتوقع:** ~24M خام → JSONL ≤26M (ضمن 28M).
- **ملاحظة:** `ses_e8f88d729ffe…` و `ses_e8f888e53ffe…` متطابقتان ⇒ تُصدَّر واحدة والثانية `covered_by` في MANIFEST (توفير ~0.8M).

### 05c — تصدير AGY (34M) — «agy 168»
- **الصيغة:** **JSONL لكل محادثة** (tier1) + **index.csv** للمتبقي بلا نص (tier2). لا MD (168 ملفاً = فوضى) — MD واحد `digest.md` لأعلى 15.
- **الترشيح:**
  - **Tier1 = 83 قوية (≥5 occurrences) ∪ 18 صريحة** ≈ ≤90 ملف → JSONL كامل.
  - **Tier2 = الباقي (~85)** → صفوف index فقط (id, occurrences, size, mtime).
- **الأوامر:**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03; D="$A/05_CONVERSATIONS/agy"; mkdir -p "$D"/{tier1_strong,digest}
C=~/.gemini/antigravity-cli/conversations
# (1) فحص schema للملف المرجعي — إلزامي (التقرير لم يوثّق جداول المحادثة)
sqlite3 "file:$(ls $C/*.db|head -1)?mode=ro" ".tables" | tee "$D/schema_tables.txt"
sqlite3 "file:$(ls $C/*.db|head -1)?mode=ro" ".schema" | tee "$D/schema_full.txt"
# (2) قائمة tier1 من التقرير (83 strong + 18 explicit — تُلصق من AGY_REPORT)
# TIER1_IDS="e9058b66-b2d2-47ae-adef-0c53abcc9cbe da09e821-... ..."
# (3) استخراج JSONL لكل tier1 (python + sqlite3 mode=ro، يقرأ كل جدول نصي ويطويه JSON line)
python3 - <<'PY'
import sqlite3,json,os,glob,csv
C=os.path.expanduser('~/.gemini/antigravity-cli/conversations')
D='/sdcard/WIKI_ARCHIVE_2026-11-03/05_CONVERSATIONS/agy'
tier1=set(open(D+'/tier1_ids.txt').read().split())
with open(D+'/index.csv','w',newline='',encoding='utf-8') as fi:
    w=csv.writer(fi); w.writerow(['conversation_id','tier','bytes','occurrences','mtime','exported'])
    for db in sorted(glob.glob(C+'/*.db')):
        cid=os.path.basename(db)[:-3]
        size=os.path.getsize(db); mtime=os.path.getmtime(db)
        if cid in tier1:
            con=sqlite3.connect(f'file:{db}?mode=ro',uri=True); con.row_factory=sqlite3.Row
            out=[]
            for (tname,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
                for r in con.execute(f'SELECT * FROM "{tname}"'):
                    out.append({'table':tname,'row':dict(r)})
            with open(f'{D}/tier1_strong/{cid}.jsonl','w',encoding='utf-8') as f:
                for o in out: f.write(json.dumps(o,ensure_ascii=False)+'\n')
            con.close()
            w.writerow([cid,'tier1',size,'','' ,'yes'])
        else:
            w.writerow([cid,'tier2',size,'','','metadata-only'])
print('tier1 done')
PY
```
- **الحجم المتوقع:** أعلى 15 وحدها ~54M خام — نصّها (JSON فقط) أقل بكثير. الحد الأعلى 30M. **إذا تجاوز:** تقلص tier1 إلى ≥20 occurrences فقط ثم ≥50.
- **يستثنى ولماذا:** ملفات `brain/` الستة (0.04M — تُنسخ رغم ذلك لأنها تافهة) · `log/` 1.1M بلا مطابقات · `~/.gemini/tmp` (فارغ) · **عدم نسخ أي `.db` كملف** (استخراج نص فقط).

### 05d — تصدير OmniRush (64M) — «omnirush 468»
- **الصيغة:** **JSONL** أصلاً (المصدر jsonl) + استخراج JSONL من sqlite لـ95 جلسة جديدة + **index.csv** موحّد.
- **الترشيح:** الـ468 «موضوع ويكي» فقط (وليس 816 بأي ذكر — كثافة أعلى).
  - 373 من `~/.omnirush/agent/sessions/*.jsonl` (موضوع) — مرتبة تنازلياً بـ`occurrences` حتى حد الميزانية.
  - 95 جديدة من القاعدة النشطة (غير موجودة في jsonl) → استخراج.
  - 33 من backup ⊆ jsonl + 7 من `BACKUP_OMINIRUSH_CHAT` ⊆ jsonl → **لا استخراج**، تُسجَّل `covered_by`.
  - 1 جلسة `wikillm` الصريحة (`ses_e81921099ffebArD7mwDNRJZnB`) + سطر `prompt-history.jsonl` → إلزامي.
- **الأوامر:**
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03; D="$A/05_CONVERSATIONS/omnirush"; mkdir -p "$D"/{jsonl_topic,db_extracted}
# (0) فحص أعمدة ملف الترتيب الجاهز
python3 -c "import json;r=json.load(open('/tmp/opencode/wiki_rows.json'));print(r[0].keys(),len(r))"
# (1) نسخ حسب الترتيب حتى بلوغ 55M
python3 - <<'PY'
import json,shutil,os,hashlib
D='/sdcard/WIKI_ARCHIVE_2026-11-03/05_CONVERSATIONS/omnirush/jsonl_topic'
BUDGET=55*1024*1024
rows=json.load(open('/tmp/opencode/wiki_rows.json'))
# ضبط المفتاح حسب نتائج الخطوة (0): افتراض 'path' و 'occurrences' و 'wiki_topic'
rows=[r for r in rows if r.get('wiki_topic') or r.get('topic')]
rows.sort(key=lambda r:-int(r.get('occurrences') or 0))
used=0
for r in rows:
    src=r.get('path')
    if not src or not os.path.isfile(src): continue
    sz=os.path.getsize(src)
    if used+sz>BUDGET: break
    shutil.copy2(src,os.path.join(D,os.path.basename(src))); used+=sz
print('copied',used)
PY
# (2) 95 الجلسات الجديدة من القاعدة النشطة → JSONL (استخراج، لا نسخ db)
python3 - <<'PY'
import sqlite3,json,os
OUT='/sdcard/WIKI_ARCHIVE_2026-11-03/05_CONVERSATIONS/omnirush/db_extracted'
con=sqlite3.connect('file:/root/.local/share/omnirush/opencode.db?mode=ro',uri=True); con.row_factory=sqlite3.Row
# (فحص schema ثم استكمال — نفس قالب 05b)
PY
```
- **الحجم المتوقع:** ~55M jsonl + ~7M استخراج = 62M (ضمن 64M).
- **يستثنى ولماذا:** `omnirush-upload-bases` 172M (محتوى ملفات مرفوعة — ليس محادثات) · `upload-spool` 88M `.zst` · `backup-v1/opencode.db` 446M (مطابق عددياً للنشط — استخراج فقط) · `~/.cache/omnirush` 177M · `~/.config/omnirush` 63M · `agent/sessions` غير الموضوعية (≈1033 ملف).

### 06_CODE_TOOLS (26M)
- **المصادر:** `/root/r/NEXUS_REFERENCES/llm-wiki-compiler` (16M) · `/root/r/NEXUS_REFERENCES/llm-wiki-plugin` (9.1M).
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03
(cd /root/r/NEXUS_REFERENCES/llm-wiki-compiler && find . -type f ! -path '*__pycache__*' ! -name '*.pyc' -print0 | tar --null -cf - -T -) | tar -xf - -C "$A/06_CODE_TOOLS/llm-wiki-compiler" --strip-components=0
mkdir -p "$A/06_CODE_TOOLS/llm-wiki-compiler" "$A/06_CODE_TOOLS/llm-wiki-plugin"
(cd /root/r/NEXUS_REFERENCES/llm-wiki-plugin && find . -type f ! -path '*/.git/*' ! -path '*node_modules*' ! -path '*__pycache__*' ! -name '*.pyc' -print0 | tar --null -cf - -T -) | tar -xf - -C "$A/06_CODE_TOOLS/llm-wiki-plugin"
```
- **يستثنى:** `.git` · `node_modules` · `__pycache__` (تضخّم بلا قيمة).

### 07_ENRICHMENT_CORE (8M)
- **المصدر:** `/root/r/nexus_enrichment` (209M) — نواة فقط.
```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03; S=/root/r/nexus_enrichment; D="$A/07_ENRICHMENT_CORE"
du -sh "$S"/* | sort -h   # فحص أولي إلزامي — يُستثنى أي مجلد يرفع الإجمالي فوق 8M
cp -r "$S/control" "$D/" 2>/dev/null || true
mkdir -p "$D/wiki_routing"
(cd "$S/wiki_routing" 2>/dev/null && find . -type f \( -name '*.md' -o -name '*.json' \) -size -500K -print0 | tar --null -cf - -T -) | tar -xf - -C "$D/wiki_routing/" || true
find "$S/reports" -name '*.md' -size -1M -exec cp {} "$D/reports_subset/" \; 2>/dev/null || true
du -sh "$D"; [ $(du -sm "$D"|cut -f1) -gt 8 ] && echo "OVER_BUDGET - استعلم قبل المتابعة"
```
- **يستثنى:** `state/runs` (تشغيلات وسيطة) · `knowledge` الكبير (يُؤشَّر) · أي ملف >1M.

---

## 3. ترتيب التنفيذ (الأصغر/الأهم أولاً — sdcard ممتلئ)

| # | المرحلة | المحتوى | حجم | شرط البدء | التحقق قبل المتابعة |
|---|---|---|---|---|---|
| 0 | Preflight | mkdir الهيكل + نسخ التقارير الستة + `df` مسجّل | ~1M | — | `df` ≥ 640M |
| 1 | `00_INDEXES` | CSVs + hashes | 2M | مرحلة 0 | الملفات الأربعة موجودة |
| 2 | `01_SDCARD_DOCS` | wikillm + skills + root files | 9.5M | 1 | `du -sm ≤ 10` |
| 3 | `02_ROOT_DOCS` | سجلات جلسات + معمارية + hubs | 4M | 1 | `du -sm ≤ 6` |
| 4 | `05a claude` | 14 jsonl + history + digest | 9M | 1 | `index.csv` = 15+ صفاً |
| 5 | `03_WIKI_LAYERS` | طبقات بدون gz | 11M | 2–4 | `du -sm ≤ 12` + لا `*.gz` في الأرشيف |
| 6 | `05b opencode` | استخراج 51 جلسة → JSONL | 25M | فحص schema | عدد JSONL = 50 (51−1 مكرر) |
| 7 | `07_ENRICHMENT_CORE` | نواة control/routing | 6M | 1 | `du -sm ≤ 8` |
| 8 | `04_NEXUS_CORE` | أقسام بدون raw/ledger | 30M | 2 | `du -sm ≤ 32` + `BIG_FILE_POINTERS.csv` ممتلئ |
| 9 | `06_CODE_TOOLS` | compiler + plugin نظيفان | 24M | 1 | `du -sm ≤ 26` |
| 10 | `05c agy` | tier1 JSONL + tier2 index | 30M | فحص schema | `du -sm ≤ 34` |
| 11 | `05d omnirush` | jsonl مرتب + استخراج 95 | 62M | فحص wiki_rows | `du -sm ≤ 64` |
| 12 | Finalize | MANIFEST.json + كل READMEs + `hashes.sha256` + `FALLBACK.md` | 1M | كل ما سبق | `du -sm الأرشيف ≤ 250` و `df ≥ 30M` |

**قواعد مرورية بين المراحل:**
1. `df -h /mnt/sdcard` بعد **كل** مرحلة → إن Available < 30M: إيقاف + تفعيل §7.
2. `du -sm <folder>` بعد كل مرحلة → إن تجاوز ميزانيته: **لا نحذف** (ممنوع) بل نُوقَف قبل المرحلة التالية ونطبّق fallback على المراحل المتبقية فقط.
3. لا مرحلة تبدأ قبل ختم السابقة (لأن الإضافة فقط — لا يمكن التراجع بالحذف).

---

## 4. خطة تصدير المحادثات (الملخص التنفيذي)

| المصدر | العدد | الصيغة | الترشيح | الحجم الخام | الحجم المتوقع | الفهرس |
|---|---|---|---|---|---|---|
| **Claude** | 14 ملف + history | JSONL خام + digest MD | القائمة الجاهزة في التقرير + grep على history | 9.0M | **~9–10.5M** | `index.csv` + digest |
| **OpenCode** | 44 + 7 = 51 جلسة | JSONL/جلسة | **النطاق A فقط** (عنوان مطابق) — لا B | 23.2M | **~25M** | `index.csv` |
| **AGY** | 168 ملف → 90 tier1 + 85 tier2 | JSONL (tier1) / metadata (tier2) | ≥5 occurrences أو عنوان صريح | ~54M (أعلى 15) | **≤30M** | `index.csv` + `digest.md` لأعلى 15 |
| **OmniRush** | 468 موضوع | JSONL (373 ملف) + استخراج (95) | «موضوع ويكي» فقط، مرتّب بـoccurrences | ~67M+ | **≤62M** | `index.csv` |
| **الإجمالي** | ~678 كائناً | | | | **≤ 126M** من أصل 126M مخصصة (05a–05d) | فهرس موحّد في `00_INDEXES/conversations_index.csv` |

**مبدأ موحّد لجميع الأربعة:** كل جلسة ملف JSONL واحد بسطور `{...}` + سطر أول `{"_meta":{session_id,title,source_db,exported_at,occurrences}}` + CSV فهرس بعمود `dedup_group` لعكس التكرارات الموثّقة (fork المتطابق، backup ⊆ jsonl،覆盖_by).

---

## 5. ملفات README المطلوبة (القائمة + مخطط المحتوى)

| # | الملف | المحتوى المخطط |
|---|---|---|
| 1 | `README.md` (الجذر) | ① عنوان + تاريخ + قيود التنفيذ ② شجرة الأرشيف ③ جدول الميزانية (فعلي/مخطط) ④ حالة كل مرحلة (✅/⏳) ⑤ روابط لكل README فرعي ⑥ كيف التحقق من MANIFEST |
| 2 | `00_INDEXES/README.md` | ① وصف ملفات CSV ② قواعد التصنيف (category/tier) ③ تعريف excluded_files ④ طريقة إعادة بناء hashes |
| 3 | `01_SDCARD_DOCS/README.md` | ① جدول المصدر→الوجهة لكل نسخة ② لماذا wikillm كامل ③ قائمة zips ونسخ الويكي الثلاث المُستثناة مع hash |
| 4 | `02_ROOT_DOCS/README.md` | ① أربعة سجلات جلسات + أيها مكرر (wiki vs wiki.md) ② لماذا استُثني nexus_enrichment الكامل ③ حالة V3 |
| 5 | `03_WIKI_LAYERS/README.md` | ① لماذا نُسخ nexus_wiki كامل وwiki جزئياً ② جدول BIG_FILE_POINTERS (17M×2) ③ كيف إعادة توليد الفهرس من المصدر |
| 6 | `04_NEXUS_LLM_WIKI_CORE/README.md` | ① جدول (قسم / مصير / سبب) ② raw=53M مُستثنا ③ خريطة collections_filtered ④ خطوات استعادة raw لاحقاً |
| 7 | `05_CONVERSATIONS/README.md` (الوالد) | ① مقارنة المصادر الأربعة (العدد/الصيغة/النطاق) ② قاعدة «لا نسخ db — استخراج فقط» ③ جدول dedup المعتمد |
| 8 | `05_CONVERSATIONS/claude/README.md` | ① قائمة ال14 ملفاً بمساراتها الأصلية ② فلتر history ③ كيف يُقرأ digest.md ④ سبب خيار JSONL |
| 9 | `05_CONVERSATIONS/opencode/README.md` | ① النطاق A مقابل B ولماذا A ② snapshot schema ③ الجلسة المكررة وكيفية covered_by ④ أمر إعادة الاستخراج |
| 10 | `05_CONVERSATIONS/agy/README.md` | ① tier1/tier2 والمعايير ② ذروة 2026-10-25 ③ brain 6 ملفات ④ لماذا لا نسخ .db |
| 11 | `05_CONVERSATIONS/omnirush/README.md` | ① معادلة ال468 (373+95+0) ③ ملفات الترتيب الجاهزة `/tmp/opencode/*.json` ④ upload-* المستثناة ⑤ جلسة wikillm الوحيدة |
| 12 | `06_CODE_TOOLS/README.md` | ① فرق compiler/plugin ② ما حُذف (git/node_modules — لا: *مُستثنا*) ③ أمثلة أوامر wiki-* المدعومة |
| 13 | `07_ENRICHMENT_CORE/README.md` | ① علاقته بـ04 ② ما لم يُنسخ من 209M ولماذا ③ routing structure |
| 14 | `_RESERVE/README.md` | ① الغرض (تنفّس/طوارئ) ② متى يُستخدم فقط ③ سقف الصرف |
| 15 | `FALLBACK.md` | سلّم §7 كاملاً (يُنسخ من هذا الملف) |
| 16 | `RISKS.md` | جدول §8 كاملاً |
| 17 | `EXPORT_NOTES.md` | أوامر الاستخراج الأربعة كاملة + نتائج فحص schema بعد التنفيذ |

---

## 6. `MANIFEST.json` — البنية (schema)

```json
{
  "$schema": "wiki-archive-manifest/1",
  "archive_name": "WIKI_ARCHIVE_2026-11-03",
  "created_at": "2026-11-03T00:00:00Z",
  "budget_mb": 250,
  "used_mb": 0,
  "constraints": {
    "add_only": true,
    "db_copy_max_mb": 50,
    "sdcard_available_at_start_mb": 646
  },
  "reports": [
    "/root/r/SDCARD_WIKI_INDEX_REPORT.md",
    "/root/r/WIKI_INDEX_REPORT.md",
    "/root/r/WIKI_CONVERSATION_SCAN_REPORT.md",
    "/root/r/OPencode_DB_WIKI_SCAN_REPORT.md",
    "/root/r/AGY_WIKI_CONVERSATIONS_SCAN_REPORT.md",
    "/root/r/OMNIRUSH_WIKI_CONVERSATIONS_SCAN_REPORT.md"
  ],
  "entries": [
    {
      "id": "ARC-000001",
      "archive_path": "01_SDCARD_DOCS/wikillm/BUILD_PROTOCOL.md",
      "source_path": "/sdcard/wikillm/BUILD_PROTOCOL.md",
      "category": "docs | layers | core | conversation | code | index | enrichment",
      "source_kind": "file | dir_tree | sqlite_extract | jsonl_filter",
      "tier": "P0 | P1 | P2",
      "source_size": 32768,
      "archive_size": 32768,
      "sha256_archive": "…",
      "sha256_source": "…",
      "exported_at": "2026-11-03T…Z",
      "export_tool": "cp | tar-find | sqlite3+python3 | grep",
      "dedup_group": null,
      "covered_by": null,
      "conversation": {
        "source_system": "claude | opencode | agy | omnirush",
        "session_id": null,
        "title": null,
        "occurrences": null,
        "date_range": null
      },
      "notes": ""
    }
  ],
  "exclusions": [
    {
      "source_path": "/sdcard/wiki/03_WIKI_V3_STRUCTURED/04_SEARCH/index.json.gz",
      "size": 17825792,
      "sha256": "…",
      "reason": "duplicate_heavy_file",
      "reason_code": "DUP | HEAVY | RAW_DB | NOISE | GENERATED",
      "pointer_file": "03_WIKI_LAYERS/BIG_FILE_POINTERS.csv"
    }
  ],
  "stage_log": [
    {"stage": 1, "name": "00_INDEXES", "status": "pending", "df_after_mb": null, "du_mb": null}
  ]
}
```

**قواعد الملء:** (1) كل ملف داخل الأرشيف = entry واحد إلزامي · (2) `sha256_archive == sha256_source` بعد كل cp (فشل ≠ تسجيل) · (3) التكرارات: `dedup_group` يشير لـid الأول و`covered_by` لمساره · (4) `exclusions` تسجّل كل ما قُرر ألا يُنسخ مع hash (لأن لا نحذف ولا نعيد فحص لاحقاً) · (5) `stage_log` سجل df/du بعد كل مرحلة.

**أداة التوليد (تُكتب في مرحلة 12):**
```bash
python3 /root/r/tools/archive_manifest.py --archive /sdcard/WIKI_ARCHIVE_2026-11-03 \
  --sources-map /root/r/00_INDEXES/source_inventory.csv --write
# تُنفَّذ: find الأرشيف → sha256 لكل ملف → مطابقة بالمسار الأصلي من source_inventory → كتابة MANIFEST.json
```

---

## 7. خطة Fallback — نفاد المساحة (الأولوية: وثائق > محادثات نصية > نصوص مكتملة > ملفات ثقيلة)

**المشغّل:** Available < 30M بعد أي مرحلة، أو تجاوز مجلد ميزانيته.

| الخطوة | الإجراء | التوفير التقديري | يُطبَّق على |
|---|---|---|---|
| **F0** | إيقاف فوري — لا تبدأ مرحلة جديدة | — | — |
| **F1** | `05d omnirush`: توقّف نسخ الـjsonl عند 55M→35M (الأعلى occurrences فقط) + استخراج 95→20 الأعلى | ~27M | omnirush |
| **F2** | `05c agy`: تقليل tier1 إلى ≥50 occurrences + 18 صريحة فقط؛ الباقي metadata في index | ~15M | agy |
| **F3** | `06_CODE_TOOLS`: الاحتفاظ بـ`*.py *.md *.json` فقط (تجاهل الباقي) | ~8M | code |
| **F4** | `04_NEXUS_CORE`: إسقاط `staging_manifests` + `sources_filtered` + `claims_filtered` (يبقى reports/systemes/indexes/charter) | ~10M | core |
| **F5** | `03_WIKI_LAYERS`: الاحتفاظ بـnexus_wiki فقط + pointer لـ`/sdcard/wiki` | ~4M | layers |
| **F6** | `05b opencode`: تصدير أعلى 20 جلسة حجم parts فقط (44→20) | ~13M | opencode |
| **F7** | `06` يُلغى كاملاً من الأرشيف (pointer للمسار الأصلي في `excluded_files.csv`) | ~24M | code |
| **F8** | `05c/05d` يُلغيان كاملاً — تبقى index.csv metadata فقط | ~50M | conv |
| **⚠️ الحد الأدنى المحمي (لا يُمس أبداً)** | `00` + `01` + `02` + `05a claude` + READMEs + MANIFEST + التقارير الستة ≈ **~25M** | — | docs |

**الترتيب المنطقي للفشل:** تُخصم الخطوات من الأحدث/P2 أولاً (F1→F2) ثم من الأثقل قيمةً نسبياً (F3→F8) — **الوثائق (00–02) لا تُلغى في أي سيناريو**.

---

## 8. جدول المخاطر + الإجراء

| # | الخطر | الاحتمال | الأثر | الإجراء الوقائي/العلاجي |
|---|---|---|---|---|
| R1 | نفاد الـ646M أثناء النسخ | عالٍ | حرج | `df` بعد كل مرحلة · سقف توقف 30M · سلّم §7 · مرتبة الأصغر أولاً |
| R2 | **عدم القدرة على الحذف** (add-only) — أي خطأ يبقى للأبد | عالٍ | حرج | لا staging مؤقت: اكتب للمسار النهائي مباشرة · تحقق `du`+hash فوراً · لا تجرب على الأرشيف |
| R3 | قاعدة opencode/omnirush نشطة تتغير أثناء الاستخراج | متوسط | متوسط | `mode=ro` · تسجيل timestamp في `exported_at` · تصدير بجلسة استعلامات واحدة متسلسلة · قبول انحراف بسيط مع توثيقه |
| R4 | نسخ db كامل بالخطأ (>50M) | متوسط | حرج | ممنوع `cp *.db` نهائياً — لا يُسمح إلا `sqlite3 … mode=ro` + استخراج نص · راجع `excluded_files.csv` قبل كل مرحلة db |
| R5 | تكرار يضاعف الحجم (17M×2، 3×23M، zip 45M×2، IGWIKI×2) | مؤكد | حرج | hash-تجميع: `sha256` قبل النسخ · `covered_by` في MANIFEST · استثناءات موثّقة |
| R6 | تجاوز ميزانية مجلد فرعي | متوسط | متوسط | `du -sm` بوابة خروج من كل مرحلة · توقّف بدل متابعة |
| R7 | schema غير موثّق لـAGY db (التقرير لم يسجل الجداول) | مؤكد | متوسط | مرحلة فحص إلزامية (`.tables`/`.schema`) قبل أي استخراج · `EXPORT_NOTES.md` يُحدَّث بالنتائج |
| R8 | ملف `wiki_rows.json` في `/tmp` قد يُمسح (tmp) | متوسط | متوسط | المرحلة 0: `cp` نسخة من `/tmp/opencode/*.json` إلى `00_INDEXES/raw_analysis/` فوراً |
| R9 | مسارات عربية/مسافات/ملفات طويلة | متوسط | منخفض | `find -print0` · `tar --null -T -` · عرض كل المسارات بين علامتي تنصيص |
| R10 | فشل grep الشامل بمهلة (حدث سابقاً 180s) | مؤكد | منخفض | لا إعادة فحص شامل — نعتمد قوائم التقارير الجاهزة + فحص موجّه فقط |
| R11 | تلف/انقطاع cp جزئي (电源/ذاكرة) | منخفض | متوسط | تحقق بعد كل cp: `sha256` المصدر == الوجهة · إعادة cp للمسار نفسه مسموحة (overwrite وليس حذف) |
| R12 | مساحة 646M تقل قبل بدء التنفيذ (استخدام آخر) | متوسط | حرج | Preflight `df` · إن < 500M: تنفيذ 00+01+02+05a فقط ثم fallback فوري |
| R13 | اختلاط محادثات non-wiki داخل tier واسع (ضوضاء) | مؤكد | منخفض | الاعتماد على «موضوع» لا «أي ذكر» (468 لا 816 · A لا B) · عمود `occurrences` للفلترة اللاحقة |
| R14 | `_RESERVE` يُستهلك ثم يتراجع الأرشيف دون مساحة | متوسط | منخفض | `_RESERVE` لا يُصرف إلا بأمر صريح · رصيده محسوب خارج المراحل |

---

## 9. الأوامر العامة الموحّدة (تُشغَّل في كل مرحلة)

```bash
A=/sdcard/WIKI_ARCHIVE_2026-11-03
stage_gate() {  # يستدعى بعد كل مرحلة
  local n="$1" cap="$2"
  df -h /mnt/sdcard | tail -1 | tee -a "$A/00_INDEXES/stage_log.txt"
  local avail=$(df -m /mnt/sdcard | awk 'NR==2{print $4}')
  local used=$(du -sm "$A" | cut -f1)
  echo "stage=$n archive_used=${used}M avail=${avail}M cap=${cap}M" | tee -a "$A/00_INDEXES/stage_log.txt"
  [ "$avail" -lt 30 ] && { echo "STOP: FALLBACK F0"; return 1; }
  [ "$used" -gt $(( cap + 2 )) ] && { echo "STOP: over stage cap"; return 1; }
  return 0
}
```

---

## 10. قائمة المخرجات المتوقعة (بعد التنفيذ)

- أرشيف ≤ **250M** (متوقع **~232M**) داخل `/sdcard/WIKI_ARCHIVE_2026-11-03/`.
- **678+** كائناً موثّقاً في `MANIFEST.json` (ملفات + استخراجات محادثات).
- **~678 محادثة/ملف** مصنّفة عبر 4 أنظمة (14+51+168+468 — مع dedup).
- **17** ملف README.
- **0** حذف · **0** نسخ db كامل · **0** تجاوز 250M.

---
*خطة تخطيطية — قراءة التقارير الستة فقط، لم يُنفَّذ أي نسخ أو حذف.*
