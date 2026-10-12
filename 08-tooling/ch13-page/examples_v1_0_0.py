"""Chapter 13 (Web Scraping) page examples, version 1.0.0: the console sessions the page's Lab tab (Chapter examples) offers.

Every session is standard library only and works with no network, so that it runs both under CPython 3.14.6 here (which records
the output in examples_out_v1_0_0.json) and in the page's own in-browser Python. The programs of the chapter that need a web
site, requests, Beautiful Soup, Selenium or Playwright are in sen0414_ch13_corpus_base_v1_0_0.py and were run against a stand-in
site; they cannot run in a browser tab, so the page shows the behaviour they rest on - addresses, status codes, robots.txt rules,
HTML events, JSON - with the same standard-library calls, and the last session shows that Selenium is not part of Python.
"""
__version__ = "1.0.0"

CONSOLES = {
    "urlparts": [
        "from urllib.parse import urlsplit, parse_qs, quote",
        "u = urlsplit('https://api.openweathermap.org/geo/1.0/direct?q=San+Francisco,CA&appid=KEY')",
        "u.scheme",
        "u.netloc",
        "u.path",
        "parse_qs(u.query)",
        "quote('777 Valencia St, San Francisco, CA')",
        "urlsplit('https://www.openstreetmap.org/search?query=x#map=19/37.75897/-122.42142').fragment",
    ],
    "urlbuild": [
        "from urllib.parse import urlencode, urljoin, urldefrag",
        "urlencode({'q': 'San Francisco,CA', 'appid': 'KEY'})",
        "'https://api.openweathermap.org/geo/1.0/direct?' + urlencode({'q': 'San Francisco,CA', 'limit': 1})",
        "urljoin('https://site.example/books/index.html', '../about.html')",
        "urljoin('https://site.example/books/index.html', '/ok.html')",
        "urldefrag('https://site.example/ok.html#top')",
    ],
    "status": [
        "from http import HTTPStatus",
        "HTTPStatus(404).phrase",
        "HTTPStatus.OK.value",
        "HTTPStatus(429).phrase",
        "[(s, s < 400) for s in (200, 301, 404, 500)]",
        "[HTTPStatus(s).is_success for s in (200, 204, 301, 404)]",
    ],
    "robots": [
        "import urllib.robotparser as rp",
        "r = rp.RobotFileParser()",
        "r.parse(['User-agent: *', 'Disallow: /private/', 'Crawl-delay: 10'])",
        "r.can_fetch('*', 'https://site.example/a')",
        "r.can_fetch('*', 'https://site.example/private/c')",
        "r.crawl_delay('*')",
    ],
    "htmlevents": [
        "from html.parser import HTMLParser",
        "class Events(HTMLParser):\n    def __init__(self):\n        super().__init__()\n        self.log = []\n    def handle_starttag(self, tag, attrs):\n        self.log.append(('start', tag, attrs))\n    def handle_data(self, data):\n        self.log.append(('text', data))\n    def handle_endtag(self, tag):\n        self.log.append(('end', tag))",
        "p = Events()",
        "p.feed('<p>Hello, <a href=\"/x\">link</a></p>')",
        "p.log",
        "import html",
        "html.unescape('&lt;p&gt; &amp; &copy;')",
        "html.escape('<p> & \"q\"')",
    ],
    "regexpitfall": [
        "import re",
        "pages = ['<a href=\"https://a.example/x\">', \"<a href='https://a.example/y'>\", '<a class=\"n\" href=\"https://a.example/z\">']",
        "[re.findall(r'<a href=\"([^\"]*)\">', t) for t in pages]",
        "from html.parser import HTMLParser",
        "class Hrefs(HTMLParser):\n    def __init__(self):\n        super().__init__()\n        self.found = []\n    def handle_starttag(self, tag, attrs):\n        if tag == 'a':\n            self.found.append(dict(attrs).get('href'))",
        "found = []\nfor t in pages:\n    h = Hrefs()\n    h.feed(t)\n    found.append(h.found)",
        "found",
    ],
    "json": [
        "import json",
        "text = '[{\"name\": \"San Francisco\", \"lat\": 37.7790262, \"lon\": -122.419906}]'",
        "data = json.loads(text)",
        "type(data).__name__",
        "data[0]['lat']",
        "json.loads('[]')",
        "json.loads('{\"cod\": \"400\", \"message\": \"wrong latitude\"}')['message']",
        "round(285.44 - 273.15, 1)",
        "round(285.44 * (9 / 5) - 459.67, 1)",
    ],
    "bytes": [
        "import io",
        "f = io.BytesIO()",
        "f.write('caf\\u00e9'.encode('utf-8'))",
        "(len('caf\\u00e9'), len('caf\\u00e9'.encode('utf-8')))",
        "data = bytes(178978)",
        "[len(data[i:i + 100000]) for i in range(0, len(data), 100000)]",
    ],
    "linkcheck": [
        "from html.parser import HTMLParser\nfrom urllib.parse import urljoin, urldefrag, urlsplit",
        "class Links(HTMLParser):\n    def __init__(self):\n        super().__init__()\n        self.hrefs = []\n    def handle_starttag(self, tag, attrs):\n        if tag == 'a':\n            self.hrefs.append(dict(attrs).get('href'))",
        "BASE = 'https://site.example/index.html'",
        "p = Links()",
        "p.feed('<a href=\"/ok.html\">a</a> <a href=\"/gone.html\">b</a> <a href=\"/ok.html#top\">c</a> <a href=\"mailto:al@example.com\">d</a> <a>e</a>')",
        "p.hrefs",
        "sorted({urldefrag(urljoin(BASE, h))[0] for h in p.hrefs if h and urlsplit(urljoin(BASE, h)).scheme in ('http', 'https')})",
    ],
    "showmap": [
        "import sys",
        "sys.argv = ['showmap.py', '777', 'Valencia', 'St,', 'San', 'Francisco,', 'CA', '94110']",
        "' '.join(sys.argv[1:])",
        "from urllib.parse import quote",
        "'https://www.openstreetmap.org/search?query=' + quote(' '.join(sys.argv[1:]))",
        "len(sys.argv) > 1",
    ],
    "packages": [
        "import importlib.util",
        "importlib.util.find_spec('json') is None",
        "importlib.util.find_spec('selenium') is None",
        "from selenium import webdriver",
    ],
}
