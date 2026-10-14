"""SEN0414 chapter 25 (the Threads subject) - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Four stories for threads, written fresh for this chapter from
Wikipedia pages and PEP 703 opened on 2026-10-14 (the HTTP status each link answered to a plain GET on that day is in LINK_STATUS, and
`python3 sen0414_ch25_stories_v1_0_0.py links` asks again):

* Therac1985 - the Therac-25 radiation therapy machine of Atomic Energy of Canada Limited, built in 1982, was involved in at least six overdoses between 1985 and 1987; Wikipedia names concurrent programming errors, also known as race conditions.
* Semaphore1962 - Edsger Dijkstra invented the semaphore in 1962 or 1963 while his team developed the THE multiprogramming system for the Electrologica X8.
* Blackout2003 - on 14 August 2003 a race condition in a General Electric Energy XA/21 energy management system stalled the alarm system of FirstEnergy's control room for over an hour; 55 million people were affected.
* Gil2023 - Sam Gross wrote PEP 703 (created 9 January 2023) to make the global interpreter lock optional, and the Steering Council accepted it on 24 October 2023.

Photograph: none is used; the study fetched no image and claims nothing about image licences.
Every sentence that says "In this study" was run on 2026-10-14 under Python 3.14.6 (and the free-threaded 3.14.6) on Ubuntu 24.04 with 2 vCPUs; the figures come from ch25-page/timing_record_v1_0_0.json and the leaves named in each source.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "Therac1985",
        "title": "A radiation machine gave patients doses far above normal in 1985 to 1987",
        "when": "1985 to 1987",
        "who": "Atomic Energy of Canada Limited, which produced the Therac-25 in 1982, and the patients of the clinics that used it",
        "where": "Cancer centres in Georgia, Ontario, Washington and Texas, among them Kennestone Regional Oncology Center and the East Texas Cancer Center",
        "link": "https://en.wikipedia.org/wiki/Therac-25",
        "concepts": ["ForcedLostUpdate", "LockFixesCounter"],
        "story": ("Wikipedia's article on the Therac-25 says the computer-controlled radiation therapy machine was produced by Atomic Energy of Canada Limited in 1982 and was involved in at least six overdoses of radiation between 1985 and 1987. "
                  "It says that concurrent programming errors, also known as race conditions, sometimes gave patients doses up to 250 times higher than normal, resulting in death or serious injury. "
                  "A race is a result that depends on the order in which two flows of control reach a shared value. "
                  "In this study two threads that read a shared counter, waited 0.05 s and wrote back the value plus one left it at 1 instead of 2 in all 3 runs, and with a lock around the read and the write it ended at 2."),
        "lesson": "Shared state without a lock gives wrong results",
        "source": ("Wikipedia, 'Therac-25' (Atomic Energy of Canada Limited, 1982, at least six overdoses 1985 to 1987, race conditions), read 2026-10-14; this study's leaves ForcedLostUpdate and LockFixesCounter."),
    },
    {
        "id": "Semaphore1962",
        "title": "Dijkstra invented the semaphore for the THE system",
        "when": "1962 or 1963",
        "who": "Edsger Dijkstra, a Dutch computer scientist, and his team",
        "where": "The team developing the THE multiprogramming system for the Electrologica X8",
        "link": "https://en.wikipedia.org/wiki/Semaphore_(programming)",
        "concepts": ["SemaphoreLimits", "QueueHandsOver"],
        "story": ("Wikipedia's article on the semaphore says the concept was invented by the Dutch computer scientist Edsger Dijkstra in 1962 or 1963, when he and his team were developing an operating system for the Electrologica X8, which became known as the THE multiprogramming system. "
                  "A semaphore is a counter that lets a fixed number of flows of control pass at once. "
                  "In this study six threads that each held a Semaphore of 2 for 0.1 s were inside the guarded block at most 2 at a time, against 6 without it, and a queue.Queue handed 5 numbers in order from a producer thread to a consumer thread."),
        "lesson": "A counter can limit how many threads work at once",
        "source": ("Wikipedia, 'Semaphore (programming)' (Dijkstra, 1962 or 1963, THE multiprogramming system, Electrologica X8), read 2026-10-14; this study's leaves SemaphoreLimits and QueueHandsOver."),
    },
    {
        "id": "Blackout2003",
        "title": "A race condition stalled the alarms before the blackout of 2003",
        "when": "14 August 2003",
        "who": "FirstEnergy's control room operators, using General Electric Energy's XA/21 energy management system",
        "where": "The northeastern United States and Ontario, Canada",
        "link": "https://en.wikipedia.org/wiki/Northeast_blackout_of_2003",
        "concepts": ["RaceInTheRecord", "DeadlockWithTwoLocks"],
        "story": ("Wikipedia's article on the Northeast blackout of 2003 says the blackout began on 14 August 2003 and affected 55 million people. "
                  "It says a software bug known as a race condition existed in General Electric Energy's Unix-based XA/21 energy management system and, once triggered, stalled the alarm system of FirstEnergy's control room for over an hour. "
                  "A race that needs a rare timing is hard to see in tests. "
                  "In this study four threads that each ran counter += 1 one million times lost no update in 12 runs on the GIL builds, but lost between 2,500,522 and 2,913,206 of 4,000,000 updates in each of 3 runs on the free-threaded build."),
        "lesson": "A race that never shows can still be there",
        "source": ("Wikipedia, 'Northeast blackout of 2003' (14 August 2003, 55 million people, a race condition in the XA/21 system), read 2026-10-14; this study's leaf RaceInTheRecord and ch25-page/timing_record_v1_0_0.json."),
    },
    {
        "id": "Gil2023",
        "title": "Python decided in 2023 to make the global interpreter lock optional",
        "when": "9 January 2023 to 24 October 2023",
        "who": "Sam Gross, the author of PEP 703, and the Python Steering Council",
        "where": "The Python Enhancement Proposals process; the target was Python 3.13",
        "link": "https://peps.python.org/pep-0703/",
        "concepts": ["FreeThreadedBuildRuns", "FreeBuildScalesWithCores"],
        "story": ("PEP 703 was written by Sam Gross, created on 9 January 2023 for Python 3.13, and resolved on 24 October 2023. "
                  "The Steering Council accepted it with the proviso that the rollout be gradual and break as little as possible, and that the changes could be rolled back. "
                  "The global interpreter lock lets one thread at a time run Python code, and the PEP made it optional. "
                  "In this study the free-threaded 3.14.6 installed with uv reported the lock as off, and four CPU-bound tasks took 1.292 s serially and 0.522 s on 4 threads on 2 CPUs, while the standard build took 0.89 s serially and 1.003 s on 4 threads."),
        "lesson": "An optional lock lets threads use several cores",
        "source": ("PEP 703 (Sam Gross; created 9 January 2023; resolution 24 October 2023), read 2026-10-14; this study's leaves FreeThreadedBuildRuns and FreeBuildScalesWithCores."),
    },
]

LINK_STATUS = {"Therac1985": 200, "Semaphore1962": 200, "Blackout2003": 200, "Gil2023": 200}


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
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("Therac1985", "1985"), ("Semaphore1962", "1962"), ("Blackout2003", "2003"), ("Gil2023", "2023")):
        if year not in by[sid]["when"]:
            bad.append("%s: year %s not in when" % (sid, year))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "sen0414-study/1.0"})
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
