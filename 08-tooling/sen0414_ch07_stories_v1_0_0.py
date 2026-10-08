"""SEN0414 chapter 7 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Four stories for
Dictionaries and Structuring Data:

* DictOrderRuling - on 15 December 2017 Guido van Rossum settled in one sentence that a dictionary keeps insertion order,
  and the textbook's statement that dictionaries have no order stopped being true of the language.
* ChessNotation - the squares a1 to h8 that the chapter uses as keys come from an algebraic notation invented in the 1730s,
  described by Staunton in 1847 and made the only international notation by FIDE in 1981.
* BrightColdDay - the sentence that characterCount.py counts is the first sentence of Nineteen Eighty-Four, published on 8 June 1949.
* JsonBirth - the text notation that carries dictionaries between programs was first used in a message of April 2001.

Usage: import STORIES; run the file for self-checks. The photographs are named in ch07-page/stories_img_v1_0_0.json.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "DictOrderRuling",
        "title": "Five words that gave dictionaries an order",
        "when": "2017-12-15",
        "who": "Guido van Rossum, the creator of Python, on the python-dev mailing list",
        "where": "the python-dev mailing list - and the dictionary section of the Python documentation",
        "link": "https://mail.python.org/pipermail/python-dev/2017-December/151283.html",
        "concepts": ["InsertionOrder"],
        "story": ("Python 3.6, released in 2016, made dictionaries remember the order of insertion, but only as a detail of the CPython implementation. "
                  "Its new compact layout followed a proposal by Raymond Hettinger and the dictionary design of the PyPy interpreter, and it used 20 to 25 percent "
                  "less memory than Python 3.5. On 15 December 2017 Guido van Rossum settled the question for the whole language with "
                  "'Make it so. \"Dict keeps insertion order\" is the ruling. Thanks!' From Python 3.7 the language itself guarantees it. "
                  "The chapter's sentence that a dictionary has no first item is the one thing in it that this ruling overtook."),
        "lesson": "A dictionary now keeps insertion order, and programs may rely on it",
        "source": ("Guido van Rossum, message to python-dev, 15 December 2017 (mail.python.org/pipermail/python-dev/2017-December/151283.html); "
                   "What's New in Python 3.6, 'New dict implementation' (proposal by Raymond Hettinger, first implemented by PyPy; 20% to 25% less memory); "
                   "What's New in Python 3.7 and the Python documentation of mapping types (order is insertion order since 3.7). "
                   "Photo: Daniel Stroud, CC BY-SA 4.0, Wikimedia Commons."),
    },
    {
        "id": "ChessNotation",
        "title": "The squares a1 to h8 are three centuries old",
        "when": "1730s; 1847; 1981",
        "who": "Philipp Stamma, Howard Staunton and FIDE",
        "where": "the chess books of an eighteenth-century Syrian player, Staunton's London handbook, and the world chess federation",
        "link": "https://en.wikipedia.org/wiki/Algebraic_notation_(chess)",
        "concepts": ["ChessboardModel", "DataStructureModel"],
        "story": ("The dictionary keys 'a1' to 'h8' of the chessboard program are a data structure that chess players have used for almost three hundred years. "
                  "An early form of algebraic notation was devised by the Syrian player Philipp Stamma in the 1730s. "
                  "Howard Staunton described the system in his Chess-Player's Handbook in 1847, and German chess literature took it up in the nineteenth century. "
                  "English-language books preferred descriptive notation for most of the twentieth century, until in 1981 FIDE stopped recognising it and algebraic notation became the international standard. "
                  "The author's program simply turned an old notation into the keys of a Python dictionary."),
        "lesson": "A good data model is often a notation people already use",
        "source": ("'Algebraic notation (chess)', Wikipedia, citing Stamma (1737), Staunton, The Chess-Player's Handbook (1847) and the FIDE decision of 1981; "
                   "Al Sweigart, Automate the Boring Stuff with Python, 3rd edition (2025), chapter 7. Photo: Wilfredor, CC0, Wikimedia Commons."),
    },
    {
        "id": "BrightColdDay",
        "title": "The sentence the character counter counts",
        "when": "1949-06-08",
        "who": "George Orwell, published by Secker and Warburg",
        "where": "London - the opening line of Nineteen Eighty-Four",
        "link": "https://en.wikipedia.org/wiki/Nineteen_Eighty-Four",
        "concepts": ["CharacterCount", "CounterClass"],
        "story": ("The message in characterCount.py, 'It was a bright cold day in April, and the clocks were striking thirteen.', is the opening line of "
                  "George Orwell's novel Nineteen Eighty-Four, which Secker and Warburg published in London on 8 June 1949. "
                  "Counting its 73 characters with a dictionary gives 23 different characters, 13 spaces and 3 letters c. "
                  "The same table shows 6 letters t and one capital A, and the thirteen strokes of the clocks are what tells the reader at once that this world is wrong. "
                  "The same few lines count the words of a whole novel."),
        "lesson": "Counting by key turns any text into a table of totals",
        "source": ("George Orwell, Nineteen Eighty-Four (Secker and Warburg, London, 8 June 1949), first sentence; Al Sweigart, Automate the Boring Stuff with Python, "
                   "3rd edition (2025), chapter 7, characterCount.py. The counts are the output of the executed program of this chapter. "
                   "Photo: Branch of the National Union of Journalists (1943), public domain, Wikimedia Commons."),
    },
    {
        "id": "JsonBirth",
        "title": "The first message in the notation that carries dictionaries",
        "when": "2001-04; 2017-12-13",
        "who": "Douglas Crockford and Chip Morningstar, State Software",
        "where": "California - and json.org and the IETF's RFC 8259",
        "link": "https://www.json.org/json-en.html",
        "concepts": ["JsonText"],
        "story": ("A dictionary exists only while its program runs, so something must carry it to another program. "
                  "Douglas Crockford, who co-founded State Software in March 2001, and Chip Morningstar sent the first JSON message in April 2001, "
                  "and json.org began in 2001 to describe the format. "
                  "Yahoo offered some of its web services in JSON in December 2005. "
                  "The IETF published JSON as RFC 8259, an Internet Standard, on 13 December 2017, two days before the Python ruling on dictionary order. "
                  "Python's json module turns a dictionary into that text and back."),
        "lesson": "JSON is how a dictionary leaves the program and comes back",
        "source": ("'JSON', Wikipedia (first message April 2001; State Software founded March 2001; Yahoo, December 2005; RFC 8259, 13 December 2017); json.org; "
                   "the Python json module documentation. Photo: Robert Claypool, CC0, Wikimedia Commons."),
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
    if "2017-12-15" not in by["DictOrderRuling"]["when"] or "15 December 2017" not in by["DictOrderRuling"]["source"]:
        bad.append("DictOrderRuling: date drifted")
    if "1981" not in by["ChessNotation"]["story"] or "1847" not in by["ChessNotation"]["story"]:
        bad.append("ChessNotation: date missing from story")
    if "8 June 1949" not in by["BrightColdDay"]["story"]:
        bad.append("BrightColdDay: date missing from story")
    if "RFC 8259" not in by["JsonBirth"]["source"] and "RFC 8259" not in by["JsonBirth"]["story"]:
        bad.append("JsonBirth: RFC missing")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
