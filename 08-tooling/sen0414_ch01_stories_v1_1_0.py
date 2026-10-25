"""SEN0414 chapter 1 - the story companion to the chapter corpus (version 1.1.0).

New file over 1.0.0, which stays as it is. The three stories are the three stories of the chapter 1 deck 4.0.0
(SEN0414_Ch01_PythonBasics_3e_v4_0_0.pptx; wording and facts in 08-tooling/ch01-deck/deck_content_v4_0_0.py), so the
page and the deck tell the same stories. Each follows 5N1K (who, what, when, where, why, how) with a dated, sourced
account and one live link; the facts rest on pages opened on 2026-10-25 and recorded in
03-materials/ch01/assets/ASSETS_PROVENANCE_v1_1_0.md:

* PythonBirth - Guido van Rossum, December 1989 at CWI, Monty Python, alt.sources, version 0.9.0 in February 1991.
* HelloWorldOrigin - Brian Kernighan, Bell Laboratories, 1972 (tutorial for the language B) and 1978 (The C Programming Language, page 6).
* LeibnizBinary - Gottfried Wilhelm Leibniz, binary arithmetic from 15 March 1679, Bouvet's letter of 1703, the paper printed in 1705.

Usage: import STORIES; run the file for self-checks. The photographs are named in ch01-page/stories_img_v2_0_0.json.
"""
__version__ = "1.1.0"

STORIES = [
    {
        "id": "PythonBirth",
        "title": "A Christmas hobby named after a comedy troupe",
        "when": "December 1989 to February 1991",
        "who": "Guido van Rossum, a programmer at the Centrum Wiskunde & Informatica (CWI)",
        "where": "At CWI in Amsterdam; the source code was posted to the alt.sources Usenet group",
        "link": "https://en.wikipedia.org/wiki/Guido_van_Rossum",
        "concepts": ["ExecutionEnvironment", "PythonImplementation"],
        "story": ("In the Christmas week of December 1989 the office at CWI in Amsterdam was closed, and Guido van Rossum, who worked there on the Amoeba project, "
                  "started a hobby scripting language, a descendant of ABC, that would be easier to read than shell scripts. "
                  "He named it after the British comedy troupe Monty Python, not after the snake. "
                  "He posted version 0.9.0 to the alt.sources newsgroup in February 1991. "
                  "Every prompt on these slides runs the grown-up descendant of that hobby."),
        "lesson": "The tool you are learning began as a one-week hobby",
        "source": ("Wikipedia, 'Guido van Rossum' and the history of Python (project begun December 1989 at CWI, name from Monty Python, 0.9.0 posted to alt.sources in "
                   "February 1991), opened 2026-10-25. Photo: Daniel Stroud, CC BY-SA 4.0, Wikimedia Commons."),
    },
    {
        "id": "HelloWorldOrigin",
        "title": "Where hello, world began, in 1972",
        "when": "1972, made famous by the 1978 book",
        "who": "Brian Kernighan, a researcher at Bell Laboratories",
        "where": "Bell Laboratories; page 6 of The C Programming Language (Prentice Hall, 1978)",
        "link": "https://en.wikipedia.org/wiki/%22Hello,_World!%22_program",
        "concepts": ["Output", "FunctionCall"],
        "story": ("In 1972 Brian Kernighan, at Bell Laboratories, wrote the first known program that puts the words hello and world together, as a teaching example in 'A Tutorial Introduction to the Language B'. "
                  "A beginner needs a first program that does one visible thing: print a greeting. "
                  "The language B held only four characters per constant, so the text had to sit in three variables. "
                  "The 1978 book 'The C Programming Language' by Kernighan and Ritchie made the greeting famous. "
                  "In Python the same program is one line."),
        "lesson": "A first program proves that write, run and see all work",
        "source": ("Wikipedia, '\"Hello, World!\" program' (Kernighan, 'A Tutorial Introduction to the Language B', Bell Laboratories, 1972; Kernighan and Ritchie, "
                   "'The C Programming Language', Prentice Hall, 1978, page 6), opened 2026-10-25. Photo: Ben Lowe, CC BY 2.0, Wikimedia Commons."),
    },
    {
        "id": "LeibnizBinary",
        "title": "Leibniz wrote every number with only 0 and 1",
        "when": "15 March 1679; letter of 1703; paper printed in 1705",
        "who": "Gottfried Wilhelm Leibniz, philosopher and mathematician, and the Jesuit Joachim Bouvet",
        "where": "The paper went to the Academie Royale des Sciences in Paris; Bouvet's letter came from Peking",
        "link": "https://historyofinformation.com/detail.php?id=395",
        "concepts": ["Integer", "Value"],
        "story": ("Leibniz first noted binary arithmetic on 15 March 1679: every number written with the two digits 0 and 1. "
                  "On 1 April 1703 a letter from the Jesuit Joachim Bouvet in Peking reached him and showed that the hexagrams of the Chinese I Ching are binary numbers. "
                  "Leibniz saw order in them and printed his paper 'Explication de l'arithmetique binaire' in 1705. "
                  "Every number is a sum of powers of two: 5 is 4 plus 1, written 101. "
                  "Computers store numbers this way."),
        "lesson": "Every number is a sum of powers of two",
        "source": ("historyofinformation.com, entry 395 (Leibniz's manuscript of 15 March 1679; Bouvet's letter written in Peking on 4 November 1701 and arriving on 1 April 1703; "
                   "'Explication de l'arithmetique binaire', Histoire de l'Academie Royale des Sciences, year 1703, printed 1705), opened 2026-10-25. "
                   "Painting: Christoph Bernhard Francke, before 1729, public domain, Wikimedia Commons."),
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
    if "December 1989" not in by["PythonBirth"]["story"] or "February 1991" not in by["PythonBirth"]["story"]:
        bad.append("PythonBirth: dates missing from story")
    if "1972" not in by["HelloWorldOrigin"]["story"] or "1978" not in by["HelloWorldOrigin"]["story"]:
        bad.append("HelloWorldOrigin: dates missing from story")
    if "15 March 1679" not in by["LeibnizBinary"]["story"] or "1705" not in by["LeibnizBinary"]["story"]:
        bad.append("LeibnizBinary: dates missing from story")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
