"""SEN0414 chapter 3 - the story companion to the chapter corpus (version 1.1.0, over 1.0.0).

Changes over 1.0.0 (the older file stays as it is): (a) the place of Dijkstra's memo EWD831 is Nuenen, the Netherlands,
where he wrote it; the archive that keeps it is at the University of Texas at Austin (1.0.0 said Austin as the place of writing);
(b) the Mersenne Twister story is not carried (no free picture; it is not in the deck 5.0.0); (c) the story of PEP 572 (the walrus
operator) is added, as on slide 12 of the deck 5.0.0. Same 5N1K shape and self-check.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.1.0"

STORIES = [
    {
        "id": "GaussSum",
        "title": "The schoolboy who refused to loop",
        "when": "legend set in the 1780s; traced in print back to 1856",
        "who": "Carl Friedrich Gauss (1777-1855), in a Brunswick schoolroom",
        "where": "the anecdote's paper trail, collected by Brian Hayes",
        "link": "https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss",
        "concepts": ["Repetition"],
        "story": ("The story says a teacher set the class to add every number from 1 to 100, and "
                  "young Gauss answered at once: pair 1 with 100, 2 with 99 - fifty pairs of 101, "
                  "5050. The tale grew in the telling - Brian Hayes traced dozens of versions back "
                  "to an 1856 memorial - but the mathematics needs no legend. The chapter's gauss "
                  "program does it both ways: the loop accumulates 5050, and Gauss's closed form "
                  "agrees without looping at all."),
        "lesson": "A loop is honest work - and sometimes a formula beats it",
        "source": ("The anecdote's documented trail: first printed in Wolfgang Sartorius von "
                   "Waltershausen's 1856 memorial of Gauss; versions collected by Brian Hayes "
                   "('Gauss's Day of Reckoning', American Scientist, 2006). Portrait: Jensen, "
                   "1840, public domain."),
    },
    {
        "id": "ZeroStart",
        "title": "Why range(5) stops before five",
        "when": "1982-08-11",
        "who": "Edsger W. Dijkstra, Turing Award 1972",
        "where": "Nuenen, the Netherlands, where he wrote the handwritten memo EWD831; the memo is kept in the EWD archive at the University of Texas at Austin",
        "link": "https://en.wikipedia.org/wiki/Edsger_W._Dijkstra",
        "concepts": ["Sequence", "Repetition"],
        "story": ("In August 1982 Dijkstra wrote a two-page memo, by fountain pen as always, "
                  "titled 'Why numbering should start at zero'. He was then a Burroughs research fellow in Nuenen. "
                  "His argument: half-open ranges - "
                  "include the start, exclude the stop - make lengths obvious (stop minus start), "
                  "let adjacent ranges meet without overlap, and avoid ugly sentinels. Python "
                  "follows it everywhere: range(5) yields five numbers starting at 0, and the "
                  "chapter's consoles show adjacent ranges clicking together exactly as the memo "
                  "promised."),
        "lesson": "Half-open ranges are a 1982 argument your loops quietly obey",
        "source": ("E.W. Dijkstra, EWD831, 'Why numbering should start at zero', dated 11 August "
                   "1982, written in Nuenen, the Netherlands; the EWD archive at the University of Texas at Austin keeps it "
                   "(https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html, not reachable from the build machine, link check open). "
                   "Photo: Hamilton Richards, CC BY-SA 3.0."),
    },
    {
        "id": "WalrusPep572",
        "title": "The walrus operator and PEP 572",
        "when": "PEP created 2018-02-28; operator in Python 3.8; Guido stepped down 2018-07-12",
        "who": "Chris Angelico, Tim Peters and Guido van Rossum (authors); Guido, Python's creator, decided",
        "where": "the python-dev mailing list and the PEP at peps.python.org",
        "link": "https://peps.python.org/pep-0572/",
        "concepts": ["Loop", "Assignment expression"],
        "story": ("PEP 572 proposed the walrus operator :=, which names a value inside an expression, "
                  "as in while chunk := f.read(5). Reading a file in pieces had needed a read and a test on separate lines; := joins them. "
                  "The debate on python-dev was long and heated. After it Guido accepted the PEP, and on 12 July 2018 he "
                  "stepped down as Python's benevolent dictator for life."),
        "lesson": "One small operator cost a language its dictator",
        "source": ("PEP 572, Assignment Expressions (created 28-Feb-2018, Python-Version 3.8), peps.python.org/pep-0572/; "
                   "Guido van Rossum's step-down on 12 July 2018. Photo: Daniel Stroud, CC BY-SA 4.0."),
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
    if "1856" not in by["GaussSum"]["source"]:
        bad.append("GaussSum: the traced-legend date missing from source")
    if "EWD831" not in by["ZeroStart"]["source"]:
        bad.append("ZeroStart: memo number missing from source")
    if "Nuenen" not in by["ZeroStart"]["where"] or "Austin" not in by["ZeroStart"]["where"]:
        bad.append("ZeroStart: the place of writing (Nuenen) and the archive (Austin) must both be named")
    if "28-Feb-2018" not in by["WalrusPep572"]["source"]:
        bad.append("WalrusPep572: PEP date missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
