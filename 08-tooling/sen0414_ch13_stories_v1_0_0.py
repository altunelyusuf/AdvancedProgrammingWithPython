"""SEN0414 chapter 13 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six
stories for Web Scraping, written fresh for this chapter from sources opened on 2026-10-12 (every link below answered
HTTP 200 to requests on that day):

* GrayWanderer1993 - Matthew Gray wrote the World Wide Web Wanderer at MIT in the spring of 1993, the first automated
  Web agent or spider by his own account, and charted the Web from 130 sites in June 1993 to 100,000 by January 1996.
* KosterRobots1994 - Martijn Koster's A Standard for Robot Exclusion records a consensus of 30 June 1994 on the robots
  mailing list; RFC 9309 published the method in September 2022 and Python's urllib.robotparser applies it from 3.14.5.
* RichardsonBeautifulSoup2004 - Leonard Richardson's Beautiful Soup, on his site crummy.com 'since 2004'.
* HugginsSelenium2004 - Jason Huggins built JavaScriptTestRunner, the start of Selenium, at ThoughtWorks in Chicago in
  2004 for an internal Time and Expenses application.
* ReitzRequests2011 - Kenneth Reitz's Requests: HISTORY.md records 0.0.1 on 2011-02-13 (Frustration, Conception) and
  0.2.0 on 2011-02-14 (Birth!), and PyPI's first upload is dated 2011-02-14.
* PlaywrightMicrosoft2020 - InfoQ reported Playwright on 30 January 2020; the Python preview was announced on 30
  September 2020 by Arjun Attam on the Microsoft for Python Developers blog.

Two items the research first planned were dropped because their sources could not be opened: Koster's original
February 1994 message on www-talk (the archive and the Wayback Machine were unreachable from this session) and the
account that Charles Stross provoked robots.txt (known only from Wikipedia's sentence, which cites a source that could not
be opened). One photograph: Kenneth Reitz at a talk in 2012, by Nils Pascal Illenseer, CC BY 3.0, fetched from Wikimedia
Commons on 2026-10-12 (03-materials/ch13/assets, mapped in ch13-page/stories_img_v1_0_0.json); the other five stories carry
none, because no free photograph of their subjects was found or Commons answered HTTP 429 (that file says which). Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "GrayWanderer1993",
        "title": "The first spider counted 130 web sites in June 1993",
        "when": "1993",
        "who": "Matthew Gray",
        "where": "Massachusetts Institute of Technology",
        "link": "https://www.mit.edu/~mkgray/net/background.html",
        "concepts": ["ComicCrawler", "PoliteDelay"],
        "story": ("Matthew Gray wrote the World Wide Web Wanderer at MIT in the spring of 1993 to traverse the Web "
                   "systematically and collect sites; he was at first motivated mainly to discover new sites, because the Web "
                   "was still a relatively small place. As the Web grew rapidly his purpose turned to charting its growth, and "
                   "his own report counts 130 Web sites in June 1993, 623 in December 1993, 2,738 in June 1994 and 23,500 in "
                   "June 1995, with 100,000 by January 1996, when the regular traversals ended. He describes the Wanderer as "
                   "the first automated Web agent, or spider. It did what the chapter's comic downloader does at toy scale: "
                   "fetch a page, find its links, follow them, and repeat."),
        "lesson": "A crawler is a program that follows links; the first one counted 130 sites",
        "source": ("Matthew Gray, 'Internet Growth and Statistics: Credits and Background', "
                    "www.mit.edu/~mkgray/net/background.html (spring 1993; traversals from June 1993 to January 1996; first "
                    "automated Web agent or spider); Matthew Gray, 'Measuring the Growth of the Web, June 1993 to June 1995', "
                    "stuff.mit.edu/people/mkgray/growth/ (the table of Web sites per month, copyright 1995)."),
    },
    {
        "id": "KosterRobots1994",
        "title": "A courtesy file for robots, agreed on 30 June 1994",
        "when": "1994-06-30",
        "who": "Martijn Koster and the robot authors of the robots mailing list",
        "where": "The robots mailing list at Nexor, and the Web",
        "link": "https://www.robotstxt.org/orig.html",
        "concepts": ["RobotsTxt", "PoliteCrawler"],
        "story": ("Martijn Koster wrote down A Standard for Robot Exclusion, a text that records a consensus reached on 30 "
                   "June 1994 on the robots mailing list at nexor.co.uk between the majority of robot authors. It answered "
                   "what the text itself reports: in 1993 and 1994 some robots had swamped servers with rapid-fire requests or "
                   "retrieved the same files repeatedly, and others had wandered into deep virtual trees and cgi scripts with "
                   "side effects such as voting. The remedy was one file at the URL /robots.txt, which a robot reads first. The "
                   "document says plainly that it is not an official standard, is not enforced by anybody, and that nothing "
                   "guarantees that every robot will use it. The method became RFC 9309 in September 2022, with Koster, Illyes, "
                   "Zeller and Sassman as authors, and Python's urllib.robotparser read its wildcard rules only from release "
                   "3.14.5 on 10 May 2026."),
        "lesson": "Robots.txt is a 1994 courtesy, not a lock: honour it",
        "source": ("'A Standard for Robot Exclusion', Martijn Koster, www.robotstxt.org/orig.html (consensus of 30 June 1994 "
                    "on the robots mailing list, robots-request@nexor.co.uk; not an official standard; not enforced by "
                    "anybody); RFC 9309, Robots Exclusion Protocol, Koster, Illyes, Zeller and Sassman, IETF, September 2022 "
                    "(a method originally defined by Martijn Koster in 1994; rules are not a form of access authorization); "
                    "Python 3.14 changelog, 3.14.5 final, released 2026-05-10, gh-138907, docs.python.org/3.14/whatsnew/changelog.html."),
    },
    {
        "id": "RichardsonBeautifulSoup2004",
        "title": "Beautiful Soup, for the awful pages somebody else wrote, since 2004",
        "when": "2004",
        "who": "Leonard Richardson",
        "where": "His site, crummy.com",
        "link": "https://www.crummy.com/software/BeautifulSoup/",
        "concepts": ["SoupObject", "RegexPitfall"],
        "story": ("Leonard Richardson's page for Beautiful Soup greets the reader with the line 'You didn't write that awful page. "
                   "You're just trying to get some data out of it', and says that since 2004 the library has been saving "
                   "programmers hours or days of work on quick-turnaround screen scraping projects. Wikipedia adds, marking the "
                   "point as needing a citation, that the name comes from the poem Beautiful Soup in Alice's Adventures in "
                   "Wonderland and plays on tag soup, the term for poorly structured HTML. Beautiful Soup 3 was the official "
                   "release line from May 2006 to March 2012, and the line the chapter installs as beautifulsoup4 is the fourth. "
                   "On 12 October 2026 the author's page named 4.14.3 of 30 November 2025 as the current release, while pip "
                   "installed 4.15.0 for this chapter: a library's own page can lag its releases."),
        "lesson": "Do not parse HTML with regular expressions; Richardson's 2004 library exists for that",
        "source": ("'Beautiful Soup', Leonard Richardson, www.crummy.com/software/BeautifulSoup/ (read 2026-10-12: 'Since 2004'; "
                    "current release 4.14.3, November 30, 2025); 'Beautiful Soup (HTML parser)', Wikipedia (original author "
                    "Leonard Richardson; 2004; name from the poem in Alice's Adventures in Wonderland, marked [citation needed]; "
                    "Beautiful Soup 3 official from May 2006 to March 2012); PyPI beautifulsoup4 4.15.0 installed 2026-10-12."),
    },
    {
        "id": "HugginsSelenium2004",
        "title": "Selenium began in 2004 as a test runner for a timesheet application",
        "when": "2004",
        "who": "Jason Huggins, with Paul Gross and Jie Tina Wang",
        "where": "ThoughtWorks, Chicago",
        "link": "https://www.selenium.dev/history/",
        "concepts": ["WebDriverStart", "DynamicPages"],
        "story": ("The Selenium project's own history says the story starts in 2004 at ThoughtWorks in Chicago, where Jason Huggins, "
                   "helped by Paul Gross and Jie Tina Wang, built the Core mode as JavaScriptTestRunner to test an internal Time "
                   "and Expenses application written in Python and Plone. Colleagues liked its immediate visual feedback, and "
                   "soon afterwards Paul Hammant saw the demo and began the talks about open sourcing it and about a driven mode "
                   "that could be used over the wire from a language of one's choice. Separately, Simon Stewart at ThoughtWorks "
                   "built WebDriver, which did not rely on JavaScript but had a client for each browser coded from scratch, and "
                   "the two projects were merged. The webdriver.Firefox() call of the chapter descends from that merge."),
        "lesson": "Selenium began in 2004 as a test tool for one internal timesheet application",
        "source": ("'Selenium History', selenium.dev/history/ (2004, ThoughtWorks in Chicago, Jason Huggins, JavaScriptTestRunner, "
                    "Paul Gross and Jie Tina Wang, Paul Hammant; Simon Stewart's WebDriver and the merge); Selenium WebDriver "
                    "documentation, selenium.dev/documentation/."),
    },
    {
        "id": "ReitzRequests2011",
        "title": "Requests was conceived out of frustration on 13 February 2011",
        "when": "2011-02-13",
        "who": "Kenneth Reitz",
        "where": "GitHub and the Python Package Index",
        "link": "https://raw.githubusercontent.com/psf/requests/main/HISTORY.md",
        "concepts": ["GetRequest", "RaiseForStatus"],
        "story": ("The release history of Requests, which its repository still carries, begins with two entries: version 0.0.1, "
                   "dated 13 February 2011, lists 'Frustration' and 'Conception', and version 0.2.0, dated the next day, lists "
                   "'Birth!'. The Python Package Index agrees on the birthday: its first upload of requests is dated 14 February "
                   "2011. The documentation says Requests was lovingly created by Kenneth Reitz, and its slogan, HTTP for Humans, "
                   "is the promise the chapter repeats when it says the module lets you download files without worrying about "
                   "network errors, connection routing and data compression. Version 2.34.2, installed for this chapter on 12 "
                   "October 2026, descends from that 0.2.0."),
        "lesson": "Requests: conceived in frustration on 13 February 2011, born the next day",
        "source": ("HISTORY.md of the psf/requests repository, raw.githubusercontent.com/psf/requests/main/HISTORY.md (0.0.1 "
                    "2011-02-13 Frustration, Conception; 0.2.0 2011-02-14 Birth!); PyPI requests, pypi.org/pypi/requests/json "
                    "(earliest upload 2011-02-14T08:49:42, version 0.2.0); 'Authors', Requests 2.34.2 documentation "
                    "(created by Kenneth Reitz)."),
    },
    {
        "id": "PlaywrightMicrosoft2020",
        "title": "Playwright reached Python in preview on 30 September 2020",
        "when": "2020-09-30",
        "who": "Arjun Attam and the Playwright team at Microsoft",
        "where": "Microsoft for Python Developers blog",
        "link": "https://devblogs.microsoft.com/python/announcing-playwright-for-python-reliable-end-to-end-testing-for-the-web/",
        "concepts": ["SyncPlaywright", "AutoWaiting"],
        "story": ("On 30 January 2020 InfoQ reported that Microsoft had announced Playwright as an alternative to Puppeteer, quoting "
                   "the team: the same team that originally built Puppeteer at Google, which had since moved on. On 30 September "
                   "2020 Arjun Attam, a program manager, announced Playwright for Python in preview on the Microsoft for Python "
                   "Developers blog, saying that the JavaScript version had been released earlier in the year. The post's first "
                   "claim is reliable, timeout-free automation: Playwright automatically waits for the UI to be ready, with an "
                   "event-driven design that listens to browser events such as DOM changes, network requests and page navigations. "
                   "That is the auto-waiting of the chapter, including the thirty seconds a mistyped selector costs."),
        "lesson": "Playwright waits for the page by itself; Python preview announced 30 September 2020",
        "source": ("'Announcing Playwright for Python: Reliable end-to-end testing for the web', Arjun Attam, Microsoft for Python "
                    "Developers Blog, September 30th, 2020, devblogs.microsoft.com/python/; 'Microsoft Announces Playwright "
                    "Alternative to Puppeteer', InfoQ, Jan 30, 2020, infoq.com/news/2020/01/playwright-browser-automation/."),
    },
]


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for x in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story"):
            if not str(x.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (x["id"], f))
        if not x.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % x["id"])
        if len(x["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % x["id"])
        if not (2 <= x["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % x["id"])
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("GrayWanderer1993", "1993"), ("KosterRobots1994", "1994"), ("RichardsonBeautifulSoup2004", "2004"),
                      ("HugginsSelenium2004", "2004"), ("ReitzRequests2011", "2011"), ("PlaywrightMicrosoft2020", "2020")):
        if year not in by[sid]["story"] or year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
