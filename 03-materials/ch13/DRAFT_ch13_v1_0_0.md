# Chapter 13 draft — Web Scraping (3rd edition)

## Status

State check (ex:TK5_StateCheck_Ch13, Lineage5) found no gap against the current standard: all six story slides match their sourced companion-script text exactly, the resources slide's 15 links are live and correct, and all 24 code examples check out — 14 need no network and were re-run to an exact match of the recorded output; the other 10 use `requests`, a weather API, Selenium or Playwright, which this sandbox cannot reach (no outbound network or browser), so they were syntax-checked (0 errors) and read against each library's own documented call signatures instead of executed. This is a direct write-up of already-correct content, not a correction pass — same situation as chapters 11-12. One open item outside the chapter's own content: a legacy YA-suffixed deck duplicating this subject, already decided this turn (see Open items).

## 1. The story

Six real, dated, sourced beats, told in the order the deck teaches them:

1. **1993 — Matthew Gray, the first spider.** Gray wrote the World Wide Web Wanderer at MIT in spring 1993 to traverse the Web and collect sites — at first to find new ones, then to chart the Web's growth. His own counts: 130 sites in June 1993, 623 in December 1993, 2,738 in June 1994, 23,500 in June 1995, 100,000 by January 1996 when the traversals ended. He calls it the first automated Web agent, or spider — fetch a page, find its links, follow them, repeat, exactly what the chapter's toy downloader does. (mit.edu/~mkgray/net/background.html)
2. **1994-06-30 — Martijn Koster, robots.txt.** Koster wrote *A Standard for Robot Exclusion*, recording a 30 June 1994 consensus on the robots mailing list, after some robots had swamped servers with rapid requests or wandered into side-effecting cgi scripts. The remedy: one file at `/robots.txt` that a robot reads first — explicitly not an official standard, not enforced by anyone, and no guarantee any robot honours it. It became RFC 9309 in September 2022 (Koster, Illyes, Zeller, Sassman); Python's `urllib.robotparser` only read its wildcard rules from release 3.14.5 (10 May 2026). (robotstxt.org/orig.html)
3. **2004 — Leonard Richardson, Beautiful Soup.** Richardson's own page: "You didn't write that awful page. You're just trying to get some data out of it" — since 2004 the library has saved screen-scraping hours. The name plays on the poem in *Alice's Adventures in Wonderland* and on "tag soup," poorly structured HTML. Beautiful Soup 3 ran May 2006–March 2012; `beautifulsoup4`, installed this chapter, is the fourth line. As of 12 October 2026 the author's page names 4.14.3 (30 Nov 2025) current, while pip installed 4.15.0 — a library's own page can lag its releases. (crummy.com/software/BeautifulSoup)
4. **2004 — Jason Huggins, Paul Gross, Jie Tina Wang, Selenium.** Selenium's own history: it began in 2004 at ThoughtWorks Chicago, where Huggins (helped by Gross and Wang) built Core mode as JavaScriptTestRunner to test an internal Time and Expenses app written in Python and Plone. Colleagues liked the immediate visual feedback; Paul Hammant pushed to open-source it and add a driven mode usable over the wire from any language. Separately, Simon Stewart built WebDriver (no JavaScript dependency, a client coded per browser); the two merged — the chapter's `webdriver.Firefox()` descends from that merge. (selenium.dev/history)
5. **2011-02-13 — Kenneth Reitz, Requests.** The project's own release history: v0.0.1 (13 Feb 2011) lists "Frustration" and "Conception"; v0.2.0, the next day, lists "Birth!" PyPI's first upload is dated 14 Feb 2011. "Lovingly created by Kenneth Reitz," slogan "HTTP for Humans" — exactly the chapter's promise of downloading without worrying about network errors, routing or compression. Version 2.34.2, installed 12 October 2026, descends from that 0.2.0. (github.com/psf/requests/HISTORY.md)
6. **2020-09-30 — Arjun Attam and the Playwright team, Microsoft.** InfoQ reported 30 Jan 2020 that Microsoft (the same team that had built Puppeteer at Google) announced Playwright as a Puppeteer alternative. On 30 Sept 2020, program manager Arjun Attam announced Playwright for Python in preview, noting the JavaScript version shipped earlier that year. Its headline claim — timeout-free, event-driven auto-waiting on DOM changes, network requests, page navigations — is exactly the chapter's auto-waiting, including the thirty seconds a mistyped selector costs. (devblogs.microsoft.com/python)

## 2. Explanations

- A URL decomposes into scheme, host, path, query and fragment; percent-codes and the query string (`quote`, `parse_qs`) handle characters a URL can't carry raw.
- HTTP status codes group by their first digit (1xx–5xx); the user-agent header tells a server who's asking.
- `robots.txt` states paths a crawler is asked to avoid, read via `urllib.robotparser`'s `can_fetch`; a polite crawler also waits between requests (`Crawl-delay`).
- `webbrowser.open` hands a page to the person's own browser; `requests` downloads programmatically — `raise_for_status` stops the program on a bad reply, `iter_content` saves large downloads in chunks.
- A weather API answers in JSON (`json.loads`); the example converts the API's Kelvin to Celsius/Fahrenheit and shows an endpoint with its parameters and a (never-hardcoded) API key.
- HTML is nested tags with attributes; Beautiful Soup's `select`/`get_text` pick elements by a CSS-like path — never parse HTML with a regular expression.
- Selenium's `find_element` raises on a missing element, `find_elements` returns an empty list; Playwright's locator/auto-wait model (`sync_playwright`, `new_page`, `goto`, `locator`) waits for the page itself rather than sleeping a fixed time.
- Capstone projects: a map-address CLI (6), the comic image + Prev link (8), opening the first search results in tabs (7), a link-verification practice program.

## 3. Slide/page-tab outline (slide order; 24/24 code examples checked)

| Slide | Content | Code example |
|---|---|---|
| 1–3 | Title, today's route, two questions this chapter answers | — |
| 4–5 | Part 1: Addresses and manners — everyday pictures | — |
| 6 | A URL is scheme/host/path/query/fragment | A URL cut into its parts |
| 7 | Percent codes and the query string | quote and parse_qs |
| 8 | HTTP status codes: first digit is the class | HTTP status codes and their classes |
| 9 | The user-agent header | The user-agent header |
| 10 | robots.txt: paths a crawler is asked to avoid | robots.txt rules with can_fetch |
| 11 | **Story: robots.txt courtesy file, 30 June 1994** | — |
| 12 | A polite crawler waits between pages | Crawl-delay and a polite pause |
| 13 | **Story: the first spider counted 130 sites, 1993** | — |
| 14–16 | Part 2: Opening and downloading — everyday pictures | — |
| 17 | webbrowser.open asks your browser to show a page | webbrowser.open with a recording stand-in |
| 18 | Project 6: a map address from the command line | showmap.py builds a map address |
| 19 | Fetching a page: reply has a type and a body | urlopen on a data address |
| 20 | **Story: Requests, conceived in frustration, 13 Feb 2011** | — |
| 21 | raise_for_status stops the program on a bad reply | A raise_for_status stand-in |
| 22 | iter_content: save a download in chunks | iter_content writes in chunks |
| 23–24 | Part 3: A weather API — everyday pictures | — |
| 25 | An API answers in JSON | json.loads reads an API reply |
| 26 | The API gives Kelvin; the program converts | Kelvin to Celsius and Fahrenheit |
| 27 | An endpoint, its parameters and a secret key | An endpoint with an API key |
| 28–30 | Part 4: Reading HTML — everyday pictures | — |
| 31 | HTML is nested tags with attributes | HTMLParser lists the tags and attributes |
| 32 | Pick elements by a path, read text/attributes | select, get_text and get with ElementTree |
| 33 | **Story: Beautiful Soup, 2004** | — |
| 34 | Do not read HTML with a regular expression | A regular expression against a parser |
| 35 | Practice program: link verification | Resolve, defragment and de-duplicate links |
| 36 | Project 8: comic image and Prev link | The comic image and the Prev link |
| 37 | Project 7: open first results in tabs | Open the first search results |
| 38–40 | Part 5: Driving a browser — everyday pictures | — |
| 41 | Why a download isn't enough: script-built pages | A page built by a script |
| 42 | **Story: Selenium began as a test runner, 2004** | — |
| 43 | Selenium: find_element fails, find_elements doesn't | find_element and find_elements |
| 44 | Playwright: start, new page, goto, locator | The shape of a Playwright program |
| 45 | **Story: Playwright reached Python, 30 Sept 2020** | — |
| 46 | Interacting with a page: wait for the element | Auto-waiting for an element |
| 47 | Which tool for which page? | — |
| 48 | What differs from the book today (research table: urllib.robotparser wildcards since 3.14.5; PurePath.as_uri deprecated; datetime.utcfromtimestamp deprecated; Selenium Manager auto-finds driver/browser since 4.51.0; error renamed NoSuchElementException; Playwright browsers installed as a second step) | — |
| 49–50 | Summary, practice questions | — |
| 51 | Resources | — |

## 4. Resources slide (15 links, all live)

Book: Automate the Boring Stuff 3e, ch13 (automatetheboringstuff.com/3e/chapter13.html) · RFC 9309, Robots Exclusion Protocol · Python docs: urllib.robotparser, urllib.parse, html.parser, webbrowser · MDN: CSS selectors, HTTP response status codes · Requests: Quickstart (requests.readthedocs.io) · OpenWeather: Geocoding API · Beautiful Soup docs (crummy.com) · Selenium: locator strategies (selenium.dev) · Playwright for Python: locators · Video: Web testing with Playwright, PyOhio 2022 (pyvideo.org).

## 5. Open items

1. **Legacy duplicate (decided this turn):** `03-materials/slides/Chapter11WebScraping_YA_v1_0_0.pptx` (old-edition numbering) duplicated this chapter's subject. Owner approved retiring it; file removed, recoverable from git history.
2. **No structural retrofit gap** — TK_Ret_Ch13_* was already Done in the closed slides lineage; not reopened here.
