# Schema — Nexus LLM Wiki New

## هوية المساحة

- **المسار:** `/sdcard/wiki/NEXUS_LLM_WIKI_NEW/`
- **الغرض:** ويكي معرفة قابلة للتتبع والاسترجاع للنماذج اللغوية.
- **حالة المصدر:** الويكي القديمة للقراءة فقط.
- **رابط الإحالة:** مسارات ملفات نسبية من جذر هذه المساحة.

## Source

كل مصدر له سجل في `sources/`:

```yaml
type: source
source_id: SRC_YYYYMMDD_slug
title: عنوان المصدر
source_path: raw/new/original.ext
content_hash: sha256:...
media_type: transcript|article|book|conversation|code|other
language: ar|en|mixed
status: new|processed|quarantined
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

## Claim

كل Claim ملف مستقل في `claims/` أو سجل قابل للفهرسة بنفس الحقول:

```yaml
type: claim
claim_id: CLM_YYYYMMDD_slug_001
statement: صياغة الادعاء
evidence_type: direct_quote|reported_result|example|inference|hypothesis
source_id: SRC_YYYYMMDD_slug
locator: line 120-128|timestamp 00:12:31|section 3
scope: نطاق التطبيق
confidence: source_reported|supported|inferred|hypothetical|disputed
status: candidate|reviewed|accepted|rejected
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

## Concept

```yaml
type: concept
concept_id: CPT_domain_slug
title: اسم المفهوم
status: draft|reviewed|accepted|disputed|deprecated
claim_refs: [CLM_...]
source_refs: [SRC_...]
related_concepts: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

الأقسام المطلوبة حسب الصلة:

1. الجوهر.
2. الآلية.
3. الشروط.
4. الحدود وحالات الفشل.
5. أمثلة موسومة.
6. التوترات والتعارضات.
7. التطبيقات.
8. سجل الأدلة.

## Master

```yaml
type: master
master_id: MSTR_domain_slug
title: اسم الماستر
status: draft|reviewed|canonical|deprecated
concept_refs: []
claim_refs: []
coverage_status: measured|partial|unknown
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

## أنواع العلاقات

- `supports`: دليل يدعم Claim أو Concept.
- `contradicts`: تعارض صريح.
- `example_of`: مثال على مفهوم.
- `derived_from`: استنتاج مشتق من Claims.
- `related_to`: علاقة تنقل أو سياق.

لا تُستخدم علاقة عامة عندما تكون العلاقة الأدق متاحة.
