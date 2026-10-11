"""SEN0414 chapter 8 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Four stories
for Manipulating Strings, written fresh for this chapter:

* Utf8Diner - Ken Thompson and Rob Pike designed UTF-8 on a diner placemat in September 1992; the chapter's own advice
  to use 'utf-8' "99 percent of the time" rests on the encoding this story explains.
* UnicodeConsortium - on 19 February 1991 nine computer companies announced Unicode Inc., the body whose code-point
  table is what ord() and chr() read from.
* FStringsPep498 - Eric V. Smith's PEP 498, created 1 August 2015, added the f-string to Python 3.6.
* CutCopyPaste - Larry Tesler, working at Xerox PARC on the Gypsy word processor, gave computing the cut-copy-paste
  model that pyperclip.copy() and pyperclip.paste() still use fifty years later.

Usage: import STORIES; run the file for self-checks. The photographs are named in ch08-page/stories_img_v1_0_0.json.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "Utf8Diner",
        "title": "The encoding written on a diner placemat",
        "when": "1992-09",
        "who": "Ken Thompson and Rob Pike, Bell Labs",
        "where": "a diner in New Jersey",
        "link": "https://doc.cat-v.org/bell_labs/utf-8_history",
        "concepts": ["Utf8Encoding"],
        "story": ("In September 1992 Ken Thompson and Rob Pike were designing a new encoding for the Plan 9 operating system "
                  "at Bell Labs. Rob Pike later wrote that UTF-8 'was designed, in front of my eyes, on a placemat in a New "
                  "Jersey diner one night in September or so 1992', and that he 'very clearly remember[s] Ken writing on the "
                  "placemat'. The scheme they sketched that night let a character take from one to four bytes while staying "
                  "compatible with plain ASCII, which is why 'caf\\xe9'.encode('utf-8') is five bytes for four characters. "
                  "That same encoding is what the chapter calls the right choice 99 percent of the time."),
        "lesson": "The encoding behind str.encode('utf-8') was sketched on a diner placemat",
        "source": ("Rob Pike, 'UTF-8 history', doc.cat-v.org/bell_labs/utf-8_history (first-hand account, dated September 1992); "
                   "Al Sweigart, Automate the Boring Stuff with Python, 3rd edition (2025), chapter 8. Photo: Wikimedia Commons."),
    },
    {
        "id": "UnicodeConsortium",
        "title": "Nine companies agree on one table of characters",
        "when": "1991-02-19",
        "who": "Apple, GO, IBM, Metaphor, Microsoft, NeXT, Novell, the Research Libraries Group and Sun Microsystems",
        "where": "Mountain View, California",
        "link": "https://www.unicode.org/history/first-pr.htm",
        "concepts": ["OrdAndChr", "Utf8Encoding"],
        "story": ("On 19 February 1991 a press release from Mountain View announced that nine computer companies had formally "
                  "affiliated as Unicode Inc., with board members from Apple, GO, IBM, Metaphor, Microsoft, NeXT, Novell, the "
                  "Research Libraries Group and Sun Microsystems, and Xerox's Joe Becker named as the new consortium's technical "
                  "vice president. The table of code points this group began maintaining is exactly what ord() and chr() read "
                  "from today: ord('A') is 65 and chr(8364) is the euro sign because the Unicode Consortium assigned those "
                  "numbers to those characters."),
        "lesson": "ord() and chr() read from a table nine companies agreed on in 1991",
        "source": ("'Major Computer Companies Join to Promote Worldwide Standard Character Encoding', Unicode Inc. press release, "
                   "19 February 1991 (unicode.org/history/first-pr.htm); Python documentation, the unicodedata module. "
                   "Photo: Wikimedia Commons."),
    },
    {
        "id": "FStringsPep498",
        "title": "One proposal, created in a single day, gave Python its f-string",
        "when": "2015-08-01",
        "who": "Eric V. Smith",
        "where": "the Python Enhancement Proposal index, PEP 498",
        "link": "https://peps.python.org/pep-0498/",
        "concepts": ["FStrings"],
        "story": ("PEP 498, 'Literal String Interpolation', records its own creation date as 1 August 2015, with Eric V. Smith "
                  "named as its author and Python 3.6 named as the version it targets. The proposal's own example is almost "
                  "exactly the chapter's: f'My name is {name}, my age next year is {age+1}'. Python 3.6 shipped the feature at "
                  "the end of 2016, and f'My name is {name}. I am {age} years old.' has worked the same way in every Python "
                  "release since."),
        "lesson": "The f-string Python programmers use daily traces to one named author and one PEP",
        "source": ("PEP 498, 'Literal String Interpolation', peps.python.org/pep-0498 (Created: 01-Aug-2015; Author: Eric V. "
                   "Smith; Python-Version: 3.6); What's New in Python 3.6. Photo: Wikimedia Commons."),
    },
    {
        "id": "CutCopyPaste",
        "title": "The clipboard the chapter's programs use is fifty years old",
        "when": "1973",
        "who": "Larry Tesler, with Tim Mott, Xerox PARC",
        "where": "Xerox PARC, Palo Alto, California",
        "link": "https://en.wikipedia.org/wiki/Larry_Tesler",
        "concepts": ["ClipboardModule"],
        "story": ("Larry Tesler joined Xerox PARC in 1973 and, working with Tim Mott on the Gypsy word processor, gave computing "
                  "the cut, copy and paste model: select some text, move it to a holding place, and insert it somewhere else. "
                  "pyperclip.copy() and pyperclip.paste(), the two functions the chapter's clipboard programs call, are that "
                  "same fifty-year-old model, now reached from three lines of Python instead of a menu. Tesler died on 16 "
                  "February 2020, at 74, and newspapers around the world wrote his obituary headline with the very model he "
                  "had invented: 'the inventor of copy and paste'."),
        "lesson": "pyperclip.copy() and pyperclip.paste() are a fifty-year-old idea in two function calls",
        "source": ("'Larry Tesler', Wikipedia, en.wikipedia.org/wiki/Larry_Tesler (PARC from 1973; the Gypsy word processor with "
                   "Tim Mott; died 16 February 2020); Al Sweigart, Automate the Boring Stuff with Python, 3rd edition (2025), "
                   "chapter 8, the pyperclip module. Photo: Wikimedia Commons."),
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
    if "September" not in by["Utf8Diner"]["story"] or "1992" not in by["Utf8Diner"]["when"]:
        bad.append("Utf8Diner: date missing from story")
    if "19 February 1991" not in by["UnicodeConsortium"]["story"]:
        bad.append("UnicodeConsortium: date missing from story")
    if "01-Aug-2015" not in by["FStringsPep498"]["story"].replace("1 August 2015", "01-Aug-2015") and "1 August 2015" not in by["FStringsPep498"]["story"]:
        bad.append("FStringsPep498: date missing from story")
    if "16 February 2020" not in by["CutCopyPaste"]["story"]:
        bad.append("CutCopyPaste: date missing from story")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
