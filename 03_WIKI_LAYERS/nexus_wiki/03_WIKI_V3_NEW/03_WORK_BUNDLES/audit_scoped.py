#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V3_SYS :: audit.py — فاحص الجودة الآلي (Quality Gate Auditor)
==============================================================

يحوّل كل عيب مكتشف يدويًا إلى فحص قابل للتشغيل الآلي.

Python 3 · **stdlib فقط** (لا pip ولا أي اعتماد خارجي).

------------------------------------------------------------------
نسخة مُنقّحة (SCOPED) — ``audit_scoped.py``
------------------------------------------------------------------
نسخة طبقية من ``V3_SYS/audit.py`` (الأصل لم يُمسّ). الإضافة الوحيدة هي
**نطاق قياس** لأن الشجرة الكاملة تنتج 247,102 مخالفة معظمها منتفخ بنيويًا
(terms_26k = 27,742 ملف بمخطط 3 أقسام بدل 6 + مجلدات عمل/مؤرشف).

  --scope full       بلا تغيير سلوكي إطلاقًا على الأصل (للتحقق/regression)
  --scope concepts   NB2/02_CONCEPTS/<قطاعات NN_*> فقط  (بلا terms_26k و _REPORTS)
  --scope atoms      NB2/02_CONCEPTS/terms_26k فقط
  --scope masters    NB2/03_MASTERS فقط

مبدآن يضمنان أن أرقام النطاق نقيّة لا مشوّهة:
  1) **النطاق يحدّ ملفات الفحص فقط**، ولا يمسّ «كون Univers» حلّ المراجع:
     C01 (الروابط المعلّقة) و C09 (القطاع بلا ماستر) و C10 (§18) تبقى
     قادرة على رؤية مفاتيح خارج النطاق، وإلا تحوّلت كل رابط عابر للنطاق
     إلى «معلّق» زائف.
  2) بِنية النطاق موثّقة في التقرير (scope + scope_base + scope_files).
  3) ``--cap 0`` = حفظ **كل** الـFindings بلا سقف (مطلوب لخريطة عيوب كل ملف)،
     و ``--dump-findings OUT.jsonl`` = تصريف Findings الخام سطرًا سطرًا.
     مع ``--scope full`` والسلوك الافتراضي يبقى الأصل متطابقًا (247,102).

------------------------------------------------------------------
البنية
------------------------------------------------------------------
* ``CHECKERS = {}``  — سجلّ الفواحص: كل فاحص يحمل
  ``id, name, severity(0-10), weight, run(ctx) -> list[Finding]``.
  (``ctx`` يحمل ``ctx.root`` = جذر الفحص، و``ctx.add()`` لإضافة Findings،
   و``ctx.corpus`` لقراءة الملفات مع كاش قراءة واحدة.)
* ``Finding = {id, checker, path, bytes, evidence, severity}``
* واحد فقط من الفواحص يقرأ الملفات فعليًا (``os.walk`` مرة واحدة)،
  والباقي يقرأ من كاش النصوص في الذاكرة.

------------------------------------------------------------------
CLI
------------------------------------------------------------------
  --root PATH            جذر الفحص (إلزامي)
  --checkers C01,C02     تشغيل مجموعة فرعية فقط
  --json OUT.json        تقرير JSON
  --md   OUT.md          تقرير Markdown
  --weight-sum           طباعة الأوزان ومجموعها (يجب = 100) والخروج
  --fail-on SEV          خروج code=1 إذا وُجدت مخالفات بخطورة >= SEV
  --max-examples N       عدد الأمثلة المحفوظة لكل فاحص في التقارير (افتراضي 3)
  --exclude NAME         استبعاد مسار (قابل للتكرار، افتراضيًا .git فقط)
  --scope S              full|concepts|atoms|masters (افتراضي full)
  --cap N                سقف Findings المحفوظة لكل فاحص (0 = بلا سقف)
  --dump-findings OUT    تفريغ كل الـFindings سطرًا سطرًا (JSONL)
  --quiet                لا تطبع الجدول

------------------------------------------------------------------
الأداء
------------------------------------------------------------------
مسار واحد عبر الشجرة + كاش نصوص بحدّ ذاكرة + إعادة استخدام القراءة
لجميع الفواحص الـ28. لا يقرأ أي فاحص ملفًا بنفسه مرتين.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from collections import OrderedDict, defaultdict

# ==================================================================
# 0) أدوات نصية مشتركة
# ==================================================================

FRONTMATTER_RE = re.compile(r"\A\ufeff?---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)
WIKILINK_RE = re.compile(r"\[\[([^\[\]\n|]+)")
SECTION_HEADING_RE = re.compile(r"(?m)^(#{1,6})[ \t]*(.+?)[ \t]*#*\s*$")
BOLD_LABEL_RE = re.compile(r"\*\*([^*\n]{2,40})\*\*")
TABLE_ROW_RE = re.compile(r"(?m)^\|\s*`?\s*\d")
CONCEPT_REF_RE = re.compile(r"Concept_[A-Za-z0-9_]")
NUM_TOKEN_RE = re.compile(r"\d{2,}\s*%|\b\d{2,}\b")
CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
FOUR_DIGITS_RE = re.compile(r"\d{4}")
GEN_SUFFIX_RE = re.compile(r"_v\d+$")
GEN_DECIMAL_RE = re.compile(r"_\d+\.\d+_")
SECTOR_DIR_RE = re.compile(r"^(\d{2})_")

# ------------------------------------------------------------------
# [SCOPED] نطاقات القياس — تُطبَّق على مجموعة ملفات الفحص فقط
# ------------------------------------------------------------------
SCOPES = ("full", "concepts", "atoms", "masters")

SCOPE_DOC = {
    "full": "الشجرة كاملة بلا تقليم (سلوك الأصل)",
    "concepts": "02_CONCEPTS/<قطاعات NN_*> فقط — بلا terms_26k و _REPORTS",
    "atoms": "02_CONCEPTS/terms_26k فقط (ذرّ الحقول — مخطط 3 أقسام)",
    "masters": "03_MASTERS فقط",
}

SCOPE_ROOTS = {
    "concepts": ("02_CONCEPTS",),
    "atoms": ("02_CONCEPTS/terms_26k",),
    "masters": ("03_MASTERS",),
}


def scope_keep(nb_rel, scope):
    """هل يدخل الملف ضمن النطاق؟ nb_rel = مساره نسبةً لجذر NB2."""
    if scope == "full":
        return True
    roots = SCOPE_ROOTS.get(scope)
    if not roots:
        raise ValueError("scope غير معروف: %r" % scope)
    for r in roots:
        if nb_rel == r:
            return True
        if not nb_rel.startswith(r + "/"):
            continue
        if scope == "concepts":
            # أبناء 02_CONCEPTS المباشرون المطابقون ^NN_ (يشمل 99_uncategorized)
            head = nb_rel[len(r) + 1:].split("/", 1)[0]
            return bool(SECTOR_DIR_RE.match(head))
        return True
    return False
MASTER_TAIL_RE = re.compile(r"_(\d{2})_[a-z0-9_]+$", re.I)
PLACEHOLDER_RE = re.compile(
    r"\bTODO\b|\bTBD\b|\bXXX\b|مفهوم استراتيجي في\s+عالم\s+الأعمال"
)

# الأقسام الستة المطلوبة (C14)
REQUIRED_SECTIONS = [
    ("التعريف", ("التعريف", "التعريف الإجرائي", "ما هو")),
    ("الآلية", ("الآلية", "آلية العمل", "كيف يعمل")),
    ("حدود الفناء", ("حدود الفناء", "الفناء", "متى لا يعمل")),
    ("الشروط", ("الشروط", "الشرائح", "متى يعمل")),
    ("الدليل", ("الدليل", "الاقتباسات", "الشواهد")),
    ("المصدرية", ("المصدرية", "المصادر", "المراجع")),
]
REQUIRED_SECTION_KEYS = [k for k, _ in REQUIRED_SECTIONS]

CONCEPT_SECTIONS = ("التعريف", "الآلية", "حدود الفناء", "الشروط", "الدليل", "المصدرية")
TENSION_TOKENS = ("التوترات", "توتر", "التعارضات", "المقارنات والتعارضات")


# ==================================================================
# 1) كاش الملفات — os.walk واحد + قراءة نصية واحدة
# ==================================================================

class FileRec:
    """سجلّ ملف واحد (بيانات وصفية فقط، بلا نص)."""

    __slots__ = ("path", "rel", "name", "stem", "dirname", "size", "mtime", "is_md")

    def __init__(self, path, rel, size, mtime):
        self.path = path
        self.rel = rel
        self.name = os.path.basename(path)
        self.stem = self.name[:-3] if self.name.endswith(".md") else self.name
        self.dirname = os.path.dirname(rel)
        self.size = size
        self.mtime = mtime
        self.is_md = self.name.endswith(".md")

    def __repr__(self):  # pragma: no cover
        return "FileRec(%r,%dB)" % (self.rel, self.size)


class Corpus:
    """مسح الشجرة مرة واحدة + كاش نصوص بحدّ ذاكرة."""

    def __init__(self, root, excludes=(".git",), cache_mb=512, jobs=1, scope="full"):
        self.root = os.path.abspath(root)
        self.excludes = tuple(excludes)
        self.jobs = max(1, int(jobs))
        self.scope = scope
        self.files = []
        self.dirs = []
        self._cache = OrderedDict()          # path -> text
        self._cache_bytes = 0
        self._cache_limit = cache_mb * 1024 * 1024
        self.bytes_read = 0
        self.files_read = 0
        self.walk_seconds = 0.0
        self.read_seconds = 0.0
        self._scan()
        self._build_universe()               # [SCOPED] قبل التقليم
        self._apply_scope()                  # [SCOPED]
        self._prefetch_markdown()

    # ---------- 1.1 المسح ----------

    def _excluded(self, name):
        for ex in self.excludes:
            if name == ex or (ex.endswith("*") and name.startswith(ex[:-1])):
                return True
        return False

    def _scan(self):
        t0 = time.time()
        excludes = self.excludes
        files, dirs = [], []
        for dirpath, dirnames, filenames in os.walk(self.root, followlinks=False):
            # التقليم أثناء المسح (يوفّر I/O على .git وما شابه)
            dirnames[:] = sorted(d for d in dirnames if d not in excludes)
            rel_dir = os.path.relpath(dirpath, self.root)
            rel_dir = "" if rel_dir == "." else rel_dir
            if rel_dir:
                dirs.append(rel_dir)
            # os.scandir يعطي size/mtime من مدخل الدليل بلا استدعاء stat إضافي
            with os.scandir(dirpath) as it:
                for ent in it:
                    try:
                        if not ent.is_file(follow_symlinks=False):
                            continue
                        st = ent.stat(follow_symlinks=False)
                    except OSError:
                        continue
                    rel = os.path.normpath(os.path.join(rel_dir, ent.name))
                    files.append(FileRec(ent.path, rel, st.st_size, st.st_mtime))
        self.files = files
        self.dirs = dirs
        self.walk_seconds = time.time() - t0

    # ---------- 1.1s [SCOPED] كون المراجع + تقليم النطاق ----------

    def _detect_scope_base(self):
        """يجد جذر NB2 النسبي: '' إذا كان root=NB2، أو '02_CONCEPTS' لو كان كذلك."""
        try:
            tops = set(os.listdir(self.root))
        except OSError:
            return ""
        if "02_CONCEPTS" in tops:
            return ""
        if "03_MASTERS" in tops:
            return ""
        return ""

    def _nb_rel(self, rel):
        return (self.scope_base + "/" + rel) if self.scope_base else rel

    def _build_universe(self):
        """«كون المراجع»: مفاتيح كل ملفات .md في الشجرة قبل التقليم.

        الغرض: ألّا يخلق التقليم مخالفات زائفة. C01 يحتاج أن يعرف أن
        ``[[Master_X]]`` موجود حتى لو كان 03_MASTERS خارج نطاق القياس.
        يُبنى من البيانات الوصفية فقط (لا قراءة I/O).
        """
        self.scope_base = self._detect_scope_base()
        stems, names, lower = set(), set(), set()
        master_recs, concept_recs = [], []
        for f in self.files:
            if not f.is_md:
                continue
            stems.add(f.stem)
            names.add(f.name)
            lower.add(f.stem.lower())
            if f.name.startswith("Master_"):
                master_recs.append(f)
            if f.name.startswith("Concept_"):
                concept_recs.append(f)
        self.universe_stems = stems
        self.universe_names = names
        self.universe_lower = lower
        self.universe_masters = master_recs
        self.universe_concepts = concept_recs

    def _apply_scope(self):
        """يقلّم self.files/self.dirs إلى نطاق القياس (لا يمسّ universe_*)."""
        if self.scope == "full":
            self.scope_kept = len(self.files)
            self.scope_dropped = 0
            return
        keep = [f for f in self.files
                if scope_keep(self._nb_rel(f.rel), self.scope)]
        dropped = len(self.files) - len(keep)
        keptdirs = {f.dirname for f in keep}
        dirs = [d for d in self.dirs if any(
            k == d or k.startswith(d + os.sep) for k in keptdirs)]
        self.files = keep
        self.dirs = sorted(dirs)
        self.scope_kept = len(keep)
        self.scope_dropped = dropped

    # ---------- 1.1b التحميل المسبق ----------

    def _prefetch_markdown(self):
        """يقرأ كل ملفات .md مرة واحدة (بـ threads) ليمتلئ الكاش.

        هذا هو سبب السرعة: f2fs هنا بطيء جدًا في القراءة، والفواحص الـ28
        كلها تشارك نفس الكاش فلا يُعاد أي قراءة.
        """
        t0 = time.time()
        targets = [f for f in self.files if f.is_md and f.size <= self._cache_limit]
        if not targets:
            self.read_seconds = time.time() - t0
            return
        data = {}
        nbytes = [0]

        def worker(rec):
            try:
                with open(rec.path, "rb") as fh:
                    raw = fh.read()
                txt = raw.decode("utf-8", "replace")
            except OSError:
                txt = ""
            data[rec.path] = txt
            nbytes[0] += len(raw)

        if self.jobs > 1:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=self.jobs) as ex:
                list(ex.map(worker, targets))
        else:
            for rec in targets:
                worker(rec)

        for rec in targets:
            txt = data.get(rec.path, "")
            self._cache[rec.path] = txt
            self._cache_bytes += len(txt)
        self.files_read = len(targets)
        self.bytes_read = nbytes[0]
        self.read_seconds = time.time() - t0

    # ---------- 1.2 كاش النصوص ----------

    def text(self, rec):
        """نص الملف (قراءة واحدة، مخزّنة مسبقًا). يعيد '' عند الفشل."""
        hit = self._cache.get(rec.path)
        if hit is not None:
            return hit
        try:
            with open(rec.path, "rb") as fh:
                t = fh.read().decode("utf-8", "replace")
        except OSError:
            t = ""
        self.files_read += 1
        self.bytes_read += rec.size
        self._cache[rec.path] = t
        self._cache_bytes += len(t)
        while self._cache_bytes > self._cache_limit and len(self._cache) > 1:
            _, old = self._cache.popitem(last=False)
            self._cache_bytes -= len(old)
        return t

    def body(self, rec):
        """نص الملف بعد نزع الـ frontmatter."""
        t = self.text(rec)
        m = FRONTMATTER_RE.match(t)
        return t[m.end():] if m else t

    def words(self, rec):
        return len(self.body(rec).split())

    # ---------- 1.3 التصنيف ----------

    def classify(self):
        """يحدّد المفاهيم/الماسترات/القطاعات/مجلدات الـmisc مرة واحدة."""
        concepts, masters, md_all, other_md = [], [], [], []
        concepts_dirs, masters_dirs = set(), set()
        for f in self.files:
            if not f.is_md:
                continue
            md_all.append(f)
            parent = os.path.basename(f.dirname)
            is_concept_named = f.name.startswith("Concept_")
            in_concepts_dir = parent in ("concepts", "02_CONCEPTS")
            if is_concept_named or in_concepts_dir:
                concepts.append(f)
                concepts_dirs.add(f.dirname)
            elif f.name.startswith("Master_"):
                masters.append(f)
                masters_dirs.add(f.dirname)
            else:
                other_md.append(f)
        self.md_all = md_all
        self.concepts = concepts
        self.masters = masters
        self.other_md = other_md
        self.concepts_dirs = concepts_dirs
        self.masters_dirs = masters_dirs
        return self

    # ---------- 1.4 مساعدات ----------

    def find_dirs(self, *names):
        """أسماء مجلدات مطلقة داخل الجذر (بحث محدود العمق)."""
        out = []
        for d in self.dirs + [""]:
            base = os.path.basename(d) if d else ""
            if base in names:
                out.append(d)
        return sorted(set(out))

    def subtree_files(self, rel_dir, pred=None):
        pref = rel_dir + os.sep if rel_dir else ""
        return [f for f in self.files
                if (not pref or f.rel.startswith(pref)) and (pred is None or pred(f))]

    def direct_file_count(self, rel_dir):
        return sum(1 for f in self.files if f.dirname == rel_dir)

    def top_breakdown(self, limit=15):
        c = defaultdict(lambda: [0, 0])
        for f in self.files:
            top = f.rel.split(os.sep)[0] if os.sep in f.rel else "(root)"
            c[top][0] += 1
            c[top][1] += f.size
        items = sorted(c.items(), key=lambda kv: -kv[1][1])[:limit]
        return [{"dir": k, "files": v[0], "bytes": v[1]} for k, v in items]

    # ---------- 1.5 [SCOPED] عدّ concepts لكل قطاع من كون المراجع ----------

    def sector_concept_counts(self, use_universe=False):
        """{اسم قطاع NN_*: عدد Concept_*.md} — أبناء 02_CONCEPTS المباشرون فقط.

        نفس منطق C10 الأصلي تمامًا (الأبناء المباشرون، terms_26k مستثنى
        لأنه ليس ابنًا مباشرًا)، لكنه يقرأ من كون المراجع حين تكون
        الـconcepts خارج مجموعة الفحص (نطاق=masters).
        """
        counts = defaultdict(int)
        if not use_universe:
            roots = [d for d in self.find_dirs("02_CONCEPTS", "concepts") if d]
            for f in self.concepts:
                for root in roots:
                    prefix = root + os.sep
                    if f.dirname.startswith(prefix):
                        rest = f.dirname[len(prefix):]
                        if os.sep not in rest and SECTOR_DIR_RE.match(rest):
                            counts[rest] += 1
                        break
            return counts
        # نسخة universe: نفس القاعدة على *مجلد* الملف نسبةً لجذر NB2
        pre = ("%s/02_CONCEPTS/" % self.scope_base) if self.scope_base \
            else "02_CONCEPTS/"
        for f in self.universe_concepts:
            nb_dir = os.path.dirname(self._nb_rel(f.rel))
            if not nb_dir.startswith(pre):
                continue
            rest = nb_dir[len(pre):]
            if os.sep in rest:
                continue
            if SECTOR_DIR_RE.match(rest):
                counts[rest] += 1
        return counts


# ==================================================================
# 2) Finding + سجل الفواحص
# ==================================================================

class Finding(dict):
    """الشكل الثابت: {id, checker, path, bytes, evidence, severity}."""

    def __init__(self, fid, checker, path, nbytes, evidence, severity):
        super().__init__(id=fid, checker=checker, path=path, bytes=nbytes,
                         evidence=evidence, severity=severity)


class Checker:
    __slots__ = ("id", "name", "severity", "weight", "run", "threshold")

    def __init__(self, cid, name, severity, weight, run, threshold="0"):
        self.id = cid
        self.name = name
        self.severity = severity
        self.weight = weight
        self.run = run
        self.threshold = threshold


CHECKERS = OrderedDict()


def checker(cid, name, severity, weight, threshold="0"):
    """مُزخرِف تسجيل الفاحص في CHECKERS."""
    def deco(fn):
        if cid in CHECKERS:
            raise RuntimeError("checker id مكرر: %s" % cid)
        CHECKERS[cid] = Checker(cid, name, severity, weight, fn, threshold)
        return fn
    return deco


class Ctx:
    """سياق التنفيذ: root + corpus + سجل الملاحظات.

    ``cap`` يحدّ Findings المحفوظة لكل فاحص حتى تبقى التقارير قابلة للقراءة
    على الشجارت الضخمة؛ ``ctx.add`` يُرجع None بعد تجاوز السقف.
    """

    def __init__(self, root, corpus, checker_id, severity, max_examples, cap=4000):
        self.root = root
        self.corpus = corpus
        self.checker_id = checker_id
        self.severity = severity
        self.max_examples = max_examples
        self.cap = None if (cap is not None and cap <= 0) else cap
        self.unbounded = self.cap is None
        self.findings = []
        self.notes = []
        self.total = 0
        self._n = 0

    def add(self, path, nbytes, evidence):
        """يسجّل مخالفة. يعيد True/False للقبول."""
        self.total += 1
        if self.cap is not None and len(self.findings) >= self.cap:
            return False
        self._n += 1
        self.findings.append(Finding(
            "%s#%d" % (self.checker_id, self._n), self.checker_id,
            path, nbytes, evidence, self.severity))
        return True

    def note(self, msg):
        self.notes.append(msg)


# ==================================================================
# 3) الفواحص الـ28
# ==================================================================

# ------------------------------------------------------------------
# C01 — روابط [[ ]] معلّقة
# ------------------------------------------------------------------
@checker("C01", "روابط [[ ]] معلّقة", 8, 7)
def c01_dangling_wikilinks(ctx):
    c = ctx.corpus
    # [SCOPED] في النطاقات المصغّرة نحلّ الروابط على «كون المراجع» (كامل الشجرة)
    # حتى لا يتحوّل كل رابط عابر للنطاق إلى «معلّق» زائف.
    if c.scope != "full":
        known = c.universe_stems | c.universe_names
        known_lower = c.universe_lower
    else:
        known = set()
        for f in c.files:
            if f.is_md:
                known.add(f.stem)
                known.add(f.name[:-3] if f.name.endswith(".md") else f.name)
        known_lower = {k.lower() for k in known}
    dangling = defaultdict(set)
    for f in c.md_all:
        for target in WIKILINK_RE.findall(c.text(f)):
            t = target.strip()
            if not t:
                continue
            if t in known or t.lower() in known_lower:
                continue
            dangling[t].add(f.rel)
    for t in sorted(dangling):
        srcs = sorted(dangling[t])
        ctx.add("[[%s]]" % t, 0, "معلّق في %d ملف، مثال: %s" % (len(srcs), srcs[0]))
    if not dangling:
        ctx.note("لا روابط معلّقة")


# ------------------------------------------------------------------
# C02 — كعبات <300B
# ------------------------------------------------------------------
@checker("C02", "كعبات <300 بايت", 6, 5)
def c02_stubs(ctx):
    n = 0
    for f in ctx.corpus.md_all:
        if f.size < 300:
            n += 1
            ctx.add(f.rel, f.size, "حجم %dB < 300B" % f.size)
    if not n:
        ctx.note("لا كعبات")


# ------------------------------------------------------------------
# C03 — تكرار حرفي بين concept
# ------------------------------------------------------------------
@checker("C03", "تكرار حرفي بين concept", 7, 5)
def c03_verbatim_duplicates(ctx):
    c = ctx.corpus
    by_hash = defaultdict(list)
    for f in c.concepts:
        body = c.body(f)
        norm = " ".join(body.split())          # نزع المسافات المتكررة
        if not norm:
            continue
        h = hashlib.sha256(norm.encode("utf-8", "replace")).hexdigest()
        by_hash[h].append(f)
    dupes = 0
    for h, group in by_hash.items():
        if len(group) < 2:
            continue
        dupes += 1
        group.sort(key=lambda f: f.rel)
        ctx.add(group[0].rel, group[0].size,
                "sha256[:12]=%s متطابق في %d ملف: %s" %
                (h[:12], len(group), " | ".join(g.rel for g in group[:ctx.max_examples])))
    if not dupes:
        ctx.note("لا تكرار حرفي")


# ------------------------------------------------------------------
# C04 — concept بلا اقتباس/مصدر
# ------------------------------------------------------------------
@checker("C04", "concept بلا اقتباس/مصدر", 8, 6)
def c04_no_evidence(ctx):
    c = ctx.corpus
    n = 0
    for f in c.concepts:
        t = c.text(f)
        has = ("## الدليل" in t) or ("## الاقتباسات" in t) or ("`" in t) or ("channel:" in t)
        if not has:
            n += 1
            ctx.add(f.rel, f.size, "لا '## الدليل' ولا backtick ولا 'channel:'")
    if not n:
        ctx.note("كل المفاهيم فيها مصدر")


# ------------------------------------------------------------------
# C05 — concept بلا «حدود الفناء»
# ------------------------------------------------------------------
@checker("C05", "concept بلا «حدود الفناء»", 8, 6)
def c05_no_fence(ctx):
    toks = ("حدود الفناء", "متى لا يعمل", "الفناء")
    n = 0
    for f in ctx.corpus.concepts:
        t = ctx.corpus.text(f)
        if not any(k in t for k in toks):
            n += 1
            ctx.add(f.rel, f.size, "لا يوجد: %s" % " / ".join(toks))
    if not n:
        ctx.note("كل المفاهيم فيها حدود الفناء")


# ------------------------------------------------------------------
# C06 — concept بلا «الآلية»
# ------------------------------------------------------------------
@checker("C06", "concept بلا «الآلية»", 7, 6)
def c06_no_mechanism(ctx):
    toks = ("الآلية", "آلية العمل")
    n = 0
    for f in ctx.corpus.concepts:
        t = ctx.corpus.text(f)
        if not any(k in t for k in toks):
            n += 1
            ctx.add(f.rel, f.size, "لا يوجد: %s" % " / ".join(toks))
    if not n:
        ctx.note("كل المفاهيم فيها الآلية")


# ------------------------------------------------------------------
# C07 — ماستر بأقسام <18
# ------------------------------------------------------------------
@checker("C07", "ماستر بأقسام <18", 8, 4)
def c07_master_sections(ctx):
    c = ctx.corpus
    if not c.masters:
        ctx.note("لا ماسترات في هذا الجذر")
    for f in c.masters:
        n = sum(1 for line in c.text(f).splitlines() if line.startswith("## §"))
        if n < 18:
            ctx.add(f.rel, f.size, "عدد أقسام '## §' = %d < 18" % n)


# ------------------------------------------------------------------
# C08 — concept مكرر الاسم
# ------------------------------------------------------------------
@checker("C08", "concept مكرر الاسم", 5, 3)
def c08_duplicate_name(ctx):
    c = ctx.corpus
    # (أ) نفس المجلد، basename متطابق بعد تجاهل حالة الأحرف
    by_dir = defaultdict(lambda: defaultdict(list))
    for f in c.concepts:
        by_dir[f.dirname][f.stem.lower()].append(f)
    n = 0
    for d, m in sorted(by_dir.items()):
        for key, group in sorted(m.items()):
            if len(group) < 2:
                continue
            n += 1
            group.sort(key=lambda f: f.rel)
            ctx.add(group[0].rel, group[0].size,
                    "تطابق اسم (case-insensitive) في %s: %s" %
                    (d or "(root)", " | ".join(g.rel for g in group)))
    # (ب) نفس الاسم بالضبط داخل قطاع واحد (شجرة فرعية)
    sectors = ctx.sector_map()
    by_sector = defaultdict(lambda: defaultdict(list))
    for f in c.concepts:
        sec = sectors.get(f.dirname)
        if sec:
            by_sector[sec][f.stem].append(f)
    for sec, m in sorted(by_sector.items()):
        for key, group in sorted(m.items()):
            if len(group) < 2:
                continue
            n += 1
            group.sort(key=lambda f: f.rel)
            ctx.add(group[0].rel, group[0].size,
                    "اسم مكرر داخل قطاع %s: %s" %
                    (sec, " | ".join(g.rel for g in group[:ctx.max_examples])))
    if not n:
        ctx.note("لا أسماء مكررة")


# ------------------------------------------------------------------
# C09 — قطاع بلا ماستر
# ------------------------------------------------------------------
@checker("C09", "قطاع بلا ماستر", 6, 3)
def c09_sector_without_master(ctx):
    """يقارن مجلدات 02_CONCEPTS المباشرة بـ 03_MASTERS المباشرة (كما في المواصفة)."""
    c = ctx.corpus
    # [SCOPED] في نطاق=concepts الماسترات خارج مجموعة الفحص، فنقرأها من
    # «كون المراجع» وإلا صار كل قطاع «بلا ماستر» زائفًا.
    masters = c.masters if (c.scope in ("full", "masters") and c.masters) \
        else c.universe_masters
    # 1) مجلدات القطاعات: أبناء 02_CONCEPTS المباشرون المطابقون ^NN_ (بلا 99_*)
    concept_roots = [d for d in c.find_dirs("02_CONCEPTS", "concepts") if d]
    if c.scope == "concepts":
        # النطاق يحذف 02_CONCEPTS كجذر من self.dirs ⇒ نعيد بناءه صراحةً
        concept_roots = ["02_CONCEPTS"]
    if not concept_roots:
        ctx.note("لا مجلد 02_CONCEPTS في هذا الجذر (تخطّي)")
        return
    sector_dirs = set()
    for root in concept_roots:
        prefix = root + os.sep
        for d in c.dirs:
            if not d.startswith(prefix):
                continue
            rest = d[len(prefix):]
            if os.sep in rest:            # أبناء المباشرين فقط
                continue
            base = rest
            if SECTOR_DIR_RE.match(base) and not base.startswith("99"):
                sector_dirs.add(base)
    if not sector_dirs:
        ctx.note("لا قطاعات (NN_*) مباشرة تحت 02_CONCEPTS — تخطّي")
        return

    # 2) القطاعات المغطّاة بماستر: باسم المجلد أو بلاحقة اسم الماستر
    master_sectors = set()
    for f in masters:
        parent = os.path.basename(f.dirname) or ""
        if SECTOR_DIR_RE.match(parent) and not parent.startswith("99"):
            master_sectors.add(parent)
        m2 = MASTER_TAIL_RE.search(f.stem)
        if m2:
            master_sectors.add(m2.group(1))
        fm = FRONTMATTER_RE.match(c.text(f))
        if fm:
            cl = re.search(r"(?m)^cluster\s*:\s*(\S+)", fm.group(1))
            if cl:
                master_sectors.add(cl.group(1).strip("'\""))
    missing = sorted(sector_dirs - master_sectors)
    for root in concept_roots:
        for s in missing:
            n = c.direct_file_count(root + os.sep + s)
            if n:
                ctx.add(s, 0, "قطاع '%s' (%d ملف) بلا ماستر — الماسترات المتاحة: %s"
                        % (s, n, sorted(master_sectors) or "لا شيء"))
    ctx.note("قطاعات: %d · مغطّاة: %d · بلا ماستر: %d"
             % (len(sector_dirs), len(sector_dirs) - len(missing), len(missing)))


# ------------------------------------------------------------------
# C10 — شرط §18
# ------------------------------------------------------------------
@checker("C10", "شرط §18 (صفوف الجدول = concepts القطاع)", 8, 4)
def c10_section18(ctx):
    c = ctx.corpus
    if not c.masters:
        ctx.note("لا ماسترات في هذا الجذر (تخطّي)")
        return
    # عدّ concepts لكل قطاع: المجلد المباشر NN_* تحت 02_CONCEPTS
    # [SCOPED] في نطاق=masters تكون الـconcepts خارج المجموعة ⇒ العدّ من كون المراجع
    sec_counts = c.sector_concept_counts(use_universe=(c.scope == "masters"))
    concept_roots = [d for d in c.find_dirs("02_CONCEPTS", "concepts") if d]
    if c.scope == "masters":
        concept_roots = ["02_CONCEPTS"]
    sec_paths = {}
    sec_by_num = {}
    for s in sec_counts:
        sec_by_num.setdefault(s.split("_", 1)[0], s)
    for f in c.masters:
        text = c.text(f)
        has18, cnt = _section18_rows(text)
        if cnt == 0:
            ctx.add(f.rel, f.size,
                    "لا جدول مفاهيم في §18%s" % ("" if has18 else " (القسم §18 غير موجود)"))
            continue
        key = os.path.basename(f.dirname)
        target = key if key in sec_counts else None
        if target is None:
            m2 = MASTER_TAIL_RE.search(f.stem)
            cand = m2.group(1) if m2 else None
            if cand:
                target = sec_by_num.get(cand)
            if target is None:
                fm = FRONTMATTER_RE.match(text)
                if fm:
                    cl = re.search(r"(?m)^cluster\s*:\s*(\S+)", fm.group(1))
                    if cl:
                        cc = cl.group(1).strip("'\"")
                        target = cc if cc in sec_counts else sec_by_num.get(
                            cc.split("_", 1)[0])
        if not target or target not in sec_counts:
            ctx.add(f.rel, f.size,
                    "تعذّر ربط الماستر بقطاع (master=%s, rows=%d, القطاعات=%s)"
                    % (f.stem, cnt, sorted(sec_counts) or "لا شيء"))
            continue
        expect = sec_counts[target]
        if cnt != expect:
            ctx.add(f.rel, f.size,
                    "§18 = %d صف · concepts(%s) = %d · فرق %+d"
                    % (cnt, target, expect, cnt - expect))


def _section18_rows(text):
    """(هل يوجد قسم §18، عدد صفوف المفاهيم داخله).

    صف المفهوم: إمّا يبدأ برقم (مُرقّم) أو يشير إلى ``Concept_*`` — لأن بعض
    الماسترات تكتب العمود الأول كـ `` `Concept_X` `` بدل رقم.
    """
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^##\s*§\s*18\b", ln):
            start = i + 1
            break
    if start is None:
        return False, 0
    cnt = 0
    for ln in lines[start:]:
        if ln.startswith("## §"):
            break
        # صف مفهوم: إمّا يبدأ برقم (مُرقّم) أو يشير إلى Concept_*
        if not ln.startswith("|"):
            continue
        if TABLE_ROW_RE.match(ln) or CONCEPT_REF_RE.search(ln):
            cnt += 1
    return True, cnt


# ------------------------------------------------------------------
# C11 — رقم بلا ⚠️ ولا مصدر
# ------------------------------------------------------------------
@checker("C11", "رقم بلا ⚠️ ولا مصدر", 6, 4)
def c11_bare_number(ctx):
    c = ctx.corpus
    n = 0
    for f in c.concepts:
        t = c.text(f)
        if not NUM_TOKEN_RE.search(t):
            continue
        if "\u26a0" in t or "مصدر" in t:
            continue
        n += 1
        m = NUM_TOKEN_RE.search(t)
        ctx.add(f.rel, f.size, "رقم بلا تنبيه/مصدر، مثال: %r" % t[max(0, m.start() - 25):m.end() + 25])
    if not n:
        ctx.note("لا أرقام عارية")


# ------------------------------------------------------------------
# C12 — فهرس stale
# ------------------------------------------------------------------
@checker("C12", "فهرس البحث stale", 4, 2)
def c12_stale_index(ctx):
    c = ctx.corpus
    idx = [f for f in c.files if f.rel.endswith((".json.gz", ".json", ".idx", ".db"))
           and ("04_SEARCH" in f.rel or "index" in f.name.lower())]
    if not idx:
        ctx.note("لا ملف فهرس (04_SEARCH/index.json.gz) — تخطّي")
        return
    newest_concept = max((f.mtime for f in c.concepts), default=0.0)
    for f in sorted(idx, key=lambda x: x.rel)[:5]:
        if newest_concept and f.mtime < newest_concept:
            delta = newest_concept - f.mtime
            ctx.add(f.rel, f.size,
                    "mtime الفهرس أقدم من أحدث concept بـ %.0f ثانية" % delta)


# ------------------------------------------------------------------
# C13 — concept بلا wikilink
# ------------------------------------------------------------------
@checker("C13", "concept بلا wikilink", 5, 3)
def c13_no_wikilink(ctx):
    c = ctx.corpus
    n = 0
    for f in c.concepts:
        if "[[" not in c.text(f):
            n += 1
            ctx.add(f.rel, f.size, "صفر روابط [[ ]]")
    if not n:
        ctx.note("كل المفاهيم فيها wikilink")


# ------------------------------------------------------------------
# C14 — concept بلا sections كاملة
# ------------------------------------------------------------------
@checker("C14", "concept بلا الأقسام الستة كاملة", 9, 7)
def c14_missing_sections(ctx):
    c = ctx.corpus
    n = 0
    for f in c.concepts:
        t = c.text(f)
        heads = " \n ".join(m.group(2) for m in SECTION_HEADING_RE.finditer(t))
        bolds = " \n ".join(BOLD_LABEL_RE.findall(t))
        pool = heads + "\n" + bolds
        missing = [key for key, alts in REQUIRED_SECTIONS
                   if not any(a in pool for a in alts)]
        if missing:
            n += 1
            ctx.add(f.rel, f.size, "أقسام ناقصة: %s" % "، ".join(missing))
    if not n:
        ctx.note("كل المفاهيم مكتملة الأقسام")


# ------------------------------------------------------------------
# C15 — أسماء مولّدة آلياً
# ------------------------------------------------------------------
@checker("C15", "أسماء مولّدة آلياً", 4, 2)
def c15_generated_names(ctx):
    n = 0
    for f in ctx.corpus.concepts:
        stem = f.stem
        why = []
        if GEN_DECIMAL_RE.search(stem):
            why.append("نمط _0.5_")
        if GEN_SUFFIX_RE.search(stem):
            why.append("لاحقة _vN")
        if FOUR_DIGITS_RE.search(stem):
            why.append("أربعة أرقام متتالية")
        if why:
            n += 1
            ctx.add(f.rel, f.size, "%s في الاسم" % " + ".join(why))
    if not n:
        ctx.note("لا أسماء مولّدة آلياً")


# ------------------------------------------------------------------
# C16 — حشو / Ukrainian
# ------------------------------------------------------------------
@checker("C16", "حشو / Ukrainian", 5, 2)
def c16_padding(ctx):
    c = ctx.corpus
    n = 0
    for f in c.md_all:
        t = c.text(f)
        m = CYRILLIC_RE.search(t)
        hit = ("نص سيريليكي (Ukrainian): %s" % m.group(0)) if m else ""
        if not m:
            m = PLACEHOLDER_RE.search(t)
            hit = ("عبارة حشو: %s" % m.group(0)) if m else ""
        if not hit:
            continue
        n += 1
        snippet = t[max(0, m.start() - 20):m.end() + 40].replace("\n", " ")
        ctx.add(f.rel, f.size, "%s — %s" % (hit, _short(snippet, 60)))
    if not n:
        ctx.note("لا حشو/نص سيريليكي")


# ------------------------------------------------------------------
# C17 — ماستر بلا حدود فناء
# ------------------------------------------------------------------
@checker("C17", "ماستر بلا حدود فناء", 7, 3)
def c17_master_no_fence(ctx):
    c = ctx.corpus
    if not c.masters:
        ctx.note("لا ماسترات في هذا الجذر (تخطّي)")
    toks = ("حدود الفناء", "متى لا يعمل", "الفناء")
    for f in c.masters:
        t = c.text(f)
        if not any(k in t for k in toks):
            ctx.add(f.rel, f.size, "لا حدود فناء")


# ------------------------------------------------------------------
# C18 — بوابات Master SPEC
# ------------------------------------------------------------------
@checker("C18", "بوابات Master SPEC", 9, 4, threshold="4 sub-gates")
def c18_master_gates(ctx):
    c = ctx.corpus
    if not c.masters:
        ctx.note("لا ماسترات في هذا الجذر (تخطّي)")
        return
    for f in c.masters:
        text = c.text(f)
        total = len(text.split())
        secs = _split_sections(text)
        s4 = secs.get(4, "")
        s15 = secs.get(15, "")
        w4 = len(s4.split())
        w15 = len(s15.split())
        nsec = sum(1 for line in text.splitlines() if line.startswith("## §"))
        fails = []
        if total < 10000:
            fails.append("كلمات=%d <10000" % total)
        if total and (w4 / float(total)) < 0.40:
            fails.append("§4=%d كلمة = %.2f%% <40%%" % (w4, 100.0 * w4 / total))
        if w15 < 1800:
            fails.append("§15=%d كلمة <1800" % w15)
        if nsec < 18:
            fails.append("أقسام=%d <18" % nsec)
        if fails:
            ctx.add(f.rel, f.size, " | ".join(fails))


def _split_sections(text):
    """{رقم §: نص القسم} لماسترات §§."""
    out = {}
    cur = None
    buf = []
    for ln in text.splitlines():
        m = re.match(r"^##\s*§\s*(\d+)", ln)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur = int(m.group(1))
            buf = []
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


# ------------------------------------------------------------------
# C19 — YAML ناقص
# ------------------------------------------------------------------
@checker("C19", "YAML ناقص (---/type/version/sections)", 6, 3)
def c19_incomplete_yaml(ctx):
    c = ctx.corpus
    if not c.masters:
        ctx.note("لا ماسترات في هذا الجذر (تخطّي)")
    for f in c.masters:
        t = c.text(f)
        m = FRONTMATTER_RE.match(t)
        if not m:
            ctx.add(f.rel, f.size, "لا frontmatter ---")
            continue
        fm = m.group(1)
        miss = [k for k in ("type:", "version:", "sections:") if k not in fm]
        if miss:
            ctx.add(f.rel, f.size, "مفاتيح ناقصة: %s" % "، ".join(miss))


# ------------------------------------------------------------------
# C20 — نسخة مطابقة بين مجلدين (تراجع v1)
# ------------------------------------------------------------------
@checker("C20", "نسخة مطابقة بين مجلدين (تراجع)", 7, 3)
def c20_cross_dir_copy(ctx):
    c = ctx.corpus
    by_hash = defaultdict(list)
    for f in c.md_all:
        if f.size > 1_048_576 or f.size == 0:
            continue
        h = hashlib.sha256(c.text(f).encode("utf-8", "replace")).hexdigest()
        by_hash[h].append(f)
    n = 0
    for h, group in by_hash.items():
        dirs = {g.dirname for g in group}
        if len(dirs) < 2:
            continue
        n += 1
        group.sort(key=lambda f: f.rel)
        ctx.add(group[0].rel, group[0].size,
                "sha256[:12]=%s في %d مجلد: %s" %
                (h[:12], len(dirs), " | ".join(g.rel for g in group[:ctx.max_examples + 2])))
    if not n:
        ctx.note("لا نسخ متطابقة بين مجلدين")


# ------------------------------------------------------------------
# C21 — مجلد >1000 ملف
# ------------------------------------------------------------------
@checker("C21", "مجلد >1000 ملف", 3, 2)
def c21_big_dir(ctx):
    c = ctx.corpus
    n = 0
    for d in c.dirs:
        cnt = c.direct_file_count(d)
        if cnt > 1000:
            n += 1
            ctx.add(d or "(root)", 0, "ملفات مباشرة = %d > 1000" % cnt)
    if not n:
        ctx.note("لا مجلد يتجاوز 1000 ملف")


# ------------------------------------------------------------------
# C22 — حجم 99_misc ≤3% من 02_CONCEPTS
# ------------------------------------------------------------------
@checker("C22", "حجم 99_misc ≤3% من 02_CONCEPTS", 5, 2, threshold="≤3%")
def c22_misc_size(ctx):
    c = ctx.corpus
    misc_dirs = sorted(d for d in c.dirs
                       if os.path.basename(d).startswith("99_misc")
                       or os.path.basename(d).startswith("99_uncategorized"))
    if not misc_dirs:
        ctx.note("لا مجلد 99_misc/99_uncategorized — تخطّي")
        return
    tot_b = sum(f.size for f in c.concepts) or 1
    tot_n = len(c.concepts) or 1
    misc_b = sum(f.size for f in c.concepts
                 if any(f.dirname == d or f.dirname.startswith(d + os.sep) for d in misc_dirs))
    misc_n = sum(1 for f in c.concepts
                 if any(f.dirname == d or f.dirname.startswith(d + os.sep) for d in misc_dirs))
    ratio_b = 100.0 * misc_b / tot_b
    ratio_n = 100.0 * misc_n / tot_n
    if ratio_b > 3.0:
        ctx.add(os.pathsep.join(misc_dirs), misc_b,
                "99_misc = %.2f%% من حجم المفاهيم (حد 3%%) · %.2f%% من العدد "
                "(%d/%d مفهوم، %d/%d بايت)" %
                (ratio_b, ratio_n, misc_n, tot_n, misc_b, tot_b))
    else:
        ctx.note("99_misc = %.2f%% (ضمن 3%%)" % ratio_b)


# ------------------------------------------------------------------
# C23 — concept بلا أقسام توتر (تقرير فقط)
# ------------------------------------------------------------------
@checker("C23", "concept بلا أقسام توتر (تقرير فقط)", 0, 0, threshold="—")
def c23_no_tension(ctx):
    c = ctx.corpus
    n = 0
    for f in c.concepts:
        t = c.text(f)
        if not any(k in t for k in TENSION_TOKENS):
            n += 1
            ctx.add(f.rel, f.size, "لا قسم توترات/تعارضات")
    if not n:
        ctx.note("كل المفاهيم فيها توترات")


# ------------------------------------------------------------------
# C24 — concept <250 كلمة
# ------------------------------------------------------------------
@checker("C24", "concept <250 كلمة", 6, 4)
def c24_too_short(ctx):
    c = ctx.corpus
    n = 0
    for f in c.concepts:
        w = c.words(f)
        if w < 250:
            n += 1
            ctx.add(f.rel, f.size, "%d كلمة < 250" % w)
    if not n:
        ctx.note("لا concepts قصيرة")


# ------------------------------------------------------------------
# C25 — concept >600 كلمة (≤3%)
# ------------------------------------------------------------------
@checker("C25", "concept >600 كلمة (≤3%)", 4, 2, threshold="≤3%")
def c25_too_long(ctx):
    c = ctx.corpus
    longs = [f for f in c.concepts if c.words(f) > 600]
    total = len(c.concepts) or 1
    ratio = 100.0 * len(longs) / total
    # [SCOPED] بلا سقف (--cap 0) ⇒ يُسرد كل concept طويل سطرًا سطرًا
    # (سلوك الأصل يبقى كما هو مع السقف الافتراضي: 10 أمثلة + سطر تجميعي)
    listed = sorted(longs, key=lambda x: -x.size)
    if not ctx.unbounded:
        listed = listed[:max(ctx.max_examples, 10)]
    for f in listed:
        ctx.add(f.rel, f.size, "%d كلمة > 600" % c.words(f))
    if ratio > 3.0:
        ctx.add("(تجميعي)", 0, "نسبة >600 كلمة = %.2f%% (%d/%d) تتجاوز 3%%" %
                (ratio, len(longs), total))
    else:
        ctx.note("نسبة >600 كلمة = %.2f%% (ضمن 3%%)" % ratio)


# ------------------------------------------------------------------
# C26 — concept بلا «## المصدرية»
# ------------------------------------------------------------------
@checker("C26", "concept بلا «## المصدرية»", 7, 4)
def c26_no_provenance(ctx):
    c = ctx.corpus
    n = 0
    for f in c.concepts:
        t = c.text(f)
        if "## المصدرية" not in t and "## المصادر" not in t and "## المراجع" not in t:
            n += 1
            ctx.add(f.rel, f.size, "لا '## المصدرية' ولا '## المصادر' ولا '## المراجع'")
    if not n:
        ctx.note("كل المفاهيم فيها مصدرية")


# ------------------------------------------------------------------
# C27 — placeholders
# ------------------------------------------------------------------
@checker("C27", "placeholders (TODO/TBD/XXX)", 5, 2)
def c27_placeholders(ctx):
    c = ctx.corpus
    n = 0
    for f in c.md_all:
        t = c.text(f)
        for m in PLACEHOLDER_RE.finditer(t):
            n += 1
            snippet = t[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")
            ctx.add(f.rel, f.size, "«%s» — %s" % (m.group(0), snippet))
    if not n:
        ctx.note("لا placeholders")


# ------------------------------------------------------------------
# C28 — concepts بلا sources غير فارغ
# ------------------------------------------------------------------
@checker("C28", "concepts بلا sources غير فارغ", 7, 2)
def c28_empty_sources(ctx):
    c = ctx.corpus
    n = 0
    for f in c.concepts:
        t = c.text(f)
        m = FRONTMATTER_RE.match(t)
        if not m:
            n += 1
            ctx.add(f.rel, f.size, "لا frontmatter ⇒ لا sources")
            continue
        fm = m.group(1)
        vals = {}
        for key in ("sources", "sources_channels", "source_channels", "sources_count",
                    "source", "source_master", "provenance_account"):
            km = re.search(r"(?m)^%s\s*:\s*(.+?)\s*$" % re.escape(key), fm)
            if km:
                vals[key] = km.group(1).strip()
        if not vals:
            n += 1
            ctx.add(f.rel, f.size, "لا مفتاح مصادر في frontmatter")
            continue
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
        if empty:
            n += 1
            ctx.add(f.rel, f.size, "مصادر فارغة: %s" %
                    ", ".join("%s=%s" % kv for kv in sorted(vals.items())))
    if not n:
        ctx.note("كل المفاهيم فيها مصادر")


# ==================================================================
# 4) سياق مشترك للقطاعات
# ==================================================================

_SECTOR_CACHE = {}


def sector_map_for(corpus):
    """{مجلد المفاهيم -> اسم القطاع}"""
    key = id(corpus)
    hit = _SECTOR_CACHE.get(key)
    if hit is not None:
        return hit
    mapping = {}
    parents = sorted({f.dirname for f in corpus.concepts}, key=lambda d: (d.count(os.sep), d))
    for d in parents:
        base = os.path.basename(d)
        m = SECTOR_DIR_RE.match(base)
        if m:
            mapping[d] = base
            continue
        # داخل شجرة قطاع (مثل terms_26k/01_outreach/part_01)
        parts = d.split(os.sep)
        for p in reversed(parts):
            if SECTOR_DIR_RE.match(p):
                mapping[d] = p
                break
        else:
            mapping[d] = None
    _SECTOR_CACHE[key] = mapping
    return mapping


def _ctx_sector_map(self):
    return sector_map_for(self.corpus)


Ctx.sector_map = _ctx_sector_map


# ==================================================================
# 5) المحرّك + التقارير
# ==================================================================

def run_audit(root, only=None, max_examples=3, excludes=(".git",), verbose=True,
              jobs=1, scope="full", cap=4000):
    t0 = time.time()
    corpus = Corpus(root, excludes=excludes, jobs=jobs, scope=scope)
    if verbose:
        sys.stderr.write("[scan] %d ملف · %d مجلد · %.2fs (قراءة %.2fs)%s\n"
                         % (len(corpus.files), len(corpus.dirs), corpus.walk_seconds,
                            corpus.read_seconds,
                            "" if scope == "full" else
                            " · scope=%s (أُبقي %d · أُسقط %d من %d)"
                            % (scope, corpus.scope_kept, corpus.scope_dropped,
                               corpus.scope_kept + corpus.scope_dropped)))
    corpus.classify()
    if verbose:
        sys.stderr.write("[class] concepts=%d masters=%d md=%d\n"
                         % (len(corpus.concepts), len(corpus.masters), len(corpus.md_all)))

    results = []
    for cid, chk in CHECKERS.items():
        if only and cid not in only:
            continue
        t1 = time.time()
        ctx = Ctx(root, corpus, cid, chk.severity, max_examples, cap=cap)
        err = None
        try:
            chk.run(ctx)
        except Exception as exc:  # pragma: no cover
            err = "%s: %s" % (type(exc).__name__, exc)
            if verbose:
                sys.stderr.write("[ERR] %s %s\n" % (cid, err))
        results.append({
            "id": cid, "name": chk.name, "severity": chk.severity,
            "weight": chk.weight, "threshold": chk.threshold,
            "count": ctx.total, "stored": len(ctx.findings),
            "notes": ctx.notes, "error": err,
            "seconds": round(time.time() - t1, 3),
            "findings": ctx.findings,
        })
        if verbose:
            sys.stderr.write("[%s] %-4s %6d finding  %.2fs\n"
                             % ("ok" if not err else "ERR", cid, len(ctx.findings),
                                results[-1]["seconds"]))

    total = round(time.time() - t0, 2)
    report = {
        "tool": "V3/03_WORK_BUNDLES/audit_scoped.py",
        "version": "1.0.0-scoped.1",
        "root": os.path.abspath(root),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "elapsed_seconds": total,
        "scope": {
            "scope": scope,
            "description": SCOPE_DOC.get(scope, "?"),
            "root_prefix": "" if scope == "full"
            else ("%s/" % (corpus.scope_base + "/") if corpus.scope_base else "")
                   + "|".join(SCOPE_ROOTS.get(scope, ())),
            "files_in_scope": getattr(corpus, "scope_kept", len(corpus.files)),
            "files_dropped": getattr(corpus, "scope_dropped", 0),
            "cap": cap,
            "unbounded": not cap or cap <= 0,
        },
        "scanned": {
            "files": len(corpus.files),
            "dirs": len(corpus.dirs),
            "md_files": len(corpus.md_all),
            "concepts": len(corpus.concepts),
            "masters": len(corpus.masters),
            "files_read": corpus.files_read,
            "bytes_read": corpus.bytes_read,
            "walk_seconds": round(corpus.walk_seconds, 3),
            "read_seconds": round(corpus.read_seconds, 3),
            "jobs": corpus.jobs,
            "excludes": list(excludes),
            "top_dirs": corpus.top_breakdown(),
        },
        "totals": {
            "findings": sum(r["count"] for r in results),
            "checkers_run": len(results),
            "checker_errors": [r["id"] for r in results if r["error"]],
            "max_severity_hit": max([r["severity"] for r in results if r["count"]] or [0]),
        },
        "checkers": results,
    }
    return report


def _pad(s, w, ar=False):
    s = str(s)
    if ar:
        s = s[::-1]
    n = w - _dlen(s)
    if n <= 0:
        return s
    return (" " * n + s) if ar else (s + " " * n)


def _dlen(s):
    return len(s)


def print_table(report, stream=sys.stdout):
    w = stream.write
    sc = report["scanned"]
    w("\n" + "=" * 96 + "\n")
    w("فاحص الجودة الآلي — audit_scoped.py\n")
    if report.get("scope"):
        sp = report["scope"]
        w("النطاق      : %s — %s\n" % (sp["scope"], sp["description"]))
        w("ملفات النطاق: %d مُدقَّقة · %d مستبعدة%s\n"
          % (sp["files_in_scope"], sp["files_dropped"],
             " · Findings بلا سقف" if sp["unbounded"] else ""))
    w("الجذر      : %s\n" % report["root"])
    w("المفاهيم   : %d · الماسترات: %d · ملفات .md: %d · إجمالي الملفات: %d\n"
      % (sc["concepts"], sc["masters"], sc["md_files"], sc["files"]))
    w("الزمن      : %.2fs (المسح %.2fs · القراءة %.2fs · %d ملف / %.1f MB · %d threads)\n"
      % (report["elapsed_seconds"], sc["walk_seconds"], sc.get("read_seconds", 0.0),
         sc["files_read"], sc["bytes_read"] / 1048576.0, sc.get("jobs", 1)))
    w("=" * 96 + "\n")
    w("%-5s %-42s %8s %7s %6s %6s  %s\n"
      % ("ID", "الفحص", "العدد", "الخطورة", "الوزن", "العتب", "أعلى 3 أمثلة"))
    w("-" * 96 + "\n")
    for r in report["checkers"]:
        ex = "؛ ".join(_short(f["evidence"], 34) for f in r["findings"][:3]) or (
            r["notes"][0] if r["notes"] else "—")
        w("%-5s %-42s %8d %7d %6d %6s  %s\n"
          % (r["id"], r["name"], r["count"], r["severity"], r["weight"],
             r["threshold"], ex))
        if r["error"]:
            w("      !! %s\n" % r["error"])
    w("-" * 96 + "\n")
    w("%-5s %-42s %8d\n" % ("", "TOTAL findings", report["totals"]["findings"]))
    w("مجموع الأوزان: %d\n" % sum(chk.weight for chk in CHECKERS.values()))
    if report["totals"]["checker_errors"]:
        w("أخطاء الفواحص: %s\n" % ", ".join(report["totals"]["checker_errors"]))
    w("=" * 96 + "\n")


def _short(s, n):
    s = re.sub(r"\s+", " ", s)
    return s if len(s) <= n else s[: n - 1] + "…"


def write_json(report, path, max_examples):
    doc = {
        "tool": report["tool"], "version": report["version"], "root": report["root"],
        "generated_at": report["generated_at"],
        "elapsed_seconds": report["elapsed_seconds"],
        "scope": report.get("scope"),
        "scanned": report["scanned"], "totals": report["totals"],
        "max_examples_per_checker": max_examples,
        "weight_sum": sum(r["weight"] for r in report["checkers"]),
        "checkers": [
            {
                "id": r["id"], "name": r["name"], "severity": r["severity"],
                "weight": r["weight"], "threshold": r["threshold"],
                "count": r["count"], "stored": r.get("stored", r["count"]),
                "notes": r["notes"], "error": r["error"],
                "seconds": r["seconds"],
                "findings": r["findings"][:max_examples],
            } for r in report["checkers"]
        ],
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
    return path


def write_md(report, path, max_examples):
    L = []
    A = L.append
    sc = report["scanned"]
    A("# تقرير فحص الجودة الآلي — audit_scoped.py\n")
    if report.get("scope"):
        sp = report["scope"]
        A("- **النطاق:** `%s` — %s" % (sp["scope"], sp["description"]))
        A("- **ملفات النطاق:** %d مُدقَّقة · %d مستبعدة%s"
          % (sp["files_in_scope"], sp["files_dropped"],
             " · Findings بلا سقف" if sp["unbounded"] else ""))
    A("- **الجذر:** `%s`" % report["root"])
    A("- **التاريخ:** %s" % report["generated_at"])
    A("- **الزمن:** %.2fs (مسح %.2fs، قراءة %.2fs، %d ملف / %.1f MB، %d threads)"
      % (report["elapsed_seconds"], sc["walk_seconds"], sc.get("read_seconds", 0.0),
         sc["files_read"], sc["bytes_read"] / 1048576.0, sc.get("jobs", 1)))
    A("- **المفاهيم:** %d · **الماسترات:** %d · **ملفات .md:** %d · **إجمالي الملفات:** %d"
      % (sc["concepts"], sc["masters"], sc["md_files"], sc["files"]))
    A("- **مجموع الأوزان:** %d\n" % sum(r["weight"] for r in report["checkers"]))
    A("## جدول النتائج\n")
    A("| ID | الفحص | العدد | الخطورة | الوزن | العتبة | الحالة |")
    A("|---|---|---:|---:|---:|---|---|")
    for r in report["checkers"]:
        if r["error"]:
            st = "❌ %s" % r["error"]
        elif r["severity"] == 0:
            st = "ℹ️ تقرير فقط (%d)" % r["count"]
        elif r["count"] == 0:
            st = "✅ نظيف"
        else:
            st = "🔴 مخالفة"
        A("| %s | %s | %d | %d | %d | %s | %s |"
          % (r["id"], r["name"], r["count"], r["severity"], r["weight"], r["threshold"], st))
    A("| — | **TOTAL** | **%d** | | **%d** | | |"
      % (report["totals"]["findings"], sum(r["weight"] for r in report["checkers"])))
    A("")
    A("## التفاصيل (حتى %d مثال لكل فاحص)\n" % max_examples)
    for r in report["checkers"]:
        A("### %s · %s — %d مخالفة" % (r["id"], r["name"], r["count"]))
        if r["error"]:
            A("> ❌ خطأ: %s\n" % r["error"])
        if r["notes"]:
            A("> ℹ️ %s\n" % " · ".join(r["notes"]))
        if r["findings"]:
            A("| # | المسار | bytes | الدليل |")
            A("|---:|---|---:|---|")
            for f in r["findings"][:max_examples]:
                A("| %s | `%s` | %d | %s |"
                  % (f["id"].split("#")[-1], f["path"], f["bytes"],
                     _short(f["evidence"], 120)))
            if r["count"] > max_examples:
                A("")
                A("> … و%d مخالفة أخرى (راجع JSON؛ محفوظ %d)"
                  % (r["count"] - max_examples, r.get("stored", r["count"])))
        A("")
    A("## أعلى المجلدات حجمًا\n")
    A("| المجلد | ملفات | bytes |")
    A("|---|---:|---:|")
    for d in sc["top_dirs"]:
        A("| `%s` | %d | %d |" % (d["dir"], d["files"], d["bytes"]))
    A("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return path


# ==================================================================
# 6) CLI
# ==================================================================

def dump_findings(report, path):
    """[SCOPED] تفريغ كل الـFindings سطرًا سطرًا (JSONL) بلا سقف."""
    n = 0
    with open(path, "w", encoding="utf-8") as fh:
        for r in report["checkers"]:
            for f in r["findings"]:
                rec = {
                    "finding_id": f["id"], "checker": f["checker"],
                    "checker_name": r["name"], "path": f["path"],
                    "bytes": f["bytes"], "evidence": f["evidence"],
                    "severity": f["severity"],
                }
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
    return n


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="audit_scoped.py",
        description="فاحص الجودة الآلي — 28 فحصًا قابلًا للتشغيل مع --scope (stdlib فقط).")
    ap.add_argument("--root", help="جذر الفحص")
    ap.add_argument("--checkers", help="قائمة معرّفات مفصولة بفاصلة، مثل C01,C02")
    ap.add_argument("--json", dest="json_out", help="مسار تقرير JSON")
    ap.add_argument("--md", dest="md_out", help="مسار تقرير Markdown")
    ap.add_argument("--weight-sum", action="store_true", help="طباعة الأوزان ومجموعها")
    ap.add_argument("--fail-on", type=float, default=None, metavar="SEV",
                    help="خروج 1 إذا وُجدت مخالفات خطورتها >= SEV")
    ap.add_argument("--max-examples", type=int, default=3, help="أمثلة محفوظة لكل فاحص")
    ap.add_argument("--exclude", action="append", default=[],
                    help="اسم مجلد مستبعد (قابل للتكرار)")
    ap.add_argument("--scope", choices=SCOPES, default="full",
                    help="نطاق القياس (افتراضي full = سلوك الأصل)")
    ap.add_argument("--cap", type=int, default=4000,
                    help="سقف Findings المحفوظة لكل فاحص (0 = بلا سقف)")
    ap.add_argument("--dump-findings", dest="dump_out",
                    help="مسار JSONL لتفريغ كل الـFindings")
    ap.add_argument("--jobs", type=int, default=1,
                    help="خيوط القراءة المسبقة (افتراضي 1؛ f2fs هنا يسلسِل I/O "
                         "والخيوث تبطّئه)")
    ap.add_argument("--quiet", action="store_true", help="بدون جدول على stdout")
    args = ap.parse_args(argv)

    # ---- weight-sum ----
    if args.weight_sum:
        print("%-5s %-42s %6s" % ("ID", "الفحص", "الوزن"))
        print("-" * 60)
        for cid, chk in CHECKERS.items():
            print("%-5s %-42s %6d" % (cid, chk.name, chk.weight))
        total = sum(chk.weight for chk in CHECKERS.values())
        print("-" * 60)
        print("%-5s %-42s %6d" % ("", "TOTAL", total))
        print("WEIGHT_SUM = %d%s" % (total, "" if total == 100 else "  <<< يجب أن يساوي 100"))
        return 0 if total == 100 else 1

    if not args.root:
        ap.error("--root مطلوب (أو استخدم --weight-sum)")
    if not os.path.isdir(args.root):
        ap.error("المسار غير موجود: %s" % args.root)

    only = None
    if args.checkers:
        only = {s.strip().upper() for s in args.checkers.split(",") if s.strip()}
        unknown = sorted(only - set(CHECKERS))
        if unknown:
            ap.error("معرّفات مجهولة: %s" % ", ".join(unknown))
        only = set(CHECKERS) & only          # بترتيب السجل

    excludes = tuple(args.exclude) if args.exclude else (".git",)
    report = run_audit(args.root, only=only, max_examples=args.max_examples,
                       excludes=excludes, verbose=not args.quiet, jobs=args.jobs,
                       scope=args.scope, cap=args.cap)

    if not args.quiet:
        print_table(report)
    if args.json_out:
        write_json(report, args.json_out, args.max_examples)
        if not args.quiet:
            print("JSON  → %s" % args.json_out)
    if args.md_out:
        write_md(report, args.md_out, args.max_examples)
        if not args.quiet:
            print("MD    → %s" % args.md_out)
    if args.dump_out:
        ndump = dump_findings(report, args.dump_out)
        print("FINDINGS → %s  (%d سطر%s)"
              % (args.dump_out, ndump,
                 " · تحذير: السقف %d" % args.cap if args.cap > 0 else ""))

    if args.fail_on is not None:
        hit = [r["id"] for r in report["checkers"] if r["count"] and r["severity"] >= args.fail_on]
        if hit:
            sys.stderr.write("FAIL-ON: مخالفات فوق العتبة %g في: %s\n"
                             % (args.fail_on, ",".join(hit)))
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
