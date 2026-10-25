"""SEN0414 chapter 4 - the story companion to the chapter corpus (version 1.1.0, over 1.0.0; the older file stays as it is).

Changes over 1.0.0: the three stories now say what the deck 3.0.0 says on its story slides 8, 36 and 42 (5N1K: who, what/how, when, where, why):
(a) ClosedSubroutine: the closed subroutine is credited to David Wheeler with Maurice Wilkes and Stanley Gill, around 1951, described in 1952; (b) CollatzMystery:
posed in 1937, two years after Collatz's doctorate; the bound checked by computers is stated; (c) Pep758Arrives: the authors (Pablo Galindo Salgado and Brett Cannon) and the
dates (created 30 September 2024, resolved 14 March 2025) are given, and the claim that the chapter program with the bare except clause was executed under Python 3.14 is
dropped - the deck 3.0.0 keeps the parentheses that work in every version. Same shape and self-check as 1.0.0.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.1.0"

STORIES = [
    {
        "id": "ClosedSubroutine",
        "title": "1952: the function gets invented",
        "when": "around 1951; described in 1952",
        "who": "David Wheeler, with Maurice Wilkes and Stanley Gill, at the University of Cambridge",
        "where": "the Mathematical Laboratory in Cambridge, on EDSAC, one of the first stored-program computers",
        "link": "https://en.wikipedia.org/wiki/David_Wheeler_(computer_scientist)",
        "concepts": ["Function", "Frames"],
        "story": ("On EDSAC, David Wheeler worked out how a program could jump into a reusable block of code and, "
                  "the hard part, find its way back to the place it came from. His 'closed subroutine' kept the "
                  "return address, and the jump was long called the Wheeler jump. A library of tested routines could "
                  "then be reused instead of written again: deduplication, long before the word. The call stack "
                  "the chapter draws is the grown-up form of that return-address bookkeeping."),
        "lesson": "def and return are 1952 inventions you use every day",
        "source": ("David Wheeler, 'The use of sub-routines in programmes', ACM national meeting, 1952; the closed "
                   "subroutine is credited to Wheeler with Wilkes and Gill around 1951 (Wikipedia: David Wheeler, "
                   "computer scientist). Photo: EDSAC, Computer Laboratory, University of Cambridge, CC BY 2.0."),
    },
    {
        "id": "CollatzMystery",
        "title": "The unsolved problem in your homework",
        "when": "posed 1937; still open",
        "who": "Lothar Collatz, who posed it two years after his doctorate; Paul Erdos, who judged it",
        "where": "mathematics papers worldwide; the chapter's own collatz function",
        "link": "https://en.wikipedia.org/wiki/Collatz_conjecture",
        "concepts": ["Function", "Result"],
        "story": ("Take any positive integer: halve it if even, triple it and add one if odd, repeat. Lothar Collatz "
                  "conjectured in 1937 that you always reach 1. Nobody has proved it and nobody has found a "
                  "counterexample; computers have checked every start up to about 2.36 times 10 to the 21. Paul Erdos "
                  "said that mathematics may not be ready for such problems. The chapter's collatz function is the "
                  "whole rule in four lines."),
        "lesson": "A five-line function can hold an unsolved problem",
        "source": ("The Collatz conjecture, introduced 1937, open to this day; the Erdos remark and the checked bound "
                   "are summarized with references at en.wikipedia.org/wiki/Collatz_conjecture. "
                   "Photo: Paul Erdos, Budapest, autumn 1992, Topsy Kretts, CC BY 3.0."),
    },
    {
        "id": "Pep758Arrives",
        "title": "The except clause sheds its parentheses",
        "when": "PEP created 30 September 2024; resolved 14 March 2025; Python 3.14",
        "who": "Pablo Galindo Salgado and Brett Cannon, Python core developers",
        "where": "the Python Enhancement Proposal process, peps.python.org; the change lives in CPython",
        "link": "https://peps.python.org/pep-0758/",
        "concepts": ["ErrorHandling", "ModernPractice"],
        "story": ("For years, catching two exception types needed parentheses: except (ValueError, TypeError). "
                  "PEP 758 lets several types be listed without parentheses when there is no as clause, so "
                  "except ValueError, TypeError reads like the list it is. Python 3.14 ships it. Python 3.13 and "
                  "earlier reject the bare list, so the slides keep the parentheses that work everywhere."),
        "lesson": "A common job gets fewer symbols in Python 3.14",
        "source": ("PEP 758, 'Allow except and except* expressions without parentheses', authors Pablo Galindo "
                   "Salgado and Brett Cannon, created 30-Sep-2024, resolved 14-Mar-2025, Python 3.14 "
                   "(peps.python.org/pep-0758). Image: Python logo, python.org, Python Software Foundation."),
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
