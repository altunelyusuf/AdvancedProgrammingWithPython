"""SEN0414 chapter 2 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this
file's self-check. Three stories for Flow Control:

* BooleTruth - the True and False on every slide are named after a person with dates.
* IndentationChoice - Python's most argued-about feature is a documented design decision, and
  the chapter's indentation programs demonstrate exactly what it buys.
* MatchArrives - the match statement has a birthday; the chapter's match programs run it.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "BooleTruth",
        "title": "The man inside the bool type",
        "when": "1847 and 1854",
        "who": "George Boole, self-taught mathematician, first professor of mathematics at Cork",
        "where": "Lincoln, England and Queen's College, Cork",
        "link": "https://en.wikipedia.org/wiki/George_Boole",
        "concepts": ["Comparison", "BooleanOperation"],
        "story": ("A shoemaker's son from Lincoln taught himself mathematics, and in 'The "
                  "Mathematical Analysis of Logic' (1847) and 'The Laws of Thought' (1854) showed "
                  "that reasoning itself obeys algebra: statements as values, AND and OR as "
                  "operations. He never saw a computer. A century later his algebra became the "
                  "switching logic of every circuit, and Python names its True-and-False type "
                  "bool after him - every condition on today's slides is Boole's arithmetic."),
        "lesson": "Every if statement runs on one Victorian's algebra",
        "source": ("George Boole, 'The Mathematical Analysis of Logic' (1847) and 'An "
                   "Investigation of the Laws of Thought' (1854); biography at "
                   "en.wikipedia.org/wiki/George_Boole. Portrait: public domain, via Wikimedia "
                   "Commons."),
    },
    {
        "id": "IndentationChoice",
        "title": "The whitespace that is the syntax",
        "when": "design decision of the late 1980s",
        "who": "Guido van Rossum, carrying a lesson from the ABC language at CWI",
        "where": "documented in Python's own design FAQ",
        "link": "https://docs.python.org/3/faq/design.html#why-does-python-use-indentation-for-grouping-of-statements",
        "concepts": ["FlowControl"],
        "story": ("Most languages mark blocks with braces and treat indentation as decoration; "
                  "Python makes the indentation itself the block. The choice came from ABC, the "
                  "teaching language Guido van Rossum worked on at CWI before Python, and the "
                  "design FAQ still defends it: what you see is what the interpreter sees, so a "
                  "program cannot look right and group wrong. The chapter's two indentation "
                  "programs run the same lines indented two ways - and print different stories."),
        "lesson": "In Python the layout cannot lie about the logic",
        "source": ("The Python design FAQ, 'Why does Python use indentation for grouping of "
                   "statements?' (docs.python.org/3/faq/design.html); the ABC lineage per van "
                   "Rossum's documented history of the language."),
    },
    {
        "id": "MatchArrives",
        "title": "A thirty-year-old wish, granted in 3.10",
        "when": "accepted 2021-02; shipped 2021-10 in Python 3.10",
        "who": "PEPs 634-636 by Brandt Bucher, Guido van Rossum and colleagues",
        "where": "peps.python.org; the Steering Council's acceptance",
        "link": "https://peps.python.org/pep-0636/",
        "concepts": ["FlowControl", "ModernPractice"],
        "story": ("For decades Python answered 'where is my switch statement?' with dictionaries "
                  "and elif chains. In February 2021 the Steering Council accepted structural "
                  "pattern matching - PEPs 634, 635 and 636 - and Python 3.10 shipped the match "
                  "statement that October. It is more than a switch: patterns destructure data "
                  "and bind names. The chapter's match programs - command words, status codes, "
                  "captures, guards - run the real thing, and their transcripts are on these "
                  "slides."),
        "lesson": "match is a 2021 feature - your textbook generation saw it arrive",
        "source": ("PEP 634/635/636 (structural pattern matching), accepted by the Python "
                   "Steering Council in February 2021; first released in Python 3.10, October "
                   "2021. Tutorial: peps.python.org/pep-0636."),
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
    if "1854" not in STORIES[0]["source"]:
        bad.append("BooleTruth: date missing from source")
    if "faq/design" not in STORIES[1]["link"]:
        bad.append("IndentationChoice: FAQ link drifted")
    if "February 2021" not in STORIES[2]["source"]:
        bad.append("MatchArrives: acceptance date missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
