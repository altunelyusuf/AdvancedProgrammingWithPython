#!/usr/bin/env python3
"""SEN0414 chapter 13 (Web Scraping, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of
sen0414_ch12_corpus_base_v1_0_0.py (written fresh for this chapter). Each program is a complete script: running it prints
what it printed on 2026-10-12 under Python 3.14.6 (uv), except where a program is marked LIVE below.

A web program needs a web site, so most programs below start a tiny site of their own on 127.0.0.1 in a thread (the text
SITE_HEAD) and point the chapter's program at it, changing only the address and, where the chapter sleeps for a second, the
sleep. Everything else in the chapter's code is kept, and a comment says so wherever it is not. Programs that import
requests, bs4, selenium or playwright need those packages; run the file with a Python that has them (the venv of the build:
uv venv, uv pip install requests beautifulsoup4 selenium playwright). Selenium finds Firefox through Selenium Manager and
Playwright finds the Firefox its own `playwright install firefox` put into PLAYWRIGHT_BROWSERS_PATH; both run headless here,
since this machine has no display.

* SHOWMAP is the chapter's showmap.py, run with a command line argument and with none, with stand-in webbrowser and
  pyperclip modules put into sys.modules (a browser cannot open here and the clipboard raised PyperclipException) so that the
  address each would have received is printed. Standard library only.
* DOWNLOAD_CHECKED is the review's download: requests.get(), raise_for_status(), iter_content(8000) written in 'wb' mode, and
  the 404 that raise_for_status() turns into an exception.
* SEARCHPYPI_LOCAL is the chapter's searchpypi.py against a stand-in results page that carries a.package-snippet links, so that
  the min(5, len(link_elems)) tabs open.
* SEARCHPYPI_LIVE is the same program unchanged against pypi.org, which answered 200 with a client-challenge page that holds no
  .package-snippet element: nothing opens. LIVE.
* XKCD_LOCAL is the chapter's downloadXkcdComics.py (with the Step 4 indentation repaired, since the printed listing raises
  IndentationError) against a stand-in comic site whose first page has a Prev link of '#'.
* XKCD_LIVE is the same program against xkcd.com with MAX_DOWNLOADS = 2. LIVE: the pages are the latest comics, so the numbers
  printed change from day to day.
* WEATHER_STANDIN calls a stand-in of the OpenWeather endpoint with requests, reads the JSON and converts kelvin to Celsius;
  WEATHER_LIVE sends the chapter's fake key to the real endpoint and prints the status and the type of the cod field. LIVE.
* LINK_CHECK reads every link of a page with Beautiful Soup and asks for each with requests.head(), reporting the status.
* POLITE_CRAWLER reads a robots.txt with urllib.robotparser, skips the disallowed paths and honours Crawl-delay. Standard library.
* SELENIUM_FORM and PLAYWRIGHT_CHECKBOX are the chapter's browser programs (open the page, find the login fields, fill and
  submit; check a box) in headless Firefox against the stand-in site.

Not run: the clipboard of pyperclip, a visible browser window, the OpenWeather programs with a real key, and the game 2048.

Sources read for this chapter, on 2026-10-12: the book chapter (automatetheboringstuff.com/3e/chapter13.html, sha256 2f5a8737...8895
as the book's ontology records), the Python 3.14 documentation (webbrowser, urllib.parse, urllib.request, urllib.robotparser,
http.server), and the documents of requests, Beautiful Soup, Selenium and Playwright.
"""
__version__ = "1.0.0"

# ---------------------------------------------------------------------------------------------------------------------------------
# The stand-in site every local program starts. One text, shared.
# ---------------------------------------------------------------------------------------------------------------------------------
SITE_HEAD = r"""import http.server, json, threading
PNG = bytes.fromhex('89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d49444154789c6360f8ffff3f0005fe02fea7d6054c0000000049454e44ae426082')
def comic(n):
    prev = '#' if n == 1 else '/%d/' % (n - 1)
    return ('<html><body><div id="comic"><img src="//%%s/comics/c%d.png"/></div><a rel="prev" href="%s">Prev</a></body></html>' % (n, prev)).encode()
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, code, body, ctype='text/html'):
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(body))); self.end_headers()
        if self.command != 'HEAD': self.wfile.write(body)
    def do_HEAD(self): self.do_GET()
    def do_GET(self):
        p, host = self.path.split('?')[0], self.headers['Host']
        if p == '/': self.send(200, comic(3).replace(b'%s', host.encode()))
        elif p in ('/2/', '/1/'): self.send(200, comic(int(p[1])).replace(b'%s', host.encode()))
        elif p.startswith('/comics/'): self.send(200, PNG, 'image/png')
        elif p == '/search/': self.send(200, ''.join('<a class="package-snippet" href="/project/p%d/">p%d</a>' % (i, i) for i in range(8)).encode())
        elif p == '/data/2.5/weather': self.send(200, json.dumps({'weather': [{'main': 'Clouds', 'description': 'broken clouds'}], 'main': {'temp': 285.44, 'humidity': 78}, 'cod': 200}).encode(), 'application/json')
        elif p == '/links.html': self.send(200, b'<a href="/ok">ok</a> <a href="/gone">gone</a> <a href="/ok">ok again</a>')
        elif p == '/ok': self.send(200, b'ok')
        elif p == '/robots.txt': self.send(200, b'User-agent: *\nDisallow: /private/\nCrawl-delay: 1\n', 'text/plain')
        elif p in ('/a', '/b', '/private/c'): self.send(200, b'page ' + p.encode())
        elif p == '/rj.txt': self.send(200, ''.join('Line %03d of a play\n' % i for i in range(1000)).encode(), 'text/plain; charset=utf-8')
        elif p == '/login.html': self.send(200, b'<html><head><title>Login</title></head><body><form action="/welcome.html"><input id="login_user" placeholder="admin"/><input id="login_pass" type="password"/><label>Agree <input type="checkbox"/></label></form></body></html>')
        elif p == '/welcome.html': self.send(200, b'<html><head><title>Welcome</title></head><body>welcome</body></html>')
        else: self.send(404, b'nope', 'text/plain')
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
HOST = '127.0.0.1:%d' % srv.server_address[1]; BASE = 'http://' + HOST
threading.Thread(target=srv.serve_forever, daemon=True).start()
import os; os.environ['NO_PROXY'] = '127.0.0.1'
"""

STAND_INS = r"""import sys, types
opened = []
webbrowser = types.ModuleType('webbrowser'); webbrowser.open = lambda url: opened.append(url) or True
pyperclip = types.ModuleType('pyperclip'); pyperclip.paste = lambda: '777 Valencia St, San Francisco, CA'
sys.modules['webbrowser'] = webbrowser; sys.modules['pyperclip'] = pyperclip
"""

# ---------------------------------------------------------------------------------------------------------------------------------
SHOWMAP = r"""import runpy, sys, tempfile, types
from pathlib import Path

SHOWMAP = '''#! python3
# showmap.py - Launches a map in the browser using an address from the
# command line or clipboard

import webbrowser, sys, pyperclip
if len(sys.argv) > 1:
    # Get address from command line.
    address = ' '.join(sys.argv[1:])
else:
    # Get address from clipboard.
    address = pyperclip.paste()

# Open the web browser.
webbrowser.open('https://www.openstreetmap.org/search?query=' + address)
'''
opened = []
webbrowser = types.ModuleType('webbrowser'); webbrowser.open = lambda url: opened.append(url) or True
pyperclip = types.ModuleType('pyperclip'); pyperclip.paste = lambda: '777 Valencia St, San Francisco, CA'
sys.modules['webbrowser'] = webbrowser; sys.modules['pyperclip'] = pyperclip
with tempfile.TemporaryDirectory() as d:
    script = Path(d, 'showmap.py'); script.write_text(SHOWMAP)
    for argv in (['showmap.py', '870', 'Valencia', 'St,', 'Mission', 'District'], ['showmap.py']):
        sys.argv = argv
        runpy.run_path(str(script))
        print((' '.join(argv[1:]) or '(clipboard)').ljust(34), '->', opened[-1])
"""

DOWNLOAD_CHECKED = SITE_HEAD + r"""import tempfile
import requests

res = requests.get(BASE + '/rj.txt')
res.raise_for_status()
print(res.status_code, len(res.text), res.headers['Content-Type'])
with tempfile.TemporaryDirectory() as d:
    path = os.path.join(d, 'RomeoAndJuliet.txt')
    play_file = open(path, 'wb')
    sizes = []
    for chunk in res.iter_content(8000):
        sizes.append(play_file.write(chunk))
    play_file.close()
    print(sizes, os.path.getsize(path))
response = requests.get(BASE + '/page_that_does_not_exist')
try:
    response.raise_for_status()
except Exception as exc:
    print(f'There was a problem: {exc}'.replace(BASE, 'SITE'))
"""

SEARCHPYPI_PROGRAM = r"""# searchpypi.py - Opens several search results on pypi.org
import requests, sys, webbrowser, bs4

print('Searching...')  # Display text while downloading the search results page.
res = requests.get(SEARCH + ' '.join(sys.argv[1:]))
res.raise_for_status()

# Retrieve top search result links.
soup = bs4.BeautifulSoup(res.text, 'html.parser')
# Open a browser tab for each result.
link_elems = soup.select('.package-snippet')
num_open = min(5, len(link_elems))
for i in range(num_open):
    url_to_open = 'https://pypi.org' + link_elems[i].get('href')
    print('Opening', url_to_open)
    webbrowser.open(url_to_open)
print(len(link_elems), 'links found;', num_open, 'opened')
"""

SEARCHPYPI_LOCAL = SITE_HEAD + STAND_INS + "SEARCH = BASE + '/search/?q='\nsys.argv = ['searchpypi.py', 'boring', 'stuff']\n" + SEARCHPYPI_PROGRAM

SEARCHPYPI_LIVE = STAND_INS + "SEARCH = 'https://pypi.org/search/?q='\nsys.argv = ['searchpypi.py', 'boring', 'stuff']\n" + SEARCHPYPI_PROGRAM

XKCD_PROGRAM = r"""# downloadXkcdComics.py - Downloads XKCD comics

import requests, os, bs4, time, tempfile

os.chdir(tempfile.mkdtemp())
show = lambda text: text.replace(HOME, 'SITE') if SCHEME == 'http' else text   # the stand-in's port changes on every run
url = START  # Starting URL
os.makedirs('xkcd', exist_ok=True)  # Store comics in ./xkcd
num_downloads = 0
while not url.endswith('#') and num_downloads < MAX_DOWNLOADS:
    # Download the page.
    print(show(f'Downloading page {url}...'))
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the URL of the comic image.
    comic_elem = soup.select('#comic img')
    if comic_elem == []:
        print('Could not find comic image.')
    else:
        comic_URL = 'https:' + comic_elem[0].get('src') if SCHEME == 'https' else 'http:' + comic_elem[0].get('src')
        # Download the image.
        print(show(f'Downloading image {comic_URL}...'))
        res = requests.get(comic_URL)
        res.raise_for_status()

        # Save the image to ./xkcd.
        image_file = open(os.path.join('xkcd', os.path.basename(comic_URL)), 'wb')
        for chunk in res.iter_content(100000):
            image_file.write(chunk)
        image_file.close()

    # Get the Prev button's URL.
    prev_link = soup.select('a[rel="prev"]')[0]
    url = HOME + prev_link.get('href')
    num_downloads += 1
    time.sleep(SLEEP)  # Pause so we don't hammer the web server.

print('Done.', sorted(os.listdir('xkcd')) if SCHEME == 'http' else len(os.listdir('xkcd')), 'file(s) saved')
"""

XKCD_LOCAL = SITE_HEAD + "START, HOME, SCHEME, MAX_DOWNLOADS, SLEEP = BASE, BASE, 'http', 10, 0.05\n" + XKCD_PROGRAM

XKCD_LIVE = "START, HOME, SCHEME, MAX_DOWNLOADS, SLEEP = 'https://xkcd.com', 'https://xkcd.com', 'https', 2, 1\n" + XKCD_PROGRAM

WEATHER_STANDIN = SITE_HEAD + r"""import requests

res = requests.get(BASE + '/data/2.5/weather', params={'q': 'San Francisco,CA,US', 'appid': 'KEY'})
res.raise_for_status()
data = res.json()
kelvin = data['main']['temp']
print(res.url.replace(BASE, 'SITE'))
print(data['weather'][0]['description'], '|', kelvin, 'K =', round(kelvin - 273.15, 1), 'C |', data['main']['humidity'], '% humidity')
"""

WEATHER_LIVE = r"""import requests

res = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q': 'San Francisco,CA,US', 'appid': 'YOUR_API_KEY_HERE'}, timeout=20)
print(res.status_code, res.headers.get('Content-Type'))
try:
    body = res.json()
    print(body, '| cod is a', type(body['cod']).__name__)
except ValueError:
    print('not JSON:', res.text[:80])
"""

LINK_CHECK = SITE_HEAD + r"""import bs4, requests

page = requests.get(BASE + '/links.html')
soup = bs4.BeautifulSoup(page.text, 'html.parser')
seen = set()
for a in soup.select('a[href]'):
    href = a.get('href')
    if href in seen:
        continue
    seen.add(href)
    status = requests.head(BASE + href, timeout=5).status_code
    print(href.ljust(6), status, 'ok' if status < 400 else 'BROKEN')
"""

POLITE_CRAWLER = SITE_HEAD + r"""import time, urllib.request
from urllib.robotparser import RobotFileParser

rp = RobotFileParser(BASE + '/robots.txt')
rp.read()
agent = 'ch13-class-bot'
delay = rp.crawl_delay(agent)
print('crawl delay:', delay)
started = time.monotonic()
for path in ('/a', '/private/c', '/b'):
    if not rp.can_fetch(agent, BASE + path):
        print('skip ', path, '(robots.txt disallows it)')
        continue
    with urllib.request.urlopen(BASE + path) as f:
        print('get  ', path, '->', f.status, f.read().decode())
    time.sleep(delay)
print('waited at least', int(time.monotonic() - started), 'seconds')
"""

SELENIUM_FORM = SITE_HEAD + r"""from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

opts = webdriver.FirefoxOptions()
opts.add_argument('-headless')           # no display on this machine; the chapter shows a window
browser = webdriver.Firefox(options=opts)
browser.get(BASE + '/login.html')
print(browser.title)
user_elem = browser.find_element(By.ID, 'login_user')
user_elem.send_keys('your_real_username_here')
password_elem = browser.find_element(By.ID, 'login_pass')
password_elem.send_keys('your_real_password_here')
print(user_elem.get_property('value'), '|', password_elem.get_attribute('type'))
password_elem.submit()
WebDriverWait(browser, 10).until(lambda b: b.title == 'Welcome')
print(browser.current_url.replace(BASE, 'SITE'), '|', browser.title)
browser.quit()
"""

PLAYWRIGHT_CHECKBOX = SITE_HEAD + r"""from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch()             # headless by default
    page = browser.new_page()
    page.goto(BASE + '/login.html')
    print(page.title())
    box = page.locator('input[type=checkbox]')
    print(box.is_checked())
    box.check()
    print(box.is_checked())
    page.locator('#login_user').fill('your_real_username_here')
    print(page.locator('#login_user').input_value())
    browser.close()
"""

# name: (program text, packages it needs, live?)
PROGRAMS = {
    "showmap_v1_0_0.py": (SHOWMAP, (), False),
    "downloadChecked_v1_0_0.py": (DOWNLOAD_CHECKED, ("requests",), False),
    "searchpypiLocal_v1_0_0.py": (SEARCHPYPI_LOCAL, ("requests", "bs4"), False),
    "searchpypiLive_v1_0_0.py": (SEARCHPYPI_LIVE, ("requests", "bs4"), True),
    "xkcdLocal_v1_0_0.py": (XKCD_LOCAL, ("requests", "bs4"), False),
    "xkcdLive_v1_0_0.py": (XKCD_LIVE, ("requests", "bs4"), True),
    "weatherStandIn_v1_0_0.py": (WEATHER_STANDIN, ("requests",), False),
    "weatherLive_v1_0_0.py": (WEATHER_LIVE, ("requests",), True),
    "linkCheck_v1_0_0.py": (LINK_CHECK, ("requests", "bs4"), False),
    "politeCrawler_v1_0_0.py": (POLITE_CRAWLER, (), False),
    "seleniumForm_v1_0_0.py": (SELENIUM_FORM, ("selenium",), False),
    "playwrightCheckbox_v1_0_0.py": (PLAYWRIGHT_CHECKBOX, ("playwright",), False),
}

if __name__ == "__main__":
    import os, subprocess, sys
    for name, (code, needs, live) in PROGRAMS.items():
        env = dict(os.environ)
        if os.environ.get("CH13_PW_BROWSERS"): env["PLAYWRIGHT_BROWSERS_PATH"] = os.environ["CH13_PW_BROWSERS"]
        env["PATH"] = os.pathsep.join(d for d in env.get("PATH", "").split(os.pathsep) if not os.path.exists(os.path.join(d, "chromedriver")))
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=300)
        print("=== %s (exit %d)%s" % (name, r.returncode, " LIVE" if live else "")); print(r.stdout.rstrip()); print(r.stderr[-300:].rstrip())
