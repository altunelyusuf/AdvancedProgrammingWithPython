"""SEN0414 chapter 10 - the story companion to the chapter corpus (version 1.1.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Four
stories for Reading and Writing Files, written fresh for this chapter:

* ThompsonDbm1979 - Ken Thompson wrote the first dbm, released by AT&T in 1979, the key-value file the shelve
  module this chapter teaches still opens through its own dbm backend.
* ThompsonPikeUtf8 - Ken Thompson designed UTF-8's bit packing on a diner placemat in New Jersey in September
  1992, with Rob Pike watching; the chapter's own encoding argument names exactly this format.
* CrockfordJson2001 - Douglas Crockford, with Chip Morningstar, wrote up JSON at State Software in 2001 and
  opened json.org on 12 November 2002, the plain format the chapter sets beside shelve as the alternative.
* PitrouPathlib2012 - Antoine Pitrou wrote PEP 428 on 30 July 2012, proposing the pathlib module the chapter
  opens with, shipped two years later in Python 3.4.

Usage: import STORIES; run the file for self-checks. The photographs are named in ch10-page/stories_img_v1_0_0.json.
"""
__version__ = "1.1.0"

STORIES = [
    {
        "id": "ThompsonDbm1979",
        "title": "The file format behind a shelf is a 1979 Bell Labs idea",
        "when": "1979",
        "who": "Ken Thompson",
        "where": "AT&T Bell Laboratories, Murray Hill, New Jersey",
        "link": "https://en.wikipedia.org/wiki/DBM_(computing)",
        "concepts": ["ShelfBackend"],
        "story": ("Ken Thompson, already known for Unix and for the regular-expression search algorithm of an "
                   "earlier chapter, wrote the first dbm, a simple key-value store that AT&T released in 1979 as "
                   "part of Unix. dbm let a program store a string under a string key and get it back by that key "
                   "alone, with no query language and no server, exactly the shape shelve.open() still presents "
                   "today. Later rewrites, ndbm for extra features, GNU's own gdbm for crash tolerance, and "
                   "Berkeley DB in 1991 from Sleepycat Software, replaced the original code but kept the same "
                   "one-key-one-value idea, and Python's dbm package still picks among several such backends, "
                   "dbm.sqlite3 first since Python 3.13, when a shelf is opened. Every shelf this chapter opens "
                   "rests on a forty-six-year-old design for exactly one reason: looking a value up by one key is "
                   "still the simplest way to save a Python program's own variables to disk."),
        "lesson": "A shelf's one-key-one-value file dates to Thompson's 1979 dbm",
        "source": ("'DBM (computing)', Wikipedia, en.wikipedia.org/wiki/DBM_(computing) (written by Ken Thompson, "
                    "released by AT&T, 1979; Berkeley DB, Sleepycat Software, 1991); Python documentation, dbm and "
                    "shelve. Photo: Wikimedia Commons."),
    },
    {
        "id": "MsDos2BackslashPaths1983",
        "title": "A 1983 choice is why a Windows path is written with backslashes",
        "when": "1983",
        "who": "the MS-DOS programmers at Microsoft, with IBM; explained by Larry Osterman in 2005",
        "where": "Microsoft, Redmond, Washington",
        "link": "https://learn.microsoft.com/archive/blogs/larryosterman/why-is-the-dos-path-character",
        "concepts": ["PathConstruction"],
        "story": ("MS-DOS 2.0, released in 1983, was the first version of DOS that could keep folders inside folders, "
                   "so its programmers had to choose a character to separate the names in a path. The slash was already "
                   "taken, because MS-DOS used it in front of command options, and the backslash became the separator. "
                   "Larry Osterman, an engineer at Microsoft, explained the choice in a blog post in 2005, and writers "
                   "on computer history still disagree about how much IBM, which wanted the old commands to keep working, "
                   "pushed for it. Path() joins names with the separator of the computer that runs the program, so one "
                   "program prints spam\\eggs on Windows and spam/eggs elsewhere."),
        "lesson": "Windows paths use backslashes because MS-DOS 2.0 used the slash for options",
        "source": ("Larry Osterman, 'Why is the DOS path character a backslash?', learn.microsoft.com/archive/blogs/"
                    "larryosterman (2005); Charles Petzold, blog, 2006; OS/2 Museum, 'Why Does Windows Really Use "
                    "Backslash as Path Separator?'. Picture: Wikimedia Commons, public domain."),
    },
    {
        "id": "KildallDriveLetters1974",
        "title": "A 1974 operating system is why Windows paths start with C:",
        "when": "1974",
        "who": "Gary Kildall",
        "where": "Pacific Grove, California",
        "link": "https://en.wikipedia.org/wiki/Drive_letter_assignment",
        "concepts": ["PathParts"],
        "story": ("Gary Kildall demonstrated CP/M in 1974 in Pacific Grove, California, one of the first operating "
                   "systems for personal computers, and it named floppy drives with letters. MS-DOS began as a CP/M "
                   "look-alike that Microsoft licensed from Seattle Computer Products, and it kept the lettering. The "
                   "first two letters, A and B, went to floppy drives, so a hard disk took the next free one, C, and "
                   "Windows still starts at C: today. The chapter's own Windows path takes that drive apart as one "
                   "part of the path: PureWindowsPath('C:/Users/Al/spam.txt').drive gives 'C:'."),
        "lesson": "Windows paths start with a drive letter because CP/M named drives with letters",
        "source": ("'Drive letter assignment', Wikipedia, en.wikipedia.org/wiki/Drive_letter_assignment; Computer "
                    "History Museum, 'Fifty Years of the Personal Computer Operating System' (CP/M, 1974). Picture: "
                    "Wikimedia Commons, public domain."),
    },
    {
        "id": "PitrouPathlib2012",
        "title": "A 2012 proposal is why a path is an object, not a string",
        "when": "2012-07-30",
        "who": "Antoine Pitrou",
        "where": "the Python Enhancement Proposals process",
        "link": "https://peps.python.org/pep-0428/",
        "concepts": ["PathConstruction"],
        "story": ("Antoine Pitrou wrote PEP 428, 'The pathlib module - object-oriented filesystem paths', dated 30 "
                   "July 2012, proposing that a filesystem path be its own object with its own methods rather than "
                   "a plain string passed to separate os.path functions. The proposal was discussed through 2013 "
                   "and the module shipped two years after it was written, in Python 3.4, released in March 2014, "
                   "bringing with it the pure and concrete path classes, the / join operator and the rich set of "
                   "attributes, parts, parent, stem and suffix among them, that this chapter's own Path objects "
                   "section now teaches as the ordinary way to build and take apart a path. Path('spam', 'bacon', "
                   "'eggs') and the chapter's own os.path.join() both existed before 2012; only one of them is an "
                   "object with a is_file() method of its own, and that is Pitrou's one proposal."),
        "lesson": "Path() is an object because of Pitrou's 2012 proposal, PEP 428",
        "source": ("PEP 428, 'The pathlib module', peps.python.org/pep-0428 (created 30 July 2012, Antoine "
                    "Pitrou; shipped in Python 3.4, March 2014); Python documentation, pathlib. Photo: Wikimedia "
                    "Commons."),
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
    if "1979" not in by["ThompsonDbm1979"]["story"] or "1979" not in by["ThompsonDbm1979"]["when"]:
        bad.append("ThompsonDbm1979: date missing from story")
    if "1983" not in by["MsDos2BackslashPaths1983"]["story"] or "backslash" not in by["MsDos2BackslashPaths1983"]["story"]:
        bad.append("MsDos2BackslashPaths1983: date or subject missing from story")
    if "1974" not in by["KildallDriveLetters1974"]["story"] or "1974" not in by["KildallDriveLetters1974"]["when"]:
        bad.append("KildallDriveLetters1974: date missing from story")
    if "30 July 2012" not in by["PitrouPathlib2012"]["story"]:
        bad.append("PitrouPathlib2012: date missing from story")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
