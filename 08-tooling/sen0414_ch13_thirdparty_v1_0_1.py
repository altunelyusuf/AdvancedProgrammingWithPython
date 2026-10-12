#!/usr/bin/env python3
"""Chapter 13: runs the chapter's third-party-library programs (requests, Beautiful Soup, Selenium, Playwright) under the given
interpreter, against local fixtures only, and writes or checks their recorded output.
1.0.1 (over 1.0.0): the Selenium and Playwright programs of the chapter are now run in a real browser. Headless Firefox is
used, the browser the chapter names: Selenium 4 finds and downloads Firefox and geckodriver itself through Selenium Manager
(the programs below pass no driver or browser path), and Playwright launches the Firefox that `python -m playwright install
firefox` put into the folder PLAYWRIGHT_BROWSERS_PATH names (give it as the environment variable CH13_PW_BROWSERS). Where the
chapter opens a window the programs run headless, since this machine has no display (launching a headed browser here is
itself recorded). The pages are served from this machine; example3.html is the file the chapter downloads, byte for byte.
The libraries are installed in a virtual environment of the interpreter (uv venv, uv pip install requests beautifulsoup4
selenium playwright), or sit in extra site directories given on the command line; the versions are printed by the first program.
Usage: sen0414_ch13_thirdparty_v1_0_1.py write|check <python> [<site-dir> ...]
Record: 08-tooling/ch13-page/third_party_record_v1_0_1.json"""
__version__ = "1.0.1"
import json, os, subprocess, sys
MODE, PY, SITES = sys.argv[1], sys.argv[2], sys.argv[3:]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch13-page", "third_party_record_v1_0_1.json")
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
BSRV = "EXAMPLE3_TEXT = %r\n" % EXAMPLE3 + r'''
import hashlib, http.server, threading, time
EX3 = EXAMPLE3_TEXT.replace('\n', '\r\n').encode()      # the bytes of https://autbor.com/example3.html (CRLF line ends)
assert hashlib.sha256(EX3).hexdigest() == 'c7a82b398aad79c3ea1112e116472f2016ae612aabc680432b367fd2c591d375'
LOCAL3 = EX3.replace(b'https://inventwithpython.com', b'/books')
PAGES = {
 '/example3.html': ('text/html; charset=utf-8', EX3),
 '/example3_local.html': ('text/html; charset=utf-8', LOCAL3),
 '/books': ('text/html', b'<title>Books</title><h1>Books by Al Sweigart</h1>'),
 '/tall.html': ('text/html', ('<html><body>' + '<p style="height:200px">row</p>' * 30 + '</body></html>').encode()),
 '/dynamic.html': ('text/html', b'<html><body><div id="app"></div><script>document.getElementById("app").textContent = "Built by a script, not in the source";</script></body></html>'),
 '/hidden.html': ('text/html', b'<p id="h" style="display:none">secret</p><p id="v">shown</p><p id="u" style="text-transform:uppercase">loud  and   spaced</p>'),
 '/keys.html': ('text/html', b'<html><body><script>window.log = []; document.addEventListener("keydown", e => window.log.push(e.key));</script><p>press keys</p></body></html>'),
}
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        key = self.path.split('?')[0]
        if key == '/ua':
            self.send_response(200); self.send_header('Content-Type', 'text/plain'); self.end_headers(); self.wfile.write(self.headers.get('User-Agent', '').encode())
        elif key in PAGES:
            ct, body = PAGES[key]; self.send_response(200); self.send_header('Content-Type', ct); self.end_headers(); self.wfile.write(body)
        else:
            self.send_response(404); self.end_headers(); self.wfile.write(b'nope')
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:%d' % PORT
local = lambda u: u.replace(base, 'SITE')
'''
SEL = r'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
opts = webdriver.FirefoxOptions(); opts.add_argument('-headless')    # no display on this machine; the chapter shows a window
'''
PWR = r'''
from playwright.sync_api import sync_playwright
'''
PROGS += [
("Selenium in a real browser: the chapter's start, find_elements, text and innerHTML, the link, the login fields", BSRV + SEL + r"""
browser = webdriver.Firefox(options=opts)
print(type(browser))
browser.get(base + '/example3.html')
print(browser.title, '|', browser.capabilities['browserName'], browser.capabilities['browserVersion'].split('.')[0])
elems = browser.find_elements(By.CSS_SELECTOR, 'p')
print(len(elems)); print(elems[0].text); print(elems[0].get_property('innerHTML'))
print(elems[0].text == elems[0].get_property('innerText'), elems[0].tag_name)
browser.get(base + '/example3_local.html')
link_elem = browser.find_element(By.LINK_TEXT, 'This text is a link')
print(type(link_elem)); link_elem.click()
WebDriverWait(browser, 10).until(lambda b: b.current_url.endswith('/books')); print(local(browser.current_url), browser.title)
browser.get(base + '/example3.html')
user_elem = browser.find_element(By.ID, 'login_user'); user_elem.send_keys('your_real_username_here')
password_elem = browser.find_element(By.ID, 'login_pass'); password_elem.send_keys('your_real_password_here')
print(user_elem.get_property('value'), user_elem.get_attribute('placeholder'), password_elem.get_attribute('type'))
password_elem.submit()
WebDriverWait(browser, 10).until(lambda b: b.current_url.endswith('?')); print(local(browser.current_url))
browser.back(); WebDriverWait(browser, 10).until(lambda b: not b.current_url.endswith('?')); print(local(browser.current_url))
browser.forward(); WebDriverWait(browser, 10).until(lambda b: b.current_url.endswith('?')); print(local(browser.current_url))
browser.refresh(); print(browser.title)
browser.quit()
"""),
("Selenium: a missing element, find_elements, the properties of Table 13-4 and the tells of automation", BSRV + SEL + r"""
browser = webdriver.Firefox(options=opts)
browser.get(base + '/example3.html')
try: browser.find_element(By.ID, 'nope')
except NoSuchElementException as e: print(type(e).__name__, '|', str(e).splitlines()[0])
print(browser.find_elements(By.ID, 'nope'))
box = browser.find_element(By.XPATH, '//input[@type="checkbox"]')
print(box.is_displayed(), box.is_enabled(), box.is_selected()); box.click(); print(box.is_selected())
print(sorted(box.size), sorted(box.location))
print([(n, len(browser.find_elements(by, v))) for n, by, v in (('CLASS_NAME', By.CLASS_NAME, 'slogan'), ('NAME', By.NAME, 'nothing'), ('TAG_NAME', By.TAG_NAME, 'P'), ('PARTIAL_LINK_TEXT', By.PARTIAL_LINK_TEXT, 'is a link'), ('ID', By.ID, 'author'))])
span = browser.find_element(By.ID, 'author'); print(span.text, span.get_attribute('id'), span.get_attribute('nothing'))
browser.get(base + '/hidden.html')
for i in 'hvu': e = browser.find_element(By.ID, i); print(i, repr(e.text), repr(e.get_property('innerText')), repr(e.get_property('textContent')), e.is_displayed())
print('navigator.webdriver:', browser.execute_script('return navigator.webdriver'))
ua = browser.execute_script('return navigator.userAgent'); print(ua.split(') ')[-1])
browser.get(base + '/ua'); print(browser.find_element(By.TAG_NAME, 'body').text.split(' ')[-1])
browser.quit()
import requests; print(requests.get(base + '/ua').text.split('/')[0])
"""),
("Selenium: Keys.END and Keys.HOME scroll a page, and arrow keys reach a page's script", BSRV + SEL + r"""
import time
browser = webdriver.Firefox(options=opts)
browser.get(base + '/tall.html')
html_elem = browser.find_element(By.TAG_NAME, 'html')
y = lambda: browser.execute_script('return Math.round(window.scrollY)')
html_elem.send_keys(Keys.END); time.sleep(0.5); bottom = y(); print('after END, scrolled down:', bottom > 0)
html_elem.send_keys(Keys.HOME); time.sleep(0.5); print('after HOME, scrollY:', y())
browser.get(base + '/keys.html')
body = browser.find_element(By.TAG_NAME, 'body')
for key in (Keys.UP, Keys.RIGHT, Keys.DOWN, Keys.LEFT) * 2: body.send_keys(key)
print(browser.execute_script('return window.log'))
browser.quit()
"""),
("Playwright in a real browser: the chapter's first program, a Response, and the locators of Table 13-5", BSRV + PWR + r"""
with sync_playwright() as playwright:
    browser = playwright.firefox.launch()
    page = browser.new_page()
    response = page.goto(base + '/example3.html')
    print(page.title()); print(local(repr(response)))
    print(browser.browser_type.name, browser.version.split('.')[0])
    for name, loc in (('get_by_role checkbox', page.get_by_role('checkbox')), ('get_by_role heading', page.get_by_role('heading', name='Example Website')),
                      ('get_by_text', page.get_by_text('is a link')), ('get_by_label', page.get_by_label('Agree')),
                      ('get_by_placeholder', page.get_by_placeholder('admin')), ('get_by_alt_text', page.get_by_alt_text('Zophie')), ('locator p', page.locator('p'))):
        print(name.ljust(21), loc.count(), loc.first.evaluate('e => e.tagName'))
    browser.close()
"""),
("Playwright: Locator methods of Table 13-6, strictness, and the answers that come at once", BSRV + PWR + r"""
with sync_playwright() as playwright:
    browser = playwright.firefox.launch(); page = browser.new_page(); page.goto(base + '/example3.html')
    elems = page.locator('p')
    print(elems.nth(0).inner_text()); print(elems.nth(0).inner_html())
    print(elems.count(), elems.first.inner_text() == elems.nth(0).inner_text(), repr(elems.last.inner_text()), len(elems.all()))
    try: elems.inner_text()
    except Exception as e: print(type(e).__name__, '|', str(e).splitlines()[0][:70])
    print(page.locator('a').get_attribute('href'), page.locator('#author').is_visible(), page.locator('#nope').is_visible(), page.query_selector('#nope'))
    box = page.locator('input[type=checkbox]'); print(box.is_enabled(), box.is_checked(), sorted(page.locator('p').first.bounding_box()))
    browser.close()
"""),
("Playwright: click toggles a checkbox, check, uncheck and set_checked set it, fill, clear, press and the missing submit", BSRV + PWR + r"""
with sync_playwright() as playwright:
    browser = playwright.firefox.launch(); page = browser.new_page(); page.goto(base + '/example3.html')
    checkbox_elem = page.get_by_role('checkbox'); state = []
    page.click('input[type=checkbox]'); state.append(checkbox_elem.is_checked()); page.click('input[type=checkbox]'); state.append(checkbox_elem.is_checked())
    print('click, click        ->', state); state = []
    checkbox_elem.check(); checkbox_elem.check(); state.append(checkbox_elem.is_checked()); checkbox_elem.uncheck(); checkbox_elem.uncheck(); state.append(checkbox_elem.is_checked())
    checkbox_elem.set_checked(True); state.append(checkbox_elem.is_checked()); checkbox_elem.set_checked(False); state.append(checkbox_elem.is_checked())
    print('check, uncheck, set -> ', state)
    page.locator('#login_user').fill('your_real_username_here'); page.locator('#login_pass').fill('your_real_password_here')
    print(page.locator('#login_user').input_value(), page.locator('#login_pass').input_value())
    page.locator('#login_user').clear(); print(repr(page.locator('#login_user').input_value()))
    print('Locator has submit():', hasattr(page.locator('input[type=submit]'), 'submit'))
    page.locator('input[type=submit]').click(); page.wait_for_url('**/example3.html?'); print(local(page.url))
    page.go_back(); print(local(page.url)); page.go_forward(); print(local(page.url)); page.reload(); print(page.title())
    page.goto(base + '/tall.html'); y = lambda: page.evaluate('Math.round(window.scrollY)')
    page.locator('html').press('End'); page.wait_for_timeout(500); print('after End, scrolled down:', y() > 0)
    page.locator('html').press('Home'); page.wait_for_timeout(500); print('after Home, scrollY:', y())
    page.goto(base + '/example3.html'); page.locator('html').press('Control+A'); print('Control+A selects more than 100 characters of the page:', len(page.evaluate('document.getSelection().toString()')) > 100)
    page.goto(base + '/keys.html')
    for key in ('ArrowUp', 'ArrowRight', 'ArrowDown', 'ArrowLeft') * 2: page.locator('html').press(key)
    print(page.evaluate('window.log'))
    browser.close()
"""),
("Playwright: the 30 second pause for a mistyped selector, and the interactive start and stop", BSRV + PWR + r"""
import time
playwright = sync_playwright().start()
browser = playwright.firefox.launch(slow_mo=50)
page = browser.new_page(); page.goto(base + '/example3.html')
t = time.monotonic()
try: page.locator('#login_usr').click()
except Exception as e: print(type(e).__name__, '|', str(e).splitlines()[0], '| waited', round(time.monotonic() - t), 's')
t = time.monotonic(); print(page.locator('#login_usr').is_visible(), page.query_selector('#login_usr'), 'answered in under a second:', time.monotonic() - t < 1)
t = time.monotonic()
try: page.locator('#login_usr').click(timeout=500)
except Exception as e: print(type(e).__name__, '| with timeout=500 waited', round(time.monotonic() - t, 1), 's')
browser.close(); playwright.stop()
"""),
("Playwright: headed launch without a display, and what playwright install would fetch", PWR + r"""
import os, subprocess, sys
env = {k: v for k, v in os.environ.items() if k != 'DISPLAY'}
with sync_playwright() as playwright:
    try: playwright.firefox.launch(headless=False)
    except Exception as e: print(type(e).__name__, '|', [l.strip() for l in str(e).splitlines() if 'XServer' in l or 'headed' in l][0][:90])
r = subprocess.run([sys.executable, '-m', 'playwright', 'install', '--dry-run'], capture_output=True, text=True, env=env)
print([l.split(' (')[0] for l in r.stdout.splitlines() if l and not l.startswith(' ')])
"""),
("A page built by a script: requests and Beautiful Soup see an empty element, the browser sees the text", BSRV + PWR + r"""
import requests, bs4
soup = bs4.BeautifulSoup(requests.get(base + '/dynamic.html').text, 'html.parser')
print(soup.select('#app')[0].get_text() == '', 'script' in requests.get(base + '/dynamic.html').text)
with sync_playwright() as playwright:
    browser = playwright.firefox.launch(); page = browser.new_page(); page.goto(base + '/dynamic.html')
    print(page.locator('#app').inner_text()); browser.close()
"""),
]

SRV2 = r"""
import http.server, json, threading, time
FORECAST = {'list': [{'dt': 1790000000 + 10800 * i, 'main': {'temp': 285.44 - i * 0.1, 'feels_like': 284.9, 'humidity': 78}, 'weather': [{'main': 'Clouds', 'description': 'broken clouds'}]} for i in range(40)]}
SITE = {
 '/index.html': '<a href="/ok.html">fine</a> <a href="/gone.html">broken</a> <a href="https://other.example/x">elsewhere</a> <a href="/ok.html#top">again</a> <a href="mailto:a@b.example">mail</a> <a>no href</a>',
 '/ok.html': '<p>ok</p>',
 '/photos': '<img class="photo" src="/img/cat.png"><img class="photo" src="/img/dog.png"><img src="/logo.png">',
}
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, code, body, ctype='text/html'):
        self.send_response(code); self.send_header('Content-Type', ctype); self.end_headers(); self.wfile.write(body if isinstance(body, bytes) else body.encode())
    def do_GET(self):
        path, _, query = self.path.partition('?'); self.server.seen.append(self.path)
        if path == '/geo/1.0/direct':
            if 'appid=KEY' not in query: return self.send(401, json.dumps({'cod': 401, 'message': 'Invalid API key.'}), 'application/json')
            if 'q=Nowhere' in query: return self.send(200, '[]', 'application/json')
            return self.send(200, json.dumps([{'name': 'San Francisco', 'lat': 37.7790262, 'lon': -122.419906, 'country': 'US', 'state': 'California'}]), 'application/json')
        if path == '/data/2.5/weather':
            if 'lat=999' in query: return self.send(400, json.dumps({'cod': '400', 'message': 'wrong latitude'}), 'application/json')
            return self.send(200, json.dumps({'coord': {'lon': -122.4199, 'lat': 37.779}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds'}], 'main': {'temp': 285.44, 'feels_like': 284.9, 'humidity': 78}, 'name': 'San Francisco', 'cod': 200}), 'application/json')
        if path == '/data/2.5/forecast': return self.send(200, json.dumps(FORECAST), 'application/json')
        if path.startswith('/img/') or path == '/logo.png': return self.send(200, b'PNG-' + path.encode(), 'image/png')
        if path == '/robots.txt': return self.send(200, 'User-agent: *\nDisallow: /private\nCrawl-delay: 1\n', 'text/plain')
        if path in SITE: return self.send(200, SITE[path])
        if path in ('/a', '/b', '/c'): return self.send(200, '<a href="/b">b</a> <a href="/c">c</a> <a href="/private/x">private</a>')
        self.send(404, 'missing')
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); srv.seen = []
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:%d' % srv.server_address[1]
"""
PROGS += [
("the weather program of the chapter against a local stand-in service: latitude, temperature, forecast, error shapes", SRV2 + r"""
import json, requests, datetime
city_name = 'San Francisco'; state_code = 'CA'; country_code = 'US'; API_key = 'KEY'
response = requests.get(f'{base}/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}')
print(response.status_code, response.headers['content-type'])
response_data = json.loads(response.text); print(type(response_data).__name__, response_data[0]['lat'], response_data[0]['lon'])
lat = json.loads(response.text)[0]['lat']; lon = json.loads(response.text)[0]['lon']
response = requests.get(f'{base}/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'); response_data = json.loads(response.text)
print(response_data['weather'][0]['main'], response_data['weather'][0]['description'], response_data['main']['temp'], response_data['main']['humidity'])
print(round(285.44 - 273.15, 1), round(285.44 * (9 / 5) - 459.67, 1))
response_data = json.loads(requests.get(f'{base}/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}').text)
print(len(response_data['list']), response_data['list'][0]['dt'], sorted(response_data['list'][0]))
print(datetime.datetime.fromtimestamp(response_data['list'][0]['dt'], tz=datetime.timezone.utc).isoformat(), (response_data['list'][-1]['dt'] - response_data['list'][0]['dt']) / 3600)
print(json.loads(requests.get(f'{base}/geo/1.0/direct?q=Nowhere&appid=KEY').text))
bad = requests.get(f'{base}/data/2.5/weather?lat=999&lon=0&appid=KEY'); print(bad.status_code, json.loads(bad.text))
wrong = requests.get(f'{base}/geo/1.0/direct?q=San Francisco&appid=nope'); print(wrong.status_code, wrong.json())
print(requests.Request('GET', f'{base}/geo/1.0/direct', params={'q': 'San Francisco,CA,US', 'appid': 'KEY'}).prepare().url.replace(base, 'SITE'))
"""),
("practice program: link verification with requests and Beautiful Soup, relative links made absolute, 404s printed", SRV2 + r"""
import bs4, requests, urllib.parse
page = base + '/index.html'
soup = bs4.BeautifulSoup(requests.get(page).text, 'html.parser')
seen = set()
for a in soup.select('a'):
    href = a.get('href')
    if not href: continue
    url = urllib.parse.urldefrag(urllib.parse.urljoin(page, href))[0]
    if not url.startswith(base) or url in seen: continue
    seen.add(url)
    if requests.get(url).status_code == 404: print('Broken link:', url.replace(base, 'SITE'), a.get_text())
print(len(soup.select('a')), 'a elements,', len(seen), 'checked')
"""),
("practice program: an image site downloader, every photo of a results page saved with iter_content", SRV2 + r"""
import bs4, os, requests, tempfile
res = requests.get(base + '/photos'); res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
with tempfile.TemporaryDirectory() as d:
    for img in soup.select('img.photo'):
        url = base + img.get('src'); r = requests.get(url); r.raise_for_status()
        with open(os.path.join(d, os.path.basename(url)), 'wb') as f:
            for chunk in r.iter_content(100000): f.write(chunk)
    print(sorted(os.listdir(d)), len(soup.select('img')), 'img elements,', len(soup.select('img.photo')), 'downloaded')
"""),
("a polite crawler: robots.txt read before the crawl, Crawl-delay obeyed, a disallowed path skipped", SRV2 + r"""
import bs4, requests, time, urllib.parse, urllib.robotparser
robots = urllib.robotparser.RobotFileParser(); robots.parse(requests.get(base + '/robots.txt').text.splitlines())
delay = robots.crawl_delay('*'); print('Crawl-delay:', delay)
queue = ['/a']; done = []; t0 = time.monotonic(); skipped = []
while queue:
    path = queue.pop(0)
    if path in done or path in skipped: continue
    if not robots.can_fetch('*', base + path): skipped.append(path); continue
    soup = bs4.BeautifulSoup(requests.get(base + path).text, 'html.parser'); done.append(path)
    queue += [a.get('href') for a in soup.select('a[href]')]
    time.sleep(delay)
print(done, 'skipped', skipped, '| took at least', round(len(done) * delay), 's:', time.monotonic() - t0 >= len(done) * delay)
"""),
]

def run(code):
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(SITES), PYTHONDONTWRITEBYTECODE="1")
    if os.environ.get("CH13_PW_BROWSERS"): env["PLAYWRIGHT_BROWSERS_PATH"] = os.environ["CH13_PW_BROWSERS"]
    env["PATH"] = os.pathsep.join(d for d in env.get("PATH", "").split(os.pathsep) if not os.path.exists(os.path.join(d, "chromedriver")))  # a stray chromedriver on PATH is not for Firefox
    r = subprocess.run([PY, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=300)
    return (r.stdout if r.returncode == 0 else r.stdout + "FAILED: " + r.stderr.strip().splitlines()[-1]).rstrip("\n")
out = [{"what": w, "code": c, "output": run(c)} for w, c in PROGS]
if MODE == "write":
    json.dump({"_version": "1.0.1", "_note": "Recorded by sen0414_ch13_thirdparty_v1_0_1.py write; every output was printed by the program beside it under the interpreter named in the first entry, with local fixtures only.", "python": subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.strip(), "items": out}, open(REC, "w"), indent=1)
    print("recorded", len(out), "programs to", REC)
else:
    old = json.load(open(REC))["items"]; bad = [(a["what"]) for a, b in zip(old, out) if a["output"] != b["output"] or a["code"] != b["code"]]
    print("%d programs; %d differ" % (len(out), len(bad)))
    for b in bad: print("  DIFFERS", b)
    sys.exit(1 if bad else 0)
