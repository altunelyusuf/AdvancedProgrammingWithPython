"""SEN0414 chapter 5 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this
file's self-check. Three stories for Debugging:

* FirstBug - the moth is real, taped into a logbook you can still see; the word 'debugging'
  grew around it.
* PrintDebugging - Kernighan's 1979 sentence gives the humble print statement its pedigree -
  and the chapter upgrades it to logging without shame.
* LoggingPep - Python's logging module has a birthday and an author; the chapter's level
  demos run the machinery that PEP proposed.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "FirstBug",
        "title": "The bug you can visit in a museum",
        "when": "1947-09-09",
        "who": "Grace Hopper's Harvard Mark II team",
        "where": "the machine's logbook - now at the Smithsonian",
        "link": "https://en.wikipedia.org/wiki/Software_bug",
        "concepts": ["BugModel"],
        "story": ("On 9 September 1947 the Harvard Mark II stopped, and the operators traced the "
                  "fault to a moth caught in relay 70 of panel F. They taped the insect into the "
                  "logbook with the note 'First actual case of bug being found' - the joke being "
                  "that engineers already said 'bug' for faults. The page, moth and all, survives "
                  "at the Smithsonian, and the photograph on this slide is the Navy's own. "
                  "Debugging has meant removing the moth ever since."),
        "lesson": "Every bug since has been a metaphor; this one had wings",
        "source": ("The Mark II logbook page of 1947-09-09, 'First actual case of bug being "
                   "found', held by the Smithsonian's National Museum of American History; "
                   "photograph courtesy of the Naval Surface Warfare Center, Dahlgren (public "
                   "domain). Note: a common file title misdates it 1945; the log page itself is "
                   "dated September 9, 1947."),
    },
    {
        "id": "PrintDebugging",
        "title": "The most effective debugging tool",
        "when": "1979",
        "who": "Brian Kernighan, Bell Labs",
        "where": "'Unix for Beginners', the Bell Labs memorandum",
        "link": "https://en.wikipedia.org/wiki/Brian_Kernighan",
        "concepts": ["Logging", "Debugger"],
        "story": ("In a 1979 Bell Labs paper Kernighan wrote the sentence every debugger vendor "
                  "has to argue with: 'The most effective debugging tool is still careful "
                  "thought, coupled with judiciously placed print statements.' This chapter "
                  "agrees, then upgrades the print statement into logging. Same idea - but with "
                  "levels, timestamps, files, and an off switch that does not require deleting "
                  "your evidence."),
        "lesson": "Logging is the print statement that grew up",
        "source": ("Brian W. Kernighan, 'Unix for Beginners' (Bell Laboratories, 1979), the "
                   "'careful thought... judiciously placed print statements' sentence; biography "
                   "and bibliography at en.wikipedia.org/wiki/Brian_Kernighan. Photo: Ben Lowe, "
                   "CC BY 2.0, at Bell Labs."),
    },
    {
        "id": "LoggingPep",
        "title": "A logging system with a birth certificate",
        "when": "PEP 282, 2002; stdlib since Python 2.3",
        "who": "Vinay Sajip and Trent Mick, through the PEP process",
        "where": "peps.python.org - and the logging module these slides run",
        "link": "https://peps.python.org/pep-0282/",
        "concepts": ["Logging"],
        "story": ("Python's logging module did not drift into the language; it was proposed as "
                  "PEP 282 in 2002 by Vinay Sajip and Trent Mick, modelled on log4j's levels, and "
                  "entered the standard library in Python 2.3. DEBUG, INFO, WARNING, ERROR, "
                  "CRITICAL - the five-step ladder on these slides is that PEP's design, and the "
                  "chapter's demos run it: to the console, to a file, forced, and disabled."),
        "lesson": "The five log levels are a 2002 design decision you inherit",
        "source": ("PEP 282, 'A Logging System', authors Vinay Sajip and Trent Mick (2002), "
                   "implemented as the standard library's logging module from Python 2.3 "
                   "(peps.python.org/pep-0282)."),
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
    if "1947-09-09" not in STORIES[0]["when"]:
        bad.append("FirstBug: date drifted")
    if "1979" not in STORIES[1]["source"]:
        bad.append("PrintDebugging: date missing from source")
    if "PEP 282" not in STORIES[2]["source"]:
        bad.append("LoggingPep: PEP missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
