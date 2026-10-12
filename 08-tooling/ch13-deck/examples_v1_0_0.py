"""Chapter 13 deck examples: every console session and whole program the lecture deck shows. Nothing here carries a result;
examples_run_v1_0_0.py runs it all under the interpreter given and records the results. A console group is one session: its
rows run in order in one namespace (as the deck check re-runs them per slide). No row touches the network, the file system or
raises SystemExit/KeyboardInterrupt. A row that needs a line break inside a string writes it as an escaped \\n, so the stored
row text never holds a newline character.

Programs come from sen0414_ch13_corpus_base_v1_0_0.py (the chapter's programs, each starting its own stand-in site on
127.0.0.1) plus one program written for the deck, dynamicPage, which shows why a script-built page needs a browser. Programs
marked LIVE reach a real public site when they run; only two are put on slides (searchpypiLive and weatherLive), because their
answer on 2026-10-12 does not change from run to run; xkcdLive prints the newest comics and is therefore not on a slide."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base13", os.path.join(HERE, "..", "sen0414_ch13_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

CONSOLES = {
    "title": ["' '.join(['showmap.py', '870', 'Valencia', 'St,', 'Mission'][1:])"],
    "url": ["from urllib.parse import urlsplit, parse_qs, quote",
            "urlsplit('https://api.openweathermap.org/geo/1.0/direct?q=San,CA,US&appid=KEY')[:4]",
            "parse_qs('q=San+Francisco%2CCA&appid=KEY')",
            "quote('777 Valencia St, San Francisco, CA 94110')",
            "urlsplit('https://www.openstreetmap.org/search?query=x#map=19/37.75897/-122.42142').fragment"],
    "status": ["import http, urllib.request, requests",
               "http.HTTPStatus(404).phrase",
               "[int(http.HTTPStatus.OK), http.HTTPStatus(429).phrase, http.HTTPStatus(500).phrase]",
               "urllib.request.build_opener().addheaders[0]",
               "requests.utils.default_user_agent()"],
    "robots": ["import urllib.robotparser as rp",
               "r = rp.RobotFileParser()",
               "r.parse(['User-agent: *', 'Disallow: /search*', 'Crawl-delay: 10'])",
               "r.can_fetch('*', 'https://pypi.org/project/pyautogui/')",
               "r.can_fetch('*', 'https://pypi.org/search/?q=boring+stuff')",
               "r.crawl_delay('*')"],
    "soup": ["import bs4, re",
             "soup = bs4.BeautifulSoup('<p id=\"a\">Hello, <b>world</b>!</p><p class=\"s\"><a href=\"/x\">a link</a></p>', 'html.parser')",
             "soup.select('#a')",
             "soup.select('#a')[0].get_text()",
             "soup.select('p.s > a')[0].get('href')",
             "soup.select('p.s a')[0].attrs",
             "soup.select('.nope')",
             "html = '<a href=\"/x\">x</a> <a class=\"k\" href=\"/y\">y</a>'",
             "re.findall('<a href=\"(.*?)\">', html)",
             "[a.get('href') for a in bs4.BeautifulSoup(html, 'html.parser').select('a')]"],
}

DYNAMIC_PAGE = r"""import http.server, threading, os
PAGE = b'<html><body><div id="app"></div><script>document.getElementById("app").textContent = "Built by a script, not in the source";</script></body></html>'
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        self.send_response(200); self.send_header('Content-Type', 'text/html'); self.end_headers(); self.wfile.write(PAGE)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
BASE = 'http://127.0.0.1:%d' % srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
os.environ['NO_PROXY'] = '127.0.0.1'
import bs4, requests
from playwright.sync_api import sync_playwright

html = requests.get(BASE + '/dynamic.html').text
print('requests sees the script:', '<script>' in html)
print('Beautiful Soup reads #app:', repr(bs4.BeautifulSoup(html, 'html.parser').select('#app')[0].get_text()))
with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    page.goto(BASE + '/dynamic.html')
    print('Playwright reads #app:', repr(page.locator('#app').inner_text()))
    browser.close()
"""

# name -> (code, stdin or None, live?)
PROGRAMS = {name: (code, None, live) for name, (code, _, live) in B.PROGRAMS.items() if name != "xkcdLive_v1_0_0.py"}
PROGRAMS["dynamicPage_v1_0_0.py"] = (DYNAMIC_PAGE, None, False)
