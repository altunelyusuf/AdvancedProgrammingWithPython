"""Chapter 13 deck examples, version 2.0.0: the code examples of the chapter 13 lecture deck (Web Scraping).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language
explanation that stands beside it, at most 30 words per code box); the lines of all groups of an example, in order, are the example's
code: that text is what the deck shows after the '>>> ' prompt of each line, what the chapter-code manifest lists and what the page runs.
Every example is self-contained (it imports what it uses), uses only the Python standard library, reads no keyboard, opens no
network connection and no window, leaves the current folder as it found it, and prints an ordinary line first.
A page that runs in a browser cannot reach the web, and a lecture must not depend on a site being up; the chapter's third-party
tools (requests, Beautiful Soup, Selenium, Playwright) are therefore shown by their standard-library counterparts and by small
stand-ins, and each slide says so beside the code: urllib.request on a data: address stands for requests.get(), html.parser and
xml.etree.ElementTree for Beautiful Soup, a recording function for webbrowser.open, a small class for the browser drivers.
Nothing here carries a result; deck_build_v2_0_0.py runs the code and takes every printed result from the run."""
__version__ = "2.0.0"

EXAMPLES = [
    # ------------------------------------------------------------ part 1: addresses, protocol, manners
    dict(id="url_anatomy", name="A URL cut into its parts", title="A URL is a scheme, a host, a path, a query and a fragment", part=1, visual="url_anatomy",
         concepts=["URL", "endpoint", "API"],
         groups=[
             (["from urllib.parse import urlsplit", "url = ('https://api.openweathermap.org/geo/1.0/direct'", "       '?q=Boston&appid=KEY#top')", "parts = urlsplit(url)"],
              "urlsplit cuts one address into named parts. This address asks the geocoding endpoint of a weather API for the place Boston."),
             (["for name in ('scheme', 'netloc', 'path', 'query', 'fragment'):", "    print(name.ljust(8), getattr(parts, name))"],
              "Each part has a name. The fragment, after the number sign, is kept by the browser and not sent to the server."),
         ]),
    dict(id="query_quote", name="quote and parse_qs", title="Percent codes and the query string", part=1, visual="query_quote",
         concepts=["URL", "endpoint"],
         groups=[
             (["from urllib.parse import parse_qs, quote", "print(quote('777 Valencia St, San Francisco'))"],
              "quote writes a space as %20 and a comma as %2C, because an address may not hold them. A browser does the same for its address bar."),
             (["query = parse_qs('q=San+Francisco%2CCA&appid=KEY')", "print(query)"],
              "parse_qs reads the name=value pairs back into a dictionary of lists. The plus sign and %2C turn back into a space and a comma."),
         ]),
    dict(id="status_codes", name="HTTP status codes and their classes", title="HTTP status codes: the first digit is the class", part=1, visual="status_codes",
         concepts=["HTTP and HTTPS", "HTTPS"],
         groups=[
             (["from http import HTTPStatus", "for code in (200, 301, 404, 429, 500):", "    status = HTTPStatus(code)",
               "    print(code, status.phrase, '| class', code // 100)"],
              "Every reply starts with a three-digit code. HTTPStatus names the code, and the integer division by 100 gives the class."),
         ]),
    dict(id="user_agent", name="The user-agent header", title="The user agent tells a server who is asking", part=1, visual="user_agent",
         concepts=["user agent"],
         groups=[
             (["import urllib.request", "opener = urllib.request.build_opener()", "name, value = opener.addheaders[0]",
               "print(name, '->', value.split('/')[0])"],
              "Python's own downloader announces itself. A server can tell a script from a browser by this header, and may refuse a script."),
             (["url = 'https://example.com/'", "headers = {'User-Agent': 'MyBot/1.0'}", "request = urllib.request.Request(url, headers=headers)", "print(request.get_header('User-agent'))"],
              "A polite program sets its own name, ideally with a contact address, so that a site owner knows whom to ask."),
         ]),
    dict(id="robots_rules", name="robots.txt rules with can_fetch", title="robots.txt: the paths a crawler is asked to avoid", part=1, visual="robots_rules",
         concepts=["Fetching a page"],
         groups=[
             (["import urllib.robotparser as rp", "robots = rp.RobotFileParser()", "robots.parse(['User-agent: *', 'Disallow: /simple/',", "              'Disallow: /account/'])"],
              "A robots.txt file lists the paths that crawlers are asked not to fetch. RobotFileParser reads its lines, here given as a list."),
             (["for path in ('/project/x/', '/simple/x/', '/account/login/'):", "    print(path, robots.can_fetch('*', 'https://pypi.org' + path))"],
              "can_fetch answers True or False for a path. It is a request and not a lock: a polite program honours it."),
         ]),
    dict(id="crawl_delay", name="Crawl-delay and a polite pause", title="A polite crawler waits between pages", part=1, visual="crawl_delay",
         concepts=["Fetching a page"],
         groups=[
             (["import urllib.robotparser as rp", "robots = rp.RobotFileParser()", "robots.parse(['User-agent: *', 'Crawl-delay: 2',", "              'Request-rate: 3/20'])"],
              "A site can state its own pace. Crawl-delay is the pause in seconds, and Request-rate is a number of pages per number of seconds."),
             (["pause = robots.crawl_delay('*')", "rate = robots.request_rate('*')", "print('wait', pause, 'seconds; rate', tuple(rate))"],
              "The parser returns the numbers: a pause, and a rate of 3 pages per 20 seconds. The book's comic downloader sleeps one second for the same reason."),
             (["for page, clock in zip('abc', range(0, 6, pause)):", "    print('t =', clock, 'fetch page', page)"],
              "A fake clock shows the schedule without really waiting: one fetch, then a pause of two seconds."),
         ]),
    dict(id="webbrowser_open", name="webbrowser.open with a recording stand-in", title="webbrowser.open asks your own browser to show a page", part=2, visual="webbrowser_open",
         concepts=["webbrowser", "webbrowser.open()"],
         groups=[
             (["import webbrowser", "opened = []", "webbrowser.open = lambda url: opened.append(url) or True"],
              "The real open starts your default browser. On this page a stand-in only records the address, so that no window opens."),
             (["print(webbrowser.open('https://inventwithpython.com/'))", "print(opened)"],
              "open returns True when a browser was started. The program cannot read the page: it only points the browser at it."),
         ]),
    dict(id="showmap", name="showmap.py builds a map address", title="Project 6: a map address from the command line", part=2, visual="showmap",
         concepts=["Project 6: Run a Program with the webbrowser Module", "URL"],
         groups=[
             (["from urllib.parse import quote", "argv = ['showmap.py', '777', 'Valencia', 'St,',", "        'San', 'Francisco,', 'CA', '94110']"],
              "sys.argv holds the words typed after python, with the script name first. Here the list is typed in by hand."),
             (["address = ' '.join(argv[1:])", "search = 'https://www.openstreetmap.org/search?query='", "url = search + quote(address)", "print(address)", "print(url)"],
              "Join the words after the script name, percent-encode them and add them to the search address. webbrowser.open would show it."),
         ]),
    dict(id="fetch_data", name="urlopen on a data address", title="Fetching a page: the reply has a type and a body", part=2, visual="fetch_data",
         concepts=["Fetching a page", "requests.get()"],
         groups=[
             (["from urllib.request import urlopen", "reply = urlopen('data:text/plain,Romeo%20and%20Juliet')"],
              "requests.get() downloads a page. Python's own urlopen does the same job; a data: address carries its text inside the address, so no network is needed."),
             (["print(reply.headers.get_content_type())", "body = reply.read()", "print(len(body), 'bytes:', body.decode('utf-8'))"],
              "The reply has a content type and a body of bytes. decode turns the bytes into text, like the text property of a response."),
         ]),
    dict(id="raise_status", name="A raise_for_status stand-in", title="raise_for_status stops the program on a bad reply", part=2, visual="raise_status",
         concepts=["raise_for_status()", "requests.get()"],
         groups=[
             (["from http import HTTPStatus", "def raise_for_status(code):", "    if code >= 400:", "        phrase = HTTPStatus(code).phrase", "        raise RuntimeError('%d %s' % (code, phrase))"],
              "The stand-in does what the requests method does: a code of 400 or more is an error, and the error names the problem."),
             (["for code in (200, 404, 500):", "    try:", "        raise_for_status(code)",
               "        print(code, 'fine')", "    except RuntimeError as err:", "        print(code, 'stopped:', err)"],
              "Call it after every download. A good reply passes quietly; a bad one stops the program before it saves an error page as a file."),
         ]),
    dict(id="chunks", name="iter_content writes in chunks", title="iter_content: save a download in chunks", part=2, visual="chunks",
         concepts=["iter_content()", "Downloading Files from the Web with the requests Module"],
         groups=[
             (["import os, tempfile", "body = b'To be, or not to be, that is the question.'"],
              "A downloaded file is bytes. This line is a short stand-in for a large file."),
             (["def iter_content(data, size):", "    for start in range(0, len(data), size):", "        yield data[start:start + size]"],
              "iter_content hands out the body in pieces of a chosen size, so a huge file never has to fit in memory at once."),
             (["with tempfile.TemporaryDirectory() as folder:", "    with open(os.path.join(folder, 'speech.txt'), 'wb') as file:",
               "        for chunk in iter_content(body, 16):", "            print(file.write(chunk))"],
              "write returns the number of bytes it saved. Each chunk is written in binary mode; the temporary folder disappears afterwards."),
         ]),
    # ------------------------------------------------------------ part 3: a weather API and JSON
    dict(id="json_loads", name="json.loads reads an API reply", title="An API answers in JSON; json.loads turns it into data", part=3, visual="json_loads",
         concepts=["json.loads()", "API", "Accessing a Weather API"],
         groups=[
             (["import json", "reply = ('{\"name\": \"Boston\", \"main\": {\"temp\": 285.44},'", "         ' \"weather\": [{\"main\": \"Clouds\"}]}')",
               "data = json.loads(reply)"],
              "A web API sends its answer as JSON text. json.loads turns the text into dictionaries, lists, numbers and strings."),
             (["print(data['name'], data['weather'][0]['main'])", "print(type(data).__name__, list(data))"],
              "Reach inside with keys and list positions, one step at a time. The top level is a dictionary."),
         ]),
    dict(id="kelvin", name="Kelvin to Celsius and Fahrenheit", title="The API gives Kelvin; the program converts", part=3, visual="kelvin",
         concepts=["Accessing a Weather API"],
         groups=[
             (["kelvin = 285.44", "celsius = kelvin - 273.15", "fahrenheit = celsius * 9 / 5 + 32"],
              "The weather API reports temperatures in Kelvin. Subtract 273.15 for Celsius, then scale and shift for Fahrenheit."),
             (["print('Result: %.1f C and %.1f F' % (celsius, fahrenheit))"],
              "The format %.1f keeps one decimal, as the chapter prints: 12.3 degrees Celsius and 54.1 degrees Fahrenheit."),
         ]),
    dict(id="api_url", name="An endpoint with an API key", title="An endpoint, its parameters and a secret key", part=3, visual="api_url",
         concepts=["endpoint", "API key", "API"],
         groups=[
             (["from urllib.parse import urlencode", "endpoint = 'https://api.openweathermap.org/data/2.5/forecast'",
               "params = {'lat': 42.36, 'lon': -71.06, 'appid': 'KEY'}"],
              "The endpoint is the address of one service. The parameters say which place; the appid is the API key that names your account."),
             (["url = endpoint + '?' + urlencode(params)", "print(url)", "print(url.replace('KEY', '***'))"],
              "urlencode joins the pairs with ampersands. Show the address in a log only with the key hidden: a key is a password."),
         ]),
    # ------------------------------------------------------------ part 4: reading HTML
    dict(id="html_elements", name="HTMLParser lists the tags and attributes", title="HTML is nested tags with attributes", part=4, visual="html_elements",
         concepts=["Understanding HTML", "Parsing HTML"],
         groups=[
             (["from html.parser import HTMLParser", "class Outline(HTMLParser):", "    def handle_starttag(self, tag, attrs):", "        print(tag, dict(attrs))"],
              "HTMLParser calls handle_starttag for every opening tag. The attributes arrive as a list of name and value pairs."),
             (["page = ('<p id=\"a\">Hello, <b>world</b>!</p>'", "        '<a class=\"s\" href=\"/x\">link</a>')", "Outline().feed(page)"],
              "feed walks through the page text. The p tag holds an id, the b tag has none, and the a tag holds a class and an address."),
         ]),
    dict(id="css_select", name="select, get_text and get with ElementTree", title="Pick elements by a path, read their text and attributes", part=4, visual="css_select",
         concepts=["select()", "get_text()", "get()", "CSS selector", "bs4.BeautifulSoup()"],
         groups=[
             (["import xml.etree.ElementTree as ET", "page = ('<div><p id=\"a\">Hello, <b>world</b>!</p>'", "        '<p class=\"s\"><a href=\"/x\">link</a></p></div>')",
               "root = ET.fromstring(page)"],
              "Beautiful Soup is not part of Python. ElementTree reads a well-formed page and offers the same three moves: select, get_text and get."),
             (["by_id = root.findall(\".//*[@id='a']\")", "print(len(by_id), repr(''.join(by_id[0].itertext())))"],
              "The path .//*[@id='a'] plays select('#a'). itertext gathers the text of the element and of its children, as get_text does."),
             (["link = root.find(\".//p[@class='s']/a\")", "print(link.get('href'), link.attrib)", "print(root.findall(\".//*[@class='nope']\"))"],
              "A path with a class and a child plays select('p.s > a'). get reads one attribute; no match gives an empty list."),
         ]),
    dict(id="regex_pitfall", name="A regular expression against a parser", title="Do not read HTML with a regular expression", part=4, visual="regex_pitfall",
         concepts=["Parsing HTML with Beautiful Soup", "Beautiful Soup (bs4)"],
         groups=[
             (["import re", "html = '<a href=\"/x\">x</a> <a class=\"k\" href=\"/y\">y</a>'", "print(re.findall('<a href=\"(.*?)\">', html))"],
              "The pattern expects href right after a. The second link has a class first, so the pattern silently misses it."),
             (["from html.parser import HTMLParser", "class Links(HTMLParser):", "    found = []", "    def handle_starttag(self, tag, attrs):",
               "        if tag == 'a':", "            self.found.append(dict(attrs)['href'])"],
              "A parser reads attributes by name, whatever their order. Beautiful Soup is a friendlier parser of the same kind."),
             (["Links().feed(html)", "print(Links.found)"],
              "Both links are found. Use a parser for HTML and keep regular expressions for plain text."),
         ]),
    dict(id="links_verify", name="Resolve, defragment and de-duplicate links", title="Practice program: link verification", part=4, visual="links_verify",
         concepts=["Practice Programs", "Parsing HTML"],
         groups=[
             (["from urllib.parse import urljoin, urldefrag", "site = 'https://example.com'", "page = site + '/guide/index.html'",
               "hrefs = ['intro.html', 'intro.html#top', '/about',", "         'https://other.org/x']", "seen = []"],
              "A page holds relative links, links with a fragment and links to other sites. The program must sort them out."),
             (["for href in hrefs:", "    full, fragment = urldefrag(urljoin(page, href))", "    if full.startswith(site) and full not in seen:", "        seen.append(full)",
               "print(seen)"],
              "urljoin makes every link absolute and urldefrag drops the fragment, so a page linked twice counts once. Other sites are skipped."),
         ]),
    dict(id="xkcd_chain", name="The comic image and the Prev link", title="Project 8: the image and the Prev link of a comic page", part=4, visual="xkcd_chain",
         concepts=["Project 8: Download XKCD Comics", "Parsing HTML"],
         groups=[
             (["import xml.etree.ElementTree as ET", "from urllib.parse import urljoin",
               "page = ('<body><div id=\"comic\">'", "        '<img src=\"//imgs.xkcd.com/comics/x.png\"/></div>'", "        '<a rel=\"prev\" href=\"/2/\">Prev</a></body>')",
               "root = ET.fromstring(page)"],
              "The chapter relies on the page structure of the comic site: the image sits inside the element with the id comic, and the Prev link has rel prev."),
             (["src = root.find(\".//*[@id='comic']/img\").get('src')", "prev = root.find(\".//a[@rel='prev']\").get('href')"],
              "Two paths find the image address and the address of the previous comic."),
             (["print(urljoin('https://xkcd.com/3/', src))", "print(urljoin('https://xkcd.com/3/', prev))"],
              "The image address begins with two slashes, so urljoin borrows the scheme. The loop would download, then follow Prev."),
         ]),
    dict(id="search_results", name="Open the first search results", title="Project 7: open the first results in browser tabs", part=4, visual="search_results",
         concepts=["Project 7: Open All Search Results", "webbrowser.open()"],
         groups=[
             (["import webbrowser, xml.etree.ElementTree as ET", "opened = []", "webbrowser.open = opened.append",
               "page = ('<ul><a href=\"/p/one\"/><a href=\"/p/two\"/>'", "        '<a href=\"/p/three\"/></ul>')"],
              "A recording stand-in replaces webbrowser.open again, so no tab really opens. The tiny results page holds three links; the real program downloads PyPI's."),
             (["links = ET.fromstring(page).findall('.//a')", "for link in links[:2]:", "    webbrowser.open('https://pypi.org' + link.get('href'))", "print(len(links), 'found;', opened)"],
              "Select all links, keep the first few, and open each address. The program does not wait for a person to click."),
         ]),
    dict(id="dynamic_page", name="A page built by a script", title="Why a download is not enough: pages built by a script", part=5, visual="dynamic_page",
         concepts=["Browser automation", "headless mode"],
         groups=[
             (["import xml.etree.ElementTree as ET", "source = ('<body><div id=\"app\"></div>'", "          '<script>show(\"Built by a script\")</script></body>')", "root = ET.fromstring(source)",
               "app = root.find(\".//*[@id='app']\")"],
              "This page writes its own text with a script. The downloaded source holds only an empty element and the script."),
             (["print('text in the source:', repr(app.text))"],
              "requests and a parser see exactly this: nothing to read."),
             (["script = root.find('.//script').text", "app.text = script.split('\"')[1]", "print('after the script ran:', repr(app.text))"],
              "A browser runs the script. This toy does it by hand. Selenium and Playwright drive a real browser, headless when no window is needed."),
         ]),
    dict(id="selenium_shape", name="find_element and find_elements", title="Selenium: find_element fails, find_elements does not", part=5, visual="selenium_shape",
         concepts=["webdriver.Firefox()", "find_element()", "find_elements()", "Selenium"],
         groups=[
             (["import xml.etree.ElementTree as ET", "root = ET.fromstring('<body><p>one</p><p>two</p></body>')", "def find_elements(path):", "    return root.findall(path)",
               "def find_element(path):", "    return find_elements(path)[0]"],
              "A stand-in for the page that webdriver.Firefox() would load. find_elements returns a list, possibly empty. find_element returns the first match."),
             (["print(len(find_elements('.//p')), find_element('.//p').text)", "print(find_elements('.//h1'))", "try:", "    find_element('.//h1')", "except IndexError:",
               "    print('Result: find_element fails when nothing matches')"],
              "Two paragraphs are found, and the first says one. A search for h1 gives an empty list, but find_element fails. Selenium raises NoSuchElementException; here IndexError tells the same story."),
         ]),
    dict(id="playwright_shape", name="The shape of a Playwright program", title="Playwright: start, new page, goto, locator", part=5, visual="playwright_shape",
         concepts=["sync_playwright()", "new_page()", "goto()", "locator()", "Playwright"],
         groups=[
             (["from contextlib import nullcontext", "class Page:", "    def goto(self, url):", "        print('visiting', url)", "    def locator(self, css):", "        return 'element ' + css"],
              "A stand-in page. goto visits an address; locator names the element to work with. The real locator also waits until the element is ready."),
             (["class Playwright:", "    def new_page(self):", "        return Page()"],
              "new_page opens a fresh tab. The real program first calls p.firefox.launch() to start a browser."),
             (["with nullcontext(Playwright()) as p:", "    page = p.new_page()", "    page.goto('https://example.com/')", "    print(page.locator('h1'))"],
              "sync_playwright() is used in a with block, which starts the tool and stops it at the end. The steps are the chapter's: start, new page, goto, locator."),
         ]),
    dict(id="auto_wait", name="Auto-waiting for an element", title="Interacting with a page: wait until the element is there", part=5, visual="auto_wait",
         concepts=["Interacting with a page", "locator()"],
         groups=[
             (["looks = [None, None, 'Hello']  # what each look sees"],
              "A page can build an element late. Each entry is one look: nothing, nothing, then the text."),
             (["def locator_text(limit):", "    for look, text in enumerate(looks[:limit], 1):", "        if text is not None:"],
              "Playwright keeps looking until the element is ready or time runs out. Selenium looks once."),
             (["            return 'found %r on look %d' % (text, look)", "    return 'timeout after %d looks' % limit"],
              "Return the text and the look it appeared on, or report a timeout when the looks run out."),
             (["print(locator_text(5))", "print(locator_text(2))"],
              "Five looks find the text on the third. Two looks give up, as Playwright does after thirty seconds."),
         ]),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
