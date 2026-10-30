#!/bin/bash
# Double-click: serves this folder on http://localhost and opens the talk in the browser.
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1 && python3 -c 'import http.server' >/dev/null 2>&1; then
  exec python3 serve.py
fi
echo "python3 was not found. Opening index.html directly (photos work; YouTube videos and music need python3)."
open index.html
