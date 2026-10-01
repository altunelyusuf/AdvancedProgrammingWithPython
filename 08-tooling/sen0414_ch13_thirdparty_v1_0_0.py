#!/usr/bin/env python3
"""Chapter 13: runs the chapter's third-party-library programs (requests, Beautiful Soup, Selenium's and Playwright's Python
interfaces) under the given interpreter, against local fixtures only, and writes or checks their recorded output.
These libraries are not part of the build interpreter, so the programs run with extra site directories on PYTHONPATH (wheels
unpacked outside the repository; the versions are printed by the first program). No browser is started and nothing leaves
this machine: the Selenium and Playwright programs only import the libraries and read their interfaces.
Usage: sen0414_ch13_thirdparty_v1_0_0.py write|check <python> <site-dir> [<site-dir> ...]
Record: 08-tooling/ch13-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import json, os, subprocess, sys
MODE, PY, SITES = sys.argv[1], sys.argv[2], sys.argv[3:]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch13-page", "third_party_record_v1_0_0.json")
EXAMPLE3 = '''<!-- This is an HTML comment. -->

<html>
<head>
    <title>Example Website Title</title>
    <style>
        .slogan {
            color: gray;
            font-size: 2em;
        }
    </style>
</head>
<body>
    <h1>Example Website</h1>
    <p>This &lt;p&gt; tag puts <b>content</b> into a <i>single</i> paragraph.</p>
    <p><a href="https://inventwithpython.com">This text is a link</a> to books by <span id="author">Al Sweigart</span>.</p>
    <p><img src="wow_such_zophie_thumb.webp" alt="Close up of my cat Zophie." /></p>
    <p class="slogan">Learn to program in Python!</p>
    <form>
        <p><label>Username: <input id="login_user" placeholder="admin" /></label></p>
        <p><label>Password: <input id="login_pass" type="password" placeholder="swordfish" /></label></p>
        <p><label>Agree to disagree: <input type="checkbox" /></label><input type="submit" value="Fake Button" /></p>
    </form>
</body>
</html>'''
BOOKLISTING = EXAMPLE3.replace('<p>This &lt;p&gt; tag', '<p>This <p> tag').replace('<a href="https://inventwithpython.com">', '<a href="https://inventwithpython.com”>')
SERVER = '''
import http.server, threading, json, os, tempfile, time
import requests
BODY = ''.join('Line %03d of a play\\n' % i for i in range(1000)).encode()
EV = threading.Event()
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path == '/rj.txt':
            self.send_response(200); self.send_header('Content-Type', 'text/plain; charset=utf-8'); self.send_header('Content-Length', str(len(BODY))); self.end_headers(); self.wfile.write(BODY)
        elif self.path == '/data.json':
            b = json.dumps({'main': {'temp': 285.44}}).encode(); self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers(); self.wfile.write(b)
        elif self.path == '/ua':
            self.send_response(200); self.end_headers(); self.wfile.write(self.headers.get('User-Agent', '').encode())
        elif self.path == '/slow':
            time.sleep(1.0); self.send_response(200); self.end_headers(); self.wfile.write(b'late')
        elif self.path == '/half':
            self.send_response(200); self.send_header('Content-Length', '10'); self.end_headers(); self.wfile.write(b'12345'); self.wfile.flush(); EV.wait(5); self.wfile.write(b'67890')
        else:
            self.send_response(404); self.end_headers(); self.wfile.write(b'nope')
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
os.environ['NO_PROXY'] = '127.0.0.1'; base = 'http://127.0.0.1:%d' % PORT
'''
PROGS = [
("versions of the libraries used", "import requests, bs4, selenium, sys\nimport soupsieve\nprint(sys.version.split()[0]); print('requests', requests.__version__); print('beautifulsoup4', bs4.__version__); print('soupsieve', soupsieve.__version__); print('selenium', selenium.__version__)\nimport importlib.metadata as m; print('playwright', m.version('playwright'))"),
("requests: Response object, status, text, errors, chunks, JSON, user agent, exceptions", SERVER + '''
r = requests.get(base + '/rj.txt')
print(type(r)); print(r.status_code == requests.codes.ok, requests.codes.ok, r.ok)
print(len(r.text), repr(r.text[:30])); print(r.headers['Content-Type'], r.encoding)
print('raise_for_status returned', r.raise_for_status())
bad = requests.get(base + '/page_that_does_not_exist'); print(bad.status_code, bad.ok)
try: bad.raise_for_status()
except Exception as exc: print(type(exc).__module__ + '.' + type(exc).__name__, str(exc).replace(str(PORT), 'PORT'))
print([c.__name__ for c in requests.exceptions.HTTPError.__mro__])
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, 'RomeoAndJuliet.txt'); sizes = []
    with open(p, 'wb') as f:
        for chunk in r.iter_content(8000): sizes.append(f.write(chunk))
    print(sizes, os.path.getsize(p), type(chunk).__name__)
rr = requests.get(base + '/data.json'); print(rr.json(), rr.json()['main']['temp'] == json.loads(rr.text)['main']['temp'])
print(requests.get(base + '/ua').text.split('/')[0])
import inspect; print(inspect.signature(requests.get))
print(inspect.getdoc(requests.Response.ok.fget).splitlines()[0])
print(issubclass(requests.exceptions.HTTPError, requests.exceptions.RequestException), issubclass(requests.exceptions.RequestException, OSError))
try: requests.get('http://127.0.0.1:1/', timeout=2)
except requests.exceptions.ConnectionError as e: print('ConnectionError raised')
'''),
("requests: no timeout by default, a timeout raises", SERVER + '''
import time
t = time.monotonic()
try: requests.get(base + '/slow', timeout=0.2)
except requests.exceptions.Timeout as e: print(type(e).__name__, [c.__name__ for c in type(e).__mro__][:3])
print(round(time.monotonic() - t, 1) < 0.9)
print(requests.get(base + '/slow').text)
'''),
("requests: stream=True returns before the body has arrived", SERVER + '''
import time
t = time.monotonic()
r = requests.get(base + '/half', stream=True)
got = r.raw.read(5)
print(got, round(time.monotonic() - t, 1) < 1.0)
EV.set(); print(r.raw.read(5))
EV.clear()
try:
    requests.get(base + '/half', timeout=0.5)
except requests.exceptions.RequestException as e:
    print('without stream=True a stalled body makes get() raise:', type(e).__name__)
'''),
("Beautiful Soup: the chapter's selections on the page the chapter downloads", "import bs4\nHTML = %r\n" % EXAMPLE3 + '''
soup = bs4.BeautifulSoup(HTML, 'html.parser')
print(type(soup))
elems = soup.select('#author')
print(type(elems), len(elems), type(elems[0]))
print(str(elems[0])); print(repr(elems[0].get_text())); print(elems[0].attrs)
ps = soup.select('p'); print(len(ps), len(soup.select('form p')))
for p in ps[:3]: print(str(p)); print(repr(p.get_text()))
span = soup.select('span')[0]; print(span.get('id'), span.get('some_nonexistent_addr') == None)
print(soup.select_one('#nothing'), soup.select('#nothing'), soup.select('#nothing') == [])
print([a.get('href') for a in soup.find_all('a')], soup.title.get_text(), soup.get_text(strip=True)[:40])
'''),
("Beautiful Soup: Table 13-2 selectors on a page that has div elements", "import bs4\n" + '''
HTML = '<div class="notice"><span>in div</span><p><span id="deep">deep</span></p></div><span>outside</span><input name="q"><input type="button" value="b"><p id="author">p</p>'
soup = bs4.BeautifulSoup(HTML, 'html.parser')
for sel in ('div', '#author', '.notice', 'div span', 'div > span', 'input[name]', 'input[type="button"]', 'p #author', 'p#author', 'p #deep'):
    print(sel, len(soup.select(sel)))
'''),
("Beautiful Soup: the page as typeset in the chapter, with a typographic quote in the link", "import bs4\nHTML = %r\n" % BOOKLISTING + '''
soup = bs4.BeautifulSoup(HTML, 'html.parser')
print(len(soup.select('#author')), len(soup.select('p')), len(soup.select('a')))
print(soup.select('a')[0].attrs)
'''),
("the search and comic programs of the chapter, with requests and Beautiful Soup, against a local fixture", SERVER + '''
import bs4, webbrowser
PAGES = {
 '/search': '<a class="package-snippet" href="/project/one/">one</a><a class="package-snippet" href="/project/two/">two</a><a class="other" href="/help/">help</a>',
 '/': '<a rel="prev" href="/2/">Prev</a><div id="comic"><img src="//COMIC/comics/three.png"></div>',
 '/2/': '<a rel="prev" href="/1/">Prev</a><div id="comic"><script>x</script></div>',
 '/1/': '<a rel="prev" href="#">Prev</a><div id="comic"><img src="//COMIC/comics/one.png"></div>',
}
class H2(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path.startswith('/comics/'): self.send_response(200); self.end_headers(); self.wfile.write(b'IMG-' + self.path.encode()); return
        key = self.path.split('?')[0]
        body = PAGES.get(key)
        if body is None: self.send_response(404); self.end_headers(); return
        self.send_response(200); self.end_headers(); self.wfile.write(body.replace('COMIC', '127.0.0.1:%d' % P2).encode())
s2 = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H2); P2 = s2.server_address[1]; threading.Thread(target=s2.serve_forever, daemon=True).start()
root = 'http://127.0.0.1:%d' % P2
res = requests.get(root + '/search?q=' + ' '.join(['boring', 'stuff'])); res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser'); link_elems = soup.select('.package-snippet')
opened = []
class Stub(webbrowser.BaseBrowser):
    def open(self, url, new=0, autoraise=True): opened.append(url); return True
webbrowser.register('stub', None, Stub('stub'), preferred=True)
for i in range(min(5, len(link_elems))):
    url_to_open = 'https://pypi.org' + link_elems[i].get('href'); print('Opening', url_to_open); webbrowser.open(url_to_open)
print(len(link_elems), len(opened))
with tempfile.TemporaryDirectory() as d:
    url = root + '/'; num_downloads = 0; MAX_DOWNLOADS = 10
    while not url.endswith('#') and num_downloads < MAX_DOWNLOADS:
        print('Downloading page', url.replace(root, 'SITE') + '...')
        res = requests.get(url); res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        comic_elem = soup.select('#comic img')
        if comic_elem == []: print('Could not find comic image.')
        else:
            comic_URL = 'http:' + comic_elem[0].get('src')
            print('Downloading image', os.path.basename(comic_URL) + '...')
            res = requests.get(comic_URL); res.raise_for_status()
            with open(os.path.join(d, os.path.basename(comic_URL)), 'wb') as image_file:
                for chunk in res.iter_content(100000): image_file.write(chunk)
        prev_link = soup.select('a[rel="prev"]')[0]
        url = root + prev_link.get('href'); num_downloads += 1
    print('Done.', sorted(os.listdir(d)), url.replace(root, 'SITE'))
'''),
("Selenium: what the chapter's tables name, read from the library without starting a browser", '''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
import selenium.common.exceptions as ex, inspect
print(webdriver.Firefox.__module__, webdriver.Firefox.__name__)
print([(n, getattr(By, n)) for n in ('CLASS_NAME', 'CSS_SELECTOR', 'ID', 'LINK_TEXT', 'PARTIAL_LINK_TEXT', 'NAME', 'TAG_NAME', 'XPATH')])
print([(n, ascii(getattr(Keys, n))) for n in ('ENTER', 'RETURN', 'HOME', 'END', 'TAB', 'F1', 'F12')])
print([m for m in ('tag_name', 'get_attribute', 'get_property', 'text', 'clear', 'is_displayed', 'is_enabled', 'is_selected', 'location', 'size', 'click', 'send_keys', 'submit') if not hasattr(WebElement, m)])
print([m for m in ('back', 'forward', 'refresh', 'quit', 'get', 'find_element', 'find_elements') if not hasattr(WebDriver, m)])
print(hasattr(ex, 'NoSuchElementException'), hasattr(ex, 'NoSuchElement'), hasattr(WebDriver, 'find_element_by_id'))
print('GET_ELEMENT_TEXT' in inspect.getsource(WebElement.text.fget), 'innerText' in inspect.getsource(WebElement.text.fget))
print(inspect.getdoc(WebElement.get_attribute).splitlines()[0])
import selenium.webdriver.common.selenium_manager as sm; print(sm.SeleniumManager.__name__)
'''),
("Playwright: what the chapter's tables name, read from the library without starting a browser", '''
from playwright.sync_api import sync_playwright, Page, Locator, BrowserType
import inspect
print([m for m in ('goto', 'title', 'go_back', 'go_forward', 'reload', 'close', 'locator', 'get_by_role', 'get_by_text', 'get_by_label', 'get_by_placeholder', 'get_by_alt_text', 'query_selector', 'click', 'check', 'uncheck', 'set_checked', 'fill', 'press') if not hasattr(Page, m)])
print([m for m in ('get_attribute', 'count', 'nth', 'first', 'last', 'all', 'inner_text', 'inner_html', 'click', 'is_visible', 'is_enabled', 'is_checked', 'bounding_box', 'fill', 'clear', 'press', 'check', 'uncheck', 'set_checked') if not hasattr(Locator, m)])
print(hasattr(Locator, 'submit'))
sig = inspect.signature(BrowserType.launch); print('headless' in sig.parameters, 'slow_mo' in sig.parameters, sig.parameters['headless'].default)
from playwright._impl import _helper; print(_helper.DEFAULT_PLAYWRIGHT_TIMEOUT_IN_MILLISECONDS)
import subprocess, sys
print(subprocess.run([sys.executable, '-m', 'playwright', '--version'], capture_output=True, text=True).stdout.strip())
print(subprocess.run([sys.executable, '-m', 'playwright', 'install', '--help'], capture_output=True, text=True).stdout.splitlines()[0])
print(inspect.getdoc(Page.query_selector).splitlines()[2][:75])
print([l.strip() for l in inspect.getdoc(Locator.is_visible).splitlines() if 'returns immediately' in l][0][:140])
'''),
]
def run(code):
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(SITES), PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([PY, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=120)
    return (r.stdout if r.returncode == 0 else r.stdout + "FAILED: " + r.stderr.strip().splitlines()[-1]).rstrip("\n")
out = [{"what": w, "code": c, "output": run(c)} for w, c in PROGS]
if MODE == "write":
    json.dump({"_version": "1.0.0", "_note": "Recorded by sen0414_ch13_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter named in the first entry, with local fixtures only.", "python": subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.strip(), "items": out}, open(REC, "w"), indent=1)
    print("recorded", len(out), "programs to", REC)
else:
    old = json.load(open(REC))["items"]; bad = [(a["what"]) for a, b in zip(old, out) if a["output"] != b["output"] or a["code"] != b["code"]]
    print("%d programs; %d differ" % (len(out), len(bad)))
    for b in bad: print("  DIFFERS", b)
    sys.exit(1 if bad else 0)
