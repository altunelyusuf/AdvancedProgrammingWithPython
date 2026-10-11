"""SEN0414 chapter 10 - the story companion to the chapter corpus (version 1.0.0).

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
__version__ = "1.0.0"

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
        "id": "ThompsonPikeUtf8",
        "title": "UTF-8 was designed on a diner placemat in September 1992",
        "when": "1992-09",
        "who": "Ken Thompson and Rob Pike",
        "where": "a diner in New Jersey, and Bell Labs, Murray Hill",
        "link": "https://doc.cat-v.org/bell_labs/utf-8_history",
        "concepts": ["EncodingArgument"],
        "story": ("Rob Pike wrote that UTF-8 was 'designed, in front of my eyes, on a placemat in a New Jersey "
                   "diner one night in September' 1992, with Ken Thompson working out the bit-packing by hand "
                   "while Pike watched; the surviving source changes date the first working code to 4 September "
                   "1992 and a proposal mailed to the X/Open committee to 8 September 1992. The two had been asked "
                   "to review a rival encoding, FSS/UTF, for the Plan 9 operating system they were building at "
                   "Bell Labs, found it unable to recover a byte stream picked up mid-character, and designed a "
                   "fix overnight instead; by the end of that week, Plan 9 ran entirely on the format. The chapter's "
                   "own encoding argument to open(), almost always 'utf-8' by the chapter's own count, names the "
                   "format that one dinner produced, now the assumed encoding of the web and, from Python 3.15 on, "
                   "the language's own default."),
        "lesson": "'utf-8' in open() names a format from one 1992 dinner",
        "source": ("Rob Pike, 'UTF-8 history', doc.cat-v.org/bell_labs/utf-8_history (first code 4 Sep 1992, "
                    "X/Open proposal 8 Sep 1992); Python documentation, io - the encoding argument, and PEP 686. "
                    "Photo: Wikimedia Commons."),
    },
    {
        "id": "CrockfordJson2001",
        "title": "A format written up in 2001 is shelve's own plain alternative",
        "when": "2001",
        "who": "Douglas Crockford and Chip Morningstar",
        "where": "State Software, a consulting firm in California",
        "link": "https://en.wikipedia.org/wiki/JSON",
        "concepts": ["JsonSaving"],
        "story": ("Working together at State Software, Douglas Crockford and Chip Morningstar wanted a browser "
                   "and a server to exchange data without reloading the page, and built it on a technique Crockford "
                   "had learned of from Netscape: writing a JavaScript object straight into a hidden frame. The "
                   "reserved word 'do' broke an early version as a bare key, so Crockford quoted every key instead, "
                   "and the quoted, minimal format he wrote up in 2001 became JSON; he opened json.org on 12 "
                   "November 2002 and kept adding compatible parsers to it as other programmers wrote them, by "
                   "design small enough to fit on a business card. The chapter sets exactly this format beside "
                   "shelve as the alternative for data meant to be read by another program or language, with "
                   "json.dump() and json.load() replacing shelve's own Python-only pickle."),
        "lesson": "json, shelve's plain alternative, was written up in 2001",
        "source": ("'JSON', Wikipedia, en.wikipedia.org/wiki/JSON (Crockford and Morningstar, State Software, "
                    "2001; json.org opened 12 November 2002); Python documentation, json - JSON encoder and "
                    "decoder. Photo: Wikimedia Commons."),
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
    if "September" not in by["ThompsonPikeUtf8"]["story"] or "1992" not in by["ThompsonPikeUtf8"]["when"]:
        bad.append("ThompsonPikeUtf8: date missing from story")
    if "2001" not in by["CrockfordJson2001"]["story"] or "12 November 2002" not in by["CrockfordJson2001"]["story"]:
        bad.append("CrockfordJson2001: date missing from story")
    if "30 July 2012" not in by["PitrouPathlib2012"]["story"]:
        bad.append("PitrouPathlib2012: date missing from story")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
