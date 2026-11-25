#!/usr/bin/env python3
"""Embed the measured snapshot in the single-file, offline explanation page."""
from pathlib import Path
import json

PAGE = Path('/sdcard/NEXUS_WIKI_EXPLAIN.html')
SNAPSHOT = Path('/sdcard/NEXUS_LLM_WIKI/reports/EXPLAIN_SNAPSHOT_2026-10-07.json')
data = json.loads(SNAPSHOT.read_text(encoding='utf-8'))
html = PAGE.read_text(encoding='utf-8')
start = html.index('<script id="snapshot" type="application/json">') + len('<script id="snapshot" type="application/json">')
end = html.index('</script>', start)
encoded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
PAGE.write_text(html[:start] + encoded + html[end:], encoding='utf-8')
print(f'page={PAGE} bytes={PAGE.stat().st_size} concepts={len(data["concepts"])}')
