#!/usr/bin/env python3
"""Assemble src/*.part into a single index.html.
Each part may contain <style>...</style>, <script>...</script> and <body>...</body> blocks.
All styles go into one <style>, all scripts into one IIFE <script>, body blocks are concatenated."""
import re, sys, pathlib, json
root = pathlib.Path(__file__).parent
src = root / 'src'
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'index.html'
parts = sorted(src.glob('*.part'))
head = (src / 'head.html').read_text(encoding='utf-8')
styles, scripts, bodies = [], [], []
for p in parts:
    t = p.read_text(encoding='utf-8')
    for m in re.finditer(r'<style>(.*?)</style>', t, re.S):
        styles.append(f'/* ── {p.stem} ── */\n' + m.group(1).strip('\n'))
    for m in re.finditer(r'<script>(.*?)</script>', t, re.S):
        scripts.append(f'/* ── {p.stem} ── */\n' + m.group(1).strip('\n'))
    for m in re.finditer(r'<body>(.*?)</body>', t, re.S):
        bodies.append(m.group(1).strip('\n'))
geo = json.loads((root / 'geo' / 'seoul_min.json').read_text()) if (root / 'geo' / 'seoul_min.json').exists() else None
js = '\n\n'.join(scripts)
if geo is not None:
    js = js.replace('/*@@SEOUL_GEO@@*/null', json.dumps(geo, separators=(',', ':')))
html = head.replace('/*@@STYLE@@*/', '\n\n'.join(styles))
html = html.replace('<!--@@BODY@@-->', '\n'.join(bodies))
html = html.replace('/*@@SCRIPT@@*/', "(() => {\n'use strict';\n" + js + "\n})();")
out.write_text(html, encoding='utf-8')
print(f'wrote {out} · {len(html):,} bytes · {html.count(chr(10)):,} lines · parts={len(parts)}')
