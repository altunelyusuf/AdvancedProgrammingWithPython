"""SEN0414 chapter 16 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
SQLite databases, written fresh for this chapter from sources opened on 2026-10-12 (the HTTP status each link answered to a
plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch16_stories_v1_0_0.py links` asks again):

* SqliteBegins2000 - D. Richard Hipp designed SQLite in the spring of 2000 while working for General Dynamics on a contract with the
  United States Navy, on damage-control software for guided-missile destroyers (Wikipedia, 'SQLite', History).
* CoddRelationalModel1970 - E. F. Codd's paper 'A Relational Model of Data for Large Shared Data Banks', Communications of the ACM,
  volume 13, number 6, June 1970, written at the IBM San Jose Research Lab (IBM's history page and the paper's own page header).
* PythonGainsSqlite2006 - Python 2.5, released on 19 September 2006, added the pysqlite wrapper to the standard library as the
  package sqlite3 (What's New in Python 2.5).
* BobbyTables2007 - xkcd 327, 'Exploits of a Mom', 10 October 2007, whose mother tells a school to sanitize its database inputs.
* StrictTables2021 - SQLite release 3.37.0 of 27 November 2021, which brought STRICT tables, the keyword the chapter uses.
* AcidNamed1983 - the acronym ACID appears in Theo Haerder and Andreas Reuter's 1983 paper 'Principles of Transaction-Oriented
  Database Recovery' in ACM Computing Surveys (Wikipedia, 'ACID').

No photograph is used. Wikimedia Commons answered 429 (too many requests) to two searches on the day, so no file was fetched and no licence record exists;
03-materials/ch16/assets is not made and there is no ASSETS_PROVENANCE; ch16-page/stories_img_v1_0_0.json says so. A claim the
research first planned and dropped: a date for the renaming of SQLiteStudio to Letos, which no page opened on the day gives.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "SqliteBegins2000",
        "title": "SQLite was written in 2000 so that a Navy warship program no longer needed a database server",
        "when": "Spring 2000",
        "who": "D. Richard Hipp, then working for General Dynamics on a contract with the United States Navy",
        "where": "Software for the damage-control system of guided-missile destroyers",
        "link": "https://en.wikipedia.org/wiki/SQLite",
        "concepts": ["SingleFileServerless", "NoGrantRevoke"],
        "story": ("Wikipedia's history of SQLite says D. Richard Hipp designed it in the spring of 2000 while he worked for General "
                   "Dynamics on a contract with the United States Navy. He was writing software for the damage-control system aboard "
                   "guided-missile destroyers, a system that first used HP-UX with an Informix database as its back end. The article "
                   "dates the first release of SQLite to 17 August 2000 and calls the software public domain. A database that is one "
                   "file with no server to start, and no user accounts to grant, is the SQLite that chapter 16 opens with Python."),
        "lesson": "A database can be a library and a file, not a server",
        "source": ("Wikipedia, 'SQLite' (History: designed in the spring of 2000 by D. Richard Hipp at General Dynamics for the US Navy; "
                    "initial release 2000-08-17; public domain), read 2026-10-12; sqlite.org/about.html and sqlite.org/serverless.html."),
    },
    {
        "id": "CoddRelationalModel1970",
        "title": "A 1970 paper from IBM's San Jose lab proposed the tables that a SQLite file still holds",
        "when": "June 1970",
        "who": "Edgar F. Codd, a mathematician at the IBM San Jose Research Lab",
        "where": "Communications of the ACM, volume 13, number 6",
        "link": "https://www.ibm.com/history/relational-database",
        "concepts": ["SeparateTableDesign", "InnerJoin"],
        "story": ("IBM's history page tells how Edgar F. Codd, an Oxford-educated mathematician at the IBM San Jose Research Lab, "
                   "published a paper in 1970 titled 'A Relational Model of Data for Large Shared Data Banks'. The paper is in Volume 13, "
                   "Number 6 of Communications of the ACM, dated June 1970. Before it, IBM says, getting data out of the large "
                   "information systems of the 1960s took specialists who often wrote whole programs to reach one fact. The chapter's "
                   "cats table and vaccinations table, linked by a number and read back with a join, are the relational model in a few lines."),
        "lesson": "Put each kind of fact in its own table and join them",
        "source": ("IBM, 'The relational database', ibm.com/history/relational-database (read 2026-10-12); E. F. Codd, 'A Relational "
                    "Model of Data for Large Shared Data Banks', Communications of the ACM 13(6), June 1970 (the paper's text, "
                    "engineering.upenn.edu/~zives/03f/cis550/codd.pdf)."),
    },
    {
        "id": "PythonGainsSqlite2006",
        "title": "Python 2.5 added the sqlite3 package to the standard library in 2006",
        "when": "19 September 2006",
        "who": "The Python developers, with the pysqlite module as the base",
        "where": "The Python standard library, release 2.5",
        "link": "https://docs.python.org/3.14/whatsnew/2.5.html",
        "concepts": ["ConnectCreatesFile", "SqliteVersion"],
        "story": ("What's New in Python 2.5, written by A.M. Kuchling, states that Python 2.5 was released on September 19, 2006. "
                   "It lists the SQLite database module among the new modules, together with ElementTree and ctypes. The section on the "
                   "package says the pysqlite wrapper had been added to the standard library under the name sqlite3. Since then a "
                   "Python program can open a database file with no install, which is why chapter 16 can start with import sqlite3. "
                   "The library inside it is a separate component, so the version of SQLite depends on the Python build."),
        "lesson": "Python ships the module, the build decides the SQLite",
        "source": ("Python documentation, 'What's New in Python 2.5' (release date; the sqlite3 package section), docs.python.org/3.14/whatsnew/2.5.html, "
                    "read 2026-10-12; this study's record of ten interpreters, which link SQLite 3.45.1, 3.50.4 and 3.53.1."),
    },
    {
        "id": "BobbyTables2007",
        "title": "A webcomic in 2007 made 'Little Bobby Tables' the standard warning about SQL injection",
        "when": "10 October 2007",
        "who": "Randall Munroe, the author of xkcd",
        "where": "xkcd comic number 327, 'Exploits of a Mom'",
        "link": "https://xkcd.com/327/",
        "concepts": ["SqlInjection", "QmarkPlaceholders"],
        "story": ("xkcd number 327, 'Exploits of a Mom', was published on 10 October 2007. In it a school phones a mother about her son, "
                   "whose name was written as text that closes a statement and drops the table of student records. The mother ends by "
                   "hoping the school has learned to sanitize its database inputs. Chapter 16 answers the comic with the ? placeholder, "
                   "and this study ran the attack: pasted into an f-string the text changed the query, bound as a parameter it matched nothing."),
        "lesson": "Bind values with placeholders; never paste them into SQL",
        "source": ("xkcd.com/327/ and xkcd.com/327/info.0.json (number 327, 2007-10-10, 'Exploits of a Mom', read 2026-10-12); this study's "
                    "leaf SqlInjection."),
    },
    {
        "id": "StrictTables2021",
        "title": "SQLite 3.37.0 gave tables a strict mode in November 2021",
        "when": "27 November 2021",
        "who": "The SQLite developers",
        "where": "SQLite release 3.37.0, announced on sqlite.org",
        "link": "https://sqlite.org/releaselog/3_37_0.html",
        "concepts": ["StrictMode", "StrictVersionClaim"],
        "story": ("The release log of SQLite 3.37.0 is dated 2021-11-27 and opens with STRICT tables, a prescriptive style of data type "
                   "management for developers who prefer that kind of thing. Before that release a column's declared type was only a "
                   "preference, so text could land in a column declared INTEGER. The chapter builds every table with STRICT, and in this "
                   "study the text 'Hello' was refused in an INTEGER column of a strict table and stored as text in a plain one. "
                   "Python 3.11 was run with SQLite 3.45.1, newer than the release that added the keyword."),
        "lesson": "Declare STRICT so a column's type is a rule",
        "source": ("SQLite release log 3.37.0 (2021-11-27), sqlite.org/releaselog/3_37_0.html, read 2026-10-12; sqlite.org/stricttables.html; "
                    "this study's leaves StrictMode and StrictVersionClaim."),
    },
    {
        "id": "AcidNamed1983",
        "title": "Two German researchers gave transactions the name ACID in 1983",
        "when": "1983",
        "who": "Theo Haerder and Andreas Reuter",
        "where": "ACM Computing Surveys, in the paper 'Principles of Transaction-Oriented Database Recovery'",
        "link": "https://en.wikipedia.org/wiki/ACID",
        "concepts": ["AtomicStatement", "DurableAfterReopen"],
        "story": ("Wikipedia says the acronym ACID appears in Theo Haerder and Andreas Reuter's 1983 paper, 'Principles of "
                   "Transaction-Oriented Database Recovery', which built on earlier work on transactions by researchers including Jim Gray. "
                   "The paper grouped atomicity, consistency, isolation and durability as the properties of a transaction. "
                   "SQLite's own pages describe SQLite as transactional and test it with simulated power loss. In this study a failed "
                   "statement changed nothing, and a committed row was still there when the file was opened again."),
        "lesson": "A transaction is all of its changes or none",
        "source": ("Wikipedia, 'ACID' (the 1983 paper by Haerder and Reuter, ACM Computing Surveys), read 2026-10-12; sqlite.org/transactional.html and "
                    "sqlite.org/testing.html; this study's leaves AtomicStatement and DurableAfterReopen."),
    },
]

LINK_STATUS = {'SqliteBegins2000': 200, 'CoddRelationalModel1970': 200, 'PythonGainsSqlite2006': 200, 'BobbyTables2007': 200, 'StrictTables2021': 200, 'AcidNamed1983': 200}


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
        if LINK_STATUS and LINK_STATUS.get(x["id"]) != 200:
            bad.append("%s: link status %r, not 200" % (x["id"], LINK_STATUS.get(x["id"])))
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("SqliteBegins2000", "2000"), ("CoddRelationalModel1970", "1970"), ("PythonGainsSqlite2006", "2006"),
                      ("BobbyTables2007", "2007"), ("StrictTables2021", "2021"), ("AcidNamed1983", "1983")):
        if year not in by[sid]["story"] or year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"})
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
