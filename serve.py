#!/usr/bin/env python3
"""Serve this folder on http://localhost and open the talk in the browser.

The page needs http(s): the embedded YouTube player refuses file:// pages. Byte ranges are supported so the
local videos in media/ can be scrubbed (Safari will not play a video without them)."""
import http.server, os, re, socketserver, sys, threading, webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def send_head(self):
        m = re.match(r'bytes=(\d*)-(\d*)$', self.headers.get('Range', ''))
        path = self.translate_path(self.path)
        if not m or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        a, b = m.groups()
        start = int(a) if a else max(0, size - int(b or 0))
        end = int(b) if a and b else size - 1
        if start >= size or start > end:
            self.send_response(416); self.send_header('Content-Range', f'bytes */{size}'); self.end_headers()
            return None
        f = open(path, 'rb'); f.seek(start)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        self._left = end - start + 1
        return f

    def copyfile(self, src, dst):
        left = getattr(self, '_left', None)
        if left is None:
            return super().copyfile(src, dst)
        while left > 0:
            chunk = src.read(min(64 * 1024, left))
            if not chunk:
                break
            dst.write(chunk); left -= len(chunk)
        self._left = None

    def log_message(self, *a):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def main():
    for port in range(8000, 8020):
        try:
            srv = Server(('127.0.0.1', port), Handler)
            break
        except OSError:
            continue
    else:
        sys.exit('No free port between 8000 and 8019.')
    url = f'http://localhost:{port}/index.html'
    print(f'BEYOND THE SPOTLIGHT  →  {url}\nKeep this window open while presenting. Close it (or Ctrl+C) to stop.')
    threading.Timer(.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
