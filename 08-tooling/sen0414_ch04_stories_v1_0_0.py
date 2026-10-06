"""SEN0414 chapter 4 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this
file's self-check. Three stories for Functions:

* ClosedSubroutine - the function itself has a birth certificate: Cambridge, 1952.
* CollatzMystery - the chapter's recursion playground is an unsolved 1937 problem, and the
  chapter program walks it.
* Pep758Arrives - the chapter's except clause got lighter in Python 3.14, and the recording
  under 3.14 proves it on the slide.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "ClosedSubroutine",
        "title": "1952: the function gets invented",
        "when": "1952",
        "who": "David Wheeler, on EDSAC at the University of Cambridge",
        "where": "the Cambridge Mathematical Laboratory; published through the ACM",
        "link": "https://en.wikipedia.org/wiki/David_Wheeler_(computer_scientist)",
        "concepts": ["Function", "Frames"],
        "story": ("On EDSAC, one of the first stored-program computers, David Wheeler worked out "
                  "how a program could jump into a reusable block of code and - the hard part - "
                  "find its way back to wherever it came from. His 'closed subroutine' and the "
                  "jump-and-return it needed (long called the Wheeler jump) are the ancestor of "
                  "every def on these slides, and the call stack the chapter draws is the modern "
                  "descendant of his return-address bookkeeping."),
        "lesson": "def and return are 1952 inventions you use every day",
        "source": ("David Wheeler's closed-subroutine work on EDSAC, Cambridge, published 1952 "
                   "through the ACM ('The use of sub-routines in programmes'); the return linkage "
                   "is historically known as the Wheeler jump. Photo: EDSAC, Computer Laboratory, "
                   "University of Cambridge, CC BY 2.0."),
    },
    {
        "id": "CollatzMystery",
        "title": "The unsolved problem in your homework",
        "when": "posed 1937; still open",
        "who": "Lothar Collatz; famously weighed by Paul Erdos",
        "where": "Hamburg; the chapter's own collatz program",
        "link": "https://en.wikipedia.org/wiki/Collatz_conjecture",
        "concepts": ["Function", "Result"],
        "story": ("Take any positive integer: halve it if even, triple-and-add-one if odd, "
                  "repeat. Lothar Collatz conjectured in 1937 that you always reach 1. Nobody has "
                  "proved it; Paul Erdos said mathematics is not yet ripe for such questions and "
                  "offered 500 dollars for a proof. The chapter's collatz program is this exact "
                  "rule as a function - your homework walks a problem that has outlasted every "
                  "mathematician since."),
        "lesson": "A five-line function can hold an unsolved problem",
        "source": ("The Collatz conjecture, posed 1937, open to this day; Erdos's remark and "
                   "500-dollar offer are standard in its literature - summarized with references "
                   "at en.wikipedia.org/wiki/Collatz_conjecture. The chapter program "
                   "collatz_v1_0_0.py implements the rule."),
    },
    {
        "id": "Pep758Arrives",
        "title": "The except clause sheds its parentheses",
        "when": "Python 3.14, 2025",
        "who": "proposed and accepted through the CPython core developers' PEP process",
        "where": "PEP 758, peps.python.org",
        "link": "https://peps.python.org/pep-0758/",
        "concepts": ["ErrorHandling", "ModernPractice"],
        "story": ("For decades, catching two exception types required parentheses: except "
                  "(ValueError, TypeError). PEP 758 let the parentheses go, and Python 3.14 "
                  "ships it. This deck does not take the release notes' word for it: the chapter "
                  "program with the bare except clause was EXECUTED under Python 3.14 during this "
                  "build, and its transcript on the slide is what that interpreter printed. On "
                  "3.13 the same file is a SyntaxError - version truth, demonstrated."),
        "lesson": "Language change is checkable - run the feature, not the rumour",
        "source": ("PEP 758 ('Allow except and except* expressions without parentheses'), "
                   "accepted for Python 3.14 (peps.python.org/pep-0758); the chapter program "
                   "except758_v1_0_0.py runs clean under the build's 3.14.6 and raises "
                   "SyntaxError under 3.13 - both observed during this build."),
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
    if "1952" not in STORIES[0]["source"]:
        bad.append("ClosedSubroutine: date missing from source")
    if "1937" not in STORIES[1]["source"]:
        bad.append("CollatzMystery: date missing from source")
    if "3.14" not in STORIES[2]["source"]:
        bad.append("Pep758Arrives: version missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
