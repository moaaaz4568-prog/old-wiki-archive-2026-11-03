#!/usr/bin/env python3
"""
add_links.py — يضيف روابط دلالية للـ concepts في Nexus Brain
يعالج batch من الملفات: Concept_A* (من 16+) و Concept_B*
"""

import os
import re
import subprocess
import sys

_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nexus_config import CONCEPTS_DIR, RAG_DIR  # noqa: E402

# Concepts live in the read-only NB2 corpus; the tools that read the index live in
# V3. NOTE: add_links.py WRITES to WIKI_DIR -- do not point it at a read-only tree.
WIKI_DIR = CONCEPTS_DIR
MIN_SCORE = 0.15
MAX_LINKS = 5

def get_existing_links(content):
    """استخرج الروابط الموجودة في الملف"""
    return set(re.findall(r'\[\[([^\]]+)\]\]', content))

def count_links_in_section(content):
    """عد الروابط في قسم الروابط فقط (آخر section)"""
    # ابحث عن آخر section (## ...)
    sections = re.split(r'\n## ', content)
    if len(sections) < 2:
        return 0
    last_section = sections[-1]
    links = re.findall(r'\[\[([^\]]+)\]\]', last_section)
    return len(links)

def search_rag(keywords):
    """ابحث في RAG وارجع النتائج"""
    try:
        result = subprocess.run(
            ['python3', 'search.py', keywords],
            cwd=RAG_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        print(f"  [RAG ERROR] {e}")
        return ""

def parse_search_results(output):
    """حلل نتائج البحث وارجع قائمة (name, score)"""
    results = []
    # النمط الفعلي: "#1 (0.643) Concept_Name.md"
    for line in output.split('\n'):
        m = re.match(r'#\d+\s+\(([0-9.]+)\)\s+(Concept_[^\s]+)\.md', line)
        if m:
            score = float(m.group(1))
            name = m.group(2).strip()
            if score >= MIN_SCORE:
                results.append((name, score))
    return results

def file_exists(concept_name):
    """تحقق إن الملف موجود على الديسك"""
    path = os.path.join(WIKI_DIR, f"{concept_name}.md")
    return os.path.exists(path)

def get_links_section_info(content):
    """احصل على معلومات قسم الروابط"""
    # ابحث عن آخر section
    # الأنماط الشائعة: ## صفحات مرتبطة, ## روابط, ## Related, ## صفحة ذات علاقة
    patterns = [
        r'(## (?:صفحات مرتبطة|روابط|Related|صفحة ذات علاقة|روابط ذات صلة)[^\n]*\n)',
    ]

    best_pos = -1
    header_text = None

    for pattern in patterns:
        matches = list(re.finditer(pattern, content))
        if matches:
            last = matches[-1]
            if last.start() > best_pos:
                best_pos = last.start()
                header_text = last.group(0)

    return best_pos, header_text

def add_links_to_file(filepath, new_links):
    """أضف روابط جديدة لملف"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    section_pos, header = get_links_section_info(content)

    # بناء نص الروابط الجديدة
    links_text = ""
    for concept_name, relation in new_links:
        links_text += f"- [[{concept_name}]] — {relation}\n"

    if section_pos >= 0:
        # أضف بعد آخر سطر في القسم
        # ابحث عن نهاية القسم (نهاية الملف أو section جديد)
        after_header = content[section_pos + len(header):]
        # اضف في نهاية المحتوى الموجود في القسم
        new_content = content.rstrip() + "\n" + links_text
    else:
        # لا يوجد section → أضف في النهاية
        new_content = content.rstrip() + "\n\n## صفحات مرتبطة\n" + links_text

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def get_concept_topic(content, filename):
    """استخرج الموضوع الأساسي من الملف"""
    # اسم الملف هو أفضل مصدر
    name = os.path.basename(filename).replace('.md', '').replace('Concept_', '').replace('_', ' ')

    # حاول تستخرج من الـ frontmatter
    m = re.search(r'name:\s*(.+)', content)
    if m:
        return m.group(1).strip()

    return name

def get_relation_text(concept_name, current_topic):
    """اقترح نص العلاقة بالعربي"""
    # نص عام بناءً على اسم الـ concept
    name = concept_name.replace('Concept_', '').replace('_', ' ')
    return f"مفهوم مرتبط بـ {current_topic}"

def process_file(filepath):
    """عالج ملف واحد"""
    filename = os.path.basename(filepath)
    concept_name = filename.replace('.md', '')

    # اقرأ الملف
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [ERROR reading] {e}")
        return 0, "error"

    # عد الروابط الحالية في قسم الروابط
    current_link_count = count_links_in_section(content)

    if current_link_count >= MAX_LINKS:
        return 0, "skip"

    # استخرج الروابط الموجودة (كل الملف)
    existing_links = get_existing_links(content)

    # استخرج الموضوع
    topic = get_concept_topic(content, filepath)

    # ابحث - بحث أول
    search1 = search_rag(topic)
    results1 = parse_search_results(search1)

    # ابحث - بحث ثاني بكلمات مختلفة
    # استخدم اسم الملف بشكل مختلف
    alt_topic = concept_name.replace('Concept_', '').replace('_', ' ').lower()
    # خذ أول 3 كلمات
    words = alt_topic.split()[:3]
    alt_keywords = ' '.join(words) if words else alt_topic

    search2 = search_rag(alt_keywords)
    results2 = parse_search_results(search2)

    # دمج النتائج وإزالة المكررات
    all_results = {}
    for name, score in results1 + results2:
        if name not in all_results or all_results[name] < score:
            all_results[name] = score

    # فلتر: بعيد عن الموجود، موجود على الديسك، مش نفس الملف
    candidates = []
    for name, score in sorted(all_results.items(), key=lambda x: -x[1]):
        if name == concept_name:
            continue
        if name in existing_links:
            continue
        if not file_exists(name):
            continue
        candidates.append((name, score))

    # احسب كم رابط نحتاج نضيف
    needed = MAX_LINKS - current_link_count
    to_add = candidates[:needed]

    if not to_add:
        return 0, "no_candidates"

    # أضف الروابط
    new_links_with_relations = []
    for name, score in to_add:
        relation = get_relation_text(name, topic)
        new_links_with_relations.append((name, relation))

    add_links_to_file(filepath, new_links_with_relations)

    return len(to_add), "added"


def main():
    # احصل على الملفات
    all_files_A = sorted([
        os.path.join(WIKI_DIR, f)
        for f in os.listdir(WIKI_DIR)
        if f.startswith('Concept_A') and f.endswith('.md')
    ])

    all_files_B = sorted([
        os.path.join(WIKI_DIR, f)
        for f in os.listdir(WIKI_DIR)
        if f.startswith('Concept_B') and f.endswith('.md')
    ])

    # خذ A من index 15 (0-indexed = file 16 وما بعد)
    files_A_batch = all_files_A[15:]
    files_B_batch = all_files_B

    all_files = files_A_batch + files_B_batch

    print(f"Total files to process: {len(all_files)} (A: {len(files_A_batch)}, B: {len(files_B_batch)})")
    print("=" * 60)

    total_processed = 0
    total_skipped = 0
    total_links_added = 0
    top_links = []  # قائمة أفضل الروابط

    for i, filepath in enumerate(all_files, 1):
        filename = os.path.basename(filepath)
        print(f"[{i}/{len(all_files)}] {filename}")

        links_added, status = process_file(filepath)

        if status == "skip":
            print(f"  → SKIP (5+ links already)")
            total_skipped += 1
        elif status == "error":
            print(f"  → ERROR")
        elif status == "no_candidates":
            print(f"  → No valid candidates found")
            total_processed += 1
        else:
            print(f"  → Added {links_added} link(s)")
            total_processed += 1
            total_links_added += links_added

            # سجل للتقرير
            if links_added > 0:
                # اقرأ ما أضفناه
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # آخر الروابط المضافة
                topic = get_concept_topic(content, filepath)
                top_links.append((filename.replace('.md',''), links_added, topic))

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(f"Files processed: {total_processed}")
    print(f"Files skipped (5+ links): {total_skipped}")
    print(f"Total new links added: {total_links_added}")
    print(f"\nTop files with new links:")
    top_links.sort(key=lambda x: -x[1])
    for name, count, topic in top_links[:10]:
        print(f"  +{count}  {name}")

if __name__ == '__main__':
    main()
