"""SEN0414 chapter 25 - the story companion to the chapter corpus (version 2.0.0, new file over the first version 1.0.0, which stays as it was).

Five real, dated, sourced stories, one live link each, checked by this file's own run_checks(). They carry the story text of the lecture deck 4.0.0 of chapter 25
(SEN0414_Ch25_Threads_3e_v4_0_0.pptx), so the page and the deck tell the same story; each story lists the page concepts it leads to (the Stories tab jumps to them).
LINK_STATUS is the HTTP status that each link answered to a plain GET on 2026-11-27 with the identifying agent "SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)";
`python3 sen0414_ch25_stories_v2_0_0.py links` asks again.
Pictures: see ch25-page/stories_img_v9_112_0.json and 03-materials/ch25/assets/story_images_v1_0_0.json (files, licences, credits).
Usage: import STORIES; run the file for the self-check, or with the argument links to ask every link again.
"""
__version__ = "2.0.0"

STORIES = [{'concepts': ['TheXkcdDownloader', 'FixedListingSkipsComics'],
  'id': 'Munroe2005',
  'lesson': 'A small script can fetch thousands of pages',
  'link': 'https://en.wikipedia.org/wiki/Xkcd',
  'source': "Wikipedia, 'Randall Munroe' and 'Xkcd', read 2026-11-27.",
  'story': 'Randall Munroe, born on 17 October 1984, is an American cartoonist, author and engineer. xkcd began in September 2005, when he scanned '
           'his doodles and put them on his personal website; in January 2006 the comic moved to a site of its own. The picture shows him in Berlin '
           "in 2016. The downloader of this part works like the book's project, but a local stand-in answers and xkcd.com is never contacted.",
  'title': 'Randall Munroe began xkcd in September 2005',
  'when': '2005',
  'where': 'His personal website, from January 2006 a site of its own',
  'who': 'Randall Munroe, an American cartoonist, author and engineer'},
 {'concepts': ['ForcedLostUpdate', 'LockFixesCounter'],
  'id': 'Therac1985',
  'lesson': 'Shared state without a lock gives wrong results',
  'link': 'https://en.wikipedia.org/wiki/Therac-25',
  'source': "Wikipedia, 'Therac-25', read 2026-11-27.",
  'story': 'The Therac-25 was a computer-controlled radiation therapy machine that Atomic Energy of Canada Limited produced in 1982. It was involved '
           'in at least six overdoses of radiation between 1985 and 1987, and Wikipedia names concurrent programming errors, also known as race '
           'conditions, among the causes. The picture is a newspaper photograph of the machine. The lost updates of this part are a small race of '
           'the same kind.',
  'title': 'The Therac-25 overdosed patients in 1985 to 1987',
  'when': '1985 to 1987',
  'where': 'Cancer centres in Georgia, Ontario, Washington and Texas',
  'who': 'Atomic Energy of Canada Limited, which produced the Therac-25 in 1982, and the patients of the clinics that used it'},
 {'concepts': ['SemaphoreLimits', 'QueueHandsOver'],
  'id': 'Semaphore1962',
  'lesson': 'A counter can limit how many threads work at once',
  'link': 'https://en.wikipedia.org/wiki/Semaphore_(programming)',
  'source': "Wikipedia, 'Semaphore (programming)', read 2026-11-27.",
  'story': 'Edsger W. Dijkstra, a Dutch computer scientist, invented the semaphore in 1962 or 1963. He and his team were then developing an '
           'operating system for the Electrologica X8, which became known as the THE multiprogramming system. The picture shows him. The Semaphore '
           'of the example is the same counter: it lets two of six threads into a block.',
  'title': 'Dijkstra invented the semaphore for the THE system',
  'when': '1962 or 1963',
  'where': 'The team developing the THE multiprogramming system for the Electrologica X8',
  'who': 'Edsger W. Dijkstra, a Dutch computer scientist, and his team'},
 {'concepts': ['RaceInTheRecord', 'ExceptionAtResult'],
  'id': 'Blackout2003',
  'lesson': 'A race that never shows can still be there',
  'link': 'https://en.wikipedia.org/wiki/Northeast_blackout_of_2003',
  'source': "Wikipedia, 'Northeast blackout of 2003', read 2026-11-27.",
  'story': 'The blackout of 14 August 2003 affected 55 million people in the northeastern United States and Ontario. A software bug known as a race '
           "condition in General Electric Energy's XA/21 energy management system stalled the alarm system of FirstEnergy's control room for over an "
           'hour. The picture is a map of the area. A race that needs a rare timing hides in tests; part 5 shows one that appeared only on the '
           'free-threaded build.',
  'title': 'A race condition stalled the alarms in 2003',
  'when': '14 August 2003',
  'where': 'The northeastern United States and Ontario, Canada',
  'who': "FirstEnergy's control room operators, using General Electric Energy's XA/21 energy management system"},
 {'concepts': ['FreeBuildScalesWithCores', 'GilBuildGivesNoSpeedup'],
  'id': 'DualCore2005',
  'lesson': 'More cores help Python only without the lock',
  'link': 'https://en.wikipedia.org/wiki/Athlon_64_X2',
  'source': "Wikipedia, 'Athlon 64 X2', read 2026-11-27.",
  'story': 'The Athlon 64 X2 was the first native dual-core desktop processor that AMD designed. Its first models were released in May 2005, the '
           'same month as the Pentium D, the first dual-core processor of Intel. The picture shows an X2 with its heat spreader removed. Only a '
           'Python build without the lock can use both cores for Python code.',
  'title': 'Dual-core desktop processors came in May 2005',
  'when': 'May 2005',
  'where': 'Desktop computers worldwide',
  'who': 'AMD, with the Athlon 64 X2, and Intel, with the Pentium D'}]

LINK_STATUS = {'Munroe2005': 200, 'Therac1985': 200, 'Semaphore1962': 200, 'Blackout2003': 200, 'DualCore2005': 200}

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
        if LINK_STATUS.get(x["id"]) != 200:
            bad.append("%s: link status %r, not 200" % (x["id"], LINK_STATUS.get(x["id"])))
    for x in STORIES:
        if x["when"] not in x["story"] and x["when"] not in x["title"]:
            bad.append("%s: year %s not in story or title" % (x["id"], x["when"]))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out[x["id"]] = r.status
        except urllib.error.HTTPError as e:
            out[x["id"]] = e.code
        except Exception as e:
            out[x["id"]] = type(e).__name__
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "links":
        print(ask_links())
    else:
        b = run_checks()
        print(len(STORIES), "stories; self-check failures:", len(b))
        for x in b:
            print("  ", x)
