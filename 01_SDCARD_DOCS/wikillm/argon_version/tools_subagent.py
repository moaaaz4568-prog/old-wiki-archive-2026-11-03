#!/usr/bin/env python3
"""subagent.py — وكلاء فرعيون عبر 9Router API مباشرة (Gemini 4 Argon Free).
استخدام: python3 subagent.py <system_prompt_file> <user_prompt_file> <output_file> [timeout_sec]
"""
import json, sys, urllib.request, pathlib

BASE = "http://127.0.0.1:20128/v1/chat/completions"
KEY = "sk-ef82ac0a5bac739d-uipxn1-f5fb32db"
MODEL = "gemini-4-argon-free"

def main():
    sysf, userf, outf = sys.argv[1], sys.argv[2], sys.argv[3]
    timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 600
    system = pathlib.Path(sysf).read_text()
    user = pathlib.Path(userf).read_text()
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 32000,
    }).encode()
    req = urllib.request.Request(BASE, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KEY}",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read())
    content = d["choices"][0]["message"]["content"]
    pathlib.Path(outf).write_text(content)
    print(f"DONE output={outf} chars={len(content)} tokens={d['usage']['total_tokens']}")

if __name__ == "__main__":
    main()
