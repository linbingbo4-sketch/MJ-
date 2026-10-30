@echo off
rem Double-click: serves this folder on http://localhost and opens the talk in the browser.
cd /d "%~dp0"
py -3 -c "import http.server" >nul 2>nul && (py -3 serve.py & goto :eof)
python -c "import http.server" >nul 2>nul && (python serve.py & goto :eof)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0serve.ps1"
