"""SEN0414 chapter 9 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Four
stories for Text Pattern Matching with Regular Expressions, written fresh for this chapter:

* KleeneRegularEvents - Stephen Kleene named and defined the regular expression in a 1951 RAND report, the
  mathematical object every pattern this chapter writes is still, formally, an instance of.
* ThompsonRegexSearch - Ken Thompson's 1968 CACM paper gave the world the compile-then-search algorithm, built on
  a non-deterministic finite automaton, that is still exactly the two-step compile()/search() the chapter teaches.
* PerlShorthandClasses - Larry Wall's Perl, first released 18 December 1987, popularised the \\d, \\w and \\s
  shorthand classes the chapter's own character-sets concepts rely on; Python's own documentation still describes
  re's syntax as similar to Perl's.
* SreBecomesRe - Fredrik Lundh's Secret Labs' Regular Expression engine, begun 24 October 1999 at a company with
  the contact address info@pythonware.com, became the engine behind every Pattern and Match object the chapter
  uses, through Python's own _sre.c source history.

Usage: import STORIES; run the file for self-checks. The photographs are named in ch09-page/stories_img_v1_0_0.json.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "KleeneRegularEvents",
        "title": "A mathematician named the pattern, in 1951, for a nerve net",
        "when": "1951",
        "who": "Stephen Cole Kleene",
        "where": "the RAND Corporation, Santa Monica, California",
        "link": "https://en.wikipedia.org/wiki/Stephen_Cole_Kleene",
        "concepts": ["Alternation"],
        "story": ("In 1951, working for the RAND Corporation as an Air Force Project RAND research memorandum, the "
                   "mathematician Stephen Cole Kleene wrote 'Representation of Events in Nerve Nets and Finite "
                   "Automata', Research Memorandum RM-704, defining what he called a regular event: a set of symbol "
                   "sequences built up from single symbols by exactly three operations, concatenation, union and "
                   "repetition. Kleene, born 5 January 1909 in Hartford, Connecticut, spent almost his whole career "
                   "at the University of Wisconsin-Madison, from 1935 until his retirement in 1979, and died on 25 "
                   "January 1994, aged 85. The union of his 1951 definition is exactly the pipe this chapter calls "
                   "alternation, Cat(erpillar|astrophe|ch|egory), and the repetition is exactly the star and plus "
                   "quantifiers; every pattern string this chapter writes is, formally, one more instance of the "
                   "object Kleene named seventy-four years before Python 3.14 compiled it."),
        "lesson": "The pipe and the star in a pattern are Kleene's 1951 union and repetition",
        "source": ("'Stephen Cole Kleene', Wikipedia, en.wikipedia.org/wiki/Stephen_Cole_Kleene (RM-704, RAND "
                    "Corporation, 1951; born 5 January 1909, died 25 January 1994); Al Sweigart, Automate the "
                    "Boring Stuff with Python, 3rd edition (2025), chapter 9. Photo: Wikimedia Commons."),
    },
    {
        "id": "ThompsonRegexSearch",
        "title": "One 1968 paper is why compile() comes before search()",
        "when": "1968-06",
        "who": "Ken Thompson",
        "where": "Communications of the ACM, volume 11, number 6",
        "link": "https://cacmb4.acm.org/magazines/1968/6/12736-programming-techniques-regular-expression-search-algorithm",
        "concepts": ["CompileAndSearch"],
        "story": ("In June 1968 Ken Thompson published 'Regular Expression Search Algorithm' in Communications of "
                   "the ACM, volume 11, number 6, article 12736, describing an algorithm that first compiles a "
                   "regular expression into machine code and then uses that compiled form to search text by "
                   "simulating a non-deterministic finite automaton. Thompson had already built this two-step "
                   "idea, compile once and then search, into the QED text editor he wrote for Bell Labs' CTSS "
                   "system, the first editor to add regular expressions to a text search at all; he later received "
                   "US Patent 3,568,156 for the technique. The chapter's own four steps, re.compile() for a Pattern "
                   "object and then search() for a Match, are the same two-step shape fifty-seven years later, now "
                   "a Python method call apart instead of a step in an editor's own command loop."),
        "lesson": "re.compile() then search() is Ken Thompson's 1968 two-step algorithm",
        "source": ("Ken Thompson, 'Regular Expression Search Algorithm', Communications of the ACM 11(6), June "
                    "1968, article 12736 (cacmb4.acm.org); Doug McIlroy, 'A Research UNIX Reader', the QED history "
                    "at plan9.io/cm/cs/who/dmr/qed.html. Photo: Wikimedia Commons."),
    },
    {
        "id": "PerlShorthandClasses",
        "title": "\\d, \\w and \\s came from a language released in December 1987",
        "when": "1987-12-18",
        "who": "Larry Wall",
        "where": "Unisys, Culver City, California",
        "link": "https://en.wikipedia.org/wiki/Perl",
        "concepts": ["ShorthandClasses"],
        "story": ("Larry Wall released Perl 1.0 on 18 December 1987 while working as a programmer at Unisys, and "
                   "Perl 2, in June 1988, shipped a markedly better regular expression engine built around the "
                   "same backslash shorthand classes this chapter teaches, \\d for a digit, \\w for a word "
                   "character and \\s for whitespace, together with their capitalised opposites. Perl's own regex "
                   "and text-handling strength is what carried it to wide popularity as a CGI scripting language "
                   "through the 1990s, and the shorthand notation travelled with the language's reputation into "
                   "most regex engines written afterward. Python's own re module documentation still introduces "
                   "itself by stating that it provides matching operations similar to those found in Perl, which "
                   "is the one sentence that ties the chapter's \\d+\\s\\w+ most directly back to 1987."),
        "lesson": "\\d, \\w and \\s travelled into Python from Perl, released in 1987",
        "source": ("'Perl', Wikipedia, en.wikipedia.org/wiki/Perl (Perl 1.0, 18 December 1987; Larry Wall at "
                    "Unisys; Perl 2, June 1988); Python documentation, re - Regular expression operations, opening "
                    "sentence. Photo: Wikimedia Commons."),
    },
    {
        "id": "SreBecomesRe",
        "title": "A company's own regex engine, begun in October 1999, still runs under re",
        "when": "1999-10-24",
        "who": "Secret Labs AB (contact info@pythonware.com)",
        "where": "Sweden, by way of Python's own _sre.c source history",
        "link": "https://chromium.googlesource.com/external/github.com/python/cpython/+/v3.7.0/Modules/_sre.c",
        "concepts": ["MatchObjectAccess"],
        "story": ("Python's _sre.c, the C source behind every Pattern and Match object the re module hands back, "
                   "carries a history log inside its own comments that opens on 24 October 1999, crediting the "
                   "initials 'fl' for most of the early engine and naming Secret Labs AB, reachable at "
                   "info@pythonware.com, as the copyright holder from 1997 to 2001. The same log records Hewlett-"
                   "Packard funding the work needed to fold the engine into Python 1.6, Martin von Loewis adding "
                   "support for wide character sets, and Guido van Rossum himself fixing a memory leak in sub() "
                   "and subn(). Every mo.group(), mo.span() and mo.start() this chapter calls on a Match object "
                   "reaches, underneath, into an engine whose own change log is now a quarter of a century old."),
        "lesson": "mo.group() and mo.span() reach a C engine logged from 24 October 1999",
        "source": ("Modules/_sre.c, CPython source history, chromium.googlesource.com (copyright Secret Labs AB "
                    "1997-2001, contact info@pythonware.com; history log from 1999-10-24); Python documentation, "
                    "re - Regular expression operations, the Match object. Photo: Wikimedia Commons."),
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
    if "1951" not in by["KleeneRegularEvents"]["story"] or "1951" not in by["KleeneRegularEvents"]["when"]:
        bad.append("KleeneRegularEvents: date missing from story")
    if "June 1968" not in by["ThompsonRegexSearch"]["story"] or "1968" not in by["ThompsonRegexSearch"]["when"]:
        bad.append("ThompsonRegexSearch: date missing from story")
    if "18 December 1987" not in by["PerlShorthandClasses"]["story"]:
        bad.append("PerlShorthandClasses: date missing from story")
    if "24 October 1999" not in by["SreBecomesRe"]["story"]:
        bad.append("SreBecomesRe: date missing from story")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
