"""SEN0414 chapter 3 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this
file's self-check. Three stories for Loops and Modules:

* GaussSum - the schoolroom legend, honestly labelled as a traced legend, and the chapter's
  gauss program that settles the arithmetic either way.
* ZeroStart - why range(5) stops before 5: Dijkstra wrote the memo, by hand, in 1982.
* MersenneRandom - the 1997 generator from Hiroshima inside every random.randint you call.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

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
        "where": "handwritten memo EWD831, Austin, Texas",
        "link": "https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html",
        "concepts": ["Sequence", "Repetition"],
        "story": ("In August 1982 Dijkstra wrote a two-page memo, by fountain pen as always, "
                  "titled 'Why numbering should start at zero'. His argument: half-open ranges - "
                  "include the start, exclude the stop - make lengths obvious (stop minus start), "
                  "let adjacent ranges meet without overlap, and avoid ugly sentinels. Python "
                  "follows it everywhere: range(5) yields five numbers starting at 0, and the "
                  "chapter's consoles show adjacent ranges clicking together exactly as the memo "
                  "promised."),
        "lesson": "Half-open ranges are a 1982 argument your loops quietly obey",
        "source": ("E.W. Dijkstra, EWD831, 'Why numbering should start at zero', dated 11 August "
                   "1982, in the EWD archive at the University of Texas. Photo: Hamilton "
                   "Richards, CC BY-SA 3.0."),
    },
    {
        "id": "MersenneRandom",
        "title": "The 1997 twister inside random",
        "when": "1997-98",
        "who": "Makoto Matsumoto and Takuji Nishimura",
        "where": "Keio and Yamagata universities, Japan; published in ACM TOMACS",
        "link": "https://en.wikipedia.org/wiki/Mersenne_Twister",
        "concepts": ["Module", "ModernPractice"],
        "story": ("When the chapter imports random, it wakes a generator with a name like a "
                  "fairground ride: the Mersenne Twister, published by Matsumoto and Nishimura in "
                  "1997-98. Its period is 2 to the 19937th minus 1 - a Mersenne prime - meaning "
                  "the sequence of 'random' numbers will not repeat within any lifetime. It became "
                  "the default generator of Python, R and countless tools; good enough for games "
                  "and simulations, and - the docs warn - deliberately not for cryptography."),
        "lesson": "import random wakes a named, dated, published algorithm",
        "source": ("Matsumoto and Nishimura, 'Mersenne Twister: a 623-dimensionally "
                   "equidistributed uniform pseudo-random number generator', ACM TOMACS 8(1), "
                   "1998; period 2^19937-1; Python's random module documents it as its core "
                   "generator."),
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
    if "1856" not in STORIES[0]["source"]:
        bad.append("GaussSum: the traced-legend date missing from source")
    if "EWD831" not in STORIES[1]["source"]:
        bad.append("ZeroStart: memo number missing from source")
    if "2^19937-1" not in STORIES[2]["source"]:
        bad.append("MersenneRandom: the period missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
