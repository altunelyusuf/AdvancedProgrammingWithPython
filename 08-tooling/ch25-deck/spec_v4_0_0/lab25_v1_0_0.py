"""Chapter 25 lab helpers, version 1.0.0 (SEN0414, Lineage14): the hidden helpers of the chapter 25 deck examples (Threads).
They give every example its own empty working folder (begin), start the local stand-in for the comic site (serve: an HTTP server of this program on 127.0.0.1; xkcd.com is never contacted),
define the downloader of the book's project against it (downloadXkcd), run a child Python program and return what it printed (py), and draw the picture of the skipped numbers (skipped_png).
Nothing here reads a clock for a printed value and nothing here uses the network outside this machine."""
__version__ = "1.0.0"
import hashlib
import http.server
import os
import struct
import subprocess
import sys
import tempfile
import threading
import warnings
import zlib

warnings.simplefilter("ignore")
U = "/root/.local/share/uv/python/"
FT = U + "cpython-3.14.6+freethreaded-linux-x86_64-gnu/bin/python3.14t"
HITS = []
BASE = [""]


def begin():
    """a new empty working folder for the example, and the thread hooks of the interpreter as they were"""
    threading.excepthook = threading.__excepthook__
    os.chdir(tempfile.mkdtemp(prefix="ch25_"))


def py(code, *args, exe=None, **env):
    """run a child Python program from a string and return what it printed, as one stripped text"""
    e = dict(os.environ, **env)
    r = subprocess.run([exe or sys.executable, "-W", "ignore", "-c", code, *args], capture_output=True, text=True, env=e, stdin=subprocess.DEVNULL)
    return (r.stdout + r.stderr).strip()


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        HITS.append(self.path)
        if self.path.startswith("/img/"):
            body, kind = b"x" * 100, "image/png"
        else:
            n = self.path.strip("/")
            body = ('<div id="comic"><img src="http://127.0.0.1:%d/img/%s.png"></div>' % (self.server.server_port, n)).encode()
            kind = "text/html"
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve():
    """the stand-in for the comic site: it answers every page with one image address; the numbers asked for are kept in HITS"""
    del HITS[:]
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True, name="stand-in").start()
    BASE[0] = "http://127.0.0.1:%d" % srv.server_port
    return srv


def requested():
    """the comic numbers the stand-in was asked for"""
    return sorted(int(p.strip("/")) for p in HITS if not p.startswith("/img/"))


def downloadXkcd(startComic, endComic):
    """the downloader of the book's project (threadedDownloadXkcd.py), with the address of the stand-in in place of xkcd.com"""
    import bs4
    import requests
    os.makedirs("xkcd", exist_ok=True)
    for urlNumber in range(startComic, endComic):
        res = requests.get(BASE[0] + "/%s" % (urlNumber))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        comicElem = soup.select("#comic img")
        if comicElem == []:
            print("Could not find comic image.")
        else:
            comicUrl = comicElem[0].get("src")
            res = requests.get(comicUrl)
            res.raise_for_status()
            imageFile = open(os.path.join("xkcd", os.path.basename(comicUrl)), "wb")
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()


def skipped_png(pages, name="skipped.png"):
    """140 cells, one for each comic number: green when the number was asked for, orange when it never was"""
    ink = {True: (47, 109, 98), False: (217, 122, 20)}
    cell, rows = 22, []
    for row in range(14):
        line = []
        for col in range(10):
            n = row * 10 + col
            c = (223, 214, 199) if n == 0 else ink[n in pages]
            line += [c] * (cell - 2) + [(250, 246, 239)] * 2
        rows += [line] * (cell - 2) + [[(250, 246, 239)] * len(line)] * 2

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in rows)
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", len(rows[0]), len(rows), 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    open(name, "wb").write(data)
    keep = os.environ.get("CH25_KEEP")
    if keep:
        open(os.path.join(keep, name), "wb").write(data)
    print("saved %s: %d bytes, sha256 %s" % (name, len(data), hashlib.sha256(data).hexdigest()[:12]))
