#!/usr/bin/env python3
"""
Nexus Brain — Query Planner
============================
يستكشف الماسترز ذات الصلة بطلب المستخدم ويعرض أدلة الاستحضار المحتملة.

العمل:
   1. يستخرج مرشحي المعرفة من الماسترز والـ graph
   2. يعرض الأدلة والمرشحين للنموذج
   3. النموذج يختار بنفسه ما يقرأه، ترتيب العمل، والمخرج

الاستخدام:
   python3 planner.py "اعمل بزنس بلان" --mode discover
  python3 planner.py "خطة محتوى ليوتيوب" --format json
  python3 planner.py "كيف اغلق صفقة" --format text
  python3 planner.py --list-playbooks
"""

import json, re, sys, os, argparse, math
from collections import defaultdict, deque

# Corpus root is the read-only NB2 vault, not the directory this tool happens to
# live in (they are split now: tools in V3, documents in NB2).
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nexus_config import MASTERS_DIR, SOURCE_ROOT  # noqa: E402

VAULT = SOURCE_ROOT
MASTERS_ROOT = MASTERS_DIR
GRAPH_PATH = os.path.join(MASTERS_ROOT, 'MASTER_GRAPH.json')
INDEX_PATH = os.path.join(MASTERS_ROOT, 'BRAIN_INDEX.md')

# ═══════════════════════════════════════════════════════════
# 1. PLAYBOOKS (مدمجة من PLAYBOOKS.md)
# ═══════════════════════════════════════════════════════════

PLAYBOOKS = {
    'business_plan': {
        'keywords': ['بزنس بلان', 'خطة عمل', 'business plan', 'ابدأ وكالة', 'ابني وكالة', 'agency from scratch', 'مشروع جديد', 'ابني بزنس', 'وكالة جديدة', 'start agency', 'خطة بزنس', 'بزنس من الصفر', 'تأسيس وكالة'],
        'pipeline': [
            {'cluster': '24_foundation_business', 'sections': ['§1', '§4'], 'label': 'الأساسيات + الرؤية'},
            {'cluster': '17_niche_positioning', 'sections': ['§1', '§4'], 'label': 'النيش والتموضع'},
            {'cluster': '14_business_models', 'sections': ['§1', '§4'], 'label': 'نموذج الأعمال + الخدمات'},
            {'cluster': '13_agency_ops', 'sections': ['§1', '§4'], 'label': 'العمليات + الأدوار'},
            {'cluster': '03_pricing_offers', 'sections': ['§1', '§4'], 'label': 'التسعير + العرض'},
            {'cluster': '01_outreach', 'sections': ['§1', '§4'], 'label': 'نظام الوصول'},
            {'cluster': '06_copywriting_scripts', 'sections': ['§1', '§4'], 'label': 'السكربتات + الرسائل'},
            {'cluster': '22_systems_workflow', 'sections': ['§1', '§4'], 'label': 'سير العمل + الأدوات'},
            {'cluster': '21_metrics', 'sections': ['§1', '§4'], 'label': 'KPIs + أهداف'},
        ],
    },
    'product_launch': {
        'keywords': ['اطلاق منتج', 'إطلاق خدمة', 'launch', 'product launch', 'اعلن عن خدمة', 'نزول منتج'],
        'pipeline': [
            {'cluster': '17_niche', 'sections': ['§1', '§4'], 'label': 'السوق + الجمهور'},
            {'cluster': '04_content_strategy', 'sections': ['§1', '§4'], 'label': 'استراتيجية المحتوى'},
            {'cluster': '08_hooks_attention', 'sections': ['§1', '§4'], 'label': 'الهوكس + الرسالة'},
            {'cluster': '05_production', 'sections': ['§1', '§4'], 'label': 'إنتاج المحتوى'},
            {'cluster': '15_funnels', 'sections': ['§1', '§4'], 'label': 'قمع الإطلاق'},
            {'cluster': '02_sales_closing', 'sections': ['§1', '§4'], 'label': 'إغلاق العملاء'},
            {'cluster': '21_metrics', 'sections': ['§1', '§4'], 'label': 'قياس الأداء'},
        ],
    },
    'personal_brand': {
        'keywords': ['براند شخصي', 'personal brand', 'هويتي', 'سمعتي', 'بناء براند', 'اتعرف', 'branding', 'براندينج', 'هوية شخصية', 'بناء سمعة'],
        'pipeline': [
            {'cluster': '09_personal_branding', 'sections': ['§1', '§4'], 'label': 'الهوية + الرسالة'},
            {'cluster': '07_storytelling', 'sections': ['§1', '§4'], 'label': 'القصة + السرد'},
            {'cluster': '12_trust_authority', 'sections': ['§1', '§4'], 'label': 'الثقة + السلطة'},
            {'cluster': '10_psychology_influence', 'sections': ['§1', '§4'], 'label': 'سيكولوجيا الجمهور'},
            {'cluster': '04_content_strategy', 'sections': ['§1', '§4'], 'label': 'خطة المحتوى'},
            {'cluster': '18_platforms', 'sections': ['§1', '§4'], 'label': 'اختيار المنصات'},
            {'cluster': '01_outreach', 'sections': ['§1', '§4'], 'label': 'التوسع + الوصول'},
        ],
    },
    'content_engine': {
        'keywords': ['خطة محتوى', 'content plan', 'استراتيجية محتوى', 'محتوى ليوتيوب', 'content engine', 'عمود محتوى', 'استراتيجية', 'content strategy', 'خطة انشاء', 'جدول محتوى'],
        'pipeline': [
            {'cluster': '04_content_strategy', 'sections': ['§1', '§4'], 'label': 'الاستراتيجية + الأعمدة'},
            {'cluster': '08_hooks_attention', 'sections': ['§1', '§4'], 'label': 'الهوكس + العناوين'},
            {'cluster': '06_copywriting_scripts', 'sections': ['§1', '§4'], 'label': 'السكربتات + النسخ'},
            {'cluster': '07_storytelling', 'sections': ['§1', '§4'], 'label': 'السرد في المحتوى'},
            {'cluster': '05_production', 'sections': ['§1', '§4'], 'label': 'الإنتاج + التحرير'},
            {'cluster': '18_platforms', 'sections': ['§1', '§4'], 'label': 'التوزيع + المنصات'},
            {'cluster': '21_metrics', 'sections': ['§1', '§4'], 'label': 'تحليل الأداء'},
        ],
    },
    'outreach_system': {
        'keywords': ['اوتيريتش', 'اوتريتش', 'اوتوريتش', 'أوتيريتش', 'أوتريتش', 'أوتوريتش', 'outreach', 'اوصل للعملاء', 'أوصل للعملاء', 'ايميل بارد', 'إيميل بارد', 'ايميلات باردة', 'إيميلات باردة', 'cold email', 'cold mail', 'وصول للعملاء', 'dm', 'دي ام', 'رسائل باردة', 'تواصل بارد', 'ايميل', 'إيميل', 'لايد', 'lead gen', 'توليد عملاء', ' prospect'],
        'pipeline': [
            {'cluster': '17_niche', 'sections': ['§1', '§4'], 'label': 'تحديد ICP'},
            {'cluster': '01_outreach', 'sections': ['§1', '§4'], 'label': 'استراتيجية الأوتريتش'},
            {'cluster': '06_copywriting_scripts', 'sections': ['§1', '§4'], 'label': 'السكربتات + الرسائل'},
            {'cluster': '15_funnels', 'sections': ['§1', '§4'], 'label': 'قمع التحويل'},
            {'cluster': '02_sales_closing', 'sections': ['§1', '§4'], 'label': 'الإغلاق'},
            {'cluster': '22_systems_workflow', 'sections': ['§1', '§4'], 'label': 'الأتمتة + الأنظمة'},
            {'cluster': '21_metrics', 'sections': ['§1', '§4'], 'label': 'تتبع + تحسين'},
        ],
    },
    'sales_closing': {
        'keywords': ['اغلق صفقة', 'close deal', 'مبيعات', 'sales', 'اعترضات', 'اقفل عميل', 'closing', 'اعتراض', 'objection', 'اجلسة بيع', 'كلوزينج', 'اغلاق', 'بيع'],
        'pipeline': [
            {'cluster': '10_psychology_influence', 'sections': ['§1', '§4'], 'label': 'سيكولوجيا البيع'},
            {'cluster': '12_trust_authority', 'sections': ['§1', '§4'], 'label': 'بناء الثقة'},
            {'cluster': '02_sales_closing', 'sections': ['§1', '§4'], 'label': 'تقنيات الإغلاق'},
            {'cluster': '03_pricing_offers', 'sections': ['§1', '§4'], 'label': 'العرض + التسعير'},
            {'cluster': '21_metrics', 'sections': ['§1', '§4'], 'label': 'معدل التحويل'},
        ],
    },
    'funnel_build': {
        'keywords': ['قمع', 'funnel', 'قمع تسويقي', 'conversion funnel', 'صفحة هبوط', 'lead magnet', 'landing page', 'مغناطيس عملاء', 'قمع بيع', 'قمع تحويل'],
        'pipeline': [
            {'cluster': '04_content_strategy', 'sections': ['§1', '§4'], 'label': 'محتوى علوي'},
            {'cluster': '08_hooks_attention', 'sections': ['§1', '§4'], 'label': 'جذب الانتباه'},
            {'cluster': '15_funnels', 'sections': ['§1', '§4'], 'label': 'بناء القمع'},
            {'cluster': '06_copywriting_scripts', 'sections': ['§1', '§4'], 'label': 'نسخ التحويل'},
            {'cluster': '02_sales_closing', 'sections': ['§1', '§4'], 'label': 'إغلاق القاع'},
            {'cluster': '21_metrics', 'sections': ['§1', '§4'], 'label': 'تحليل التسرب'},
        ],
    },
    'agency_scaling': {
        'keywords': ['صعد', 'صعّد', 'scale', 'تصعيد', 'نمو وكالة', 'وسع وكالة', 'أوسع وكالة', 'أوسع الوكالة', 'توسيع الوكالة', 'scaling agency', 'توسيع', 'scale agency', 'نمو الايجنسي', 'تكبير وكالة', 'وسع الايجنسي', 'كبر وكالة'],
        'pipeline': [
            {'cluster': '13_agency_ops', 'sections': ['§1', '§4'], 'label': 'العمليات الحالية'},
            {'cluster': '16_growth_frameworks', 'sections': ['§1', '§4'], 'label': 'أطر النمو'},
            {'cluster': '22_systems_workflow', 'sections': ['§1', '§4'], 'label': 'الأنظمة + الأتمتة'},
            {'cluster': '20_ai_automation', 'sections': ['§1', '§4'], 'label': 'أتمتة بالذكاء الاصطناعي'},
            {'cluster': '14_business_models', 'sections': ['§1', '§4'], 'label': 'نماذج التوسع'},
            {'cluster': '21_metrics', 'sections': ['§1', '§4'], 'label': 'مؤشرات التصعيد'},
        ],
    },
    'youtube_channel': {
        'keywords': ['يوتيوب', 'youtube', 'قناة يوتيوب', 'youtube channel', 'فيديوهات يوتيوب', 'قناة', 'channel', 'يوتيوبر'],
        'pipeline': [
            {'cluster': '19_youtube', 'sections': ['§1', '§4'], 'label': 'استراتيجية القناة'},
            {'cluster': '08_hooks_attention', 'sections': ['§1', '§4'], 'label': 'هوكس الفيديو'},
            {'cluster': '07_storytelling', 'sections': ['§1', '§4'], 'label': 'سرد الفيديو'},
            {'cluster': '05_production', 'sections': ['§1', '§4'], 'label': 'إنتاج + تحرير'},
            {'cluster': '04_content_strategy', 'sections': ['§1', '§4'], 'label': 'خطة المحتوى'},
            {'cluster': '18_platforms', 'sections': ['§1', '§4'], 'label': 'توزيع + خوارزمية'},
            {'cluster': '21_metrics', 'sections': ['§1', '§4'], 'label': 'تحليل القناة'},
        ],
    },
    'pricing_design': {
        'keywords': ['سعر', 'تسعير', 'pricing', 'عرض سعر', 'package', 'باقة', 'price offer', 'سعّر', 'استراتيجية سعر', 'تسعيره'],
        'pipeline': [
            {'cluster': '10_psychology_influence', 'sections': ['§1', '§4'], 'label': 'سيكولوجيا التسعير'},
            {'cluster': '03_pricing_offers', 'sections': ['§1', '§4'], 'label': 'استراتيجية التسعير'},
            {'cluster': '14_business_models', 'sections': ['§1', '§4'], 'label': 'النموذج المالي'},
            {'cluster': '02_sales_closing', 'sections': ['§1', '§4'], 'label': 'عرض السعر للعميل'},
        ],
    },
}

# ═══════════════════════════════════════════════════════════
# 2. تحميل الـ graph + الماسترز
# ═══════════════════════════════════════════════════════════

def load_graph():
    with open(GRAPH_PATH, encoding='utf-8') as f:
        return json.load(f)

def normalize_text(text):
    """Light Arabic normalization; retrieval still uses exact token boundaries."""
    return re.sub(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]', '',
                  text.lower().translate(str.maketrans('أإآىة', 'ااايه')))


def normalize_token(token):
    """Remove common Arabic conjunction/preposition prefixes without aggressive stemming."""
    token = normalize_text(token)
    for prefix in ('وال', 'بال', 'كال', 'فال', 'لل', 'ال'):
        if token.startswith(prefix) and len(token) - len(prefix) >= 3:
            return token[len(prefix):]
    return token


def tokenize(text):
    return [normalize_token(token) for token in re.findall(r'[\w\u0600-\u06FF]+', text)
            if len(normalize_token(token)) > 1]


def extract_sections(text):
    """Return top-level master sections as independently searchable evidence units."""
    matches = list(re.finditer(r'^##\s*§\s*(\d+)\s*[^\n]*', text, re.M))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append({
            'number': int(match.group(1)),
            'heading': ' '.join(match.group(0).replace('##', '').split()),
            'text': text[match.start():end],
        })
    return sections


def load_masters_index():
    """Build a small, live lexical index from active canonical master sections only."""
    graph = load_graph()
    result = {}
    for node in graph.get('nodes', []):
        path = os.path.join(VAULT, node['path'])
        text = ''
        try:
            with open(path, encoding='utf-8', errors='replace') as f:
                text = f.read()
        except OSError:
            pass
        title_match = re.search(r'^#\s+(.+)$', text, re.M)
        title = title_match.group(1).strip() if title_match else node['id'].replace('_', ' ')
        sections = extract_sections(text)
        if not sections and text:
            sections = [{'number': None, 'heading': title, 'text': text}]
        result[node['id']] = {
            'master_name': node['id'], 'file_path': path, 'title': title,
            'sections_data': sections,
            'tldr': ' '.join((sections[0]['text'] if sections else text).split())[:500],
        }
    return result

# ═══════════════════════════════════════════════════════════
# 3. تصنيف القصد (intent classification)
# ═══════════════════════════════════════════════════════════

def classify_intent(question):
    """يطابق السؤال بـ playbook keywords. يرجّع (playbook_id, score)"""
    q = question.lower().strip()
    scores = {}
    for pid, pb in PLAYBOOKS.items():
        score = 0
        for kw in pb['keywords']:
            if kw.lower() in q:
                score += len(kw.split()) * 2  # كلمات متعددة = وزن أعلى
        if score > 0:
            scores[pid] = score
    if scores:
        best = max(scores, key=scores.get)
        return best, scores[best]
    return None, 0

# ═══════════════════════════════════════════════════════════
# 4. حل الكلاستر → ماسترز
# ═══════════════════════════════════════════════════════════

CLUSTER_CANONICAL = {
    '05_production': '05_content_production',
    '05_video_production': '05_content_production',
    '10_psychology_influence': '10_psychology_influence',
    '13_agency': '13_agency',
    '13_agency_ops': '13_agency_ops',
    '15_funnels': '15_funnels_conversion',
    '17_niche': '17_niche',
    '17_niche_positioning': '17_niche_positioning',
    '18_platforms': '18_platforms_algorithm',
}

def cluster_to_masters(graph, cluster_name):
    """يرجّع كل الماسترز اللي في كلاستر (مع تطبيع الكلاسترات المزدوجة)"""
    canon = CLUSTER_CANONICAL.get(cluster_name, cluster_name)
    result = []
    for n in graph['nodes']:
        nc = CLUSTER_CANONICAL.get(n['cluster'], n['cluster'])
        if nc == canon or n['cluster'] == cluster_name:
            result.append(n['id'])
    return result

# ═══════════════════════════════════════════════════════════
# 5. بناء الـ pipeline
# ═══════════════════════════════════════════════════════════

def build_pipeline_from_playbook(graph, pb_id, masters_idx):
    pb = PLAYBOOKS[pb_id]
    steps = []
    seen_masters = set()
    for i, step in enumerate(pb['pipeline'], 1):
        masters = cluster_to_masters(graph, step['cluster'])
        # اختار ماستر واحد بس (الأول اللي مش اتكرر)
        chosen = None
        for mname in masters:
            if mname not in seen_masters:
                chosen = mname
                seen_masters.add(mname)
                break
        if not chosen and masters:
            chosen = masters[0]  # fallback
        if chosen:
            tldr = masters_idx.get(chosen, {}).get('tldr', '')[:200]
            steps.append({
                'order': i,
                'master': chosen,
                'file_path': masters_idx.get(chosen, {}).get('file_path', ''),
                'sections': step['sections'],
                'label': step['label'],
                'tldr': tldr,
            })
        else:
            steps.append({
                'order': i,
                'master': f'[NO MASTER IN {step["cluster"]}]',
                'file_path': '',
                'sections': step['sections'],
                'label': step['label'],
                'tldr': '',
            })
    return {'intent': pb_id, 'source': 'playbook', 'pipeline': steps}

def build_pipeline_dynamic(graph, question, masters_idx):
    """يبني مسار ديناميكي من الـ graph بناءً على تطابق كلمات السؤال مع أسماء/كلاسترات الماسترز"""
    q = question.lower()
    # سكور لكل node
    scores = {}
    for n in graph['nodes']:
        s = 0
        # تطابق الاسم
        if n['id'].lower().replace('_',' ') in q or any(w in q for w in n['id'].lower().split('_')):
            s += 3
        # تطابق الكلاستر
        if n['cluster'].lower().replace('_',' ') in q:
            s += 2
        if s > 0:
            scores[n['id']] = s
    
    if not scores:
        # fallback: رجّع أعلى 5 ماسترز من الـ graph بشكل عام
        top = [n['id'] for n in graph['nodes'][:5]]
    else:
        top = sorted(scores, key=scores.get, reverse=True)[:3]
    
    # اتبع prerequisite edges من الـ top
    visited = set()
    ordered = []
    queue = deque(top)
    while queue and len(ordered) < 8:
        m = queue.popleft()
        if m in visited:
            continue
        visited.add(m)
        # ضيف prerequisites الأول
        prereqs = [e['source'] for e in graph['edges'] if e['target']==m and e['relation']=='prerequisite']
        for p in prereqs:
            if p not in visited:
                queue.appendleft(p)
        ordered.append(m)
    
    steps = []
    for i, mname in enumerate(ordered, 1):
        tldr = masters_idx.get(mname, {}).get('tldr', '')[:200]
        steps.append({
            'order': i,
            'master': mname,
            'file_path': masters_idx.get(mname, {}).get('file_path', ''),
            'sections': ['§1', '§4'],
            'label': 'تلقائي من الـ graph',
            'tldr': tldr,
        })
    return {'intent': 'dynamic', 'source': 'graph', 'pipeline': steps}


DISCOVERY_STOP_WORDS = {
    'عايز', 'عايزك', 'اعمل', 'اعملي', 'لي', 'من', 'في', 'على', 'عن', 'مع',
    'هذا', 'ده', 'دي', 'الى', 'إلى', 'كيف', 'ايه', 'إيه', 'اللي', 'انا',
    'اني', 'محتاج', 'عاوز', 'عاوزه', 'عاوزك', 'نظام', 'سيستم', 'كامل',
    'ابن', 'ابني', 'ابنيها', 'ضع', 'اعطني', 'ساعدني', 'جديد', 'جديده',
    'please', 'make', 'build', 'create', 'system', 'for', 'the', 'and',
}

# Small bilingual bridge for common domain terms. It broadens evidence lookup,
# not the planning decision, and deliberately avoids a closed-domain router.
DISCOVERY_ALIASES = {
    'براند': ('brand', 'branding'), 'براندا': ('brand', 'branding'), 'شخصيا': ('personal',),
    'اطلاق': ('launch',), 'منتج': ('product',), 'خدمه': ('service', 'consulting'),
    'استشاريه': ('consulting',), 'سعر': ('pricing',), 'سعره': ('pricing',), 'سعرر': ('pricing',),
    'اوتريتش': ('outreach',), 'اوتيريتش': ('outreach',), 'بريد': ('email',), 'بارد': ('cold',),
    'وكاله': ('agency',), 'تسليم': ('delivery',), 'مشاريع': ('project',),
    'نظام': ('workflow', 'systems'), 'سيستم': ('system', 'workflow'),
}


def discovery_tokens(question):
    """Extract meaningful query terms, preserving word boundaries and Arabic clitics."""
    tokens = [token for token in tokenize(question)
              if token not in DISCOVERY_STOP_WORDS and len(token) > 1]
    expanded = []
    for token in tokens:
        expanded.append(token)
        expanded.extend(DISCOVERY_ALIASES.get(token, ()))
    return list(dict.fromkeys(expanded))


def evidence_snippet(text, matched_terms, limit=280):
    """Return a local, inspectable excerpt around the strongest matched term."""
    compact = ' '.join(text.split())
    normalized = normalize_text(compact)
    positions = [normalized.find(term) for term in matched_terms if normalized.find(term) >= 0]
    if not positions:
        return compact[:limit]
    start = max(0, min(positions) - 90)
    end = min(len(compact), start + limit)
    return ('...' if start else '') + compact[start:end] + ('...' if end < len(compact) else '')


def is_reference_section(heading):
    """Reference lists repeat many terms but do not substantiate a task-specific recommendation."""
    normalized = normalize_text(heading)
    return any(marker in normalized for marker in ('المصادر', 'المراجع', 'روابط', 'concept index', 'قائمه المفاهيم'))


def build_discovery(graph, question, masters_idx):
    """Rank masters by matches in their actual sections; never build an execution plan."""
    tokens = discovery_tokens(question)
    documents = []
    for master, data in masters_idx.items():
        for section in data['sections_data']:
            if is_reference_section(section['heading']):
                continue
            documents.append((master, section, set(tokenize(section['text']))))

    # IDF prevents generic terms such as "system" from making unrelated masters win.
    document_frequency = {token: sum(token in terms for _, _, terms in documents) for token in tokens}
    idf = {token: math.log((len(documents) + 1) / (count + 1)) + 1
           for token, count in document_frequency.items()}
    candidate_evidence = {}
    for master, section, section_terms in documents:
        matches = [token for token in tokens if token in section_terms]
        if not matches:
            continue
        text_tokens = tokenize(section['text'])
        score = sum(idf[token] * (1 + math.log(text_tokens.count(token))) for token in matches)
        title_terms = set(tokenize(f"{masters_idx[master]['title']} {master}"))
        score += sum(idf[token] * 2 for token in matches if token in title_terms)
        candidate_evidence.setdefault(master, []).append({
            'section': f"§{section['number']}" if section['number'] else 'مقدمة',
            'heading': section['heading'], 'matched_terms': matches,
            'snippet': evidence_snippet(section['text'], matches), 'score': round(score, 3),
        })

    candidates = []
    for master, evidence in candidate_evidence.items():
        evidence.sort(key=lambda item: -item['score'])
        unique_evidence = []
        seen_sections = set()
        for item in evidence:
            if item['section'] not in seen_sections:
                unique_evidence.append(item)
                seen_sections.add(item['section'])
        evidence = unique_evidence
        # The best two independent passages supply evidence without over-rewarding a long master.
        score = evidence[0]['score'] + (evidence[1]['score'] * 0.35 if len(evidence) > 1 else 0)
        candidates.append({
            'master': master, 'file_path': masters_idx[master]['file_path'],
            'sections': [item['section'] for item in evidence[:2]],
            'label': 'مرشح مدعوم بمقاطع؛ النموذج يقرر الحاجة والترتيب',
            'score': round(score, 3), 'matches': sorted({term for item in evidence[:2] for term in item['matched_terms']}),
            'evidence': evidence[:2],
        })

    candidates.sort(key=lambda item: (-item['score'], item['master']))
    steps = []
    for rank, candidate in enumerate(candidates[:8], 1):
        candidate['order'] = rank
        steps.append(candidate)
    return {
        'intent': 'discovery',
        'source': 'evidence-not-a-playbook',
        'query_tokens': tokens,
        'notice': 'هذه نتائج استكشاف وليست خطة أو ترتيباً أو قائمة قراءة إلزامية. افهم الطلب واختر الحد الأدنى المفيد بنفسك.',
        'pipeline': steps,
    }

# ═══════════════════════════════════════════════════════════
# 6. الإخراج
# ═══════════════════════════════════════════════════════════

def output_text(plan):
    lines = []
    lines.append(f'🎯 القصد: {plan["intent"]} (المصدر: {plan["source"]})')
    lines.append(f'📋 المسار: {len(plan["pipeline"])} خطوة')
    lines.append('')
    for s in plan['pipeline']:
        lines.append(f'  {s["order"]}. {s["master"]}')
        lines.append(f'     📂 {s["file_path"]}')
        lines.append(f'     📑 اقرأ: {", ".join(s["sections"])} — {s["label"]}')
        if s['tldr']:
            lines.append(f'     💡 {s["tldr"][:120]}...')
        lines.append('')
    if plan['intent'] == 'discovery':
        lines.append('⚡ القرار للنموذج: افهم الاحتياج، افحص الأدلة، ثم اختر فقط ما يلزم وبالترتيب الذي يناسب المهمة.')
    else:
        lines.append('⚡ هذا playbook مرجع اختياري؛ عدّله أو تجاهله عندما لا يخدم الطلب.')
    return '\n'.join(lines)

def output_json(plan):
    return json.dumps(plan, ensure_ascii=False, indent=2)

def output_compact(plan):
    """صيغة مختصرة للصق في النموذج"""
    if plan['intent'] == 'discovery':
        lines = ['[DISCOVERY: مرشحون فقط، وليسوا مساراً إلزامياً]']
    else:
        lines = [f'[PLAYBOOK: {plan["intent"]}]']
    for s in plan['pipeline']:
        lines.append(f'{s["order"]}. {s["master"]} | اقرأ: {",".join(s["sections"])} | {s["label"]}')
        if plan['intent'] == 'discovery' and s.get('evidence'):
            lines.append(f'   دليل: {s["evidence"][0]["section"]} ({", ".join(s["evidence"][0]["matched_terms"])})')
    return '\n'.join(lines)

# ═══════════════════════════════════════════════════════════
# 7. CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Nexus Brain Query Planner — يحوّل السؤال لمسار ماسترز')
    parser.add_argument('question', nargs='?', help='السؤال/المهمة')
    parser.add_argument('--format', choices=['text', 'json', 'compact'], default='text', help='صيغة الإخراج')
    parser.add_argument('--list-playbooks', action='store_true', help='اعرض المسارات المرجعية الاختيارية')
    parser.add_argument('--mode', choices=['discover', 'playbook'], default='discover', help='discover الافتراضي: مرشحون فقط؛ playbook: مسار مرجعي اختياري')
    args = parser.parse_args()

    if args.list_playbooks:
        print('📋 Playbooks المتاحة:')
        for pid, pb in PLAYBOOKS.items():
            kws = ', '.join(pb['keywords'][:3])
            print(f'  {pid}: {len(pb["pipeline"])} خطوات | كلمات مفتاحية: {kws}')
        return

    if not args.question:
        parser.print_help()
        return

    graph = load_graph()
    masters_idx = load_masters_index()

    if args.mode == 'playbook':
        pb_id, score = classify_intent(args.question)
        if pb_id and score > 0:
            plan = build_pipeline_from_playbook(graph, pb_id, masters_idx)
        else:
            plan = build_pipeline_dynamic(graph, args.question, masters_idx)
    else:
        plan = build_discovery(graph, args.question, masters_idx)

    if args.format == 'json':
        print(output_json(plan))
    elif args.format == 'compact':
        print(output_compact(plan))
    else:
        print(output_text(plan))

if __name__ == '__main__':
    main()
