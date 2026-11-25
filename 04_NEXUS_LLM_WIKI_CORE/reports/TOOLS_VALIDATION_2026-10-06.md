# Wiki quality report

## الأدوات

- `tools/wiki_quality.py`: يتحقق من frontmatter، فرادة IDs، وجود المصدر، بصمة المصدر الخام، تطابق `evidence_start/evidence_end` مع `evidence_quote`، بصمة المقتطف، حراس نوع الدليل، مراجع Concepts، والروابط المحلية. لا يكتب شيئًا إلا عند تمرير `--index` أو `--report` صراحة.
- `tools/wiki_query.py`: استرجاع lexical محلي بسيط مع تطبيع عربي، أوزان للعنوان والبيان والنطاق، واستبعاد `candidate/rejected` وConcepts المسودة افتراضيًا. استخدم `--include-drafts` لرؤية المسودات.

## أوامر التحقق

```text
python3 /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py --vault /sdcard/NEXUS_LLM_WIKI --index --report /sdcard/NEXUS_LLM_WIKI/reports/TOOLS_VALIDATION_2026-10-06.md --json
python3 -m py_compile /sdcard/NEXUS_LLM_WIKI/tools/wiki_quality.py /sdcard/NEXUS_LLM_WIKI/tools/wiki_query.py
```

النتيجة: `PASS`، مع 5 Sources و15 Claims و4 Concepts و0 Masters و0 أخطاء.

## اختبارات استرجاع

- سؤال السكريبت والاستماع أعاد Claim إدارة المكالمة وConcept السكريبت المرن مع `--include-drafts`.
- سؤال «12 نقطة معيار عالمي للاحتفاظ» أعاد Claim المثال، ولم يحوله إلى معيار.
- سؤال «أسعار الطقس على المريخ» أعاد `insufficient_evidence: true`.

## الحدود

- الاسترجاع lexical وليس embedding أو semantic reranking.
- لا يستنتج التعارضات تلقائيًا؛ التعارضات تسجل تحريريًا في Concepts والتقارير.
- لا يثبت صحة النتائج التجارية؛ يتحقق من التتبع البنيوي ومطابقة النص فقط.

```json
{
  "ok": true,
  "vault": "/sdcard/NEXUS_LLM_WIKI",
  "counts": {
    "sources": {
      "files": 5,
      "statuses": {
        "processed": 5
      }
    },
    "claims": {
      "files": 15,
      "statuses": {
        "reviewed": 15
      }
    },
    "concepts": {
      "files": 4,
      "statuses": {
        "draft": 4
      }
    },
    "masters": {
      "files": 0,
      "statuses": {}
    }
  },
  "errors": []
}
```
