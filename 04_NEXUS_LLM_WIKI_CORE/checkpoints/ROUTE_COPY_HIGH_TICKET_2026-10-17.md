# Checkpoint — route + copy high-ticket — 2026-10-17

## الحالة

- **source_id:** `SRC_NEW_b0140a4d41654bab_b1f4775a`
- **route_status:** `route_done`
- **source_extraction_status:** `not_started`
- **primary:** `sales/high_ticket_closing`
- **النطاق:** مصدر واحد؛ route + copy فقط، وليس snapshot كاملة للمجال.
- **التقرير:** `reports/route-copy-high-ticket-2026-10-17.md`
- **manifest التشغيلي:** `staging/routing/ROUTE_RUN_20261017_HIGH_TICKET.json`

## ما تم إثباته

- قُرئ raw الحالي كاملًا: `30,707/30,707` bytes، UTF-8 strict، EOF، سطر واحد،
  `30,707` Unicode code points، و`decode_replacements=0`.
- SHA-256 الحالي: `sha256:b0140a4d41654babf5ec880c63fa0da5e68ff72a8a2e5611a4b5652b31bb0d54`؛
  مطابق لسجل القراءة القديم بعد إعادة التحقق، لا اعتمادًا عليه وحده.
- التغطية المتصلة: `[0,10235)+[10235,20471)+[20471,30707)`؛ بلا فجوات أو overlap.
- الاقتباسات ذات locators من المتن: **5/5 exact** مع hash مطابق.
- النسخة المباشرة regular byte-exact: `30,707` bytes، نفس SHA-256،
  `symlink=false`، `hardlink=false`، `same_inode=false`، و`st_nlink=1` للطرفين.
- `REF_...json` و`ROUTE_...md` و`INDEX.md` المحلي موجودة؛ لا parent index تعدّل.
- لا Terms/Claims/Concepts/Masters منشأة أو مرتبطة؛ refs المعرفية في REF كلها `[]`.

## raw pre/post

الجرد استخدم `os.walk(followlinks=False)` و`lstat` وSHA-256 للملفات؛ بصمة الشجرة
أسطر JSON مرتبة من `(relative_path,type,size/hash)`.

| الجذر | pre | post | الحكم |
|---|---|---|---|
| `raw/` | `1833 entries / 1820 regular / 0 symlink / 13 other / 50,898,163 bytes / 5a18a1e3be5c8ac735be3d36197e71a2247afbca3763ab66fa0f839b111fb881` | نفس القيم والبصمة | **UNCHANGED** |
| `raw/new/` | `1776 files / 43,757,343 bytes / 47739e2830fd37cf47e97862bb2d3d10d6556c6c65fabfa2dbf72c5e91cd4c29` | نفس القيم والبصمة | **UNCHANGED** |

## قيود ظاهرة

- سجل `raw/SOURCE_MANIFEST.tsv:780` يربط نفس البصمة بمسار legacy مفقود؛ سُجل
  `stale_legacy_manifest_reference` ولم يُخفَ أو يُحسب duplicate نشطًا.
- سجل Source التاريخي يقرأ `processed` ولم يُعدّل؛ REF يوضح أن حالة workflow
  للتوجيه `new` وأن `processed` التاريخية ليست source_done.
- لا independent reviewer منفصل مُدّعى؛ التحقق self-check من Worker.
- لم تُعدّل `raw/` أو manifests القائمة (`collections/sales/manifest.json`،
  `collections/corpus/manifest.jsonl`، `raw/SOURCE_MANIFEST.tsv`) أو `config/*`
  أو parent indexes؛ سجلات route الجديدة فقط تحت `staging/routing/`.
- لا توجد مطالبة بـ`source_done` أو `domain_done` أو T/C/K/M/QA.

## أوامر التحقق الأساسية

```text
python3 tools/wiki_workflow.py validate-batch --manifest staging/routing/ROUTE_RUN_20261017_HIGH_TICKET.json --json
```

النتيجة: **PASS** — `ok=true`, `valid_entries=1`, `knowledge_requested=false`,
`writes_performed=0`, `errors=[]`.

```text
python3 -m json.tool staging/routing/ROUTE_RUN_20261017_HIGH_TICKET.json
python3 -m json.tool done/sales/high_ticket_closing/REF_SRC_NEW_b0140a4d41654bab_b1f4775a.json
```

النتيجة: **PASS**؛ أُعيد أيضًا فحص slices والـhash و`lstat` وraw post-scan.

```text
python3 tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --json
```

النتيجة: **PASS** في نطاق الفحص المساعد (`ok=true`, `errors=[]`)؛ لا يُعامل
كبديل عن فحص route/copy الموضعي.

## الخطوة التالية

تبقى أي قراءة extraction أو إنشاء Terms/Claims أو مراجعة بوابات T/C/K/M/QA
خارج هذا checkpoint وتحتاج تكليفًا منفصلًا؛ لا يُفهم `route_done` كإذن لها.
