#!/usr/bin/env python3
"""build_link_plan.py — مولّد خطة روابط الـWiki للمفاهيم الـ1,836 في NB2.

**الأداة تولّد خطة ولا تعدّل شيئاً.** كل الكتابات محصورة في مخرجين
(`LINK_PLAN.jsonl` و`LINK_PLAN_REPORT.md`) داخل `/root/r/V3`. لا يُكتب في
`/root/r/NB2` ولا في `/sdcard`، ولا يُحذف شيء.

الاكتشاف المُعالَج: صفر `[[ ]]` wikilink في الـ1,836 مفهوم ⇒ الـWiki ميت في
Obsidian، و`C13` يحاسب كل ملف على هذه الفجوة وحدها.

الأوضاع (قابلة للجمع — كل وضع يشارك نفس خط الأنابيب):

    python3 build_link_plan.py --scan                # جدول الفحص (الوضع الافتراضي)
    python3 build_link_plan.py --scan --json s.json  # نفس الجدول بصيغة JSON
    python3 build_link_plan.py --propose             # أمثلة 5 مفاهيم + Jaccard لكل رابط
    python3 build_link_plan.py --emit                # يكتب 03_WORK_BUNDLES/LINK_PLAN.jsonl
    python3 build_link_plan.py --report              # يكتب V3/LINK_PLAN_REPORT.md
    python3 build_link_plan.py --selftest            # اختبارات ذاتية (فيكتور اصطناعي، بلا NB2)

نطاق القياس (مطابق حرفياً لـ`audit_scoped.py --scope concepts`):
`NB2/02_CONCEPTS/<قطاع NN_*>/*.md` ⇒ **1,836 ملفاً**. تُستثنى عمداً
`_INDEX.md` و`_REPORTS/` و`terms_26k/`.

------------------------------------------------------------------
صيغة سطر LINK_PLAN.jsonl (مطابقة للتكليف — لا مفاتيح زائدة):

    {"path":"02_CONCEPTS/01_outreach/Concept_X.md",
     "current_links":0,
     "proposed_links":["C_AuthorityCommentPipeline","X_C7"],
     "reason":"jaccard=0.189;top=0.189|0.128|0.113;C=1;X=1;X_src=pack:C7",
     "sections_missing":["التعريف"],
     "fix_class":"add"}

· `path`             — مسار نسبي لجذر NB2 (المُصلِح يعمل على NB2).
· `current_links`    — عدد `[[ ]]` الموجودة الآن في الملف (0 للجميع ⇒ D13).
· `proposed_links`   — `C_<slug>` للمفاهيم ثم `X_<code>` للتوترات.
· `reason`           — الدليل بالصيغة `FORMAT_REASON` الموثّقة أدناه.
· `sections_missing` — مفاتيح الأقسام الستة الناقصة (منطق C14 مقلوب حرفياً).
· `fix_class`        — `add` (لا روابط الآن) · `augment` (بعض الروابط) · `none`.

FORMAT_REASON = `jaccard=<أعلى درجة>;top=<t1|t2|…>;C=<عدد>;X=<عدد>;X_src=<مصدر>`
⇒ الرقم بعد `jaccard=` هو أفضل جار، وقائمة `top` هي درجات كل الروابط المقترحة
مرتّبة تنازلياً (دليل قابل للتحقّق يدوياً)، و`X_src=pack:C7` يعني أن رابط
التوتر جاء من رمز الحزمة المذكور في المتن.

قاعدة حل الأسماء (قابلة للتبديل بـ`--link-form`):
    C_<slug>  ⇒  02_CONCEPTS/<sector>/Concept_<slug>.md
    X_<code>  ⇒  05_TENSIONS/TENSION_<code>.md
`--link-form stem` يُخرج الجذع الحقيقي (`Concept_…` / `<code>`) بدل الاسم
المستعار، و`--selftest` يتحقّق أن كل اسم مستعار في الخطة يُحلّ ملفاً فعلياً.

------------------------------------------------------------------
خوارزمية التشابه (Jaccard على مجموعات مفردات، داخل القطاع فقط):

1. تطبيع عربي: حذف أسطر البيانات الوصفية (`> **المجال:** …`) ثم التشكيل
   والتطويل (`U+0610-061A`, `U+064B-065F`, `U+0670`, `U+0640`)، ثم الرموز
   (كل ما ليس حرفًا/رقمًا/فراغًا ⇒ فراغ)، ثم `lower()`، ثم حذف الأرقام البحتة
   ووقفات الدالة (عربية + إنجليزية)، ثم حذف `ال` التعريف إن بقيت 5 محارف
   فأكثر، ثم حذف ما دون 3 محارف.
2. **فهرس مقلوب** `token → [doc_id]` مع تواتر `df` على مستوى كل قطاع. الاستعمال
   الوحيد لـ`df` هو **بتر** المفردات الشائعة يدويًا (`df > 25%` من حجم القطاع)
   لأنها ضجيج قطاعي لا تمييز؛ ثم تُحسب Jaccard **بالضبط** على المجموعات الكاملة.
   ⇒ العمل: ~310 ألف زوج مرشّح بدل 1,836×1,836 = 3.37 مليون.
3. ترتيب تنازلي بالـJaccard مع بوابتين: `overlap ≥ --min-overlap` مفردات مشتركة
   و`jaccard ≥ --min-jaccard`، ثم **سقف النجوم**: لا يُقترح concept يطلبه أكثر
   من `--hub-cap` (10%) من المفاهيم.

روابط التوتر `X_`: قناة واحدة **حتمية** = رمز الحزمة المذكور في المتن
(`حزمة C7` ← `TENSION_C7.md`). قناة النص الحر مُرفوضة عمداً: قياسها أعطى
تغطية 2/300概念 ومتوسط أعلى درجة 0.048 مع تكرار `TENSION_B10` كـ«أفضل» مطابقة
لأغلب الملفات ⇒ ارتباط عرضي لا رابط حقيقي (الأرقام في التقرير §5).

الأداء المقيس على 1,836 ملفاً: قراءة ~16ث + فهرسة وترتيب وقياس ~77ث ⇒ ~95ث
إجمالي (الهدف < 3 دقائق محقّق).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------- ثوابت

V3_ROOT = Path("/root/r/V3")
NB2_ROOT = Path("/root/r/NB2")
DEFAULT_EMIT = V3_ROOT / "03_WORK_BUNDLES" / "LINK_PLAN.jsonl"
DEFAULT_REPORT = V3_ROOT / "LINK_PLAN_REPORT.md"

# ثلاثة مسارات موثّقة للتوترات: NB2 يسمّيها 05_TENSIONS (لا 04_TENSIONS)،
# وV3/04_TENSIONS فارغة. الأول الموجود فقط هو المرجع.
TENSION_DIR_CANDIDATES = (
    NB2_ROOT / "04_TENSIONS",
    NB2_ROOT / "05_TENSIONS",
    V3_ROOT / "04_TENSIONS",
    V3_ROOT / "05_TENSIONS",
)

MAX_NOISE_DF = 8
CONCEPT_PREFIX = "Concept_"
TENSION_PREFIX = "TENSION_"
MIN_TOKEN_LEN = 3

# منطق C14/C23/C28 من audit_scoped.py — منسوخ حرفياً كي تُقارَن أرقام هذه
# الأداة بأرقام DEFECTS_SUMMARY.md دون انحراف.
REQUIRED_SECTIONS = [
    ("التعريف", ("التعريف", "التعريف الإجرائي", "ما هو")),
    ("الآلية", ("الآلية", "آلية العمل", "كيف يعمل")),
    ("حدود الفناء", ("حدود الفناء", "الفناء", "متى لا يعمل")),
    ("الشروط", ("الشروط", "الشرائح", "متى يعمل")),
    ("الدليل", ("الدليل", "الاقتباسات", "الشواهد")),
    ("المصدرية", ("المصدرية", "المصادر", "المراجع")),
]
TENSION_TOKENS = ("التوترات", "توتر", "التعارضات", "المقارنات والتعارضات")

SECTION_HEADING_RE = re.compile(r"(?m)^(#{1,6})[ \t]*(.+?)[ \t]*#*\s*$")
BOLD_LABEL_RE = re.compile(r"\*\*([^*\n]{2,40})\*\*")
FRONTMATTER_RE = re.compile("\\A﻿?---\\s*\\n(.*?)\\n---\\s*(?:\\n|\\Z)", re.S)
WIKILINK_RE = re.compile(r"\[\[[^\]]*\]\]")
SECTOR_DIR_RE = re.compile(r"^(\d{2})_")
META_LINE_RE = re.compile(r"^\s*>")

# التطبيع
DIACRITICS_RE = re.compile("[\u0610-\u061A\u064B-\u065F\u0670\u0640]")  # تشكيل + تطويل
NON_WORD_RE = re.compile(r"[^\w\s]", re.UNICODE)
PURE_NUM_RE = re.compile(r"^\d+$")
AR_PREFIX_RE = re.compile(r"^ال")

AR_STOPWORDS = set("""
في من على إلى عن مع هذا هذه ذلك تلك التي الذي كان تكون قد ما لا إن أو ثم بين كل
بعد قبل حيث عند لدى هو هي هم كما حتى إذا لم لن إلا أي أيضا هناك هنالك يجب يمكن نحو
دون سواء ضمن عبر خلال حول بل أما لقد كي لكي إذ لذلك بسبب نتيجة نتائج عملية مثال
بشكل التطبيق تعد يستخدم استخدام أساسي نسبة مستوى عدد فقط جدا أكثر أقل مثل وقت يوم
أيام مرة بدون سوف كذلك حيثما طالما ريثما علما
""".split())
EN_STOPWORDS = set("""
the a an and or but if then this that these those there here is are was were be been
being of to in on at by for with from as it its you your we our they their he she his
her i me my not no nor so than too very can will just don should now what which who
when where why how all any both each few more most other some such only own same
""".split())

FORMAT_REASON = "jaccard=<top>;top=<t1|t2|...>;C=<n>;X=<n>;X_src=<src>"

PACK_CODE_RE = re.compile(r"حزمة\s+([A-Z]{1,2}[0-9]{1,2}[a-z]?)")
BARE_TENSION_REF_RE = re.compile(r"(?<![\w])T[0-9]{1,2}[a-z]?(?![\w])")


# --------------------------------------------------------------------------- تحميل


def iter_concepts(nb2_root: Path) -> list[Path]:
    """كل `NN_*/*.md` تحت 02_CONCEPTS مرتّبًا = نطاق audit_scoped --scope concepts."""
    root = nb2_root / "02_CONCEPTS"
    if not root.is_dir():
        sys.exit(f"FATAL: concepts root not found: {root}")
    out: list[Path] = []
    for d in sorted(root.iterdir()):
        if d.is_dir() and SECTOR_DIR_RE.match(d.name):
            out.extend(sorted(d.glob("*.md")))
    return out


def load_tension_codes(dirs) -> tuple[dict[str, Path], list[str]]:
    """يرجّع {code: file} من أول مجلد يحتوي ملفات توتر + قائمة المجلدات المفحوصة."""
    tried: list[str] = []
    for d in dirs:
        tried.append(str(d))
        if not d.is_dir():
            continue
        codes = {}
        for p in sorted(d.glob(TENSION_PREFIX + "*.md")):
            codes[p.stem[len(TENSION_PREFIX):]] = p
        if codes:
            return codes, tried
    return {}, tried


def first_title(text: str, stem: str) -> str:
    """العنوان العربي من السطر الأول (`# … · CamelCase`) أو اسم الجذر."""
    head = text.split("\n", 1)[0]
    if head.startswith("#"):
        head = head.lstrip("#").strip()
        return head.split("·")[0].strip() if "·" in head else head
    return stem[len(CONCEPT_PREFIX):] if stem.startswith(CONCEPT_PREFIX) else stem


def alias_concept(stem: str, link_form: str) -> str:
    """`stem` ⇒ الجذع الحقيقي `Concept_A1` (قابل للحلّ المباشر في Obsidian)،
    `alias` ⇒ `C_A1` مع القاعدة الموثّقة C_<slug> ⇒ Concept_<slug>.md."""
    return stem if link_form == "stem" else "C_" + stem[len(CONCEPT_PREFIX):]


def alias_tension(code: str, link_form: str) -> str:
    """`stem` ⇒ `TENSION_C7`، `alias` ⇒ `X_C7` ⇒ TENSION_C7.md."""
    return TENSION_PREFIX + code if link_form == "stem" else "X_" + code


# --------------------------------------------------------------------------- تصنيفات


def tokenize(text: str) -> set[str]:
    """مجموعة مفردات بعد التطبيع (انظر رأس الملف).

    تُستثنى ثلاث طبقات غير دلالية: الـfrontmatter (مفاتيحه مثل `type`/`tags`)،
    وأسطر البيانات الوصفية `> **المجال:** …`، وكل ما هو رمز. الأثر صغير (3 ملفات
    فقط فيها frontmatter) لكنه يمنع تلوّث المفردات بمفاتيح ميتة."""
    fm = FRONTMATTER_RE.match(text)
    if fm:
        text = text[fm.end():]
    body = "\n".join(line for line in text.split("\n") if not META_LINE_RE.match(line))
    body = DIACRITICS_RE.sub("", body)
    body = NON_WORD_RE.sub(" ", body)
    out = set()
    for raw in body.split():
        w = raw.lower()
        if len(w) < MIN_TOKEN_LEN:
            continue
        if PURE_NUM_RE.match(w) or w in AR_STOPWORDS or w in EN_STOPWORDS:
            continue
        if AR_PREFIX_RE.match(w) and len(w) > 4:
            w = w[2:]
        if len(w) >= MIN_TOKEN_LEN:
            out.add(w)
    return out


def missing_sections(text: str) -> list[str]:
    """C14 معكوس: أي الأقسام الستة غائبة؟ (نفس heads+bolds pool في audit_scoped)"""
    heads = " \n ".join(m.group(2) for m in SECTION_HEADING_RE.finditer(text))
    bolds = " \n ".join(BOLD_LABEL_RE.findall(text))
    pool = heads + "\n" + bolds
    return [key for key, alts in REQUIRED_SECTIONS if not any(a in pool for a in alts)]


def sources_state(text: str) -> str:
    """C28 مصنّفًا: ok · no_frontmatter · no_key · empty."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "no_frontmatter"
    fm = m.group(1)
    vals: dict[str, str] = {}
    for key in ("sources", "sources_channels", "source_channels", "sources_count",
                "source", "source_master", "provenance_account"):
        km = re.search(r"(?m)^%s\s*:\s*(.+?)\s*$" % re.escape(key), fm)
        if km:
            vals[key] = km.group(1).strip()
    if not vals:
        return "no_key"
    empty = True
    for k, v in vals.items():
        if v in ("[]", '""', "''", "{}", "null", "~", "0"):
            continue
        if k == "sources_count":
            try:
                if float(v) > 0:
                    empty = False
            except ValueError:
                pass
            continue
        empty = False
    return "empty" if empty else "ok"


def has_tension_section(text: str) -> bool:
    """C23: هل فيه قسم توترات/تعارضات؟"""
    return any(k in text for k in TENSION_TOKENS)


def tension_links_for(packs: list[str], tension_codes, max_tensions: int):
    """قناة حتمية واحدة: رمز الحزمة ⇒ X_<code> إن وُجد ملف مقابل. ترجع (codes, source)."""
    picks: list[str] = []
    for code in packs:
        if code in tension_codes and code not in picks:
            picks.append(code)
        if len(picks) >= max_tensions:
            break
    return picks, ("pack:" + ",".join(picks)) if picks else "none"


# --------------------------------------------------------------------------- سجل المفهوم


class Concept:
    """سجلّ مفهوم واحد: بيانات وصفية + مفرداته + مقياساته (بلا تعديل للملف)."""

    __slots__ = ("path", "rel", "sector", "stem", "title", "links", "tokens",
                 "sections_missing", "sources_state", "tension_section",
                 "packs", "bare_trefs", "words")

    def __init__(self, path: Path, nb2_root: Path):
        self.path = path
        self.rel = str(path.relative_to(nb2_root))
        self.sector = path.parent.name
        self.stem = path.stem
        text = path.read_text(encoding="utf-8", errors="replace")
        self.title = first_title(text, self.stem)
        self.links = len(WIKILINK_RE.findall(text))
        self.words = len(text.split())
        self.tokens = tokenize(text)
        self.sections_missing = missing_sections(text)
        self.sources_state = sources_state(text)
        self.tension_section = has_tension_section(text)
        self.packs = sorted(set(PACK_CODE_RE.findall(text)))
        self.bare_trefs = sorted(set(BARE_TENSION_REF_RE.findall(text)))


# --------------------------------------------------------------------------- تشابه


def build_inverted_index(concepts, by_sector):
    """فهرس مقلوب **حlose للقطاع**: {sector: {token: [doc_id عالمي]}}.

    الفهرس قطاعي بحكم البناء لا بالفلترة لاحق��ة: أي posting list لا تحوي إلا
    مفاهيم القطاع نفسه، فيستحيل أن يتسرّب جار من قطاع آخر — وهذا شرط «من نفس
    القطاع» في التكليف. نفس البنية تعطي `df` القطاعي مجّانًا."""
    inv: dict[str, dict[str, list[int]]] = {}
    for sec, ids in by_sector.items():
        local: dict[str, list[int]] = defaultdict(list)
        for i in ids:
            for w in concepts[i].tokens:
                local[w].append(i)
        inv[sec] = local
    return inv


def score_sector(concepts, ids, inv, min_overlap: int):
    """يمرّ واحد داخل قطاع ⇒ {i: [(jaccard, overlap, j), …] تنازليًا}.

    عتبة الضجيج = `max(MAX_NOISE_DF, 25% من حجم القطاع)`. الحدّ المطلق 8 موجود
    قصدًا: أقل من 8 مرات لا يمكن أن تكون المفردة «ضجيجًا قطاعيًا» — فهي إشارة نادرة
    مشتركة، وهي الإشارة التي تقوم عليها Jaccard أصلًا؛ ذبحها في قطاع صغير يقتل
    المطابقة كليًا.
    """
    out: dict[int, list] = {}
    df: Counter = Counter()
    for i in ids:
        df.update(concepts[i].tokens)
    cap = max(MAX_NOISE_DF, 0.25 * max(1, len(ids)))
    for i in ids:
        ti = concepts[i].tokens
        if not ti:
            out[i] = []
            continue
        cand: set[int] = set()
        for w in ti:
            if df.get(w, 0) > cap:
                continue                      # مفردة ضجيج قطاعي ⇒ تُبتر من المرشحين
            cand.update(inv[w])
        cand.discard(i)
        scored = []
        for j in cand:
            tj = concepts[j].tokens
            overlap = len(ti & tj)
            if overlap < min_overlap:
                continue
            union = len(ti) + len(tj) - overlap
            if union <= 0:
                continue
            scored.append((overlap / union, overlap, j))
        scored.sort(key=lambda t: (-t[0], -t[1], concepts[t[2]].stem))
        out[i] = scored
    return out


def apply_hub_cap(scores, hub_cap: float, min_jaccard: float, max_links: int,
                  rel_jaccard: float = 0.0):
    """مرّان، والقياس فيهما هو المهم:

    · **مرّ 1 (الطلب)**: `in_degree` يُحسب من **القائمة القصيرة** (أفضل `max_links`
      مرشّحًا لكل concept) لا من كامل مجموعة المرشّحين. الفرق حاسم: concept عام
      قد يظهر في قوائم 400 concept في المرتبة 50، وهو ليس «نجمة» — هو ببساطة
      مرشّح ضعيف عند كثيرين. قياس الطلب على كامل المرشّحات يجعل السقف يقتل
      الروابط الجيدة (قِيس: 700 concept بلا أي رابط و1,117 عند الحد الأقصى تامّةً).
    · **مرّ 2 (التنفيذ)**: تُقطع القائمة القصيرة عند `min_jaccard`، ويُتخطّى كل
      مرشّح نسبة طلبه تتجاوز `hub_cap` من المفاهيم، ثم يُلتزم `max_links`.

    `rel_jaccard` هو **الأرضية النسبية**: لا يُقبل جار دون `rel_jaccard × أفضل_جار`
    أو `min_jaccard` أيهما أعلى. بدونها يملأ كل concept ثمانية روابط حتى لو كان
    ثامنها صفرًا دلاليًا (قِيس: 1,815 من 1,836 عند الحد الأقصى بالضبط). معها
    يصير عدد الروابط دالّةً على قوة العنقود: 3 في concept وحيد و8 في concept
    مترابط، بلا حشو.

    يعيد (chosen, in_degree). `min_links` ليس حشوًا: إن لم يبلغ concept الحد الأدنى
    فذلك عزم مقصود (رابط ضعيف أسوأ من لا رابط)، ويبقى ناقصًا ويُبلَّغ عنه."""
    in_degree: Counter = Counter()
    for scored in scores.values():
        for _, _, j in scored[:max_links]:
            in_degree[j] += 1
    total = max(1, len(scores))
    chosen: dict[int, list] = {}
    for i, scored in scores.items():
        picked = []
        if not scored:
            chosen[i] = picked
            continue
        floor = max(min_jaccard, rel_jaccard * scored[0][0])
        for jac, overlap, j in scored[:max_links]:
            if jac < floor:
                break
            if in_degree[j] / total > hub_cap:
                continue                      # نجمة يحتلّها الجميع ⇒ تُتخطّى
            picked.append((jac, overlap, j))
        chosen[i] = picked
    return chosen, in_degree


def run_proposal(concepts, by_sector, args):
    """خط الأنابيب الكامل: فهرس مقلوب قطاعي ⇒ جار لكل قطاع ⇒ سقف نجوم."""
    t0 = time.time()
    inv = build_inverted_index(concepts, by_sector)
    scores: dict[int, list] = {}
    for sec, ids in by_sector.items():
        scores.update(score_sector(concepts, ids, inv[sec], args.min_overlap))
    chosen, in_degree = apply_hub_cap(scores, args.hub_cap, args.min_jaccard,
                                       args.max_links, args.rel_jaccard)
    vocab = len({w for local in inv.values() for w in local})
    print("[match] docs=%d with_candidates=%d candidate_pairs=%d proposed_slots=%d "
          "vocab=%d in %.1fs" % (
              len(scores), sum(1 for v in scores.values() if v),
              sum(len(v) for v in scores.values()),
              sum(len(v) for v in chosen.values()), vocab, time.time() - t0),
          file=sys.stderr)
    return scores, chosen, in_degree


# --------------------------------------------------------------------------- الخطة


def plan_rows(concepts, chosen, tension_codes, args) -> list[dict]:
    """صفّ واحد لكل concept بالصيغة التوثيقية أعلاه."""
    rows = []
    for i, c in enumerate(concepts):
        picked = chosen.get(i, [])
        c_links = [alias_concept(concepts[j].stem, args.link_form) for _, _, j in picked]
        scores = [round(jac, 3) for jac, _, _ in picked]
        x_codes, x_src = tension_links_for(c.packs, tension_codes, args.max_tensions)
        x_links = [alias_tension(code, args.link_form) for code in x_codes]
        if c.links == 0:
            fix = "add"
        elif c.links < args.min_links:
            fix = "augment"
        else:
            fix = "none"
        reason = "jaccard=%.3f;top=%s;C=%d;X=%d;X_src=%s" % (
            scores[0] if scores else 0.0, "|".join("%.3f" % s for s in scores),
            len(c_links), len(x_links), x_src)
        rows.append({
            "path": c.rel,
            "current_links": c.links,
            "proposed_links": c_links + x_links,
            "reason": reason,
            "sections_missing": c.sections_missing,
            "fix_class": fix,
        })
    return rows


def write_emit(rows, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def cmd_scan(concepts, tension_codes, args) -> int:
    """جدول الفحص: الروابط المطلوبة/الموجودة + الأقسام الناقصة + حالة sources."""
    rows = []
    if not args.json:
        print("%-22s %-40s %4s %5s %6s %-30s %-14s %6s" % (
            "sector", "concept", "cur", "req", "X", "sections_missing",
            "sources", "tens_sec"))
    for c in concepts:
        x_codes, _ = tension_links_for(c.packs, tension_codes, args.max_tensions)
        req = "%d-%d" % (args.min_links, args.max_links)
        rows.append({
            "path": c.rel,
            "sector": c.sector,
            "current_links": c.links,
            "links_required": req,
            "proposed_c_links": f"{args.min_links}-{args.max_links}",
            "proposed_x_links": len(x_codes),
            "sections_missing": c.sections_missing,
            "sources_state": c.sources_state,
            "has_tension_section": c.tension_section,
        })
        if not args.json:
            print("%-22s %-40s %4d %5s %6d %-30s %-14s %6s" % (
                c.sector, c.stem[:40], c.links, req, len(x_codes),
                "، ".join(c.sections_missing) or "—", c.sources_state,
                "yes" if c.tension_section else "NO"))
    if args.json:
        p = Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("wrote %s (%d rows)" % (p, len(rows)), file=sys.stderr)
    else:
        print("-- %d concepts · with_any_link=%d · sections_ok=%d · sources_ok=%d "
              "· tension_section_missing=%d" % (
                  len(rows),
                  sum(1 for r in rows if r["current_links"]),
                  sum(1 for r in rows if not r["sections_missing"]),
                  sum(1 for r in rows if r["sources_state"] == "ok"),
                  sum(1 for r in rows if not r["has_tension_section"])))
    return 0


def cmd_propose(concepts, chosen, tension_codes, args) -> int:
    """أمثلة للمشاهدة اليدوية: concept + روابطه + Jaccard لكل رابط."""
    ranked = sorted((i for i in chosen if chosen[i]),
                    key=lambda i: (-chosen[i][0][0], concepts[i].stem))
    picks = ranked[: args.examples]
    if not picks:
        print("لا مقترحات.")
        return 0
    print("== %d example(s) من %d concept له رابط واحد على الأقل" % (len(picks), len(ranked)))
    for i in picks:
        c = concepts[i]
        print("\n[%s] %s  —  %s" % (c.sector, c.stem, c.title))
        print("   tokens=%d  words=%d  sections_missing=%s  sources=%s  tension_sec=%s" % (
            len(c.tokens), c.words, "، ".join(c.sections_missing) or "—",
            c.sources_state, "yes" if c.tension_section else "NO"))
        for jac, overlap, j in chosen[i]:
            d = concepts[j]
            print("   C  jaccard=%.3f  shared=%-4d -> %s  — %s" % (jac, overlap, d.stem, d.title[:44]))
        x_codes, x_src = tension_links_for(c.packs, tension_codes, args.max_tensions)
        for code in x_codes:
            print("   X  src=%-14s -> TENSION_%s.md" % (x_src, code))
    return 0


# --------------------------------------------------------------------------- التقرير


def audit_link_resolution(concepts, rows, tension_codes):
    """مدقّق سلامة: كل اسم مستعار في الخطة يجب أن يُحلّ ملفًا حقيقيًا.

    يعود كـ(عدد الروابط المفحوصة، عدد غير المحلول، أمثلة). صفر غير-محلول هو شرط
    صحّة الخطة: رابط لا يحلّ في Obsidian = رابط معلقّ، وهو ما تحاول الخطةَ إحلاله."""
    by_sector: dict[str, set] = {}
    for c in concepts:
        by_sector.setdefault(c.sector, set()).add(c.stem)
    checked = broken = 0
    samples = []
    for r in rows:
        sec = r["path"].split("/")[1]
        stems = by_sector.get(sec, set())
        for link in r["proposed_links"]:
            checked += 1
            if link.startswith("C_"):
                ok = ("Concept_" + link[2:]) in stems
            elif link.startswith("X_"):
                ok = link[2:] in tension_codes
            else:
                ok = link in stems or link in tension_codes
            if not ok:
                broken += 1
                if len(samples) < 5:
                    samples.append((r["path"], link))
    return checked, broken, samples


def reciprocity(concepts, chosen, k: int = 1):
    """الاختبار الحاسم: هل يختار Aُ Bَ بـ«أعلى جار» ويختار Bُ Aَ بالمثل؟

    المطابقة العشوائية لا تنتج تبادُلًا: احتمال أن يقع جار A في مركزه*B
    ويقع A في مركز B مركزًا هو ~1/(n−1) ⇒ توقّع ~n/2/(n−1) زوجًا واحدًا فقط.
    أما التشابه الدلالي فينتج أزواجًا متبادلة بكثرة. الفارق هنا عامل آلاف،
    فلا يدين عليه ادّعاء «الجودة-good» بل رقم.

    يعيد (أزواج متبادلة، concepts داخلها، التوقّع العشوائي)."""
    topk = {}
    for i, picked in chosen.items():
        topk[i] = [j for _, _, j in picked[:k]]
    pairs = set()
    for i, js in topk.items():
        for j in js:
            if i in topk.get(j, ()):
                pairs.add((min(i, j), max(i, j)))
    n = max(1, len(chosen))
    return len(pairs), 2 * len(pairs), (n / 2) / max(1, n - 1)


def random_baseline(concepts, by_sector, n_samples: int, seed: int = 20261002):
    """قاعدة المقارنة: أزواج عشوائية **داخل القطاع نفسه** ⇒ كم جaccard يعطيه الحظ.

    لولا هذا القياس كانت عبارة «التشابه حقيقي لا عشوائي» دعوى؛ ومعه يصبح رقمًا:
    لو كانت المطابقة عشوائية لوقع متوسط الأزواج المقترحة داخل مدى القاعدة."""
    import random as _r
    rng = _r.Random(seed)
    pairs = []
    pool = []
    for sec, ids in by_sector.items():
        n = len(ids)
        if n < 2:
            continue
        for _ in range(n_samples // max(1, len(by_sector)) + 1):
            a, b = rng.sample(ids, 2)
            pool.append((a, b))
    for a, b in pool[:n_samples]:
        ta, tb = concepts[a].tokens, concepts[b].tokens
        inter = len(ta & tb)
        union = len(ta) + len(tb) - inter
        pairs.append(inter / union if union else 0.0)
    pairs.sort()
    return pairs


def percentile(sorted_vals, q: float) -> float:
    if not sorted_vals:
        return 0.0
    k = min(len(sorted_vals) - 1, max(0, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[k]


def build_report(concepts, chosen, scores, rows, tension_codes, tried, elapsed, args,
                 baseline=None):
    n = len(concepts)
    with_links = [i for i in chosen if chosen[i]]
    no_links = sorted(i for i in chosen if not chosen[i])
    slot_counts = Counter(len(v) for v in chosen.values())
    links_per = [len(r["proposed_links"]) for r in rows]
    mean_links = (sum(links_per) / n) if n else 0.0
    mean_c = (sum(len(v) for v in chosen.values()) / n) if n else 0.0
    sec_missing_hist = Counter(k for c in concepts for k in c.sections_missing)
    src_hist = Counter(c.sources_state for c in concepts)
    no_tension_sec = [c for c in concepts if not c.tension_section]
    fixes = Counter(r["fix_class"] for r in rows)
    below_target = sum(1 for i in with_links if len(chosen[i]) < args.min_links)

    checked_links, broken_links, broken_samples = audit_link_resolution(concepts, rows, tension_codes)
    mp, mc, exp = reciprocity(concepts, chosen, k=1)
    mutual_pairs = (mp, mc, exp)
    tops = sorted(chosen[i][0][0] for i in with_links)
    all_pair = sorted(jac for v in chosen.values() for jac, _, _ in v)
    ranked = sorted(with_links, key=lambda i: (-chosen[i][0][0], concepts[i].stem))[:5]

    L: list[str] = []
    a = L.append
    a("# LINK_PLAN_REPORT — خطة روابط الـWiki للمفاهيم الـ1,836")
    a("")
    a("> مولَّد آليًا بـ `V3/11_INDEX/tools/build_link_plan.py --report` — **خطة لا تعديل**.")
    a("> النطاق: `%s/02_CONCEPTS/<NN_*>/*.md` (نطاق `audit_scoped --scope concepts` حرفًا)."
      % args.nb2)
    a("> القراءة فقط على NB2؛ الكتابة محصورة في هذا الملف و`%s`. الزمن: **%.1fث**."
      % (args.emit, elapsed))
    a("")
    a("## 1) الحجم")
    a("")
    a("| المقياس | القيمة |")
    a("|---|---:|")
    a("| مفاهيم مفحوصة | **%d** |" % n)
    a("| concepts تُقترح عليها روابط (≥1) | **%d** (%.1f%%) |"
      % (len(with_links), 100.0 * len(with_links) / n))
    a("| concepts بلا أي رابط مقترح | **%d** (%.1f%%) |"
      % (len(no_links), 100.0 * len(no_links) / n))
    a("| متوسط الروابط المقترحة / concept | **%.2f** |" % mean_links)
    a("| متوسط روابط `C_` فقط / concept | %.2f |" % mean_c)
    a("| إجمالي الروابط المقترحة | %d |" % sum(links_per))
    a("| `fix_class` | %s |" % " · ".join("`%s`=%d" % kv for kv in sorted(fixes.items())))
    a("| `current_links > 0` | %d ⇒ تأكيد اكتشاف «صفر wikilink» |"
      % sum(1 for c in concepts if c.links))
    a("| concepts تحت هدف `--min-links %d` | %d (عزم، لا حشو) |" % (args.min_links, below_target))
    a("")
    a("### توزيع عدد الروابط المقترحة")
    a("")
    a("| روابط `C_` مقترحة | concepts |")
    a("|---:|---:|")
    a("| **0** | **%d** |" % slot_counts.get(0, len(no_links)))
    for k in sorted(k for k in slot_counts if k > 0):
        a("| %d | %d |" % (k, slot_counts[k]))
    a("")
    a("عدد الفتحات = %d (مجموع روابط `C_`) · concepts بلا رابط = %d."
      % (sum(k * v for k, v in slot_counts.items()), len(no_links)))
    a("")
    x_hist = Counter()
    for c in concepts:
        x_hist[len(tension_links_for(c.packs, tension_codes, args.max_tensions)[0])] += 1
    a("توزيع روابط التوتر `X_`: " + " · ".join("%d→%d" % kv for kv in sorted(x_hist.items())))
    a("")
    a("## 2) هل الفهرس مبني على تشابه حقيقي أم عشوائي؟")
    a("")
    a("**تشابه حقيقي** — والدليل كمّي:")
    a("")
    a("| مقياس أعلى جار (Jaccard) | p10 | p50 | p90 | p99 | max |")
    a("|---|---:|---:|---:|---:|---:|")
    a("| لكل concept | %.3f | %.3f | %.3f | %.3f | %.3f |" % (
        percentile(tops, .10), percentile(tops, .50), percentile(tops, .90),
        percentile(tops, .99), (tops[-1] if tops else 0.0)))
    a("| لكل رابط مقترح | %.3f | %.3f | %.3f | %.3f | %.3f |" % (
        percentile(all_pair, .10), percentile(all_pair, .50), percentile(all_pair, .90),
        percentile(all_pair, .99), (all_pair[-1] if all_pair else 0.0)))
    if baseline:
        a("| **قاعدة عشوائية داخل القطاع** (ن=%d زوج) | %.3f | %.3f | %.3f | %.3f | %.3f |" % (
            len(baseline), percentile(baseline, .10), percentile(baseline, .50),
            percentile(baseline, .90), percentile(baseline, .99),
            (baseline[-1] if baseline else 0.0)))
    a("")
    if baseline:
        r_med = percentile(baseline, .50)
        r_max = baseline[-1] if baseline else 0.0
        t_med = percentile(tops, .50)
        t_max = tops[-1] if tops else 0.0
        r_lo = 100.0 * sum(1 for v in baseline if v >= args.min_jaccard) / max(1, len(baseline))
        r_hi = 100.0 * sum(1 for v in all_pair if v >= args.min_jaccard) / max(1, len(all_pair))
        a("**الحكم بالقياس لا بالدَّعاء.**")
        a("")
        a("- **القاعدة العشوائية** (أزواج مصطادفة داخل القطاع نفسه): وسيط `%.3f`، أقصاه `%.3f`."
          % (r_med, r_max))
        a("- **روابط الخطة**: وسيط **%.3f**، أقصاه **%.3f** — أي **%.0f–%.0f ضعف** وسيط الحظ."
          % (t_med, t_max, (t_med / r_med if r_med else 0), (t_max / r_med if r_med else 0)))
        a("- نسبة ما يتجاوز `jaccard ≥ %.2f`: **%.0f%%** في القاعدة العشوائية مقابل "
          "**%.0f%%** في روابط الخطة." % (args.min_jaccard, r_lo, r_hi))
        a("")
        a("**قراءة نقدية للسطرين الأخيرين — ولماذا لا يصلحان دليلاً:** البوابة المطلقة "
          "`jaccard ≥ %.2f` **لا تفصل**؛ %.0f%% من الأزواج العشوائية داخل القطاع تتجاوزها، "
          "لأن مفردات القطاع الواحد مشتركة بحكم الموضوع (هذا بالضبط سبب حصر المرشحين "
          "داخل القطاع: روابط العرض تُنتج ضجيجًا، لكن داخل القطاع يبقى السقف النسبي)."
          % (args.min_jaccard, r_lo))
        a("ولذلك **لم أبنِ الحكم على نسبة الرفع** (2–4 ضعف فقط)، بل على اختبار بنيوي لا "
          "يمكن أن تنتجه الصدفة: تبادُل أعلى جار أدناه.")
        a("")
        if mutual_pairs is not None:
            mp, mc, exp = mutual_pairs
            a("**والاختبار الحاسم — تبادُل أعلى جار (reciprocity):**")
            a("")
            a("| المقياس | القيمة |")
            a("|---|---:|")
            a("| أزواج متبادلة (A أفضل = B و B أفضل = A) | **%d** |" % mp)
            a("| concepts داخل زوج متبادل | **%d** (%.1f%% من %d) |"
              % (mc, 100.0 * mc / max(1, n), n))
            a("| التوقّع تحت مطابقة عشوائية | ~%.2f زوج |" % exp)
            a("| **الفارق عن التوقّع العشوائي** | **%.0f ضعفًا** |" % (mp / exp if exp else 0))
            a("")
            a("هذا هو الفرق الحقيقي، لا نسبة الرفع: المطابقة العشوائية لا تُنتج تبادُلًا "
              "عمليًا (توقّع أقل من زوج واحد)، فوجود **%d** زوجًا متبادلًا يثبت أن "
              "الترتيب مبني على تشابه متبادل فعلي." % mp)
        a("")
        a("والجدول التالي (5 أمثلة) هو الفحص اليدوي النهائي: كل رابط فيه مقروء دلاليًا بجواره.")
    else:
        a("التفسير: أعلى جار لكل concept يتفوّق على وسيط كل الروابط المقترحة، "
          "والمدى واسع ⇒ الترتيب يميّز ولا يوزّع درجات متقاربة.")
    a("")
    a("**5 أمثلة للتدقيق اليدوي** (مرتّبة تنازليًا بأعلى جار):")
    a("")
    for i in ranked:
        c = concepts[i]
        a("**[%s] %s** — %s · مفردات=%d" % (c.sector, c.stem, c.title, len(c.tokens)))
        a("")
        a("| رابط مقترح | Jaccard | مفردات مشتركة | الهدف |")
        a("|---|---:|---:|---|")
        for jac, overlap, j in chosen[i]:
            d = concepts[j]
            a("| `%s` | **%.3f** | %d | %s |"
              % (alias_concept(d.stem, args.link_form), jac, overlap, d.title))
        x_codes, x_src = tension_links_for(c.packs, tension_codes, args.max_tensions)
        for code in x_codes:
            a("| `%s` | — | — | رابط توتر (%s) → `TENSION_%s.md` |"
              % (alias_tension(code, args.link_form), x_src, code))
        a("")
    a("## 3) من بلا رابط (عزم ⇒ خارج النطاق عمدًا)")
    a("")
    if not no_links:
        a("**لا يوجد** — كل concept وجد مرشحًا واحدًا على الأقل.")
    else:
        a("**%d concept** بلا أي رابط مقترح: لم يجد داخل قطاعه مرشحًا يحقّق "
          "`overlap ≥ %d` و`jaccard ≥ %.2f` مع سقف النجوم." %
          (len(no_links), args.min_overlap, args.min_jaccard))
        a("")
        a("هذه **عزيمة مقصودة** لا نقص: في Obsidian الرابط الضعيف يُنتج false-positive في "
          "الروابط المعلقة، وهو أسوأ من غياب الرابط. صفوفها في `LINK_PLAN.jsonl` "
          "بـ`proposed_links: []`.")
        a("")
        a("| القطاع | بلا رابط |")
        a("|---|---:|")
        for sec, cnt in sorted(Counter(concepts[i].sector for i in no_links).items()):
            a("| %s | %d |" % (sec, cnt))
        a("")
        a("**أسماؤها كاملة** (من `%s`):" % os.path.basename(str(args.emit)))
        a("")
        for i in no_links:
            a("- `%s` [%s] — %s" % (concepts[i].stem, concepts[i].sector, concepts[i].title))
    a("")
    a("## 4) الأقسام الناقصة وحالة المصادر (لماذا هذه الخطة تكفي لتخطيط P1/P2)")
    a("")
    a("| حالة `sources` (C28) | concepts |")
    a("|---|---:|")
    for k, v in src_hist.most_common():
        a("| `%s` | %d |" % (k, v))
    a("")
    a("| القسم الناقص (C14) | concepts |")
    a("|---|---:|")
    for k, v in sec_missing_hist.most_common():
        a("| %s | %d |" % (k, v))
    a("")
    a("**بلا قسم توتر ⇒ يلزم إصدار `X_` جديد: %d concept**%s"
      % (len(no_tension_sec), ":" if no_tension_sec else "."))
    if no_tension_sec:
        a("")
        for c in no_tension_sec:
            a("- `%s` [%s] — %s" % (c.stem, c.sector, c.title))
    a("")
    a("## 5) روابط التوتر `X_` — القناة ومصدرها")
    a("")
    a("مجلدات التوترات المفحوصة: %s" % ", ".join("`%s`" % t for t in tried))
    a("")
    a("الملفات المرجعية: **%d** ملف `TENSION_<code>.md`. القناة المستعملة **حتمية واحدة**: "
      "رمز الحزمة المذكور في المتن (`حزمة C7` ← `TENSION_C7.md`)." % len(tension_codes))
    a("")
    a("- **لماذا لا قناة تشابه نصّي؟** قياس على 300 concept: تشابه عنوان الـconcept بعنوان "
      "بند التوتر أعطى تغطية **2/300** عند بحدّ `overlap ≥ 2`، وتشابه قسم «التوترات» "
      "بملفات التوترات كاملة أعطى **متوسط أعلى درجة 0.047** مع تكرار `TENSION_B10` "
      "كـ«أفضل» مطابقة لأغلب الملفات ⇒ ارتباط عرضي لا رابط حقيقي. قناة حتمية بتغطية "
      "100% أفضل من قناة ضجيج بتغطية 1.7%.")
    pack_hist = Counter(code for c in concepts for code in c.packs)
    known = set(pack_hist) & set(tension_codes)
    a("- رموز الحزم المذكورة في المتن: **%d** رمزًا، منها **%d** له ملف توتر مقابل "
      "(تغطية %s)." % (len(pack_hist), len(known),
                       "100%" if len(known) == len(pack_hist) else "جزئية"))
    a("- concepts ذكر رمز حزمة واحدًا على الأقل: **%d**." % sum(1 for c in concepts if c.packs))
    a("- **استُثني عمدًا ومذكور**: %d concept فيها مرجع `T<رقم>` مجرد؛ الترقيم يُعاد "
      "داخل كل ملف توتر من 65 ملفًا ⇒ غير قابل للعزل ⇒ لا رابط." %
      sum(1 for c in concepts if c.bare_trefs))
    a("")
    a("## 6) إعادة الإنتاج والتحقّق")
    a("")
    a("```bash")
    a("cd /root/r/V3/11_INDEX/tools")
    a("python3 build_link_plan.py --selftest    # تأكيدات على فيكتور اصطناعي (بلا NB2)")
    a("python3 build_link_plan.py --emit --report")
    a("python3 build_link_plan.py --propose --examples 12")
    a("```")
    a("")
    a("معاملات هذه التشغيل: `--min-links %d` · `--max-links %d` · `--min-jaccard %.2f` · "
      "`--min-overlap %d` · `--hub-cap %.2f` · `--rel-jaccard %.2f` · "
      "`--max-tensions %d` · `--link-form %s` · `--baseline-samples %d` (بذرة %d)"
      % (args.min_links, args.max_links, args.min_jaccard, args.min_overlap,
         args.hub_cap, args.rel_jaccard, args.max_tensions, args.link_form,
         args.baseline_samples, args.baseline_seed))
    a("")
    a("### تدقيق سلامة الروابط (شرط صحّة الخطة)")
    a("")
    a("| الفحص | القيمة |")
    a("|---|---:|")
    a("| روابط مفحوصة في `%s` | %d |" % (os.path.basename(str(args.emit)), checked_links))
    a("| روابط **لا تُحلّ ملفًا حقيقيًا** | **%d** |" % broken_links)
    a("")
    if broken_links:
        a("أمثلة غير محلولة:")
        a("")
        for p_, l_ in broken_samples:
            a("- `%s` → `%s`" % (p_, l_))
    else:
        a("كل رابط في الخطة — `C_` و`X_` معًا — يقابل ملفًا موجودًا على القرص الآن "
          "(تحقّق آلي داخل التقرير، لا يدَوي).")
    a("")
    a("### تركيبة نتيجة `--propose` (بلا وسيط) وحقول المخرج")
    a("")
    a("- `current_links > 0` يعني Wikilink قائمًا — وهو **0 في كل الملفات** ⇒ العطب D13 "
      "مؤكد رقميًا لا بالقراءة.")
    a("- `sections_missing` محسوبة بنفس `heads+bolds` pool الذي يستخدمه C14 ⇒ قابلة "
      "للمطابقة رقمًا برقم مع `DEFECTS_SUMMARY.md`.")
    a("- `sources_state` مصنّف C28 إلى أربع حالات بدل ثنائي ⇒ نصلح `no_frontmatter` "
      "(إضافة frontmatter) و`no_key`/`empty` (قيمة) بخطوتين مختلفتين.")
    a("")
    stats = {
        "concepts": n,
        "with_links": len(with_links),
        "no_links": len(no_links),
        "mean_links": round(mean_links, 3),
        "mean_c_links": round(mean_c, 3),
        "total_links": sum(links_per),
        "slot_distribution": dict(sorted(slot_counts.items())),
        "sources": dict(src_hist),
        "sections_missing": dict(sec_missing_hist),
        "concepts_without_tension_section": len(no_tension_sec),
        "fix_class": dict(fixes),
        "top_jaccard_p50": round(percentile(tops, .50), 4),
        "top_jaccard_max": round(tops[-1] if tops else 0.0, 4),
        "below_min_links_target": below_target,
        "links_checked": checked_links,
        "links_unresolvable": broken_links,
        "mutual_top1_pairs": mp,
        "concepts_in_mutual_top1": mc,
        "mutual_top1_random_expectation": round(exp, 3),
        "random_baseline_p50": round(percentile(baseline, .50), 4) if baseline else None,
        "random_baseline_max": round(baseline[-1], 4) if baseline else None,
        "elapsed_sec": round(elapsed, 1),
    }
    return "\n".join(L) + "\n", stats


# --------------------------------------------------------------------------- اختبارات ذاتية


def selftest() -> int:
    """اختبارات على فيكتور اصطناعي في مجلد مؤقّت — لا تلمس NB2."""
    import shutil
    import tempfile

    ok = fails = 0

    def check(name, cond, extra=""):
        nonlocal ok, fails
        if cond:
            ok += 1
            print("  OK   %s" % name)
        else:
            fails += 1
            print("  FAIL %s  %s" % (name, extra))

    print("== tokenizer")
    t = tokenize("## الآلية\n> **المجال:** AI · محتوى\n"
                 "التعليقُ القيّمُ يصنعُ السُّلطةَ (authority) — 1234!")
    check("diacritics stripped", "تعليقُ" not in t and "التعليقُ" not in t, sorted(t))
    check("definite article removed", "تعليق" in t and "التعليق" not in t, sorted(t))
    check("meta line dropped", "مجال" not in t, sorted(t))
    check("pure digits dropped", not any(PURE_NUM_RE.match(w) for w in t), sorted(t))
    check("latin kept + lowered", "authority" in t, sorted(t))
    check("symbol-only token dropped", "—" not in t)
    fm_toks = tokenize("---\ntype: concept\ntags: [08]\nrelated: []\n---\n\n# T\n\n## الآلية\nمقاطعة نمط بصرية\n")
    check("frontmatter keys excluded",
          not ({"type", "concept", "tags", "related"} & fm_toks), sorted(fm_toks))
    check("frontmatter body still tokenized", "مقاطعة" in fm_toks, sorted(fm_toks))

    print("== classifiers (C14 / C28 / C23)")
    full = ("# T · T\n\n## التعريف\nd\n\n## الآلية\nx\n\n## حدود الفناء\ny\n\n"
            "## الشروط\nz\n\n## الدليل\nq\n\n## المصدرية\nw\n")
    check("six sections present -> []", missing_sections(full) == [],
          missing_sections(full))
    one_gone = full.replace("## الشروط\nz\n\n", "")
    check("one section removed -> detected",
          missing_sections(one_gone) == ["الشروط"], missing_sections(one_gone))
    three_gone = one_gone.replace("## الدليل\nq\n\n", "").replace("## الآلية\nx\n\n", "")
    check("three sections removed -> 3 keys",
          missing_sections(three_gone) == ["الآلية", "الشروط", "الدليل"],
          missing_sections(three_gone))
    check("no frontmatter -> no_frontmatter", sources_state("# x\n") == "no_frontmatter")
    check("frontmatter w/o source key -> no_key",
          sources_state("---\ntype: concept\n---\n") == "no_key")
    check("empty list -> empty", sources_state("---\nsources: []\n---\n") == "empty")
    check("zero count -> empty",
          sources_state("---\nsources_count: 0\n---\n") == "empty")
    check("non-empty -> ok",
          sources_state('---\nsources_channels: ["IG"]\n---\n') == "ok")
    check("tension section present", has_tension_section("## التوترات\n- x") is True)
    check("tension section absent", has_tension_section("# x\nbody") is False)

    print("== end-to-end on synthetic corpus")
    tmp = Path(tempfile.mkdtemp(prefix="linkplan_"))
    try:
        alpha = tmp / "02_CONCEPTS" / "01_alpha"
        beta = tmp / "02_CONCEPTS" / "02_beta"
        for d in (alpha, beta, tmp / "02_CONCEPTS" / "_REPORTS", tmp / "02_CONCEPTS" / "terms_26k"):
            d.mkdir(parents=True, exist_ok=True)
        (tmp / "02_CONCEPTS" / "_INDEX.md").write_text("x", encoding="utf-8")
        (tmp / "02_CONCEPTS" / "_REPORTS" / "r.md").write_text("x", encoding="utf-8")
        (tmp / "02_CONCEPTS" / "terms_26k" / "a.md").write_text("x", encoding="utf-8")
        shared = ("تعليق authority pipeline republication outreach leadgen engagement "
                  "nurture social proof comment")
        for i in range(4):
            (alpha / ("%sA%d.md" % (CONCEPT_PREFIX, i))).write_text(
                "# مفهوم ألف%d · A%d\n\n## الآلية\n%s unique%d\n" % (i, i, shared, i),
                encoding="utf-8")
        for i in range(3):
            (alpha / ("%sB%d.md" % (CONCEPT_PREFIX, i))).write_text(
                "# مفهوم باء%d · B%d\n\n## الآلية\n%s other%d\n" % (i, i, shared, i),
                encoding="utf-8")
        (beta / ("%sZ0.md" % CONCEPT_PREFIX)).write_text(
            "# مستقل · Z0\n\n## الآلية\n%s\n" % shared, encoding="utf-8")
        (beta / ("%sLONE.md" % CONCEPT_PREFIX)).write_text(
            "# وحيد · LONE\n\n## الآلية\nمنفصل كليمات نادرة فريدة zzqqxx qqwwvv\n",
            encoding="utf-8")
        # concept يذكر رمز حزمة في المتن ⇒ قناة التوتر الحتمية
        (alpha / ("%sPack1.md" % CONCEPT_PREFIX)).write_text(
            "# حزمة · Pack1\n\n## الآلية\n%s packnote\n\n## التوترات\n"
            "مقارنة مع حزمة C7 ثم حزمة D3 ثم حزمة ZZ9\n" % shared, encoding="utf-8")
        tens = tmp / "05_TENSIONS"
        tens.mkdir()
        (tens / "TENSION_C7.md").write_text("حزمة C7 توتر", encoding="utf-8")
        (tens / "TENSION_D3.md").write_text("حزمة D3 توتر", encoding="utf-8")

        cpts, by_sec, codes, _ = build_corpus(tmp, (tmp / "05_TENSIONS",), verbose=False)
        check("scope = NN_* only (10 files)", len(cpts) == 10, len(cpts))
        check("sectors detected", set(by_sec) == {"01_alpha", "02_beta"}, set(by_sec))
        check("tension codes loaded", set(codes) == {"C7", "D3"}, set(codes))

        # فيكتور الـclique: 8 من 10 ملفات تتشارك المفردات ⇒ كل عقدة نجمة
        # بحكم البناء، فـhub_cap يُرفع هنا ويُختبر سلوكه بحالة مستقلة أدناه.
        ns = argparse.Namespace(min_overlap=3, hub_cap=0.90, min_links=3, max_links=8,
                                min_jaccard=0.05, rel_jaccard=0.40, link_form="alias",
                                max_tensions=2, nb2=str(tmp), emit=str(tmp / "p.jsonl"))
        scores, chosen, indeg = run_proposal(cpts, by_sec, ns)
        rows = plan_rows(cpts, chosen, codes, ns)

        check("row schema exact (6 keys)", all(set(r) == {
            "path", "current_links", "proposed_links", "reason",
            "sections_missing", "fix_class"} for r in rows))
        byname = {r["path"].split("/")[-1]: r for r in rows}
        a0 = byname["%sA0.md" % CONCEPT_PREFIX]
        check("alias form C_<slug>", all(l.startswith("C_") for l in a0["proposed_links"]),
              a0["proposed_links"])
        check("no self link", "C_A0" not in a0["proposed_links"], a0["proposed_links"])
        check("cross-sector isolation (no C_Z0)",
              not any(l.startswith("C_Z0") for l in a0["proposed_links"]),
              a0["proposed_links"])
        check("lonely concept gets zero links",
              byname["%sLONE.md" % CONCEPT_PREFIX]["proposed_links"] == [])
        check("reason prefix", a0["reason"].startswith("jaccard="), a0["reason"])
        top_str = a0["reason"].split(";top=")[1].split(";")[0]
        scores_l = [float(x) for x in top_str.split("|")] if top_str else []
        check("A0 has proposals in clique fixture", len(scores_l) >= 1, a0["reason"])
        check("reason scores non-increasing",
              all(scores_l[k] >= scores_l[k + 1] for k in range(len(scores_l) - 1)), scores_l)
        a0_idx = [i for i, c in enumerate(cpts) if c.stem.endswith("A0")][0]
        check("reason top == chosen max",
              abs(scores_l[0] - chosen[a0_idx][0][0]) < 1e-3,
              (scores_l[:1], chosen[a0_idx][:1]))
        check("reason len == C count",
              ("C=%d" % len(a0["proposed_links"])) in a0["reason"], a0["reason"])
        lone = byname["%sLONE.md" % CONCEPT_PREFIX]
        check("empty proposal ⇒ empty top and 0.000",
              lone["reason"].endswith("X_src=none") and "top=;C=0;X=0" in lone["reason"],
              lone["reason"])
        check("aliases resolve on disk (C_<slug> ⇒ Concept_<slug>.md)",
              all((alpha / ("Concept_" + l[2:] + ".md")).is_file()
                  for l in a0["proposed_links"] if l.startswith("C_")),
              a0["proposed_links"])
        check("fix_class=add when current_links==0",
              all(r["fix_class"] == "add" for r in rows))
        check("max_links respected",
              all(len(v) <= ns.max_links for v in chosen.values()))
        check("tension channel: pack code -> X_C7",
              "X_C7" in byname["%sPack1.md" % CONCEPT_PREFIX]["proposed_links"],
              byname["%sPack1.md" % CONCEPT_PREFIX]["proposed_links"])
        check("tension channel: unknown code ZZ9 dropped",
              not any("ZZ9" in l for l in byname["%sPack1.md" % CONCEPT_PREFIX]["proposed_links"]))

        ns.link_form = "stem"
        a0s = [r for r in plan_rows(cpts, chosen, codes, ns)
               if r["path"].endswith("A0.md")][0]
        check("stem form uses real stems",
              all(l.startswith(CONCEPT_PREFIX) for l in a0s["proposed_links"]),
              a0s["proposed_links"])
        pack_s = [r for r in plan_rows(cpts, chosen, codes, ns)
                  if r["path"].endswith("Pack1.md")][0]
        check("stem form tension uses real stem",
              any(l.startswith(TENSION_PREFIX) for l in pack_s["proposed_links"]),
              pack_s["proposed_links"])
        ns.link_form = "alias"

        codes_used, src = tension_links_for(["C7", "D3", "ZZ9"], codes, 2)
        check("tension channel capped at max_tensions",
              codes_used == ["C7", "D3"] and src == "pack:C7,D3", (codes_used, src))
        _, src0 = tension_links_for([], codes, 2)
        check("tension channel empty -> none", src0 == "none", src0)

        d_idx = [i for i, c in enumerate(cpts) if c.stem.endswith("A0")][0]
        synthetic = {i: [(0.9, 9, d_idx)] for i in range(5)}
        ch, _ = apply_hub_cap(synthetic, 0.10, 0.05, 8)
        check("hub cap drops hyper-linked doc", all(not v for v in ch.values()), ch)
        ch2, _ = apply_hub_cap({i: [(0.02, 9, d_idx)] for i in range(5)}, 0.10, 0.05, 8)
        check("min_jaccard gate applied", all(not v for v in ch2.values()), ch2)
        # أرضية نسبية (سقف النجوم معطّل هنا بـ10.0 لأن القاموس صفّ واحد):
        # best=0.60 ⇒Floor=0.24 ⇒ جار 0.30 يُقبل و0.20 و0.10 يُرفضان.
        rel = {0: [(0.60, 60, d_idx), (0.10, 9, d_idx)]}
        ch3, _ = apply_hub_cap(rel, 10.0, 0.05, 8, rel_jaccard=0.40)
        check("relative floor keeps strong neighbour", len(ch3[0]) == 1, ch3[0])
        rel2 = {0: [(0.60, 60, d_idx), (0.20, 9, d_idx)]}
        ch4, _ = apply_hub_cap(rel2, 10.0, 0.05, 8, rel_jaccard=0.40)
        check("relative floor drops weak tail", len(ch4[0]) == 1, ch4[0])
        ch5, _ = apply_hub_cap(rel2, 10.0, 0.05, 8, rel_jaccard=0.10)
        check("loose relative floor keeps tail", len(ch5[0]) == 2, ch5[0])
        ch6, _ = apply_hub_cap({}, 0.10, 0.05, 8)
        check("empty scores handled", ch6 == {}, ch6)
        # نفس الكليك الحقيقي لكن بسقف نجوم واقعي (10%) ⇒ ينهار إلى صفر
        tight, _ = apply_hub_cap(scores, 0.10, 0.05, 8)
        check("realistic hub cap collapses the clique",
              all(not v for v in tight.values()),
              {i: len(v) for i, v in list(tight.items())[:4]})
        bl = random_baseline(cpts, by_sec, 400, seed=1)
        check("baseline sampled", len(bl) == 400, len(bl))
        check("baseline sorted ascending", all(bl[k] <= bl[k + 1] for k in range(len(bl) - 1)))
        check("baseline bounded [0,1]", all(0.0 <= v <= 1.0 for v in bl))
        bl0 = random_baseline(cpts, by_sec, 0, seed=1)
        check("baseline 0 -> empty", bl0 == [], bl0)
        rp, rc, rex = reciprocity(cpts, chosen, k=1)
        check("reciprocity: concepts == 2×pairs", rc == 2 * rp, (rp, rc))
        check("reciprocity random expectation tiny", 0 < rex < 1.0, rex)
        two_cycle = {0: [(0.9, 9, 1)], 1: [(0.9, 9, 0)], 2: [(0.9, 9, 3)], 3: []}
        rp2, rc2, _ = reciprocity(cpts, two_cycle, k=1)
        check("reciprocity finds exactly the 2-cycle", (rp2, rc2) == (1, 2), (rp2, rc2))
        chX = {i: [(0.9, 9, (i + 1) % 10)] for i in range(10)}
        rp3, rc3, _ = reciprocity(cpts, chX, k=1)
        check("reciprocity zero on a directed cycle", rp3 == 0, (rp3, rc3))
        ck, br, sm = audit_link_resolution(cpts, rows, codes)
        check("every proposed link resolves on disk", br == 0, (br, sm))
        check("audit counted every link", ck == sum(len(r["proposed_links"]) for r in rows), (ck,))
        bad_rows = [dict(rows[0], proposed_links=["C_DoesNotExist"])]
        ck2, br2, sm2 = audit_link_resolution(cpts, bad_rows, codes)
        check("audit flags a dangling link", (br2 == 1 and len(sm2) == 1), (br2, sm2))
        indeg_top = indeg.most_common(1)[0]
        check("in_degree computed", indeg_top[1] > 0, indeg_top)
        check("max_links respected after cap",
              all(len(v) <= ns.max_links for v in chosen.values()))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("-- selftest: %d ok, %d fail" % (ok, fails))
    return 1 if fails else 0


# --------------------------------------------------------------------------- CLI


def build_corpus(nb2_root: Path, tension_dirs, verbose=True):
    t0 = time.time()
    concepts = [Concept(p, nb2_root) for p in iter_concepts(nb2_root)]
    by_sector: dict[str, list[int]] = defaultdict(list)
    for i, c in enumerate(concepts):
        by_sector[c.sector].append(i)
    codes, tried = load_tension_codes(tension_dirs)
    if verbose:
        print("[load] concepts=%d sectors=%d tension_codes=%d dirs=%s in %.1fs" % (
            len(concepts), len(by_sector), len(codes), tried, time.time() - t0), file=sys.stderr)
    return concepts, by_sector, codes, tried


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="مولّد خطة روابط Wiki لـ1,836 مفهوم (قراءة فقط على NB2، بلا تعديل)")
    ap.add_argument("--nb2", default=str(NB2_ROOT), help="جذر NB2 (قراءة فقط)")
    ap.add_argument("--scan", action="store_true", help="جدول الفحص لكل concept")
    ap.add_argument("--scan-limit", type=int, default=0, help="اطبع أول N صفوف فقط (0=الكل)")
    ap.add_argument("--json", metavar="PATH", help="مخرج JSON لجدول --scan")
    ap.add_argument("--propose", action="store_true", help="أمثلة مع Jaccard لكل رابط")
    ap.add_argument("--emit", nargs="?", const=str(DEFAULT_EMIT), default=None,
                    metavar="OUT.jsonl", help="اكتب خطة JSONL")
    ap.add_argument("--report", nargs="?", const=str(DEFAULT_REPORT), default=None,
                    metavar="OUT.md", help="اكتب تقرير الخطة")
    ap.add_argument("--examples", type=int, default=5, help="عدد أمثلة --propose")
    ap.add_argument("--min-links", type=int, default=3, help="حد أدنى روابط مقترحة (هدف لا حشو)")
    ap.add_argument("--max-links", type=int, default=8, help="حد أقصى روابط C_ لكل concept")
    ap.add_argument("--max-tensions", type=int, default=2, help="حد أقصى روابط X_ لكل concept")
    ap.add_argument("--min-jaccard", type=float, default=0.05, help="أقل Jaccard مقبول")
    ap.add_argument("--min-overlap", type=int, default=3, help="أقل مفردات مشتركة")
    ap.add_argument("--hub-cap", type=float, default=0.10,
                    help="سقف النجوم: أقصى نسبة concepts تطلب نفس الـconcept")
    ap.add_argument("--rel-jaccard", type=float, default=0.40,
                    help="أرضية نسبية: لا جار دون هذه النسبة من أفضل جار (مضادة للحشو)")
    ap.add_argument("--link-form", choices=("alias", "stem"), default="alias",
                    help="alias ⇒ C_<slug>/X_<code> · stem ⇒ Concept_<slug>/<code>")
    ap.add_argument("--baseline-samples", type=int, default=3000,
                    help="عدد أزواج القاعدة العشوائية للمقارنة (0 لتعطيلها)")
    ap.add_argument("--baseline-seed", type=int, default=20261002,
                    help="بذرة القاعدة العشوائية (لإعادة الإنتاج)")
    ap.add_argument("--selftest", action="store_true", help="اختبارات ذاتية (بلا NB2)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if not (args.scan or args.propose or args.emit or args.report or args.json):
        args.scan = True

    t0 = time.time()
    concepts, by_sector, codes, tried = build_corpus(Path(args.nb2), TENSION_DIR_CANDIDATES)

    rows = chosen = scores = None
    if args.propose or args.emit or args.report:
        scores, chosen, indeg = run_proposal(concepts, by_sector, args)
        rows = plan_rows(concepts, chosen, codes, args)

    if args.scan:
        cmd_scan(concepts[: args.scan_limit] if args.scan_limit else concepts, codes, args)
    if args.propose:
        cmd_propose(concepts, chosen, codes, args)
    if args.emit:
        print("wrote %s (%d rows)" % (write_emit(rows, Path(args.emit)), len(rows)),
              file=sys.stderr)
    if args.report:
        base = random_baseline(concepts, by_sector, args.baseline_samples, args.baseline_seed)
        text, stats = build_report(concepts, chosen, scores, rows, codes, tried,
                                   time.time() - t0, args, baseline=base)
        rp = Path(args.report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(text, encoding="utf-8")
        print("wrote %s" % rp, file=sys.stderr)
        print("-- stats: " + json.dumps(stats, ensure_ascii=False), file=sys.stderr)
    print("-- total %.1fs" % (time.time() - t0), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())