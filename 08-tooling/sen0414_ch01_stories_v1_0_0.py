"""SEN0414 chapter 1 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule, carried over from the SEN0401 materials: every story on a slide is real,
dated and sourced, with one live link, enforced by this file's self-check. Three stories for
Python Basics:

* PythonBirth - a Christmas holiday in 1989, a language named after a comedy troupe, and the
  interpreter every example in this course runs on.
* BookFree - the course textbook is free to read online by its author's own choice; the course
  pins the 3rd edition.
* FreeThreading - the chapter's ModernPractice branch, dated: PEP 703, and the gil console on
  these slides interrogates the very interpreter in front of you.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "PythonBirth",
        "title": "A Christmas project named after a comedy troupe",
        "when": "1989-12 to 1991-02",
        "who": "Guido van Rossum, at CWI in Amsterdam",
        "where": "released to the alt.sources newsgroup as version 0.9.0",
        "link": "https://en.wikipedia.org/wiki/Guido_van_Rossum",
        "concepts": ["ExecutionEnvironment", "Value"],
        "story": ("Over the 1989 Christmas break, a researcher at the Dutch CWI institute started "
                  "a hobby interpreter to keep himself busy while the office was closed. He named "
                  "it after Monty Python's Flying Circus, not the snake. In February 1991 he "
                  "posted version 0.9.0 to the alt.sources newsgroup, and for the next three "
                  "decades served as the language's 'Benevolent Dictator For Life'. Every "
                  "prompt on these slides is that hobby project, grown up."),
        "lesson": "The tool you are learning began as one person's two-week itch",
        "source": ("Python's documented history: project begun December 1989 at CWI; 0.9.0 posted "
                   "to alt.sources in February 1991; summarized with references at "
                   "en.wikipedia.org/wiki/Guido_van_Rossum. Photo: Daniel Stroud, CC BY-SA 4.0."),
    },
    {
        "id": "BookFree",
        "title": "The textbook that gives itself away",
        "when": "3rd edition, 2025",
        "who": "Al Sweigart, with No Starch Press",
        "where": "automatetheboringstuff.com - free to read online",
        "link": "https://automatetheboringstuff.com",
        "concepts": ["ModernPractice"],
        "story": ("The course follows 'Automate the Boring Stuff with Python', and its author "
                  "publishes the full text free on the web under a Creative Commons licence - the "
                  "paper edition funds the habit. The 3rd edition of 2025 is the one this course "
                  "pins, and every chapter corpus in this repository records which printed claims "
                  "it verified against which sources. Read ahead any evening; it costs nothing."),
        "lesson": "Your textbook is a link, not a bill - use it every week",
        "source": ("automatetheboringstuff.com, the author's own free online edition (Creative "
                   "Commons licensed); 3rd edition, No Starch Press, 2025 - the edition the "
                   "chapter sources file cites as its first entry."),
    },
    {
        "id": "FreeThreading",
        "title": "The interpreter sheds its oldest lock",
        "when": "accepted 2023-07; optional builds since Python 3.13",
        "who": "Sam Gross's design, accepted by the Python Steering Council as PEP 703",
        "where": "peps.python.org - and the interpreter running these slides",
        "link": "https://peps.python.org/pep-0703/",
        "concepts": ["ModernPractice", "ExecutionEnvironment"],
        "story": ("For most of Python's life a Global Interpreter Lock let only one thread run "
                  "Python code at a time. In July 2023 the Steering Council accepted PEP 703, "
                  "built on Sam Gross's work, making the lock optional; free-threaded builds have "
                  "shipped beside the standard ones since Python 3.13. This is not trivia from a "
                  "changelog: the gil console on these slides asks the interpreter in front of "
                  "you whether its lock is on, and prints what it answers."),
        "lesson": "Modern practice is checkable - ask your own interpreter",
        "source": ("PEP 703 'Making the Global Interpreter Lock Optional in CPython', author Sam "
                   "Gross, accepted by the Steering Council in July 2023 (peps.python.org/pep-0703); "
                   "the deck's gil console reads sys._is_gil_enabled() from the build interpreter."),
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
    if "February 1991" not in STORIES[0]["source"]:
        bad.append("PythonBirth: release date missing from source")
    if "3rd edition" not in STORIES[1]["source"]:
        bad.append("BookFree: edition missing from source")
    if "PEP 703" not in STORIES[2]["source"]:
        bad.append("FreeThreading: PEP missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
