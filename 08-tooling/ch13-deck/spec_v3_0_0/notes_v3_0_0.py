"""Chapter 13 deck speaker notes, version 3.0.0: READER notes (handover of 2026-11-19, practice 3). The slides are handed to students together with their notes, so each note explains the slide's short wording in
fuller sentences, adds detail that the slide does not carry, and connects the slide to related slides and chapters. A note gives no direction to a presenter, has no think-of statement, no prompt marker, no
lambda and no everyday picture. The facts are those of the chapter's examples, of their runs and of the chapter research of deck 2.0.0. RESULT_SAYS: for each code slide, the first result balloon (what the run showed).
Slide numbers: 1 title, 2 route, 3 questions, 4 part 1, 5 A1, 6 url_anatomy, 7 query_quote, 8 status_codes, 9 user_agent, 10 robots_rules, 11 koster story, 12 crawl_delay, 13 gray story, 14 part 2, 15 A2, 16 A3,
17 webbrowser_open, 18 showmap, 19 fetch_data, 20 reitz story, 21 raise_status, 22 chunks, 23 part 3, 24 A4, 25 json_loads, 26 kelvin, 27 api_url, 28 part 4, 29 A5, 30 A6, 31 html_elements, 32 css_select,
33 richardson story, 34 regex_pitfall, 35 links_verify, 36 xkcd_chain, 37 search_results, 38 part 5, 39 A7, 40 A8, 41 dynamic_page, 42 huggins story, 43 selenium_shape, 44 playwright_shape,
45 playwright story, 46 auto_wait, 47 tools, 48 current, 49 summary, 50 practice, 51 resources."""
__version__ = "3.0.0"

NOTES = {
    "title": "This chapter of the book, Web Scraping, explains how a program gets a page from the Web and reads it: the address, the reply, the service that answers in data, the HTML of a page, and the browser that "
             "a program may have to drive. The deck has twenty-four code examples that run on the chapter page, six true stories about the tools, and a table where a comparison helps. Slide 2 lays out the "
             "five parts. Chapter 12 comes before it with command-line programs, and chapter 14 follows with spreadsheets.",
    "route": "The table is the map of the chapter. Each row is one of the five parts, with the slides it covers and what you will run in it. The last row covers the changes against the book, the summary, the practice "
             "questions and the links. The same twenty-four examples are listed in the Slide code tab of the chapter page, in this order, so a slide and its tab can be opened side by side. Part 1 starts on slide 4, "
             "and each later part begins with a divider slide that names its four ideas.",
    "questions": "Two questions run through the chapter, and the deck answers them near the end. The first asks which tool reaches which kind of page and what decides the choice; the answer is the table of tools on "
                 "slide 47. The second asks where the book's printed outputs and programs differ from current Python and from today's web; slide 48 lists those changes from the chapter research. Keeping both "
                 "questions in mind makes each later slide easier to place.",
    "divider1": "Part 1 is about addresses and manners. A URL is cut into named parts, a status code tells in its first digit what kind of reply came back, the user agent is the name a program gives to the server, and "
                "robots.txt lists the paths that a crawler is asked not to visit. The four cards are the ideas of the part. Slides 5 to 13 cover them, and part 2 later puts these manners into a download.",
    "divider2": "Part 2 is about opening and downloading. The webbrowser module shows a page to a person and reads nothing; requests fetches a page or a file into the program; raise_for_status stops the program on a "
                "failed reply; and iter_content saves a big download in chunks. The four cards are the ideas of the part. Slides 15 to 22 cover them, and part 1 earlier explains the status codes that raise_for_status checks.",
    "divider3": "Part 3 is about a weather API. A service is called by address and answers in JSON; the program reads that text with json.loads, converts the temperature from Kelvin, and keeps the API key out of "
                "its logs. The four cards are the ideas of the part. Slides 24 to 27 cover them, and part 1 earlier explains the address parts that the endpoint and its parameters use.",
    "divider4": "Part 4 is about reading HTML. A page is a tree of nested elements; select finds elements by a selector path; get_text and get read the text or one attribute; and a regular expression misses links "
                "that a parser finds. The four cards are the ideas of the part. Slides 29 to 37 cover them, and part 5 later turns to pages that a script builds, which a parser alone cannot read.",
    "divider5": "Part 5 is about driving a browser. Some pages are written by a script after the download, so only a real browser can read them. Selenium drives one through a separate driver, Playwright drives one and "
                "waits by itself, and headless mode runs it without a window. The four cards are the ideas of the part. Slides 39 to 47 cover them, and part 4 earlier shows how static HTML is read.",
    "A1": "An address names a page, a reply carries a status code, and a polite program names itself. The rows give a plain meaning to each idea. HTTP is the protocol of the Web and HTTPS adds encryption. A URL is "
          "the full address of a page, an endpoint is one address of a service, and the user agent is the header in which a program names itself. Slides 6 to 9 show each of them in code, and slide 10 "
          "adds the file that a site publishes for crawlers.",
    "A2": "The webbrowser module shows a page to a person and reads nothing back. Its open call asks the default browser to show an address and returns True when a browser started. Project 6 of the book uses it: "
          "the words typed on the command line become a map address, and the browser opens it. Slides 17 and 18 show both in code. Compare it with slide 16, where requests brings the page into the program.",
    "A3": "The requests library fetches a page or a file into the program and reports how the request went. It is a third-party package, installed with pip, and its slogan is HTTP for Humans. The call get sends a "
          "request to one address and returns a response; raise_for_status turns a bad status code into an error; and iter_content hands out a big body in chunks. Slides 19 to 22 show these ideas with "
          "standard-library stand-ins, and slide 20 tells how Requests began.",
    "A4": "An API is called by address and answers in data, not in a page. The weather service of the book answers in JSON, which json.loads turns into dictionaries and lists. The API key is a secret code that "
          "identifies your account, so it stays out of logs and repositories. Slides 25 to 27 show the reply, the conversion from Kelvin and the address with its key. Chapter 14 later reads data from a "
          "different source, spreadsheets.",
    "A5": "A page is a tree of nested elements, and a parser reads the page text into that tree. Each element has a tag, attributes and perhaps text. Beautiful Soup is the parser of the book, installed as "
          "beautifulsoup4; a CSS selector such as p.s > a picks elements in the tree; and the developer tools of a browser show the elements and can copy a selector. Slides 31 and 32 show the same "
          "ideas with parsers of the standard library.",
    "A6": "Three calls pick things out of a parsed page. The call select returns the list of elements that match a selector, and the list is empty when none match; get_text returns the text inside an element; "
          "and get returns one attribute, such as href. Projects 7 and 8 of the book use them: one opens the first search results in browser tabs, the other follows the Prev link of a comic. See slides 36 and 37.",
    "A7": "Selenium starts a real browser through a driver and gives it commands, so a program can read a page that a script builds. The call webdriver.Firefox starts the browser; find_element returns the first "
          "match and raises an error when there is none; find_elements returns a list, which may be empty. Headless mode runs the browser without a window. Slide 43 shows the difference between the two find "
          "calls, and slide 42 tells how Selenium began.",
    "A8": "Playwright drives a browser and waits by itself until an element is ready. It has its own browsers, which a second step, playwright install, puts on the machine. The context manager sync_playwright "
          "starts the tool, new_page opens a tab, goto loads an address and locator names the element to work with. Slide 44 shows these steps and slide 46 the waiting. Compare it with Selenium on slide 39.",
    "compare_tools": "The table answers the first question of the chapter. If a person should see the page, webbrowser opens it. If the address and its content are known, requests fetches text or a file. If a service "
                     "offers an API, requests and json give a structured answer that a key identifies. If the page is static HTML, a parser reads it. Only a page that a script builds, or one behind a login, needs "
                     "Selenium or Playwright. Slides 17 to 46 show each row in code.",
    "url_anatomy": "A URL is not one string but five named parts. The function urlsplit cuts the address into scheme, host, path, query and fragment, and the program prints each with its name. The scheme says how to talk, "
                   "the host says to whom, the path says which resource, and the query holds the questions. The fragment stays in the browser and is never sent to the server. Slide 7 turns to the query, and "
                   "slide 27 builds such an address for a weather service.",
    "query_quote": "An address may not hold a space or a comma, so they are written as percent codes: a space becomes %20 and a comma %2C. The function quote does this on the way out. On the way in, parse_qs reads "
                   "a query string back into a dictionary of lists, and the plus sign and %2C become a space and a comma again. Browsers do the same for their address bar. Slide 18 uses quote to build a map "
                   "address, and slide 6 names the query part.",
    "status_codes": "Every reply starts with a three-digit status code, and its first digit is the class. Two means success, three means redirection, four means that the request was at fault, and five means that "
                    "the server failed. The module http names each code, and integer division by 100 gives the class. The code 429 means too many requests, which a polite crawler meets when it asks too fast. "
                    "Slide 21 turns a bad code into an error, and slide 12 shows how to slow down.",
    "user_agent": "Python's own downloader announces itself as Python-urllib, and a server can tell a script from a browser by this header and may refuse the script. A polite program sets its own name, "
                  "ideally with a contact address, so that a site owner knows whom to ask. The first box reads the default header; the second builds a request with a header of its own. Later in "
                  "part 1, slide 10 shows the file in which a site states what it asks of a crawler.",
    "robots_rules": "A robots.txt file lists the paths that crawlers are asked not to fetch. The class RobotFileParser reads its lines, and can_fetch answers True or False for a path. It is a request and not a lock: "
                    "nobody enforces it, so a polite program honours it. Here two path prefixes are disallowed, so the project path is allowed and the other two are not. Slide 11 tells how the file began, "
                    "and slide 12 adds the pace a site may ask for.",
    "crawl_delay": "A site can state its own pace in its robots file. Crawl-delay is a pause in seconds, and Request-rate is a number of pages per number of seconds. The parser returns both numbers. The loop "
                   "uses a fake clock, so the schedule shows without really waiting: one fetch, then a pause of two seconds. The book's comic downloader sleeps for one second for the same reason. Slide 10 "
                   "shows the rules about paths, and slide 36 is the program that needs this pause.",
    "webbrowser_open": "The real call webbrowser.open starts the default browser and returns True when a browser was started. It cannot read the page; it only points the browser at it. On this page a small function "
                       "named record replaces the real call, so that no window opens and the address is kept in a list. Compare slide 19, where a program fetches a page into itself. Project 6 on slide 18 and "
                       "project 7 on slide 37 both use this call.",
    "showmap": "Project 6 of the book turns the words typed after the script name into a map address. The list argv holds those words, with the script's own name first. The program joins the words after the name "
               "into one address, percent-encodes it with quote and adds it to the search address; webbrowser.open would then show the map. Here the list is typed in by hand so that nothing depends on a "
               "keyboard. Slide 7 explains quote, and chapter 12 explains sys.argv.",
    "fetch_data": "The call requests.get downloads a page. Python's own urlopen does the same job, and an address that starts with data: carries its text inside the address, so no network is needed. The reply has "
                  "a content type and a body of bytes; decode turns the bytes into text, as the text property of a requests response does. The body here is sixteen bytes. Slide 21 checks such a reply, "
                  "and slide 22 saves a large one in chunks.",
    "raise_status": "The method raise_for_status of requests raises an error when the status code is 400 or more. The stand-in does the same: it names the problem with the phrase of the code. A good reply "
                    "passes quietly, and a bad one stops the program before it saves an error page as if it were the file. Call it after every download. Slide 8 explains the classes of status codes, and "
                    "slide 22 shows the step that follows a good reply.",
    "chunks": "A downloaded file is bytes, and a big file should not have to fit in memory. The function iter_content hands out the body in pieces of a chosen size, and the loop writes each piece in binary mode. "
              "The call write returns the number of bytes saved: sixteen, sixteen and ten for a body of forty-two bytes. The temporary folder disappears afterwards. Slide 21 comes before this step in a real "
              "download, and chapter 11 explains files and folders.",
    "json_loads": "A web API sends its answer as JSON text. The function json.loads turns it into dictionaries, lists, numbers and strings, and the program then reaches inside one step at a time with keys and list "
                  "positions. The top level here is a dictionary with three keys: name, main and weather. The weather entry is a list, so its first item is read by position. Slide 26 converts the temperature "
                  "from this reply, and chapter 14 later reads other structured data.",
    "kelvin": "The weather service reports temperatures in Kelvin. Subtracting 273.15 gives Celsius, and scaling by nine fifths and adding 32 gives Fahrenheit. The format %.1f keeps one decimal, so the "
              "program prints 12.3 degrees Celsius and 54.1 degrees Fahrenheit, as the book does. The value 285.44 is the temperature of the reply on slide 25. Convert another value on slide 50, in the "
              "practice questions.",
    "api_url": "An endpoint is the address of one service, and the parameters say what is wanted: here a place by its latitude and longitude, and the appid, which is the API key that names your account. The function "
               "urlencode joins the pairs with ampersands. A key is a password, so a log shows the address only with the key hidden, as the second line does. Slide 6 names the parts of such an address, and "
               "slide 7 the encoding.",
    "html_elements": "HTML is nested tags with attributes. The class HTMLParser calls the method handle_starttag for every opening tag, and the attributes arrive as pairs of a name and a value. The p tag holds an id, "
                     "the b tag has none, and the a tag holds a class and an address. Feeding the parser the page text walks through the tree from the outside in. Slide 32 reads the same page by a path, and "
                     "slide 34 uses the same parser to find links.",
    "css_select": "Beautiful Soup is not part of Python, so ElementTree reads a well-formed page and offers the same three moves: select, get_text and get. The path .//*[@id='a'] plays the selector #a, and itertext "
                  "gathers the text of an element and of its children, as get_text does. A path with a class and a child plays p.s > a, and get reads one attribute. A path that matches nothing gives an empty "
                  "list. Slide 30 names the three calls.",
    "regex_pitfall": "The pattern expects href right after the tag name, so it silently misses a link that has a class first. The parser reads attributes by name in whatever order they come, so both links are found. "
                     "The result is one link against two. Use a parser for HTML and keep regular expressions for plain text. Beautiful Soup is a friendlier parser of the same kind; see slide 33 for the author's own words "
                     "on pages he did not write.",
    "links_verify": "This practice program of the book sorts out the links of a page. The function urljoin makes each link absolute, urldefrag drops the fragment, a link to another site is skipped, and a page that "
                    "was already seen is not added again. Of four links, two remain: the introduction page, which was linked twice, and the about page. Slide 6 explains the fragment, and the first story "
                    "of this chapter, slide 13, tells how the first spider worked the same way.",
    "xkcd_chain": "Project 8 of the book relies on the structure of the comic site: the image sits inside the element with the id comic, and the Prev link has rel set to prev. Two paths find the image address and "
                  "the address of the previous comic. The image address begins with two slashes, so urljoin borrows the scheme of the page. The real loop downloads the image and then follows Prev. "
                  "Slide 12 explains why such a loop should pause between pages.",
    "search_results": "Project 7 of the book opens the first search results in browser tabs. A recording stand-in replaces webbrowser.open again, so no tab opens. The small page holds three links; the program selects "
                      "all of them, keeps the first two and opens each address. As of 12 October 2026 the real PyPI search page answers with a challenge page, so the book's program finds no links; slide 48 "
                      "lists this change. See slide 17 for the open call.",
    "dynamic_page": "Some pages write their own text with a script after the download. The source then holds only an empty element and the script, and a program that downloads the page and parses it sees nothing to "
                    "read. A browser runs the script and gets the text; the toy here does that step by hand. Selenium and Playwright drive a real browser for this reason, headless when no window is needed. "
                    "Slides 43 to 46 show their shapes, and slide 31 shows static HTML.",
    "selenium_shape": "This stand-in shows how the two find calls of Selenium behave. The function find_elements returns a list, which may be empty, and find_element returns the first match and fails when there "
                      "is none. Two paragraphs are found and the first says one; a search for h1 gives an empty list, but find_element fails. Selenium raises NoSuchElementException, where this stand-in "
                      "raises IndexError. Compare slide 32, where an empty list is also a valid answer.",
    "playwright_shape": "The steps of a Playwright program are the same four as in the chapter: start the tool, open a new page, go to an address and name an element with a locator. A stand-in page prints the "
                        "address it visits and returns the name of the element. The context manager of the real sync_playwright starts the tool and stops it at the end of the with block, and a real program "
                        "also launches a browser first. Slide 46 shows the waiting that the locator adds.",
    "auto_wait": "A page can build an element late. Each entry of the list is one look at the page: nothing, nothing, then the text. Playwright keeps looking until the element is ready or time runs out, and "
                 "Selenium looks once. With five looks the text is found on the third; with two looks the program gives up, as Playwright does after thirty seconds. Slide 41 shows why a late element "
                 "exists, and slide 43 shows the single look of Selenium.",
    "current": "Python and the tools move on, so the book's printed outputs and programs differ from today's in places. The table lists each change with its version or date and what it means for the chapter; "
               "the last column names the slide whose example it touches. The robot parser reads wildcard rules since Python 3.14.5, Selenium finds its driver by itself, and Playwright needs a second install step. "
               "Run what the book printed, then check what changed; slide 3 asked this question.",
    "summary": "Five ideas are worth keeping. An address has parts and a reply has a status code. A polite program reads robots.txt, waits between pages and names itself. Every reply is checked, and big files are "
               "saved in chunks. An API answers in JSON, and its key is a password. HTML is read with a parser, and a real browser is used only when a script builds the page. The chart counts the code examples "
               "of each part; see the route on slide 2.",
    "practice": "Four short drills close the chapter. The first cuts an address into its parts, the second asks what a robots rule allows, the third converts a temperature, and the fourth lists the pages one link "
                "away. Predict each answer first, then run what you can on the chapter page; each answer fits in a few lines. The examples on slides 6, 10, 26 and 35 hold the code that each drill "
                "needs.",
    "resources": "Start with the chapter of the book, then the Python documentation of the modules used, the documents of the four tools, and the protocol texts. The stories link to first-hand sources: "
                 "the original robots standard, the author's own pages and the release history of Requests. Chapter 12 and chapter 14 of the same book come before and after this one. Choose one link "
                 "and read it before the next class.",
}

STORY_NOTES = {
    "koster": "Martijn Koster wrote down the consensus of 30 June 1994 after some robots had swamped servers. The file is a courtesy and not a lock: the text itself says that nobody enforces it, and "
              "it became RFC 9309 only in September 2022. A reader has a choice to make when a site asks not to be crawled, and a polite program honours the request. Slide 10 shows the rules in code, "
              "and slide 12 shows the pause that sites may ask for.",
    "gray": "Matthew Gray built the first spider in 1993 to find new sites and then to count the Web: 130 sites in June 1993, 2,738 in June 1994 and 100,000 by January 1996. His method is the one of the "
            "chapter's link program on slide 35: fetch a page, find its links, follow them and repeat. His own reports are still online at MIT, which the link below opens. Slide 11 tells why such "
            "programs needed manners.",
    "reitz": "Requests was conceived on 13 February 2011 and born the next day, and the version history still says Frustration, Conception and Birth. What frustrated its author is what the library hides: "
             "network errors, connection routing and data compression. One call, get, and a check with raise_for_status are enough for the chapter's downloads. Slide 21 shows that check, and "
             "slide 16 gives the plain meaning of the library.",
    "richardson": "Leonard Richardson has kept Beautiful Soup since 2004, and his page promises that the reader did not write the awful page and only wants some data out of it. That is why the chapter reads HTML "
                  "with a parser and not with a regular expression, as slide 34 shows. The name echoes a poem in Alice in Wonderland and the term tag soup for badly built HTML. Slide 32 shows the three "
                  "moves of the library.",
    "huggins": "Selenium began in 2004 at ThoughtWorks as a test tool for an internal timesheet application written in Python and Plone. Later it merged with the WebDriver of Simon Stewart, so that a program "
               "drives a browser from outside, which is why a driver is needed. The slides on Selenium follow this story: slide 43 shows the find calls and slide 39 the plain meanings. Compare the later "
               "tool Playwright on slide 45.",
    "playwright": "Arjun Attam announced Playwright for Python in preview on 30 September 2020, and its first promise is automatic waiting, which the last example imitates. It is event-driven, so it reacts to "
                  "changes of the page and not to a timer. Slide 46 shows the waiting, and slide 44 shows the steps of a program. Compare the older tool Selenium on slide 42, whose find calls look once.",
}

RESULT_SAYS = {
    "url_anatomy": "The address is cut into five named parts.",
    "query_quote": "The text is quoted, and the query reads back as a dictionary.",
    "status_codes": "Each code has a phrase and a class from two to five.",
    "user_agent": "The default name is Python-urllib; the program's own name is MyBot.",
    "robots_rules": "The project path is allowed; the other two are not.",
    "crawl_delay": "A pause of two seconds, a rate of three pages in twenty.",
    "webbrowser_open": "The call returned True and the address was recorded.",
    "showmap": "The words became one quoted map address.",
    "fetch_data": "A plain-text reply of sixteen bytes decodes to a title.",
    "raise_status": "The code 200 passes; 404 and 500 stop the program.",
    "chunks": "The body was written in three chunks of 16, 16 and 10 bytes.",
    "json_loads": "The reply reads as a dictionary: Boston and Clouds.",
    "kelvin": "285.44 Kelvin is 12.3 Celsius and 54.1 Fahrenheit.",
    "api_url": "The address holds the key; the logged copy hides it.",
    "html_elements": "Three opening tags, each with its own attributes.",
    "css_select": "One match by id, one link by path, and an empty list for none.",
    "regex_pitfall": "The pattern found one link; the parser found both.",
    "links_verify": "Two pages remain: the guide page once, and the about page.",
    "xkcd_chain": "The image and the previous page became full addresses.",
    "search_results": "Three links were found and the first two were opened.",
    "dynamic_page": "The source holds no text; after the script it does.",
    "selenium_shape": "Two paragraphs were found; an empty list; then a failure.",
    "playwright_shape": "The page visited the address and returned the element h1.",
    "auto_wait": "Five looks found the text on the third; two looks timed out.",
}
