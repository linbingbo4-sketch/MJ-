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


def fetch_photos():
    """Copy the free-licensed Commons photos the page uses into media/photos/ once, so later talks work offline."""
    import urllib.parse, urllib.request
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    want = re.findall(r"file: '([^']+\.jpg)', commons: '([^']+)'", html)
    folder = os.path.join(ROOT, 'media', 'photos'); os.makedirs(folder, exist_ok=True)
    missing = [(f, c) for f, c in want if not os.path.isfile(os.path.join(folder, f))]
    got = 0
    for f, c in missing:
        url = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(c) + '?width=1200'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'BeyondTheSpotlight/1.0 (classroom talk; local photo cache)'})
            data = urllib.request.urlopen(req, timeout=30).read()
            if data[:3] != b'\xff\xd8\xff':
                continue
            tmp = os.path.join(folder, f + '.part')
            with open(tmp, 'wb') as out:
                out.write(data)
            os.replace(tmp, os.path.join(folder, f)); got += 1
        except Exception:
            pass
    if missing:
        print(f'Photos: saved {got} of {len(missing)} to media/photos/' + ('' if got == len(missing) else ' (the rest load online)'))


def main():
    threading.Thread(target=fetch_photos, daemon=True).start()
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
