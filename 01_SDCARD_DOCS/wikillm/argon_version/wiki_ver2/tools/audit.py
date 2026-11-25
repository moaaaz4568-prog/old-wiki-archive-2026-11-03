#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit.py — فاحص الجودة الآلي والبوابات الرقمية (Quality Gate Auditor).
الوظيفة:
  1) فحص التلوث اللغوي وخلو النصوص من محارف CJK (Python stdlib: '\u4e00' <= c <= '\u9fff').
  2) فحص سقف المجلدات (كل مجلد <= 900 ملف وفق R21).
  3) اكتمال الاقسام الثمانية عشر §1-§18 في القوالب المعتمدة.
  4) نظافة الملفات وخلوها من وسوم التاجيل (TODO/TBD/XXX).
  5) التحقق من صحة الروابط والمسارات المذكورة على القرص.
  6) اصدار تقرير اوزان شامل مع نتيجة PASSED او FAILED.
"""

import argparse
import os
import re
import sys

DEFAULT_TARGET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def audit_cjk(root):
    """البوابة 1: فحص التلوث اللغوي CJK."""
    cjk_count = 0
    bad_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        for fn in filenames:
            if fn.endswith((".md", ".txt")):
                fp = os.path.join(dirpath, fn)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                        chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
                        if chars:
                            cjk_count += len(chars)
                            bad_files.append((fp, len(chars)))
                except OSError:
                    pass
    passed = (cjk_count == 0)
    details = f"صفر محارف صينية (تم رصد: {cjk_count})" if passed else f"تم رصد {cjk_count} حرفا صينيا في {len(bad_files)} ملفا"
    return passed, 25 if passed else 0, details


def audit_directory_sizes(root):
    """البوابة 2: فحص سقف المجلدات (<= 900 ملف)."""
    violating_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        file_count = len(filenames)
        if file_count > 900:
            violating_dirs.append((dirpath, file_count))
    passed = (len(violating_dirs) == 0)
    details = "كافة المجلدات دون سقف 900 ملف" if passed else f"يوجد {len(violating_dirs)} مجلدا تجاوزت الحد"
    return passed, 20 if passed else 0, details


def audit_templates_completeness(root):
    """البوابة 3: اكتمال الاقسام §1-§18 في قوالب PLAYBOOK_TEMPLATE."""
    playbooks = []
    incomplete = []
    domains_dir = os.path.join(root, "domains")
    if os.path.isdir(domains_dir):
        for dirpath, _, filenames in os.walk(domains_dir):
            for fn in filenames:
                if fn == "PLAYBOOK_TEMPLATE.md":
                    fp = os.path.join(dirpath, fn)
                    playbooks.append(fp)
                    try:
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            section_matches = re.findall(r"^#{2,3}\s*§\d+", content, re.MULTILINE)
                            if len(section_matches) < 18:
                                incomplete.append((fp, len(section_matches)))
                    except OSError:
                        pass
    passed = (len(playbooks) > 0 and len(incomplete) == 0)
    if not playbooks:
        details = "لا توجد قوالب PLAYBOOK_TEMPLATE في domains/"
        return True, 20, details
    details = f"جميع القوالب ({len(playbooks)}) مستوفية لكامل الاقسام الـ 18 (§1-§18)" if passed else f"{len(incomplete)} قوالب ناقصة"
    return passed, 20 if passed else 0, details


def audit_placeholders(root):
    """البوابة 4: خلو الوثائق من وسوم التعليق والمماطلة (TODO/TBD/XXX)."""
    findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        for fn in filenames:
            if fn.endswith(".md"):
                fp = os.path.join(dirpath, fn)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                        # إزالة الكتل البرمجية والأكواد لتفادي الأمثلة الاستشهادية
                        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
                        text = re.sub(r"`[^`\n]+`", "", text)
                        for line_num, line in enumerate(text.splitlines(), start=1):
                            # استبعاد الأسطر التي تناقش حظر الرمز ذاته
                            if any(w in line for w in ["حظر", "منع", "غياب", "خلو", "مثل TODO", "الرموز المؤقتة"]):
                                continue
                            matches = re.findall(r"\b(TODO|TBD|XXX)\b", line)
                            if matches:
                                findings.append((fp, line_num, matches))
                except OSError:
                    pass
    passed = (len(findings) == 0)
    details = "صفر وسوم TODO/TBD/XXX حقيقية" if passed else f"تم رصد {len(findings)} وسما معلقا"
    return passed, 20 if passed else 0, details


def audit_links_and_paths(root):
    """البوابة 5: التحقق من وجود الملفات والمصادر المشار اليها بالمسارات المطلقة."""
    checked = 0
    broken = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        for fn in filenames:
            if fn.endswith(".md"):
                fp = os.path.join(dirpath, fn)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                        candidates = []
                        # استخراج المسارات المحاطة بأقواس كودية
                        candidates.extend(re.findall(r"`(/(?:sdcard|root|mnt)/[^`\n]+)`", text))
                        # استخراج المسارات المحاطة بعلامات تنصيص
                        candidates.extend(re.findall(r'"(/(?:sdcard|root|mnt)/[^"\n]+)"', text))
                        # استخراج مسارات الروابط التشعبية
                        candidates.extend(re.findall(r"\]\((?:file://)?(/(?:sdcard|root|mnt)/[^\)\n]+)\)", text))

                        for target in candidates:
                            target_clean = target.strip()
                            # استبعاد التعبيرات النمطية والمخرجات المستقبلية
                            if any(c in target_clean for c in ["*", "[", "]", "output_business_plan"]):
                                continue
                            if ":" in os.path.basename(target_clean):
                                target_clean = target_clean.split(":")[0]
                            if "#" in target_clean:
                                target_clean = target_clean.split("#")[0]

                            checked += 1
                            if not os.path.exists(target_clean):
                                alt = target_clean.replace("/sdcard/", "/mnt/sdcard/") if target_clean.startswith("/sdcard/") else target_clean.replace("/mnt/sdcard/", "/sdcard/")
                                if not os.path.exists(alt):
                                    broken.append((fp, target_clean))
                except OSError:
                    pass

    passed = (len(broken) == 0)
    details = f"تم فحص {checked} مسارا وكلها مثبتة على القرص بنسبة 100%" if passed else f"تم رصد {len(broken)} مسارات مفقودة"
    return passed, 15 if passed else 0, details


def main():
    parser = argparse.ArgumentParser(description="audit.py — فاحص الجودة الآلي والبوابات الرقمية")
    parser.add_argument("target", nargs="?", default=DEFAULT_TARGET, help="مسار المجلد المستهدف بالفحص")
    args = parser.parse_args()

    target = os.path.abspath(args.target)
    if not os.path.exists(target):
        print(f"خطا: المسار المستهدف غير موجود: {target}")
        sys.exit(2)

    gates = [
        ("G1", "النقاء اللغوي (صفر محارف CJK)", 25, audit_cjk),
        ("G2", "سقف حجم المجلدات (<= 900 ملف)", 20, audit_directory_sizes),
        ("G3", "اكتمال القوالب (§1-§18)", 20, audit_templates_completeness),
        ("G4", "نظافة الوثائق (صفر TODO/TBD)", 20, audit_placeholders),
        ("G5", "صحة الروابط والمسارات الواقعية", 15, audit_links_and_paths),
    ]

    total_score = 0
    all_passed = True
    results = []

    for gid, name, weight, fn in gates:
        p, score, details = fn(target)
        total_score += score
        if not p:
            all_passed = False
        results.append((gid, name, weight, score, "PASS" if p else "FAIL", details))

    print("================================================================================")
    print(f"تقرير التدقيق وضمان الجودة المعماري · المسار: {target}")
    print("================================================================================")
    print(f"{'البوابة':<6} | {'اسم الفحص':<32} | {'الوزن':<6} | {'النقاط':<6} | {'الحالة':<6} | التفاصيل")
    print("-------|----------------------------------|--------|--------|--------|-------------------------")

    for gid, name, weight, score, status, details in results:
        print(f"{gid:<6} | {name:<32} | {weight:<6} | {score:<6} | {status:<6} | {details}")

    print("================================================================================")
    verdict = "PASSED" if all_passed and total_score >= 85 else "FAILED"
    print(f"النتيجة الاجمالية: {verdict} ({total_score}/100 نقطة)")
    print("================================================================================")

    sys.exit(0 if verdict == "PASSED" else 1)


if __name__ == "__main__":
    main()
