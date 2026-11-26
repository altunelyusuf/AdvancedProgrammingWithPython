"""Chapter 13 deck content, version 3.0.0: the words of the deck for the generic builder (parts, plan, route, questions, plain meanings, stories, take-aways, tables, summary, practice, resources).
The chapter's content is that of deck 2.0.0 (deck_content_v2_0_0.py and the plan and parts of the chapter's own builder deck_build_v2_0_0.py); what the rulings force is changed: the everyday pictures
become plain meanings (no analogy anywhere; the box label is IN SHORT), the six stories are the same stories with the same facts and links, told as prose in paragraphs of at most 30 words, the
table of tools is a comparison slide of its own kind, and the notes are notes_v3_0_0.py."""
__version__ = "3.0.0"

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "In short"
CONCEPTS_TAIL = "each with a plain meaning"

PARTS = {
    1: ("Part 1: Addresses and manners", "An address has parts, a reply has a code, and a polite program obeys the site's rules", [
        ("URL", "An address cut into scheme, host, path and query."),
        ("Status code", "A three-digit number whose first digit is the class."),
        ("User agent", "The name a program gives to the server."),
        ("robots.txt", "The paths a crawler is asked not to visit."),
    ]),
    2: ("Part 2: Opening and downloading", "Show a page to a person, or fetch it into the program and check the reply", [
        ("webbrowser", "Opens a page in your own browser and reads nothing."),
        ("requests", "Downloads a page or a file into the program."),
        ("raise_for_status", "Stops the program when the reply is a failure."),
        ("iter_content", "Saves a big download in small chunks."),
    ]),
    3: ("Part 3: A weather API", "A service answers in JSON; the program reads it and keeps its key secret", [
        ("API", "A service you call by address and read as data."),
        ("API key", "A secret that names your account to the service."),
        ("json.loads", "Turns JSON text into dictionaries and lists."),
        ("Kelvin", "The service's temperature scale; subtract 273.15."),
    ]),
    4: ("Part 4: Reading HTML", "A page is a tree of elements; a parser, not a pattern, finds what you need", [
        ("HTML tags", "Nested elements, each with its own attributes."),
        ("select", "Finds the elements that match a selector path."),
        ("get_text, get", "Read the text, or one attribute, of an element."),
        ("Regex trap", "A pattern misses links that a parser finds."),
    ]),
    5: ("Part 5: Driving a browser", "When a script builds the page, only a real browser can read it", [
        ("Dynamic page", "A script writes the content after the download."),
        ("Selenium", "Drives a real browser through a separate driver."),
        ("Playwright", "Drives a browser and waits by itself."),
        ("Headless", "A browser that runs with no window at all."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("code", "url_anatomy"), ("code", "query_quote"), ("code", "status_codes"), ("code", "user_agent"), ("code", "robots_rules"),
        ("story", "koster"), ("code", "crawl_delay"), ("story", "gray"),
        ("divider", 2), ("analogy", "A2"), ("analogy", "A3"), ("code", "webbrowser_open"), ("code", "showmap"), ("code", "fetch_data"), ("story", "reitz"), ("code", "raise_status"),
        ("code", "chunks"),
        ("divider", 3), ("analogy", "A4"), ("code", "json_loads"), ("code", "kelvin"), ("code", "api_url"),
        ("divider", 4), ("analogy", "A5"), ("analogy", "A6"), ("code", "html_elements"), ("code", "css_select"), ("story", "richardson"), ("code", "regex_pitfall"),
        ("code", "links_verify"), ("code", "xkcd_chain"), ("code", "search_results"),
        ("divider", 5), ("analogy", "A7"), ("analogy", "A8"), ("code", "dynamic_page"), ("story", "huggins"), ("code", "selenium_shape"), ("code", "playwright_shape"),
        ("story", "playwright"), ("code", "auto_wait"), ("compare", "tools"),
        ("current",), ("summary",), ("practice",), ("resources",)]

ROUTE_RUNS = {1: "urlsplit, quote, status codes, robots.txt", 2: "webbrowser, showmap, a download, chunks", 3: "json.loads, Kelvin, an endpoint and its key",
              4: "tags, select, links, comics, search results", 5: "a script-built page, Selenium and Playwright shapes, the tools"}

ROUTE_TAIL = ("Changes, summary, practice, resources", "what current Python and the tools add")

QUESTIONS = [("1", "Which tool reaches which kind of page, and what decides the choice?",
              "Answer on slide %d: the table of tools, from a page to show to a page a script builds.", [("compare", "tools")]),
             ("2", "Which printed outputs and programs of the book differ in current Python and on today's web?",
              "Answer on slide %d: the changes, from the chapter research.", [("current",)])]

QUESTIONS_TAKEAWAY = "Choose the tool by the page; check what changed."

ANALOGIES = [
    ("A1", "In short: addresses and manners", "An address names a page, a reply carries a status code, and a polite program names itself.", [
        ("HTTP and HTTPS", "The protocol of the Web; HTTPS adds encryption, so that the exchange cannot be read on the way."),
        ("URL", "The full address of a page: scheme, host, path, query and fragment."),
        ("HTTPS", "HTTP over an encrypted connection; the content of the page and its path are not readable on the way."),
        ("endpoint", "One address of a service that answers one kind of request."),
        ("user agent", "A header in which a program names itself to the server."),
        ("Fetching a page", "Asking a server for a page; the reply has a status code, a content type and a body."),
    ]),
    ("A2", "In short: opening a page with webbrowser", "The webbrowser module shows a page to a person and reads nothing back.", [
        ("webbrowser", "A standard module that opens a page in the person's own browser."),
        ("webbrowser.open()", "Asks the default browser to show an address; it returns True when a browser started."),
        ("Project 6: Run a Program with the webbrowser Module", "Joins the words typed on the command line into a map address and opens it."),
    ]),
    ("A3", "In short: downloading with requests", "The requests library fetches a page or a file into the program and reports how the request went.", [
        ("Downloading Files from the Web with the requests Module", "Fetches a page or a file into the program and saves it to a file."),
        ("requests", "A third-party library for HTTP, installed with pip; its slogan is HTTP for Humans."),
        ("requests.get()", "Sends a request to one address and returns a response with a status, headers and a body."),
        ("raise_for_status()", "Raises an error when the status code is 400 or more, so that a bad reply is not used."),
        ("iter_content()", "Hands out the body in chunks of a chosen size, so that a big file need not fit in memory."),
    ]),
    ("A4", "In short: a weather API", "An API is called by address and answers in data, which the program reads with json.loads.", [
        ("Accessing a Weather API", "Calls a weather service by address and reads its answer as data."),
        ("API", "A service that a program calls by address and that answers in data, not in a page."),
        ("API key", "A secret code that identifies your account to the service; keep it out of logs and repositories."),
        ("json.loads()", "Turns JSON text into dictionaries, lists, numbers and strings."),
    ]),
    ("A5", "In short: reading HTML", "A page is a tree of nested elements, and a parser reads the page text into that tree.", [
        ("Understanding HTML", "A page is nested elements; each has a tag, attributes and perhaps text."),
        ("Parsing HTML", "Reading the page text into a tree of elements that the program can search."),
        ("Parsing HTML with Beautiful Soup", "Beautiful Soup reads even badly built HTML into a tree."),
        ("Beautiful Soup (bs4)", "A third-party library, installed as beautifulsoup4, that searches HTML by selector."),
        ("bs4.BeautifulSoup()", "Builds the tree from the page text and the name of a parser."),
        ("CSS selector", "A path of tag, id and class names that picks elements, such as p.s > a."),
        ("Developer Tools", "A panel of the browser that shows the page's elements and can copy a selector."),
    ]),
    ("A6", "In short: picking things out of a page", "Three calls pick things out of a parsed page: select, get_text and get.", [
        ("select()", "Returns the list of elements that match a selector; the list is empty when none match."),
        ("get_text()", "Returns the text inside an element, without its tags."),
        ("get()", "Returns the value of one attribute of an element, such as href."),
        ("Project 7: Open All Search Results", "Selects the result links of a search page and opens the first few in browser tabs."),
        ("Project 8: Download XKCD Comics", "Downloads the comic image of a page, then follows the Prev link and repeats."),
        ("Practice Programs", "Short programs that apply the ideas of a chapter; here the link verification of slide 35."),
    ]),
    ("A7", "In short: driving a browser with Selenium", "Selenium starts a real browser through a driver and gives it commands.", [
        ("Controlling the Browser with Selenium", "A program starts a real browser through a driver and gives it commands."),
        ("Selenium", "An older, widely used tool for driving browsers; Selenium Manager finds the driver itself."),
        ("webdriver.Firefox()", "Starts a Firefox browser that the program controls."),
        ("find_element()", "Returns the first match and raises an error when there is none."),
        ("find_elements()", "Returns a list of all matches; an empty list is a valid answer."),
        ("Browser automation", "A program clicks, types and reads in a real browser."),
        ("headless mode", "A browser that runs without a window."),
    ]),
    ("A8", "In short: driving a browser with Playwright", "Playwright drives a browser and waits by itself until an element is ready.", [
        ("Controlling the Browser with Playwright", "A program drives a browser that Playwright installed, and the tool waits for each element."),
        ("Playwright", "A newer tool with its own browsers, installed by a second step, playwright install."),
        ("sync_playwright()", "A context manager that starts Playwright and stops it at the end of the with block."),
        ("new_page()", "Opens a new tab and returns a page object."),
        ("goto()", "Loads an address in the page."),
        ("locator()", "Names the element to work with; it looks again each time it is used and waits until the element is ready."),
        ("Interacting with a page", "Click, type and scroll on the elements of the page, then wait for the result."),
    ]),
]

STORIES = {
    "koster": dict(title="Story: a courtesy file for robots, 30 June 1994", img="image_koster_robots.jpg",
                   prose=["Martijn Koster wrote A Standard for Robot Exclusion, recording a consensus reached on the robots mailing list on 30 June 1994.",
                          "Some robots had swamped servers with rapid requests, or had wandered into scripts with side effects, such as voting.",
                          "The remedy was one text file, /robots.txt, that a robot reads first; nobody enforces it, so a polite program honours it.",
                          "It was published as RFC 9309 in September 2022, and Python's robot parser reads its wildcard rules since release 3.14.5."],
                   link="https://www.robotstxt.org/orig.html", linktext="A Standard for Robot Exclusion (robotstxt.org)"),
    "gray": dict(title="Story: the first spider counted 130 sites, 1993", img="image_gray_wanderer.jpg",
                 prose=["Matthew Gray wrote the World Wide Web Wanderer at MIT in spring 1993; by his account it was the first automated Web agent, or spider.",
                        "He began to find new sites and soon used it to chart the growth of the Web; traversals ran from June 1993 to January 1996.",
                        "It fetched a page, found its links, followed them and repeated, as the link program of this chapter does on a small scale.",
                        "His counts: 130 sites in June 1993, 2,738 in June 1994, 23,500 in June 1995 and 100,000 by January 1996."],
                 link="https://www.mit.edu/~mkgray/net/background.html", linktext="Internet Growth and Statistics: Credits and Background (MIT)"),
    "reitz": dict(title="Story: Requests, conceived in frustration, 13 February 2011", img="photo_kenneth_reitz.jpg",
                  prose=["Kenneth Reitz created Requests, the Python library whose slogan is HTTP for Humans; version 0.0.1 is dated 13 February 2011.",
                         "The release history lists Frustration and Conception for that day, and Birth! for version 0.2.0 on the next day.",
                         "He wanted downloading without worry about network errors, connection routing or data compression: one call, requests.get(), and then raise_for_status().",
                         "Version 2.34.2, installed for this chapter, descends from that 0.2.0; the photograph is from a talk in 2012."],
                  link="https://raw.githubusercontent.com/psf/requests/main/HISTORY.md", linktext="HISTORY.md of Requests (GitHub)"),
    "richardson": dict(title="Story: Beautiful Soup, for pages somebody else wrote, 2004", img="image_richardson_tortoise.jpg",
                       prose=["Leonard Richardson has kept Beautiful Soup since 2004. His page says that the awful page is not the reader's fault; the reader only wants its data.",
                              "The library turns tag soup, badly built HTML, into a tree that select() and get_text() can search.",
                              "Beautiful Soup 3 was the official line from May 2006 to March 2012; this chapter installs beautifulsoup4.",
                              "The picture on his site, crummy.com, is Tenniel's Mock Turtle from Alice, and the name echoes a poem there."],
                       link="https://www.crummy.com/software/BeautifulSoup/", linktext="Beautiful Soup (crummy.com)"),
    "huggins": dict(title="Story: Selenium began as a test runner for a timesheet, 2004", img="image_selenium_logo.png",
                    prose=["At ThoughtWorks in Chicago in 2004, Jason Huggins, helped by Paul Gross and Jie Tina Wang, built JavaScriptTestRunner, the first form of Selenium.",
                           "It tested an internal Time and Expenses application in Python and Plone, and ran as JavaScript inside the browser.",
                           "Simon Stewart built WebDriver separately; the two merged, so a program can drive a browser from outside, through a driver.",
                           "The webdriver.Firefox() of this chapter descends from that merge."],
                    link="https://www.selenium.dev/history/", linktext="Selenium History (selenium.dev)"),
    "playwright": dict(title="Story: Playwright reached Python on 30 September 2020", img="image_playwright_logo.png",
                       prose=["On 30 September 2020 Arjun Attam, a program manager at Microsoft, announced Playwright for Python in preview on the Microsoft for Python Developers blog.",
                              "InfoQ had reported Playwright itself on 30 January 2020; the same team had built Puppeteer at Google.",
                              "Its promise is reliable end-to-end tests without timeouts, because it waits for the page to be ready by itself.",
                              "It is event-driven and listens to browser events such as DOM changes, network requests and navigations; the last example imitates the waiting."],
                       link="https://devblogs.microsoft.com/python/announcing-playwright-for-python-reliable-end-to-end-testing-for-the-web/",
                       linktext="Announcing Playwright for Python (Microsoft)"),
}

TAKEAWAY = {
    "url_anatomy": "An address has five named parts.", "query_quote": "Quote on the way out; parse_qs on the way in.", "status_codes": "The first digit is the class of the reply.",
    "user_agent": "Name your program and give a contact.", "robots_rules": "robots.txt is a request: honour it.", "crawl_delay": "Wait between pages; the site may say how long.",
    "webbrowser_open": "open shows a page; it cannot read it.", "showmap": "Join the words, quote them, open the address.", "fetch_data": "A reply has a type and a body of bytes.",
    "raise_status": "Check every reply before you save it.", "chunks": "Save a big download chunk by chunk.",
    "json_loads": "JSON text becomes dictionaries and lists.", "kelvin": "Kelvin minus 273.15 is Celsius.", "api_url": "The key is a password: hide it in logs.",
    "html_elements": "HTML is nested tags with attributes.", "css_select": "select, get_text and get: the three moves.", "regex_pitfall": "Use a parser for HTML, not a pattern.",
    "links_verify": "Absolute, no fragment, same site, once.", "xkcd_chain": "Image address, then the Prev link, then repeat.", "search_results": "Select the links, open the first few.",
    "dynamic_page": "A script-built page needs a real browser.", "selenium_shape": "find_element fails; find_elements gives a list.", "playwright_shape": "Start, new page, goto, locator.",
    "auto_wait": "Playwright waits for the element; Selenium looks once.",
}

COMPARES = {
    "tools": dict(title="Which tool for which page", sub="From a page to show to a page that a script builds",
                  rows=[["Page in front of the program", "Tool", "Why"],
                        ["A person should see the page", "webbrowser", "Opens the user's own browser; reads nothing"],
                        ["A known address, text or a file", "requests", "get, raise_for_status, a timeout, chunks"],
                        ["A service that offers an API", "requests and json", "Structured answer; a key identifies you"],
                        ["Static HTML to read", "Beautiful Soup", "Parses the text received; select, get_text, get"],
                        ["A page built by a script, or a login", "Selenium or Playwright", "Only a real browser runs the script"]],
                  colw=[3.2, 2.4, 3.4], rowh=0.6, fs=12, takeaway="Choose the tool by the page in front of the program."),
}

CURRENT_SUB = "What differs from the book, from the chapter research"

CURRENT = [["What changed", "What it means for the chapter", "Example"],
           ["urllib.robotparser reads the wildcard * and the end mark $ (Python 3.14.5)", "A rule like Disallow: /search* now blocks the path", "robots_rules"],
           ["PurePath.as_uri() is deprecated; use Path.as_uri() (Python 3.14)", "file:// addresses of local help pages", ""],
           ["datetime.utcfromtimestamp() is deprecated (Python 3.12)", "Forecast times: fromtimestamp, in the machine's time zone", ""],
           ["Selenium Manager finds the driver and browser itself (Selenium 4.51.0)", "No manual geckodriver download", "selenium_shape"],
           ["The error is NoSuchElementException (Selenium 4.51.0)", "The chapter writes NoSuchElement", "selenium_shape"],
           ["Browsers are installed by a second step, playwright install (Playwright 1.63.0)", "pip install alone is not enough", "playwright_shape"],
           ["Pass a timeout; use stream=True for a file (Requests 2.34.2)", "A call without a timeout can hang", "raise_status"],
           ["The PyPI search page answers with a challenge page (12 Oct 2026)", "searchpypi.py finds no result links", "search_results"]]

CURRENT_TAKEAWAY = "Run what the book printed; then check what changed."

SUMMARY_ANALOGY = "A summary keeps only the five ideas you need to take away from the lecture."

SUMMARY_POINTS = ["An address has parts; a reply has a status code.",
                  "A polite program reads robots.txt, waits and names itself.",
                  "Check every reply, and save big files in chunks.",
                  "An API answers in JSON; the key is a password.",
                  "Parse HTML with a parser; use a real browser only when a script builds the page."]

SUMMARY_TAKEAWAY = "Choose the tool by the page; behave politely."

PRACTICE_SUB = "Predict first, then run what you can on the chapter page"

PRACTICE_ANALOGY = "Practice questions are short drills: predict the answer first, then run the code."

PRACTICE = ["Cut 'https://xkcd.com/3/#top' into its parts. Which part does the server never receive?",
            "A robots file says Disallow: /search/. What does can_fetch give for '/search/?q=a'?",
            "Convert 300 Kelvin to Celsius and Fahrenheit with the code of the Kelvin slide.",
            "Practice program: list the pages one link away on a page, without counting a page twice."]

PRACTICE_TAKEAWAY = "Each answer fits in a few lines you can run."

RESOURCES_SUB = "Reading and watching, chosen for this chapter; every link is live"

RESOURCES_TAKEAWAY = "Pick one link and read it before the next class."

RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 13", "https://automatetheboringstuff.com/3e/chapter13.html", "automatetheboringstuff.com"),
    ("Python documentation: urllib.parse", "https://docs.python.org/3/library/urllib.parse.html", "docs.python.org"),
    ("Python documentation: urllib.robotparser", "https://docs.python.org/3/library/urllib.robotparser.html", "docs.python.org"),
    ("Python documentation: html.parser", "https://docs.python.org/3/library/html.parser.html", "docs.python.org"),
    ("Python documentation: webbrowser", "https://docs.python.org/3/library/webbrowser.html", "docs.python.org"),
    ("Requests: Quickstart", "https://requests.readthedocs.io/en/latest/user/quickstart/", "requests.readthedocs.io"),
    ("Beautiful Soup documentation", "https://www.crummy.com/software/BeautifulSoup/bs4/doc/", "crummy.com"),
    ("Selenium: locator strategies", "https://www.selenium.dev/documentation/webdriver/elements/locators/", "selenium.dev"),
    ("Playwright for Python: locators", "https://playwright.dev/python/docs/locators", "playwright.dev"),
    ("RFC 9309: Robots Exclusion Protocol", "https://www.rfc-editor.org/rfc/rfc9309", "rfc-editor.org"),
    ("MDN: CSS selectors", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors", "developer.mozilla.org"),
    ("MDN: HTTP response status codes", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status", "developer.mozilla.org"),
    ("OpenWeather: Geocoding API", "https://openweathermap.org/api/geocoding-api", "openweathermap.org"),
    ("Video: Web testing with Playwright (PyOhio 2022)", "https://pyvideo.org/pyohio-2022/a-quickstart-to-web-testing-with-playwright.html", "pyvideo.org"),
]
